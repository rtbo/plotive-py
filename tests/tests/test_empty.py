import plotive as pv

from . import *

def test_empty():
    plot = pv.Plot(series=[])
    fig = fig_small(plot)

    assert_fig_eq_ref(fig, "empty")

def test_empty_title():
    plot = pv.Plot(series=[])
    fig = fig_small(plot, title="Title")

    assert_fig_eq_ref(fig, "empty-title")
