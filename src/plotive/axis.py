"""Axis configuration primitives, tick locators, and formatters."""

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

class Scale:
    """Defines how data is mapped to axis coordinates."""

    @staticmethod
    def _normalize(scale: Scale | Range | str) -> Scale:
        if isinstance(scale, Scale):
            return scale
        elif isinstance(scale, tuple) and len(scale) == 2:
            return LinScale(range=scale)
        elif isinstance(scale, str):
            scalel = scale.lower()
            if scalel == "auto":
                return AutoScale()
            elif scalel == "lin":
                return LinScale()
            elif scalel == "log":
                return LogScale()
            else:
                return SharedScale(scale)
        else:
            raise ValueError(f"Invalid scale specification: {scale}")


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
    """Defines strategy to locate ticks on an axis"""

    @staticmethod
    def _normalize(ticks: TicksLocator | list[float] | list[int] | str):
        if isinstance(ticks, TicksLocator):
            return ticks
        elif isinstance(ticks, str):
            ticksl = ticks.lower()
            if ticksl == "auto":
                return AutoTicksLocator()
            elif ticksl == "maxn":
                return MaxNTicksLocator()
            elif ticksl == "pimultiple":
                return PiMultipleTicksLocator()
            elif ticksl == "log":
                return LogTicksLocator()
            elif ticksl == "datetime":
                return DateTimeTicksLocator()
            elif ticksl == "timedelta":
                return TimeDeltaTicksLocator()
            else:
                raise ValueError(f"Invalid ticks locator specification: {ticks}")
        elif isinstance(ticks, list):
            return ListTicksLocator(ticks)
        else:
            raise ValueError(f"Invalid ticks locator specification: {ticks}")


class AutoTicksLocator(TicksLocator):
    """Automatically selected tick locator."""

    pass


class ListTicksLocator(TicksLocator):
    """Ticks location specified by a list"""

    def __init__(self, ticks: list[float] | list[int]):
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
    """Defines strategy to format tick labels on an axis"""

    @staticmethod
    def _normalize(formatter: TicksFormatter | str):
        if isinstance(formatter, TicksFormatter):
            return formatter
        elif isinstance(formatter, str):
            formatterl = formatter.lower()
            if formatterl == "auto":
                return AutoTicksFormatter()
            elif formatterl == "percent":
                return PercentTicksFormatter()
            elif formatterl == "decimal":
                return DecimalTicksFormatter()
            elif formatterl == "datetime":
                return DateTimeTicksFormatter()
            elif formatterl == "timedelta":
                return TimeDeltaTicksFormatter()
            else:
                raise ValueError(f"Invalid ticks formatter specification: {formatter}")
        else:
            raise ValueError(f"Invalid ticks formatter specification: {formatter}")

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


class Ticks:
    """Major tick configuration for an axis."""

    def __init__(
        self,
        locator: TicksLocator | list[float] | list[int] | str = "auto",
        formatter: TicksFormatter | str = "auto",
        label_props: None | TextProps = None,
        color: None | Color = None
    ):
        """Initialize major tick location and formatting settings.

        Parameters
        ----------
        locator : TicksLocator | list[float] | list[int] | str, default="auto"
            Tick locator configuration.
        formatter : TicksFormatter | str, default="auto
            Tick label formatter configuration.
        """
        self.locator = TicksLocator._normalize(locator)
        self.formatter = TicksFormatter._normalize(formatter)
        self.label_props = label_props
        self.color = color

    @staticmethod
    def _normalize(input: Ticks | TicksLocator | list[float] | list[int] | TicksFormatter | str):
        if isinstance(input, Ticks):
            return input
        elif isinstance(input, TicksLocator):
            return Ticks(locator=input)
        elif isinstance(input, TicksFormatter):
            return Ticks(formatter=input)
        elif isinstance(input, str):
            inputl = input.lower()
            if inputl == "auto":
                return Ticks(locator=AutoTicksLocator(), formatter=AutoTicksFormatter())
            elif inputl == "maxn":
                return Ticks(locator=MaxNTicksLocator())
            elif inputl == "pimultiple" or inputl == "pi":
                return Ticks(locator=PiMultipleTicksLocator())
            elif inputl == "log":
                return Ticks(locator=LogTicksLocator())
            elif inputl == "percent":
                return Ticks(formatter=PercentTicksFormatter())
            elif inputl == "decimal":
                return Ticks(formatter=DecimalTicksFormatter())
            elif inputl == "datetime":
                return Ticks(locator=DateTimeTicksLocator(), formatter=DateTimeTicksFormatter())
            elif inputl == "timedelta":
                return Ticks(locator=TimeDeltaTicksLocator(), formatter=TimeDeltaTicksFormatter())
            else:
                raise ValueError(f"Invalid ticks specification: {input}")
        elif isinstance(input, list):
            return Ticks(locator=input)
        else:
            raise ValueError(f"Invalid ticks specification: {input}")


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

    @staticmethod
    def _normalize(grid: Grid | Stroke | str):
        if isinstance(grid, Grid):
            return grid
        elif isinstance(grid, Stroke):
            return grid
        elif isinstance(grid, str):
            if grid.lower() == "auto":
                return Grid()
            else:
                return Grid(color=grid)
        else:
            raise ValueError(f"Invalid grid specification: {grid}")


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

    @staticmethod
    def _normalize(grid: MinorGrid | Stroke | str):
        if isinstance(grid, MinorGrid):
            return grid
        elif isinstance(grid, Stroke):
            return grid
        elif isinstance(grid, str):
            if grid.lower() == "auto":
                return MinorGrid()
            else:
                return MinorGrid(color=grid)
        else:
            raise ValueError(f"Invalid grid specification: {grid}")


class Axis:
    """Full axis definition for a plot."""

    def __init__(
        self,
        *,
        title: str | None = None,
        id: str | None = None,
        scale: Scale | str | Range = "auto",
        opposite_side: bool | None = None,
        side: str | None = None,
        ticks: Ticks | TicksLocator | list[float] | list[int] | TicksFormatter | str | None = None,
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
        self.scale = Scale._normalize(scale)

        if opposite_side is not None and side is not None:
            raise ValueError("Cannot specify both 'opposite_side' and 'side'.")
        if side is not None:
            sidel = side.lower()
            if sidel in ["left", "right", "top", "bottom"]:
                self._side = sidel
            else:
                raise ValueError(
                    f"Invalid side value: {side}. Must be 'left', 'right', 'top' or 'bottom'."
                )
            self.opposite_side = sidel == "right" or sidel == "top"
        elif opposite_side is not None:
            self.opposite_side = opposite_side
        else:
            self.opposite_side = False

        self.ticks = Ticks._normalize(ticks) if ticks is not None else None

        self.grid = Grid._normalize(grid) if grid is not None else None

        self.minor_ticks = TicksLocator._normalize(minor_ticks) if minor_ticks is not None else None

        self.minor_grid = MinorGrid._normalize(minor_grid) if minor_grid is not None else None
