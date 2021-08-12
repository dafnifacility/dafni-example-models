from io import StringIO
import numpy as np
import pandas as pd
from pandas.core.frame import DataFrame
from pyspark.context import SparkContext
from pyspark.sql import SparkSession
from typing import Tuple
import os
from post_processing import define_months, define_threshold, get_prediction_data
from shutil import copyfile
import zipfile

OUTPUT_FOLDER = "/data/outputs/"
INPUT_FOLDER = "/data/inputs/"


def setup_spark() -> SparkContext:
    # Start Spark sesssion
    spark = (
        SparkSession.builder.appName("climateChange")
        .config("spark.driver.memory", "8g")
        .getOrCreate()
    )
    return spark.sparkContext


def process_file(tup: Tuple, feature: str):
    # Convert tuples to strings and load them into Pandas dataframe
    tuple_string = "".join(tup[0:2])
    df = pd.read_csv(StringIO(tuple_string), header=None)

    # Slice the output and store filename in "filename dataframe"
    filename = df[0:1]
    filename = filename.iloc[0][0].replace("txtncols         180", "")

    # For daily data, the range is -9 to -1
    if feature == "rainfall" or feature == "maximum-temperature":
        last_underscore = filename.rfind("_")
        filename = filename[last_underscore + 1 : -1]
        if len(filename) == 6:
            filename += "01"

    # For monthly data, the range is -7 to -1
    elif feature == "sunshine" or feature == "snow-falling":
        filename = filename[-7:-1]

    # Store the content of file in "content dataframe"
    content = df[6:]

    # Iterate through all the rows and columns of the file
    mod_pandas_df = (
        content.iloc[:, 0].str.split(" ", expand=True).replace("-9999", float("NaN"))
    )
    mod_pandas_df = mod_pandas_df.astype("float")
    mod_pandas_df = mod_pandas_df.values
    xDF = np.nanmean(mod_pandas_df)
    mean = np.nanmean(xDF)

    return filename, mean


def read_files(feature: str, spark_context: SparkContext):
    path = f"{INPUT_FOLDER}{feature}/"
    unzip_inputs(path)

    # Get Resilient Distributed Dataset containing one record for each file.
    files_rdd = spark_context.wholeTextFiles(path + "*", minPartitions=20)
    print("Number of records:", files_rdd.count())

    # Map lines to words
    records = files_rdd.map(lambda n: process_file(n, feature))

    # Transform the RDD into a list
    rdd_list = records.collect()

    # Two arrays
    values = []
    months = []

    # Store the filename in months array and its corrosponding value(mean) in values array
    for line in rdd_list:
        values.append(line[1])
        months.append(line[0])

    # Convert arrays to dataframes
    values_df = pd.DataFrame({"Values": values[:]})
    year_month_df = pd.DataFrame({"YearMonth": months[:]})

    # Merge two dataframes into one
    final_df = pd.merge(year_month_df, values_df, left_index=True, right_index=True)

    # Sort the index
    final_df = final_df.sort_values("YearMonth")

    # Convert first column to integer format
    final_df["YearMonth"] = final_df["YearMonth"].astype("int")

    # Convert first column of daily data from integer to datetime format
    if feature == "rainfall" or feature == "maximum-temperature":
        final_df["YearMonth"] = pd.to_datetime(
            final_df["YearMonth"].astype(str), format="%Y%m%d"
        )

    # Convert first column of monthly data from integer to datetime format
    elif feature == "sunshine" or feature == "snow-falling":
        final_df["YearMonth"] = pd.to_datetime(
            final_df["YearMonth"].astype(str), format="%Y%m"
        )

    # Extract year and month
    final_df["Year"] = final_df["YearMonth"].dt.year
    final_df["Month"] = final_df["YearMonth"].dt.month

    return final_df


def do_post_processing(df: DataFrame, feature: str):
    season = os.getenv("SEASON", "summer").lower()
    month_definition_df = define_months(df, season)
    threshold_df = define_threshold(month_definition_df, season, feature)

    prediction_data = get_prediction_data(threshold_df, feature)

    df.to_csv(f"{feature}-base.csv", index=False)
    prediction_data.to_csv(f"{feature}-prediction.csv", index=False)


def process_selected_types(spark_context: SparkContext):
    processing_types = ["rainfall", "maximum-temperature", "sunshine", "snow-falling"]

    for processing_type in processing_types:
        processing_env = processing_type.upper().replace("-", "_")
        process_string = os.getenv(f"PROCESS_{processing_env}", "false")
        if process_string.lower() in ["true", "t"]:
            print(f"Processing data for {processing_type}")
            df = read_files(processing_type, spark_context)
            do_post_processing(df, processing_type)


def move_output_files_to_folder():
    for file in os.listdir("./"):
        if file.endswith(".csv"):
            copyfile(file, OUTPUT_FOLDER + file)


def unzip_inputs(path: str):
    for file in os.listdir(path):
        if file.endswith("zip"):
            zip_file_loc = os.path.join(path, file)
            with zipfile.ZipFile(zip_file_loc, "r") as zip_ref:
                zip_ref.extractall(path)
                os.remove(zip_file_loc)


if __name__ == "__main__":
    if not os.path.exists(OUTPUT_FOLDER):
        os.makedirs(OUTPUT_FOLDER)
    spark_context = setup_spark()
    process_selected_types(spark_context)
    move_output_files_to_folder()
