import plotive as pv

fig = pv.Figure(
    title="Minimal Figure",
    plot=pv.Plot(
        series=[
            pv.series.Line(
                x="x",
                y="y",
            ),
        ],
    ),
)

data = {
    "x": [1.0, 2.0, 3.0],
    "y": [3.0, 1.0, 2.0],
}

import _common

_common.process_figure(fig, data, "minimal")
