type Color = str | tuple[float, float, float] | tuple[float, float, float, float]
"""
Named string or Hex string or RGB(A) tuple.
Tuples are expressed in sRGB color space with components in the [0, 1] interval.
String can either be a named color from the CSS color specification, or the XKCD color survey.
Color can also be strings in the form of 'rgb(r, g, b)' or 'rgba(r, g, b, a)' where r, g and b are integers in the [0, 255] interval and a is a float in the [0, 1] interval.
Color can also be a hex color code in the form "#RGB", "#RGBA", "#RRGGBB" or "#RRGGBBAA" (both lower and upper case hex accepted).
"""
