import plotive as pv


def test_series_mapping_keys_are_camel_case():
    s = pv.series.Line(x=[1.0, 2.0], y=[3.0, 4.0], x_axis="x", y_axis="y")

    as_dict = dict(s)

    assert "xAxis" in as_dict
    assert "yAxis" in as_dict
    assert "x_axis" not in as_dict
    assert "y_axis" not in as_dict


def test_series_mapping_getitem_accepts_camel_and_snake():
    s = pv.series.Line(x=[1.0, 2.0], y=[3.0, 4.0], x_axis="x", y_axis="y")

    assert s["xAxis"] == "x"
    assert s["x_axis"] == "x"
    assert s["yAxis"] == "y"
    assert s["y_axis"] == "y"


def test_figure_mapping_keys_are_camel_case():
    fig = pv.Figure(plot=pv.Plot(series=[]), title="A title")

    as_dict = dict(fig)

    assert "plots" in as_dict
    assert "title" in as_dict
