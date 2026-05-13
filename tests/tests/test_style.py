import plotive as pv

from . import *


def test_style_line():
    x, y = [0, 1], [0, 1]
    plot = pv.Plot(
        pv.series.Line(x=x, y=y, stroke=pv.Stroke(width=2)),
    )
    assert_fig_eq_ref(fig_small(plot), "style/line-solid")


def test_style_line_dashed():
    x, y = [0, 1], [0, 1]
    plot = pv.Plot(
        pv.series.Line(x=x, y=y, stroke=pv.Stroke(width=2, pattern=[5, 5])),
    )
    assert_fig_eq_ref(fig_small(plot), "style/line-dashed")


def test_style_line_dotted():
    x, y = [0, 1], [0, 1]
    plot = pv.Plot(
        pv.series.Line(x=x, y=y, stroke=pv.Stroke(width=2, pattern=[1, 1])),
    )
    assert_fig_eq_ref(fig_small(plot), "style/line-dotted")


def test_style_line_dash_dotted():
    x, y = [0, 1], [0, 1]
    plot = pv.Plot(
        pv.series.Line(x=x, y=y, stroke=pv.Stroke(width=2, pattern=[5, 5, 1, 5])),
    )
    assert_fig_eq_ref(fig_small(plot), "style/line-dash-dot")


def test_style_line_color():
    x, y = [0, 1], [0, 1]
    plot = pv.Plot(
        pv.series.Line(x=x, y=y, stroke=pv.Stroke(color="indian red", width=2)),
    )
    assert_fig_eq_ref(fig_small(plot), "style/line-color")


def test_style_line_marker():
    x, y = [0, 1], [0, 1]
    plot = pv.Plot(
        pv.series.Line(x=x, y=y, marker=pv.Marker()),
    )
    assert_fig_eq_ref(fig_small(plot), "style/line-marker")


def test_style_line_mpl_style():
    x, y = [0, 1], [0, 1]
    plot = pv.Plot(
        pv.series.Line(x=x, y=y, style="o--r"),
    )
    assert_fig_eq_ref(fig_small(plot), "style/line-marker-dash-red")
