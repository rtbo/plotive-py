import numpy as np
import plotive as pv

x = np.linspace(0.0, np.pi, 500)
data = {
    "x": x,
    "y1": np.sin(x) - 0.8 * np.pow(np.sin(x), 2),
    "y2": 100.0 * np.cos(x - np.pi/4),
    "y3": 1000.0 * np.sin(x),
}

fig = pv.Figure(
    plot=pv.Plot(
        series=[
            pv.series.Line(
                x="x",
                y="y1",
                name="y1 = sin(x) - 0.8*sin(x)^2",
            ),
            pv.series.Line(
                x="x",
                y="y2",
                name="y2 = 100 * cos(x - π)",
                # reference the second y-axis by its id
                y_axis="y2",
            ),
            pv.series.Line(
                x="x",
                y="y3",
                name="y3 = 1000*sin(x)",
                # reference the third y-axis by its title
                y_axis="Y3",
            ),
        ],
        x_axis=pv.Axis(title="X", ticks="pimultiple"),
        y_axes=[
            pv.Axis(title="Y1", ticks="percent"),
            pv.Axis(id="y2", title="Y2", ticks="auto", side="right"),
            pv.Axis(title="Y3", ticks="auto", side="right"),
        ],
    ),
    legend="bottom",
)

import _common
_common.process_figure(fig, data, "multiple-axes")

