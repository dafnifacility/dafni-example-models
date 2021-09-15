import itertools
import numpy as np
import pandas as pd
import os
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt
import statsmodels.api as sm
from statsmodels.tsa.base.tsa_model import ValueWarning
from statsmodels.tools.sm_exceptions import ConvergenceWarning
import warnings

warnings.simplefilter("ignore", category=ValueWarning)
warnings.simplefilter("ignore", category=ConvergenceWarning)
plt.style.use("fivethirtyeight")
fig = plt.figure(figsize=(40, 10))


def plot_trend(df, feature):
    plt.plot(df.YearMonth, df.Values)

    if feature == "rainfall":
        plt.title("Daily Rainfall in UK (1960 - 2016)")
        plt.ylabel("Rainfall (mm)")

    if feature == "maximum-temperature":
        plt.title("Daily Max Temperature of UK (1960 - 2016)")
        plt.ylabel("Temperature")

    if feature == "sunshine":
        plt.title("Monthly Sunshine in UK (1929 - 2016)")
        plt.ylabel("Number of Hours")

    if feature == "snow-falling":
        plt.title("Monthly Snowfall in UK (1971 - 2011)")
        plt.ylabel("Number of Days")

    plt.xlabel("Date")
    plt.xticks(np.arange(0, len(df.YearMonth), 365), rotation="vertical", fontsize=8)
    plt.show()


def plot_best_fit_line(df, feature):
    y_values = df["Values"]

    # create a set of intervals equal to the number of dates
    x_values = np.linspace(0, 1, len(df.loc[:, "Values"]))
    poly_degree = 3

    coeffs = np.polyfit(x_values, y_values, poly_degree)
    poly_eqn = np.poly1d(coeffs)
    y_hat = poly_eqn(x_values)

    if feature == "rainfall":
        plt.title("Daily Rainfall in UK (1910 - 2016)")
        plt.ylabel("Rainfall (mm)")

    if feature == "maximum-temperature":
        plt.title("Daily Max Temperature of UK (1960 - 2016)")
        plt.ylabel("Temperature")

    if feature == "sunshine":
        plt.title("Monthly Sunshine in UK (1929 - 2016)")
        plt.ylabel("Number of Hours")

    if feature == "snow-falling":
        plt.title("Monthly Snowfall in UK (1971 - 2011)")
        plt.ylabel("Number of Days")

    plt.xlabel("Date")
    plt.xticks(np.arange(0, len(df.YearMonth), 365), rotation="vertical", fontsize=8)

    plt.plot(df.loc[:, "YearMonth"], df.loc[:, "Values"], "ro")
    plt.plot(df.loc[:, "YearMonth"], y_hat)


def prediction(prediction_df, feature, season):
    prediction_df = prediction_df.astype({"Values": float})
    prediction_df.to_csv("PredictionData.csv", index=False)

    if feature == "rainfall" or feature == "maximum-temperature":
        df = pd.read_csv("PredictionData.csv", index_col="YearMonth")

    if feature == "snow-falling" or feature == "sunshine":
        df = pd.read_csv("PredictionData.csv", index_col="Year")

    df.index = pd.to_datetime(df.index, format="%Y")

    p = d = q = range(0, 2)
    pdq = list(itertools.product(p, d, q))

    # set seasonal parameter = 12
    if (
        feature == "rainfall"
        or feature == "maximum-temperature"
        or feature == "sunshine"
    ):
        seasonal_pdq = [
            (x[0], x[1], x[2], 12) for x in list(itertools.product(p, d, q))
        ]

    # set seasonal parameter = 3
    if feature == "snow-falling":
        seasonal_pdq = [(x[0], x[1], x[2], 3) for x in list(itertools.product(p, d, q))]

    # goal here is to use a “grid search” to find the optimal set of parameters(p, d, q) that yields the best performance for our model.
    param_min = 0
    param_seasonal_min = 0
    results_min = 10000
    for param in pdq:
        for param_seasonal in seasonal_pdq:
            mod = sm.tsa.statespace.SARIMAX(
                df,
                order=param,
                seasonal_order=param_seasonal,
                enforce_stationarity=False,
                enforce_invertibility=False,
            )
            results = mod.fit(
                disp=0, method_kwargs={"warn_convergence": False, "warn_value": False}
            )

            if results.aic < results_min:
                param_min = param
                param_seasonal_min = param_seasonal
                results_min = results.aic

    # fitting the arima model
    mod = sm.tsa.statespace.SARIMAX(
        df,
        order=param_min,
        seasonal_order=param_seasonal_min,
        enforce_stationarity=False,
        enforce_invertibility=False,
    )
    results = mod.fit(
        disp=0, method_kwargs={"warn_convergence": False, "warn_value": False}
    )

    # validating forecasts from 2000 to the end date
    if (
        feature == "rainfall"
        or feature == "maximum-temperature"
        or feature == "sunshine"
    ):
        pred = results.get_prediction(start=pd.to_datetime("2000-01-01"), dynamic=False)

    # validating forecasts from 2005 to the end date
    if feature == "snow-falling":
        pred = results.get_prediction(start=pd.to_datetime("2005-01-01"), dynamic=False)

    pred_ci = pred.conf_int()

    if feature == "rainfall" or feature == "maximum-temperature":
        ax = df["1960":].plot(label="Observed")

    if feature == "sunshine":
        ax = df["1960":].plot(label="Observed")

    if feature == "snow-falling":
        ax = df["1971":].plot(label="Observed")

    pred.predicted_mean.plot(
        ax=ax, label="One-step ahead Forecast", alpha=0.7, figsize=(14, 7)
    )

    ax.fill_between(
        pred_ci.index, pred_ci.iloc[:, 0], pred_ci.iloc[:, 1], color="k", alpha=0.2
    )

    if feature == "rainfall" or feature == "maximum-temperature":
        plt.title("Training from 1960 to 2016, Testing from 2000 to 2016")
        ax.set_ylabel("Number of Days")

    if feature == "snow-falling":
        plt.title("Training from 1971 to 2011, Testing from 2005 to 2011")
        ax.set_ylabel("Number of Days")

    if feature == "sunshine":
        plt.title("Training from 1960 to 2016, Testing from 2000 to 2016")
        ax.set_ylabel("Number of Hours")

    ax.set_xlabel("Year")
    plt.legend()
    plt.show()

    if (
        feature == "rainfall"
        or feature == "maximum-temperature"
        or feature == "sunshine"
    ):
        # validating forecasts from 2000 to the end date
        pred = results.get_prediction(start=pd.to_datetime("2000-01-01"), dynamic=False)

    if feature == "snow-falling":
        # validating forecasts from 2005 to the end date
        pred = results.get_prediction(start=pd.to_datetime("2005-01-01"), dynamic=False)

    pred_ci = pred.conf_int()

    if feature == "rainfall" or feature == "maximum-temperature":
        ax = df["1960":"2000"].plot(label="Observed")

    if feature == "sunshine":
        ax = df["1960":"2000"].plot(label="Observed")

    if feature == "snow-falling":
        ax = df["1971":"2005"].plot(label="Observed")

    pred.predicted_mean.plot(
        ax=ax, label="One-step ahead Forecast", alpha=0.7, figsize=(14, 7)
    )

    ax.fill_between(
        pred_ci.index, pred_ci.iloc[:, 0], pred_ci.iloc[:, 1], color="k", alpha=0.2
    )

    if feature == "rainfall" or feature == "maximum-temperature":
        plt.title("Training from 1960 to 2000, Testing from 2000 to 2016")
        ax.set_ylabel("Number of Days")

    if feature == "sunshine":
        plt.title("Training from 1960 to 2000, Testing from 2000 to 2016")
        ax.set_ylabel("Number of Hours")

    if feature == "snow-falling":
        plt.title("Training from 1971 to 2005, Testing from 2005 to 2011")
        ax.set_ylabel("Number of Days")

    ax.set_xlabel("Year")
    plt.legend()
    plt.show()

    # Compute the root-mean-square
    y_forecasted = pred.predicted_mean
    y_forecasted = y_forecasted.to_frame()

    if (
        feature == "rainfall"
        or feature == "maximum-temperature"
        or feature == "sunshine"
    ):
        y_truth = df["2000-01-01":]

    if feature == "snow-falling":
        y_truth = df["2005-01-01":]

    y_forecasted.columns = ["Values"]
    y_forecasted.index.names = ["Year"]

    rms = np.sqrt(mean_squared_error(y_forecasted, y_truth))
    print("The Root Mean Squared Error of our forecasts is:", rms)

    # Get forecast 50 steps ahead in future
    pred_uc = results.get_forecast(steps=50)

    # Get confidence intervals of forecasts
    pred_ci = pred_uc.conf_int()

    ax = df.plot(label="Observed", figsize=(14, 7))
    pred_uc.predicted_mean.plot(ax=ax, label="Forecast")
    ax.fill_between(
        pred_ci.index, pred_ci.iloc[:, 0], pred_ci.iloc[:, 1], color="k", alpha=0.25
    )

    if (
        feature == "rainfall"
        or feature == "maximum-temperature"
        or feature == "snow-falling"
    ):
        plt.title("Forecast for " + feature + " in " + season)
        ax.set_ylabel("Number of Days")

    if feature == "sunshine":
        plt.title("Forecast for " + feature)
        ax.set_ylabel("Number of Hours")

    ax.set_xlabel("Year")
    plt.legend()
    plt.show()


def get_output_folder():
    folder = os.listdir("./data/")[0]
    return f"/home/jovyan/data/{folder}"


for feature_type in ["rainfall", "maximum-temperature", "snow-falling"]:
    output_folder = get_output_folder()
    base_df = pd.read_csv(f"{output_folder}/{feature_type}-base.csv")
    prediction_df = pd.read_csv(f"{output_folder}/{feature_type}-prediction.csv")
    plot_trend(base_df, feature_type)
    plot_best_fit_line(base_df, feature_type)
    prediction(prediction_df, feature_type, "summer")
