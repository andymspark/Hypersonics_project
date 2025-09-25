import numpy as np
import math
from Bowyer_Watson import orient2d

# ------------------ Quality metrics ------------------
def triangle_metrics(points, tris):
    """Compute min angle and radius-edge ratio for each triangle."""
    pts = np.asarray(points)
    min_angles = []
    rad_edge = []
    for (i,j,k) in tris:
        a = pts[i]; b = pts[j]; c = pts[k]
        ab = np.linalg.norm(a-b)
        bc = np.linalg.norm(b-c)
        ca = np.linalg.norm(c-a)
        # area
        area2 = abs(orient2d(a,b,c))
        if area2 < 1e-16:
            continue
        # circumradius R = abc / (4A), but A = area2/2
        R = (ab*bc*ca) / (2*area2 + 1e-18)
        lmin = min(ab, bc, ca)
        rad_edge.append(R / (lmin + 1e-18))
        # angles via cosine law (clip to [-1,1])
        def angle(op, s1, s2):
            val = (s1*s1 + s2*s2 - op*op) / (2*s1*s2 + 1e-18)
            val = max(-1.0, min(1.0, val))
            return math.degrees(math.acos(val))
        Aang = angle(bc, ab, ca)
        Bang = angle(ca, ab, bc)
        Cang = angle(ab, bc, ca)
        min_angles.append(min(Aang, Bang, Cang))
    return np.array(min_angles), np.array(rad_edge)

def unique_edges(tris):
    """Return array of unique undirected edges (i<j)."""
    s = set()
    for (i,j,k) in tris:
        e = [(i,j), (j,k), (k,i)]
        for (u,v) in e:
            if u>v: u,v = v,u
            s.add((u,v))
    return np.array(list(s), dtype=int)

def gradation_metric(points, tris):
    """Simple gradation: for each vertex, ratio (max edge length / min edge length) of incident edges."""
    edges = unique_edges(tris)
    pts = np.asarray(points)
    lengths = np.linalg.norm(pts[edges[:,0]] - pts[edges[:,1]], axis=1)
    # incident lists
    N = len(points)
    inc = [[] for _ in range(N)]
    for idx, (u,v) in enumerate(edges):
        inc[u].append(lengths[idx])
        inc[v].append(lengths[idx])
    ratios = []
    for i in range(N):
        L = inc[i]
        if len(L) >= 2:
            ratios.append(max(L)/ (min(L) + 1e-18))
    return np.array(ratios)