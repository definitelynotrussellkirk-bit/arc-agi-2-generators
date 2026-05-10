"""Reference solvers for ARC-style additional puzzle bank volume 10.

This volume leans into exact-shape completion, divider reflection, control-driven
rotations, rectangle construction, shortest paths, wall-constrained Voronoi fills,
nested-frame band selection, and legend-based chamber fills.

New helper primitives emphasized here:
- apply_dihedral(shape, reflect_code, rot_code)
- shortest_path(grid, start, goal, blocked)
- band_between_nested_frames(frames, k)  # conceptual, used in H67
- combine_shapes(a, b, op)
"""
from typing import List
from collections import deque
import collections

Grid = List[List[int]]
DIR4 = [(-1,0),(1,0),(0,-1),(0,1)]
ROT_MAP = {2:0,4:1,5:2,6:3}
OP_MAP = {3:"union",4:"inter",6:"xor",7:"diff12"}

def blank(h,w,val=0):
    return [[val]*w for _ in range(h)]

def clone(g):
    return [row[:] for row in g]

def dims(g):
    return len(g), len(g[0])

def bbox(cells):
    rs=[r for r,c in cells]; cs=[c for r,c in cells]
    return min(rs), min(cs), max(rs), max(cs)

def normalize(cells):
    cells=set(cells)
    if not cells: return set()
    r0,c0,r1,c1 = bbox(cells)
    return {(r-r0, c-c0) for r,c in cells}

def render_shape(shape, color=1):
    s=normalize(shape)
    if not s:
        return [[0]]
    h=max(r for r,c in s)+1
    w=max(c for r,c in s)+1
    g=blank(h,w)
    for r,c in s:
        g[r][c]=color
    return g

def rotate_shape(shape, k=1):
    s=normalize(shape)
    for _ in range(k%4):
        if not s: return set()
        h=max(r for r,c in s)+1
        s={(c, h-1-r) for r,c in s}
        s=normalize(s)
    return s

def reflect_h(shape):
    s=normalize(shape)
    if not s: return set()
    w=max(c for r,c in s)+1
    return normalize({(r, w-1-c) for r,c in s})

def scale_shape(shape, k):
    s=normalize(shape)
    out=set()
    for r,c in s:
        for dr in range(k):
            for dc in range(k):
                out.add((r*k+dr,c*k+dc))
    return normalize(out)

def components(g, colors=None, bg=0):
    h,w=dims(g)
    seen=[[False]*w for _ in range(h)]
    out=[]
    for r in range(h):
        for c in range(w):
            if seen[r][c]: continue
            seen[r][c]=True
            v=g[r][c]
            if v==bg or (colors is not None and v not in colors):
                continue
            stack=[(r,c)]
            cells=[(r,c)]
            while stack:
                rr,cc=stack.pop()
                for dr,dc in DIR4:
                    nr,nc=rr+dr,cc+dc
                    if 0<=nr<h and 0<=nc<w and not seen[nr][nc] and g[nr][nc]==v:
                        seen[nr][nc]=True
                        stack.append((nr,nc))
                        cells.append((nr,nc))
            out.append({"color":v, "cells":cells, "bbox":bbox(cells)})
    return out

def crop_to_bbox(g, cells):
    r0,c0,r1,c1=bbox(cells)
    out=blank(r1-r0+1, c1-c0+1)
    for r in range(r0,r1+1):
        for c in range(c0,c1+1):
            out[r-r0][c-c0]=g[r][c]
    return out

def chamber_regions_by_walls(grid, wall=5):
    h,w=dims(grid)
    seen=[[False]*w for _ in range(h)]
    regs=[]
    for r in range(h):
        for c in range(w):
            if seen[r][c] or grid[r][c]==wall:
                continue
            stack=[(r,c)]; seen[r][c]=True; cells=[(r,c)]
            while stack:
                rr,cc=stack.pop()
                for dr,dc in DIR4:
                    nr,nc=rr+dr,cc+dc
                    if 0<=nr<h and 0<=nc<w and not seen[nr][nc] and grid[nr][nc]!=wall:
                        seen[nr][nc]=True; stack.append((nr,nc)); cells.append((nr,nc))
            regs.append(cells)
    return regs

def shortest_path(grid, start, goal, blocked={5}):
    h,w=dims(grid)
    q=deque([start]); prev={start:None}
    while q:
        r,c=q.popleft()
        if (r,c)==goal: break
        for dr,dc in DIR4:
            nr,nc=r+dr,c+dc
            if 0<=nr<h and 0<=nc<w and (nr,nc) not in prev and grid[nr][nc] not in blocked:
                prev[(nr,nc)]=(r,c); q.append((nr,nc))
    if goal not in prev:
        return None
    path=[]; cur=goal
    while cur is not None:
        path.append(cur); cur=prev[cur]
    return path[::-1]

def dist_from_seeds(grid, seed_color, wall=5):
    h,w=dims(grid)
    INF=10**9
    dist=[[INF]*w for _ in range(h)]
    q=deque()
    for r in range(h):
        for c in range(w):
            if grid[r][c]==seed_color:
                dist[r][c]=0
                q.append((r,c))
    while q:
        r,c=q.popleft()
        for dr,dc in DIR4:
            nr,nc=r+dr,c+dc
            if 0<=nr<h and 0<=nc<w and grid[nr][nc]!=wall and dist[nr][nc]==INF:
                dist[nr][nc]=dist[r][c]+1
                q.append((nr,nc))
    return dist

def rectangular_frames(grid, color=4):
    comps=components(grid, colors={color})
    frames=[]
    for comp in comps:
        cells=set(comp["cells"])
        r0,c0,r1,c1=bbox(cells)
        # check perimeter rectangle
        perim={(r0,c) for c in range(c0,c1+1)} | {(r1,c) for c in range(c0,c1+1)} | {(r,c0) for r in range(r0,r1+1)} | {(r,c1) for r in range(r0,r1+1)}
        if cells==perim:
            frames.append((r0,c0,r1,c1))
    frames.sort(key=lambda b: ((b[2]-b[0]+1)*(b[3]-b[1]+1)), reverse=True)
    return frames

def apply_dihedral(shape, reflect_code, rot_code):
    s=normalize(shape)
    if reflect_code==3:
        s=reflect_h(s)
    rot_map={4:0,5:1,6:2,7:3}
    s=rotate_shape(s, rot_map[rot_code])
    return s

def combine_shapes(s1,s2,op):
    s1=set(s1); s2=set(s2)
    if op=="union":
        return s1|s2
    if op=="inter":
        return s1&s2
    if op=="xor":
        return (s1-s2)|(s2-s1)
    if op=="diff12":
        return s1-s2
    raise ValueError(op)

def solve_E64(grid):
    out=clone(grid)
    for comp in components(grid, colors={2}):
        cells=set(comp["cells"])
        if len(cells)==3:
            r0,c0,r1,c1=bbox(cells)
            if (r1-r0+1, c1-c0+1)==(2,2):
                for r in range(r0,r1+1):
                    for c in range(c0,c1+1):
                        out[r][c]=3
    return out

def solve_E65(grid):
    out=clone(grid)
    h,w=dims(grid)
    for r in range(h-1):
        for c in range(w-1):
            block=[[grid[r+dr][c+dc] for dc in range(2)] for dr in range(2)]
            vals=[block[dr][dc] for dr in range(2) for dc in range(2)]
            if vals.count(1)==2 and vals.count(0)==2:
                if (block[0][0]==1 and block[1][1]==1 and block[0][1]==0 and block[1][0]==0) or \
                   (block[0][1]==1 and block[1][0]==1 and block[0][0]==0 and block[1][1]==0):
                    for dr in range(2):
                        for dc in range(2):
                            out[r+dr][c+dc]=8
    return out

def solve_E66(grid):
    out=clone(grid)
    h,w=dims(grid)
    for r in range(h):
        c=0
        while c<w:
            if grid[r][c]==4:
                c2=c
                while c2<w and grid[r][c2]==4:
                    c2+=1
                length=c2-c
                if length==3:
                    left_blank = c-1>=0 and grid[r][c-1]==0
                    right_blank = c2<w and grid[r][c2]==0
                    # ensure not part of vertical block? not necessary maybe exact horizontal run
                    if left_blank:
                        out[r][c-1]=6
                    if right_blank:
                        out[r][c2]=6
                c=c2
            else:
                c+=1
    return out

def solve_E67(grid):
    out=clone(grid)
    h,w=dims(grid)
    for comp in components(grid, colors={1}):
        cells=comp["cells"]
        touches_top=any(r==0 for r,c in cells)
        touches_other=any(r==h-1 or c==0 or c==w-1 for r,c in cells)
        if touches_top and not touches_other:
            for r,c in cells:
                out[r][c]=3
    return out

def solve_E68(grid):
    out=clone(grid)
    h,w=dims(grid)
    divider_cols=[c for c in range(w) if all(grid[r][c]==6 for r in range(h))]
    if not divider_cols:
        return out
    cdiv=divider_cols[0]
    orange=[(r,c) for r in range(h) for c in range(cdiv) if grid[r][c]==7]
    for r,c in orange:
        mc = 2*cdiv - c
        if 0<=mc<w and out[r][mc]==0:
            out[r][mc]=8
    return out

def solve_E69(grid):
    comps=[]
    h,w=dims(grid)
    seen=[[False]*w for _ in range(h)]
    for r in range(h):
        for c in range(w):
            if seen[r][c] or grid[r][c]==0: 
                seen[r][c]=seen[r][c] or False
                continue
            color=grid[r][c]
            stack=[(r,c)]; seen[r][c]=True; cells=[(r,c)]
            while stack:
                rr,cc=stack.pop()
                for dr,dc in DIR4:
                    nr,nc=rr+dr,cc+dc
                    if 0<=nr<h and 0<=nc<w and not seen[nr][nc] and grid[nr][nc]==color:
                        seen[nr][nc]=True; stack.append((nr,nc)); cells.append((nr,nc))
            comps.append(cells)
    comps.sort(key=lambda cells:(len(cells), bbox(cells)))
    target=comps[0]
    return crop_to_bbox(grid, target)

def solve_E70(grid):
    out=clone(grid)
    for comp in components(grid, colors={2}):
        cells=comp["cells"]
        if len(cells)==1:
            r,c=cells[0]
            for rr,cc in [(r,c),(r-1,c),(r+1,c),(r,c-1),(r,c+1)]:
                if 0<=rr<len(grid) and 0<=cc<len(grid[0]):
                    out[rr][cc]=4
    return out

def solve_M64(grid):
    out=clone(grid)
    h,w=dims(grid)
    positions=collections.defaultdict(list)
    for r in range(h):
        for c in range(w):
            v=grid[r][c]
            if v!=0:
                positions[v].append((r,c))
    for color, cells in positions.items():
        if len(cells)==2:
            (r1,c1),(r2,c2)=cells
            if r1!=r2 and c1!=c2:
                for c in range(min(c1,c2), max(c1,c2)+1):
                    out[r1][c]=color; out[r2][c]=color
                for r in range(min(r1,r2), max(r1,r2)+1):
                    out[r][c1]=color; out[r][c2]=color
    return out

def solve_M65(grid):
    out=clone(grid)
    h,w=dims(grid)
    control=None; anchor=None
    for r in range(h):
        for c in range(w):
            if grid[r][c] in ROT_MAP:
                control=(r,c,grid[r][c])
            if grid[r][c]==9:
                anchor=(r,c)
    if control is None or anchor is None:
        return out
    comps=components(grid, colors={3})
    if not comps:
        return out
    comps.sort(key=lambda comp:(len(comp["cells"]), bbox(comp["cells"])))
    shape=normalize(comps[0]["cells"])
    shape=rotate_shape(shape, ROT_MAP[control[2]])
    ar,ac=anchor
    for dr,dc in shape:
        rr,cc=ar+dr, ac+dc
        if 0<=rr<h and 0<=cc<w:
            out[rr][cc]=8
    return out

def solve_M66(grid):
    out=clone(grid)
    for cells in chamber_regions_by_walls(grid, wall=5):
        seeds=sum(1 for r,c in cells if grid[r][c]==2)
        if seeds==2:
            for r,c in cells:
                if grid[r][c]==0:
                    out[r][c]=8
    return out

def solve_M67(grid):
    out=clone(grid)
    comps=components(grid, colors={1})
    comps.sort(key=lambda comp:(len(comp["cells"]), bbox(comp["cells"])))
    if len(comps) >= 3:
        recolors=[2,3,8]
        for comp,newc in zip(comps[:3], recolors):
            for r,c in comp["cells"]:
                out[r][c]=newc
    return out

def solve_M68(grid):
    cells=[(r,c) for r,row in enumerate(grid) for c,v in enumerate(row) if v in {1,2,4}]
    if not cells:
        return clone(grid)
    r0,c0,r1,c1=bbox(cells)
    out=clone(grid)
    rows=[r for r in range(r0+1,r1) if grid[r][c0]==2]
    cols=[c for c in range(c0+1,c1) if grid[r0][c]==1]
    for r in rows:
        for c in cols:
            out[r][c]=3
    return out

def solve_M69(grid):
    comps1=components(grid, colors={1})
    comps2=components(grid, colors={2})
    if not comps1 or not comps2:
        return [[0]]
    s1=normalize(comps1[0]["cells"])
    s2=normalize(comps2[0]["cells"])
    xor = (s1 - s2) | (s2 - s1)
    return render_shape(xor, 8)

def solve_M70(grid):
    out=clone(grid)
    start=goal=None
    for r,row in enumerate(grid):
        for c,v in enumerate(row):
            if v==2: start=(r,c)
            elif v==3: goal=(r,c)
    if start is None or goal is None:
        return out
    path=shortest_path(grid, start, goal, blocked={5})
    if path:
        for r,c in path[1:-1]:
            out[r][c]=8
    return out

def solve_H64(grid):
    out=clone(grid)
    reflect_code=rot_code=None; anchor=None
    for r,row in enumerate(grid):
        for c,v in enumerate(row):
            if v in {2,3} and reflect_code is None:
                reflect_code=v
            elif v in {4,5,6,7} and rot_code is None:
                rot_code=v
            elif v==9:
                anchor=(r,c)
    comps=components(grid, colors={1})
    if reflect_code is None or rot_code is None or anchor is None or not comps:
        return out
    shape=normalize(comps[0]["cells"])
    shape=apply_dihedral(shape, reflect_code, rot_code)
    ar,ac=anchor
    for dr,dc in shape:
        rr,cc=ar+dr, ac+dc
        if 0<=rr<len(grid) and 0<=cc<len(grid[0]):
            out[rr][cc]=8
    return out

def solve_H65(grid):
    out=clone(grid)
    pts={}
    for r,row in enumerate(grid):
        for c,v in enumerate(row):
            if v in {2,3,4,7}:
                pts[v]=(r,c)
    if not all(k in pts for k in (2,3,4,7)):
        return out
    order=[2,3,4,7]
    for a,b in zip(order, order[1:]):
        path=shortest_path(grid, pts[a], pts[b], blocked={5})
        if not path:
            continue
        for r,c in path[1:-1]:
            out[r][c]=8
    return out

def solve_H66(grid):
    out=clone(grid)
    d2=dist_from_seeds(grid, 2, wall=5)
    d3=dist_from_seeds(grid, 3, wall=5)
    INF=10**9
    h,w=dims(grid)
    for r in range(h):
        for c in range(w):
            if grid[r][c]==0:
                if d2[r][c] < d3[r][c]:
                    out[r][c]=2
                elif d3[r][c] < d2[r][c]:
                    out[r][c]=3
                else:
                    out[r][c]=0
    return out

def solve_H67(grid):
    out=clone(grid)
    frames=rectangular_frames(grid, color=4)
    if not frames:
        return out
    k=sum(1 for v in grid[0] if v==2)
    k=max(1, min(k, len(frames)))
    r0,c0,r1,c1 = frames[k-1]
    inner = frames[k] if k < len(frames) else None
    for r in range(r0+1, r1):
        for c in range(c0+1, c1):
            if inner and inner[0] < r < inner[2] and inner[1] < c < inner[3]:
                continue
            if out[r][c]==0:
                out[r][c]=8
    return out

def solve_H68(grid):
    comps=components(grid, colors={1})
    freq=collections.Counter(tuple(sorted(normalize(comp["cells"]))) for comp in comps)
    target_shape=None
    for comp in comps:
        key=tuple(sorted(normalize(comp["cells"])))
        if freq[key]==1:
            target_shape=set(key)
            break
    if target_shape is None:
        return [[0]]
    return render_shape(scale_shape(target_shape, 2), 8)

def solve_H69(grid):
    control=None
    for r,row in enumerate(grid):
        for c,v in enumerate(row):
            if v in OP_MAP:
                control=v; break
        if control is not None: break
    comps1=components(grid, colors={1}); comps2=components(grid, colors={2})
    if control is None or not comps1 or not comps2:
        return [[0]]
    s1=normalize(comps1[0]["cells"])
    s2=normalize(comps2[0]["cells"])
    result=combine_shapes(s1,s2,OP_MAP[control])
    return render_shape(result, 8)

def solve_H70(grid):
    out=clone(grid)
    h,w=dims(grid)
    mapping={}
    for c in range(w):
        top=grid[0][c]
        bot=grid[1][c] if h>1 else 0
        if top in {1,2,3} and bot!=0:
            mapping[top]=bot
    # regions below legend rows
    sub=[row[:] for row in grid[2:]]
    regs=chamber_regions_by_walls(sub, wall=5)
    for cells in regs:
        counts=collections.Counter(sub[r][c] for r,c in cells if sub[r][c] in {1,2,3})
        if counts:
            mc=counts.most_common()
            if len(mc)==1 or mc[0][1] > mc[1][1]:
                maj=mc[0][0]
                fill_color=mapping.get(maj, 8)
                for r,c in cells:
                    if sub[r][c]==0:
                        out[r+2][c]=fill_color
    return out

SOLVERS = {
    "E64": solve_E64,
    "E65": solve_E65,
    "E66": solve_E66,
    "E67": solve_E67,
    "E68": solve_E68,
    "E69": solve_E69,
    "E70": solve_E70,
    "M64": solve_M64,
    "M65": solve_M65,
    "M66": solve_M66,
    "M67": solve_M67,
    "M68": solve_M68,
    "M69": solve_M69,
    "M70": solve_M70,
    "H64": solve_H64,
    "H65": solve_H65,
    "H66": solve_H66,
    "H67": solve_H67,
    "H68": solve_H68,
    "H69": solve_H69,
    "H70": solve_H70,
}

if __name__ == '__main__':
    import json
    from pathlib import Path
    data = json.loads(Path(__file__).with_name('arc_additional_puzzle_bank_volume10.json').read_text())
    for puzzle in data:
        solver = SOLVERS[puzzle['id']]
        for pair in puzzle['train'] + puzzle['test']:
            got = solver(pair['input'])
            assert got == pair['output'], f"validation failed for {puzzle['id']}"
    print(f'validated {len(data)} puzzles')
