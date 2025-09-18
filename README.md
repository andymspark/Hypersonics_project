
# Hypersonics: Blunt-Body Heating — Correlations vs CFD (starter kit)

This repo gives you a ready-to-run scaffold to compare classic hypersonic heating correlations
— Sutton–Graves and Fay–Riddell (laminar stagnation) — under perfect-gas air assumptions.
You can sweep Mach number and nose radius and generate figures.

> What this is: An undergraduate-friendly starting point that is easy to extend toward CFD.
> What this is not (yet): A full Navier–Stokes flow solver or chemistry/nonequilibrium model.

## Quick start
```bash
python cases/M7_blunted_cone/run_case.py
```
- Outputs CSV under `results/`
- Saves plots under `plots/`

## Structure
```
src/
  aero/normal_shock.py        # perfect-gas normal shock relations
  models/sutton_graves.py     # Sutton–Graves correlation (unit-safe; W/m^2 output)
  models/fay_riddell.py       # Simplified Fay–Riddell stagnation formula (perfect gas, Le=1)
  thermo/air.py               # Air properties: Sutherland mu(T), cp, gamma, R, Pr
  util/plots.py               # Simple matplotlib helpers
cases/M7_blunted_cone/
  config.json                 # Freestream & geometry settings (SI units)
  run_case.py                 # Orchestrates sweeps and plotting
results/                      # CSV outputs
plots/                        # Figures
tests/                        # Minimal checks for relations
```

## Correlations & references (read these if you change formulas)
- Sutton–Graves stagnation-point convective heating (axisymmetric blunt body):
  qdot_c = 1.83e-4 * sqrt(rho / Rn) * V^3  with rho in kg/m^3, Rn in m, V in m/s — returns W/cm^2 (converted in code to W/m^2).
  See NASA NTRS summary and usage notes.
- Fay–Riddell laminar stagnation-point heating (perfect-gas simplification, Lewis = 1):
  qdot_c = 0.76 * Pr_w^(-0.6) * (rho_w*mu_w)^(0.1) * (rho_e*mu_e)^(0.4) * (h_e - h_w) * (1/Rn) * sqrt( 2*(p_e - p_inf)/rho_e ).
  We obtain edge values from a normal shock (blunt-body approximation).

Primary sources: see the inline citations in the ChatGPT message that delivered this repo.

## Next steps toward CFD (suggested)
1) Replace the normal-shock edge model with a bow-shock stand-off estimate and use post-shock edge conditions along the stagnation streamline.
2) Add adiabatic wall temperature via Walz/recovery factor or solve an integral BL for (h_e - h_w).
3) Couple to your 2-D transient conduction (CSD) and optimize TPS thickness.

---

Units: All inputs are SI. Plots are in W/m^2.
Limitations: Perfect gas (gamma=1.4), constant cp, no chemistry; Lewis number set to 1.
