
"""Color type aliases used across Plotive."""

type Color = str | tuple[int, int, int] | tuple[int, int, int, float]
"""
Named/CSS color string or RGB(A) tuple. (note the alpha component is a float in [0, 1])
When used in the context of a themable element (text, axis, grid etc.),
the string can also be a reference to a theme palette color by name.
Accepted theme colors are "background", "foreground", "grid", "legend-fill" and "legend-border".
"""
