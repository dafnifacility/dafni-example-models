from pandas import DataFrame
import pandas as pd


def define_months(df: DataFrame, season: str) -> DataFrame:
    if season == "winter":
        month_df = df.loc[df["Month"].isin([1, 2, 12])]
    if season == "summer":
        month_df = df.loc[df["Month"].isin([6, 7, 8])]
    if season == None:
        month_df = df.loc[df["Month"].isin([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12])]
    return month_df


def define_threshold(df: DataFrame, season: str, feature: str) -> DataFrame:
    if feature == "sunshine" or feature == "snow-falling":
        return df
    if season == "winter":
        return df.loc[(df["Values"] >= 10)]
    if season == "summer" and feature == "rainfall":
        return df.loc[(df["Values"] <= 1)]
    if season == "summer" and feature == "maximum-temperature":
        return df.loc[(df["Values"] >= 18)]
    return df


def get_prediction_data(df: DataFrame, feature: str) -> DataFrame:
    # count number of days in a year for daily data
    if feature in ["rainfall", "maximum-temperature"]:
        df = df.drop(["Year", "Month"], axis=1)

        # count the rows grouped by year
        count = (
            df["YearMonth"].groupby([df.YearMonth.dt.year]).agg({"count"}).reset_index()
        )

        df = pd.DataFrame(count)
        df.columns = ["YearMonth", "Values"]
        temp = 0

        # if the dataframe has missing years, add that year and assign 0 as its corresponding value
        for _ in range(10):
            for i in range(df.shape[0]):
                if i == 0:
                    temp = df.iloc[0][0]
                if df.iloc[i][0] != (temp + i):
                    df = df.append({"YearMonth": i + temp}, {"Values": 0.0})
                    df = df.sort_values("YearMonth")

        df = df.replace(float("NaN"), 0)
        df["YearMonth"] = df["YearMonth"].astype(int)
        return df

    # calculate the sum of the values for monthly data
    else:
        # calculate the sum of rows and group them by year
        df = df.groupby(["Year"])["Values"].agg("sum").reset_index()
        return df
