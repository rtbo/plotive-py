from os import path
import pandas as pd
import plotive as pv

csv_file = path.join(path.dirname(path.abspath(__file__)), "Iris.csv")
df = pd.read_csv(csv_file, index_col="Id")

data = {
    "setosa_sep_len": df.loc[df["Species"] == "Iris-setosa", "SepalLengthCm"].values,
    "setosa_sep_wid": df.loc[df["Species"] == "Iris-setosa", "SepalWidthCm"].values,
    "versicolor_sep_len": df.loc[
        df["Species"] == "Iris-versicolor", "SepalLengthCm"
    ].values,
    "versicolor_sep_wid": df.loc[
        df["Species"] == "Iris-versicolor", "SepalWidthCm"
    ].values,
    "virginica_sep_len": df.loc[
        df["Species"] == "Iris-virginica", "SepalLengthCm"
    ].values,
    "virginica_sep_wid": df.loc[
        df["Species"] == "Iris-virginica", "SepalWidthCm"
    ].values,
}

fig = pv.Figure(
    title="Iris dataset",
    plot=pv.Plot(
        series=[
            pv.series.Scatter(
                x="setosa_sep_len",
                y="setosa_sep_wid",
                name="Setosa",
            ),
            pv.series.Scatter(
                x="versicolor_sep_len",
                y="versicolor_sep_wid",
                name="Versicolor",
            ),
            pv.series.Scatter(
                x="virginica_sep_len",
                y="virginica_sep_wid",
                name="Virginica",
            ),
        ],
        x_axis=pv.Axis(title="Sepal Length [cm]", ticks="auto", grid="auto"),
        y_axis=pv.Axis(title="Sepal Width [cm]", ticks="auto", grid="auto"),
    ),
    legend="right",
)

import _common

_common.process_figure(fig, data, "iris")
