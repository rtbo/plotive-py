import plotive as pv

from . import *


def test_annot_lines():
    x, y = [0, 1], [0, 1]
    plot = pv.Plot(
        pv.series.Line(x=x, y=y),
        annotations=[
            pv.annot.Line(horizontal=0, stroke=pv.Stroke(color="red", width=2)),
            pv.annot.Line(
                vertical=1,
                stroke=pv.Stroke(color="blue", width=2, pattern=[5, 5, 1, 5]),
            ),
            pv.annot.Line(
                two_points=((0.4, 0.8), (0.8, 0.2)),
                stroke=pv.Stroke(color="green", width=2, pattern="dashed"),
            ),
            pv.annot.Line(
                slope=((0.2, 0.8), -2),
                stroke=pv.Stroke(color="orange", width=2, pattern="dotted"),
            ),
        ],
    )
    assert_fig_eq_ref(fig_small(plot), "annot/lines")


def test_annot_markers():
    x, y = [0, 1], [0, 1]
    plot = pv.Plot(
        pv.series.Line(x=x, y=y),
        annotations=[
            pv.annot.Marker(
                (0.5, 0.5),
                marker=pv.style.ThemeMarker(shape="square", color="purple", size=12**2),
            ),
            pv.annot.Marker(
                (0.2, 0.8),
                marker=pv.style.ThemeMarker(
                    shape="diamond",
                    size=24**2,
                    stroke=pv.Stroke(color="indian red", width=2),
                    fill=pv.Fill(color="indian red", opacity=0.5),
                ),
            ),
            pv.annot.Marker(
                (0.8, 0.2),
                marker=pv.style.ThemeMarker(shape="circle", color="purple", size=12**2),
            ),
        ],
    )
    assert_fig_eq_ref(fig_small(plot), "annot/markers")
