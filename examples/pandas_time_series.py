import pandas as pd
import plotive as pv

# Create a time series with a date range as the index
date_range = pd.date_range(start='2023-01-01', periods=10, freq='D')
dataframe = pd.DataFrame({'value': range(10), 'time': date_range})

fig = pv.Figure(
    plot=pv.Plot(
        series = pv.series.Line(
            x="time",
            y="value",
        ),
        x_axis=pv.Axis(ticks="auto"),
    ),
)

import _common
_common.process_figure(fig, dataframe, "pandas-time-series")

