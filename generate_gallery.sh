#!/bin/sh

maturin develop
python examples/primes.py gallery/primes.png
python examples/bode_rlc.py gallery/bode_rlc.png
python examples/bode_rlc.py gallery/bode_rlc-mocha.png --style mocha
python examples/bode_rlc.py gallery/bode_rlc-macchiato.png --style macchiato
