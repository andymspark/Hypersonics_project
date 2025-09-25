import numpy as np
import math

EPS = 1e-12

# ------------------ Delaunay predicates ------------------
def orient2d(a, b, c):
    ax, ay = a; bx, by = b; cx, cy = c
    return (bx-ax)*(cy-ay) - (by-ay)*(cx-ax)

def circumcircle_contains(a, b, c, p):
    ax, ay = a; bx, by = b; cx, cy = c; px, py = p
    d = 2.0 * (ax*(by-cy) + bx*(cy-ay) + cx*(ay-by))
    if abs(d) < EPS:
        return False
    a2 = ax*ax + ay*ay
    b2 = bx*bx + by*by
    c2 = cx*cx + cy*cy
    ux = (a2*(by-cy) + b2*(cy-ay) + c2*(ay-by)) / d
    uy = (a2*(cx-bx) + b2*(ax-cx) + c2*(bx-ax)) / d
    r2 = (ux-ax)**2 + (uy-ay)**2
    dist2 = (ux-px)**2 + (uy-py)**2
    return dist2 <= r2 * (1.0 + 1e-12)

def bowyer_watson(points):
    pts = np.asarray(points, dtype=float)
    n = pts.shape[0]

    # Supertriangle
    minx, miny = pts.min(axis=0); maxx, maxy = pts.max(axis=0)
    dx = maxx - minx; dy = maxy - miny
    delta = max(dx, dy) if max(dx, dy) > 0 else 1.0
    mx = 0.5*(minx + maxx); my = 0.5*(miny + maxy)
    pS1 = np.array([mx - 20*delta, my - 20*delta])
    pS2 = np.array([mx,             my + 20*delta])
    pS3 = np.array([mx + 20*delta, my - 20*delta])
    pts_ext = np.vstack([pts, pS1, pS2, pS3])
    iS1, iS2, iS3 = n, n+1, n+2

    triangles = [(iS1, iS2, iS3)]

    def orient_triangle(t):
        i,j,k = t
        if orient2d(pts_ext[i], pts_ext[j], pts_ext[k]) < 0:
            return (i,k,j)
        return t

    for p_idx in range(n):
        p = pts_ext[p_idx]

        bad_tris = []
        for (i, j, k) in triangles:
            if circumcircle_contains(pts_ext[i], pts_ext[j], pts_ext[k], p):
                bad_tris.append((i, j, k))

        edge_count = {}
        oriented_edges = []
        for (i, j, k) in bad_tris:
            edges = [(i, j), (j, k), (k, i)]
            for e in edges:
                oriented_edges.append(e)
                key = tuple(sorted(e))
                edge_count[key] = edge_count.get(key, 0) + 1

        boundary = []
        for e in oriented_edges:
            key = tuple(sorted(e))
            if edge_count.get(key, 0) == 1:
                boundary.append(e)

        triangles = [t for t in triangles if t not in bad_tris]
        for (i, j) in boundary:
            triangles.append((i, j, p_idx))

        triangles = [orient_triangle(t) for t in triangles]

    final_tris = [t for t in triangles if all(v < n for v in t)]
    return pts, np.array(final_tris, dtype=int)