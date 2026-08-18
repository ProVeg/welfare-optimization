"""Unit checks: maps, slack signs, ODE finite values."""

from __future__ import annotations

import unittest
from pathlib import Path

import numpy as np

from cwo.dynamics import headcount, initial_state, rhs, slack, smooth_plus
from cwo.parameters import load_params
from cwo.simulate import constant_control, simulate
from cwo.static_nlp import solve_static

ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / "configs" / "default.yaml"


class DynamicsTests(unittest.TestCase):
    def setUp(self) -> None:
        self.p, _ = load_params(CONFIG)

    def test_smooth_plus_matches_max_at_extremes(self) -> None:
        self.assertAlmostEqual(float(smooth_plus(2.0, 1e-12)), 2.0, places=6)
        self.assertAlmostEqual(float(smooth_plus(-2.0, 1e-12)), 0.0, places=5)

    def test_headcount_rises_when_quality_rises_at_fixed_output(self) -> None:
        y = self.p.Y0
        n_low = headcount(y, 0.0, self.p.P0, self.p)
        n_high = headcount(y, self.p.Q_ecc, self.p.P0, self.p)
        self.assertGreater(n_high, n_low)

    def test_slack_positive_at_initial_condition(self) -> None:
        y, q, e, price, labor = initial_state(self.p)
        sl = slack(y, q, e, price, labor, 0.0, 0.0, self.p)
        self.assertGreater(sl["E"], 0.0)
        self.assertGreater(sl["P"], 0.0)
        self.assertGreater(sl["labor"], 0.0)
        self.assertGreater(sl["budget"], 0.0)

    def test_rhs_finite(self) -> None:
        deriv = rhs(0.0, initial_state(self.p), 0.5, 0.5, self.p)
        self.assertTrue(np.all(np.isfinite(deriv)))

    def test_bau_grows_output(self) -> None:
        tr = simulate(self.p, constant_control(0.0, 0.0), label="BAU")
        self.assertGreater(tr.Y[-1], tr.Y[0])
        self.assertTrue(np.all(np.isfinite(tr.N)))

    def test_reduction_lowers_headcount_vs_bau(self) -> None:
        bau = simulate(self.p, constant_control(0.0, 0.0), label="BAU")
        red = simulate(self.p, constant_control(0.0, 1.0), label="red")
        self.assertLess(red.N[-1], bau.N[-1])

    def test_static_optimum_obeys_inequalities(self) -> None:
        out = solve_static(self.p)
        for name, value in out.slack.items():
            self.assertGreaterEqual(value, -1e-5, msg=name)


if __name__ == "__main__":
    unittest.main()
