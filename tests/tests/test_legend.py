import plotive as pv

from . import *


def line(**kwargs):
    x = [1.0, 2.0, 3.0]
    y = [1.0, 2.0, 3.0]
    return pv.series.Line(x=x, y=y, **kwargs)


def test_legend_pos_default():
    series = line(name="line")
    plot = pv.Plot(series=series, legend="auto")
    assert_fig_eq_ref(fig_small(plot), "legend/pos-bottom")


def test_legend_pos_top():
    series = line(name="line")
    plot = pv.Plot(series=series, legend="out-top")
    assert_fig_eq_ref(fig_small(plot), "legend/pos-top")


def test_legend_pos_right():
    series = line(name="line")
    plot = pv.Plot(series=series, legend="out-right")
    assert_fig_eq_ref(fig_small(plot), "legend/pos-right")


def test_legend_pos_bottom():
    series = line(name="line")
    plot = pv.Plot(series=series, legend="out-bottom")
    assert_fig_eq_ref(fig_small(plot), "legend/pos-bottom")


def test_legend_pos_left():
    series = line(name="line")
    plot = pv.Plot(series=series, legend="out-left")
    assert_fig_eq_ref(fig_small(plot), "legend/pos-left")


def test_legend_pos_in_top_left():
    series = line(name="line")
    plot = pv.Plot(series=series, legend="in-top-left")
    assert_fig_eq_ref(fig_small(plot), "legend/pos-in_top_left")


def test_legend_pos_in_top():
    series = line(name="line")
    plot = pv.Plot(series=series, legend="in-top")
    assert_fig_eq_ref(fig_small(plot), "legend/pos-in_top")


def test_legend_pos_in_top_right():
    series = line(name="line")
    plot = pv.Plot(series=series, legend="in-top-right")
    assert_fig_eq_ref(fig_small(plot), "legend/pos-in_top_right")


def test_legend_pos_in_right():
    series = line(name="line")
    plot = pv.Plot(series=series, legend="in-right")
    assert_fig_eq_ref(fig_small(plot), "legend/pos-in_right")


def test_legend_pos_in_bottom_right():
    series = line(name="line")
    plot = pv.Plot(series=series, legend="in-bottom-right")
    assert_fig_eq_ref(fig_small(plot), "legend/pos-in_bottom_right")


def test_legend_pos_in_bottom():
    series = line(name="line")
    plot = pv.Plot(series=series, legend="in-bottom")
    assert_fig_eq_ref(fig_small(plot), "legend/pos-in_bottom")


def test_legend_pos_in_bottom_left():
    series = line(name="line")
    plot = pv.Plot(series=series, legend="in-bottom-left")
    assert_fig_eq_ref(fig_small(plot), "legend/pos-in_bottom_left")


def test_legend_pos_in_left():
    series = line(name="line")
    plot = pv.Plot(series=series, legend="in-left")
    assert_fig_eq_ref(fig_small(plot), "legend/pos-in_left")
