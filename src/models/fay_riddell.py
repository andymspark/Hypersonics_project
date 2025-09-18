import numpy as np
from ..thermo.air import density, enthalpy, sutherland_mu, PRANDTL

def q_fay_riddell_stagnation(p_inf, T_inf, M_inf, Rn, gamma=1.4, R=287.05, T_wall=300.0):
    """Simplified Fay–Riddell convective heat flux at stagnation (W/m^2).
    - Perfect gas, Lewis number = 1 (ignores dissociation enthalpy term).
    - Edge (e) values from a *normal shock* (blunt-body approximation).
    - Wall pressure ~ edge pressure.
    """
    # Freestream
    a_inf = np.sqrt(gamma * R * T_inf)
    V_inf = M_inf * a_inf
    rho_inf = p_inf / (R * T_inf)

    # Normal shock to get edge state
    gm1, gp1 = gamma - 1.0, gamma + 1.0
    M1 = M_inf
    p2_p1 = 1.0 + 2.0 * gamma / gp1 * (M1**2 - 1.0)
    rho2_rho1 = gp1 * M1**2 / (gm1 * M1**2 + 2.0)
    T2_T1 = p2_p1 / rho2_rho1
    p_e = p_inf * p2_p1
    T_e = T_inf * T2_T1
    rho_e = rho_inf * rho2_rho1

    # Transport and thermodynamic props
    mu_e = sutherland_mu(T_e)
    mu_w = sutherland_mu(T_wall)
    rho_w = p_e / (R * T_wall)  # wall pressure ~ edge pressure
    h_e = (gamma * R / (gamma - 1.0)) * T_e
    h_w = (gamma * R / (gamma - 1.0)) * T_wall

    # Velocity gradient at stagnation (per common form)
    due_dx_stag = (1.0 / Rn) * np.sqrt(2.0 * (p_e - p_inf) / rho_e)

    q = 0.76 * (PRANDTL**(-0.6)) * (rho_w * mu_w)**0.1 * (rho_e * mu_e)**0.4 * (h_e - h_w) * due_dx_stag
    return q  # W/m^2
