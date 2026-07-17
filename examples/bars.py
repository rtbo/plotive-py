import plotive as pv

data = {
    "fruits": ["Apples", "Bananas", "Cherries", "Dates", "Elderberries"],
    "2023": [50, 30, 20, 10, 5],
    "2024": [60, 25, 15, 5, 10],
    "2025": [70, 20, 10, 5, 15],
}


def make_bars_series(y_col: str, pos: tuple[float, float]) -> pv.Series:
    return pv.series.Bars(
        x="fruits",
        y=y_col,
        name=y_col.capitalize(),
        position=pos,
    )


fig = pv.Figure(
    title="Fruit Stock Levels Over Years",
    plot=pv.Plot(
        series=[
            make_bars_series("2023", (0.2, 0.2)),
            make_bars_series("2024", (0.4, 0.2)),
            make_bars_series("2025", (0.6, 0.2)),
        ],
        x_axis=pv.Axis(title="Fruits", ticks="auto", grid="auto"),
        y_axis=pv.Axis(title="Stock Levels [tons]", ticks="auto", grid="auto"),
    ),
    legend="right",
)

import _common

_common.process_figure(fig, data, "bars")
