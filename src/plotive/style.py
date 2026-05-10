"""Global styling primitives for figures and series."""

from typing import Literal

from ._rs import parse_color as _parse_color

type Color = str | tuple[float, float, float] | tuple[float, float, float, float]
"""
Named/CSS color string or RGB(A) tuple.
Tuples are expressed in sRGB color space with components in the [0, 1] interval.
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


class Fill[C = Color]:
    """Type alias for fill colors."""

    def __init__(self, color: C, *, opacity: float | None = None):
        """Initialize a fill color."""
        self.color = color
        self.opacity = opacity


class ThemeFill(Fill[ThemeColor]):
    def __init__(self, color: ThemeColor = "background", *, opacity: float | None = None):
        """Initialize a fill color."""
        super().__init__(color=color, opacity=opacity)

    @staticmethod
    def _normalize(input: ThemeFill | ThemeColor) -> ThemeFill:
        """Normalize a fill specification to a ThemeFill object."""
        if isinstance(input, Fill):
            return input
        else:
            return ThemeFill(color=input)


class SeriesFill(Fill[SeriesColor]):
    def __init__(self, color: SeriesColor = "auto", *, opacity: float | None = None):
        """Initialize a fill color."""
        super().__init__(color=color, opacity=opacity)

    @staticmethod
    def _normalize(input: SeriesFill | SeriesColor) -> SeriesFill:
        """Normalize a fill specification to a SeriesFill object."""
        if isinstance(input, SeriesFill):
            return input
        else:
            return SeriesFill(color=input)


class Stroke[C = Color]:
    """Line stroke style.

    Parameters
    ----------
    color : Color or ThemeColor or SeriesColor (depending on context)
        Stroke color.
    width : float, default=1.0
        Stroke width in pixels.
    pattern : list[float] | str | None, default=None
        Dash pattern specification.
    opacity : float, default=1.0
        Stroke opacity in the ``[0, 1]`` interval.
    """

    def __init__(
        self,
        color: C,
        *,
        width: float = 1.0,
        pattern: None | list[float] | str = None,
        opacity: float = 1.0,
    ):
        """Initialize a stroke style."""
        self.color = color
        self.width = width
        self.pattern = pattern
        self.opacity = opacity


class ThemeStroke(Stroke[ThemeColor]):
    """Line stroke style for theme elements.

    Parameters
    ----------
    color : ThemeColor
        Stroke color.
    width : float, default=1.0
        Stroke width in pixels.
    pattern : list[float] | str | None, default=None
        Dash pattern specification.
    opacity : float, default=1.0
        Stroke opacity in the ``[0, 1]`` interval.
    """

    def __init__(
        self,
        color: ThemeColor = "foreground",
        *,
        width: float = 1.0,
        pattern: None | list[float] | str = None,
        opacity: float = 1.0,
    ):
        """Initialize a stroke style."""
        self.color = color
        self.width = width
        self.pattern = pattern
        self.opacity = opacity

    @staticmethod
    def _normalize(input: ThemeStroke | ThemeColor) -> ThemeStroke:
        """Normalize a stroke specification to a ThemeStroke object."""
        if isinstance(input, ThemeStroke):
            return input
        else:
            return ThemeStroke(color=input)

class SeriesStroke(Stroke[SeriesColor]):
    """Line stroke style for series.

    Parameters
    ----------
    color : SeriesColor
        Stroke color.
    width : float, default=1.5
        Stroke width in pixels.
    pattern : list[float] | str | None, default=None
        Dash pattern specification.
    opacity : float, default=1.0
        Stroke opacity in the ``[0, 1]`` interval.
    """

    def __init__(
        self,
        color: SeriesColor = "auto",
        *,
        width: float = 1.5,
        pattern: None | list[float] | str = None,
        opacity: float = 1.0,
    ):
        """Initialize a stroke style."""
        self.color = color
        self.width = width
        self.pattern = pattern
        self.opacity = opacity

    @staticmethod
    def _normalize(input: SeriesStroke | SeriesColor) -> SeriesStroke:
        """Normalize a stroke specification to a SeriesStroke object."""
        if isinstance(input, SeriesStroke):
            return input
        else:
            return SeriesStroke(color=input)


type MarkerShape = Literal[
    "circle",
    "square",
    "diamond",
    "cross",
    "plus",
    "triangle-up",
    "triangle-down",
    "triangle-left",
    "triangle-right",
]


class Marker[C]:
    """Marker style for scatter series."""

    def __init__(
        self,
        shape: MarkerShape = "circle",
        *,
        size: float = 8.5**2,
        fill: None | Fill[C] | C = None,
        stroke: None | Stroke[C] | C = None,
    ):
        """Initialize a marker style.

        Parameters
        ----------
        shape : MarkerShape
            Marker shape. One of "circle", "square", "diamond", "cross", "plus", "triangle-up", "triangle-down", "triangle-left", "triangle-right".
        size : float, default=10.0
            Marker size in pixels.
        fill : Fill[C] | None, default=None
            Marker fill color.
        stroke : Stroke[C] | None, default=None
            Marker stroke style.
        """
        self.shape = shape
        self.size = size
        self.fill = fill
        self.stroke = stroke


class ThemeMarker(Marker[ThemeColor]):
    """Marker style for annotations"""

    def __init__(
        self,
        shape: str = "circle",
        *,
        size: float = 8.5**2,
        fill: None | ThemeFill | ThemeColor = "foreground",
        stroke: None | ThemeStroke | ThemeColor = "foreground",
    ):
        """Initialize a marker style.

        Parameters
        ----------
        shape : MarkerShape
            Marker shape. One of "circle", "square", "diamond", "cross", "plus", "triangle-up", "triangle-down", "triangle-left", "triangle-right".
        size : float, default=8.5**2
            Marker size. It is interpreted as an area, therefore the dimensions of markers are proportional to sqrt(size)
        fill : ThemeFill | ThemeColor | None, default="foreground"
            Marker fill color.
        stroke : ThemeStroke | ThemeColor | None, default="foreground"
            Marker stroke style.
        """
        self.shape = shape
        self.size = size
        self.fill = ThemeFill._normalize(fill) if fill is not None else None
        self.stroke = ThemeStroke._normalize(stroke) if stroke is not None else None

class SeriesMarker(Marker[SeriesColor]):
    """Marker style for scatter series."""

    def __init__(
        self,
        shape: str = "circle",
        *,
        size: float = 8.5**2,
        fill: None | SeriesFill | SeriesColor = "auto",
        stroke: None | SeriesStroke | SeriesColor = "auto",
    ):
        """Initialize a marker style.

        Parameters
        ----------
        shape : MarkerShape
            Marker shape. One of "circle", "square", "diamond", "cross", "plus", "triangle-up", "triangle-down", "triangle-left", "triangle-right".
        size : float, default=10.0
            Marker size in pixels.
        fill : Fill[C] | None, default=None
            Marker fill color.
        stroke : Stroke[C] | None, default=None
            Marker stroke style.
        """
        self.shape = shape
        self.size = size
        self.fill = SeriesFill._normalize(fill) if fill is not None else None
        self.stroke = SeriesStroke._normalize(stroke) if stroke is not None else None


class ThemePalette:
    """Theme palette for structural chart colors.

    Parameters
    ----------
    background : Color | None, default=None
        Figure background color.
    foreground : Color | None, default=None
        Main foreground color.
    grid : Color | None, default=None
        Grid line color.
    axis : Color | None, default=None
        Axis line and tick color.
    text : Color | None, default=None
        Text color.
    """

    def __init__(
        self,
        *,
        background: None | Color = None,
        foreground: None | Color = None,
        grid: None | Color = None,
        axis: None | Color = None,
        text: None | Color = None,
    ):
        """Initialize a theme palette."""
        self.background = background
        self.foreground = foreground
        self.grid = grid
        self.axis = axis
        self.text = text


type Theme = ThemePalette | str
"""Explicit theme object or predefined theme name."""

type SeriesPalette = list[Color] | str
"""Explicit series palette or predefined palette name."""


class Style:
    """Top-level style configuration for figure rendering.

    Parameters
    ----------
    theme : Theme | None, default=None
        Figure theme configuration.
    palette : SeriesPalette | None, default=None
        Color palette used for data series.
    """

    def __init__(
        self,
        *,
        theme: None | Theme = None,
        palette: None | SeriesPalette = None,
    ):
        """Initialize global style settings."""
        self.theme = theme
        self.palette = palette
