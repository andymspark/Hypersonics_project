import numpy as np
import math

# ------------------ Blue-noise sampling ------------------
# generates Poisson-disk (blue-noise) points in a rectangle: 
# a set of points that are evenly spread so any two are at least distance r apart.
def poisson_disk_2d(width, height, r, k=30, seed=0):
    """Bridson's algorithm in [0,width]x[0,height]."""
    
    rng = np.random.default_rng(seed)
    cell = r / math.sqrt(2)
    nx, ny = int(math.ceil(width/cell)), int(math.ceil(height/cell))
    grid = -np.ones((nx, ny), dtype=int)

    samples = []        #list of accepted points
    active = []

    def grid_coords(p):
        return int(p[0] // cell), int(p[1] // cell)

    def in_window(p):
        return 0 <= p[0] < width and 0 <= p[1] < height

    def fits(p):
        gx, gy = grid_coords(p)
        ix0 = max(gx-2, 0); iy0 = max(gy-2, 0)
        ix1 = min(gx+3, nx); iy1 = min(gy+3, ny)
        for ix in range(ix0, ix1):
            for iy in range(iy0, iy1):
                sidx = grid[ix, iy]
                if sidx != -1:
                    q = samples[sidx]
                    if np.hypot(p[0]-q[0], p[1]-q[1]) < r - 1e-12:
                        return False
        return True

    # initial point
    p0 = np.array([rng.random()*width, rng.random()*height])
    samples.append(p0)
    active.append(0)
    gx, gy = grid_coords(p0)
    grid[gx, gy] = 0

    while active:
        idx = rng.choice(active)
        base = samples[idx]
        found = False
        for _ in range(k):
            rad = r*(1 + rng.random())
            ang = rng.random()*2*math.pi
            cand = np.array([base[0] + rad*math.cos(ang),
                             base[1] + rad*math.sin(ang)])
            if in_window(cand) and fits(cand):
                samples.append(cand)
                active.append(len(samples)-1)
                gx, gy = grid_coords(cand)
                grid[gx, gy] = len(samples)-1
                found = True
                break
        if not found:
            active.remove(idx)

    return np.array(samples, dtype=float)