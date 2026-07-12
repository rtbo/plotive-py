import plotive as pv


def get_n_primes(n):
    primes = []
    candidate = 2
    while len(primes) < n:
        is_prime = all(candidate % p != 0 for p in primes)
        if is_prime:
            primes.append(candidate)
        candidate += 1
    return primes


n = 30
primes = get_n_primes(n)
indices = list(range(1, n + 1))

data_src = {
    "primes": primes,
    "indices": indices,
}

fig = pv.Figure(
    title=f"First {n} Prime Numbers",
    plot=pv.Plot(
        series=[
            pv.series.Line(
                x="primes",
                y="indices",
                interpolation="step-late",
            )
        ],
        x_axis=pv.Axis(title="Prime", ticks="auto", grid="auto"),
        y_axis=pv.Axis(title="Index", ticks="auto", grid="auto"),
        legend="in-top-left",
    ),
)

import _common
_common.process_figure(fig, data_src, "primes")

