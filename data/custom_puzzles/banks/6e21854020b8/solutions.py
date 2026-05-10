"""Reference solvers for ARC-style additional puzzle bank volume 11.

This volume leans into border-signature filters, sparse rectangle completion,
control-driven rotations, shortest-path routing, nested-frame band selection,
graph-distance dilation, mirror-beam tracing, and shortest-path intersection.

New helper primitives emphasized here:
- trace_beam(grid)
- mandatory_shortest_path_cells(grid, start, goal)  # conceptual, used in H77
- graph_dilate(seed_cells, blocked, radius)         # conceptual, used in H73
- selected_frame_band(frames, k)                    # conceptual, used in H72
"""
from typing import List
from collections import deque, Counter, defaultdict
import itertools

Grid = List[List[int]]
DIR4 = [(-1,0),(1,0),(0,-1),(0,1)]
DIR_CODE = {1:(-1,0), 2:(0,1), 3:(1,0), 4:(0,-1)}

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
    if not cells:
        return set()
    r0,c0,r1,c1=bbox(cells)
    return {(r-r0,c-c0) for r,c in cells}


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
        if not s: 
            return set()
        h=max(r for r,c in s)+1
        s={(c, h-1-r) for r,c in s}
        s=normalize(s)
    return s


def scale_shape(shape, k):
    s=normalize(shape)
    out=set()
    for r,c in s:
        for dr in range(k):
            for dc in range(k):
                out.add((r*k+dr, c*k+dc))
    return normalize(out)


def fill_rect(g,r0,c0,r1,c1,color):
    for r in range(r0,r1+1):
        for c in range(c0,c1+1):
            g[r][c]=color


def draw_rect_border(g, r0,c0,r1,c1, color):
    for c in range(c0,c1+1):
        g[r0][c]=g[r1][c]=color
    for r in range(r0,r1+1):
        g[r][c0]=g[r][c1]=color


def components(g, colors=None, bg=0):
    h,w=dims(g)
    seen=[[False]*w for _ in range(h)]
    out=[]
    for r in range(h):
        for c in range(w):
            if seen[r][c]:
                continue
            seen[r][c]=True
            v=g[r][c]
            if v==bg or (colors is not None and v not in colors):
                continue
            q=[(r,c)]
            cells=[(r,c)]
            while q:
                rr,cc=q.pop()
                for dr,dc in DIR4:
                    nr,nc=rr+dr,cc+dc
                    if 0<=nr<h and 0<=nc<w and not seen[nr][nc] and g[nr][nc]==v:
                        seen[nr][nc]=True
                        q.append((nr,nc))
                        cells.append((nr,nc))
            out.append({"color":v,"cells":cells})
    return out


def shortest_path_cells(grid, start, goal, blocked={5}):
    h,w=dims(grid)
    q=deque([start])
    prev={start: None}
    while q:
        cur=q.popleft()
        if cur==goal:
            break
        r,c=cur
        for dr,dc in DIR4:
            nr,nc=r+dr,c+dc
            if 0<=nr<h and 0<=nc<w and (nr,nc) not in prev and grid[nr][nc] not in blocked:
                prev[(nr,nc)] = cur
                q.append((nr,nc))
    if goal not in prev:
        return None
    path=[]
    cur=goal
    while cur is not None:
        path.append(cur)
        cur=prev[cur]
    path.reverse()
    return path


def multi_source_distance(grid, starts, blocked={5}):
    h,w=dims(grid)
    dist=[[None]*w for _ in range(h)]
    q=deque()
    for s in starts:
        r,c=s
        dist[r][c]=0
        q.append(s)
    while q:
        r,c=q.popleft()
        for dr,dc in DIR4:
            nr,nc=r+dr,c+dc
            if 0<=nr<h and 0<=nc<w and dist[nr][nc] is None and grid[nr][nc] not in blocked:
                dist[nr][nc]=dist[r][c]+1
                q.append((nr,nc))
    return dist


def pairwise(iterable):
    xs=list(iterable)
    return zip(xs,xs[1:])


def border_touch_count(cells, h, w):
    count=0
    if any(r==0 for r,c in cells): count+=1
    if any(r==h-1 for r,c in cells): count+=1
    if any(c==0 for r,c in cells): count+=1
    if any(c==w-1 for r,c in cells): count+=1
    return count


def is_T_tetromino(cells):
    if len(cells)!=4:
        return False
    s=normalize(cells)
    # All rotations of T tetromino
    base={(0,0),(0,1),(0,2),(1,1)}
    rots={frozenset(rotate_shape(base,k)) for k in range(4)}
    return frozenset(s) in rots


def interior_cells_of_bbox(r0,c0,r1,c1):
    return {(r,c) for r in range(r0+1,r1) for c in range(c0+1,c1)}


def border_cells_of_bbox(r0,c0,r1,c1):
    cells=set()
    for c in range(c0,c1+1):
        cells.add((r0,c)); cells.add((r1,c))
    for r in range(r0,r1+1):
        cells.add((r,c0)); cells.add((r,c1))
    return cells


def combine_shapes(a, b, op):
    if op=="union": return a | b
    if op=="inter": return a & b
    if op=="xor": return a ^ b
    if op=="diff": return a - b
    raise ValueError(op)


def trace_beam(grid):
    h,w=dims(grid)
    start=None; d=None
    for r,row in enumerate(grid):
        for c,v in enumerate(row):
            if v in DIR_CODE:
                start=(r,c); d=DIR_CODE[v]; break
        if start: break
    if not start:
        return []
    r,c=start
    path=[]
    seen=set()
    while True:
        state=(r,c,d)
        if state in seen:
            break
        seen.add(state)
        nr,nc=r+d[0], c+d[1]
        if not (0<=nr<h and 0<=nc<w):
            break
        cell=grid[nr][nc]
        if cell==5:
            break
        # step into cell
        r,c=nr,nc
        path.append((r,c))
        if cell==6:      # slash /
            d=(-d[1], -d[0])
        elif cell==7:    # backslash \
            d=(d[1], d[0])
        else:
            pass
    return path


def shortest_path_dists_counts(grid, start, blocked={5}):
    h,w=dims(grid)
    dist=[[None]*w for _ in range(h)]
    count=[[0]*w for _ in range(h)]
    q=deque([start]); dist[start[0]][start[1]]=0; count[start[0]][start[1]]=1
    order=[start]
    while q:
        r,c=q.popleft()
        for dr,dc in DIR4:
            nr,nc=r+dr,c+dc
            if 0<=nr<h and 0<=nc<w and grid[nr][nc] not in blocked:
                nd=dist[r][c]+1
                if dist[nr][nc] is None:
                    dist[nr][nc]=nd; count[nr][nc]=count[r][c]; q.append((nr,nc)); order.append((nr,nc))
                elif dist[nr][nc]==nd:
                    count[nr][nc]+=count[r][c]
    return dist,count


def solve_E71(grid):
    out=clone(grid)
    for comp in components(grid, colors={2}):
        cells=comp["cells"]
        if is_T_tetromino(cells):
            r0,c0,r1,c1=bbox(cells)
            fill_rect(out,r0,c0,r1,c1,3)
    return out


def solve_E72(grid):
    out=clone(grid)
    h,w=dims(grid)
    pos=defaultdict(list)
    for r in range(h):
        for c,v in enumerate(grid[r]):
            if v!=0:
                pos[v].append((r,c))
    for color,cells in pos.items():
        if len(cells)!=2:
            continue
        (r1,c1),(r2,c2)=cells
        if r1==r2:
            lo,hi=sorted([c1,c2])
            if all(grid[r1][c]==0 for c in range(lo+1,hi)):
                for c in range(lo,hi+1):
                    out[r1][c]=color
        elif c1==c2:
            lo,hi=sorted([r1,r2])
            if all(grid[r][c1]==0 for r in range(lo+1,hi)):
                for r in range(lo,hi+1):
                    out[r][c1]=color
    return out


def solve_E73(grid):
    out=clone(grid)
    h,w=dims(grid)
    for comp in components(grid, colors={7}):
        if border_touch_count(comp["cells"],h,w)==1:
            for r,c in comp["cells"]:
                out[r][c]=8
    return out


def solve_E74(grid):
    out=clone(grid)
    h,w=dims(grid)
    for comp in components(grid, colors={2}):
        if len(comp["cells"])==1:
            r,c=comp["cells"][0]
            for rr,cc in [(r,c),(r-1,c-1),(r-1,c+1),(r+1,c-1),(r+1,c+1)]:
                if 0<=rr<h and 0<=cc<w and grid[rr][cc] in {0,2}:
                    out[rr][cc]=3
    return out


def solve_E75(grid):
    comps=components(grid, colors=None)
    if not comps:
        return [[0]]
    comps_sorted=sorted(comps, key=lambda comp: (len(comp["cells"]), bbox(comp["cells"])[0], bbox(comp["cells"])[1]))
    cells=comps_sorted[0]["cells"]
    r0,c0,r1,c1=bbox(cells)
    out=blank(r1-r0+1,c1-c0+1)
    for r,c in cells:
        out[r-r0][c-c0]=grid[r][c]
    return out


def solve_E76(grid):
    out=clone(grid)
    reds=[(r,c) for r,row in enumerate(grid) for c,v in enumerate(row) if v==2]
    redset=set(reds)
    added=set()
    for a,b,c in itertools.combinations(reds,3):
        rows={a[0],b[0],c[0]}
        cols={a[1],b[1],c[1]}
        if len(rows)==2 and len(cols)==2:
            for rr in rows:
                for cc in cols:
                    if (rr,cc) not in {a,b,c}:
                        added.add((rr,cc))
    for r,c in added:
        if out[r][c]==0:
            out[r][c]=3
    return out


def solve_E77(grid):
    out=clone(grid)
    h,w=dims(grid)
    for r in range(h-2):
        for c in range(w-2):
            cells=[grid[r+dr][c+dc] for dr in range(3) for dc in range(3)]
            if all(cells[i]==4 for i in [0,1,2,3,5,6,7,8]) and cells[4]==0:
                out[r+1][c+1]=8
    return out


def solve_M71(grid):
    h,w=dims(grid)
    control=None
    for c,v in enumerate(grid[0]):
        if v in {1,2,3,4}:
            control=v
            break
    if control is None:
        control=1
    anchors=[(r,c) for r,row in enumerate(grid) for c,v in enumerate(row) if v==8]
    if not anchors:
        return blank(h,w)
    ar,ac=anchors[0]
    comps=components(grid, colors={2})
    if not comps:
        return blank(h,w)
    shape=normalize(comps[0]["cells"])
    rot=control-1
    shape=rotate_shape(shape, rot)
    out=blank(h,w)
    for r,c in shape:
        rr,cc=ar+r, ac+c
        if 0<=rr<h and 0<=cc<w:
            out[rr][cc]=3
    return out


def solve_M72(grid):
    out=clone(grid)
    h,w=dims(grid)
    k=None
    for c,v in enumerate(grid[0]):
        if v in {1,2,3}:
            k=v
            break
    if k is None:
        k=1
    seeds=[(r,c) for r,row in enumerate(grid) for c,v in enumerate(row) if v==2]
    if not seeds:
        return out
    sr,sc=seeds[0]
    for r in range(h):
        for c in range(w):
            if grid[r][c] in {0,2} and abs(r-sr)+abs(c-sc)==k:
                out[r][c]=8
    return out


def solve_M73(grid):
    out=clone(grid)
    h,w=dims(grid)
    pos=defaultdict(list)
    for r in range(h):
        for c,v in enumerate(grid[r]):
            if v!=0:
                pos[v].append((r,c))
    for color,cells in pos.items():
        if len(cells)==2:
            (r1,c1),(r2,c2)=cells
            if r1!=r2 and c1!=c2:
                r0,r1s=sorted([r1,r2]); c0,c1s=sorted([c1,c2])
                draw_rect_border(out,r0,c0,r1s,c1s,color)
    return out


def solve_M74(grid):
    out=clone(grid)
    starts=[(r,c) for r,row in enumerate(grid) for c,v in enumerate(row) if v==2]
    goals=[(r,c) for r,row in enumerate(grid) for c,v in enumerate(row) if v==3]
    if not starts or not goals:
        return out
    path=shortest_path_cells(grid, starts[0], goals[0], blocked={5})
    if path:
        for r,c in path[1:-1]:
            if out[r][c]==0:
                out[r][c]=8
    return out


def solve_M75(grid):
    comps=components(grid, colors=None)
    if not comps:
        return [[0]]
    pieces=[]
    for comp in comps:
        cells=comp["cells"]
        r0,c0,r1,c1=bbox(cells)
        h,w=r1-r0+1,c1-c0+1
        piece=blank(h,w)
        for r,c in cells:
            piece[r-r0][c-c0]=grid[r][c]
        pieces.append((len(cells), r0, c0, piece))
    pieces.sort(key=lambda x:(-x[0], x[1], x[2]))
    height=max(len(p[3]) for p in pieces)
    width=sum(len(p[3][0]) for p in pieces)+ (len(pieces)-1)
    out=blank(height,width)
    x=0
    for _,_,_,piece in pieces:
        ph,pw=len(piece),len(piece[0])
        for r in range(ph):
            for c in range(pw):
                if piece[r][c]!=0:
                    out[r][x+c]=piece[r][c]
        x += pw+1
    return out


def solve_M76(grid):
    comps2=components(grid, colors={2})
    comps1=components(grid, colors={1})
    if not comps1 or not comps2:
        return [[0]]
    s1=normalize(comps1[0]["cells"])
    s2=normalize(comps2[0]["cells"])
    res = s1 ^ s2
    return render_shape(res, 8)


def solve_M77(grid):
    out=clone(grid)
    h,w=dims(grid)
    # detect full divider
    divider=None
    for c in range(w):
        if all(grid[r][c]==5 for r in range(h)):
            divider=('v',c); break
    if divider is None:
        for r in range(h):
            if all(grid[r][c]==5 for c in range(w)):
                divider=('h',r); break
    if divider is None:
        return out
    comps=components(grid, colors={2})
    if not comps:
        return out
    cells=comps[0]["cells"]
    orient,val=divider
    reflected=[]
    if orient=='v':
        d=val
        for r,c in cells:
            rc = 2*d - c
            reflected.append((r,rc))
    else:
        d=val
        for r,c in cells:
            rr = 2*d - r
            reflected.append((rr,c))
    for r,c in reflected:
        if 0<=r<h and 0<=c<w and out[r][c]==0:
            out[r][c]=3
    return out


def solve_H71(grid):
    out=clone(grid)
    work=clone(grid)
    points={}
    for r,row in enumerate(grid):
        for c,v in enumerate(row):
            if v in {1,2,3,4}:
                points[v]=(r,c)
    seq=[points[k] for k in sorted(points) if k in points]
    for a,b in pairwise(seq):
        path=shortest_path_cells(work,a,b,blocked={5})
        if path:
            for r,c in path[1:-1]:
                if out[r][c]==0:
                    out[r][c]=8
                if work[r][c]==0:
                    work[r][c]=8
    return out


def solve_H72(grid):
    out=clone(grid)
    k=sum(1 for v in grid[0] if v==2)
    frames=[]
    for comp in components(grid, colors={4}):
        cells=set(comp["cells"])
        r0,c0,r1,c1=bbox(cells)
        if cells == border_cells_of_bbox(r0,c0,r1,c1):
            frames.append((r0,c0,r1,c1))
    frames.sort(key=lambda b: (-(b[2]-b[0]+1)*(b[3]-b[1]+1), b[0], b[1]))
    if not frames or k<1 or k>len(frames):
        return out
    i=k-1
    r0,c0,r1,c1 = frames[i]
    band = interior_cells_of_bbox(r0,c0,r1,c1)
    if i+1 < len(frames):
        ir0,ic0,ir1,ic1 = frames[i+1]
        band -= border_cells_of_bbox(ir0,ic0,ir1,ic1)
        band -= interior_cells_of_bbox(ir0,ic0,ir1,ic1)
    for r,c in band:
        if out[r][c]==0:
            out[r][c]=8
    return out


def solve_H73(grid):
    out=clone(grid)
    k=None
    for c,v in enumerate(grid[0]):
        if v in {1,2,3}:
            k=v
            break
    if k is None:
        k=1
    starts=[(r,c) for r,row in enumerate(grid) for c,v in enumerate(row) if v==2]
    if not starts:
        return out
    dist=multi_source_distance(grid, starts, blocked={5})
    h,w=dims(grid)
    for r in range(h):
        for c in range(w):
            if grid[r][c]==0 and dist[r][c] is not None and dist[r][c] <= k:
                out[r][c]=8
    return out


def solve_H74(grid):
    op_code=None; rot_code=None
    # read first two nonzero controls in top row
    nz=[v for v in grid[0] if v!=0]
    if nz:
        op_code=nz[0]
    if len(nz) > 1:
        rot_code=nz[1]
    if op_code not in {3,4,6,7}:
        op_code=6
    if rot_code not in {1,2,3,4}:
        rot_code=1
    op_map={3:"union",4:"inter",6:"xor",7:"diff"}
    comps2=components(grid, colors={2})
    comps1=components(grid, colors={1})
    if not comps2 or not comps1:
        return [[0]]
    s2=normalize(comps2[0]["cells"])
    s1=normalize(comps1[0]["cells"])
    s1=rotate_shape(s1, rot_code-1)
    res=combine_shapes(s2,s1,op_map[op_code])
    return render_shape(res, 8)


def solve_H75(grid):
    comps=components(grid, colors=None)
    if not comps:
        return [[0]]
    freq=Counter()
    byshape={}
    firstpos={}
    for comp in comps:
        s=frozenset(normalize(comp["cells"]))
        freq[s]+=1
        byshape[s]=set(s)
        firstpos.setdefault(s, bbox(comp["cells"])[:2])
    best=sorted(freq.items(), key=lambda kv:(-kv[1], firstpos[kv[0]][0], firstpos[kv[0]][1]))[0]
    shape,count=best
    return render_shape(scale_shape(set(shape), count), 8)


def solve_H76(grid):
    out=clone(grid)
    for r,c in trace_beam(grid):
        if out[r][c]==0:
            out[r][c]=8
    return out


def solve_H77(grid):
    out=clone(grid)
    starts=[(r,c) for r,row in enumerate(grid) for c,v in enumerate(row) if v==2]
    goals=[(r,c) for r,row in enumerate(grid) for c,v in enumerate(row) if v==3]
    if not starts or not goals:
        return out
    s,g=starts[0], goals[0]
    ds,cs = shortest_path_dists_counts(grid,s,blocked={5})
    dg,cg = shortest_path_dists_counts(grid,g,blocked={5})
    D=ds[g[0]][g[1]]
    if D is None:
        return out
    total=cs[g[0]][g[1]]
    h,w=dims(grid)
    for r in range(h):
        for c in range(w):
            if (r,c) in {s,g}: 
                continue
            if ds[r][c] is not None and dg[r][c] is not None and ds[r][c]+dg[r][c]==D:
                if cs[r][c]*cg[r][c] == total and out[r][c]==0:
                    out[r][c]=8
    return out


SOLVERS = {
    "E71": solve_E71,
    "E72": solve_E72,
    "E73": solve_E73,
    "E74": solve_E74,
    "E75": solve_E75,
    "E76": solve_E76,
    "E77": solve_E77,
    "M71": solve_M71,
    "M72": solve_M72,
    "M73": solve_M73,
    "M74": solve_M74,
    "M75": solve_M75,
    "M76": solve_M76,
    "M77": solve_M77,
    "H71": solve_H71,
    "H72": solve_H72,
    "H73": solve_H73,
    "H74": solve_H74,
    "H75": solve_H75,
    "H76": solve_H76,
    "H77": solve_H77,
}

if __name__ == "__main__":
    import json
    from pathlib import Path
    data = json.loads(Path(__file__).with_name("arc_additional_puzzle_bank_volume11.json").read_text())
    for puzzle in data:
        solver = SOLVERS[puzzle["id"]]
        for pair in puzzle["train"] + puzzle["test"]:
            got = solver(pair["input"])
            assert got == pair["output"], f"validation failed for {puzzle['id']}"
    print(f"validated {len(data)} puzzles")
