from os import path
import pandas as pd
import plotive as pv

def ra_to_deg(ra: str) -> float:
    """Convert a right ascension string in the format "h:m:s" to degrees."""
    h, m, s = map(float, ra.split(":"))
    return (h + m / 60.0 + s / 3600.0) * 15.0

def dec_to_deg(dec: str) -> float:
    """Convert a declination string in the format "d:m:s" to degrees."""
    d, m, s = map(float, dec.split(":"))
    sign = -1.0 if d < 0 else 1.0
    return sign * (abs(d) + m / 60.0 + s / 3600.0)

csv_file = path.join(path.dirname(path.abspath(__file__)), "stars.csv")
df = pd.read_csv(csv_file)


# Map the apparent magnitude to a size factor for the star markers
AM_COL = "Apparent Magnitude"
MIN_SIZE = 0.2
MAX_SIZE = 20.0
mag_bounds = (df[AM_COL].min(), df[AM_COL].max())
mag_sizes = MAX_SIZE - (df[AM_COL] - mag_bounds[0]) / (mag_bounds[1] - mag_bounds[0]) * (MAX_SIZE - MIN_SIZE)

# Map the right ascension and declination to x and y coordinates in degrees
x_coords = df["RA (h:m:s)"].apply(ra_to_deg)
y_coords = df["DEC (d:m:s)"].apply(dec_to_deg)

data = {
    "x": x_coords,
    "y": y_coords,
    "mag_sizes": mag_sizes,
    "temp": df["Surface Temperature (K)"],
}

fig = pv.Figure(
    title=["45 [bold]bright[/bold] [color=sun yellow]stars[/color]"],
    plot=pv.Plot(
        series=[
            pv.series.Scatter(
                x="x",
                y="y",
                sizes="mag_sizes",
                colors="temp",
                marker=pv.series.Marker(fill_opacity=0.85),
                cmap="stellar",
            ),
        ],
        colorbar=pv.ColorBar(
            title="Surface Temperature [K]",
            ticks=pv.STELLAR_TICKS,
        ),
    )
)

import _common
_common.process_figure(fig, data, "stars")

