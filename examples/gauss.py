import numpy as np
import plotive as pv

MU = 13.0
SIGMA = 2.0
X_MIN = MU - 4.0 * SIGMA
X_MAX = MU + 4.0 * SIGMA

x = np.linspace(X_MIN, X_MAX, 100)
y = 1.0 / (SIGMA * (2.0 * np.pi) ** 0.5) * np.exp(-0.5 * ((x - MU) / SIGMA) ** 2)
data = {"x": x, "y": y, "pop": np.random.normal(MU, SIGMA, 1000)}

fig = pv.Figure(
    title=[
        "Normal distribution",
        f"[size=16]\u03bc={MU}, \u03c3={SIGMA}[/size]",
    ],
    plot=pv.Plot(
        series=[
            pv.series.Line(
                x="x",
                y="y",
                name="Distribution",
                stroke=pv.Stroke(width=4.0),
            ),
            pv.series.Histogram(
                x="pop",
                name="Population",
                fill=pv.Fill(color="auto", opacity=0.7),
                bins=16,
                density=True,
            ),
        ],
        x_axis=pv.Axis(
            title="x",
            ticks=[5, 9, 11, 13, 15, 17, 21],
        ),
        y_axis=pv.Axis(
            title="y",
            ticks="percent",
        ),
        legend="out-right",
    ),
)

import _common

_common.process_figure(fig, data, "gauss")
