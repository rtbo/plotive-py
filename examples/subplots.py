import numpy as np
import plotive as pv

x1 = np.linspace(0.0, 2.0 * np.pi, 400)
y1 = np.sin(x1 * x1)
x2 = np.linspace(0.5 * np.pi, 2.5 * np.pi, 400)
y2 = -np.sin(x2 * x2)

data = {
    "x1": x1,
    "y1": y1,
    "x2": x2,
    "y2": y2,
}

fig = pv.Figure(
    space=10.0,
    size=(800, 900),
    plots=[
        pv.Plot(
            series=[
                pv.series.Line(
                    x="x1",
                    y="y1",
                )
            ],
            x_axis=pv.Axis(
                grid="auto",
                scale="x2",
            ),
        ),
        pv.Plot(
            series=[
                pv.series.Line(
                    x="x2",
                    y="y2",
                )
            ],
            x_axis=pv.Axis(
                id="x2",
                ticks="pimultiple",
                grid="auto",
            ),
        )
    ]
)

import _common
_common.process_figure(fig, data, "subplots")

