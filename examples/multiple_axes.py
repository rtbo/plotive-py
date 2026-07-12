import numpy as np
import plotive as pv

x = np.linspace(0.0, 6.0 * np.pi, 500)
data = {
    "x": x,
    "sin(x)": np.sin(x),
    "exp(x)": np.exp(x),
}

fig = pv.Figure(
    title="Multiple Axes",
    plot=pv.Plot(
        border="arrow",
        series=[
            pv.series.Line(
                x="x",
                y="sin(x)",
            ),
            pv.series.Line(
                x="x",
                y="exp(x)",
                # reference the second y-axis
                # using the title of the axis also works
                y_axis="y2",
            ),
        ],
        x_axis=pv.Axis(title="x", ticks="pimultiple"),
        y_axes=[
            pv.Axis(title="sin(x)", ticks="auto"),
            pv.Axis(id="y2", title="exp(x)", scale="log", ticks="auto"),
        ],
    ),
)

import _common
_common.process_figure(fig, data, "multiple-axes")

