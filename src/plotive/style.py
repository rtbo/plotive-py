from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .color import Color

type Fill = Color

@dataclass(kw_only=True)
class Stroke:
    color: Color
    width: float = 1.0
    pattern: None | list[float] = None
