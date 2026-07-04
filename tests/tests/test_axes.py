import plotive as pv

from . import *


def line():
    x = [1.0, 2.0, 3.0]
    y = [1.0, 2.0, 3.0]
    return pv.series.Line(x=x, y=y)


def test_axes_default():
    series = line()
    plot = pv.Plot(series=[series])
    fig = fig_small(plot)

    assert_fig_eq_ref(fig, "axes/default")


def test_axes_x_title():
    series = line()
    plot = pv.Plot(series=[series], x_axis=pv.Axis(title="x axis"))
    fig = fig_small(plot)

    assert_fig_eq_ref(fig, "axes/x-title")


def test_axes_y_title():
    series = line()
    plot = pv.Plot(series=[series], y_axis=pv.Axis(title="y axis"))
    fig = fig_small(plot)

    assert_fig_eq_ref(fig, "axes/y-title")


def test_axes_titles():
    series = line()
    plot = pv.Plot(
        series=[series], x_axis=pv.Axis(title="x axis"), y_axis=pv.Axis(title="y axis")
    )
    fig = fig_small(plot)

    assert_fig_eq_ref(fig, "axes/titles")


def test_axes_x_major_ticks():
    series = line()
    plot = pv.Plot(series=[series], x_axis=pv.Axis(ticks="auto"))
    fig = fig_small(plot)

    assert_fig_eq_ref(fig, "axes/x-major-ticks")


def test_axes_y_major_ticks():
    series = line()
    plot = pv.Plot(series=[series], y_axis=pv.Axis(ticks=pv.axis.Ticks()))
    fig = fig_small(plot)

    assert_fig_eq_ref(fig, "axes/y-major-ticks")


def test_axes_major_ticks():
    series = line()
    plot = pv.Plot(
        series=[series], x_axis=pv.Axis(ticks="auto"), y_axis=pv.Axis(ticks="auto")
    )
    fig = fig_small(plot)

    assert_fig_eq_ref(fig, "axes/major-ticks")


def test_axes_x_title_major_ticks():
    series = line()
    plot = pv.Plot(
        series=[series],
        x_axis=pv.Axis(title="x axis", ticks="auto"),
    )
    fig = fig_small(plot)

    assert_fig_eq_ref(fig, "axes/x-title-major-ticks")


def test_axes_y_title_major_ticks():
    series = line()
    plot = pv.Plot(
        series=[series],
        y_axis=pv.Axis(title="y axis", ticks="auto"),
    )
    fig = fig_small(plot)

    assert_fig_eq_ref(fig, "axes/y-title-major-ticks")


def test_axes_titles_major_ticks():
    series = line()
    plot = pv.Plot(
        series=[series],
        x_axis=pv.Axis(title="x axis", ticks="auto"),
        y_axis=pv.Axis(title="y axis", ticks="auto"),
    )
    fig = fig_small(plot)

    assert_fig_eq_ref(fig, "axes/titles-major-ticks")


def test_axes_minor_ticks():
    series = line()
    plot = pv.Plot(
        series=[series],
        x_axis=pv.Axis(ticks="auto", minor_ticks="auto"),
        y_axis=pv.Axis(ticks="auto", minor_ticks="auto"),
    )
    fig = fig_small(plot)

    assert_fig_eq_ref(fig, "axes/minor-ticks")


def test_axes_x_major_grid():
    series = line()
    plot = pv.Plot(
        series=[series],
        x_axis=pv.Axis(ticks="auto", grid="auto"),
    )
    fig = fig_small(plot)

    assert_fig_eq_ref(fig, "axes/x-major-grid")


def test_axes_y_major_grid():
    series = line()
    plot = pv.Plot(
        series=[series],
        y_axis=pv.Axis(ticks="auto", grid="auto"),
    )
    fig = fig_small(plot)

    assert_fig_eq_ref(fig, "axes/y-major-grid")


def test_axes_major_grid():
    series = line()
    plot = pv.Plot(
        series=[series],
        x_axis=pv.Axis(ticks="auto", grid="auto"),
        y_axis=pv.Axis(ticks="auto", grid="auto"),
    )
    fig = fig_small(plot)

    assert_fig_eq_ref(fig, "axes/major-grid")


def test_axes_minor_grid():
    series = line()
    axis = pv.Axis(ticks="auto", grid="auto", minor_ticks="auto", minor_grid="auto")
    plot = pv.Plot(
        series=[series],
        x_axis=axis,
        y_axis=axis,
    )
    fig = fig_small(plot)

    assert_fig_eq_ref(fig, "axes/minor-grid")


def test_axes_categories():
    x = ["a", "b", "c"]
    y = [1, 1.4, 3]
    series = pv.series.Bars(x, y, fill="transparent", stroke=pv.Stroke())
    plot = pv.Plot(series=[series], x_axis=pv.Axis(ticks=pv.axis.Ticks()))
    fig = fig_small(plot)

    assert_fig_eq_ref(fig, "axes/categories")


def test_axes_pi_locator():
    from math import pi

    x = [pi, 2 * pi, 3 * pi]
    y = [1, 1.4, 3]
    series = pv.series.Line(x, y)
    plot = pv.Plot(
        series,
        x_axis=pv.Axis(ticks=pv.axis.Ticks(locator=pv.axis.PiMultipleTicksLocator(5))),
    )
    fig = fig_small(plot)

    assert_fig_eq_ref(fig, "axes/pi-locator")


def test_axes_pi_locator_minor():
    from math import pi

    x = [pi, 2 * pi, 3 * pi]
    y = [1, 1.4, 3]
    series = pv.series.Line(x, y)
    plot = pv.Plot(
        series,
        x_axis=pv.Axis(
            ticks=pv.axis.Ticks(locator=pv.axis.PiMultipleTicksLocator(5)),
            minor_ticks=pv.axis.PiMultipleTicksLocator(30),
        ),
    )
    fig = fig_small(plot)

    assert_fig_eq_ref(fig, "axes/pi-locator-minor")


def test_axes_top_right():
    series = line()
    plot = pv.Plot(
        series=[series],
        x_axis=pv.Axis(ticks="auto", side="top"),
        y_axis=pv.Axis(ticks="auto", side="right"),
    )
    fig = fig_small(plot)

    assert_fig_eq_ref(fig, "axes/top-right")


def test_axes_multiple_bl():
    s1 = line()
    s2 = pv.series.Line([4.0, 5.0, 6.0], [6.0, 5.0, 4.0], x_axis="x2", y_axis="y2")
    plot = pv.Plot(
        series=[s1, s2],
        x_axes=[pv.Axis(ticks="auto"), pv.Axis(id="x2", ticks="auto")],
        y_axes=[pv.Axis(ticks="auto"), pv.Axis(id="y2", ticks="auto")],
    )
    fig = fig_small(plot)

    assert_fig_eq_ref(fig, "axes/multiple-bl")


def test_axes_multiple_trbl():
    s1 = line()
    s2 = pv.series.Line([4.0, 5.0, 6.0], [6.0, 5.0, 4.0], x_axis="x2", y_axis="y2")
    plot = pv.Plot(
        series=[s1, s2],
        x_axes=[
            pv.Axis(ticks="auto"),
            pv.Axis(id="x2", ticks="auto", side="top"),
        ],
        y_axes=[
            pv.Axis(ticks="auto"),
            pv.Axis(id="y2", ticks="auto", side="right"),
        ],
    )
    fig = fig_small(plot)

    assert_fig_eq_ref(fig, "axes/multiple-trbl")


def test_axes_multiple_trbl_titles():
    s1 = line()
    s2 = pv.series.Line([4.0, 5.0, 6.0], [6.0, 5.0, 4.0], x_axis="x2", y_axis="y2")
    plot = pv.Plot(
        series=[s1, s2],
        x_axes=[
            pv.Axis(ticks="auto", title="x1"),
            pv.Axis(ticks="auto", title="x2", side="top"),
        ],
        y_axes=[
            pv.Axis(ticks="auto", title="y1"),
            pv.Axis(ticks="auto", title="y2", side="right"),
        ],
    )
    fig = fig_mid(plot)

    assert_fig_eq_ref(fig, "axes/multiple-trbl-titles")


def test_axes_datetime_locator():
    import datetime

    start = datetime.datetime(2020, 1, 1)
    x = [start + datetime.timedelta(days=i) for i in range(10)]
    y = [1.0 / (i + 1.0) for i in range(10)]
    series = pv.series.Line(x=x, y=y)
    plot = pv.Plot(
        series=[series],
        x_axis=pv.Axis(
            ticks=pv.axis.Ticks(locator=pv.axis.DateTimeTicksLocator(period=(2, "day")))
        ),
    )
    fig = fig_small(plot)

    assert_fig_eq_ref(fig, "axes/datetime-locator")


def axes_num_datetime_locator():
    import datetime

    start = datetime.datetime(2020, 1, 1)
    x = [(start + datetime.timedelta(days=i)).timestamp() for i in range(10)]
    y = [1.0 / (i + 1.0) for i in range(10)]
    series = pv.series.Line(x=x, y=y)
    plot = pv.Plot(
        series=[series],
        x_axis=pv.Axis(
            ticks=pv.axis.Ticks(locator=pv.axis.DateTimeTicksLocator(period=(2, "day")))
        ),
    )
    fig = fig_small(plot)

    assert_fig_eq_ref(fig, "axes/datetime-locator")
