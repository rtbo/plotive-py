"""Global styling primitives for figures and series."""

from typing import Literal

from .mapping import PvMapping

from .color import Color

type Auto = Literal["auto"]

type ThemePaletteColor = Literal[
    "background", "foreground", "grid", "legend-border", "legend-fill"
]
type ThemeColor = Color | ThemePaletteColor

type SeriesPaletteColor = Literal["auto"] | int
type SeriesColor = Color | SeriesPaletteColor

type Pattern = list[float] | list[int] | Literal[
    "solid", "dashed", "dotted", "dash-dot"
]
"""Line pattern specification, either as a list of dash/gap lengths in pixels or as a predefined pattern name."""


class Fill[ColType: Color | ThemeColor | SeriesColor](PvMapping):
    """Type alias for fill colors."""

    def __init__(self, color: ColType = "auto", *, opacity: float | None = None):
        """Initialize a fill color.

        Parameters
        ----------
        color : ColType, default="auto"
            Fill color. "auto" means that the default color for the context will be used.
        opacity : float | None, default=None
            Fill opacity in the ``[0, 1]`` interval.
            None means opaque.
        """
        self.color = color
        self.opacity = opacity


class Stroke[ColType: Color | ThemeColor | SeriesColor](PvMapping):
    """Line stroke style."""

    def __init__(
        self,
        color: ColType | Auto = "auto",
        *,
        width: float | None = None,
        pattern: Pattern | None = None,
        opacity: float | None = None,
    ):
        """Initialize a stroke style.


        Parameters
        ----------
        color : ColType | Auto, default="auto"
            Stroke color. "auto" means that the default color for the context will be used.
        width : float | None
            Stroke width in pixels. None means that the default width for the context will be used.
            (1.0 for theme strokes, 1.5 for series strokes)
        pattern : Pattern | None, default=None
            Dash pattern specification. None means solid line.
        opacity : float | None, default=None
            Stroke opacity in the ``[0, 1]`` interval.
            None means opaque
        """
        self.color = color
        self.width = width
        self.pattern = pattern
        self.opacity = opacity


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


class Marker[ColType: Color | ThemeColor | SeriesColor](PvMapping):
    """Marker style for scatter series."""

    def __init__(
        self,
        *,
        shape: MarkerShape = "circle",
        size: float = 8.5**2,
        fill: None | Fill[ColType] | ColType | Auto = "auto",
        stroke: None | Stroke[ColType] | ColType | Auto = "auto",
        color: None | ColType = None,
        fill_opacity: None | float = None,
    ):
        """Initialize a marker style.

        Parameters
        ----------
        shape : MarkerShape
            Marker shape. One of "circle", "square", "diamond", "cross", "plus", "triangle-up", "triangle-down", "triangle-left", "triangle-right".
        size : float, default=8.5**2
            Marker size in pixels. The size is proportional to the area of the marker,
        fill : Fill | None, default=None
            Marker fill color.
        stroke : Stroke | Color | None, default=None
            Marker stroke style.
        color: Color | None, default=None
            Optional shorthand to set both fill and stroke color to the same value. Overrides fill and stroke and colors
        fill_opacity: float | None, default=None
            Optional shorthand fill opacity in the [0, 1] interval. Overrides fill.opacity if fill is not None.
        """
        self.shape = shape
        self.size = size
        self.fill = fill
        self.stroke = stroke
        self.color = color
        self.fill_opacity = fill_opacity


type ThemeFill = Fill[ThemeColor]
type ThemeStroke = Stroke[ThemeColor]
type ThemeMarker = Marker[ThemeColor]

type SeriesFill = Fill[SeriesColor]
type SeriesStroke = Stroke[SeriesColor]
type SeriesMarker = Marker[SeriesColor]


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
    legend-fill : Color | None, default=None
        Legend fill color.
    legend-border : Color | None, default=None
        Legend border color.
    """

    def __init__(
        self,
        *,
        background: None | Color = None,
        foreground: None | Color = None,
        grid: None | Color = None,
        legend_fill: None | Color = None,
        legend_border: None | Color = None,
    ):
        """Initialize a theme palette."""
        self.background = background
        self.foreground = foreground
        self.grid = grid
        self.legend_fill = legend_fill
        self.legend_border = legend_border


type Theme = ThemePalette | Literal[
    "light",
    "dark",
    "catppuccin-mocha",
    "catppuccin-macchiato",
    "catppuccin-frappe",
    "catppuccin-latte",
    "dracula",
    "alucard",
]
"""Explicit theme object or predefined theme name."""

type SeriesPalette = list[Color] | Literal[
    "black",
    "standard",
    "pastel",
    "tol-bright",
    "okabe-ito",
    "catppuccin-mocha",
    "catppuccin-macchiato",
    "catppuccin-frappe",
    "catppuccin-latte",
    "dracula",
    "alucard",
]
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


type BuiltinStyle = Literal[
    "black-white",
    "light",
    "dark",
    "tol-bright",
    "okabe-ito",
    "catppuccin-mocha",
    "catppuccin-macchiato",
    "catppuccin-frappe",
    "catppuccin-latte",
    "dracula",
    "alucard",
]

BUILTIN_STYLES = [
    "black-white",
    "light",
    "dark",
    "tol-bright",
    "okabe-ito",
    "catppuccin-mocha",
    "catppuccin-macchiato",
    "catppuccin-frappe",
    "catppuccin-latte",
    "dracula",
    "alucard",
]


def _parse_mpl_style(
    mpl_style: str,
) -> tuple[MarkerShape | None, Pattern | None, SeriesColor | None]:
    from ._rs import parse_color as rs_parse_color

    try:
        color = rs_parse_color(mpl_style)
        return (None, None, color)
    except ValueError:
        pass

    shape = None
    pattern = None
    color = None

    def set_shape(new_shape):
        nonlocal shape
        if shape is not None:
            raise ValueError(f"Multiple marker shapes specified in style: {mpl_style}")
        shape = new_shape

    def set_pattern(new_pattern):
        nonlocal pattern
        if pattern is not None:
            raise ValueError(
                f"Multiple marker patterns specified in style: {mpl_style}"
            )
        pattern = new_pattern

    def set_color(new_color):
        nonlocal color
        if color is not None:
            raise ValueError(f"Multiple colors specified in style: {mpl_style}")
        color = new_color

    i = 0
    while i < len(mpl_style):
        if i + 1 < len(mpl_style):
            c2 = mpl_style[i : i + 2]
            if c2 == "--":
                set_pattern("dashed")
                i += 2
                continue
            if c2 == ".-":
                set_pattern("dash-dot")
                i += 2
                continue
        c = mpl_style[i]
        if c == "o":
            set_shape("circle")
            i += 1
        elif c == "s":
            set_shape("square")
            i += 1
        elif c == "D":
            set_shape("diamond")
            i += 1
        elif c == "x":
            set_shape("cross")
            i += 1
        elif c == "+":
            set_shape("plus")
            i += 1
        elif c == "^":
            set_shape("triangle-up")
            i += 1
        elif c == "v":
            set_shape("triangle-down")
            i += 1
        elif c == "<":
            set_shape("triangle-left")
            i += 1
        elif c == ">":
            set_shape("triangle-right")
            i += 1
        elif c == "-":
            set_pattern("solid")
            i += 1
        elif c == ":":
            set_pattern("dotted")
            i += 1
        elif c == "b":
            set_color("#0000ff")
            i += 1
        elif c == "g":
            set_color("#008000")
            i += 1
        elif c == "r":
            set_color("#ff0000")
            i += 1
        elif c == "c":
            set_color("#00bfbf")
            i += 1
        elif c == "m":
            set_color("#bf00bf")
            i += 1
        elif c == "y":
            set_color("#bfbf00")
            i += 1
        elif c == "k":
            set_color("#000000")
            i += 1
        elif c == "w":
            set_color("#ffffff")
            i += 1
        elif c == "C":
            i += 1
            try:
                idx = int(mpl_style[i:])
                set_color(idx)
                break
            except ValueError:
                raise ValueError(f"Invalid color index in style: {mpl_style}")
        else:
            # Try to parse the rest as a color
            try:
                set_color(rs_parse_color(mpl_style[i:]))
                break
            except ValueError:
                raise ValueError(
                    f"Unrecognized style component '{c}' in style: {mpl_style}"
                )

    return (shape, pattern, color)
