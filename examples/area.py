import plotive as pv

data = {
    "x": [0.0, 1.0, 2.0, 3.0, 4.0, 5.0],
    "y1": [10.0, 15.0, 8.0, 6.0, 12.0, 10.0],
    "y2": [4.0, 9.0, 2.0, 0.0, 6.0, 4.0],
}

fig = pv.Figure(
    plot=pv.Plot(
        series=[
            pv.series.Area(
                x="x",
                y1="y1",
                y2="y2",
            ),
            pv.series.Area(
                x="x",
                y1="y2",
            ),
        ]
    )
)

import _common

_common.process_figure(fig, data, "area")
