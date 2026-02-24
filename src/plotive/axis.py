"""Axis configuration primitives, tick locators, and formatters."""

from .style import Stroke

type AxisRef = str | int
"""
Represents a reference to an axis, either by its string ID or title or integer index.
"""

type Range = tuple[str | None, str | None]
"""
The Range type represents a range with optional start and end values.
None indicates that the bound in that direction is determined automatically.
"""


class Scale:
    """Factory namespace for axis scale strategies."""

    @classmethod
    def Auto(cls) -> "AutoScale":
        """Create an automatic scale."""
        return AutoScale()

    @classmethod
    def Lin(cls, range: Range = (None, None)) -> "LinScale":
        """Create a linear scale."""
        return LinScale(range)

    @classmethod
    def Log(cls, base: float = 10, range: Range = (None, None)) -> "LogScale":
        """Create a logarithmic scale."""
        return LogScale(base, range)

    @classmethod
    def Shared(cls, ref: AxisRef = 0) -> "SharedScale":
        """Create a scale shared with another axis."""
        return SharedScale(ref)

class AutoScale(Scale):
    """Scale whose bounds are fully determined automatically."""

    pass

class LinScale(Scale):
    """Linear scale with optional bounds."""

    def __init__(self, range: Range = (None, None)):
        """Initialize a linear scale.

        Parameters
        ----------
        range : Range, default=(None, None)
            Optional lower and upper bounds.
        """
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
        self.ref = ref


class TicksLocator:
    """Factory namespace for tick locator strategies."""

    @classmethod
    def Auto(cls) -> "AutoTicksLocator":
        """Create an automatic tick locator."""
        return AutoTicksLocator()

    @classmethod
    def MaxN(cls, bins: int = 9, steps: list[float] = [1, 2, 2.5, 5]) -> "MaxNTicksLocator":
        """Create a locator capped to a maximum number of major ticks."""
        return MaxNTicksLocator(bins, steps)

    @classmethod
    def PiMultiple(cls, bins: int = 9) -> "PiMultipleTicksLocator":
        """Create a locator in multiples of pi."""
        return PiMultipleTicksLocator(bins)

    @classmethod
    def Log(cls, base: float = 10) -> "LogTicksLocator":
        """Create a locator for logarithmic axes."""
        return LogTicksLocator(base)

    @classmethod
    def DateTime(cls, period: int = 1, unit: str = "auto") -> "DateTimeTicksLocator":
        """Create a locator for calendar datetimes."""
        return DateTimeTicksLocator(period, unit)

    @classmethod
    def TimeDelta(cls, period: int = 1, unit: str = "auto") -> "TimeDeltaTicksLocator":
        """Create a locator for time durations."""
        return TimeDeltaTicksLocator(period, unit)

class AutoTicksLocator(TicksLocator):
    """Automatically selected tick locator."""

    pass

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
        self.base = base

class DateTimeTicksLocator(TicksLocator):
    """Tick locator for date/time values."""

    def __init__(self, period: int = 1, unit: str = "auto"):
        """Initialize a datetime tick locator.

        Parameters
        ----------
        period : int, default=1
            Tick period. Ignored when ``unit='auto'``.
        unit : str, default="auto"
            Time unit: ``auto``, ``micros``, ``seconds``, ``minutes``,
            ``hours``, ``days``, ``weeks``, ``months``, or ``years``.
        """
        self.period = period
        self.unit = unit

class TimeDeltaTicksLocator(TicksLocator):
    """Tick locator for duration values."""

    def __init__(self, period: int = 1, unit: str = "auto"):
        """Initialize a timedelta tick locator.

        Parameters
        ----------
        period : int, default=1
            Tick period. Ignored when ``unit='auto'``.
        unit : str, default="auto"
            Time unit: ``auto``, ``micros``, ``seconds``, ``minutes``,
            ``hours``, or ``days``.
        """
        self.period = period
        self.unit = unit


class TicksFormatter:
    """Factory namespace for tick label formatter strategies."""

    @classmethod
    def Auto(cls) -> "AutoTicksFormatter":
        """Create an automatic formatter."""
        return AutoTicksFormatter()

    @classmethod
    def SharedAuto(cls) -> "SharedAutoTicksFormatter":
        """Create a shared automatic formatter."""
        return SharedAutoTicksFormatter()

    @classmethod
    def Decimal(cls, precision: int = 2) -> "DecimalTicksFormatter":
        """Create a decimal formatter."""
        return DecimalTicksFormatter(precision)

    @classmethod
    def Percent(cls, decimals: int | None = None) -> "PercentTicksFormatter":
        """Create a percentage formatter."""
        return PercentTicksFormatter(decimals)

    @classmethod
    def DateTime(cls, fmt: str | None = None) -> "DateTimeTicksFormatter":
        """Create a datetime formatter."""
        return DateTimeTicksFormatter(fmt)

    @classmethod
    def TimeDelta(cls, fmt: str | None = None) -> "TimeDeltaTicksFormatter":
        """Create a timedelta formatter."""
        return TimeDeltaTicksFormatter(fmt)

class AutoTicksFormatter(TicksFormatter):
    """Default automatically selected tick formatter."""

    pass

class SharedAutoTicksFormatter(TicksFormatter):
    """Automatic formatter synchronized with a shared axis."""

    pass

class DecimalTicksFormatter(TicksFormatter):
    """Decimal tick formatter with fixed precision."""

    def __init__(self, precision: int = 2):
        """Initialize a decimal formatter.

        Parameters
        ----------
        precision : int, default=2
            Number of decimal digits.
        """
        self.precision = precision

class PercentTicksFormatter(TicksFormatter):
    """Percentage tick formatter."""

    def __init__(self, decimals: int | None = None):
        """Initialize a percentage formatter.

        Parameters
        ----------
        decimals : int | None, default=None
            Optional number of decimal digits.
        """
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
        self.fmt = fmt

def _ticks_locator_from_str(s: str) -> TicksLocator:
    """Convert a string shortcut into a tick locator instance."""
    s = s.lower()
    if s == "auto":
        return TicksLocator.Auto()
    elif s.startswith("maxn"):
        bins = int(s[4:]) if len(s) > 4 else 9
        return TicksLocator.MaxN(bins)
    elif s.startswith("pimultiple"):
        bins = int(s[10:]) if len(s) > 10 else 9
        return TicksLocator.PiMultiple(bins)
    elif s.startswith("pi"):
        bins = int(s[2:]) if len(s) > 2 else 9
        return TicksLocator.PiMultiple(bins)
    elif s.startswith("log"):
        base = float(s[3:]) if len(s) > 3 else 10
        return TicksLocator.Log(base)
    elif s.startswith("datetime"):
        period_unit = s[8:].split(",") if len(s) > 8 else []
        period = int(period_unit[0]) if len(period_unit) > 0 and period_unit[0].isdigit() else 1
        unit = period_unit[1] if len(period_unit) > 1 else "auto"
        return TicksLocator.DateTime(period, unit)
    elif s.startswith("timedelta"):
        period_unit = s[9:].split(",") if len(s) > 9 else []
        period = int(period_unit[0]) if len(period_unit) > 0 and period_unit[0].isdigit() else 1
        unit = period_unit[1] if len(period_unit) > 1 else "auto"
        return TicksLocator.TimeDelta(period, unit)
    else:
        raise ValueError(f"Unknown ticks locator string: {s}")

def _get_ticks_locator(locator: TicksLocator | str) -> TicksLocator:
    """Normalize a tick locator from string or locator instance."""
    if isinstance(locator, str):
        return _ticks_locator_from_str(locator)
    elif isinstance(locator, TicksLocator):
        return locator
    else:
        raise ValueError(f"Invalid ticks locator specification: {locator}")

class Ticks:
    """Major tick configuration for an axis."""

    def __init__(
        self,
        locator: TicksLocator | str = TicksLocator.Auto(),
        formatter: TicksFormatter = TicksFormatter.Auto(),
    ):
        """Initialize major tick location and formatting settings.

        Parameters
        ----------
        locator : TicksLocator | str, default=TicksLocator.Auto()
            Tick locator configuration.
        formatter : TicksFormatter, default=TicksFormatter.Auto()
            Tick label formatter configuration.
        """
        self.locator = _get_ticks_locator(locator)
        self.formatter = formatter

class Axis:
    """Full axis definition for a plot."""

    def __init__(
        self,
        *,
        title: str | None = None,
        id: str | None = None,
        scale: Scale | str = AutoScale(),
        opposite_side: bool | None = None,
        side: str | None = None,
        ticks: Ticks | str | None = None,
        grid: Stroke | str | None = None,
        minor_ticks: TicksLocator | str | None = None,
        minor_grid: Stroke | str | None = None,
    ):
        """Initialize an axis and normalize rendering options.

        Parameters
        ----------
        title : str | None, default=None
            Axis title.
        id : str | None, default=None
            Axis identifier.
        scale : Scale | str, default=AutoScale()
            Scale strategy or string shortcut.
        opposite_side : bool | None, default=None
            Put axis on the opposite side.
        side : str | None, default=None
            Explicit side: ``left``, ``right``, ``top``, or ``bottom``.
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
        if isinstance(scale, str):
            if scale.lower() == "auto":
                self.scale = AutoScale()
            elif scale.lower() == "lin":
                self.scale = LinScale()
            elif scale.lower() == "log":
                self.scale = LogScale()
            else:
                self.scale = SharedScale(scale)
        else:
            self.scale = scale

        if opposite_side is not None and side is not None:
            raise ValueError("Cannot specify both 'opposite_side' and 'side'.")
        if side is not None:
            if side.lower() in ["left", "right", "top", "bottom"]:
                self._side = side.lower()
            else:
                raise ValueError(f"Invalid side value: {side}. Must be 'left', 'right', 'top' or 'bottom'.")
            self.opposite_side = (side == "right" or side == "top")
        elif opposite_side is not None:
            self.opposite_side = opposite_side
        else:
            self.opposite_side = False

        if isinstance(ticks, str):
            self.ticks = Ticks(locator=_get_ticks_locator(ticks))
        elif isinstance(ticks, Ticks):
            self.ticks = ticks
        elif ticks is None:
            self.ticks = None

        if isinstance(grid, str):
            if grid.lower() == "auto":
                self.grid = Stroke(color="grid")
            else:
                self.grid = Stroke(color=grid)
        else:
            self.grid = grid

        if minor_ticks is not None:
            self.minor_ticks = _get_ticks_locator(minor_ticks)
        else:
            self.minor_ticks = None

        if isinstance(minor_grid, str):
            if minor_grid.lower() == "auto":
                self.minor_grid = Stroke(color="grid", width=0.5, pattern=[5, 5])
            else:
                self.minor_grid = Stroke(color=minor_grid, width=0.5, pattern=[5, 5])
        else:
            self.minor_grid = minor_grid
