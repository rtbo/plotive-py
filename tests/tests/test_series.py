import plotive as pv

from . import *


def line(**kwargs):
    x = [1.0, 2.0, 3.0, 4.0, 5.0, 6.0]
    y = [0.0, 2.0, 3.0, 1.0, 4.0, 4.0]
    return pv.series.Line(x=x, y=y, **kwargs)


def test_series_line_nodata():
    series = pv.series.Line(x=[], y=[])
    plot = pv.Plot(series)
    assert_fig_eq_ref(fig_small(plot), "series/line-nodata")


def test_series_line_interp_linear():
    series = line(interp="linear")
    plot = pv.Plot(series)
    assert_fig_eq_ref(fig_small(plot), "series/line-interp-linear")


def test_series_line_interp_step_early():
    series = line(interp="step-early")
    plot = pv.Plot(series)
    assert_fig_eq_ref(fig_small(plot), "series/line-interp-step-early")


def test_series_line_interp_step_middle():
    series = line(interp="step-middle")
    plot = pv.Plot(series)
    assert_fig_eq_ref(fig_small(plot), "series/line-interp-step-middle")


def test_series_line_interp_step_late():
    series = line(interp="step-late")
    plot = pv.Plot(series)
    assert_fig_eq_ref(fig_small(plot), "series/line-interp-step-late")


def test_series_line_interp_spline():
    series = line(interp="spline")
    plot = pv.Plot(series)
    assert_fig_eq_ref(fig_small(plot), "series/line-interp-spline")


def test_series_scatter_nodata():
    series = pv.series.Scatter(x=[], y=[])
    plot = pv.Plot(series)
    assert_fig_eq_ref(fig_small(plot), "series/scatter-nodata")


def test_series_scatter():
    rnd = NotRandom()
    x = rnd.make_col_uniform(15)
    y = rnd.make_col_uniform(15)

    color = "light eggplant"
    series = pv.series.Scatter(
        x=x,
        y=y,
        marker=pv.Marker(
            size=24**2,
            color=color,
            fill_opacity=0.6,
        ),
    )
    plot = pv.Plot(series)
    assert_fig_eq_ref(fig_small(plot), "series/scatter")


def test_series_scatter_sizes():
    rnd = NotRandom()
    x = rnd.make_col_uniform(15)
    y = rnd.make_col_uniform(15)
    sizes = rnd.make_col_uniform(15, 1.0, 24.0)

    color = "light eggplant"

    series = pv.series.Scatter(
        x=x,
        y=y,
        sizes=sizes,
        marker=pv.Marker(
            stroke=pv.Stroke(width=2.0),
            color=color,
            fill_opacity=0.6,
        ),
    )
    plot = pv.Plot(series)
    assert_fig_eq_ref(fig_small(plot), "series/scatter-sizes")


def test_series_scatter_colors():
    rnd = NotRandom()
    x = rnd.make_col_uniform(15)
    y = rnd.make_col_uniform(15)
    colors = [float(i) / 14 for i in range(15)]

    series = pv.series.Scatter(
        x=x,
        y=y,
        colors=colors,
        marker=pv.Marker(size=16**2),
    )
    plot = pv.Plot(series)
    assert_fig_eq_ref(fig_small(plot), "series/scatter-colors")


def test_series_scatter_colors_stellar():
    rnd = NotRandom()
    x = rnd.make_col_uniform(15)
    y = rnd.make_col_uniform(15)
    colors = [float(i * 1000) + 1000 for i in range(15)]

    series = pv.series.Scatter(
        x=x,
        y=y,
        colors=colors,
        cmap="stellar",
        marker=pv.Marker(size=16**2),
    )
    plot = pv.Plot(series)
    assert_fig_eq_ref(fig_small(plot), "series/scatter-colors-stellar")


def test_series_area_double():
    x = [0.0, 1.0, 2.0, 3.0, 4.0, 5.0]
    y1 = [10.0, 15.0, 8.0, 6.0, 12.0, 10.0]
    y2 = [4.0, 9.0, 2.0, 0.0, 6.0, 4.0]

    fill = "gray"
    stroke = "black"

    series1 = pv.series.Area(
        x=x, y1=y1, y2=y2, fill=fill, y1_stroke=stroke, y2_stroke=stroke
    )
    series2 = pv.series.Area(x=x, y1=y2, fill=fill, y1_stroke=stroke, y2_stroke=stroke)

    plot = pv.Plot([series1, series2])
    fig = fig_small(plot)

    assert_fig_eq_ref(fig, "series/area-double")


def test_series_area_double_legend():
    x = [0.0, 1.0, 2.0, 3.0, 4.0, 5.0]
    y1 = [10.0, 15.0, 8.0, 6.0, 12.0, 10.0]
    y2 = [4.0, 9.0, 2.0, 0.0, 6.0, 4.0]

    fill1 = "#888"
    fill2 = "#444"
    stroke = "black"

    series1 = pv.series.Area(
        x=x, y1=y1, y2=y2, name="area1", fill=fill1, y1_stroke=stroke, y2_stroke=stroke
    )
    series2 = pv.series.Area(
        x=x, y1=y2, name="area2", fill=fill2, y1_stroke=stroke, y2_stroke=stroke
    )

    plot = pv.Plot([series1, series2])
    fig = fig_small(plot, legend="auto")

    assert_fig_eq_ref(fig, "series/area-double-legend")
