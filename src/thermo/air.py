import numpy as np

# Perfect-gas air (starter values)
GAMMA = 1.4
R_AIR = 287.05           # J/(kg·K)
CP_AIR = GAMMA * R_AIR / (GAMMA - 1.0)  # ~1004.68 J/(kg·K)
PRANDTL = 0.71           # assume constant

def sound_speed(T, gamma=GAMMA, R=R_AIR):
    return np.sqrt(gamma * R * T)

def sutherland_mu(T):
    """Dynamic viscosity of air via Sutherland's law (Pa·s).
    Reference: mu_ref @ T_ref = 1.716e-5 Pa·s at 273.15 K; S = 110.4 K.
    """
    T_ref = 273.15
    mu_ref = 1.716e-5
    S = 110.4
    return mu_ref * (T / T_ref)**1.5 * (T_ref + S) / (T + S)

def density(p, T, R=R_AIR):
    return p / (R * T)

def enthalpy(T, cp=CP_AIR):
    return cp * T
