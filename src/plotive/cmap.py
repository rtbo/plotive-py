from typing import Literal

from . import axis
from .color import Color
from .mapping import PvMapping
from .style import SeriesColor

type BuiltinLerpCmap = Literal["viridis", "stellar"]

type LerpMethod = Literal["nearest", "srgb", "linear", "perceptual", "xyz"]


class LerpColorMap(PvMapping):
    def __init__(
        self,
        cmap: BuiltinLerpCmap | None = None,
        stops: None | list[Color] = None,
        method: LerpMethod | None = None,
        scale: None | axis.Scale = None,
    ):
        """Initializes a colormap

        Either of cmap or stops must be provided (but not both).

        Parameters
        ----------
        cmap : str
            Colormap name.
            Can't be used with `stops` argument.
        stops : list[Color] | None, default=None
            Optional list of colors for the colormap.
            Can't be used with `cmap` argument.
        method : str | None, default="auto"
            interp method for the colormap.
            Ignored if `cmap` isn't a list of colors.
            Accepted values are:
                - "auto":
                        - If the list has fewer than 256 colors, use "linear" interp.
                        - If the list has 256 colors or more, use "nearest" interp,
                         since the colormap is already at the maximum resolution typically used for rendering.
                - None: using nearest neighbor
                - "nearest: same as None
                - "srgb" (interp in sRGB color space)
                - "fast": same as "srgb"
                - "linear" (interp in linear RGB color space)
                - "perceptual" (interp in OkLab color space)
        scale : Scale | None, default=None
            Optional scale for mapping data values to the colormap. If None, a default linear scale will be used,
            that maps the full data range to the full colormap.
        """
        self.cmap = cmap
        self.stops = stops
        self.method = method
        self.scale = scale


type CatColorMap = Literal["cat", "categorical"] | dict[str, SeriesColor]
"""A colormap that maps categorical data values to colors.
The mapping can be specified as a dictionary of {category: color} pairs,
or by using automatic category-to-color assignment with "cat" or "categorical" (both are equivalent).
In automatic mode, the colormap will assign colors to categories in the order of series colors.
"""

type LiteralColorMap = Literal["literal"]
"""A colormap that interprets data values directly as colors.
For string data, the data values are parsed as a color name, html hex code or 'rgb(...)' or rgba(...)' string.
For numeric data, the data values are interpreted as a 32-bit integer color value in RGBA format (0xRRGGBBAA).
"""

type ColorMap = Literal["auto"] | LerpColorMap | BuiltinLerpCmap | list[
    Color
] | CatColorMap | LiteralColorMap
"""A colormap that can be used for mapping data values to colors.
There are three types of colormaps:
1. Continuous colormaps (LerpColorMap, BuiltinLerpCmap, list[Color]): These colormaps are used for continuous data and interpolate colors between specified stops.
2. Categorical colormaps (CatColorMap): These colormaps are used for categorical data and map each category to a specific color.
3. Literal colormaps (LiteralColorMap): These colormaps interpret data values directly as colors.

The special value "auto" can be used to automatically select an appropriate colormap based on the data type (continuous or categorical).
"""
