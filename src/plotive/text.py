
from .style import Color, Fill, Stroke


class TextProps:
    """Text rendering properties."""

    def __init__(
        self,
        *,
        family: None | str | list[str] = None,
        weight: None | str | int = None,
        width: None | str | int = None,
        style: None | str = None,
        size: None | float = None,
        color: None | Fill = None,
        outline: None | Stroke | Color = None,
        underline: None | bool = None,
        strikethrough: None | bool = None,
    ):
        """Initialize text properties.

        Parameters
        ----------
        family : str | list[str] | None, default=None
            Font family name or list of font family names.
        weight : str | int | None, default=None
            Font weight. Accepted values are "normal", "bold", "light", "ultralight", "semibold", "heavy" and "black".
        width : str | int | None, default=None
            Font width. Accepted values are "normal", "condensed", "expanded", "ultracondensed", "semicondensed", "semiexpanded", "ultraexpanded" and "extraexpanded".
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
        self.size = size
        self.color = Fill._normalize(color) if color is not None else None
        self.weight = weight
        self.style = style
        self.outline = Stroke._normalize(outline, default_width=1.0) if outline is not None else None
        self.underline = underline
        self.strikethrough = strikethrough

type Text = str | list[str] | tuple[str, dict[str, TextProps]]
"""Text content. When a single is provided, it is considered as plain text.
When a list of strings or a tuple is provided, it is parsed as a rich text with optional properties for each segment.
"""
