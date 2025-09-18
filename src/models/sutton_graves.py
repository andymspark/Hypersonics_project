import numpy as np

def q_sutton_graves(rho_inf, V_inf, Rn, return_units="W_per_m2"):
    """Sutton–Graves convective stagnation heat flux.
    rho_inf: kg/m^3, V_inf: m/s, Rn: m
    Canonical form returns W/cm^2 with constant 1.83e-4. We convert to W/m^2.
    """
    q_w_cm2 = 1.83e-4 * np.sqrt(rho_inf / Rn) * V_inf**3  # W/cm^2
    q_w_m2 = q_w_cm2 * 1.0e4  # convert to W/m^2
    if return_units == "W_per_cm2":
        return q_w_cm2
    return q_w_m2
