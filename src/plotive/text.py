from typing import Literal

from .style import Color, Fill, Stroke, ThemeColor, ThemeFill, ThemeStroke
from .mapping import PvMapping

type BuiltinFamily = Literal["sans-serif", "serif", "monospace", "cursive", "fantasy"]

type Weight = Literal[
    "thin",
    "extra-light",
    "light",
    "normal",
    "medium",
    "semi-bold",
    "bold",
    "semibold",
    "extra-bold",
    "black",
]

type Width = Literal[
    "ultra-condensed",
    "extra-condensed",
    "condensed",
    "semi-condensed",
    "normal",
    "semi-expanded",
    "expanded",
    "extra-expanded",
    "ultra-expanded",
]

type Style = Literal["normal", "italic", "oblique"]


class TextProps(PvMapping):
    """Text rendering properties."""

    def __init__(
        self,
        *,
        family: None | str | BuiltinFamily | list[BuiltinFamily | str] = None,
        weight: None | Weight | int = None,
        width: None | Width | int = None,
        style: None | Style = None,
        size: None | float = None,
        color: None | ThemeColor | ThemeFill = None,
        outline: None | ThemeStroke | ThemeColor = None,
        underline: None | bool = None,
        strikethrough: None | bool = None,
    ):
        """Initialize text properties.

        Parameters
        ----------
        family : str | BuiltinFamily | list[BuiltinFamily | str] | None, default=None
            Font family name or list of font family names.
        weight : Weight | int | None, default=None
            Font weight. Accepted values are "thin", "extra-light", "light", "normal", "medium", "semi-bold", "bold", "extra-bold", "semibold", "black".
        width : Width | int | None, default=None
            Font width. Accepted values are "ultra-condensed", "extra-condensed", "condensed", "semi-condensed", "normal", "semi-expanded", "expanded", "extra-expanded", "ultra-expanded".
        style : str | None, default=None
            Font style. Accepted values are "normal" and "italic".
        size : float | None, default=None
            Font size in pixels.
        color : Fill | None, default=None
            Text color.
        outline : Stroke | None, default=None
            Text outline.
        underline : bool | None, default=None
            Whether the text is underlined.
        strikethrough : bool | None, default=None
            Whether the text is strikethrough.
        """
        self.family = family
        self.width = width
        self.weight = weight
        self.style = style
        self.size = size
        self.color = color
        self.outline = outline
        self.underline = underline
        self.strikethrough = strikethrough


type Text = str | list[str] | tuple[str, dict[str, TextProps]]
"""Text content. When a single is provided, it is considered as plain text.
When a list of strings or a tuple is provided, it is parsed as a rich text with optional properties for each segment.
"""
