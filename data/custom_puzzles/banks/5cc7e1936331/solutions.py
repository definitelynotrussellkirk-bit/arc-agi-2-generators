from __future__ import annotations

from collections import defaultdict, deque
import json

DIR4 = [(-1, 0), (1, 0), (0, -1), (0, 1)]

def blank(h,w,val=0):
    return [[val]*w for _ in range(h)]

def clone(g):
    return [row[:] for row in g]

def size(g):
    return (len(g), len(g[0]) if g else 0)

def in_bounds(g,r,c):
    h,w=size(g)
    return 0<=r<h and 0<=c<w

def strings_from_grid(g):
    return ["".join(str(x) for x in row) for row in g]

def grid_from_strings(rows):
    return [[int(ch) for ch in row.strip()] for row in rows]

def bbox(cells):
    rs=[r for r,c in cells]; cs=[c for r,c in cells]
    return min(rs), min(cs), max(rs), max(cs)

def crop_bbox(g, cells=None):
    if cells is None:
        cells=[(r,c) for r,row in enumerate(g) for c,v in enumerate(row) if v!=0]
    if not cells:
        return [[0]]
    r0,c0,r1,c1=bbox(cells)
    return [row[c0:c1+1] for row in g[r0:r1+1]]

def crop_nonzero(g):
    return crop_bbox(g)

def rotate90(g):
    h,w=size(g)
    return [[g[h-1-r][c] for r in range(h)] for c in range(w)]

def rotate180(g):
    return [list(reversed(row)) for row in reversed(g)]

def rotate270(g):
    h,w=size(g)
    return [[g[r][w-1-c] for r in range(h)] for c in range(w-1,-1,-1)]

def flip_h(g):
    return [list(reversed(row)) for row in g]

def flip_v(g):
    return list(reversed([row[:] for row in g]))

def normalize_cells(cells):
    if not cells:
        return []
    r0,c0,_,_=bbox(cells)
    return sorted((r-r0,c-c0) for r,c in cells)

def normalize_binary_shape(comp_cells):
    return tuple(normalize_cells(comp_cells))

def normalize_grid_binary(g):
    cells=[(r,c) for r,row in enumerate(g) for c,v in enumerate(row) if v!=0]
    return tuple(normalize_cells(cells))

def components_nonzero(g):
    h,w=size(g)
    seen=set()
    comps=[]
    for r in range(h):
        for c in range(w):
            if g[r][c]==0 or (r,c) in seen:
                continue
            color=g[r][c]
            q=[(r,c)]
            seen.add((r,c))
            cells=[]
            while q:
                rr,cc=q.pop()
                cells.append((rr,cc))
                for dr,dc in DIR4:
                    nr,nc=rr+dr,cc+dc
                    if in_bounds(g,nr,nc) and (nr,nc) not in seen and g[nr][nc]==color:
                        seen.add((nr,nc))
                        q.append((nr,nc))
            comps.append({"color":color,"cells":cells})
    return comps

def components_any_nonzero(g):
    """Connected components of all nonzero cells, regardless of color."""
    h,w=size(g)
    seen=set()
    comps=[]
    for r in range(h):
        for c in range(w):
            if g[r][c]==0 or (r,c) in seen:
                continue
            q=[(r,c)]
            seen.add((r,c))
            cells=[]
            while q:
                rr,cc=q.pop()
                cells.append((rr,cc))
                for dr,dc in DIR4:
                    nr,nc=rr+dr,cc+dc
                    if in_bounds(g,nr,nc) and (nr,nc) not in seen and g[nr][nc]!=0:
                        seen.add((nr,nc))
                        q.append((nr,nc))
            comps.append({"cells":cells})
    return comps

def place_shape(g, shape, top, left):
    for r,row in enumerate(shape):
        for c,v in enumerate(row):
            if v!=0 and in_bounds(g, top+r, left+c):
                g[top+r][left+c]=v
    return g

def unique_colors(g, exclude=(0,)):
    s=sorted({v for row in g for v in row if v not in exclude})
    return s

def count_holes_binary(shape):
    # shape: grid with nonzero as filled
    h,w=size(shape)
    # background reachable from border in bbox
    bg_seen=set()
    q=deque()
    for r in range(h):
        for c in range(w):
            if r in (0,h-1) or c in (0,w-1):
                if shape[r][c]==0 and (r,c) not in bg_seen:
                    bg_seen.add((r,c)); q.append((r,c))
    while q:
        r,c=q.popleft()
        for dr,dc in DIR4:
            nr,nc=r+dr,c+dc
            if 0<=nr<h and 0<=nc<w and shape[nr][nc]==0 and (nr,nc) not in bg_seen:
                bg_seen.add((nr,nc)); q.append((nr,nc))
    holes=0
    seen=set(bg_seen)
    for r in range(h):
        for c in range(w):
            if shape[r][c]==0 and (r,c) not in seen:
                holes+=1
                q=deque([(r,c)])
                seen.add((r,c))
                while q:
                    rr,cc=q.popleft()
                    for dr,dc in DIR4:
                        nr,nc=rr+dr,cc+dc
                        if 0<=nr<h and 0<=nc<w and shape[nr][nc]==0 and (nr,nc) not in seen:
                            seen.add((nr,nc)); q.append((nr,nc))
    return holes

def transform_code(g, code):
    # 1=id 2=rot90 3=rot180 4=rot270 5=flip_h 6=flip_v
    if code==1: return clone(g)
    if code==2: return rotate90(g)
    if code==3: return rotate180(g)
    if code==4: return rotate270(g)
    if code==5: return flip_h(g)
    if code==6: return flip_v(g)
    raise ValueError(code)

def apply_named_transform(g, name):
    if name=="id": return clone(g)
    if name=="rot90": return rotate90(g)
    if name=="rot180": return rotate180(g)
    if name=="rot270": return rotate270(g)
    if name=="flip_h": return flip_h(g)
    if name=="flip_v": return flip_v(g)
    raise ValueError(name)

def detect_transform(a,b):
    # both cropped objects with same colors, search among transforms
    candidates=["id","rot90","rot180","rot270","flip_h","flip_v"]
    for name in candidates:
        if apply_named_transform(a,name)==b:
            return name
    raise ValueError("no transform")

def split_panels_horizontal(g, sep_color=5):
    h,w=size(g)
    # assume vertical separator columns all sep_color
    sep_cols=[c for c in range(w) if all(g[r][c]==sep_color for r in range(h))]
    # group panels between separators
    panels=[]
    start=0
    for c in sep_cols + [w]:
        if c>start:
            panels.append([row[start:c] for row in g])
        start=c+1
    return panels

def chamber_components(g, wall_color):
    h,w=size(g)
    seen=set()
    chambers=[]
    for r in range(h):
        for c in range(w):
            if g[r][c]==wall_color or (r,c) in seen:
                continue
            q=deque([(r,c)])
            seen.add((r,c))
            cells=[]
            while q:
                rr,cc=q.popleft()
                cells.append((rr,cc))
                for dr,dc in DIR4:
                    nr,nc=rr+dr,cc+dc
                    if in_bounds(g,nr,nc) and (nr,nc) not in seen and g[nr][nc]!=wall_color:
                        seen.add((nr,nc)); q.append((nr,nc))
            chambers.append(cells)
    return chambers

def resolve_chambers(base_grid, wall_color, reducer, preserve_walls=True):
    """
    reducer(chamber_cells, markers, grid) -> either scalar color or dict {(r,c):color}
    markers is list of (r,c,v) inside chamber with v not 0 and v != wall_color.
    """
    g=clone(base_grid)
    out=blank(*size(g))
    if preserve_walls:
        for r,row in enumerate(g):
            for c,v in enumerate(row):
                if v==wall_color:
                    out[r][c]=wall_color
    for cells in chamber_components(g, wall_color):
        markers=[(r,c,g[r][c]) for r,c in cells if g[r][c] not in (0, wall_color)]
        result=reducer(cells, markers, g)
        if isinstance(result, dict):
            for r,c in cells:
                out[r][c]=result.get((r,c),0)
        else:
            for r,c in cells:
                out[r][c]=result
    return out

def equal_grid_up_to_rotation(g1,g2):
    target=normalize_grid_binary(g2)
    g=g1
    for _ in range(4):
        if normalize_grid_binary(g)==target:
            return True
        g=rotate90(g)
    return False

def rule_e99(g):
    wall=5
    return resolve_chambers(g, wall, lambda cells, markers, grid: markers[0][2] if markers else 0)

def rule_e100(g):
    h,w=size(g)
    out=clone(g)
    for r in range(h):
        for c in range(w):
            if g[r][c]!=0:
                continue
            hits=[]
            if 0<r<h-1 and 0<c<w-1 and g[r-1][c-1]!=0 and g[r-1][c-1]==g[r+1][c+1]:
                hits.append(g[r-1][c-1])
            if 0<r<h-1 and 0<c<w-1 and g[r-1][c+1]!=0 and g[r-1][c+1]==g[r+1][c-1]:
                hits.append(g[r-1][c+1])
            hits=list(dict.fromkeys(hits))
            if len(hits)==1:
                out[r][c]=hits[0]
    return out

def rule_e101(g):
    out=clone(g)
    h,w=size(g)
    for r in range(h):
        positions=defaultdict(list)
        for c,v in enumerate(g[r]):
            if v!=0:
                positions[v].append(c)
        if len(positions)==1:
            color=list(positions.keys())[0]
            cols=positions[color]
            if len(cols)==2:
                for c in range(min(cols), max(cols)+1):
                    out[r][c]=color
    return out

def rule_e102(g):
    out=clone(g)
    by_color=defaultdict(list)
    for r,row in enumerate(g):
        for c,v in enumerate(row):
            if v!=0:
                by_color[v].append((r,c))
    out=blank(*size(g))
    for color,cells in by_color.items():
        if not cells:
            continue
        r0,c0,r1,c1=bbox(cells)
        for c in range(c0,c1+1):
            out[r0][c]=color; out[r1][c]=color
        for r in range(r0,r1+1):
            out[r][c0]=color; out[r][c1]=color
    return out

def rule_e103(g):
    target=g[0][0]
    cells=[(r,c) for r,row in enumerate(g) for c,v in enumerate(row) if v==target and not (r==0 and c==0)]
    return crop_bbox(g, cells)

def rule_e104(g):
    h,w=size(g)
    assert h==w
    out=clone(g)
    for r in range(h):
        for c in range(w):
            if g[r][c]==0 and g[c][r]!=0:
                out[r][c]=g[c][r]
    return out

def rule_e105(g):
    code=g[0][0]
    delta={1:(-1,0),2:(0,1),3:(1,0),4:(0,-1)}[code]
    out=blank(*size(g))
    h,w=size(g)
    dr,dc=delta
    for r,row in enumerate(g):
        for c,v in enumerate(row):
            if (r,c)==(0,0) or v==0:
                continue
            nr,nc=r+dr,c+dc
            if 0<=nr<h and 0<=nc<w:
                out[nr][nc]=v
    return out

def rule_m99(g):
    wall=5
    return resolve_chambers(g, wall, lambda cells, markers, grid: max(v for _,_,v in markers) if markers else 0)

def rule_m100(g):
    code=g[0][0]
    g2=clone(g); g2[0][0]=0
    obj=crop_nonzero(g2)
    return transform_code(obj, code)

def rule_m101(g):
    comps=components_nonzero(g)
    items=[]
    for comp in comps:
        color=comp["color"]
        area=len(comp["cells"])
        items.append(( -area, color, area))
    items.sort()
    row=[]
    for neg_area,color,area in items:
        row.extend([color]*area)
    return [row] if row else [[0]]

def rule_m102(g):
    colors=unique_colors(g)
    assert len(colors)==2
    c1,c2=colors
    cells1=[(r,c) for r,row in enumerate(g) for c,v in enumerate(row) if v==c1]
    cells2=[(r,c) for r,row in enumerate(g) for c,v in enumerate(row) if v==c2]
    n1=normalize_cells(cells1); n2=normalize_cells(cells2)
    maxr=max([r for r,c in n1+n2]+[0]); maxc=max([c for r,c in n1+n2]+[0])
    out=blank(maxr+1, maxc+1)
    for r,c in n1:
        out[r][c]=c1
    for r,c in n2:
        out[r][c]=9 if out[r][c]!=0 else c2
    return out

def rule_m103(g):
    comps=components_any_nonzero(g)
    comps=sorted(comps, key=lambda comp: bbox(comp["cells"])[1])  # left to right
    shapes=[normalize_binary_shape(comp["cells"]) for comp in comps]
    n=len(shapes)
    out=blank(n,n)
    for i in range(n):
        for j in range(n):
            if shapes[i]==shapes[j]:
                out[i][j]=8
    return out

def rule_m104(g):
    rank=g[0][0]
    g2=clone(g); g2[0][0]=0
    comps=components_nonzero(g2)
    comps=sorted(comps, key=lambda comp: (-len(comp["cells"]), bbox(comp["cells"])[1], comp["color"]))
    comp=comps[rank-1]
    return crop_bbox(g2, comp["cells"])

def rule_m105(g):
    # top-left 3x3-ish motif color 1-ish? Actually any nonzero except bottom row commands
    h,w=size(g)
    commands=[v for v in g[h-1] if v!=0]
    base=[row[:] for row in g[:-1]]
    motif=crop_nonzero(base)
    mh,mw=size(motif)
    out=blank(mh, len(commands)*mw + max(0,len(commands)-1))
    cursor=0
    src_colors=[v for row in motif for v in row if v!=0]
    src_color=src_colors[0] if src_colors else 1
    for i,cmd in enumerate(commands):
        recolored=[[cmd if v!=0 else 0 for v in row] for row in motif]
        place_shape(out, recolored, 0, cursor)
        cursor += mw + 1
    return out

def rule_h99(g):
    wall=5
    def reducer(cells, markers, grid):
        colors=sorted({v for _,_,v in markers})
        if len(colors)<2:
            fill=colors[0] if colors else 0
            return {pos: fill for pos in cells}
        a,b=colors[0], colors[-1]
        r0,c0,_,_=bbox(cells)
        d={}
        for r,c in cells:
            d[(r,c)] = a if ((r-r0)+(c-c0))%2==0 else b
        return d
    return resolve_chambers(g, wall, reducer)

def rule_h100(g):
    panels=split_panels_horizontal(g, sep_color=5)
    assert len(panels)==3
    A,B,C=panels
    a=crop_nonzero(A); b=crop_nonzero(B); c=crop_nonzero(C)
    tf=detect_transform(a,b)
    return apply_named_transform(c, tf)

def rule_h101(g):
    commands=[v for v in g[0] if v!=0]
    base=[row[:] for row in g[1:]]
    motif=crop_nonzero(base)
    pieces=[]
    for cmd in commands:
        pieces.append(transform_code(motif, cmd))
    height=max(len(p) for p in pieces)
    width=sum(len(p[0]) for p in pieces)+(len(pieces)-1)
    out=blank(height,width)
    cur=0
    for p in pieces:
        place_shape(out,p,0,cur)
        cur += len(p[0])+1
    return out

def rule_h102(g):
    comps=components_nonzero(g)
    items=[]
    for comp in comps:
        cropped=crop_bbox(g, comp["cells"])
        binary=[[1 if v!=0 else 0 for v in row] for row in cropped]
        holes=count_holes_binary(binary)
        area=len(comp["cells"])
        items.append((holes, -area, comp["color"], cropped))
    items.sort(key=lambda t:(t[0], t[1], t[2]))
    height=max(len(cropped) for _,_,_,cropped in items)
    width=sum(len(cropped[0]) for _,_,_,cropped in items)+(len(items)-1)
    out=blank(height,width)
    cur=0
    for _,_,_,cropped in items:
        place_shape(out,cropped,0,cur)
        cur += len(cropped[0])+1
    return out

def rule_h103(g):
    comps=components_any_nonzero(g)
    comps=sorted(comps, key=lambda comp: bbox(comp["cells"])[1])
    shapes=[]
    for comp in comps:
        cropped=crop_bbox(g, comp["cells"])
        shapes.append([[1 if v!=0 else 0 for v in row] for row in cropped])
    n=len(shapes)
    out=blank(n,n)
    for i in range(n):
        for j in range(n):
            if equal_grid_up_to_rotation(shapes[i], shapes[j]):
                out[i][j]=7
    return out

def rule_h104(g):
    colors=unique_colors(g)
    # expect three colors: object1 color, object2 color, anchor 9 included in objects
    # components_any_nonzero over all nonzero regardless color; should yield 2 objects
    comps=components_any_nonzero(g)
    assert len(comps)==2
    overlays=[]
    colors_per=[]
    for comp in comps:
        cells=comp["cells"]
        # anchor cell color 9 inside component
        anchor=[(r,c) for r,c in cells if g[r][c]==9]
        assert len(anchor)==1
        ar,ac=anchor[0]
        rel=[(r-ar,c-ac,g[r][c]) for r,c in cells]
        overlays.append(rel)
    rs=[r for rel in overlays for r,c,v in rel]
    cs=[c for rel in overlays for r,c,v in rel]
    rshift=-min(rs); cshift=-min(cs)
    maxr=max(rs)+rshift; maxc=max(cs)+cshift
    out=blank(maxr+1,maxc+1)
    for rel in overlays:
        for r,c,v in rel:
            rr,cc=r+rshift,c+cshift
            if out[rr][cc]==0:
                out[rr][cc]=v
            else:
                out[rr][cc]=8
    return out

def rule_h105(g):
    panels=split_panels_horizontal(g, sep_color=5)
    assert len(panels)==3
    A,B,C=panels
    a=crop_nonzero(A); b=crop_nonzero(B); c=crop_nonzero(C)
    # infer transform ignoring colors via binary support
    abinary=[[1 if v!=0 else 0 for v in row] for row in a]
    bbinary=[[1 if v!=0 else 0 for v in row] for row in b]
    tf=detect_transform(abinary, bbinary)
    a_colors=sorted({v for row in a for v in row if v!=0})
    b_colors=sorted({v for row in b for v in row if v!=0})
    # expect one nonzero color each
    src=a_colors[0]; dst=b_colors[0]
    transformed=apply_named_transform(c, tf)
    out=[[dst if v!=0 else 0 for v in row] for row in transformed]
    return out

PUZZLES = json.loads(r'''[
  {
    "id": "E99",
    "title": "Chamber Seed Fill",
    "difficulty": "easy",
    "skills": [
      "chamber partitioning",
      "seed propagation",
      "wall handling"
    ],
    "staged_hint": "Treat the wall color as hard boundaries first. Then solve each chamber independently from its one seed.",
    "written_solution": "The wall cells split the board into chambers. Each chamber contains exactly one colored seed; fill every non-wall cell in that chamber with that seed color.",
    "uses_new_primitive": true,
    "program_name": "rule_e99",
    "train": [
      {
        "input": [
          "5555555555",
          "5200050305",
          "5000050005",
          "5555555555",
          "5000050005",
          "5040050605",
          "5000050005",
          "5555555555"
        ],
        "output": [
          "5555555555",
          "5222253335",
          "5222253335",
          "5555555555",
          "5444456665",
          "5444456665",
          "5444456665",
          "5555555555"
        ]
      },
      {
        "input": [
          "55555555555",
          "52050005065",
          "50050405005",
          "50050005005",
          "55555555555",
          "50050005005",
          "57050805035",
          "50050005005",
          "55555555555"
        ],
        "output": [
          "55555555555",
          "52254445665",
          "52254445665",
          "52254445665",
          "55555555555",
          "57758885335",
          "57758885335",
          "57758885335",
          "55555555555"
        ]
      },
      {
        "input": [
          "5555555555",
          "5200050305",
          "5000050005",
          "5555555555",
          "5040050605",
          "5000050005",
          "5555555555",
          "5000050005",
          "5070050805",
          "5555555555"
        ],
        "output": [
          "5555555555",
          "5222253335",
          "5222253335",
          "5555555555",
          "5444456665",
          "5444456665",
          "5555555555",
          "5777758885",
          "5777758885",
          "5555555555"
        ]
      },
      {
        "input": [
          "5555555555555",
          "5200504005065",
          "5000500005005",
          "5555555555555",
          "5000500005005",
          "5030507005085",
          "5555555555555"
        ],
        "output": [
          "5555555555555",
          "5222544445665",
          "5222544445665",
          "5555555555555",
          "5333577775885",
          "5333577775885",
          "5555555555555"
        ]
      }
    ],
    "test": {
      "input": [
        "5555555555555",
        "5200503050405",
        "5555555555555",
        "5060507050805",
        "5000500050005",
        "5555555555555",
        "5000500050005",
        "5090502050305",
        "5555555555555"
      ],
      "output": [
        "5555555555555",
        "5222533354445",
        "5555555555555",
        "5666577758885",
        "5666577758885",
        "5555555555555",
        "5999522253335",
        "5999522253335",
        "5555555555555"
      ]
    },
    "program_source": "def rule_e99(g):\n    wall=5\n    return resolve_chambers(g, wall, lambda cells, markers, grid: markers[0][2] if markers else 0)"
  },
  {
    "id": "E100",
    "title": "Diagonal Midpoint Completion",
    "difficulty": "easy",
    "skills": [
      "local diagonal rule",
      "midpoint inference",
      "same-size"
    ],
    "staged_hint": "Look only at empty cells. An empty cell changes only when it sits exactly between two equal diagonal neighbors.",
    "written_solution": "Whenever two equal colored cells lie on a diagonal with one empty cell between them, copy that color into the midpoint.",
    "uses_new_primitive": false,
    "program_name": "rule_e100",
    "train": [
      {
        "input": [
          "00000000",
          "04000000",
          "00000020",
          "00040000",
          "00002000",
          "00000000",
          "00000070",
          "00000000"
        ],
        "output": [
          "00000000",
          "04000000",
          "00400020",
          "00040200",
          "00002000",
          "00000000",
          "00000070",
          "00000000"
        ]
      },
      {
        "input": [
          "000000000",
          "000000030",
          "000000000",
          "000503000",
          "000000000",
          "000805000",
          "000000000",
          "080000000",
          "000000000"
        ],
        "output": [
          "000000000",
          "000000030",
          "000000300",
          "000503000",
          "000050000",
          "000805000",
          "008000000",
          "080000000",
          "000000000"
        ]
      },
      {
        "input": [
          "0000000000",
          "0600000040",
          "0000000000",
          "0006204000",
          "0000000000",
          "0000002000",
          "0000000000"
        ],
        "output": [
          "0000000000",
          "0600000040",
          "0060000400",
          "0006204000",
          "0000020000",
          "0000002000",
          "0000000000"
        ]
      },
      {
        "input": [
          "00000000",
          "00000000",
          "00900000",
          "00000000",
          "00009000",
          "00000700",
          "00000200",
          "00070000",
          "00000002",
          "00000000"
        ],
        "output": [
          "00000000",
          "00000000",
          "00900000",
          "00090000",
          "00009000",
          "00000700",
          "00007200",
          "00070020",
          "00000002",
          "00000000"
        ]
      }
    ],
    "test": {
      "input": [
        "0000000000",
        "0040000060",
        "0000000000",
        "0000406000",
        "0000800000",
        "0003000000",
        "0000008000",
        "0300000000",
        "0000000000"
      ],
      "output": [
        "0000000000",
        "0040000060",
        "0004000600",
        "0000406000",
        "0000800000",
        "0003080000",
        "0030008000",
        "0300000000",
        "0000000000"
      ]
    },
    "program_source": "def rule_e100(g):\n    h,w=size(g)\n    out=clone(g)\n    for r in range(h):\n        for c in range(w):\n            if g[r][c]!=0:\n                continue\n            hits=[]\n            if 0<r<h-1 and 0<c<w-1 and g[r-1][c-1]!=0 and g[r-1][c-1]==g[r+1][c+1]:\n                hits.append(g[r-1][c-1])\n            if 0<r<h-1 and 0<c<w-1 and g[r-1][c+1]!=0 and g[r-1][c+1]==g[r+1][c-1]:\n                hits.append(g[r-1][c+1])\n            hits=list(dict.fromkeys(hits))\n            if len(hits)==1:\n                out[r][c]=hits[0]\n    return out"
  },
  {
    "id": "E101",
    "title": "Row Span Paint",
    "difficulty": "easy",
    "skills": [
      "segment completion",
      "row-wise reasoning",
      "same-size"
    ],
    "staged_hint": "Process one row at a time. The two colored endpoints on a row define the whole span.",
    "written_solution": "Each active row contains two endpoints of the same color. Fill every cell between those endpoints, inclusive, with that color.",
    "uses_new_primitive": false,
    "program_name": "rule_e101",
    "train": [
      {
        "input": [
          "0000000000",
          "0200020000",
          "0000000000",
          "0040000400",
          "0000000000",
          "7000000007",
          "0000000000"
        ],
        "output": [
          "0000000000",
          "0222220000",
          "0000000000",
          "0044444400",
          "0000000000",
          "7777777777",
          "0000000000"
        ]
      },
      {
        "input": [
          "003000300",
          "000000000",
          "080080000",
          "000000000",
          "000000000",
          "000000000",
          "000500005",
          "000000000"
        ],
        "output": [
          "003333300",
          "000000000",
          "088880000",
          "000000000",
          "000000000",
          "000000000",
          "000555555",
          "000000000"
        ]
      },
      {
        "input": [
          "00000000000",
          "40000000004",
          "00000000000",
          "00006006000",
          "00200000020",
          "00000000000"
        ],
        "output": [
          "00000000000",
          "44444444444",
          "00000000000",
          "00006666000",
          "00222222220",
          "00000000000"
        ]
      },
      {
        "input": [
          "000000000000",
          "000000000000",
          "000700007000",
          "000000000000",
          "050000000050",
          "000000000000",
          "000000000000",
          "900090000000",
          "000000000000"
        ],
        "output": [
          "000000000000",
          "000000000000",
          "000777777000",
          "000000000000",
          "055555555550",
          "000000000000",
          "000000000000",
          "999990000000",
          "000000000000"
        ]
      }
    ],
    "test": {
      "input": [
        "0000000000",
        "0400000040",
        "0000000000",
        "6000060000",
        "0000000000",
        "0000000000",
        "0030000003",
        "0000000000"
      ],
      "output": [
        "0000000000",
        "0444444440",
        "0000000000",
        "6666660000",
        "0000000000",
        "0000000000",
        "0033333333",
        "0000000000"
      ]
    },
    "program_source": "def rule_e101(g):\n    out=clone(g)\n    h,w=size(g)\n    for r in range(h):\n        positions=defaultdict(list)\n        for c,v in enumerate(g[r]):\n            if v!=0:\n                positions[v].append(c)\n        if len(positions)==1:\n            color=list(positions.keys())[0]\n            cols=positions[color]\n            if len(cols)==2:\n                for c in range(min(cols), max(cols)+1):\n                    out[r][c]=color\n    return out"
  },
  {
    "id": "E102",
    "title": "Rectangle Outline from Corners",
    "difficulty": "easy",
    "skills": [
      "rectangle inference",
      "corner markers",
      "outline drawing"
    ],
    "staged_hint": "Ignore the empty background and treat each color separately. The four colored cells are the corners of one rectangle.",
    "written_solution": "For each color, the input marks the four corners of a rectangle. Draw that rectangle's outline in the same color.",
    "uses_new_primitive": false,
    "program_name": "rule_e102",
    "train": [
      {
        "input": [
          "0000000000",
          "0200020000",
          "0000000440",
          "0000000000",
          "0200020000",
          "0000000000",
          "0000000440",
          "0000000000"
        ],
        "output": [
          "0000000000",
          "0222220000",
          "0200020440",
          "0200020440",
          "0222220440",
          "0000000440",
          "0000000440",
          "0000000000"
        ]
      },
      {
        "input": [
          "000000000",
          "060600000",
          "000000000",
          "000008080",
          "000000000",
          "000000000",
          "000008080",
          "060600000",
          "000000000"
        ],
        "output": [
          "000000000",
          "066600000",
          "060600000",
          "060608880",
          "060608080",
          "060608080",
          "060608880",
          "066600000",
          "000000000"
        ]
      },
      {
        "input": [
          "000000007007",
          "003003000000",
          "000000000000",
          "000000000000",
          "000000007007",
          "003003000000",
          "000000000000"
        ],
        "output": [
          "000000007777",
          "003333007007",
          "003003007007",
          "003003007007",
          "003003007777",
          "003333000000",
          "000000000000"
        ]
      },
      {
        "input": [
          "0000000000",
          "0000009009",
          "0040400000",
          "0000000000",
          "0000000000",
          "0000009009",
          "0000000000",
          "0000000000",
          "0040400000",
          "0000000000"
        ],
        "output": [
          "0000000000",
          "0000009999",
          "0044409009",
          "0040409009",
          "0040409009",
          "0040409999",
          "0040400000",
          "0040400000",
          "0044400000",
          "0000000000"
        ]
      }
    ],
    "test": {
      "input": [
        "00000000000",
        "02020000000",
        "00000500050",
        "00000000000",
        "00000000000",
        "00000000000",
        "02020000000",
        "00000500050"
      ],
      "output": [
        "00000000000",
        "02220000000",
        "02020555550",
        "02020500050",
        "02020500050",
        "02020500050",
        "02220500050",
        "00000555550"
      ]
    },
    "program_source": "def rule_e102(g):\n    out=clone(g)\n    by_color=defaultdict(list)\n    for r,row in enumerate(g):\n        for c,v in enumerate(row):\n            if v!=0:\n                by_color[v].append((r,c))\n    out=blank(*size(g))\n    for color,cells in by_color.items():\n        if not cells:\n            continue\n        r0,c0,r1,c1=bbox(cells)\n        for c in range(c0,c1+1):\n            out[r0][c]=color; out[r1][c]=color\n        for r in range(r0,r1+1):\n            out[r][c0]=color; out[r][c1]=color\n    return out"
  },
  {
    "id": "E103",
    "title": "Legend Color Crop",
    "difficulty": "easy",
    "skills": [
      "selection by code",
      "cropping",
      "object extraction"
    ],
    "staged_hint": "Read the top-left legend cell first. Then ignore every object whose color does not match it.",
    "written_solution": "The top-left cell names the target color. Keep only cells of that color and crop the result to their bounding box.",
    "uses_new_primitive": false,
    "program_name": "rule_e103",
    "train": [
      {
        "input": [
          "4000000000",
          "0000007700",
          "0400007700",
          "0400000000",
          "0444000000",
          "0000022200",
          "0000000000",
          "0000000000"
        ],
        "output": [
          "400",
          "400",
          "444"
        ]
      },
      {
        "input": [
          "600000000",
          "000000880",
          "066600880",
          "006000000",
          "006000000",
          "000003000",
          "000003300",
          "000003330",
          "000000000"
        ],
        "output": [
          "666",
          "060",
          "060"
        ]
      },
      {
        "input": [
          "20000000000",
          "00000005000",
          "00000005000",
          "00220005550",
          "00020000000",
          "00022000000",
          "00000099900",
          "00000000000"
        ],
        "output": [
          "220",
          "020",
          "022"
        ]
      },
      {
        "input": [
          "7000000000",
          "0000003330",
          "0000000300",
          "0000000300",
          "0707000000",
          "0707000000",
          "0777000000",
          "0000000220",
          "0000000220",
          "0000000000"
        ],
        "output": [
          "707",
          "707",
          "777"
        ]
      }
    ],
    "test": {
      "input": [
        "500000000000",
        "000000003300",
        "005000000300",
        "005500000330",
        "005550000000",
        "000000000000",
        "000000077700",
        "000000000000",
        "000000000000"
      ],
      "output": [
        "500",
        "550",
        "555"
      ]
    },
    "program_source": "def rule_e103(g):\n    target=g[0][0]\n    cells=[(r,c) for r,row in enumerate(g) for c,v in enumerate(row) if v==target and not (r==0 and c==0)]\n    return crop_bbox(g, cells)"
  },
  {
    "id": "E104",
    "title": "Main-Diagonal Mirror",
    "difficulty": "easy",
    "skills": [
      "symmetry",
      "reflection",
      "square grids"
    ],
    "staged_hint": "Treat the main diagonal as the mirror line. Every colored cell should appear at the transposed position too.",
    "written_solution": "Copy every colored cell across the main diagonal while keeping the originals. Empty transposed positions become the mirrored color.",
    "uses_new_primitive": false,
    "program_name": "rule_e104",
    "train": [
      {
        "input": [
          "0000700",
          "0002000",
          "0000040",
          "0000003",
          "0000000",
          "0000000",
          "0000000"
        ],
        "output": [
          "0000700",
          "0002000",
          "0000040",
          "0200003",
          "7000000",
          "0040000",
          "0003000"
        ]
      },
      {
        "input": [
          "00000600",
          "00000020",
          "00000008",
          "00000400",
          "00000000",
          "00000000",
          "00000000",
          "00000000"
        ],
        "output": [
          "00000600",
          "00000020",
          "00000008",
          "00000400",
          "00000000",
          "60040000",
          "02000000",
          "00800000"
        ]
      },
      {
        "input": [
          "000900",
          "000050",
          "000002",
          "000000",
          "000000",
          "000000"
        ],
        "output": [
          "000900",
          "000050",
          "000002",
          "900000",
          "050000",
          "002000"
        ]
      },
      {
        "input": [
          "000000002",
          "000000030",
          "000000007",
          "000000400",
          "000000000",
          "000000000",
          "000000000",
          "000000000",
          "000000000"
        ],
        "output": [
          "000000002",
          "000000030",
          "000000007",
          "000000400",
          "000000000",
          "000000000",
          "000400000",
          "030000000",
          "207000000"
        ]
      }
    ],
    "test": {
      "input": [
        "00000004",
        "00000800",
        "00000030",
        "00000006",
        "00000000",
        "00000000",
        "00000000",
        "00000000"
      ],
      "output": [
        "00000004",
        "00000800",
        "00000030",
        "00000006",
        "00000000",
        "08000000",
        "00300000",
        "40060000"
      ]
    },
    "program_source": "def rule_e104(g):\n    h,w=size(g)\n    assert h==w\n    out=clone(g)\n    for r in range(h):\n        for c in range(w):\n            if g[r][c]==0 and g[c][r]!=0:\n                out[r][c]=g[c][r]\n    return out"
  },
  {
    "id": "E105",
    "title": "One-Step Shift by Code",
    "difficulty": "easy",
    "skills": [
      "coded direction",
      "translation",
      "same-size"
    ],
    "staged_hint": "Separate the code cell from the object. The code is only a direction, not part of the moved shape.",
    "written_solution": "The top-left cell encodes a one-cell direction: 1 up, 2 right, 3 down, 4 left. Shift the whole object one step that way and remove the code.",
    "uses_new_primitive": false,
    "program_name": "rule_e105",
    "train": [
      {
        "input": [
          "200000000",
          "000000000",
          "000000000",
          "004000000",
          "004000000",
          "004440000",
          "000000000",
          "000000000"
        ],
        "output": [
          "000000000",
          "000000000",
          "000000000",
          "000400000",
          "000400000",
          "000444000",
          "000000000",
          "000000000"
        ]
      },
      {
        "input": [
          "10000000",
          "00000000",
          "00000000",
          "00000000",
          "00066600",
          "00006000",
          "00006000",
          "00000000",
          "00000000"
        ],
        "output": [
          "00000000",
          "00000000",
          "00000000",
          "00066600",
          "00006000",
          "00006000",
          "00000000",
          "00000000",
          "00000000"
        ]
      },
      {
        "input": [
          "3000000000",
          "0000000000",
          "0000022000",
          "0000002000",
          "0000002200",
          "0000000000",
          "0000000000",
          "0000000000"
        ],
        "output": [
          "0000000000",
          "0000000000",
          "0000000000",
          "0000022000",
          "0000002000",
          "0000002200",
          "0000000000",
          "0000000000"
        ]
      },
      {
        "input": [
          "400000000",
          "000000000",
          "000000000",
          "000000000",
          "000077000",
          "000077000",
          "000000000",
          "000000000",
          "000000000"
        ],
        "output": [
          "000000000",
          "000000000",
          "000000000",
          "000000000",
          "000770000",
          "000770000",
          "000000000",
          "000000000",
          "000000000"
        ]
      }
    ],
    "test": {
      "input": [
        "2000000000",
        "0000000000",
        "0000000000",
        "0050000000",
        "0055000000",
        "0055500000",
        "0000000000",
        "0000000000",
        "0000000000",
        "0000000000"
      ],
      "output": [
        "0000000000",
        "0000000000",
        "0000000000",
        "0005000000",
        "0005500000",
        "0005550000",
        "0000000000",
        "0000000000",
        "0000000000",
        "0000000000"
      ]
    },
    "program_source": "def rule_e105(g):\n    code=g[0][0]\n    delta={1:(-1,0),2:(0,1),3:(1,0),4:(0,-1)}[code]\n    out=blank(*size(g))\n    h,w=size(g)\n    dr,dc=delta\n    for r,row in enumerate(g):\n        for c,v in enumerate(row):\n            if (r,c)==(0,0) or v==0:\n                continue\n            nr,nc=r+dr,c+dc\n            if 0<=nr<h and 0<=nc<w:\n                out[nr][nc]=v\n    return out"
  },
  {
    "id": "M99",
    "title": "Chamber Max Selector",
    "difficulty": "medium",
    "skills": [
      "chamber partitioning",
      "aggregation",
      "wall handling"
    ],
    "staged_hint": "Again solve one chamber at a time. This time the chamber color is not a single seed position but the largest marker value inside it.",
    "written_solution": "The wall cells define chambers. In each chamber, inspect the colored markers already present and repaint the entire chamber with the largest color number found there.",
    "uses_new_primitive": true,
    "program_name": "rule_m99",
    "train": [
      {
        "input": [
          "5555555555",
          "5270050305",
          "5000050045",
          "5555555555",
          "5000050005",
          "5040050105",
          "5006050085",
          "5555555555"
        ],
        "output": [
          "5555555555",
          "5777754445",
          "5777754445",
          "5555555555",
          "5666658885",
          "5666658885",
          "5666658885",
          "5555555555"
        ]
      },
      {
        "input": [
          "55555555555",
          "52050605065",
          "50550405015",
          "50050005005",
          "55555555555",
          "50050005005",
          "57350805035",
          "50050205095",
          "55555555555"
        ],
        "output": [
          "55555555555",
          "52256665665",
          "52556665665",
          "52256665665",
          "55555555555",
          "57758885995",
          "57758885995",
          "57758885995",
          "55555555555"
        ]
      },
      {
        "input": [
          "5555555555",
          "5200050305",
          "5090050405",
          "5555555555",
          "5040050605",
          "5005050015",
          "5555555555",
          "5008050305",
          "5070050205",
          "5555555555"
        ],
        "output": [
          "5555555555",
          "5999954445",
          "5999954445",
          "5555555555",
          "5444456665",
          "5445456665",
          "5555555555",
          "5888853335",
          "5888853335",
          "5555555555"
        ]
      },
      {
        "input": [
          "5555555555555",
          "5230504005065",
          "5000508005705",
          "5555555555555",
          "5000500005405",
          "5930507205085",
          "5555555555555"
        ],
        "output": [
          "5555555555555",
          "5333588885775",
          "5333588885775",
          "5555555555555",
          "5999577775885",
          "5999577775885",
          "5555555555555"
        ]
      }
    ],
    "test": {
      "input": [
        "5555555555555",
        "5240503950455",
        "5555555555555",
        "5060507050805",
        "5010508050205",
        "5555555555555",
        "5000500050005",
        "5093502750365",
        "5555555555555"
      ],
      "output": [
        "5555555555555",
        "5444599954455",
        "5555555555555",
        "5666588858885",
        "5666588858885",
        "5555555555555",
        "5999577756665",
        "5999577756665",
        "5555555555555"
      ]
    },
    "program_source": "def rule_m99(g):\n    wall=5\n    return resolve_chambers(g, wall, lambda cells, markers, grid: max(v for _,_,v in markers) if markers else 0)"
  },
  {
    "id": "M100",
    "title": "Commanded Crop Rotation",
    "difficulty": "medium",
    "skills": [
      "cropping",
      "rotation",
      "coded transform"
    ],
    "staged_hint": "First remove the code cell and crop the object. Only then apply the transform chosen by the code.",
    "written_solution": "Ignore the top-left command cell when finding the object. Crop the object's bounding box, then rotate it according to the code: 1 identity, 2 90\u00b0, 3 180\u00b0, 4 270\u00b0.",
    "uses_new_primitive": false,
    "program_name": "rule_m100",
    "train": [
      {
        "input": [
          "100000000",
          "000000000",
          "000000000",
          "000203000",
          "000233000",
          "000000000",
          "000000000",
          "000000000"
        ],
        "output": [
          "203",
          "233"
        ]
      },
      {
        "input": [
          "2000000000",
          "0000000000",
          "0000000000",
          "0000440000",
          "0000045000",
          "0000005000",
          "0000000000",
          "0000000000",
          "0000000000"
        ],
        "output": [
          "004",
          "044",
          "550"
        ]
      },
      {
        "input": [
          "30000000",
          "00000000",
          "00006000",
          "00006700",
          "00007700",
          "00000000",
          "00000000",
          "00000000"
        ],
        "output": [
          "77",
          "76",
          "06"
        ]
      },
      {
        "input": [
          "4000000000",
          "0000000000",
          "0000000000",
          "0000000000",
          "0000000000",
          "0022000000",
          "0002300000",
          "0000300000",
          "0000000000",
          "0000000000"
        ],
        "output": [
          "200",
          "220",
          "033"
        ]
      }
    ],
    "test": {
      "input": [
        "200000000",
        "000000000",
        "000000000",
        "000000000",
        "000808000",
        "000080000",
        "000000000",
        "000000000",
        "000000000"
      ],
      "output": [
        "08",
        "80",
        "08"
      ]
    },
    "program_source": "def rule_m100(g):\n    code=g[0][0]\n    g2=clone(g); g2[0][0]=0\n    obj=crop_nonzero(g2)\n    return transform_code(obj, code)"
  },
  {
    "id": "M101",
    "title": "Area-Sorted Color Strip",
    "difficulty": "medium",
    "skills": [
      "component analysis",
      "counting",
      "sorting"
    ],
    "staged_hint": "Turn each object into two facts: its color and its area. The output is only a sorted one-dimensional encoding of those facts.",
    "written_solution": "Find each connected colored object, measure its area, sort objects from largest to smallest (breaking ties by color), and output a single row where each object's color is repeated by its area.",
    "uses_new_primitive": false,
    "program_name": "rule_m101",
    "train": [
      {
        "input": [
          "000000000000",
          "020000044000",
          "020000044000",
          "022200000000",
          "000000000900",
          "007770009900",
          "000000009000",
          "000000000000"
        ],
        "output": [
          "2222244449999777"
        ]
      },
      {
        "input": [
          "00000000000",
          "03000000000",
          "03300008880",
          "03330000000",
          "00000000000",
          "06600000000",
          "06600000000",
          "00000000000",
          "00000000000"
        ],
        "output": [
          "3333336666888"
        ]
      },
      {
        "input": [
          "0000000000000",
          "0555000000000",
          "0050000000000",
          "0050000200000",
          "0000000200000",
          "0000000222990",
          "0000000000990",
          "0000000000000"
        ],
        "output": [
          "22222555559999"
        ]
      },
      {
        "input": [
          "000000000000",
          "040400000000",
          "040400000000",
          "044400000000",
          "000000002200",
          "000000002200",
          "077700000000",
          "000000000000",
          "000000000000",
          "000000000000"
        ],
        "output": [
          "44444442222777"
        ]
      }
    ],
    "test": {
      "input": [
        "000000000000",
        "006000003300",
        "066600003300",
        "006000000000",
        "000000000002",
        "000000000022",
        "000008880020",
        "000000000000",
        "000000000000"
      ],
      "output": [
        "6666622223333888"
      ]
    },
    "program_source": "def rule_m101(g):\n    comps=components_nonzero(g)\n    items=[]\n    for comp in comps:\n        color=comp[\"color\"]\n        area=len(comp[\"cells\"])\n        items.append(( -area, color, area))\n    items.sort()\n    row=[]\n    for neg_area,color,area in items:\n        row.extend([color]*area)\n    return [row] if row else [[0]]"
  },
  {
    "id": "M102",
    "title": "Normalized Overlap Overlay",
    "difficulty": "medium",
    "skills": [
      "shape normalization",
      "overlay",
      "set algebra"
    ],
    "staged_hint": "Forget the absolute positions. Crop both colored shapes to their own bounding boxes and align them at the same top-left origin.",
    "written_solution": "Take the two colored shapes, normalize each to its own top-left bounding-box origin, and overlay them on one canvas. Cells belonging to both become 9; otherwise keep the single shape's color.",
    "uses_new_primitive": false,
    "program_name": "rule_m102",
    "train": [
      {
        "input": [
          "000000000000",
          "020000000000",
          "020000033300",
          "022200003000",
          "000000003000",
          "000000000000",
          "000000000000",
          "000000000000"
        ],
        "output": [
          "933",
          "230",
          "292"
        ]
      },
      {
        "input": [
          "00000000000",
          "04000000000",
          "04400000000",
          "04440000000",
          "00000077000",
          "00000077000",
          "00000000000",
          "00000000000",
          "00000000000"
        ],
        "output": [
          "970",
          "990",
          "444"
        ]
      },
      {
        "input": [
          "000000000000",
          "066000000000",
          "006000000000",
          "006600020000",
          "000000020000",
          "000000022200",
          "000000000000",
          "000000000000"
        ],
        "output": [
          "960",
          "260",
          "299"
        ]
      },
      {
        "input": [
          "000000000000",
          "030300000000",
          "030300000000",
          "033300000000",
          "000000000800",
          "000000008880",
          "000000000800",
          "000000000000",
          "000000000000",
          "000000000000"
        ],
        "output": [
          "383",
          "989",
          "393"
        ]
      }
    ],
    "test": {
      "input": [
        "0000000000000",
        "0000000000000",
        "0050000000000",
        "0550000000000",
        "0500000002200",
        "0000000002200",
        "0000000000000",
        "0000000000000",
        "0000000000000"
      ],
      "output": [
        "29",
        "99",
        "50"
      ]
    },
    "program_source": "def rule_m102(g):\n    colors=unique_colors(g)\n    assert len(colors)==2\n    c1,c2=colors\n    cells1=[(r,c) for r,row in enumerate(g) for c,v in enumerate(row) if v==c1]\n    cells2=[(r,c) for r,row in enumerate(g) for c,v in enumerate(row) if v==c2]\n    n1=normalize_cells(cells1); n2=normalize_cells(cells2)\n    maxr=max([r for r,c in n1+n2]+[0]); maxc=max([c for r,c in n1+n2]+[0])\n    out=blank(maxr+1, maxc+1)\n    for r,c in n1:\n        out[r][c]=c1\n    for r,c in n2:\n        out[r][c]=9 if out[r][c]!=0 else c2\n    return out"
  },
  {
    "id": "M103",
    "title": "Shape Equality Matrix",
    "difficulty": "medium",
    "skills": [
      "object normalization",
      "relational output",
      "matrix construction"
    ],
    "staged_hint": "Read the components left to right. The output is not a transformed picture but a comparison table between their normalized shapes.",
    "written_solution": "List the disconnected objects from left to right and compare their shapes after normalizing away position and color. Output an N\u00d7N matrix with 8 wherever two normalized shapes are equal, else 0.",
    "uses_new_primitive": false,
    "program_name": "rule_m103",
    "train": [
      {
        "input": [
          "0000000000000",
          "0200070004440",
          "0200070000400",
          "0222077700400",
          "0000000000000",
          "0000000000000",
          "0000000000000"
        ],
        "output": [
          "880",
          "880",
          "008"
        ]
      },
      {
        "input": [
          "0000000000000000",
          "0000000000000000",
          "0330008880055000",
          "0330000000055000",
          "0000000000000000",
          "0000000000000000",
          "0000000000000000",
          "0000000000000000"
        ],
        "output": [
          "808",
          "080",
          "808"
        ]
      },
      {
        "input": [
          "000000000000000",
          "000000000000000",
          "066000222009900",
          "006000020000900",
          "006600020000990",
          "000000000000000",
          "000000000000000",
          "000000000000000",
          "000000000000000"
        ],
        "output": [
          "808",
          "080",
          "808"
        ]
      },
      {
        "input": [
          "00000000000000",
          "00000000000000",
          "00700040000200",
          "07700040002200",
          "07000044402000",
          "00000000000000",
          "00000000000000",
          "00000000000000"
        ],
        "output": [
          "808",
          "080",
          "808"
        ]
      }
    ],
    "test": {
      "input": [
        "000000000000000000",
        "000000000000000000",
        "030300055000808000",
        "030300055000808000",
        "033300000000888000",
        "000000000000000000",
        "000000000000000000",
        "000000000000000000"
      ],
      "output": [
        "808",
        "080",
        "808"
      ]
    },
    "program_source": "def rule_m103(g):\n    comps=components_any_nonzero(g)\n    comps=sorted(comps, key=lambda comp: bbox(comp[\"cells\"])[1])  # left to right\n    shapes=[normalize_binary_shape(comp[\"cells\"]) for comp in comps]\n    n=len(shapes)\n    out=blank(n,n)\n    for i in range(n):\n        for j in range(n):\n            if shapes[i]==shapes[j]:\n                out[i][j]=8\n    return out"
  },
  {
    "id": "M104",
    "title": "Ranked Object Extraction",
    "difficulty": "medium",
    "skills": [
      "component ranking",
      "selection",
      "cropping"
    ],
    "staged_hint": "Use the code cell only as a rank. After ranking objects by area, you only need one of them.",
    "written_solution": "The top-left cell gives a rank: 1 largest, 2 second largest, 3 third largest. Rank the disconnected objects by area and crop out the object at that rank.",
    "uses_new_primitive": false,
    "program_name": "rule_m104",
    "train": [
      {
        "input": [
          "10000000000000",
          "00000000000000",
          "02000004400000",
          "02000004400000",
          "02220000000000",
          "00000000000000",
          "00000000007770",
          "00000000000000",
          "00000000000000"
        ],
        "output": [
          "200",
          "200",
          "222"
        ]
      },
      {
        "input": [
          "20000000000000",
          "00000000000000",
          "03000000008880",
          "03300000000000",
          "03330000000000",
          "00000000660000",
          "00000000660000",
          "00000000000000",
          "00000000000000"
        ],
        "output": [
          "66",
          "66"
        ]
      },
      {
        "input": [
          "300000000000000",
          "000000000000000",
          "050500020000000",
          "050500020000000",
          "055500022200000",
          "000000000000000",
          "000000000009900",
          "000000000009900",
          "000000000000000",
          "000000000000000"
        ],
        "output": [
          "99",
          "99"
        ]
      },
      {
        "input": [
          "2000000000000000",
          "0000000000000000",
          "0040000077000000",
          "0444000077000000",
          "0040000000000000",
          "0000000000000000",
          "0000000000002220",
          "0000000000000000",
          "0000000000000000",
          "0000000000000000"
        ],
        "output": [
          "77",
          "77"
        ]
      }
    ],
    "test": {
      "input": [
        "100000000000000",
        "000000000000000",
        "006000030000000",
        "066000033000000",
        "060000033300000",
        "000000000000000",
        "000000000008800",
        "000000000008800",
        "000000000000000"
      ],
      "output": [
        "300",
        "330",
        "333"
      ]
    },
    "program_source": "def rule_m104(g):\n    rank=g[0][0]\n    g2=clone(g); g2[0][0]=0\n    comps=components_nonzero(g2)\n    comps=sorted(comps, key=lambda comp: (-len(comp[\"cells\"]), bbox(comp[\"cells\"])[1], comp[\"color\"]))\n    comp=comps[rank-1]\n    return crop_bbox(g2, comp[\"cells\"])"
  },
  {
    "id": "M105",
    "title": "Motif Recolor Broadcast",
    "difficulty": "medium",
    "skills": [
      "motif extraction",
      "recoloring",
      "sequence composition"
    ],
    "staged_hint": "Extract the source motif before looking at the command row. The bottom-row colors tell you how many recolored copies to emit and in what order.",
    "written_solution": "Crop the source motif from the upper part of the grid. For each nonzero color in the bottom row, make one recolored copy of the motif and place the copies side by side with a one-column gap.",
    "uses_new_primitive": false,
    "program_name": "rule_m105",
    "train": [
      {
        "input": [
          "000000000",
          "010100000",
          "011100000",
          "000000000",
          "000000000",
          "246000000"
        ],
        "output": [
          "20204040606",
          "22204440666"
        ]
      },
      {
        "input": [
          "0000000000",
          "0000000000",
          "0011000000",
          "0001100000",
          "0000100000",
          "0000000000",
          "3580000000"
        ],
        "output": [
          "33005500880",
          "03300550088",
          "00300050008"
        ]
      },
      {
        "input": [
          "00000000",
          "00010000",
          "00011000",
          "00011000",
          "00000000",
          "72490000"
        ],
        "output": [
          "70020040090",
          "77022044099",
          "77022044099"
        ]
      },
      {
        "input": [
          "00000000000",
          "00000000000",
          "01010000000",
          "00100000000",
          "00000000000",
          "00000000000",
          "68300000000"
        ],
        "output": [
          "60608080303",
          "06000800030"
        ]
      }
    ],
    "test": {
      "input": [
        "0000000000",
        "0000000000",
        "0011000000",
        "0001100000",
        "0000100000",
        "0000000000",
        "4720000000"
      ],
      "output": [
        "44007700220",
        "04400770022",
        "00400070002"
      ]
    },
    "program_source": "def rule_m105(g):\n    # top-left 3x3-ish motif color 1-ish? Actually any nonzero except bottom row commands\n    h,w=size(g)\n    commands=[v for v in g[h-1] if v!=0]\n    base=[row[:] for row in g[:-1]]\n    motif=crop_nonzero(base)\n    mh,mw=size(motif)\n    out=blank(mh, len(commands)*mw + max(0,len(commands)-1))\n    cursor=0\n    src_colors=[v for row in motif for v in row if v!=0]\n    src_color=src_colors[0] if src_colors else 1\n    for i,cmd in enumerate(commands):\n        recolored=[[cmd if v!=0 else 0 for v in row] for row in motif]\n        place_shape(out, recolored, 0, cursor)\n        cursor += mw + 1\n    return out"
  },
  {
    "id": "H99",
    "title": "Chamber Checker Weave",
    "difficulty": "hard",
    "skills": [
      "chamber partitioning",
      "pattern fill",
      "multi-seed reasoning"
    ],
    "staged_hint": "Partition into chambers first. Inside each chamber, reduce the markers to the smallest and largest colors, then use only those two to paint a local pattern.",
    "written_solution": "The wall cells define chambers. In each chamber, take the smallest and largest marker colors present there and fill the chamber with a checkerboard anchored at that chamber's top-left cell.",
    "uses_new_primitive": true,
    "program_name": "rule_h99",
    "train": [
      {
        "input": [
          "5555555555",
          "5200050305",
          "5070050065",
          "5555555555",
          "5000050005",
          "5040050105",
          "5008050095",
          "5555555555"
        ],
        "output": [
          "5555555555",
          "5272753635",
          "5727256365",
          "5555555555",
          "5484851915",
          "5848459195",
          "5484851915",
          "5555555555"
        ]
      },
      {
        "input": [
          "55555555555",
          "52050405065",
          "50550905085",
          "50050005005",
          "55555555555",
          "50050005005",
          "57050205015",
          "50350805045",
          "55555555555"
        ],
        "output": [
          "55555555555",
          "52254945685",
          "52559495865",
          "52254945685",
          "55555555555",
          "53752825145",
          "57358285415",
          "53752825145",
          "55555555555"
        ]
      },
      {
        "input": [
          "5555555555",
          "5200050305",
          "5090050405",
          "5555555555",
          "5040050605",
          "5007050015",
          "5555555555",
          "5008050505",
          "5070050205",
          "5555555555"
        ],
        "output": [
          "5555555555",
          "5292953435",
          "5929254345",
          "5555555555",
          "5474751615",
          "5747456165",
          "5555555555",
          "5787852525",
          "5878752225",
          "5555555555"
        ]
      },
      {
        "input": [
          "5555555555555",
          "5200504005065",
          "5030508005705",
          "5555555555555",
          "5900500005405",
          "5030507205085",
          "5555555555555"
        ],
        "output": [
          "5555555555555",
          "5232548485675",
          "5323584845765",
          "5555555555555",
          "5393527275485",
          "5939572725845",
          "5555555555555"
        ]
      }
    ],
    "test": {
      "input": [
        "5555555555555",
        "5240503950455",
        "5555555555555",
        "5060507050805",
        "5010508050205",
        "5555555555555",
        "5000500050005",
        "5093502750365",
        "5555555555555"
      ],
      "output": [
        "5555555555555",
        "5242539354455",
        "5555555555555",
        "5161578752825",
        "5616587858285",
        "5555555555555",
        "5393527253635",
        "5939572756365",
        "5555555555555"
      ]
    },
    "program_source": "def rule_h99(g):\n    wall=5\n    def reducer(cells, markers, grid):\n        colors=sorted({v for _,_,v in markers})\n        if len(colors)<2:\n            fill=colors[0] if colors else 0\n            return {pos: fill for pos in cells}\n        a,b=colors[0], colors[-1]\n        r0,c0,_,_=bbox(cells)\n        d={}\n        for r,c in cells:\n            d[(r,c)] = a if ((r-r0)+(c-c0))%2==0 else b\n        return d\n    return resolve_chambers(g, wall, reducer)"
  },
  {
    "id": "H100",
    "title": "Panel Transform Analogy",
    "difficulty": "hard",
    "skills": [
      "analogy",
      "transform inference",
      "panel parsing"
    ],
    "staged_hint": "Split the three panels first. The first two tell you the transform; the third is just the same transform applied again.",
    "written_solution": "The input contains three panels separated by full separator columns. Infer the geometric transform that maps panel A's cropped object to panel B's, then apply that same transform to panel C's cropped object.",
    "uses_new_primitive": false,
    "program_name": "rule_h100",
    "train": [
      {
        "input": [
          "00000500000500000",
          "01000501110501110",
          "01000501000500100",
          "01110501000500100",
          "00000500000500000"
        ],
        "output": [
          "001",
          "111",
          "001"
        ]
      },
      {
        "input": [
          "00000500000500000",
          "01100501100501000",
          "00100500100501100",
          "00110500110501110",
          "00000500000500000"
        ],
        "output": [
          "100",
          "110",
          "111"
        ]
      },
      {
        "input": [
          "00000500000500000",
          "00100501000501000",
          "01100501100501000",
          "01000500100501110",
          "00000500000500000"
        ],
        "output": [
          "001",
          "001",
          "111"
        ]
      },
      {
        "input": [
          "00000500000500000",
          "01110501000501100",
          "00100501110501100",
          "00100501000500000",
          "00000500000500000"
        ],
        "output": [
          "11",
          "11"
        ]
      }
    ],
    "test": {
      "input": [
        "00000500000500000",
        "01000501110501100",
        "01100501100500100",
        "01110501000500110",
        "00000500000500000"
      ],
      "output": [
        "001",
        "111",
        "100"
      ]
    },
    "program_source": "def rule_h100(g):\n    panels=split_panels_horizontal(g, sep_color=5)\n    assert len(panels)==3\n    A,B,C=panels\n    a=crop_nonzero(A); b=crop_nonzero(B); c=crop_nonzero(C)\n    tf=detect_transform(a,b)\n    return apply_named_transform(c, tf)"
  },
  {
    "id": "H101",
    "title": "Sequential Transform Mosaic",
    "difficulty": "hard",
    "skills": [
      "command sequences",
      "transform composition",
      "dynamic output"
    ],
    "staged_hint": "Read the command strip separately from the motif. The output is simply a tiled replay of transformed motif variants in command order.",
    "written_solution": "The top row is a sequence of transform codes and the lower part contains one source motif. Crop the motif and emit transformed copies in command order, separated by one blank column.",
    "uses_new_primitive": false,
    "program_name": "rule_h101",
    "train": [
      {
        "input": [
          "123000",
          "000000",
          "010100",
          "011100",
          "000000",
          "000000"
        ],
        "output": [
          "1010110111",
          "1110100101",
          "0000110000"
        ]
      },
      {
        "input": [
          "4120000",
          "0000000",
          "0011000",
          "0001100",
          "0000100",
          "0000000",
          "0000000"
        ],
        "output": [
          "10001100001",
          "11000110011",
          "01100010110"
        ]
      },
      {
        "input": [
          "2431000",
          "0000000",
          "0000000",
          "0010000",
          "0011000",
          "0011000",
          "0000000"
        ],
        "output": [
          "1110111011010",
          "1100011011011",
          "0000000001011"
        ]
      },
      {
        "input": [
          "32100000",
          "00000000",
          "00000000",
          "00110000",
          "00011000",
          "00001000",
          "00000000",
          "00000000"
        ],
        "output": [
          "10000010110",
          "11000110011",
          "01101100001"
        ]
      }
    ],
    "test": {
      "input": [
        "4213000",
        "0000000",
        "0010100",
        "0001000",
        "0000000",
        "0000000",
        "0000000"
      ],
      "output": [
        "1000101010010",
        "0101000100101",
        "1000100000000"
      ]
    },
    "program_source": "def rule_h101(g):\n    commands=[v for v in g[0] if v!=0]\n    base=[row[:] for row in g[1:]]\n    motif=crop_nonzero(base)\n    pieces=[]\n    for cmd in commands:\n        pieces.append(transform_code(motif, cmd))\n    height=max(len(p) for p in pieces)\n    width=sum(len(p[0]) for p in pieces)+(len(pieces)-1)\n    out=blank(height,width)\n    cur=0\n    for p in pieces:\n        place_shape(out,p,0,cur)\n        cur += len(p[0])+1\n    return out"
  },
  {
    "id": "H102",
    "title": "Hole-Count Packing",
    "difficulty": "hard",
    "skills": [
      "topology",
      "component sorting",
      "packing"
    ],
    "staged_hint": "Do not sort by color or raw size first. Each object's number of holes is the primary key.",
    "written_solution": "Crop each disconnected object, count how many enclosed holes it contains, then pack the cropped objects left to right in increasing hole count order, breaking ties by larger area first.",
    "uses_new_primitive": false,
    "program_name": "rule_h102",
    "train": [
      {
        "input": [
          "0000000000000000",
          "0220004440000000",
          "0220004040000000",
          "0000004440777770",
          "0000000000707070",
          "0000000000777770",
          "0000000000000000",
          "0000000000000000",
          "0000000000000000",
          "0000000000000000"
        ],
        "output": [
          "220444077777",
          "220404070707",
          "000444077777"
        ]
      },
      {
        "input": [
          "000000000000000000",
          "033300000000000000",
          "030300000000000000",
          "033300000008888000",
          "000000000008008000",
          "000000660008008000",
          "000000660008888000",
          "000000000000000000",
          "000000000000000000",
          "000000000000000000",
          "000000000000000000"
        ],
        "output": [
          "66088880333",
          "66080080303",
          "00080080333",
          "00088880000"
        ]
      },
      {
        "input": [
          "000000000000000000",
          "055555000000000000",
          "050505000000000000",
          "055555000000000000",
          "000000000000000000",
          "000000000000000000",
          "000000002220000000",
          "000000002020000000",
          "000000002220009900",
          "000000000000009900",
          "000000000000000000",
          "000000000000000000"
        ],
        "output": [
          "990222055555",
          "990202050505",
          "000222055555"
        ]
      },
      {
        "input": [
          "00000000000000000",
          "04444000000000000",
          "04004000000000000",
          "04004000000000000",
          "04444000000022200",
          "00000000000020200",
          "00000007700022200",
          "00000007700000000",
          "00000000000000000",
          "00000000000000000"
        ],
        "output": [
          "77044440222",
          "77040040202",
          "00040040222",
          "00044440000"
        ]
      }
    ],
    "test": {
      "input": [
        "0000000000000000000",
        "0660000000000000000",
        "0660000000000000000",
        "0000000033333000000",
        "0000000030303000000",
        "0000000033333000000",
        "0000000000000000000",
        "0000000000000008880",
        "0000000000000008080",
        "0000000000000008880",
        "0000000000000000000"
      ],
      "output": [
        "660888033333",
        "660808030303",
        "000888033333"
      ]
    },
    "program_source": "def rule_h102(g):\n    comps=components_nonzero(g)\n    items=[]\n    for comp in comps:\n        cropped=crop_bbox(g, comp[\"cells\"])\n        binary=[[1 if v!=0 else 0 for v in row] for row in cropped]\n        holes=count_holes_binary(binary)\n        area=len(comp[\"cells\"])\n        items.append((holes, -area, comp[\"color\"], cropped))\n    items.sort(key=lambda t:(t[0], t[1], t[2]))\n    height=max(len(cropped) for _,_,_,cropped in items)\n    width=sum(len(cropped[0]) for _,_,_,cropped in items)+(len(items)-1)\n    out=blank(height,width)\n    cur=0\n    for _,_,_,cropped in items:\n        place_shape(out,cropped,0,cur)\n        cur += len(cropped[0])+1\n    return out"
  },
  {
    "id": "H103",
    "title": "Rotation-Equivalence Matrix",
    "difficulty": "hard",
    "skills": [
      "rotation invariance",
      "relational output",
      "shape comparison"
    ],
    "staged_hint": "Normalize position and ignore color, but do not require exact orientation. Two objects match if one can become the other by quarter turns.",
    "written_solution": "List the disconnected objects from left to right. Output an N\u00d7N matrix with 7 when two objects have the same shape up to rotation, and 0 otherwise.",
    "uses_new_primitive": false,
    "program_name": "rule_h103",
    "train": [
      {
        "input": [
          "000000000000000000",
          "000000000000000000",
          "020000077700044400",
          "020000070000004000",
          "022200070000004000",
          "000000000000000000",
          "000000000000000000",
          "000000000000000000",
          "000000000000000000"
        ],
        "output": [
          "770",
          "770",
          "007"
        ]
      },
      {
        "input": [
          "000000000000000000",
          "000000000000000000",
          "033300080000055000",
          "000000080000055000",
          "000000080000000000",
          "000000000000000000",
          "000000000000000000",
          "000000000000000000",
          "000000000000000000"
        ],
        "output": [
          "770",
          "770",
          "007"
        ]
      },
      {
        "input": [
          "00000000000000000000",
          "00000000000000000000",
          "06600000220000009000",
          "00600000020000099000",
          "00660000022000090000",
          "00000000000000000000",
          "00000000000000000000",
          "00000000000000000000",
          "00000000000000000000",
          "00000000000000000000"
        ],
        "output": [
          "770",
          "770",
          "007"
        ]
      },
      {
        "input": [
          "00000000000000000000",
          "00000000000000000000",
          "07000000044400002000",
          "07700000004400002000",
          "07770000000400002220",
          "00000000000000000000",
          "00000000000000000000",
          "00000000000000000000",
          "00000000000000000000",
          "00000000000000000000"
        ],
        "output": [
          "770",
          "770",
          "007"
        ]
      }
    ],
    "test": {
      "input": [
        "000000000000000000",
        "000000000000000000",
        "033300000600000000",
        "003000000600009900",
        "003000006660009900",
        "000000000000000000",
        "000000000000000000",
        "000000000000000000",
        "000000000000000000",
        "000000000000000000"
      ],
      "output": [
        "770",
        "770",
        "007"
      ]
    },
    "program_source": "def rule_h103(g):\n    comps=components_any_nonzero(g)\n    comps=sorted(comps, key=lambda comp: bbox(comp[\"cells\"])[1])\n    shapes=[]\n    for comp in comps:\n        cropped=crop_bbox(g, comp[\"cells\"])\n        shapes.append([[1 if v!=0 else 0 for v in row] for row in cropped])\n    n=len(shapes)\n    out=blank(n,n)\n    for i in range(n):\n        for j in range(n):\n            if equal_grid_up_to_rotation(shapes[i], shapes[j]):\n                out[i][j]=7\n    return out"
  },
  {
    "id": "H104",
    "title": "Anchor-Aligned Overlap",
    "difficulty": "hard",
    "skills": [
      "anchor alignment",
      "overlay",
      "special overlap color"
    ],
    "staged_hint": "Each object has one anchor cell of color 9. Align anchors first; only after that should you think about overlap colors.",
    "written_solution": "Treat each connected object as having a single anchor cell colored 9. Translate both objects so their anchors coincide, then overlay them; cells claimed by both become 8.",
    "uses_new_primitive": false,
    "program_name": "rule_h104",
    "train": [
      {
        "input": [
          "000000000000",
          "090000000000",
          "022000000000",
          "002200000000",
          "000000090000",
          "000000060000",
          "000000066600",
          "000000000000",
          "000000000000"
        ],
        "output": [
          "800",
          "820",
          "688"
        ]
      },
      {
        "input": [
          "0000000000000",
          "0000000000000",
          "0090000000000",
          "0440000000000",
          "0040000000000",
          "0000000009000",
          "0000000007700",
          "0000000007000",
          "0000000000000",
          "0000000000000"
        ],
        "output": [
          "080",
          "487",
          "080"
        ]
      },
      {
        "input": [
          "00000000000000",
          "00900000000000",
          "00300000000000",
          "00333000000000",
          "00000000090000",
          "00000000088000",
          "00000000008800",
          "00000000000000",
          "00000000000000"
        ],
        "output": [
          "800",
          "880",
          "388"
        ]
      },
      {
        "input": [
          "000000000000",
          "000000000000",
          "000900000000",
          "000550000000",
          "000500000000",
          "000000000000",
          "000000009000",
          "000000022000",
          "000000002000",
          "000000000000"
        ],
        "output": [
          "080",
          "285",
          "080"
        ]
      }
    ],
    "test": {
      "input": [
        "00000000000000",
        "00090000000000",
        "00044000000000",
        "00004400000000",
        "00000000000000",
        "00000000009000",
        "00000000007700",
        "00000000007000",
        "00000000000000",
        "00000000000000"
      ],
      "output": [
        "800",
        "880",
        "744"
      ]
    },
    "program_source": "def rule_h104(g):\n    colors=unique_colors(g)\n    # expect three colors: object1 color, object2 color, anchor 9 included in objects\n    # components_any_nonzero over all nonzero regardless color; should yield 2 objects\n    comps=components_any_nonzero(g)\n    assert len(comps)==2\n    overlays=[]\n    colors_per=[]\n    for comp in comps:\n        cells=comp[\"cells\"]\n        # anchor cell color 9 inside component\n        anchor=[(r,c) for r,c in cells if g[r][c]==9]\n        assert len(anchor)==1\n        ar,ac=anchor[0]\n        rel=[(r-ar,c-ac,g[r][c]) for r,c in cells]\n        overlays.append(rel)\n    rs=[r for rel in overlays for r,c,v in rel]\n    cs=[c for rel in overlays for r,c,v in rel]\n    rshift=-min(rs); cshift=-min(cs)\n    maxr=max(rs)+rshift; maxc=max(cs)+cshift\n    out=blank(maxr+1,maxc+1)\n    for rel in overlays:\n        for r,c,v in rel:\n            rr,cc=r+rshift,c+cshift\n            if out[rr][cc]==0:\n                out[rr][cc]=v\n            else:\n                out[rr][cc]=8\n    return out"
  },
  {
    "id": "H105",
    "title": "Color+Transform Analogy",
    "difficulty": "hard",
    "skills": [
      "analogy",
      "transform inference",
      "color remapping"
    ],
    "staged_hint": "The first two panels teach both the geometry change and the color change. Apply both lessons to the third panel.",
    "written_solution": "Split the three panels. Infer the geometric transform from panel A to panel B and also the uniform recolor from A's nonzero color to B's; then apply both to panel C's cropped object.",
    "uses_new_primitive": false,
    "program_name": "rule_h105",
    "train": [
      {
        "input": [
          "00000500000500000",
          "02000507770504440",
          "02000507000500400",
          "02220507000500400",
          "00000500000500000"
        ],
        "output": [
          "007",
          "777",
          "007"
        ]
      },
      {
        "input": [
          "00000500000500000",
          "03300500880506000",
          "00300500800506600",
          "00330508800506660",
          "00000500000500000"
        ],
        "output": [
          "008",
          "088",
          "888"
        ]
      },
      {
        "input": [
          "00000500000500000",
          "04440500200507000",
          "00400500200507000",
          "00400502220507770",
          "00000500000500000"
        ],
        "output": [
          "222",
          "002",
          "002"
        ]
      },
      {
        "input": [
          "00000500000500000",
          "06000503330508800",
          "06600503300500800",
          "06660503000500880",
          "00000500000500000"
        ],
        "output": [
          "003",
          "333",
          "300"
        ]
      }
    ],
    "test": {
      "input": [
        "00000500000500000",
        "00700500440502200",
        "07700504400502200",
        "07000500000500000",
        "00000500000500000"
      ],
      "output": [
        "44",
        "44"
      ]
    },
    "program_source": "def rule_h105(g):\n    panels=split_panels_horizontal(g, sep_color=5)\n    assert len(panels)==3\n    A,B,C=panels\n    a=crop_nonzero(A); b=crop_nonzero(B); c=crop_nonzero(C)\n    # infer transform ignoring colors via binary support\n    abinary=[[1 if v!=0 else 0 for v in row] for row in a]\n    bbinary=[[1 if v!=0 else 0 for v in row] for row in b]\n    tf=detect_transform(abinary, bbinary)\n    a_colors=sorted({v for row in a for v in row if v!=0})\n    b_colors=sorted({v for row in b for v in row if v!=0})\n    # expect one nonzero color each\n    src=a_colors[0]; dst=b_colors[0]\n    transformed=apply_named_transform(c, tf)\n    out=[[dst if v!=0 else 0 for v in row] for row in transformed]\n    return out"
  }
]''')

RULES = {
    "E99": rule_e99,
    "E100": rule_e100,
    "E101": rule_e101,
    "E102": rule_e102,
    "E103": rule_e103,
    "E104": rule_e104,
    "E105": rule_e105,
    "M99": rule_m99,
    "M100": rule_m100,
    "M101": rule_m101,
    "M102": rule_m102,
    "M103": rule_m103,
    "M104": rule_m104,
    "M105": rule_m105,
    "H99": rule_h99,
    "H100": rule_h100,
    "H101": rule_h101,
    "H102": rule_h102,
    "H103": rule_h103,
    "H104": rule_h104,
    "H105": rule_h105
}

def validate():
    n_pairs = 0
    for p in PUZZLES:
        fn = RULES[p["id"]]
        for pair in p["train"]:
            n_pairs += 1
            inp = grid_from_strings(pair["input"])
            want = grid_from_strings(pair["output"])
            got = fn(inp)
            if got != want:
                raise AssertionError(f"Train mismatch for {p['id']}")
        pair = p["test"]
        n_pairs += 1
        inp = grid_from_strings(pair["input"])
        want = grid_from_strings(pair["output"])
        got = fn(inp)
        if got != want:
            raise AssertionError(f"Test mismatch for {p['id']}")
    print(f"Validated {len(PUZZLES)} puzzles / {n_pairs} pairs.")

if __name__ == "__main__":
    validate()
