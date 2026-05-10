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
    series = line(interpolation="linear")
    plot = pv.Plot(series)
    assert_fig_eq_ref(fig_small(plot), "series/line-interp-linear")


def test_series_line_interp_step_early():
    series = line(interpolation="step-early")
    plot = pv.Plot(series)
    assert_fig_eq_ref(fig_small(plot), "series/line-interp-step-early")


def test_series_line_interp_step_middle():
    series = line(interpolation="step-middle")
    plot = pv.Plot(series)
    assert_fig_eq_ref(fig_small(plot), "series/line-interp-step-middle")


def test_series_line_interp_step_late():
    series = line(interpolation="step-late")
    plot = pv.Plot(series)
    assert_fig_eq_ref(fig_small(plot), "series/line-interp-step-late")


def test_series_line_interp_spline():
    series = line(interpolation="spline")
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
        marker=pv.style.SeriesMarker(
            size=24**2,
            fill=pv.style.SeriesFill(color, opacity=0.6),
            stroke=pv.style.SeriesStroke(color),
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
        marker=pv.style.SeriesMarker(
            fill=pv.style.SeriesFill(color, opacity=0.6),
            stroke=pv.style.SeriesStroke(color, width=2.0),
        ),
    )
    plot = pv.Plot(series)
    assert_fig_eq_ref(fig_small(plot), "series/scatter-sizes")


def test_series_scatter_nodata():
    series = pv.series.Scatter(x=[], y=[])
    plot = pv.Plot(series)
    assert_fig_eq_ref(fig_small(plot), "series/scatter-nodata")


# #[test]
# fn series_area_double() {
#     let x = vec![0.0, 1.0, 2.0, 3.0, 4.0, 5.0];
#     let y1 = vec![10.0, 15.0, 8.0, 6.0, 12.0, 10.0];
#     let y2 = vec![4.0, 9.0, 2.0, 0.0, 6.0, 4.0];

#     let fill = plotive::Rgba8::from_hex(b"#888").into();
#     let stroke: style::series::Stroke = plotive::Rgba8::from_hex(b"#000").into();

#     let plot = des::Plot::new(vec![
#         des::series::Area::new(
#             des::data_inline(x.clone()),
#             des::data_inline(y1.clone()),
#             des::data_inline(y2.clone()).into(),
#         )
#         .with_fill(Some(fill))
#         .with_stroke_y1(stroke.clone())
#         .with_stroke_y2(stroke.clone())
#         .into(),
#         des::series::Area::new(
#             des::data_inline(x.clone()),
#             des::data_inline(y2.clone()),
#             Default::default(),
#         )
#         .with_fill(Some(fill))
#         .with_stroke_y1(stroke.clone())
#         .with_stroke_y2(stroke.clone())
#         .into(),
#     ]);
#     let fig = fig_small(plot);

#     assert_fig_eq_ref!(&fig, "series/area-double");
# }

# #[test]
# fn series_area_double_legend() {
#     let x = vec![0.0, 1.0, 2.0, 3.0, 4.0, 5.0];
#     let y1 = vec![10.0, 15.0, 8.0, 6.0, 12.0, 10.0];
#     let y2 = vec![4.0, 9.0, 2.0, 0.0, 6.0, 4.0];

#     let fill1 = plotive::Rgba8::from_hex(b"#888").into();
#     let fill2 = plotive::Rgba8::from_hex(b"#444").into();
#     let stroke: style::series::Stroke = plotive::Rgba8::from_hex(b"#000").into();

#     let plot = des::Plot::new(vec![
#         des::series::Area::new(
#             des::data_inline(x.clone()),
#             des::data_inline(y1.clone()),
#             des::data_inline(y2.clone()).into(),
#         )
#         .with_name("area1")
#         .with_fill(Some(fill1))
#         .with_stroke_y1(stroke.clone())
#         .with_stroke_y2(stroke.clone())
#         .into(),
#         des::series::Area::new(
#             des::data_inline(x.clone()),
#             des::data_inline(y2.clone()),
#             Default::default(),
#         )
#         .with_name("area2")
#         .with_fill(Some(fill2))
#         .with_stroke_y1(stroke.clone())
#         .with_stroke_y2(stroke.clone())
#         .into(),
#     ]);
#     let fig = fig_small(plot).with_legend(Default::default());

#     assert_fig_eq_ref!(&fig, "series/area-double-legend");
# }
