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
    assert_fig_eq_ref(fig_small(plot), "colorbar/right")


def test_colorbar_right():
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
    plot = pv.Plot(series, colorbar="right")
    assert_fig_eq_ref(fig_small(plot), "colorbar/right")


def test_colorbar_bottom():
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
    plot = pv.Plot(series, colorbar="bottom")
    assert_fig_eq_ref(fig_small(plot), "colorbar/bottom")


def test_colorbar_left():
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
    plot = pv.Plot(series, colorbar="left")
    assert_fig_eq_ref(fig_small(plot), "colorbar/left")


def test_colorbar_top():
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
    plot = pv.Plot(series, colorbar="top")
    assert_fig_eq_ref(fig_small(plot), "colorbar/top")


# def test_colorbar_right_with_axes():
#     rnd = NotRandom()
#     x = rnd.make_col_uniform(15)
#     y = rnd.make_col_uniform(15)
#     colors = [float(i) / 14 for i in range(15)]

#     series = pv.series.Scatter(
#         x=x,
#         y=y,
#         colors=colors,
#         cmap="viridis",
#         marker=pv.style.SeriesMarker(size=16**2),
#     )
#     plot = pv.Plot(
#         series,
#         colorbar="right",
#         x_axis=pv.Axis(ticks="auto", scale=(0, 1)),
#         y_axis=pv.Axis(ticks="auto", scale=(0, 1)),
#     )
#     assert_fig_eq_ref(fig_small(plot), "colorbar/right-with-axes")

# def test_colorbar_bottom_with_axes():
#     rnd = NotRandom()
#     x = rnd.make_col_uniform(15)
#     y = rnd.make_col_uniform(15)
#     colors = [float(i) / 14 for i in range(15)]

#     series = pv.series.Scatter(
#         x=x,
#         y=y,
#         colors=colors,
#         cmap="viridis",
#         marker=pv.style.SeriesMarker(size=16**2),
#     )
#     plot = pv.Plot(
#         series,
#         colorbar="bottom",
#         x_axis=pv.Axis(ticks="auto"),
#         y_axis=pv.Axis(ticks="auto"),
#     )
#     assert_fig_eq_ref(fig_small(plot), "colorbar/bottom-with-axes")

# def test_colorbar_left_with_axes():
#     rnd = NotRandom()
#     x = rnd.make_col_uniform(15)
#     y = rnd.make_col_uniform(15)
#     colors = [float(i) / 14 for i in range(15)]

#     series = pv.series.Scatter(
#         x=x,
#         y=y,
#         colors=colors,
#         cmap="viridis",
#         marker=pv.style.SeriesMarker(size=16**2),
#     )
#     plot = pv.Plot(
#         series,
#         colorbar="auto",
#         x_axis=pv.Axis(ticks="auto"),
#         y_axis=pv.Axis(ticks="auto"),
#     )
#     assert_fig_eq_ref(fig_small(plot), "colorbar/left-with-axes")

# def test_colorbar_top_with_axes():
#     rnd = NotRandom()
#     x = rnd.make_col_uniform(15)
#     y = rnd.make_col_uniform(15)
#     colors = [float(i) / 14 for i in range(15)]

#     series = pv.series.Scatter(
#         x=x,
#         y=y,
#         colors=colors,
#         cmap="viridis",
#         marker=pv.style.SeriesMarker(size=16**2),
#     )
#     plot = pv.Plot(
#         series,
#         colorbar="top",
#         x_axis=pv.Axis(ticks="auto"),
#         y_axis=pv.Axis(ticks="auto"),
#     )
#     assert_fig_eq_ref(fig_small(plot), "colorbar/top-with-axes")


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
