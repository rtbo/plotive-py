import plotive as pv
import numpy as np

from . import *


def _make_basic_scatter_series(cmap="viridis"):
    rnd = NotRandom()
    x = rnd.make_col_uniform(15)
    y = rnd.make_col_uniform(15)
    colors = [float(i) / 14 for i in range(15)]

    return pv.series.Scatter(
        x=x,
        y=y,
        colors=colors,
        cmap=cmap,
        marker=pv.Marker(size=16**2),
    )


def _make_stellar_scatter_series():
    rnd = NotRandom()
    x = rnd.make_col_uniform(15)
    y = rnd.make_col_uniform(15)
    colors = np.linspace(1000, 15000, 15)

    return pv.series.Scatter(
        x=x,
        y=y,
        colors=colors,
        cmap="stellar",
        marker=pv.Marker(size=16**2),
    )


def test_colorbar_pos_auto():
    series = _make_basic_scatter_series()
    plot = pv.Plot(series, colorbar="auto")
    assert_fig_eq_ref(fig_small(plot), "colorbar/right")


def test_colorbar_pos_right():
    series = _make_basic_scatter_series()
    plot = pv.Plot(series, colorbar="right")
    assert_fig_eq_ref(fig_small(plot), "colorbar/right")


def test_colorbar_pos_bottom():
    series = _make_basic_scatter_series()
    plot = pv.Plot(series, colorbar="bottom")
    assert_fig_eq_ref(fig_small(plot), "colorbar/bottom")


def test_colorbar_pos_left():
    series = _make_basic_scatter_series()
    plot = pv.Plot(series, colorbar="left")
    assert_fig_eq_ref(fig_small(plot), "colorbar/left")


def test_colorbar_pos_top():
    series = _make_basic_scatter_series()
    plot = pv.Plot(series, colorbar="top")
    assert_fig_eq_ref(fig_small(plot), "colorbar/top")


def test_colorbar_with_axes_right():
    series = _make_basic_scatter_series()
    plot = pv.Plot(
        series,
        colorbar="right",
        x_axis=pv.Axis(ticks="auto", scale=(0, 1)),
        y_axis=pv.Axis(ticks="auto", scale=(0, 1)),
    )
    assert_fig_eq_ref(fig_small(plot), "colorbar/right-with-axes")


def test_colorbar_with_axes_bottom():
    series = _make_basic_scatter_series()
    plot = pv.Plot(
        series,
        colorbar="bottom",
        x_axis=pv.Axis(ticks="auto", scale=(0, 1)),
        y_axis=pv.Axis(ticks="auto", scale=(0, 1)),
    )
    assert_fig_eq_ref(fig_small(plot), "colorbar/bottom-with-axes")


def test_colorbar_with_axes_left():
    series = _make_basic_scatter_series()
    plot = pv.Plot(
        series,
        colorbar="left",
        x_axis=pv.Axis(ticks="auto", scale=(0, 1)),
        y_axis=pv.Axis(ticks="auto", scale=(0, 1)),
    )
    assert_fig_eq_ref(fig_small(plot), "colorbar/left-with-axes")


def test_colorbar_with_axes_top():
    series = _make_basic_scatter_series()
    plot = pv.Plot(
        series,
        colorbar="top",
        x_axis=pv.Axis(ticks="auto", scale=(0, 1)),
        y_axis=pv.Axis(ticks="auto", scale=(0, 1)),
    )
    assert_fig_eq_ref(fig_small(plot), "colorbar/top-with-axes")


def test_colorbar_with_axes_title_right():
    series = _make_basic_scatter_series()
    plot = pv.Plot(
        series,
        colorbar="right",
        x_axis=pv.Axis(ticks="auto", scale=(0, 1), title="X Axis"),
        y_axis=pv.Axis(ticks="auto", scale=(0, 1), title="Y Axis"),
    )
    assert_fig_eq_ref(fig_small(plot), "colorbar/right-with-axes-title")


def test_colorbar_with_axes_title_bottom():
    series = _make_basic_scatter_series()
    plot = pv.Plot(
        series,
        colorbar="bottom",
        x_axis=pv.Axis(ticks="auto", scale=(0, 1), title="X Axis"),
        y_axis=pv.Axis(ticks="auto", scale=(0, 1), title="Y Axis"),
    )
    assert_fig_eq_ref(fig_small(plot), "colorbar/bottom-with-axes-title")


def test_colorbar_with_axes_title_left():
    series = _make_basic_scatter_series()
    plot = pv.Plot(
        series,
        colorbar="left",
        x_axis=pv.Axis(ticks="auto", scale=(0, 1), title="X Axis"),
        y_axis=pv.Axis(ticks="auto", scale=(0, 1), title="Y Axis"),
    )
    assert_fig_eq_ref(fig_small(plot), "colorbar/left-with-axes-title")


def test_colorbar_with_axes_title_top():
    series = _make_basic_scatter_series()
    plot = pv.Plot(
        series,
        colorbar="top",
        x_axis=pv.Axis(ticks="auto", scale=(0, 1), title="X Axis"),
        y_axis=pv.Axis(ticks="auto", scale=(0, 1), title="Y Axis"),
    )
    assert_fig_eq_ref(fig_small(plot), "colorbar/top-with-axes-title")


def test_colorbar_title_with_axes_title_right():
    series = _make_basic_scatter_series()
    plot = pv.Plot(
        series,
        colorbar=pv.ColorBar("right", title="Color Scale"),
        x_axis=pv.Axis(ticks="auto", scale=(0, 1), title="X Axis"),
        y_axis=pv.Axis(ticks="auto", scale=(0, 1), title="Y Axis"),
    )
    assert_fig_eq_ref(fig_small(plot), "colorbar/right-title-with-axes-title")


def test_colorbar_title_with_axes_title_bottom():
    series = _make_basic_scatter_series()
    plot = pv.Plot(
        series,
        colorbar=pv.ColorBar("bottom", title="Color Scale"),
        x_axis=pv.Axis(ticks="auto", scale=(0, 1), title="X Axis"),
        y_axis=pv.Axis(ticks="auto", scale=(0, 1), title="Y Axis"),
    )
    assert_fig_eq_ref(fig_small(plot), "colorbar/bottom-title-with-axes-title")


def test_colorbar_title_with_axes_title_left():
    series = _make_basic_scatter_series()
    plot = pv.Plot(
        series,
        colorbar=pv.ColorBar("left", title="Color Scale"),
        x_axis=pv.Axis(ticks="auto", scale=(0, 1), title="X Axis"),
        y_axis=pv.Axis(ticks="auto", scale=(0, 1), title="Y Axis"),
    )
    assert_fig_eq_ref(fig_small(plot), "colorbar/left-title-with-axes-title")


def test_colorbar_title_with_axes_title_top():
    series = _make_basic_scatter_series()
    plot = pv.Plot(
        series,
        colorbar=pv.ColorBar("top", title="Color Scale"),
        x_axis=pv.Axis(ticks="auto", scale=(0, 1), title="X Axis"),
        y_axis=pv.Axis(ticks="auto", scale=(0, 1), title="Y Axis"),
    )
    assert_fig_eq_ref(fig_small(plot), "colorbar/top-title-with-axes-title")


def test_colorbar_stellar_ticks():
    series = _make_stellar_scatter_series()
    plot = pv.Plot(series, colorbar=pv.ColorBar(ticks=pv.STELLAR_TICKS))
    assert_fig_eq_ref(fig_small(plot), "colorbar/stellar-ticks")
