import plotive as pv

from . import *


def test_cmap_default():
    rnd = NotRandom()
    x = rnd.make_col_uniform(15)
    y = rnd.make_col_uniform(15)
    colors = [float(i) / 14 for i in range(15)]

    series = pv.series.Scatter(
        x=x,
        y=y,
        colors=colors,
        marker=pv.style.SeriesMarker(size=16**2),
    )
    plot = pv.Plot(series, colorbar="auto")
    assert_fig_eq_ref(fig_small(plot), "cmap/default")


def test_cmap_viridis():
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
    assert_fig_eq_ref(fig_small(plot), "cmap/default")


def test_cmap_stellar():
    rnd = NotRandom(1234)
    colors = [1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 10000, 11000, 12000, 13000, 14000, 15000]
    x = rnd.make_col_uniform(len(colors))
    y = rnd.make_col_uniform(len(colors))

    series = pv.series.Scatter(
        x=x,
        y=y,
        colors=colors,
        cmap="stellar",
        marker=pv.style.SeriesMarker(size=16**2),
    )
    plot = pv.Plot(series)
    assert_fig_eq_ref(fig_small(plot), "cmap/stellar")

def test_cmap_stellar_noscale():
    rnd = NotRandom(1234)
    colors = [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0, 11.0, 12.0, 13.0, 14.0, 15.0]
    x = rnd.make_col_uniform(len(colors))
    y = rnd.make_col_uniform(len(colors))

    series = pv.series.Scatter(
        x=x,
        y=y,
        colors=colors,
        cmap=pv.series.ColorMap("stellar", scale=None),
        marker=pv.style.SeriesMarker(size=16**2),
    )
    plot = pv.Plot(series)
    assert_fig_eq_ref(fig_small(plot), "cmap/stellar")
