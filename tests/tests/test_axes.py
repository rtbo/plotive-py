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


# def test_axes_categories():
#     x = ["a", "b", "c"]
#     y = [1, 1.4, 3]

# #[test]
# fn axes_categories() {
#     let x = vec!["a".to_string(), "b".to_string(), "c".to_string()];
#     let y = vec![1.0, 1.4, 3.0];
#     let series = des::series::Bars::new(x.into(), y.into())
#         .with_fill(color::TRANSPARENT.into())
#         .with_outline(Default::default());

#     let plot = des::Plot::new(vec![series.into()])
#         .with_x_axis(des::Axis::new().with_ticks(Default::default()));
#     let fig = fig_small(plot);

#     assert_fig_eq_ref!(&fig, "axes/categories");
# }

# #[test]
# fn axes_pi_locator() {
#     use std::f64::consts::PI;
#     let x = vec![PI, 2.0 * PI, 3.0 * PI];
#     let y = vec![1.0, 1.4, 3.0];
#     let series = des::series::Line::new(x.into(), y.into());

#     let plot = des::Plot::new(vec![series.into()]).with_x_axis(
#         des::Axis::new().with_ticks(
#             des::axis::Ticks::new()
#                 .with_locator(des::axis::ticks::PiMultipleLocator { bins: 5 }.into()),
#         ),
#     );
#     let fig = fig_small(plot);

#     assert_fig_eq_ref!(&fig, "axes/pi-locator");
# }

# #[test]
# fn axes_pi_locator_minor() {
#     use std::f64::consts::PI;
#     let x = vec![PI, 2.0 * PI, 3.0 * PI];
#     let y = vec![1.0, 1.4, 3.0];
#     let series = des::series::Line::new(x.into(), y.into());

#     let plot = des::Plot::new(vec![series.into()]).with_x_axis(
#         des::Axis::new()
#             .with_ticks(
#                 des::axis::Ticks::new()
#                     .with_locator(des::axis::ticks::PiMultipleLocator { bins: 5 }.into()),
#             )
#             .with_minor_ticks(
#                 des::axis::MinorTicks::new()
#                     .with_locator(des::axis::ticks::PiMultipleLocator { bins: 30 }.into()),
#             ),
#     );
#     let fig = fig_small(plot);

#     assert_fig_eq_ref!(&fig, "axes/pi-locator-minor");
# }

# #[test]
# fn axes_top_right() {
#     let s1 = line();
#     let plot = des::Plot::new(vec![s1.into()])
#         .with_x_axis(
#             des::Axis::new()
#                 .with_ticks(Default::default())
#                 .with_opposite_side(),
#         )
#         .with_y_axis(
#             des::Axis::new()
#                 .with_ticks(Default::default())
#                 .with_opposite_side(),
#         );
#     let fig = fig_small(plot);

#     assert_fig_eq_ref!(&fig, "axes/top-right");
# }

# #[test]
# fn axes_multiple_bl() {
#     let s1 = line();
#     let s2 = line2(&[4.0, 5.0, 6.0], &[6.0, 5.0, 4.0])
#         .with_x_axis(des::axis::Ref::Id("x2".to_string()))
#         .with_y_axis(des::axis::Ref::Id("y2".to_string()));
#     let plot = des::Plot::new(vec![s1.into(), s2.into()])
#         .with_x_axis(des::Axis::new().with_ticks(Default::default()))
#         .with_y_axis(des::Axis::new().with_ticks(Default::default()))
#         .with_x_axis(
#             des::Axis::new()
#                 .with_ticks(Default::default())
#                 .with_id("x2"),
#         )
#         .with_y_axis(
#             des::Axis::new()
#                 .with_ticks(Default::default())
#                 .with_id("y2"),
#         );
#     let fig = fig_small(plot);

#     assert_fig_eq_ref!(&fig, "axes/multiple-bl");
# }

# #[test]
# fn axes_multiple_trbl() {
#     let s1 = line();
#     let s2 = line2(&[4.0, 5.0, 6.0], &[6.0, 5.0, 4.0])
#         .with_x_axis(des::axis::Ref::Id("x2".to_string()))
#         .with_y_axis(des::axis::Ref::Id("y2".to_string()));
#     let plot = des::Plot::new(vec![s1.into(), s2.into()])
#         .with_x_axis(des::Axis::new().with_ticks(Default::default()))
#         .with_y_axis(des::Axis::new().with_ticks(Default::default()))
#         .with_x_axis(
#             des::Axis::new()
#                 .with_ticks(Default::default())
#                 .with_id("x2")
#                 .with_opposite_side(),
#         )
#         .with_y_axis(
#             des::Axis::new()
#                 .with_ticks(Default::default())
#                 .with_id("y2")
#                 .with_opposite_side(),
#         );
#     let fig = fig_small(plot);

#     assert_fig_eq_ref!(&fig, "axes/multiple-trbl");
# }

# #[test]
# fn axes_multiple_trbl_titles() {
#     let s1 = line();
#     let s2 = line2(&[4.0, 5.0, 6.0], &[6.0, 5.0, 4.0])
#         .with_x_axis(des::axis::Ref::Id("x2".to_string()))
#         .with_y_axis(des::axis::Ref::Id("y2".to_string()));
#     let plot = des::Plot::new(vec![s1.into(), s2.into()])
#         .with_x_axis(
#             des::Axis::new()
#                 .with_ticks(Default::default())
#                 .with_title("x1".into()),
#         )
#         .with_y_axis(
#             des::Axis::new()
#                 .with_ticks(Default::default())
#                 .with_title("y1".into()),
#         )
#         .with_x_axis(
#             des::Axis::new()
#                 .with_ticks(Default::default())
#                 .with_title("x2".into())
#                 .with_opposite_side(),
#         )
#         .with_y_axis(
#             des::Axis::new()
#                 .with_ticks(Default::default())
#                 .with_title("y2".into())
#                 .with_opposite_side(),
#         );
#     let fig = fig_mid(plot);

#     assert_fig_eq_ref!(&fig, "axes/multiple-trbl-titles");
# }

# #[test]
# fn axes_datetime_locator() {
#     use plotive::time;

#     let start = time::DateTime::fmt_parse("2020-01-01", "%Y-%m-%d").unwrap();
#     let x = (0..10)
#         .map(|i| start + time::TimeDelta::from_days(i as f64))
#         .collect::<Vec<_>>();
#     let y = (0..10).map(|i| 1.0 / (i as f64 + 1.0)).collect::<Vec<_>>();

#     let series = des::series::Line::new(x.into(), y.into());

#     let plot = des::Plot::new(vec![series.into()]).with_x_axis(des::Axis::new().with_ticks(
#         des::axis::Ticks::new().with_locator(des::axis::ticks::DateTimeLocator::Days(2).into()),
#     ));
#     let fig = fig_small(plot);

#     assert_fig_eq_ref!(&fig, "axes/datetime-locator");
# }

# #[test]
# fn axes_num_datetime_locator() {
#     use plotive::time;

#     let start = time::DateTime::fmt_parse("2020-01-01", "%Y-%m-%d").unwrap();
#     let x = (0..10)
#         .map(|i| start + time::TimeDelta::from_days(i as f64))
#         .map(|dt| dt.timestamp())
#         .collect::<Vec<_>>();
#     let y = (0..10).map(|i| 1.0 / (i as f64 + 1.0)).collect::<Vec<_>>();

#     let series = des::series::Line::new(x.into(), y.into());

#     let plot = des::Plot::new(vec![series.into()]).with_x_axis(des::Axis::new().with_ticks(
#         des::axis::Ticks::new().with_locator(des::axis::ticks::DateTimeLocator::Days(2).into()),
#     ));
#     let fig = fig_small(plot);

#     assert_fig_eq_ref!(&fig, "axes/datetime-locator");
# }
