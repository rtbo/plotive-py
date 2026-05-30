"""Global styling primitives for figures and series."""

from typing import Literal

from ._rs import parse_color as _parse_color

type Color = str | tuple[float, float, float] | tuple[float, float, float, float]
"""
Named string or Hex string or RGB(A) tuple.
Tuples are expressed in sRGB color space with components in the [0, 1] interval.
String can either be a named color from the CSS color specification, or the XKCD color survey,
or a hex color code in the form "#RGB", "#RGBA", "#RRGGBB" or "#RRGGBBAA" (both lower and upper case hex accepted).

Colors can be used either in the context of a theme (foreground, background, grid, etc.) or in the context of a series palette.
In a theme context, color strings can also refer to theme color names ("background", "foreground", "grid", "legend-fill" and "legend-border").
In a series palette context, color strings can also refer to a color in the series palette by index (e.g. "C0" for the first color, "C1" for the second etc.)
The special string "auto" can be used in both contexts to refer to the default color for the context.
"""

type Pattern = list[float] | list[int] | Literal["solid", "dashed", "dotted", "dash-dot"]
"""Line pattern specification, either as a list of dash/gap lengths in pixels or as a predefined pattern name."""


class Fill:
    """Type alias for fill colors."""

    def __init__(self, color: Color = "auto", *, opacity: float | None = None):
        """Initialize a fill color.

        Parameters
        ----------
        color : Color, default="auto"
            Fill color. "auto" means that the default color for the context will be used.
        opacity : float | None, default=None
            Fill opacity in the ``[0, 1]`` interval.
            None means opaque.
        """
        self.color = color
        self.opacity = opacity

    @staticmethod
    def _normalize(input: Fill | Color) -> Fill:
        """Normalize a fill specification to a ThemeFill object."""
        if isinstance(input, Fill):
            return Fill(color=input.color, opacity=input.opacity)
        else:
            return Fill(color=input)


class Stroke:
    """Line stroke style."""

    def __init__(
        self,
        color: Color = "auto",
        *,
        width: float | None = None,
        pattern: Pattern | None = None,
        opacity: float | None = None,
    ):
        """Initialize a stroke style.


        Parameters
        ----------
        color : Color, default="auto"
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

    @staticmethod
    def _normalize(
        input: Stroke | Color, default_width: float
    ) -> Stroke:
        """Normalize a stroke specification to a ThemeStroke object."""
        if isinstance(input, Stroke):
            return Stroke(
                color=input.color,
                width=input.width if input.width is not None else default_width,
                pattern=input.pattern, # type: ignore[arg-type]
                opacity=input.opacity,
            )
        else:
            return Stroke(color=input, width=default_width)


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


class Marker:
    """Marker style for scatter series."""

    def __init__(
        self,
        *,
        shape: MarkerShape = "circle",
        size: float = 8.5**2,
        fill: None | Fill | Color = "auto",
        stroke: None | Stroke | Color = "auto",
        color: None | Color = None,
        fill_opacity: None | float = None,
    ):
        """Initialize a marker style.

        Parameters
        ----------
        shape : MarkerShape
            Marker shape. One of "circle", "square", "diamond", "cross", "plus", "triangle-up", "triangle-down", "triangle-left", "triangle-right".
        size : float, default=10.0
            Marker size in pixels.
        fill : Fill | None, default="auto"
            Marker fill color.
        stroke : Stroke | Color | None, default="auto"
            Marker stroke style.
        color: Color | None, default=None
            Optional shorthand to set both fill and stroke color to the same value. Overrides fill and stroke and colors
        fill_opacity: float | None, default=None
            Optional shorthand fill opacity in the [0, 1] interval. Overrides fill.opacity if fill is not None.
        """
        self.shape = shape
        self.size = size
        self.fill = Fill._normalize(fill) if fill is not None else None
        self.stroke = Stroke._normalize(stroke, default_width=1.5) if stroke is not None else None
        if color is not None:
            if self.fill is None:
                self.fill = Fill(color=color)
            else:
                self.fill.color = color
            if self.stroke is None:
                self.stroke = Stroke(color=color)
            else:
                self.stroke.color = color
        if self.fill and fill_opacity is not None:
            self.fill.opacity = fill_opacity


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


def _parse_mpl_style(
    mpl_style: str,
) -> tuple[MarkerShape | None, Pattern | None, Color | None]:
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
