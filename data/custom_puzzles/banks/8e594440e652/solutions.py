"""Reference helper library and 21 reference solve functions for the twenty-second custom ARC puzzle bank.

New primitive introduced in this set:

  marker_frame(grid, colors=(2,3,4))

Interpret three adjacent colored markers as a local coordinate frame:
the first color is the origin, the second is +x, and the third is +y.
The same frame logic is reused with colors (5,6,7) for target or
candidate frames. Many tasks in this bank work by converting between
global cells and frame-relative local coordinates.

All solve_* functions are deterministic reference programs for the
synthetic ARC-style tasks in set 22.
"""
from typing import List
from collections import defaultdict

Grid = List[List[int]]

def blank(h,w,v=0):
    return [[v]*w for _ in range(h)]


def dims(g):
    return len(g), len(g[0])


def gpos(origin, vx, vy, u, v):
    r,c = origin
    return r + u*vx[0] + v*vy[0], c + u*vx[1] + v*vy[1]


def copy_grid(g):
    return [row[:] for row in g]


def find_frames(grid, colors=(2,3,4)):
    a,b,c = colors
    h,w = dims(grid)
    frames = []
    dirs = [(-1,0),(1,0),(0,-1),(0,1)]
    for r in range(h):
        for cc in range(w):
            if grid[r][cc] != a:
                continue
            xnbrs=[]; ynbrs=[]
            for dr,dc in dirs:
                nr,nc = r+dr, cc+dc
                if 0 <= nr < h and 0 <= nc < w:
                    if grid[nr][nc] == b:
                        xnbrs.append((nr,nc))
                    if grid[nr][nc] == c:
                        ynbrs.append((nr,nc))
            for xr,xc in xnbrs:
                for yr,yc in ynbrs:
                    vx=(xr-r, xc-cc)
                    vy=(yr-r, yc-cc)
                    if vx[0]*vy[0] + vx[1]*vy[1] != 0:
                        continue
                    if abs(vx[0])+abs(vx[1]) != 1 or abs(vy[0])+abs(vy[1]) != 1:
                        continue
                    frames.append({"origin": (r,cc), "vx": vx, "vy": vy, "colors": colors})
    # dedupe by origin+vx+vy
    uniq=[]
    seen=set()
    for f in frames:
        key=(f["origin"],f["vx"],f["vy"],f["colors"])
        if key not in seen:
            seen.add(key)
            uniq.append(f)
    uniq.sort(key=lambda f: (f["origin"][0], f["origin"][1], f["vx"], f["vy"]))
    return uniq


def lpos(frame, rc):
    r,c = rc
    orr,orc = frame["origin"]
    dr,dc = r-orr, c-orc
    vx,vy = frame["vx"], frame["vy"]
    u = dr*vx[0] + dc*vx[1]
    v = dr*vy[0] + dc*vy[1]
    # verify exact reconstruction
    rr,cc = gpos(frame["origin"], vx, vy, u, v)
    if (rr,cc) != (r,c):
        raise ValueError(("not in frame plane?", frame, rc, (u,v), (rr,cc)))
    return (u,v)


def extract_local_points(grid, frame, motif_colors={8}, radius=4, multicolor=True):
    pts=[]
    h,w = dims(grid)
    radius=min(radius,3)
    for r in range(h):
        for c in range(w):
            val=grid[r][c]
            if val not in motif_colors:
                continue
            try:
                u,v = lpos(frame, (r,c))
            except Exception:
                continue
            if max(abs(u), abs(v)) <= radius:
                pts.append(((u,v), val))
    pts.sort(key=lambda x: (x[0][0], x[0][1], x[1]))
    if multicolor:
        return pts
    return [uv for uv,col in pts]


def canonical_offsets(pts, multicolor=False):
    if multicolor:
        return tuple(sorted((u,v,col) for (u,v),col in pts))
    return tuple(sorted(pts))


def local_bbox(pts):
    us=[u for u,v in pts]
    vs=[v for u,v in pts]
    return min(us), min(vs), max(us), max(vs)


def bbox_fill_pts(pts, color=8):
    minu,minv,maxu,maxv = local_bbox(pts)
    return [((u,v),color) for u in range(minu,maxu+1) for v in range(minv,maxv+1)]


def bbox_boundary_pts(pts, color=8):
    minu,minv,maxu,maxv = local_bbox(pts)
    arr=[]
    for u in range(minu,maxu+1):
        for v in range(minv,maxv+1):
            if u in (minu,maxu) or v in (minv,maxv):
                arr.append(((u,v),color))
    return arr


def qcounts(pts):
    q=[0,0,0,0]
    for u,v in pts:
        if u>0 and v>0: q[0]+=1
        elif u<0 and v>0: q[1]+=1
        elif u<0 and v<0: q[2]+=1
        elif u>0 and v<0: q[3]+=1
    return q


def manhattan_radius(uv):
    u,v = uv
    return abs(u)+abs(v)


def transform_uv(uv, kind):
    u,v = uv
    if kind=="id": return (u,v)
    if kind=="rot90": return (-v,u)
    if kind=="rot180": return (-u,-v)
    if kind=="rot270": return (v,-u)
    if kind=="refl_x": return (u,-v)
    if kind=="refl_y": return (-u,v)
    if kind=="refl_diag": return (v,u)
    if kind=="refl_anti": return (-v,-u)
    raise KeyError(kind)


def transform_points(pts, kind, multicolor=False):
    if multicolor:
        return [ (transform_uv(uv,kind), col) for uv,col in pts ]
    return [ transform_uv(uv,kind) for uv in pts ]


def frame_signature(frame):
    return (frame["vx"], frame["vy"])


CANON_E7 = [(2, 0), (0, 2), (1, 1), (2, 2)]

def solve_S22_E1(grid):
    out = copy_grid(grid)
    frame = find_frames(grid, (5,6,7))[0]
    r,c = gpos(frame["origin"], frame["vx"], frame["vy"], 1, 1)
    out[r][c] = 8
    return out


def solve_S22_E2(grid):
    out = copy_grid(grid)
    frame = find_frames(grid,(5,6,7))[0]
    for uv in [(0,0),(1,0),(0,1),(1,1)]:
        r,c = gpos(frame["origin"], frame["vx"], frame["vy"], *uv)
        out[r][c] = 8
    return out


def solve_S22_E3(grid):
    out = copy_grid(grid)
    frame = find_frames(grid,(5,6,7))[0]
    for uv in [(0,0),(1,0),(2,0)]:
        r,c = gpos(frame["origin"], frame["vx"], frame["vy"], *uv)
        out[r][c] = 8
    return out


def solve_S22_E4(grid):
    out = copy_grid(grid)
    sf = find_frames(grid,(2,3,4))[0]
    tf = find_frames(grid,(5,6,7))[0]
    pts = extract_local_points(grid, sf, {8}, radius=4)
    assert len(pts)==1
    (uv,col) = pts[0]
    r,c = gpos(tf["origin"], tf["vx"], tf["vy"], *uv)
    out[r][c] = col
    return out


def solve_S22_E5(grid):
    out = copy_grid(grid)
    sf = find_frames(grid,(2,3,4))[0]
    tf = find_frames(grid,(5,6,7))[0]
    pts = extract_local_points(grid, sf, {8}, radius=4)
    for uv,col in pts:
        r,c = gpos(tf["origin"], tf["vx"], tf["vy"], *uv)
        out[r][c] = col
    return out


def solve_S22_E6(grid):
    out = copy_grid(grid)
    sf = find_frames(grid,(2,3,4))[0]
    tf = find_frames(grid,(5,6,7))[0]
    pts = extract_local_points(grid, sf, {8}, radius=4)
    maxu = max(u for (u,v),col in pts)
    chosen = [ (uv,col) for uv,col in pts if uv[0]==maxu ]
    for uv,col in chosen:
        r,c = gpos(tf["origin"], tf["vx"], tf["vy"], *uv)
        out[r][c] = col
    return out


def solve_S22_E7(grid):
    sf = find_frames(grid,(2,3,4))[0]
    pts = set(uv for uv,col in extract_local_points(grid, sf, {8}, radius=4))
    return [[8 if uv in pts else 0 for uv in CANON_E7]]


def solve_S22_M1(grid):
    out = copy_grid(grid)
    sf = find_frames(grid,(2,3,4))[0]
    tf = find_frames(grid,(5,6,7))[0]
    pts = extract_local_points(grid, sf, {8}, radius=4)
    for uv,col in pts:
        r,c = gpos(tf["origin"], tf["vx"], tf["vy"], *uv)
        out[r][c] = col
    return out


def solve_S22_M2(grid):
    out = copy_grid(grid)
    sf = find_frames(grid,(2,3,4))[0]
    tf = find_frames(grid,(5,6,7))[0]
    pts = extract_local_points(grid, sf, {8,9}, radius=4)
    for uv,col in pts:
        r,c = gpos(tf["origin"], tf["vx"], tf["vy"], *uv)
        out[r][c] = col
    return out


def solve_S22_M3(grid):
    out = copy_grid(grid)
    sf = find_frames(grid,(2,3,4))[0]
    tf = find_frames(grid,(5,6,7))[0]
    pts = [uv for uv,col in extract_local_points(grid,sf,{8},radius=4)]
    for uv,col in bbox_fill_pts(pts,8):
        r,c = gpos(tf["origin"], tf["vx"], tf["vy"], *uv)
        out[r][c] = col
    return out


def solve_S22_M4(grid):
    out = copy_grid(grid)
    sf = find_frames(grid,(2,3,4))[0]
    tf = find_frames(grid,(5,6,7))[0]
    pts = [uv for uv,col in extract_local_points(grid,sf,{8},radius=4)]
    for uv,col in bbox_boundary_pts(pts,8):
        r,c = gpos(tf["origin"], tf["vx"], tf["vy"], *uv)
        out[r][c] = col
    return out


def solve_S22_M5(grid):
    sf = find_frames(grid,(2,3,4))[0]
    pts = [uv for uv,col in extract_local_points(grid,sf,{8},radius=4)]
    return [qcounts(pts)]


def solve_S22_M6(grid):
    out = copy_grid(grid)
    sf = find_frames(grid,(2,3,4))[0]
    tfs = find_frames(grid,(5,6,7))
    pts = extract_local_points(grid, sf, {8}, radius=4)
    sig = frame_signature(sf)
    for tf in tfs:
        if frame_signature(tf) == sig:
            for uv,col in pts:
                r,c = gpos(tf["origin"], tf["vx"], tf["vy"], *uv)
                out[r][c] = col
    return out


def solve_S22_M7(grid):
    out = copy_grid(grid)
    sf = find_frames(grid,(2,3,4))[0]
    tf = find_frames(grid,(5,6,7))[0]
    pts = extract_local_points(grid,sf,{8},radius=4)
    maxrad = max(manhattan_radius(uv) for uv,col in pts)
    chosen = [ (uv,col) for uv,col in pts if manhattan_radius(uv)==maxrad ]
    for uv,col in chosen:
        r,c = gpos(tf["origin"], tf["vx"], tf["vy"], *uv)
        out[r][c] = col
    return out


def solve_S22_H1(grid):
    sf = find_frames(grid,(2,3,4))[0]
    candidates = find_frames(grid,(5,6,7))
    src_sig = canonical_offsets([uv for uv,col in extract_local_points(grid,sf,{8},radius=4)])
    odd=[]
    for i,tf in enumerate(candidates):
        sig = canonical_offsets([uv for uv,col in extract_local_points(grid,tf,{8},radius=4)])
        odd.append(sig)
    # choose candidate whose signature differs from majority
    # assume exactly one odd
    counts = defaultdict(int)
    for sig in odd:
        counts[sig]+=1
    idx = [i for i,sig in enumerate(odd) if counts[sig]==1][0]
    out=[[0]*len(candidates)]
    out[0][idx]=8
    return out


def solve_S22_H2(grid):
    out = copy_grid(grid)
    sf = find_frames(grid,(2,3,4))[0]
    tf = find_frames(grid,(5,6,7))[0]
    pts = extract_local_points(grid,sf,{8},radius=4)
    newpts = [ (transform_uv(uv,'refl_diag'), col) for uv,col in pts ]
    for uv,col in newpts:
        r,c = gpos(tf["origin"], tf["vx"], tf["vy"], *uv)
        out[r][c]=col
    return out


def solve_S22_H3(grid):
    out = copy_grid(grid)
    sf = find_frames(grid,(2,3,4))[0]
    tf = find_frames(grid,(5,6,7))[0]
    pts = extract_local_points(grid,sf,{8,9},radius=4)
    newpts = [ (transform_uv(uv,'rot90'), col) for uv,col in pts ]
    for uv,col in newpts:
        r,c = gpos(tf["origin"], tf["vx"], tf["vy"], *uv)
        out[r][c]=col
    return out


def solve_S22_H4(grid):
    sf = find_frames(grid,(2,3,4))[0]
    pts = set(uv for uv,col in extract_local_points(grid,sf,{8},radius=2))
    out = blank(3,3,0)
    for u in [-1,0,1]:
        for v in [-1,0,1]:
            if (u,v) in pts:
                out[v+1][u+1] = 8  # row by v, col by u
    return out


def solve_S22_H5(grid):
    out = copy_grid(grid)
    sf = find_frames(grid,(2,3,4))[0]
    tf = find_frames(grid,(5,6,7))[0]
    pts = extract_local_points(grid,sf,{8},radius=4)
    pset = set(uv for uv,col in pts)
    keep = [ (uv,col) for uv,col in pts if (-uv[0], uv[1]) in pset ]
    for uv,col in keep:
        r,c = gpos(tf["origin"], tf["vx"], tf["vy"], *uv)
        out[r][c]=col
    return out


def solve_S22_H6(grid):
    sfs = find_frames(grid,(2,3,4))
    tfs = find_frames(grid,(5,6,7))
    # pair source/target by reading order, query is last source, answer goes in last target
    assert len(sfs)==len(tfs)==3
    src_motifs = [canonical_offsets([uv for uv,col in extract_local_points(grid,sf,{8},radius=4)]) for sf in sfs]
    tgt_pts = [extract_local_points(grid,tf,{8,9},radius=4) for tf in tfs]
    # examples 0,1 map source->target
    mapping = {src_motifs[i]: tgt_pts[i] for i in range(2)}
    query_sig = src_motifs[2]
    value = mapping[query_sig]
    out = copy_grid(grid)
    qtf = tfs[2]
    for uv,col in value:
        r,c = gpos(qtf["origin"], qtf["vx"], qtf["vy"], *uv)
        out[r][c]=col
    return out


def solve_S22_H7(grid):
    sf = find_frames(grid,(2,3,4))[0]
    candidates = find_frames(grid,(5,6,7))
    src_sig = canonical_offsets(transform_points([uv for uv,col in extract_local_points(grid,sf,{8},radius=4)], 'rot90'))
    idx=None
    for i,tf in enumerate(candidates):
        sig = canonical_offsets([uv for uv,col in extract_local_points(grid,tf,{8},radius=4)])
        if sig == src_sig:
            idx = i
            break
    out=[[0]*len(candidates)]
    out[0][idx]=8
    return out

