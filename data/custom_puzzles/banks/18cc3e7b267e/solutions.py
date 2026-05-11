"""Reference solvers for ARC-style additional puzzle bank volume 3."""
from typing import List
from collections import deque
Grid = List[List[int]]

DIR4 = [(-1,0),(1,0),(0,-1),(0,1)]

def parse_grid(s: str) -> Grid:
    lines=[line.strip() for line in s.strip().splitlines() if line.strip()]
    return [[int(ch) for ch in line] for line in lines]

def grid_to_str(g: Grid) -> str:
    return "\n".join("".join(str(c) for c in row) for row in g)

def clone(g: Grid) -> Grid:
    return [row[:] for row in g]

def dims(g):
    return len(g), len(g[0])

def inb(g,r,c):
    h,w=dims(g)
    return 0<=r<h and 0<=c<w

def safe(g,r,c,d=0):
    return g[r][c] if inb(g,r,c) else d

def components(g: Grid, colors=None):
    # returns list of dicts: color, cells
    h,w=dims(g)
    seen=[[False]*w for _ in range(h)]
    comps=[]
    for r in range(h):
        for c in range(w):
            if seen[r][c]:
                continue
            seen[r][c]=True
            val=g[r][c]
            if val==0 or (colors is not None and val not in colors):
                continue
            stack=[(r,c)]
            cells=[(r,c)]
            while stack:
                rr,cc=stack.pop()
                for dr,dc in DIR4:
                    nr,nc=rr+dr,cc+dc
                    if inb(g,nr,nc) and not seen[nr][nc] and g[nr][nc]==val:
                        seen[nr][nc]=True
                        stack.append((nr,nc))
                        cells.append((nr,nc))
            rs=[r for r,c in cells]; cs=[c for r,c in cells]
            comps.append({"color":val,"cells":cells,"bbox":(min(rs),min(cs),max(rs),max(cs))})
    return comps

def bbox(cells):
    rs=[r for r,c in cells]; cs=[c for r,c in cells]
    return min(rs), min(cs), max(rs), max(cs)

def crop_to_bbox(g: Grid, cells=None):
    if cells is None:
        cells=[(r,c) for r,row in enumerate(g) for c,v in enumerate(row) if v!=0]
    if not cells:
        return [[0]]
    r0,c0,r1,c1=bbox(cells)
    return [row[c0:c1+1] for row in g[r0:r1+1]]

def normalize_cells(cells):
    if not cells: return []
    r0=min(r for r,c in cells); c0=min(c for r,c in cells)
    return [(r-r0,c-c0) for r,c in cells]

def rotate_cw_cells(cells):
    # cells as set of (r,c), return rotated normalized cw 90 in bbox
    rs=[r for r,c in cells]; cs=[c for r,c in cells]
    h=max(rs)-min(rs)+1; w=max(cs)-min(cs)+1
    norm=[(r-min(rs),c-min(cs)) for r,c in cells]
    rot=[(c, h-1-r) for r,c in norm]
    rmin=min(r for r,c in rot); cmin=min(c for r,c in rot)
    return [(r-rmin, c-cmin) for r,c in rot]

def rotate_k_cells(cells,k):
    out=normalize_cells(cells)
    for _ in range(k%4):
        out=rotate_cw_cells(out)
    return out

def align_shape_cells(g, color):
    cells=[(r,c) for r,row in enumerate(g) for c,v in enumerate(row) if v==color]
    if not cells:
        return set(), (0,0)
    r0,c0,r1,c1=bbox(cells)
    return {(r-r0,c-c0) for r,c in cells}, (r1-r0+1, c1-c0+1)

def solve_E15(g):
    out=clone(g)
    h,w=dims(g)
    for r in range(h):
        for c in range(w):
            if g[r][c]==3:
                deg=sum(1 for dr,dc in DIR4 if safe(g,r+dr,c+dc)==3)
                if deg==1:
                    out[r][c]=2
    return out

def solve_E16(g):
    out=clone(g)
    h,w=dims(g)
    for r in range(h):
        for c in range(w):
            if g[r][c]==0 and all(safe(g,r+dr,c+dc)==2 for dr,dc in [(-1,-1),(-1,1),(1,-1),(1,1)]):
                out[r][c]=1
    return out

def solve_E17(g):
    out=clone(g)
    h,w=dims(g)
    for comp in components(g, colors={7}):
        borders=set()
        for r,c in comp["cells"]:
            if r==0: borders.add("top")
            if r==h-1: borders.add("bottom")
            if c==0: borders.add("left")
            if c==w-1: borders.add("right")
        if len(borders)==1:
            for r,c in comp["cells"]:
                out[r][c]=8
    return out

def solve_E18(g):
    h,w=dims(g)
    out=[[0]*w for _ in range(h)]
    # copy non-red cells first
    for r in range(h):
        for c in range(w):
            if g[r][c]!=2:
                out[r][c]=g[r][c]
    for r in range(h):
        for c in range(w):
            if g[r][c]==2:
                if sum(1 for dr,dc in DIR4 if safe(g,r+dr,c+dc)==2)==0 and c+1<w and g[r][c+1]==0:
                    out[r][c+1]=2
                else:
                    out[r][c]=2
    return out

def solve_E19(g):
    out=clone(g)
    h,w=dims(g)
    for r in range(h):
        for c in range(w):
            if g[r][c]==1:
                deg=sum(1 for dr,dc in DIR4 if safe(g,r+dr,c+dc)==1)
                if deg==3:
                    out[r][c]=4
    return out

def solve_E20(g):
    out=clone(g)
    for comp in components(g, colors={6}):
        if len(comp["cells"])==2:
            for r,c in comp["cells"]:
                out[r][c]=7
    return out

def solve_E21(g):
    out=clone(g)
    h,w=dims(g)
    changed=True
    while changed:
        changed=False
        for r in range(h-1):
            for c in range(w-1):
                pos=[(r,c),(r+1,c),(r,c+1),(r+1,c+1)]
                vals=[out[rr][cc] for rr,cc in pos]
                if vals.count(3)==3 and vals.count(0)==1:
                    rr,cc=pos[vals.index(0)]
                    out[rr][cc]=3
                    changed=True
    return out

def solve_M15(g):
    out=[[0]*len(g[0]) for _ in range(len(g))]
    for comp in components(g):
        color=comp["color"]
        r0,c0,r1,c1=comp["bbox"]
        for r in range(r0,r1+1):
            for c in range(c0,c1+1):
                out[r][c]=color
    return out

def solve_M16(g):
    s1, d1 = align_shape_cells(g,1)
    s2, d2 = align_shape_cells(g,2)
    h=max(d1[0] if s1 else 0, d2[0] if s2 else 0)
    w=max(d1[1] if s1 else 0, d2[1] if s2 else 0)
    out=[[0]*w for _ in range(h)]
    for r in range(h):
        for c in range(w):
            present = ((r,c) in s1) ^ ((r,c) in s2)
            if present:
                out[r][c]=8
    return out

def solve_M17(g):
    out=[[0]*len(g[0]) for _ in range(len(g))]
    for comp in components(g):
        color = 3 if len(comp["cells"])%2==1 else 8
        for r,c in comp["cells"]:
            out[r][c]=color
    return out

def solve_M18(g):
    h,w=dims(g)
    pivot=None
    cells=[]
    color=None
    for r in range(h):
        for c in range(w):
            v=g[r][c]
            if v==2:
                pivot=(r,c)
            elif v!=0:
                cells.append((r,c,v))
                color=v
    assert pivot is not None
    out=[[0]*w for _ in range(h)]
    pr,pc=pivot
    for r,c,v in cells:
        dr,dc=r-pr,c-pc
        nr,nc=pr+dc, pc-dr
        if 0<=nr<h and 0<=nc<w:
            out[nr][nc]=v
    return out

def solve_M19(g):
    h,w=dims(g)
    out=[[0]*w for _ in range(h)]
    colors=sorted({v for row in g for v in row if v!=0})
    for color in colors:
        cells=[(r,c) for r,row in enumerate(g) for c,v in enumerate(row) if v==color]
        if not cells:
            continue
        r0,c0,r1,c1=bbox(cells)
        for r in range(r0,r1+1):
            for c in range(c0,c1+1):
                out[r][c]=color
    return out

def solve_M20(g):
    h,w=dims(g)
    marker=None
    # objects are all nonzero except marker color 9
    for r in range(h):
        for c in range(w):
            if g[r][c]==9:
                marker=(r,c)
    assert marker is not None
    mr,mc=marker
    comps=components([[0 if v==9 else v for v in row] for row in g])
    best=None
    for comp in comps:
        dist=min(abs(r-mr)+abs(c-mc) for r,c in comp["cells"])
        key=(dist, comp["bbox"][0], comp["bbox"][1])
        if best is None or key<best[0]:
            best=(key,comp)
    comp=best[1]
    r0,c0,r1,c1=comp["bbox"]
    out=[[0]*(c1-c0+1) for _ in range(r1-r0+1)]
    for r,c in comp["cells"]:
        out[r-r0][c-c0]=comp["color"]
    return out

def solve_M21(g):
    out=clone(g)
    for comp in components(g):
        color=comp["color"]
        r0,c0,r1,c1=comp["bbox"]
        for r,c in comp["cells"]:
            rr=r0+r1-r
            cc=c0+c1-c
            out[rr][cc]=color
    return out

def solve_H15(g):
    # control at top-left cell: 3=OR,4=XOR,5=AND; shapes colors 1 and 2
    ctrl=g[0][0]
    s1,d1=align_shape_cells(g,1)
    s2,d2=align_shape_cells(g,2)
    h=max(d1[0] if s1 else 0, d2[0] if s2 else 0)
    w=max(d1[1] if s1 else 0, d2[1] if s2 else 0)
    out=[[0]*w for _ in range(h)]
    for r in range(h):
        for c in range(w):
            a=(r,c) in s1
            b=(r,c) in s2
            if ctrl==3:
                ok=a or b
            elif ctrl==4:
                ok=(a ^ b)
            elif ctrl==5:
                ok=(a and b)
            else:
                ok=False
            if ok:
                out[r][c]=8
    return out

def solve_H16(g):
    ctrl=None
    cells=[]
    for r,row in enumerate(g):
        for c,v in enumerate(row):
            if v in (2,3,4,5):
                ctrl=v
            elif v==1:
                cells.append((r,c))
    k={2:0,3:1,4:2,5:3}[ctrl]
    rot=rotate_k_cells(cells,k)
    rmax=max(r for r,c in rot); cmax=max(c for r,c in rot)
    out=[[0]*(cmax+1) for _ in range(rmax+1)]
    for r,c in rot:
        out[r][c]=8
    return out

def solve_H17(g):
    # gray frames color 5, interior fill with color of largest enclosed non-gray object
    h,w=dims(g)
    out=[[0]*w for _ in range(h)]
    # keep frames
    for r in range(h):
        for c in range(w):
            if g[r][c]==5:
                out[r][c]=5
    # detect rectangular frames as components of 5 with bbox perimeter only
    for comp in components(g, colors={5}):
        r0,c0,r1,c1=comp["bbox"]
        inside=[(r,c) for r in range(r0+1,r1) for c in range(c0+1,c1)]
        # find non-zero non-5 comps inside based on original grid restricting to inside
        sub={}
        # use components on masked subgrid
        cells_inside={(r,c) for r,c in inside}
        seen=set()
        inner_comps=[]
        for r,c in inside:
            if (r,c) in seen:
                continue
            v=g[r][c]
            if v==0 or v==5:
                seen.add((r,c))
                continue
            stack=[(r,c)]
            seen.add((r,c))
            cells=[(r,c)]
            while stack:
                rr,cc=stack.pop()
                for dr,dc in DIR4:
                    nr,nc=rr+dr,cc+dc
                    if (nr,nc) in cells_inside and (nr,nc) not in seen and g[nr][nc]==v:
                        seen.add((nr,nc)); stack.append((nr,nc)); cells.append((nr,nc))
            inner_comps.append((len(cells), v))
        if inner_comps:
            size,color=max(inner_comps, key=lambda t:(t[0], t[1]))
            for r in range(r0+1,r1):
                for c in range(c0+1,c1):
                    out[r][c]=color
    return out

def solve_H18(g):
    # walls 5, seeds are nonzero non-wall colors; fill empty cells by nearest seed using BFS on open cells
    h,w=dims(g)
    out=clone(g)
    q=deque()
    owner=[[None]*w for _ in range(h)]
    dist=[[-1]*w for _ in range(h)]
    for r in range(h):
        for c in range(w):
            v=g[r][c]
            if v!=0 and v!=5:
                owner[r][c]=v
                dist[r][c]=0
                q.append((r,c))
    while q:
        r,c=q.popleft()
        for dr,dc in DIR4:
            nr,nc=r+dr,c+dc
            if not inb(g,nr,nc) or g[nr][nc]==5:
                continue
            if dist[nr][nc]==-1:
                dist[nr][nc]=dist[r][c]+1
                owner[nr][nc]=owner[r][c]
                q.append((nr,nc))
            else:
                # tie at same distance -> smaller color wins
                if dist[nr][nc]==dist[r][c]+1 and owner[r][c] is not None:
                    owner[nr][nc]=min(owner[nr][nc], owner[r][c])
    for r in range(h):
        for c in range(w):
            if g[r][c]!=5:
                out[r][c]=owner[r][c] if owner[r][c] is not None else 0
    return out

def solve_H19(g):
    # control at top-left value n in 1..9 indicates nth largest object among nonzero except control itself and color 9 markers absent
    n=g[0][0]
    g2=clone(g); g2[0][0]=0
    comps=components(g2)
    comps_sorted=sorted(comps, key=lambda comp:(-len(comp["cells"]), comp["bbox"][0], comp["bbox"][1]))
    comp=comps_sorted[n-1]
    r0,c0,r1,c1=comp["bbox"]
    out=[[0]*(c1-c0+1) for _ in range(r1-r0+1)]
    for r,c in comp["cells"]:
        out[r-r0][c-c0]=comp["color"]
    return out

def solve_H20(g):
    # global 90-degree symmetry completion around single pivot 2. blue cells 1. Output pivot kept and all rotations of blue cells added.
    h,w=dims(g)
    out=clone(g)
    pivot=None
    cells=[]
    for r in range(h):
        for c,v in enumerate(g[r]):
            if v==2: pivot=(r,c)
            elif v==1: cells.append((r,c))
    pr,pc=pivot
    for r,c in cells:
        dr,dc=r-pr,c-pc
        for _ in range(4):
            nr,nc=pr+dr,pc+dc
            if 0<=nr<h and 0<=nc<w:
                out[nr][nc]=1
            dr,dc=dc,-dr
    out[pr][pc]=2
    return out

def solve_H21(g):
    h,w=dims(g)
    out=[[5 if g[r][c]==5 else 0 for c in range(w)] for r in range(h)]
    seen=[[False]*w for _ in range(h)]
    for r in range(h):
        for c in range(w):
            if g[r][c]==5 or seen[r][c]:
                continue
            stack=[(r,c)]
            seen[r][c]=True
            cells=[]
            counts={}
            while stack:
                rr,cc=stack.pop()
                cells.append((rr,cc))
                v=g[rr][cc]
                if v in (2,3,4):
                    counts[v]=counts.get(v,0)+1
                for dr,dc in DIR4:
                    nr,nc=rr+dr,cc+dc
                    if inb(g,nr,nc) and not seen[nr][nc] and g[nr][nc]!=5:
                        seen[nr][nc]=True
                        stack.append((nr,nc))
            if counts:
                maj=max(counts.items(), key=lambda kv:(kv[1], -kv[0]))[0]
                for rr,cc in cells:
                    out[rr][cc]=maj
            else:
                for rr,cc in cells:
                    out[rr][cc]=0
    return out

SOLVERS = {
    'E15': solve_E15,
    'E16': solve_E16,
    'E17': solve_E17,
    'E18': solve_E18,
    'E19': solve_E19,
    'E20': solve_E20,
    'E21': solve_E21,
    'M15': solve_M15,
    'M16': solve_M16,
    'M17': solve_M17,
    'M18': solve_M18,
    'M19': solve_M19,
    'M20': solve_M20,
    'M21': solve_M21,
    'H15': solve_H15,
    'H16': solve_H16,
    'H17': solve_H17,
    'H18': solve_H18,
    'H19': solve_H19,
    'H20': solve_H20,
    'H21': solve_H21,
}

if __name__ == '__main__':
    print('Available solvers:', ', '.join(sorted(SOLVERS)))