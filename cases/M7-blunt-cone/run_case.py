import os, json, csv
import numpy as np
from pathlib import Path

from ...src.models.sutton_graves import q_sutton_graves
from ...src.models.fay_riddell import q_fay_riddell_stagnation
from ...src.thermo.air import sound_speed

from ...src.util.plots import plot_q_vs_M, plot_q_vs_Rn

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
RESULTS = ROOT / 'results'
PLOTS = ROOT / 'plots'

def main():
    with open(HERE / 'config.json','r') as f:
        cfg = json.load(f)

    T_inf = cfg['free_stream']['T_inf_K']
    p_inf = cfg['free_stream']['p_inf_Pa']
    M_list = cfg['free_stream']['M_list']
    gamma = cfg['free_stream']['gamma']
    R_air = cfg['free_stream']['R_air']

    Rn_list = cfg['body']['Rn_list_m']
    T_wall = cfg['body']['T_wall_K']

    RESULTS.mkdir(parents=True, exist_ok=True)
    PLOTS.mkdir(parents=True, exist_ok=True)
    out_csv = RESULTS / f"{cfg['case_name']}_sweep.csv"

    rows = []
    for Rn in Rn_list:
        for M in M_list:
            a_inf = np.sqrt(gamma * R_air * T_inf)
            V_inf = M * a_inf
            rho_inf = p_inf/(R_air*T_inf)
            q_sg = q_sutton_graves(rho_inf=rho_inf, V_inf=V_inf, Rn=Rn, return_units='W_per_m2')
            q_fr = q_fay_riddell_stagnation(p_inf=p_inf, T_inf=T_inf, M_inf=M, Rn=Rn, gamma=gamma, R=R_air, T_wall=T_wall)
            rows.append(dict(M=M, Rn_m=Rn, q_SG_Wm2=float(q_sg), q_FR_Wm2=float(q_fr)))

    with open(out_csv, 'w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        for r in rows: w.writerow(r)

    per_Rn = {}
    for Rn in Rn_list:
        per_Rn[Rn] = [r for r in rows if abs(r['Rn_m']-Rn) < 1e-12]
    plot_q_vs_M(per_Rn, str(PLOTS / f"{cfg['case_name']}_q_vs_M.png"))

    per_M = {}
    for M in M_list:
        per_M[M] = [r for r in rows if abs(r['M']-M) < 1e-12]
    plot_q_vs_Rn(per_M, str(PLOTS / f"{cfg['case_name']}_q_vs_Rn.png"))

    print(f"Wrote {out_csv}")
    print(f"Saved plots to {PLOTS}")

if __name__ == '__main__':
    main()
