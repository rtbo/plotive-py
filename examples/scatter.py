import numpy as np
import plotive as pv


data = {
    "x1": np.random.normal(loc=30, scale=5, size=300),
    "y1": np.random.normal(loc=20, scale=2, size=300),
    "x2": np.random.normal(loc=40, scale=2, size=500),
    "y2": np.random.normal(loc=10, scale=5, size=500),
}

fig = pv.Figure(
    title="Scatter Plot Example",
    plot=pv.Plot(
        series=[
            pv.series.Scatter(
                x="x1",
                y="y1",
                name="Series 1",
                marker=pv.style.Marker(shape="circle", size=3),
            ),
            pv.series.Scatter(
                x="x2",
                y="y2",
                name="Series 2",
                marker=pv.style.Marker(shape="square", size=3),
            ),
        ],
        x_axis=pv.Axis(ticks="auto", grid="auto"),
        y_axis=pv.Axis(ticks="auto", grid="auto"),
    ),
    legend=pv.Legend("bottom"),
)

import _common
_common.process_figure(fig, data)
