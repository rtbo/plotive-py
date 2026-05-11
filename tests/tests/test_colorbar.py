import plotive as pv
import numpy as np

from . import *

def test_colorbar_auto():
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


def test_colorbar_stellar_ticks():
    rnd = NotRandom()
    x = rnd.make_col_uniform(15)
    y = rnd.make_col_uniform(15)
    colors = np.linspace(1000, 15000, 15)
    print(colors)

    series = pv.series.Scatter(
        x=x,
        y=y,
        colors=colors,
        cmap="stellar",
        marker=pv.style.SeriesMarker(size=16**2),
    )
    plot = pv.Plot(series, colorbar=pv.ColorBar(ticks=pv.STELLAR_TICKS))
    assert_fig_eq_ref(fig_small(plot), "colorbar/stellar-ticks")
