import numpy as np

def normal_shock_ratios(M1, gamma=1.4):
    """Return downstream ratios for a perfect-gas normal shock.
    Outputs: dict with M2, p2_p1, T2_T1, rho2_rho1
    """
    gm1 = gamma - 1.0
    gp1 = gamma + 1.0

    M1n2 = M1**2
    p2_p1 = 1.0 + 2.0 * gamma / gp1 * (M1n2 - 1.0)
    rho2_rho1 = gp1 * M1n2 / (gm1 * M1n2 + 2.0)
    T2_T1 = p2_p1 / rho2_rho1
    M2_sq = (1.0 + 0.5 * gm1 * M1n2) / (gamma * M1n2 - 0.5 * gm1)
    M2 = np.sqrt(M2_sq)
    return dict(M2=M2, p2_p1=p2_p1, T2_T1=T2_T1, rho2_rho1=rho2_rho1)
