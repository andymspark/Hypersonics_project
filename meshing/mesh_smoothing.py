import numpy as np

# ------------------ Simple smoothing (optional) ------------------
def laplacian_smooth(points, tris, boundary_mask, n_iter=3, lam=0.5):
    """Move interior point to average of its neighbors (boundary fixed)."""
    N = len(points)
    # Build adjacency
    adj = [set() for _ in range(N)]
    for (i,j,k) in tris:
        adj[i].update([j,k]); adj[j].update([i,k]); adj[k].update([i,j])
    P = points.copy()
    for _ in range(n_iter):
        Q = P.copy()
        for i in range(N):
            if boundary_mask[i]:
                continue
            if not adj[i]:
                continue
            nbrs = np.array([P[j] for j in adj[i]], dtype=float)
            avg = nbrs.mean(axis=0)
            Q[i] = (1-lam)*P[i] + lam*avg
            # keep inside the unit square
            Q[i,0] = min(1.0, max(0.0, Q[i,0]))
            Q[i,1] = min(1.0, max(0.0, Q[i,1]))
        P = Q
    return P