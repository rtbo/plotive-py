"""Axis configuration primitives, tick locators, and formatters."""

from abc import ABC
from typing import Literal

from .mapping import PvMapping
from .text import TextProps

from .style import Color, Pattern, Stroke

type AxisRef = str | int
"""
Represents a reference to an axis, either by its string ID or title or integer index.
"""

type Range = tuple[float | None, float | None]
"""
The Range type represents a range with optional start and end values.
None indicates that the bound in that direction is determined automatically.
"""


class Scale(ABC, PvMapping):
    """Defines how data is mapped to axis coordinates."""

    pass


class AutoScale(Scale):
    """Scale whose bounds are fully determined automatically."""

    def __init__(self):
        self.type = "auto"


class LinScale(Scale):
    """Linear scale with optional bounds."""

    def __init__(self, range: Range = (None, None)):
        """Initialize a linear scale.

        Parameters
        ----------
        range : Range, default=(None, None)
            Optional lower and upper bounds.
        """
        self.type = "lin"
        self.range = range


class LogScale(Scale):
    """Logarithmic scale with configurable base."""

    def __init__(self, base: float = 10, range: Range = (None, None)):
        """Initialize a logarithmic scale.

        Parameters
        ----------
        base : float, default=10
            Logarithm base.
        range : Range, default=(None, None)
            Optional lower and upper bounds.
        """
        self.type = "log"
        self.base = base
        self.range = range


class SharedScale(Scale):
    """Scale that reuses limits from a reference axis."""

    def __init__(self, ref: AxisRef = 0):
        """Initialize a shared scale.

        Parameters
        ----------
        ref : AxisRef, default=0
            Reference axis id or index.
        """
        self.type = "shared"
        self.ref = ref


class TicksLocator(PvMapping):
    """Defines strategy to locate ticks on an axis"""

    pass


class AutoTicksLocator(TicksLocator):
    """Automatically selected tick locator."""

    def __init__(self):
        self.type = "auto"


class ListTicksLocator(TicksLocator):
    """Ticks location specified by a list"""

    def __init__(self, ticks: list[float] | list[int]):
        self.type = "list"
        self.ticks = ticks


class MaxNTicksLocator(TicksLocator):
    """Tick locator limiting the number of major ticks."""

    def __init__(self, bins: int = 9, steps: list[float] = [1, 2, 2.5, 5]):
        """Initialize a MaxN tick locator.

        Parameters
        ----------
        bins : int, default=9
            Maximum number of major tick bins.
        steps : list[float], default=[1, 2, 2.5, 5]
            Allowed step multipliers.
        """
        self.type = "maxn"
        self.bins = bins
        self.steps = steps


class PiMultipleTicksLocator(TicksLocator):
    """Tick locator using multiples of pi."""

    def __init__(self, bins: int = 9):
        """Initialize a pi-multiple tick locator.

        Parameters
        ----------
        bins : int, default=9
            Maximum number of major tick bins.
        """
        self.type = "pimultiple"
        self.bins = bins


class LogTicksLocator(TicksLocator):
    """Tick locator for logarithmic scales."""

    def __init__(self, base: float = 10):
        """Initialize a logarithmic tick locator.

        Parameters
        ----------
        base : float, default=10
            Logarithm base.
        """
        self.type = "log"
        self.base = base


type DateTimeUnit = Literal[
    "year",
    "years",
    "month",
    "months",
    "week",
    "weeks",
    "day",
    "days",
    "hour",
    "hours",
    "min",
    "mins",
    "sec",
    "secs",
    "milli",
    "millis",
    "micro",
    "micros",
]

class DateTimeTicksLocator(TicksLocator):
    """Tick locator for date/time values."""

    def __init__(self, period: tuple[int, DateTimeUnit] | None = None):
        """Initialize a datetime tick locator.

        Parameters
        ----------
        period : tuple[int, DateTimeUnit] | None, default=None
            Tick period and unit. Ignored when ``period=None``.
        """
        self.type = "datetime"
        self.period = period

type TimeDeltaUnit = Literal[
    "day",
    "days",
    "hour",
    "hours",
    "min",
    "mins",
    "sec",
    "secs",
    "milli",
    "millis",
    "micro",
    "micros",
]

class TimeDeltaTicksLocator(TicksLocator):
    """Tick locator for duration values."""

    def __init__(self, period: tuple[int, TimeDeltaUnit] | None = None):
        """Initialize a timedelta tick locator.

        Parameters
        ----------
        period : tuple[int, TimeDeltaUnit] | None, default=None
            Tick period and unit. Ignored when ``period=None``.
        """
        self.type = "timedelta"
        self.period = period


class TicksFormatter(PvMapping):
    """Defines strategy to format tick labels on an axis"""

    pass


class AutoTicksFormatter(TicksFormatter):
    """Default automatically selected tick formatter."""

    def __init__(self):
        self.type = "auto"


class SharedAutoTicksFormatter(TicksFormatter):
    """Automatic formatter synchronized with a shared axis."""

    def __init__(self):
        self.type = "shared-auto"


class DecimalTicksFormatter(TicksFormatter):
    """Decimal tick formatter with fixed precision."""

    def __init__(self, decimals: int | None = None):
        """Initialize a decimal formatter.

        Parameters
        ----------
        decimals : int | None, default=None
            Number of decimal digits (None means automatic).
        """
        self.type = "decimal"
        self.decimals = decimals


class PercentTicksFormatter(TicksFormatter):
    """Percentage tick formatter."""

    def __init__(self, decimals: int | None = None):
        """Initialize a percentage formatter.

        Parameters
        ----------
        decimals : int | None, default=None
            Optional number of decimal digits (None means automatic).
        """
        self.type = "percent"
        self.decimals = decimals


class DateTimeTicksFormatter(TicksFormatter):
    """Tick formatter for calendar datetime labels."""

    def __init__(self, fmt: str | None = None):
        """Initialize a datetime formatter.

        Parameters
        ----------
        fmt : str | None, default=None
            Datetime formatting string.
        """
        self.type = "datetime"
        self.fmt = fmt


class TimeDeltaTicksFormatter(TicksFormatter):
    """Tick formatter for duration labels."""

    def __init__(self, fmt: str | None = None):
        """Initialize a timedelta formatter.

        Parameters
        ----------
        fmt : str | None, default=None
            Timedelta formatting string.
        """
        self.type = "timedelta"
        self.fmt = fmt


class Ticks(PvMapping):
    """Major tick configuration for an axis."""

    def __init__(
        self,
        locator: TicksLocator | list[float] | list[int] | str = "auto",
        formatter: TicksFormatter | str = "auto",
        label_props: None | TextProps = None,
        color: None | Color = None,
    ):
        """Initialize major tick location and formatting settings.

        Parameters
        ----------
        locator : TicksLocator | list[float] | list[int] | str, default="auto"
            Tick locator configuration.
        formatter : TicksFormatter | str, default="auto
            Tick label formatter configuration.
        """
        self.locator = locator
        self.formatter = formatter
        self.label_props = label_props
        self.color = color


class Grid(Stroke):
    """Major grid configuration for an axis"""

    def __init__(
        self,
        *,
        color: Color = "grid",
        width: float = 1.0,
        pattern: None | Pattern = "solid",
        opacity: float = 0.6,
    ):
        """Initialize a grid style."""
        super().__init__(color=color, width=width, pattern=pattern, opacity=opacity)


class MinorGrid(Stroke):
    """Minor grid configuration for an axis"""

    def __init__(
        self,
        *,
        color: Color = "grid",
        width: float = 0.5,
        pattern: None | Pattern = "dashed",
        opacity: float = 0.6,
    ):
        """Initialize a grid style."""
        super().__init__(color=color, width=width, pattern=pattern, opacity=opacity)


type AxisSide = Literal["main", "opposite", "left", "right", "top", "bottom"]


class Axis(PvMapping):
    """Full axis definition for a plot."""

    def __init__(
        self,
        *,
        title: str | None = None,
        id: str | None = None,
        scale: Scale | str | Range = "auto",
        side: AxisSide = "main",
        ticks: (
            Ticks | TicksLocator | list[float] | list[int] | TicksFormatter | str | None
        ) = None,
        grid: Grid | Stroke | str | None = None,
        minor_ticks: TicksLocator | str | None = None,
        minor_grid: MinorGrid | Stroke | str | None = None,
    ):
        """Initialize an axis and normalize rendering options.

        Parameters
        ----------
        title : str | None, default=None
            Axis title.
        id : str | None, default=None
            Axis identifier.
        scale : Scale | str | Range, default="auto"
            Scale strategy or string shortcut.
        side : AxisSide, default="main"
            Axis side: ``main``, ``opposite``, ``left``, ``right``, ``top``, or ``bottom``.
        ticks : Ticks | str | None, default=None
            Major tick configuration.
        grid : Stroke | str | None, default=None
            Major grid style.
        minor_ticks : TicksLocator | str | None, default=None
            Minor tick locator.
        minor_grid : Stroke | str | None, default=None
            Minor grid style.

        Raises
        ------
        ValueError
            If incompatible side options are provided.
        """
        self.title = title
        self.id = id
        self.scale = scale
        self.side = side
        self.ticks = ticks
        self.grid = grid
        self.minor_ticks = minor_ticks
        self.minor_grid = minor_grid
