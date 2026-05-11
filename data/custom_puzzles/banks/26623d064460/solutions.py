"""Reference solvers for ARC-style additional puzzle bank volume 2."""
from pathlib import Path
import json
import collections
from typing import List

Grid = List[List[int]]

DIR4 = [(-1,0),(1,0),(0,-1),(0,1)]

def parse_grid(s: str) -> Grid:
    lines = [line.strip() for line in s.strip().splitlines() if line.strip()]
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

def safe_at(g,r,c,d=0):
    return g[r][c] if inb(g,r,c) else d

def components(g: Grid, color=None):
    h,w=dims(g)
    seen=[[False]*w for _ in range(h)]
    comps=[]
    for r in range(h):
        for c in range(w):
            if seen[r][c]:
                continue
            val=g[r][c]
            if val==0 or (color is not None and val!=color):
                seen[r][c]=True
                continue
            target=val if color is None else color
            stack=[(r,c)]
            seen[r][c]=True
            cells=[]
            while stack:
                rr,cc=stack.pop()
                cells.append((rr,cc))
                for dr,dc in DIR4:
                    nr,nc=rr+dr,cc+dc
                    if inb(g,nr,nc) and not seen[nr][nc] and g[nr][nc]==target:
                        seen[nr][nc]=True
                        stack.append((nr,nc))
            comps.append((target,cells))
    return comps

def bbox(cells):
    rs=[r for r,c in cells]; cs=[c for r,c in cells]
    return min(rs), max(rs), min(cs), max(cs)

def normalize(cells):
    r0=min(r for r,c in cells); c0=min(c for r,c in cells)
    return sorted((r-r0,c-c0) for r,c in cells)

def rotate_cells(cells):
    # cells normalized
    cells=normalize(cells)
    h=max(r for r,c in cells)+1
    w=max(c for r,c in cells)+1
    return normalize([(c, h-1-r) for r,c in cells])

def reflect_cells(cells):
    cells=normalize(cells)
    h=max(r for r,c in cells)+1
    w=max(c for r,c in cells)+1
    return normalize([(r, w-1-c) for r,c in cells])

def dihedral_forms(cells):
    forms=[]
    x=normalize(cells)
    for _ in range(4):
        forms.append(tuple(x))
        forms.append(tuple(reflect_cells(x)))
        x=rotate_cells(x)
    uniq=[]
    seen=set()
    for f in forms:
        if f not in seen:
            seen.add(f); uniq.append(list(f))
    return uniq

def cells_with_hole(cells):
    # Determine if component has a 0-hole within bbox
    r0,r1,c0,c1=bbox(cells)
    occ=set(cells)
    H=r1-r0+1; W=c1-c0+1
    seen=set()
    from collections import deque
    q=deque()
    for r in range(r0,r1+1):
        for c in range(c0,c1+1):
            if r in (r0,r1) or c in (c0,c1):
                if (r,c) not in occ and (r,c) not in seen:
                    seen.add((r,c)); q.append((r,c))
    while q:
        r,c=q.popleft()
        for dr,dc in DIR4:
            nr,nc=r+dr,c+dc
            if r0<=nr<=r1 and c0<=nc<=c1 and (nr,nc) not in occ and (nr,nc) not in seen:
                seen.add((nr,nc)); q.append((nr,nc))
    for r in range(r0,r1+1):
        for c in range(c0,c1+1):
            if (r,c) not in occ and (r,c) not in seen:
                return True
    return False

def flood_fill_reachable(g,start,passable=lambda v: v==0):
    h,w=dims(g)
    from collections import deque
    q=deque([start]); seen={start}
    while q:
        r,c=q.popleft()
        for dr,dc in DIR4:
            nr,nc=r+dr,c+dc
            if inb(g,nr,nc) and (nr,nc) not in seen and passable(g[nr][nc]):
                seen.add((nr,nc)); q.append((nr,nc))
    return seen

def solve_e8(g):
    out=clone(g)
    h,w=dims(g)
    for r in range(h):
        for c in range(w):
            if g[r][c]==2 and all(safe_at(g,r+dr,c+dc,0)!=2 for dr,dc in DIR4):
                out[r][c]=3
    return out

def solve_e9(g):
    out=clone(g); h,w=dims(g)
    for r in range(h):
        for c in range(1,w-1):
            if g[r][c]==0 and g[r][c-1]==1 and g[r][c+1]==1:
                out[r][c]=1
    return out

def solve_e10(g):
    out=clone(g); h,w=dims(g)
    for r in range(1,h-1):
        for c in range(w):
            if g[r][c]==3 and g[r-1][c]==3 and g[r+1][c]==3:
                # require exact vertical triplet maybe neighbors above/below not 3
                if safe_at(g,r-2,c,0)!=3 and safe_at(g,r+2,c,0)!=3:
                    out[r][c]=4
    return out

def solve_e11(g):
    out=clone(g)
    for color,cells in components(g, color=7):
        h,w=dims(g)
        if any(r==0 or c==0 or r==h-1 or c==w-1 for r,c in cells):
            for r,c in cells:
                out[r][c]=0
    return out

def solve_e12(g):
    out=clone(g); h,w=dims(g)
    for r in range(h):
        for c in range(w):
            if g[r][c]==8 and safe_at(g,r,c-1,0)!=8 and safe_at(g,r,c+1,0)!=8 and safe_at(g,r-1,c,0)!=8 and safe_at(g,r+1,c,0)!=8:
                if c+1<w and out[r][c+1]==0:
                    out[r][c+1]=6
    return out

def solve_e13(g):
    # recolor exact yellow L triomino components to blue
    out=clone(g)
    for color,cells in components(g, color=4):
        if len(cells)==3:
            norm=normalize(cells)
            forms=[normalize([(0,0),(1,0),(1,1)]),
                   normalize([(0,1),(1,0),(1,1)]),
                   normalize([(0,0),(0,1),(1,0)]),
                   normalize([(0,0),(0,1),(1,1)])]
            if norm in forms:
                for r,c in cells:
                    out[r][c]=1
    return out

def solve_e14(g):
    out=clone(g); h,w=dims(g)
    for r in range(h):
        c=0
        while c<w:
            if g[r][c]==3 and safe_at(g,r,c-1,0)!=3:
                c2=c
                while c2+1<w and g[r][c2+1]==3:
                    c2+=1
                # segment from c to c2
                if c2+1<w and g[r][c2+1]==0:
                    out[r][c2+1]=2
                c=c2+1
            else:
                c+=1
    return out

def solve_m8(g):
    comps=components(g)
    if not comps:
        return clone(g)
    # nonzero components by size desc, tie by top-left reading order
    info=[]
    for color,cells in comps:
        b=bbox(cells)
        info.append((len(cells), b[0], b[2], color, cells))
    info.sort(key=lambda x:(-x[0], x[1], x[2]))
    target=info[1] if len(info)>=2 else info[0]
    out=clone(g)
    for _,_,_,color,cells in [target]:
        for r,c in cells:
            out[r][c]=8
    return out

def solve_m9(g):
    out=[[0]*len(g[0]) for _ in range(len(g))]
    for color,cells in components(g):
        r0,r1,c0,c1=bbox(cells)
        for r in range(r0,r1+1):
            for c in range(c0,c1+1):
                if r in (r0,r1) or c in (c0,c1):
                    out[r][c]=color
    return out

def solve_m10(g):
    out=clone(g)
    h,w=dims(g)
    # for each color appearing exactly twice, fill rectangle between cells
    pos_by_color=collections.defaultdict(list)
    for r in range(h):
        for c in range(w):
            if g[r][c]!=0:
                pos_by_color[g[r][c]].append((r,c))
    for color, cells in pos_by_color.items():
        if len(cells)==2:
            (r1,c1),(r2,c2)=cells
            # must be diagonal pair (neither same row nor same col)
            if r1!=r2 and c1!=c2:
                for r in range(min(r1,r2),max(r1,r2)+1):
                    for c in range(min(c1,c2),max(c1,c2)+1):
                        out[r][c]=color
    return out

def solve_m11(g):
    # vertical divider 5 or horizontal divider 5; a single marker 2 indicates source side.
    h,w=dims(g)
    out=clone(g)
    # assume one full divider line of 5s
    vert=None; horiz=None
    for c in range(w):
        if all(g[r][c]==5 for r in range(h)):
            vert=c; break
    for r in range(h):
        if all(g[r][c]==5 for c in range(w)):
            horiz=r; break
    # marker color 2 singletons; other object colors nonzero except 5 and 2
    markers=[(r,c) for r in range(h) for c in range(w) if g[r][c]==2]
    if not markers:
        return out
    mr,mc=markers[0]
    if vert is not None:
        left_side = mc < vert
        # object components excluding 2 and 5 on source side only
        src_cells=[]
        color_map={}
        for r in range(h):
            for c in range(w):
                if g[r][c] not in (0,2,5) and ((c<vert)==left_side):
                    nr, nc = r, 2*vert-c
                    if inb(g,nr,nc) and nc!=vert:
                        out[nr][nc]=g[r][c]
        out[mr][mc]=0
    elif horiz is not None:
        top_side = mr < horiz
        for r in range(h):
            for c in range(w):
                if g[r][c] not in (0,2,5) and ((r<horiz)==top_side):
                    nr, nc = 2*horiz-r, c
                    if inb(g,nr,nc) and nr!=horiz:
                        out[nr][nc]=g[r][c]
        out[mr][mc]=0
    return out

def solve_m12(g):
    # find component with hole, place at top-left on blank grid same size using same bbox size and color
    h,w=dims(g)
    out=[[0]*w for _ in range(h)]
    target=None; color=None
    for col,cells in components(g):
        if cells_with_hole(cells):
            target=cells; color=col; break
    if target is None:
        return out
    norm=normalize(target)
    for r,c in norm:
        out[r][c]=color
    return out

def solve_m13(g):
    # one object color 6, one arrow marker color indicates direction: 1 left,2 up,3 right,4 down
    h,w=dims(g)
    out=[[0]*w for _ in range(h)]
    marker=None
    for r in range(h):
        for c in range(w):
            if g[r][c] in (1,2,3,4):
                marker=(r,c,g[r][c]); break
        if marker: break
    drdc={1:(0,-1),2:(-1,0),3:(0,1),4:(1,0)}
    dr,dc=drdc[marker[2]]
    cells=[(r,c) for r in range(h) for c in range(w) if g[r][c]==6]
    for r,c in cells:
        nr,nc=r+dr,c+dc
        if inb(g,nr,nc):
            out[nr][nc]=6
    return out

def solve_m14(g):
    # replace each filled rectangle component with its border only, same color
    h,w=dims(g)
    out=[[0]*w for _ in range(h)]
    for color,cells in components(g):
        r0,r1,c0,c1=bbox(cells)
        # assume filled rectangle
        for r in range(r0,r1+1):
            for c in range(c0,c1+1):
                if r in (r0,r1) or c in (c0,c1):
                    out[r][c]=color
    return out

def solve_h8(g):
    # walls 5, seed 2; fill reachable 0s from seed with 8, keep seed 2
    out=clone(g)
    h,w=dims(g)
    seeds=[(r,c) for r in range(h) for c in range(w) if g[r][c]==2]
    if not seeds: return out
    start=seeds[0]
    reachable=flood_fill_reachable(g,start,passable=lambda v: v in (0,2))
    for r,c in reachable:
        if g[r][c]==0:
            out[r][c]=8
    return out

def solve_h9(g):
    # two objects colors 2 and 3. Align by top-left of bbox; output intersection at top-left in color 8 on blank grid same size
    h,w=dims(g)
    out=[[0]*w for _ in range(h)]
    objs={}
    for color,cells in components(g):
        if color in (2,3):
            objs[color]=cells
    if 2 not in objs or 3 not in objs:
        return out
    n2=set(normalize(objs[2])); n3=set(normalize(objs[3]))
    inter=n2 & n3
    for r,c in inter:
        out[r][c]=8
    return out

def solve_h10(g):
    # top row 1 markers select columns; left col 2 markers select rows; output green(3) intersections on blank grid same size
    h,w=dims(g)
    out=[[0]*w for _ in range(h)]
    cols=[c for c in range(w) if g[0][c]==1]
    rows=[r for r in range(h) if g[r][0]==2]
    for r in rows:
        for c in cols:
            out[r][c]=3
    return out

def solve_h11(g):
    # recolor odd-one-out under dihedral symmetry among color 4 objects to color 8
    out=clone(g)
    comps=[cells for color,cells in components(g,color=4)]
    canonical=[min(tuple(form) for form in dihedral_forms(cells)) for cells in comps]
    freq=collections.Counter(canonical)
    for cells,can in zip(comps,canonical):
        if freq[can]==1:
            for r,c in cells:
                out[r][c]=8
            break
    return out

def solve_h12(g):
    # outer rectangle border color 4 and inner rectangle border color 1; fill annulus between them with 8, keep borders
    out=clone(g)
    comps_by_color={4:[],1:[]}
    for col,cells in components(g):
        if col in comps_by_color:
            comps_by_color[col].append(cells)
    if not comps_by_color[4] or not comps_by_color[1]:
        return out
    outer=max(comps_by_color[4], key=lambda c: len(c))
    inner=max(comps_by_color[1], key=lambda c: len(c))
    ro0,ro1,co0,co1=bbox(outer)
    ri0,ri1,ci0,ci1=bbox(inner)
    for r in range(ro0+1,ro1):
        for c in range(co0+1,co1):
            if not (ri0<=r<=ri1 and ci0<=c<=ci1):
                out[r][c]=8
    return out

def solve_h13(g):
    # template color 3 component. Markers colors: 1=0deg,2=90,4=180,6=270. Copy template at marker cell as top-left of rotated bbox, remove markers/template? maybe keep template and add copies. output blank except copies? Let's choose output with copies only, markers removed, original template removed.
    h,w=dims(g)
    out=[[0]*w for _ in range(h)]
    # template is the largest color-3 component? or unique component not a single marker.
    comps3=[cells for col,cells in components(g,color=3)]
    if not comps3:
        return out
    template=max(comps3,key=len)
    base=normalize(template)
    markers=[]
    for r in range(h):
        for c in range(w):
            if g[r][c] in (1,2,4,6):
                markers.append((r,c,g[r][c]))
    rot_map={1:0,2:1,4:2,6:3}
    def rot_n(cells,n):
        x=normalize(cells)
        for _ in range(n):
            x=rotate_cells(x)
        return x
    for r,c,color in markers:
        shape=rot_n(base, rot_map[color])
        for dr,dc in shape:
            nr,nc=r+dr,c+dc
            if inb(g,nr,nc):
                out[nr][nc]=3
    return out

def solve_h14(g):
    # walls 5, seeds colors 1-4 fill their compartments (zeros) with same seed color
    out=clone(g)
    h,w=dims(g)
    seeds=[(r,c,g[r][c]) for r in range(h) for c in range(w) if g[r][c] in (1,2,3,4)]
    filled=set()
    for r,c,color in seeds:
        region=flood_fill_reachable(g,(r,c),passable=lambda v, color=color: v in (0,color))
        for rr,cc in region:
            if g[rr][cc]==0:
                out[rr][cc]=color
    return out

SOLVERS = {
    "E8": solve_e8,
    "E9": solve_e9,
    "E10": solve_e10,
    "E11": solve_e11,
    "E12": solve_e12,
    "E13": solve_e13,
    "E14": solve_e14,
    "M8": solve_m8,
    "M9": solve_m9,
    "M10": solve_m10,
    "M11": solve_m11,
    "M12": solve_m12,
    "M13": solve_m13,
    "M14": solve_m14,
    "H8": solve_h8,
    "H9": solve_h9,
    "H10": solve_h10,
    "H11": solve_h11,
    "H12": solve_h12,
    "H13": solve_h13,
    "H14": solve_h14,
}

def load_bank(path: Path | None = None):
    path = path or Path(__file__).with_name("arc_additional_puzzle_bank_volume2.json")
    return json.loads(path.read_text())

def validate(bank=None):
    bank = bank or load_bank()
    for puzzle in bank:
        solver = SOLVERS[puzzle["id"]]
        for pair in puzzle["train"] + puzzle["test"]:
            got = solver(pair["input"])
            if got != pair["output"]:
                raise AssertionError(f'Mismatch for {puzzle["id"]}\nExpected:\n{grid_to_str(pair["output"])}\nGot:\n{grid_to_str(got)}')
    print(f"validated {len(bank)} puzzles")

if __name__ == "__main__":
    validate()