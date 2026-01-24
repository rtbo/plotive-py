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
    @classmethod
    def Auto(cls) -> "AutoScale":
        return AutoScale()

    @classmethod
    def Lin(cls, range: Range = (None, None)) -> "LinScale":
        return LinScale(range)

    @classmethod
    def Log(cls, base: float = 10, range: Range = (None, None)) -> "LogScale":
        return LogScale(base, range)

    @classmethod
    def Shared(cls, ref: AxisRef = 0) -> "SharedScale":
        return SharedScale(ref)

class AutoScale(Scale):
    pass

class LinScale(Scale):
    def __init__(self, range: Range = (None, None)):
        self.range = range


class LogScale(Scale):
    def __init__(self, base: float = 10, range: Range = (None, None)):
        self.base = base
        self.range = range


class SharedScale(Scale):
    def __init__(self, ref: AxisRef = 0):
        self.ref = ref


class TicksLocator:
    @classmethod
    def Auto(cls) -> "AutoTicksLocator":
        return AutoTicksLocator()

    @classmethod
    def MaxN(cls, bins: int = 9, steps: list[float] = [1, 2, 2.5, 5]) -> "MaxNTicksLocator":
        return MaxNTicksLocator(bins, steps)

    @classmethod
    def PiMultiple(cls, bins: int = 9) -> "PiMultipleTicksLocator":
        return PiMultipleTicksLocator(bins)

    @classmethod
    def Log(cls, base: float = 10) -> "LogTicksLocator":
        return LogTicksLocator(base)

    @classmethod
    def DateTime(cls, period: int = 1, unit: str = "auto") -> "DateTimeTicksLocator":
        return DateTimeTicksLocator(period, unit)

    @classmethod
    def TimeDelta(cls, period: int = 1, unit: str = "auto") -> "TimeDeltaTicksLocator":
        return TimeDeltaTicksLocator(period, unit)

class AutoTicksLocator(TicksLocator):
    pass

class MaxNTicksLocator(TicksLocator):
    def __init__(self, bins: int = 9, steps: list[float] = [1, 2, 2.5, 5]):
        self.bins = bins
        self.steps = steps

class PiMultipleTicksLocator(TicksLocator):
    def __init__(self, bins: int = 9):
        self.bins = bins

class LogTicksLocator(TicksLocator):
    def __init__(self, base: float = 10):
        self.base = base

class DateTimeTicksLocator(TicksLocator):
    def __init__(self, period: int = 1, unit: str = "auto"):
        """
        period: The period between ticks. Ignored if unit is "auto".
        unit: The unit of period for the ticks. Can be "auto", "micros", "seconds", "minutes", "hours", "days", "weeks", "months", or "years".
        """
        self.period = period
        self.unit = unit

class TimeDeltaTicksLocator(TicksLocator):
    def __init__(self, period: int = 1, unit: str = "auto"):
        """
        period: The period between ticks. Ignored if unit is "auto".
        unit: The unit of period for the ticks. Can be "auto", "micros", "seconds", "minutes", "hours" or "days".
        """
        self.period = period
        self.unit = unit


class TicksFormatter:
    @classmethod
    def Auto(cls) -> "AutoTicksFormatter":
        return AutoTicksFormatter()

    @classmethod
    def SharedAuto(cls) -> "SharedAutoTicksFormatter":
        return SharedAutoTicksFormatter()

    @classmethod
    def Decimal(cls, precision: int = 2) -> "DecimalTicksFormatter":
        return DecimalTicksFormatter(precision)

    @classmethod
    def Percent(cls, decimals: int | None = None) -> "PercentTicksFormatter":
        return PercentTicksFormatter(decimals)

    @classmethod
    def DateTime(cls, fmt: str | None = None) -> "DateTimeTicksFormatter":
        return DateTimeTicksFormatter(fmt)

    @classmethod
    def TimeDelta(cls, fmt: str | None = None) -> "TimeDeltaTicksFormatter":
        return TimeDeltaTicksFormatter(fmt)

class AutoTicksFormatter(TicksFormatter):
    pass

class SharedAutoTicksFormatter(TicksFormatter):
    pass

class DecimalTicksFormatter(TicksFormatter):
    def __init__(self, precision: int = 2):
        self.precision = precision

class PercentTicksFormatter(TicksFormatter):
    def __init__(self, decimals: int | None = None):
        self.decimals = decimals

class DateTimeTicksFormatter(TicksFormatter):
    def __init__(self, fmt: str | None = None):
        self.fmt = fmt

class TimeDeltaTicksFormatter(TicksFormatter):
    def __init__(self, fmt: str | None = None):
        self.fmt = fmt

def _ticks_locator_from_str(s: str) -> TicksLocator:
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
    if isinstance(locator, str):
        return _ticks_locator_from_str(locator)
    elif isinstance(locator, TicksLocator):
        return locator
    else:
        raise ValueError(f"Invalid ticks locator specification: {locator}")

class Ticks:
    def __init__(
        self,
        locator: TicksLocator | str = TicksLocator.Auto(),
        formatter: TicksFormatter = TicksFormatter.Auto(),
    ):
        self.locator = _get_ticks_locator(locator)
        self.formatter = formatter

class Axis:
    def __init__(
        self,
        *,
        title: str | None = None,
        id: str | None = None,
        scale: Scale | str = AutoScale(),
        opposite_side: bool = False,
        ticks: Ticks | str | None = None,
        grid: Stroke | str | None = None,
        minor_ticks: TicksLocator | str | None = None,
        minor_grid: Stroke | str | None = None,
    ):
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
        self.opposite_side = opposite_side

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
