from os import path
import pandas as pd
import plotive as pv

csv_file = path.join(path.dirname(path.abspath(__file__)), "Iris.csv")
df = pd.read_csv(csv_file, index_col="Id")

data = {
    "setosa_sepal_length": df.loc[df["Species"] == "Iris-setosa", "SepalLengthCm"].values,
    "setosa_petal_length": df.loc[df["Species"] == "Iris-setosa", "PetalLengthCm"].values,
    "versicolor_sepal_length": df.loc[df["Species"] == "Iris-versicolor", "SepalLengthCm"].values,
    "versicolor_petal_length": df.loc[df["Species"] == "Iris-versicolor", "PetalLengthCm"].values,
    "virginica_sepal_length": df.loc[df["Species"] == "Iris-virginica", "SepalLengthCm"].values,
    "virginica_petal_length": df.loc[df["Species"] == "Iris-virginica", "PetalLengthCm"].values,
}

fig = pv.Figure(
    title="Iris dataset",
    plot=pv.Plot(
        series=[
            pv.series.Scatter(
                x="setosa_sepal_length",
                y="setosa_petal_length",
                name="Setosa",
            ),
            pv.series.Scatter(
                x="versicolor_sepal_length",
                y="versicolor_petal_length",
                name="Versicolor",
            ),
            pv.series.Scatter(
                x="virginica_sepal_length",
                y="virginica_petal_length",
                name="Virginica",
            ),
        ],
        x_axis=pv.Axis(title="Sepal Length [cm]", ticks="auto", grid="auto"),
        y_axis=pv.Axis(title="Petal Length [cm]", ticks="auto", grid="auto"),
        legend="in-bottom-right",
    ),
)

import _common
_common.process_figure(fig, data, "iris")

