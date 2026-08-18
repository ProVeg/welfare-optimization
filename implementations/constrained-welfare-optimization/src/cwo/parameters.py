"""Load YAML parameters, scenario overlays, and CLI key=value overrides."""

from __future__ import annotations

import copy
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml


def _deep_update(base: dict, overlay: dict) -> dict:
    out = copy.deepcopy(base)
    for key, value in overlay.items():
        if isinstance(value, dict) and isinstance(out.get(key), dict):
            out[key] = _deep_update(out[key], value)
        else:
            out[key] = copy.deepcopy(value)
    return out


def _set_dotted(cfg: dict, dotted: str, value: Any) -> None:
    keys = dotted.split(".")
    cur = cfg
    for key in keys[:-1]:
        if key not in cur or not isinstance(cur[key], dict):
            cur[key] = {}
        cur = cur[key]
    raw = value
    if isinstance(raw, str):
        try:
            raw = yaml.safe_load(raw)
        except yaml.YAMLError:
            pass
    cur[keys[-1]] = raw


def load_yaml(path: Path) -> dict:
    with path.open(encoding="utf-8") as handle:
        data = yaml.safe_load(handle)
    if not isinstance(data, dict):
        raise ValueError(f"Expected a mapping in {path}")
    return data


@dataclass(frozen=True)
class Params:
    """Aggregate small-bodied model parameters. Units are in field names / comments."""

    t0: float
    T: float
    n_points: int
    fsb_year: float
    N0: float
    pi0: float
    kappa_pi: float
    r: float
    epsilon: float
    s_coeff: float
    Q0: float
    Q_max: float
    Q_ecc: float
    omega: float
    phi_conv: float
    phi_hw: float
    rho: float
    P0: float
    P_lim: float
    h_exp: float
    h_ecc: float
    psi: float
    smooth_eps: float
    E0: float
    E_lim: float
    kappa: float
    alpha_E: float
    delta_E: float
    beta: float
    gamma: float
    L0: float
    xi_lim: float
    xi_star: float
    sigma0: float
    sigma_p: float
    delta_L: float
    theta_L: float
    lambda_D: float
    eta_W: float
    c_W: float
    c_D: float
    B: float
    ivp_method: str
    ivp_rtol: float
    ivp_atol: float
    ocp_nodes: int
    ocp_max_iter: int
    slsqp_pieces: int
    static_alpha_max_k: float

    @property
    def horizon_years(self) -> float:
        return self.T - self.t0

    @property
    def Y0(self) -> float:
        """Edible kg / year at t0 with S(P0)=1 and Q=Q0."""
        return self.N0 * self.productivity(self.Q0)

    def productivity(self, quality: float) -> float:
        """Edible kg per standing-animal-year, falling in quality."""
        return self.pi0 / (1.0 + self.kappa_pi * quality)

    def as_dict(self) -> dict:
        return {key: getattr(self, key) for key in self.__dataclass_fields__}


def params_from_mapping(raw: dict) -> Params:
    h = raw.get("horizon", {})
    return Params(
        t0=float(h.get("t0", raw.get("t0"))),
        T=float(h.get("T", raw.get("T"))),
        n_points=int(h.get("n_points", raw.get("n_points", 241))),
        fsb_year=float(h.get("fsb_year", raw.get("fsb_year", 2050.0))),
        N0=float(raw["N0"]),
        pi0=float(raw["pi0"]),
        kappa_pi=float(raw["kappa_pi"]),
        r=float(raw["r"]),
        epsilon=float(raw["epsilon"]),
        s_coeff=float(raw["s_coeff"]),
        Q0=float(raw["Q0"]),
        Q_max=float(raw["Q_max"]),
        Q_ecc=float(raw["Q_ecc"]),
        omega=float(raw["omega"]),
        phi_conv=float(raw["phi_conv"]),
        phi_hw=float(raw["phi_hw"]),
        rho=float(raw["rho"]),
        P0=float(raw["P0"]),
        P_lim=float(raw["P_lim"]),
        h_exp=float(raw["h_exp"]),
        h_ecc=float(raw["h_ecc"]),
        psi=float(raw["psi"]),
        smooth_eps=float(raw["smooth_eps"]),
        E0=float(raw["E0"]),
        E_lim=float(raw["E_lim"]),
        kappa=float(raw["kappa"]),
        alpha_E=float(raw["alpha_E"]),
        delta_E=float(raw["delta_E"]),
        beta=float(raw["beta"]),
        gamma=float(raw["gamma"]),
        L0=float(raw["L0"]),
        xi_lim=float(raw["xi_lim"]),
        xi_star=float(raw["xi_star"]),
        sigma0=float(raw["sigma0"]),
        sigma_p=float(raw["sigma_p"]),
        delta_L=float(raw["delta_L"]),
        theta_L=float(raw["theta_L"]),
        lambda_D=float(raw["lambda_D"]),
        eta_W=float(raw["eta_W"]),
        c_W=float(raw["c_W"]),
        c_D=float(raw["c_D"]),
        B=float(raw["B"]),
        ivp_method=str(raw.get("ivp_method", "BDF")),
        ivp_rtol=float(raw.get("ivp_rtol", 1e-6)),
        ivp_atol=float(raw.get("ivp_atol", 1e-8)),
        ocp_nodes=int(raw.get("ocp_nodes", 61)),
        ocp_max_iter=int(raw.get("ocp_max_iter", 400)),
        slsqp_pieces=int(raw.get("slsqp_pieces", 10)),
        static_alpha_max_k=float(raw.get("static_alpha_max_k", 2.0)),
    )


def load_params(config_path: Path, overrides: list[str] | None = None) -> tuple[Params, dict]:
    raw = load_yaml(config_path)
    for item in overrides or []:
        if "=" not in item:
            raise ValueError(f"Override must be key=value, got {item!r}")
        key, value = item.split("=", 1)
        _set_dotted(raw, key.strip(), value.strip())
    return params_from_mapping(raw), raw


def dump_yaml(data: dict, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        yaml.safe_dump(data, handle, sort_keys=False)
