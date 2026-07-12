from os import path
import pandas as pd
import plotive as pv

csv_file = path.join(path.dirname(path.abspath(__file__)), "BTC-USD.csv")
df = pd.read_csv(csv_file, parse_dates=["Date"], index_col="Date")

fig = pv.Figure(
    title="Bitcoin historical data",
    plot=pv.Plot(
        series=[
            pv.series.Line(
                x="Date",
                y="Close",
                name="Closing Price",
            ),
            pv.series.Line(
                x="Date",
                y="Volume",
                name="Volume",
                y_axis="volume",
            ),
        ],
        x_axis=pv.Axis(
            title="Date",
            ticks="auto",
        ),
        y_axes=[
            pv.Axis(
                title="Price [USD]",
                scale=(0, 8e4),
                ticks="auto",
                grid="auto",
            ),
            pv.Axis(
                title="Volume [USD]",
                scale=(0, 4e11),
                ticks="auto",
                id="volume",
                side="right",
            )
        ],
        legend="in-top-left",
    ),
)

import _common

_common.process_figure(fig, df, "bitcoin")
