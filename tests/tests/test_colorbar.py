import plotive as pv
import numpy as np

from . import *


def test_colorbar_pos():
    rnd = NotRandom()
    x = rnd.make_col_uniform(15)
    y = rnd.make_col_uniform(15)
    colors = [float(i) / 14 for i in range(15)]

    series = pv.series.Scatter(
        x=x,
        y=y,
        colors=colors,
        cmap="viridis",
        marker=pv.Marker(size=16**2),
    )

    def test(pos, ref):
        plot = pv.Plot(series, colorbar=pos)
        assert_fig_eq_ref(fig_small(plot), f"colorbar/{ref}")

    test("auto", "right")
    test("right", "right")
    test("bottom", "bottom")
    test("left", "left")
    test("top", "top")


def test_colorbar_with_axes():
    rnd = NotRandom()
    x = rnd.make_col_uniform(15)
    y = rnd.make_col_uniform(15)
    colors = [float(i) / 14 for i in range(15)]

    series = pv.series.Scatter(
        x=x,
        y=y,
        colors=colors,
        cmap="viridis",
        marker=pv.Marker(size=16**2),
    )

    def test(pos, ref):
        plot = pv.Plot(
            series,
            colorbar=pos,
            x_axis=pv.Axis(ticks="auto", scale=(0, 1)),
            y_axis=pv.Axis(ticks="auto", scale=(0, 1)),
        )
        assert_fig_eq_ref(fig_small(plot), f"colorbar/{ref}-with-axes")

    test("right", "right")
    test("bottom", "bottom")
    test("left", "left")
    test("top", "top")


def test_colorbar_with_axes_title():
    rnd = NotRandom()
    x = rnd.make_col_uniform(15)
    y = rnd.make_col_uniform(15)
    colors = [float(i) / 14 for i in range(15)]

    series = pv.series.Scatter(
        x=x,
        y=y,
        colors=colors,
        cmap="viridis",
        marker=pv.Marker(size=16**2),
    )

    def test(pos, ref):
        plot = pv.Plot(
            series,
            colorbar=pos,
            x_axis=pv.Axis(ticks="auto", scale=(0, 1), title="X Axis"),
            y_axis=pv.Axis(ticks="auto", scale=(0, 1), title="Y Axis"),
        )
        assert_fig_eq_ref(fig_small(plot), f"colorbar/{ref}-with-axes-title")

    test("right", "right")
    test("bottom", "bottom")
    test("left", "left")
    test("top", "top")


def test_colorbar_title_with_axes_title():
    rnd = NotRandom()
    x = rnd.make_col_uniform(15)
    y = rnd.make_col_uniform(15)
    colors = [float(i) / 14 for i in range(15)]

    series = pv.series.Scatter(
        x=x,
        y=y,
        colors=colors,
        cmap="viridis",
        marker=pv.Marker(size=16**2),
    )

    def test(pos, ref):
        plot = pv.Plot(
            series,
            colorbar=pv.ColorBar(pos, title="Color Scale"),
            x_axis=pv.Axis(ticks="auto", scale=(0, 1), title="X Axis"),
            y_axis=pv.Axis(ticks="auto", scale=(0, 1), title="Y Axis"),
        )
        assert_fig_eq_ref(fig_small(plot), f"colorbar/{ref}-title-with-axes-title")

    test("right", "right")
    test("bottom", "bottom")
    test("left", "left")
    test("top", "top")


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
        marker=pv.Marker(size=16**2),
    )
    plot = pv.Plot(series, colorbar=pv.ColorBar(ticks=pv.STELLAR_TICKS))
    assert_fig_eq_ref(fig_small(plot), "colorbar/stellar-ticks")
