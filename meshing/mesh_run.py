import numpy as np
import matplotlib.pyplot as plt
import math
from Bowyer_Watson import bowyer_watson
from Blue_noise_sampling import poisson_disk_2d
from mesh_boundary import sample_square_boundary
from mesh_smoothing import laplacian_smooth
from mesh_quality import triangle_metrics
from mesh_quality import gradation_metric
# ------------------ Build a quasi-uniform mesh ------------------
# User knobs:
h = 0.04          # target uniform edge size
hb = 0.5*h        # boundary spacing (finer than interior to resolve curvature/edges)
r  = h            # Poisson-disk minimum distance

# 1) Boundary
# airfoil geometry
B = sample_square_boundary(hb)

# 2) Interior blue-noise
Pint = poisson_disk_2d(1.0, 1.0, r, k=30, seed=42)

# 3) Merge and remove duplicates close to boundary points
P = np.vstack([Pint, B])
# Deduplicate with a small tolerance
def dedup(P, tol=1e-6):
    P = np.asarray(P)
    order = np.lexsort((P[:,1], P[:,0]))
    P = P[order]
    keep = [0]
    for i in range(1, len(P)):
        if np.hypot(P[i,0]-P[keep[-1],0], P[i,1]-P[keep[-1],1]) > tol:
            keep.append(i)
    return P[keep]

P = dedup(P)

# 4) Triangulate
pts0, tris0 = bowyer_watson(P)

# 5) Identify boundary points (on the square edge within tolerance)
tol = 1e-9
is_boundary = ((np.abs(pts0[:,0]) < tol) | (np.abs(pts0[:,0]-1.0) < tol) |
               (np.abs(pts0[:,1]) < tol) | (np.abs(pts0[:,1]-1.0) < tol))

# 6) Optional smoothing (few iterations; boundary fixed)
pts1 = laplacian_smooth(pts0, tris0, is_boundary, n_iter=5, lam=0.5)
# Re-triangulate after smoothing
pts, tris = bowyer_watson(pts1)

# 7) Quality metrics
min_angles, rad_edge = triangle_metrics(pts, tris)
grad_ratio = gradation_metric(pts, tris)

# 8) Plots
# Triangulation
plt.figure(figsize=(6,6))
for (i,j,k) in tris:
    px = [pts[i,0], pts[j,0], pts[k,0], pts[i,0]]
    py = [pts[i,1], pts[j,1], pts[k,1], pts[i,1]]
    plt.plot(px, py, linewidth=0.7)
plt.plot([0,1,1,0,0], [0,0,1,1,0], linewidth=1.0)
plt.gca().set_aspect('equal', adjustable='box')
plt.xlim(0,1); plt.ylim(0,1)
plt.title("Quasi‑uniform Delaunay mesh in unit square")
plt.tight_layout()
plt.show()

# Min‑angle histogram
plt.figure(figsize=(6,4))
plt.hist(min_angles, bins=20)
plt.xlabel("Triangle minimum angle (degrees)")
plt.ylabel("Count")
plt.title("Min‑angle distribution")
plt.tight_layout()
plt.show()

# 9) Print summary stats
print(f"#points = {len(pts)}, #triangles = {len(tris)}")
print(f"Min angle: min={min_angles.min():.2f}°, p5={np.percentile(min_angles,5):.2f}°, median={np.median(min_angles):.2f}°")
print(f"Radius‑edge ratio: median={np.median(rad_edge):.3f}, max={rad_edge.max():.3f}")
print(f"Gradation (vertex max/min incident edge lengths): median={np.median(grad_ratio):.3f}, 95%={np.percentile(grad_ratio,95):.3f}")