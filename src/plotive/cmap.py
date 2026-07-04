from typing import Literal

from . import axis
from .color import Color
from .mapping import PvMapping

type BuiltinCmap = Literal["viridis", "stellar"]

type LerpMethod = Literal["nearest", "srgb", "linear", "perceptual", "xyz"]


class ColorMap(PvMapping):
    def __init__(
        self,
        cmap: BuiltinCmap,
        stops: None | list[Color] = None,
        method: LerpMethod | None = None,
        scale: None | axis.Scale = None,
    ):
        """Initializes a colormap

        Parameters
        ----------
        cmap : str
            Colormap name.
            Can't be used with `stops` and `method` argument.
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
