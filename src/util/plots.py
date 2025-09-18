import matplotlib.pyplot as plt

def plot_q_vs_M(results_per_Rn, out_png):
    fig, ax = plt.subplots(figsize=(6,4))
    for Rn, rows in results_per_Rn.items():
        Ms = [r["M"] for r in rows]
        q_sg = [r["q_SG_Wm2"] for r in rows]
        q_fr = [r["q_FR_Wm2"] for r in rows]
        ax.plot(Ms, q_sg, marker='o', linestyle='-', label=f'SG Rn={Rn*1000:.1f} mm')
        ax.plot(Ms, q_fr, marker='s', linestyle='--', label=f'FR Rn={Rn*1000:.1f} mm')
    ax.set_xlabel('Freestream Mach M∞')
    ax.set_ylabel('Stagnation heat flux q [W/m²]')
    ax.set_title('Sutton–Graves vs Fay–Riddell (perfect gas)')
    ax.grid(True, alpha=0.3)
    ax.legend()
    fig.tight_layout()
    fig.savefig(out_png, dpi=200)
    plt.close(fig)

def plot_q_vs_Rn(results_per_M, out_png):
    fig, ax = plt.subplots(figsize=(6,4))
    for M, rows in results_per_M.items():
        Rns = [r["Rn_m"]*1000 for r in rows]  # mm
        q_sg = [r["q_SG_Wm2"] for r in rows]
        q_fr = [r["q_FR_Wm2"] for r in rows]
        ax.plot(Rns, q_sg, marker='o', linestyle='-', label=f'SG M={M}')
        ax.plot(Rns, q_fr, marker='s', linestyle='--', label=f'FR M={M}')
    ax.set_xlabel('Nose radius Rn [mm]')
    ax.set_ylabel('Stagnation heat flux q [W/m²]')
    ax.set_title('Scaling with nose radius')
    ax.grid(True, alpha=0.3)
    ax.legend()
    fig.tight_layout()
    fig.savefig(out_png, dpi=200)
    plt.close(fig)
