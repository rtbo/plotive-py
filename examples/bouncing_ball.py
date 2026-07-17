import numpy as np
import pandas as pd
from scipy.integrate import odeint
import plotive as pv

START_HEIGHT = 60.0
BOUNCE_RESTITUTION = 0.76


def bouncing_ball(y, _t):
    # approximate parameters for a tennis ball
    # drag coefficient
    cd = 0.5
    # ball mass
    m = 0.058
    # ball diameter
    d = 0.065
    # frontal surface
    s = 3.14159 * d * d / 4.0
    # air density
    rho = 1.225
    # gravity constant
    g = 9.81

    vel = y[1]
    drag_force = 0.5 * rho * vel * vel * s * cd

    drag_direction = 1 if vel >= 0 else -1

    dy = [0, 0]
    dy[0] = y[1]
    dy[1] = -g - drag_direction * drag_force / m

    return dy


def calc_data():
    data = {
        "time": [],
        "height": [],
        "velocity": [],
    }

    t0 = 0.0
    t_end = 10.0
    t = np.linspace(t0, t_end, 500)

    y0 = [START_HEIGHT, 0.0]

    bounce = 1
    MAX_BOUNCE = 10

    while True:
        y = odeint(bouncing_ball, y0, t)
        rebounce = np.where(y[:, 0] <= 0.0)[0]
        rebounce = rebounce[0] if len(rebounce) > 0 else None
        last_i = rebounce if rebounce is not None else len(t) - 1
        bounce_t = t[: last_i + 1]
        bounce_y = y[: last_i + 1]
        data["time"].extend(bounce_t)
        data["height"].extend(bounce_y[:, 0])
        data["velocity"].extend(bounce_y[:, 1])

        t = t[last_i + 1 :]
        if len(t) == 0:
            break
        bounce += 1
        if bounce > MAX_BOUNCE:
            break
        y0 = bounce_y[-1]
        y0[0] = abs(y0[0])
        y0[1] *= -BOUNCE_RESTITUTION

    return pd.DataFrame(data)


data = calc_data()

title = "Tennis ball thrown from 1\u02e2\u1d57 floor of Eiffel Tower"
fig = pv.Figure(
    title=title,
    plot=pv.Plot(
        series=[
            pv.series.Line(
                x="time",
                y="height",
                name="Height (m)",
            ),
            pv.series.Line(
                x="time",
                y="velocity",
                name="Velocity (m/s)",
            ),
        ],
        x_axis=pv.Axis(
            title="Time",
            ticks=pv.axis.Ticks(
                locator=pv.axis.TimeDeltaTicksLocator((2, "secs")),
                formatter=pv.axis.TimeDeltaTicksFormatter(fmt="%M:%S"),
            ),
            grid="auto",
        ),
        y_axis=pv.Axis(
            title="Height / Velocity",
            ticks="auto",
            grid="auto",
        ),
        legend="in-top-right",
    ),
)

import _common

_common.process_figure(fig, data, "bouncing-ball")
