import plotive as pv

from . import *


def test_series_scatter_colors():
    rnd = NotRandom()
    x = rnd.make_col_uniform(15)
    y = rnd.make_col_uniform(15)
    colors = [float(i) / 14 for i in range(15)]

    series = pv.series.Scatter(
        x=x,
        y=y,
        colors=colors,
        cmap="viridis",
        marker=pv.style.SeriesMarker(size=16**2),
    )
    plot = pv.Plot(series, colorbar="auto")
    assert_fig_eq_ref(fig_small(plot), "colorbar/auto")
