import numpy as np
import plotive as pv
import _common

np.random.seed(1234)

NUM = 50

x = np.random.uniform(0, 10, NUM)
y = np.random.uniform(0, 10, NUM)
sizes = np.random.uniform(0.5, 20, NUM)
colors = np.linspace(10, 20, NUM)

axis = pv.Axis(scale=(-0.3, 10.3), ticks="auto", grid="auto")

fig = pv.Figure(
    plot=pv.Plot(
        series=pv.series.Scatter(
            x=x,
            y=y,
            sizes=sizes,
            colors=colors,
            # uses the default "viridis" colormap
        ),
        x_axis=axis,
        y_axis=axis,
        colorbar="auto",
    ),
)

_common.process_figure(fig, {}, "colormap")
