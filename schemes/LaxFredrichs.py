import numpy as np
import matplotlib.pyplot as plt

gamma = 1.4

# variable changes(primitive <--> conservative)
def prim_to_cons(rho, u, p):
    E = p/(gamma-1.0) + 0.5*rho*u*u
    return np.stack([rho, rho*u, E], axis=0)

def cons_to_prim(U):
    rho = U[0]
    u   = U[1]/rho
    E   = U[2]
    p   = (gamma-1.0)*(E - 0.5*rho*u*u)
    return rho, u, p

# flux vector
def flux(U):
    rho, u, p = cons_to_prim(U)
    F1 = rho*u
    F2 = rho*u*u + p
    F3 = (U[2] + p)*u
    return np.stack([F1, F2, F3], axis=0)

def sound_speed(rho, p):
    return np.sqrt(gamma*p/rho)

def rusanov_flux(UL, UR):
    FL = flux(UL)
    FR = flux(UR)
    rhoL, uL, pL = cons_to_prim(UL)
    rhoR, uR, pR = cons_to_prim(UR)
    aL = sound_speed(rhoL, pL)
    aR = sound_speed(rhoR, pR)
    smax = np.maximum(np.abs(uL)+aL, np.abs(uR)+aR)
    return 0.5*(FL + FR) - 0.5*smax*(UR - UL)

# Grid/setup
Nx   = 400
x0   = 0.5
x    = np.linspace(0.0, 1.0, Nx)
dx   = x[1] - x[0]
t    = 0.0
t_end= 0.2
CFL  = 0.9

# Initial condition
rho = np.where(x < x0, 1.0, 0.125)
u   = np.zeros_like(x)
p   = np.where(x < x0, 1.0, 0.1)

U = prim_to_cons(rho, u, p)

def timestep(U):
    rho, u, p = cons_to_prim(U)
    a = sound_speed(rho, p)
    wavespeed = np.max(np.abs(u) + a)
    return CFL * dx / wavespeed

# Time integration (explicit Euler with FV updates)
while t < t_end:
    dt = timestep(U)
    if t + dt > t_end:
        dt = t_end - t

    # Ghost cells (transmissive)
    UL = U[:, 0].copy()
    UR = U[:, -1].copy()
    Uext = np.column_stack([UL, U, UR])

    # Interface fluxes
    Fnum = np.zeros((3, Nx+1))
    for i in range(Nx+1):
        FL = Uext[:, i]
        FR = Uext[:, i+1]
        Fnum[:, i] = rusanov_flux(FL, FR)

    # FV update
    U = U - (dt/dx) * (Fnum[:, 1:] - Fnum[:, :-1])
    t += dt

# Convert to primitive for plotting
rho, u, p = cons_to_prim(U)

fig, axs = plt.subplots(3, 1, figsize=(7,8), sharex=True)
axs[0].plot(x, rho); axs[0].set_ylabel(r'$\rho$')
axs[1].plot(x, u);   axs[1].set_ylabel(r'$u$')
axs[2].plot(x, p);   axs[2].set_ylabel(r'$p$'); axs[2].set_xlabel('x')
fig.suptitle('Sod shock tube at t = 0.2 (Rusanov FV, Nx={})'.format(Nx))
plt.show()
