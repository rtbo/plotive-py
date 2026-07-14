import plotive as pv
import numpy as np

fig = pv.Figure(
    title="Sine Wave",
    plot=pv.Plot(
        series=[
            pv.series.Line(
                x="x",
                y="y",
                name="y=sin(x)",
            )
        ],
        x_axis=pv.Axis(title="x", ticks="pimultiple", grid="auto"),
        y_axis=pv.Axis(title="sin(x)", ticks="auto", grid="auto"),
        legend="in-top-right",
    ),
)

x = np.linspace(0, 2 * np.pi, 500)
y = np.sin(x)

import _common
_common.process_figure(fig, {"x": x, "y": y}, "sine")

