
"""Color type aliases used across Plotive."""

type Color = str | tuple[int, int, int] | tuple[int, int, int, float]
"""
Named/CSS color string or RGB(A) tuple. (note the alpha component is a float in [0, 1])
"""

type ThemeColor = Color | str
"""
Color used in the context of a theme palette (grids, background, foreground, etc.). 
Can be a named/CSS color string, RGB(A) tuple as well as a reference to a theme color by name.
Accepted theme colors are "background", "foreground", "grid", "legend-fill" and "legend-border".
"""

type SeriesColor = Color | str | int
"""
Color used in the context of a series palette. 
Can be a named/CSS color string, RGB(A) tuple as well as a reference to a series palette by index.
If "auto", the color will be automatically assigned from the series palette based on the series index.
Can also be an integer index referring to a color in the series palette.
"""
