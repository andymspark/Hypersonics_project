CFD_Sod/
├─ CMakeLists.txt
├─ README.md
├─ examples/
│  └─ sod.yaml
├─ src/
│  ├─ main.cpp                # reads config, runs simulation, writes output
│  ├─ app/
│  │  └─ simulator.h/.cpp
│  ├─ numerics/
│  │  ├─ scheme.h             # abstract Scheme interface
│  │  ├─ scheme_factory.h/.cpp
│  │  ├─ lf/                  # Lax-Friedrichs implementation
│  │  │  └─ lf.h/.cpp
│  │  ├─ muscl/               # MUSCL (reconstruction + HLLC/Roe)
│  │  │  └─ muscl.h/.cpp
│  │  └─ weno/                # WENO5 + HLLC
│  │     └─ weno5.h/.cpp
│  ├─ physics/
│  │  └─ euler.h/.cpp         # state conversions, flux, wavespeed, HLLC solver
│  └─ io/
│     └─ vtk_writer.h/.cpp    # optional; or dump CSV
├─ scripts/
│  ├─ run_all_schemes.sh
│  └─ evaluate_errors.py
└─ experiments/                # results/CSV for reproducibility