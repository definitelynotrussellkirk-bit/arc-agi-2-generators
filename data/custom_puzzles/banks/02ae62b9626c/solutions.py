from __future__ import annotations

from collections import defaultdict, deque, Counter
import json

DIR4 = [(-1, 0), (1, 0), (0, -1), (0, 1)]


def blank(h,w,val=0):
    return [[val]*w for _ in range(h)]

def clone(g):
    return [row[:] for row in g]

def size(g):
    return len(g), len(g[0]) if g else 0

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

def transpose(g):
    h,w=size(g)
    return [[g[r][c] for r in range(h)] for c in range(w)]

def normalize_cells(cells):
    if not cells: return []
    r0,c0,_,_=bbox(cells)
    return sorted((r-r0,c-c0) for r,c in cells)

def normalize_binary_shape(comp_cells):
    return tuple(normalize_cells(comp_cells))

def components_by_color(g):
    h,w=size(g)
    seen=set()
    comps=[]
    for r in range(h):
        for c in range(w):
            v=g[r][c]
            if v==0 or (r,c) in seen:
                continue
            q=[(r,c)]
            seen.add((r,c))
            cells=[]
            while q:
                rr,cc=q.pop()
                cells.append((rr,cc))
                for dr,dc in DIR4:
                    nr,nc=rr+dr,cc+dc
                    if in_bounds(g,nr,nc) and (nr,nc) not in seen and g[nr][nc]==v:
                        seen.add((nr,nc))
                        q.append((nr,nc))
            comps.append({"color":v,"cells":cells})
    return comps

def place_shape(g, shape, top, left):
    for r,row in enumerate(shape):
        for c,v in enumerate(row):
            if v!=0 and in_bounds(g, top+r, left+c):
                g[top+r][left+c]=v
    return g

def legend_compose(row_keys, col_keys, resolver):
    return [[resolver(rk, ck) for ck in col_keys] for rk in row_keys]

def apply_transform(g, code):
    # 1=id,2=rot90,3=rot180,4=rot270,5=flip_h,6=flip_v,7=transpose
    if code==1: return clone(g)
    if code==2: return rotate90(g)
    if code==3: return rotate180(g)
    if code==4: return rotate270(g)
    if code==5: return flip_h(g)
    if code==6: return flip_v(g)
    if code==7: return transpose(g)
    raise ValueError(code)

def motif_library(mid):
    if mid==2:
        return grid_from_strings(["200","220","222"])
    if mid==3:
        return grid_from_strings(["300","030","003"])
    if mid==4:
        return grid_from_strings(["040","444","040"])
    raise ValueError(mid)

def transform_code_motif(code, motif):
    # 1=id,2=rot90,3=rot180,4=flip_h
    if code==1: return clone(motif)
    if code==2: return rotate90(motif)
    if code==3: return rotate180(motif)
    if code==4: return flip_h(motif)
    raise ValueError(code)

def split_panels(g, divider=1):
    h,w=size(g)
    div_cols=[c for c in range(w) if all(g[r][c]==divider for r in range(h))]
    starts=[]
    prev=0
    panels=[]
    for dc in div_cols+[w]:
        if dc>prev:
            panel=[row[prev:dc] for row in g]
            panels.append(panel)
        prev=dc+1
    return panels, div_cols

def transform_candidates():
    return {
        "id": lambda x: clone(x),
        "rot90": rotate90,
        "rot180": rotate180,
        "rot270": rotate270,
        "flip_h": flip_h,
        "flip_v": flip_v,
        "transpose": transpose,
    }

def color_mapping_from_pair(a,b):
    map_={}
    h1,w1=size(a); h2,w2=size(b)
    if h1!=h2 or w1!=w2:
        return None
    for r in range(h1):
        for c in range(w1):
            va,vb=a[r][c],b[r][c]
            if va==0 and vb==0: 
                continue
            if va==0 or vb==0:
                return None
            if va in map_ and map_[va]!=vb:
                return None
            map_[va]=vb
    return map_

def apply_color_map(g, cmap):
    h,w=size(g)
    out=blank(h,w)
    for r in range(h):
        for c,v in enumerate(g[r]):
            out[r][c]=cmap.get(v,0) if v!=0 else 0
    return out

def rule_e92(g):
    h,w=size(g)
    row_keys=[g[r][0] for r in range(1,h)]
    col_keys=g[0][1:]
    out=clone(g)
    fill=legend_compose(row_keys, col_keys, lambda a,b: a if a==b else 0)
    for r in range(1,h):
        for c in range(1,w):
            out[r][c]=fill[r-1][c-1]
    return out

def rule_e93(g):
    pts=[(r,c,v) for r,row in enumerate(g) for c,v in enumerate(row) if v!=0]
    if not pts:
        return [[0]]
    color=pts[0][2]
    cells=[(r,c) for r,c,v in pts]
    r0,c0,r1,c1=bbox(cells)
    out=blank(*size(g))
    for r in range(r0,r1+1):
        for c in range(c0,c1+1):
            out[r][c]=color
    return out

def rule_e94(g):
    return crop_nonzero(g)

def rule_e95(g):
    h,w=size(g)
    # guide color 5 occupies a full column
    guide_col=None
    for c in range(w):
        if all(g[r][c]==5 for r in range(h)):
            guide_col=c; break
    out=clone(g)
    if guide_col is None: return out
    for r in range(h):
        for c,v in enumerate(g[r]):
            if v!=0 and c!=guide_col and v!=5:
                mc=2*guide_col-c
                if 0<=mc<w:
                    out[r][mc]=v
    return out

def rule_e96(g):
    vals=[v for row in g for v in row if v!=0]
    color=Counter(vals).most_common(1)[0][0]
    n=len(vals)
    return [[color]*n]

def rule_e97(g):
    h,w=size(g)
    by_color=defaultdict(list)
    for r,row in enumerate(g):
        for c,v in enumerate(row):
            if v!=0:
                by_color[v].append((r,c))
    out=blank(h,w)
    for color, pts in by_color.items():
        if len(pts)!=2:
            for r,c in pts: out[r][c]=color
            continue
        (r1,c1),(r2,c2)=pts
        if r1==r2:
            for c in range(min(c1,c2), max(c1,c2)+1):
                out[r1][c]=color
        elif c1==c2:
            for r in range(min(r1,r2), max(r1,r2)+1):
                out[r][c1]=color
        else:
            out[r1][c1]=out[r2][c2]=color
    return out

def rule_e98(g):
    h,w=size(g)
    assert h==w
    out=clone(g)
    for r in range(h):
        for c in range(w):
            if g[r][c]!=0:
                out[c][r]=g[r][c]
    return out

def rule_m92(g):
    h,w=size(g)
    row_keys=[g[r][0] for r in range(1,h)]
    col_keys=g[0][1:]
    tile_h=2; tile_w=2
    out=blank(len(row_keys)*tile_h, len(col_keys)*tile_w)
    for i,a in enumerate(row_keys):
        for j,b in enumerate(col_keys):
            tile=[[a,b],[b,a]]
            place_shape(out, tile, i*tile_h, j*tile_w)
    return out

def rule_m93(g):
    h,w=size(g)
    out=clone(g)
    # seed cells are colors !=0 and !=8
    seeds=[(r,c,v) for r,row in enumerate(g) for c,v in enumerate(row) if v not in (0,8)]
    # walls color 8, seeds should not spread through each other? treat other nonzero as passable? no, only seed cells.
    # We'll flood zeros plus starting seed but cannot cross walls or another seed color cell.
    for sr,sc,color in seeds:
        q=deque([(sr,sc)])
        seen={(sr,sc)}
        while q:
            r,c=q.popleft()
            out[r][c]=color
            for dr,dc in DIR4:
                nr,nc=r+dr,c+dc
                if not in_bounds(g,nr,nc) or (nr,nc) in seen:
                    continue
                if g[nr][nc]==8:
                    continue
                # avoid crossing into another seed of different color
                if g[nr][nc] not in (0,color):
                    continue
                seen.add((nr,nc))
                q.append((nr,nc))
    return out

def rule_m94(g):
    cmd=g[0][0]
    # object is all nonzero except (0,0)
    gg=clone(g)
    gg[0][0]=0
    obj=crop_nonzero(gg)
    return apply_transform(obj, cmd)

def rule_m95(g):
    comps=components_by_color(g)
    items=[]
    for comp in comps:
        cells=comp["cells"]
        area=len(cells)
        color=comp["color"]
        crop=crop_bbox(g,cells)
        items.append(( -area, color, crop, area))
    items.sort(key=lambda x:(x[0], x[1]))
    crops=[it[2] for it in items]
    heights=[len(c) for c in crops]
    widths=[len(c[0]) for c in crops]
    out=blank(max(heights), sum(widths)+max(0,len(crops)-1))
    c0=0
    for crop in crops:
        place_shape(out, crop, 0, c0)
        c0 += len(crop[0]) + 1
    return out

def rule_m96(g):
    # object colors 2 and 3 possibly multicolor? use exact nonzero color sets 2 and 3
    def cells_of(color):
        return [(r,c) for r,row in enumerate(g) for c,v in enumerate(row) if v==color]
    c2,c3=cells_of(2),cells_of(3)
    crop2=normalize_cells(c2)
    crop3=normalize_cells(c3)
    if not crop2 and not crop3: return [[0]]
    max_r=max([r for r,c in crop2+crop3], default=0)
    max_c=max([c for r,c in crop2+crop3], default=0)
    out=blank(max_r+1, max_c+1)
    s2=set(crop2); s3=set(crop3)
    for r in range(max_r+1):
        for c in range(max_c+1):
            if (r,c) in s2 and (r,c) in s3: out[r][c]=8
            elif (r,c) in s2: out[r][c]=2
            elif (r,c) in s3: out[r][c]=3
    return out

def rule_m97(g):
    h,w=size(g)
    anchor=None; target=None
    for r,row in enumerate(g):
        for c,v in enumerate(row):
            if v==8: anchor=(r,c)
            elif v==9: target=(r,c)
    # object = all nonzero except 8/9
    obj_cells=[(r,c) for r,row in enumerate(g) for c,v in enumerate(row) if v not in (0,8,9)]
    out=blank(h,w)
    if anchor and target:
        dr=target[0]-anchor[0]; dc=target[1]-anchor[1]
        for r,c in obj_cells:
            nr,nc=r+dr,c+dc
            if 0<=nr<h and 0<=nc<w:
                out[nr][nc]=g[r][c]
    return out

def rule_m98(g):
    h,w=size(g)
    # frames: border-colored rectangles; seeds = cells of colors not matching frame border? We'll infer frames by colored rectangle borders.
    out=clone(g)
    # detect all rectangles by scanning nonzero bbox per color? easier since generators will know simple frames maybe same border color.
    # We'll detect candidate rectangles from border colors by bounding boxes of each color components that form rectangles.
    comps=components_by_color(g)
    frames=[]
    for comp in comps:
        color=comp["color"]
        cells=comp["cells"]
        r0,c0,r1,c1=bbox(cells)
        border={(r,c) for r in range(r0,r1+1) for c in range(c0,c1+1) if r in (r0,r1) or c in (c0,c1)}
        if set(cells)==border and r1-r0>=2 and c1-c0>=2:
            frames.append((r0,c0,r1,c1,color))
    for r0,c0,r1,c1,bcolor in frames:
        # seed inside: any nonzero cell strictly inside and not border color
        seed=None
        for r in range(r0+1,r1):
            for c in range(c0+1,c1):
                v=g[r][c]
                if v!=0 and v!=bcolor:
                    seed=v
                    break
            if seed is not None: break
        if seed is not None:
            for r in range(r0+1,r1):
                for c in range(c0+1,c1):
                    out[r][c]=seed
    return out

def rule_h92(g):
    h,w=size(g)
    row_keys=[g[r][0] for r in range(1,h)]
    col_keys=g[0][1:]
    tile_size=3
    out=blank(len(row_keys)*tile_size, len(col_keys)*tile_size)
    for i,code in enumerate(row_keys):
        for j,mid in enumerate(col_keys):
            tile=transform_code_motif(code, motif_library(mid))
            place_shape(out, tile, i*tile_size, j*tile_size)
    return out

def rule_h93(g):
    h,w=size(g)
    seeds=[(r,c,v) for r,row in enumerate(g) for c,v in enumerate(row) if v!=0]
    out=blank(h,w)
    seed_pts=[(r,c) for r,c,v in seeds]
    for r,c,v in seeds:
        out[r][c]=v
    for r in range(h):
        for c in range(w):
            if g[r][c]!=0:
                out[r][c]=g[r][c]
            else:
                dists=[(abs(r-sr)+abs(c-sc), color) for sr,sc,color in seeds]
                if not dists:
                    continue
                dists.sort()
                if len(dists)>=2 and dists[0][0]==dists[1][0]:
                    out[r][c]=0
                else:
                    out[r][c]=dists[0][1]
    return out

def rule_h94(g):
    panels,_=split_panels(g, divider=1)
    a = crop_nonzero([[0 if v==1 else v for v in row] for row in panels[0]])
    b = crop_nonzero([[0 if v==1 else v for v in row] for row in panels[1]])
    q = crop_nonzero([[0 if v==1 else v for v in row] for row in panels[2]])
    for name,fn in transform_candidates().items():
        if fn(a)==b:
            return fn(q)
    return q

def rule_h95(g):
    h,w=size(g)
    out=blank(h,w)
    # frames are nonzero borders, possibly same color 1
    # Determine depth of each nonzero border cell by count of containing rectangles.
    comps=components_by_color(g)
    rects=[]
    for comp in comps:
        cells=comp["cells"]
        r0,c0,r1,c1=bbox(cells)
        border={(r,c) for r in range(r0,r1+1) for c in range(c0,c1+1) if r in (r0,r1) or c in (c0,c1)}
        if set(cells)==border:
            rects.append((r0,c0,r1,c1))
    for r in range(h):
        for c in range(w):
            if g[r][c]==0:
                continue
            depth=sum(1 for r0,c0,r1,c1 in rects if (r in (r0,r1) and c0<=c<=c1) or (c in (c0,c1) and r0<=r<=r1))
            # But cell on multiple overlapping borders only possible corners. need depth by smallest containing frame rank
            containing=[(r0,c0,r1,c1) for r0,c0,r1,c1 in rects if r0<=r<=r1 and c0<=c<=c1]
            depth=len(containing)
            out[r][c]=depth+1
    return out

def rule_h96(g):
    h,w=size(g)
    motif=[row[:3] for row in g[1:4]]
    cmds=[v for v in g[0][3:] if v!=0]
    mapping={1: lambda x: clone(x), 2: rotate90, 3: flip_h, 4: rotate180}
    tiles=[mapping[c](motif) for c in cmds]
    out=blank(3, sum(len(t[0]) for t in tiles))
    c0=0
    for tile in tiles:
        place_shape(out, tile, 0, c0)
        c0 += len(tile[0])
    return out

def rule_h97(g):
    comps=components_by_color(g)
    # order by bbox top-left
    comps.sort(key=lambda comp: bbox(comp["cells"])[:2])
    norms=[normalize_binary_shape(comp["cells"]) for comp in comps]
    n=len(comps)
    out=blank(n,n)
    for i in range(n):
        for j in range(n):
            out[i][j]=8 if norms[i]==norms[j] else 0
    return out

def rule_h98(g):
    panels,_=split_panels(g, divider=1)
    a = crop_nonzero([[0 if v==1 else v for v in row] for row in panels[0]])
    b = crop_nonzero([[0 if v==1 else v for v in row] for row in panels[1]])
    q = crop_nonzero([[0 if v==1 else v for v in row] for row in panels[2]])
    cmap=color_mapping_from_pair(a,b)
    if cmap is None:
        return q
    return apply_color_map(q,cmap)

RULES = {
    'E92': rule_e92,
    'E93': rule_e93,
    'E94': rule_e94,
    'E95': rule_e95,
    'E96': rule_e96,
    'E97': rule_e97,
    'E98': rule_e98,
    'M92': rule_m92,
    'M93': rule_m93,
    'M94': rule_m94,
    'M95': rule_m95,
    'M96': rule_m96,
    'M97': rule_m97,
    'M98': rule_m98,
    'H92': rule_h92,
    'H93': rule_h93,
    'H94': rule_h94,
    'H95': rule_h95,
    'H96': rule_h96,
    'H97': rule_h97,
    'H98': rule_h98
}


PUZZLES = json.loads(r'''[
  {
    "id": "E92",
    "title": "Legend Match Matrix",
    "difficulty": "easy",
    "skills": [
      "row/column headers",
      "legend matching",
      "same-size"
    ],
    "staged_hint": "Read the left-column legend and the top-row legend separately. Then decide each interior cell from just that row-key and column-key pair.",
    "written_solution": "Keep the headers where they are. For each interior position, compare the row's left legend with the column's top legend; write that color only when they match, otherwise write 0.",
    "uses_new_primitive": true,
    "program_name": "rule_e92",
    "train": [
      {
        "input": [
          "04232",
          "20000",
          "30000",
          "40000",
          "20000"
        ],
        "output": [
          "04232",
          "20202",
          "30030",
          "44000",
          "20202"
        ]
      },
      {
        "input": [
          "07565",
          "50000",
          "60000",
          "70000"
        ],
        "output": [
          "07565",
          "50505",
          "60060",
          "77000"
        ]
      },
      {
        "input": [
          "0128",
          "8000",
          "1000",
          "8000",
          "2000"
        ],
        "output": [
          "0128",
          "8008",
          "1100",
          "8008",
          "2020"
        ]
      },
      {
        "input": [
          "065436",
          "300000",
          "400000",
          "500000",
          "600000"
        ],
        "output": [
          "065436",
          "300030",
          "400400",
          "505000",
          "660006"
        ]
      }
    ],
    "test": {
      "input": [
        "01424",
        "40000",
        "20000",
        "40000",
        "10000"
      ],
      "output": [
        "01424",
        "40404",
        "20020",
        "40404",
        "11000"
      ]
    },
    "program_source": "def rule_e92(g):\n    h,w=size(g)\n    row_keys=[g[r][0] for r in range(1,h)]\n    col_keys=g[0][1:]\n    out=clone(g)\n    fill=legend_compose(row_keys, col_keys, lambda a,b: a if a==b else 0)\n    for r in range(1,h):\n        for c in range(1,w):\n            out[r][c]=fill[r-1][c-1]\n    return out"
  },
  {
    "id": "E93",
    "title": "Corner Rectangle Fill",
    "difficulty": "easy",
    "skills": [
      "rectangle inference",
      "corner markers",
      "same-size"
    ],
    "staged_hint": "Ignore the empty background. The four colored cells are just the corners of one axis-aligned rectangle.",
    "written_solution": "The only colored cells are the four corners of a rectangle. Fill the entire rectangle spanned by those corners in the same color.",
    "uses_new_primitive": false,
    "program_name": "rule_e93",
    "train": [
      {
        "input": [
          "00000000",
          "00300030",
          "00000000",
          "00000000",
          "00000000",
          "00300030",
          "00000000",
          "00000000"
        ],
        "output": [
          "00000000",
          "00333330",
          "00333330",
          "00333330",
          "00333330",
          "00333330",
          "00000000",
          "00000000"
        ]
      },
      {
        "input": [
          "700700000",
          "000000000",
          "000000000",
          "000000000",
          "700700000",
          "000000000",
          "000000000"
        ],
        "output": [
          "777700000",
          "777700000",
          "777700000",
          "777700000",
          "777700000",
          "000000000",
          "000000000"
        ]
      },
      {
        "input": [
          "000000000",
          "000000000",
          "000050005",
          "000000000",
          "000000000",
          "000000000",
          "000000000",
          "000050005",
          "000000000"
        ],
        "output": [
          "000000000",
          "000000000",
          "000055555",
          "000055555",
          "000055555",
          "000055555",
          "000055555",
          "000055555",
          "000000000"
        ]
      },
      {
        "input": [
          "0000000000",
          "0000020002",
          "0000000000",
          "0000000000",
          "0000020002",
          "0000000000"
        ],
        "output": [
          "0000000000",
          "0000022222",
          "0000022222",
          "0000022222",
          "0000022222",
          "0000000000"
        ]
      }
    ],
    "test": {
      "input": [
        "0000000000",
        "0000000000",
        "0400000400",
        "0000000000",
        "0000000000",
        "0000000000",
        "0400000400",
        "0000000000"
      ],
      "output": [
        "0000000000",
        "0000000000",
        "0444444400",
        "0444444400",
        "0444444400",
        "0444444400",
        "0444444400",
        "0000000000"
      ]
    },
    "program_source": "def rule_e93(g):\n    pts=[(r,c,v) for r,row in enumerate(g) for c,v in enumerate(row) if v!=0]\n    if not pts:\n        return [[0]]\n    color=pts[0][2]\n    cells=[(r,c) for r,c,v in pts]\n    r0,c0,r1,c1=bbox(cells)\n    out=blank(*size(g))\n    for r in range(r0,r1+1):\n        for c in range(c0,c1+1):\n            out[r][c]=color\n    return out"
  },
  {
    "id": "E94",
    "title": "Tight Crop",
    "difficulty": "easy",
    "skills": [
      "cropping",
      "bounding box",
      "variable-size output"
    ],
    "staged_hint": "You do not need to change any colors or geometry. Just cut away the all-zero margins.",
    "written_solution": "Find the minimal bounding box that contains every nonzero cell and return exactly that cropped subgrid.",
    "uses_new_primitive": false,
    "program_name": "rule_e94",
    "train": [
      {
        "input": [
          "000000000",
          "000000000",
          "000200000",
          "000200000",
          "000222000",
          "000000000",
          "000000000",
          "000000000"
        ],
        "output": [
          "200",
          "200",
          "222"
        ]
      },
      {
        "input": [
          "0000000000",
          "0000007000",
          "0000077700",
          "0000000000",
          "0000000000",
          "0000000000"
        ],
        "output": [
          "070",
          "777"
        ]
      },
      {
        "input": [
          "0000000",
          "0000000",
          "0000000",
          "0000000",
          "0033000",
          "0330000",
          "0000000",
          "0000000",
          "0000000"
        ],
        "output": [
          "033",
          "330"
        ]
      },
      {
        "input": [
          "00000000",
          "00000000",
          "00040000",
          "00444000",
          "00040000",
          "00000000",
          "00000000",
          "00000000"
        ],
        "output": [
          "040",
          "444",
          "040"
        ]
      }
    ],
    "test": {
      "input": [
        "00000000000",
        "00000000000",
        "00000000000",
        "00000550000",
        "00000055000",
        "00000000000",
        "00000000000",
        "00000000000",
        "00000000000"
      ],
      "output": [
        "550",
        "055"
      ]
    },
    "program_source": "def rule_e94(g):\n    return crop_nonzero(g)"
  },
  {
    "id": "E95",
    "title": "Reflect Across Guide",
    "difficulty": "easy",
    "skills": [
      "reflection",
      "guide line",
      "same-size"
    ],
    "staged_hint": "First locate the full vertical guide line. Then mirror every non-guide colored cell across it.",
    "written_solution": "Locate the vertical guide line of 5s. Copy every other colored cell to its mirror position across that line, preserving the original cells and the guide.",
    "uses_new_primitive": false,
    "program_name": "rule_e95",
    "train": [
      {
        "input": [
          "000050000",
          "000050000",
          "022050000",
          "002050000",
          "000050000",
          "000050000",
          "000050000"
        ],
        "output": [
          "000050000",
          "000050000",
          "022050220",
          "002050200",
          "000050000",
          "000050000",
          "000050000"
        ]
      },
      {
        "input": [
          "00000500000",
          "00300500000",
          "03330500000",
          "00030500000",
          "00000500000",
          "00000500000",
          "00000500000",
          "00000500000"
        ],
        "output": [
          "00000500000",
          "00300500300",
          "03330503330",
          "00030503000",
          "00000500000",
          "00000500000",
          "00000500000",
          "00000500000"
        ]
      },
      {
        "input": [
          "0000005000",
          "0000005000",
          "0004405000",
          "0004045000",
          "0000005000",
          "0000005000"
        ],
        "output": [
          "0000005000",
          "0000005000",
          "0004405044",
          "0004045404",
          "0000005000",
          "0000005000"
        ]
      },
      {
        "input": [
          "0000005000000",
          "0000005000000",
          "0000005000000",
          "0000005000000",
          "0077005000000",
          "0007005000000",
          "0000005000000",
          "0000005000000",
          "0000005000000"
        ],
        "output": [
          "0000005000000",
          "0000005000000",
          "0000005000000",
          "0000005000000",
          "0077005007700",
          "0007005007000",
          "0000005000000",
          "0000005000000",
          "0000005000000"
        ]
      }
    ],
    "test": {
      "input": [
        "000000050000",
        "000000050000",
        "006600050000",
        "000600050000",
        "006660050000",
        "000000050000",
        "000000050000",
        "000000050000"
      ],
      "output": [
        "000000050000",
        "000000050000",
        "006600050006",
        "000600050006",
        "006660050066",
        "000000050000",
        "000000050000",
        "000000050000"
      ]
    },
    "program_source": "def rule_e95(g):\n    h,w=size(g)\n    # guide color 5 occupies a full column\n    guide_col=None\n    for c in range(w):\n        if all(g[r][c]==5 for r in range(h)):\n            guide_col=c; break\n    out=clone(g)\n    if guide_col is None: return out\n    for r in range(h):\n        for c,v in enumerate(g[r]):\n            if v!=0 and c!=guide_col and v!=5:\n                mc=2*guide_col-c\n                if 0<=mc<w:\n                    out[r][mc]=v\n    return out"
  },
  {
    "id": "E96",
    "title": "Count-to-Bar",
    "difficulty": "easy",
    "skills": [
      "counting",
      "dynamic-size output",
      "single-color abstraction"
    ],
    "staged_hint": "There is only one object color. Count how many colored cells exist, then output a one-row bar of that many cells.",
    "written_solution": "Count all nonzero cells in the input and output a single horizontal row of that same color with length equal to the count.",
    "uses_new_primitive": false,
    "program_name": "rule_e96",
    "train": [
      {
        "input": [
          "0000000",
          "0600000",
          "0006000",
          "0000000",
          "0000060",
          "0000000"
        ],
        "output": [
          "666"
        ]
      },
      {
        "input": [
          "00000004",
          "00000000",
          "00000000",
          "00400000",
          "00000000",
          "00000400",
          "04000000"
        ],
        "output": [
          "4444"
        ]
      },
      {
        "input": [
          "000800000",
          "080000080",
          "000000000",
          "000080000",
          "800000000"
        ],
        "output": [
          "88888"
        ]
      },
      {
        "input": [
          "00000000",
          "00000000",
          "00300300",
          "00030000",
          "00003000",
          "00300300",
          "00000000",
          "00000000"
        ],
        "output": [
          "333333"
        ]
      }
    ],
    "test": {
      "input": [
        "0000000000",
        "0000000070",
        "0070000000",
        "0000000000",
        "0000070000",
        "0700000070",
        "0000000000"
      ],
      "output": [
        "77777"
      ]
    },
    "program_source": "def rule_e96(g):\n    vals=[v for row in g for v in row if v!=0]\n    color=Counter(vals).most_common(1)[0][0]\n    n=len(vals)\n    return [[color]*n]"
  },
  {
    "id": "E97",
    "title": "Endpoint Segments",
    "difficulty": "easy",
    "skills": [
      "segment completion",
      "endpoint detection",
      "same-size"
    ],
    "staged_hint": "Group cells by color. Each color gives two aligned endpoints, so fill the straight span between them.",
    "written_solution": "Each color appears as two aligned endpoints. Draw the full horizontal or vertical segment joining the endpoints, including both ends.",
    "uses_new_primitive": false,
    "program_name": "rule_e97",
    "train": [
      {
        "input": [
          "00000000",
          "02000200",
          "00000000",
          "00000040",
          "00000000",
          "00000040",
          "00000000"
        ],
        "output": [
          "00000000",
          "02222200",
          "00000000",
          "00000040",
          "00000040",
          "00000040",
          "00000000"
        ]
      },
      {
        "input": [
          "00600000",
          "00000000",
          "00000000",
          "00000000",
          "00600000",
          "00000000",
          "00000303",
          "00000000"
        ],
        "output": [
          "00600000",
          "00600000",
          "00600000",
          "00600000",
          "00600000",
          "00000000",
          "00000333",
          "00000000"
        ]
      },
      {
        "input": [
          "0000000007",
          "0000000000",
          "0500000050",
          "0000000000",
          "0000000007",
          "0000000000"
        ],
        "output": [
          "0000000007",
          "0000000007",
          "0555555557",
          "0000000007",
          "0000000007",
          "0000000000"
        ]
      },
      {
        "input": [
          "000000000",
          "000000080",
          "000000000",
          "000000000",
          "000000000",
          "020002000",
          "000000000",
          "000000080",
          "000000000"
        ],
        "output": [
          "000000000",
          "000000080",
          "000000080",
          "000000080",
          "000000080",
          "022222080",
          "000000080",
          "000000080",
          "000000000"
        ]
      }
    ],
    "test": {
      "input": [
        "6000000000",
        "0000000000",
        "0040000400",
        "0000000000",
        "0000000000",
        "0000030003",
        "6000000000",
        "0000000000"
      ],
      "output": [
        "6000000000",
        "6000000000",
        "6044444400",
        "6000000000",
        "6000000000",
        "6000033333",
        "6000000000",
        "0000000000"
      ]
    },
    "program_source": "def rule_e97(g):\n    h,w=size(g)\n    by_color=defaultdict(list)\n    for r,row in enumerate(g):\n        for c,v in enumerate(row):\n            if v!=0:\n                by_color[v].append((r,c))\n    out=blank(h,w)\n    for color, pts in by_color.items():\n        if len(pts)!=2:\n            for r,c in pts: out[r][c]=color\n            continue\n        (r1,c1),(r2,c2)=pts\n        if r1==r2:\n            for c in range(min(c1,c2), max(c1,c2)+1):\n                out[r1][c]=color\n        elif c1==c2:\n            for r in range(min(r1,r2), max(r1,r2)+1):\n                out[r][c1]=color\n        else:\n            out[r1][c1]=out[r2][c2]=color\n    return out"
  },
  {
    "id": "E98",
    "title": "Main Diagonal Mirror",
    "difficulty": "easy",
    "skills": [
      "matrix symmetry",
      "transpose reflection",
      "same-size"
    ],
    "staged_hint": "Treat the grid as a square matrix. Every colored cell should also appear in the transposed position.",
    "written_solution": "Reflect the pattern across the main diagonal by copying every colored cell at (r,c) to (c,r), taking the union with the original pattern.",
    "uses_new_primitive": false,
    "program_name": "rule_e98",
    "train": [
      {
        "input": [
          "002007",
          "000030",
          "005000",
          "000000",
          "000000",
          "000000"
        ],
        "output": [
          "002007",
          "000030",
          "205000",
          "000000",
          "030000",
          "700000"
        ]
      },
      {
        "input": [
          "0400000",
          "0000008",
          "0000060",
          "0002000",
          "0000000",
          "0000000",
          "0000000"
        ],
        "output": [
          "0400000",
          "4000008",
          "0000060",
          "0002000",
          "0000000",
          "0060000",
          "0800000"
        ]
      },
      {
        "input": [
          "00005",
          "00300",
          "00900",
          "00000",
          "00000"
        ],
        "output": [
          "00005",
          "00300",
          "03900",
          "00000",
          "50000"
        ]
      },
      {
        "input": [
          "00000070",
          "00040000",
          "00000002",
          "00000000",
          "00006000",
          "00000000",
          "00000000",
          "00000000"
        ],
        "output": [
          "00000070",
          "00040000",
          "00000002",
          "04000000",
          "00006000",
          "00000000",
          "70000000",
          "00200000"
        ]
      }
    ],
    "test": {
      "input": [
        "0000080",
        "0000003",
        "0000400",
        "0007000",
        "0000000",
        "0000000",
        "0000000"
      ],
      "output": [
        "0000080",
        "0000003",
        "0000400",
        "0007000",
        "0040000",
        "8000000",
        "0300000"
      ]
    },
    "program_source": "def rule_e98(g):\n    h,w=size(g)\n    assert h==w\n    out=clone(g)\n    for r in range(h):\n        for c in range(w):\n            if g[r][c]!=0:\n                out[c][r]=g[r][c]\n    return out"
  },
  {
    "id": "M92",
    "title": "Legend Weave Tiles",
    "difficulty": "medium",
    "skills": [
      "row/column legends",
      "tile expansion",
      "pairwise composition"
    ],
    "staged_hint": "Read the row headers and column headers first. Each pair expands into the same 2\u00d72 weave tile.",
    "written_solution": "Ignore the blank interior of the header grid. For each row-header / column-header pair, place a 2\u00d72 tile [[row,col],[col,row]] into the output mosaic.",
    "uses_new_primitive": true,
    "program_name": "rule_m92",
    "train": [
      {
        "input": [
          "0352",
          "2000",
          "4000"
        ],
        "output": [
          "232522",
          "325222",
          "434542",
          "345424"
        ]
      },
      {
        "input": [
          "086",
          "600",
          "700",
          "800"
        ],
        "output": [
          "6866",
          "8666",
          "7876",
          "8767",
          "8886",
          "8868"
        ]
      },
      {
        "input": [
          "0753",
          "3000",
          "5000",
          "7000"
        ],
        "output": [
          "373533",
          "735333",
          "575553",
          "755535",
          "777573",
          "775737"
        ]
      },
      {
        "input": [
          "02468",
          "40000",
          "20000"
        ],
        "output": [
          "42444648",
          "24446484",
          "22242628",
          "22426282"
        ]
      }
    ],
    "test": {
      "input": [
        "035",
        "500",
        "100",
        "300"
      ],
      "output": [
        "5355",
        "3555",
        "1315",
        "3151",
        "3335",
        "3353"
      ]
    },
    "program_source": "def rule_m92(g):\n    h,w=size(g)\n    row_keys=[g[r][0] for r in range(1,h)]\n    col_keys=g[0][1:]\n    tile_h=2; tile_w=2\n    out=blank(len(row_keys)*tile_h, len(col_keys)*tile_w)\n    for i,a in enumerate(row_keys):\n        for j,b in enumerate(col_keys):\n            tile=[[a,b],[b,a]]\n            place_shape(out, tile, i*tile_h, j*tile_w)\n    return out"
  },
  {
    "id": "M93",
    "title": "Seeded Chambers",
    "difficulty": "medium",
    "skills": [
      "flood fill",
      "barriers",
      "chamber reasoning"
    ],
    "staged_hint": "Find the wall color, then work chamber by chamber. Only chambers containing a seed get flooded with that seed's color.",
    "written_solution": "Treat color 8 as an impermeable wall. Starting from each seed cell, flood only the reachable interior cells of its chamber with the seed's color, while leaving walls unchanged.",
    "uses_new_primitive": false,
    "program_name": "rule_m93",
    "train": [
      {
        "input": [
          "000000000000",
          "088880088880",
          "082080080080",
          "080080083080",
          "088880080080",
          "000000088880",
          "008888000000",
          "008008000000",
          "008888000000",
          "000000000000"
        ],
        "output": [
          "000000000000",
          "088880088880",
          "082280083380",
          "082280083380",
          "088880083380",
          "000000088880",
          "008888000000",
          "008008000000",
          "008888000000",
          "000000000000"
        ]
      },
      {
        "input": [
          "00000000000",
          "08880888880",
          "08480806080",
          "08880800080",
          "00000888880",
          "00000088880",
          "00000080280",
          "00000088880",
          "00000000000"
        ],
        "output": [
          "00000000000",
          "08880888880",
          "08480866680",
          "08880866680",
          "00000888880",
          "00000088880",
          "00000082280",
          "00000088880",
          "00000000000"
        ]
      },
      {
        "input": [
          "000000000000",
          "088880000000",
          "080080088880",
          "085080080080",
          "080080080080",
          "080080088880",
          "088880000000",
          "000000000000"
        ],
        "output": [
          "000000000000",
          "088880000000",
          "085580088880",
          "085580080080",
          "085580080080",
          "085580088880",
          "088880000000",
          "000000000000"
        ]
      },
      {
        "input": [
          "00000000000",
          "08888088880",
          "08708080080",
          "08008080080",
          "08888088880",
          "00000000000",
          "08888088880",
          "08008083080",
          "08008080080",
          "08888088880",
          "00000000000"
        ],
        "output": [
          "00000000000",
          "08888088880",
          "08778080080",
          "08778080080",
          "08888088880",
          "00000000000",
          "08888088880",
          "08008083380",
          "08008083380",
          "08888088880",
          "00000000000"
        ]
      }
    ],
    "test": {
      "input": [
        "0000000000000",
        "0888880888880",
        "0802080800080",
        "0800080800080",
        "0888880888880",
        "0008888888000",
        "0008400068000",
        "0008000008000",
        "0008888888000",
        "0000000000000"
      ],
      "output": [
        "0000000000000",
        "0888880888880",
        "0822280800080",
        "0822280800080",
        "0888880888880",
        "0008888888000",
        "0008466668000",
        "0008666668000",
        "0008888888000",
        "0000000000000"
      ]
    },
    "program_source": "def rule_m93(g):\n    h,w=size(g)\n    out=clone(g)\n    # seed cells are colors !=0 and !=8\n    seeds=[(r,c,v) for r,row in enumerate(g) for c,v in enumerate(row) if v not in (0,8)]\n    # walls color 8, seeds should not spread through each other? treat other nonzero as passable? no, only seed cells.\n    # We'll flood zeros plus starting seed but cannot cross walls or another seed color cell.\n    for sr,sc,color in seeds:\n        q=deque([(sr,sc)])\n        seen={(sr,sc)}\n        while q:\n            r,c=q.popleft()\n            out[r][c]=color\n            for dr,dc in DIR4:\n                nr,nc=r+dr,c+dc\n                if not in_bounds(g,nr,nc) or (nr,nc) in seen:\n                    continue\n                if g[nr][nc]==8:\n                    continue\n                # avoid crossing into another seed of different color\n                if g[nr][nc] not in (0,color):\n                    continue\n                seen.add((nr,nc))\n                q.append((nr,nc))\n    return out"
  },
  {
    "id": "M94",
    "title": "Commanded Rotation Crop",
    "difficulty": "medium",
    "skills": [
      "object extraction",
      "rotation command",
      "variable-size output"
    ],
    "staged_hint": "Separate the command cell from the object. Crop the object tightly, then apply the commanded rotation.",
    "written_solution": "The top-left cell is a rotation command. Remove it, crop the remaining object to its bounding box, and rotate it by the commanded amount.",
    "uses_new_primitive": false,
    "program_name": "rule_m94",
    "train": [
      {
        "input": [
          "20000000",
          "00000000",
          "00200000",
          "00200000",
          "00222000",
          "00000000",
          "00000000",
          "00000000"
        ],
        "output": [
          "222",
          "200",
          "200"
        ]
      },
      {
        "input": [
          "300000000",
          "000000000",
          "000000000",
          "000055500",
          "000005000",
          "000005000",
          "000000000",
          "000000000"
        ],
        "output": [
          "050",
          "050",
          "555"
        ]
      },
      {
        "input": [
          "40000000",
          "00066000",
          "00006000",
          "00006000",
          "00000000",
          "00000000",
          "00000000"
        ],
        "output": [
          "600",
          "666"
        ]
      },
      {
        "input": [
          "1000000",
          "0000000",
          "0070000",
          "0777000",
          "0000000",
          "0000000"
        ],
        "output": [
          "070",
          "777"
        ]
      }
    ],
    "test": {
      "input": [
        "200000000",
        "000000000",
        "000008800",
        "000008000",
        "000008000",
        "000000000",
        "000000000"
      ],
      "output": [
        "888",
        "008"
      ]
    },
    "program_source": "def rule_m94(g):\n    cmd=g[0][0]\n    # object is all nonzero except (0,0)\n    gg=clone(g)\n    gg[0][0]=0\n    obj=crop_nonzero(gg)\n    return apply_transform(obj, cmd)"
  },
  {
    "id": "M95",
    "title": "Area-Sorted Packing",
    "difficulty": "medium",
    "skills": [
      "connected components",
      "area ranking",
      "packing"
    ],
    "staged_hint": "Extract each disconnected object, measure its area, sort by area descending, then pack the cropped pieces left to right.",
    "written_solution": "Extract each monochrome connected component, crop it to its own bounding box, sort the cropped pieces by descending area, and pack them left to right with one blank column between them.",
    "uses_new_primitive": false,
    "program_name": "rule_m95",
    "train": [
      {
        "input": [
          "000000000000",
          "020000000000",
          "020000000000",
          "022200077700",
          "000000007000",
          "000000007000",
          "044000000000",
          "044000000000",
          "000000000000",
          "000000000000"
        ],
        "output": [
          "2000777044",
          "2000070044",
          "2220070000"
        ]
      },
      {
        "input": [
          "0000000000000",
          "0000000033330",
          "0000000000000",
          "0000000000000",
          "0000000000000",
          "0550000000000",
          "0550000000660",
          "0500000006600",
          "0000000006000"
        ],
        "output": [
          "55006603333",
          "55066000000",
          "50060000000"
        ]
      },
      {
        "input": [
          "00000000000",
          "00600000000",
          "06660000000",
          "00600000000",
          "00000808000",
          "00000888000",
          "00000000000",
          "00000002200",
          "00000002200",
          "00000000000",
          "00000000000"
        ],
        "output": [
          "0600808022",
          "6660888022",
          "0600000000"
        ]
      },
      {
        "input": [
          "00000000000000",
          "00000000000000",
          "00044000000000",
          "00440000000000",
          "00400000000000",
          "00000000000000",
          "00000000070000",
          "00000000070000",
          "05555000077700",
          "00000000000000"
        ],
        "output": [
          "044070005555",
          "440070000000",
          "400077700000"
        ]
      }
    ],
    "test": {
      "input": [
        "0000000000000",
        "0222000000000",
        "0020000000000",
        "0020000040000",
        "0000000040000",
        "0000000044400",
        "0000000000000",
        "0660000000000",
        "0660000000000",
        "0000000000000"
      ],
      "output": [
        "2220400066",
        "0200400066",
        "0200444000"
      ]
    },
    "program_source": "def rule_m95(g):\n    comps=components_by_color(g)\n    items=[]\n    for comp in comps:\n        cells=comp[\"cells\"]\n        area=len(cells)\n        color=comp[\"color\"]\n        crop=crop_bbox(g,cells)\n        items.append(( -area, color, crop, area))\n    items.sort(key=lambda x:(x[0], x[1]))\n    crops=[it[2] for it in items]\n    heights=[len(c) for c in crops]\n    widths=[len(c[0]) for c in crops]\n    out=blank(max(heights), sum(widths)+max(0,len(crops)-1))\n    c0=0\n    for crop in crops:\n        place_shape(out, crop, 0, c0)\n        c0 += len(crop[0]) + 1\n    return out"
  },
  {
    "id": "M96",
    "title": "Normalized Overlap Map",
    "difficulty": "medium",
    "skills": [
      "shape normalization",
      "boolean overlay",
      "cropped output"
    ],
    "staged_hint": "Ignore the original positions. Crop the two shapes separately, align them at the top-left, then compare occupancy cell by cell.",
    "written_solution": "Take the color-2 pattern and the color-3 pattern, crop and normalize them to the same origin, then build a comparison grid: 8 for overlap, 2 for only the first, 3 for only the second.",
    "uses_new_primitive": false,
    "program_name": "rule_m96",
    "train": [
      {
        "input": [
          "00000000000000",
          "02000000000000",
          "02000000000000",
          "02220000000000",
          "00000000000000",
          "00000000330000",
          "00000000330000",
          "00000000300000",
          "00000000000000",
          "00000000000000"
        ],
        "output": [
          "830",
          "830",
          "822"
        ]
      },
      {
        "input": [
          "00000000000000",
          "00000000000000",
          "00222000000000",
          "00020000000000",
          "00020000003000",
          "00000000033300",
          "00000000003000",
          "00000000000000",
          "00000000000000",
          "00000000000000"
        ],
        "output": [
          "282",
          "383",
          "080"
        ]
      },
      {
        "input": [
          "00000000000000",
          "00000000020000",
          "00000000002000",
          "00000000000200",
          "00000000000000",
          "00033000000000",
          "00330000000000",
          "00300000000000",
          "00000000000000",
          "00000000000000"
        ],
        "output": [
          "233",
          "380",
          "302"
        ]
      },
      {
        "input": [
          "00000000000000",
          "00000000030000",
          "00000000030000",
          "00000000033300",
          "02020000000000",
          "02220000000000",
          "00000000000000",
          "00000000000000",
          "00000000000000",
          "00000000000000"
        ],
        "output": [
          "802",
          "822",
          "333"
        ]
      }
    ],
    "test": {
      "input": [
        "00000000000000",
        "00000000000000",
        "00220000000000",
        "00220000000000",
        "00200000000000",
        "00000000003000",
        "00000000033300",
        "00000000003000",
        "00000000000000",
        "00000000000000"
      ],
      "output": [
        "280",
        "883",
        "230"
      ]
    },
    "program_source": "def rule_m96(g):\n    # object colors 2 and 3 possibly multicolor? use exact nonzero color sets 2 and 3\n    def cells_of(color):\n        return [(r,c) for r,row in enumerate(g) for c,v in enumerate(row) if v==color]\n    c2,c3=cells_of(2),cells_of(3)\n    crop2=normalize_cells(c2)\n    crop3=normalize_cells(c3)\n    if not crop2 and not crop3: return [[0]]\n    max_r=max([r for r,c in crop2+crop3], default=0)\n    max_c=max([c for r,c in crop2+crop3], default=0)\n    out=blank(max_r+1, max_c+1)\n    s2=set(crop2); s3=set(crop3)\n    for r in range(max_r+1):\n        for c in range(max_c+1):\n            if (r,c) in s2 and (r,c) in s3: out[r][c]=8\n            elif (r,c) in s2: out[r][c]=2\n            elif (r,c) in s3: out[r][c]=3\n    return out"
  },
  {
    "id": "M97",
    "title": "Anchor Vector Move",
    "difficulty": "medium",
    "skills": [
      "translation vectors",
      "anchor markers",
      "same-size"
    ],
    "staged_hint": "The two special markers define a translation vector. Move every ordinary colored cell by that exact vector.",
    "written_solution": "The cell 8 is the source anchor and the cell 9 is the target anchor. Translate the whole ordinary object by the vector from 8 to 9 and discard the markers.",
    "uses_new_primitive": false,
    "program_name": "rule_m97",
    "train": [
      {
        "input": [
          "0000000000",
          "0800000000",
          "0022000000",
          "0002000000",
          "0022200000",
          "0000009000",
          "0000000000",
          "0000000000",
          "0000000000"
        ],
        "output": [
          "0000000000",
          "0000000000",
          "0000000000",
          "0000000000",
          "0000000000",
          "0000000000",
          "0000000220",
          "0000000020",
          "0000000222"
        ]
      },
      {
        "input": [
          "800000000000",
          "000000330000",
          "000000033000",
          "000000000000",
          "009000000000",
          "000000000000",
          "000000000000",
          "000000000000"
        ],
        "output": [
          "000000000000",
          "000000000000",
          "000000000000",
          "000000000000",
          "000000000000",
          "000000003300",
          "000000000330",
          "000000000000"
        ]
      },
      {
        "input": [
          "0000000000",
          "0000000000",
          "0000090000",
          "0000000000",
          "0000000000",
          "0040000000",
          "0444000000",
          "0040000000",
          "0000000080",
          "0000000000"
        ],
        "output": [
          "4000000000",
          "0000000000",
          "0000000000",
          "0000000000",
          "0000000000",
          "0000000000",
          "0000000000",
          "0000000000",
          "0000000000",
          "0000000000"
        ]
      },
      {
        "input": [
          "00000000000",
          "00000000080",
          "00000000000",
          "00000770000",
          "00000700000",
          "00000700000",
          "00900000000",
          "00000000000",
          "00000000000"
        ],
        "output": [
          "00000000000",
          "00000000000",
          "00000000000",
          "00000000000",
          "00000000000",
          "00000000000",
          "00000000000",
          "00000000000",
          "00000000000"
        ]
      }
    ],
    "test": {
      "input": [
        "000000000080",
        "000000000000",
        "000550000000",
        "000055000000",
        "000000000000",
        "000000900000",
        "000000000000",
        "000000000000",
        "000000000000",
        "000000000000"
      ],
      "output": [
        "000000000000",
        "000000000000",
        "000000000000",
        "000000000000",
        "000000000000",
        "000000000000",
        "000000000000",
        "500000000000",
        "550000000000",
        "000000000000"
      ]
    },
    "program_source": "def rule_m97(g):\n    h,w=size(g)\n    anchor=None; target=None\n    for r,row in enumerate(g):\n        for c,v in enumerate(row):\n            if v==8: anchor=(r,c)\n            elif v==9: target=(r,c)\n    # object = all nonzero except 8/9\n    obj_cells=[(r,c) for r,row in enumerate(g) for c,v in enumerate(row) if v not in (0,8,9)]\n    out=blank(h,w)\n    if anchor and target:\n        dr=target[0]-anchor[0]; dc=target[1]-anchor[1]\n        for r,c in obj_cells:\n            nr,nc=r+dr,c+dc\n            if 0<=nr<h and 0<=nc<w:\n                out[nr][nc]=g[r][c]\n    return out"
  },
  {
    "id": "M98",
    "title": "Seeded Frames Fill",
    "difficulty": "medium",
    "skills": [
      "rectangular frames",
      "containment",
      "conditional fill"
    ],
    "staged_hint": "Detect each rectangular frame first. If a non-border seed lies inside it, flood that frame's interior with the seed color.",
    "written_solution": "Find every rectangular border. If a frame contains a non-border seed inside, fill its interior with the seed color while keeping the border itself intact.",
    "uses_new_primitive": false,
    "program_name": "rule_m98",
    "train": [
      {
        "input": [
          "0000000000000",
          "0222200555550",
          "0270200500050",
          "0200200500050",
          "0222200500050",
          "0000000555550",
          "0000000000000",
          "0000000000000",
          "0000000000000",
          "0000000000000"
        ],
        "output": [
          "0000000000000",
          "0222200555550",
          "0277200500050",
          "0277200500050",
          "0222200500050",
          "0000000555550",
          "0000000000000",
          "0000000000000",
          "0000000000000",
          "0000000000000"
        ]
      },
      {
        "input": [
          "000000000000",
          "033333000000",
          "030003000000",
          "030803000000",
          "030003000000",
          "033333000000",
          "006666666000",
          "006040006000",
          "006000006000",
          "006666666000",
          "000000000000"
        ],
        "output": [
          "000000000000",
          "033333000000",
          "038883000000",
          "038883000000",
          "038883000000",
          "033333000000",
          "006666666000",
          "006444446000",
          "006444446000",
          "006666666000",
          "000000000000"
        ]
      },
      {
        "input": [
          "00000000000000",
          "04444440000000",
          "04000040077770",
          "04000040072070",
          "04444440070070",
          "00000000070070",
          "00000000070070",
          "00000000077770",
          "00000000000000"
        ],
        "output": [
          "00000000000000",
          "04444440000000",
          "04000040077770",
          "04000040072270",
          "04444440072270",
          "00000000072270",
          "00000000072270",
          "00000000077770",
          "00000000000000"
        ]
      },
      {
        "input": [
          "00000000000000",
          "05555500000000",
          "05090500666600",
          "05000500600600",
          "05555500666600",
          "00000000222220",
          "00000000204020",
          "00000000200020",
          "00000000222220",
          "00000000000000"
        ],
        "output": [
          "00000000000000",
          "05555500000000",
          "05999500666600",
          "05999500600600",
          "05555500666600",
          "00000000222220",
          "00000000244420",
          "00000000244420",
          "00000000222220",
          "00000000000000"
        ]
      }
    ],
    "test": {
      "input": [
        "00000000000000",
        "02222200666660",
        "02070200600060",
        "02000200600060",
        "02000200666660",
        "02222200000000",
        "00044444444000",
        "00040800004000",
        "00040000004000",
        "00044444444000",
        "00000000000000"
      ],
      "output": [
        "00000000000000",
        "02222200666660",
        "02777200600060",
        "02777200600060",
        "02777200666660",
        "02222200000000",
        "00044444444000",
        "00048888884000",
        "00048888884000",
        "00044444444000",
        "00000000000000"
      ]
    },
    "program_source": "def rule_m98(g):\n    h,w=size(g)\n    # frames: border-colored rectangles; seeds = cells of colors not matching frame border? We'll infer frames by colored rectangle borders.\n    out=clone(g)\n    # detect all rectangles by scanning nonzero bbox per color? easier since generators will know simple frames maybe same border color.\n    # We'll detect candidate rectangles from border colors by bounding boxes of each color components that form rectangles.\n    comps=components_by_color(g)\n    frames=[]\n    for comp in comps:\n        color=comp[\"color\"]\n        cells=comp[\"cells\"]\n        r0,c0,r1,c1=bbox(cells)\n        border={(r,c) for r in range(r0,r1+1) for c in range(c0,c1+1) if r in (r0,r1) or c in (c0,c1)}\n        if set(cells)==border and r1-r0>=2 and c1-c0>=2:\n            frames.append((r0,c0,r1,c1,color))\n    for r0,c0,r1,c1,bcolor in frames:\n        # seed inside: any nonzero cell strictly inside and not border color\n        seed=None\n        for r in range(r0+1,r1):\n            for c in range(c0+1,c1):\n                v=g[r][c]\n                if v!=0 and v!=bcolor:\n                    seed=v\n                    break\n            if seed is not None: break\n        if seed is not None:\n            for r in range(r0+1,r1):\n                for c in range(c0+1,c1):\n                    out[r][c]=seed\n    return out"
  },
  {
    "id": "H92",
    "title": "Legend Motif Composer",
    "difficulty": "hard",
    "skills": [
      "legend composition",
      "motif library",
      "transform selection"
    ],
    "staged_hint": "The headers do not describe single cells anymore; they choose full motif tiles. One header chooses the transform and the other chooses the motif.",
    "written_solution": "The left legend chooses a transform and the top legend chooses one motif from a small library. Compose those choices for every row/column pair and tile the transformed 3\u00d73 motifs into the output.",
    "uses_new_primitive": true,
    "program_name": "rule_h92",
    "train": [
      {
        "input": [
          "0234",
          "1000",
          "2000"
        ],
        "output": [
          "200300040",
          "220030444",
          "222003040",
          "222003040",
          "220030444",
          "200300040"
        ]
      },
      {
        "input": [
          "042",
          "400",
          "300",
          "100"
        ],
        "output": [
          "040002",
          "444022",
          "040222",
          "040222",
          "444022",
          "040002",
          "040200",
          "444220",
          "040222"
        ]
      },
      {
        "input": [
          "0342",
          "2000",
          "1000",
          "4000"
        ],
        "output": [
          "003040222",
          "030444220",
          "300040200",
          "300040200",
          "030444220",
          "003040222",
          "003040002",
          "030444022",
          "300040222"
        ]
      },
      {
        "input": [
          "02432",
          "30000",
          "20000"
        ],
        "output": [
          "222040300222",
          "022444030022",
          "002040003002",
          "222040003222",
          "220444030220",
          "200040300200"
        ]
      }
    ],
    "test": {
      "input": [
        "043",
        "100",
        "400",
        "200"
      ],
      "output": [
        "040300",
        "444030",
        "040003",
        "040003",
        "444030",
        "040300",
        "040003",
        "444030",
        "040300"
      ]
    },
    "program_source": "def rule_h92(g):\n    h,w=size(g)\n    row_keys=[g[r][0] for r in range(1,h)]\n    col_keys=g[0][1:]\n    tile_size=3\n    out=blank(len(row_keys)*tile_size, len(col_keys)*tile_size)\n    for i,code in enumerate(row_keys):\n        for j,mid in enumerate(col_keys):\n            tile=transform_code_motif(code, motif_library(mid))\n            place_shape(out, tile, i*tile_size, j*tile_size)\n    return out"
  },
  {
    "id": "H93",
    "title": "Nearest-Seed Partition",
    "difficulty": "hard",
    "skills": [
      "nearest seed",
      "Manhattan geometry",
      "tie handling"
    ],
    "staged_hint": "Every blank cell belongs to the closest seed in Manhattan distance. If two seeds tie, the cell stays blank.",
    "written_solution": "Each blank location is colored by the unique nearest seed under Manhattan distance. When two or more seeds are equally near, the cell remains 0.",
    "uses_new_primitive": false,
    "program_name": "rule_h93",
    "train": [
      {
        "input": [
          "0000000",
          "0200030",
          "0000000",
          "0000000",
          "0000000",
          "0004000",
          "0000000"
        ],
        "output": [
          "2220333",
          "2220333",
          "2220333",
          "2204033",
          "0044400",
          "4444444",
          "4444444"
        ]
      },
      {
        "input": [
          "00000000",
          "00000050",
          "00000000",
          "00000000",
          "00700000",
          "00000000",
          "00000020",
          "00000000"
        ],
        "output": [
          "77755555",
          "77755555",
          "77775555",
          "77777555",
          "77777022",
          "77770222",
          "77702222",
          "77702222"
        ]
      },
      {
        "input": [
          "000000000",
          "060000030",
          "000000000",
          "000000000",
          "000080000",
          "000000000"
        ],
        "output": [
          "666603333",
          "666603333",
          "666080333",
          "660888033",
          "008888800",
          "008888800"
        ]
      },
      {
        "input": [
          "0000000",
          "0000000",
          "0400020",
          "0000000",
          "0000000",
          "0000000",
          "0000000",
          "0006000",
          "0000000"
        ],
        "output": [
          "4440222",
          "4440222",
          "4440222",
          "4440222",
          "4446222",
          "4466622",
          "6666666",
          "6666666",
          "6666666"
        ]
      }
    ],
    "test": {
      "input": [
        "000000000",
        "003000050",
        "000000000",
        "000000000",
        "000000000",
        "000000000",
        "000080000",
        "000000000"
      ],
      "output": [
        "333335555",
        "333335555",
        "333335555",
        "333380555",
        "333888055",
        "888888800",
        "888888888",
        "888888888"
      ]
    },
    "program_source": "def rule_h93(g):\n    h,w=size(g)\n    seeds=[(r,c,v) for r,row in enumerate(g) for c,v in enumerate(row) if v!=0]\n    out=blank(h,w)\n    seed_pts=[(r,c) for r,c,v in seeds]\n    for r,c,v in seeds:\n        out[r][c]=v\n    for r in range(h):\n        for c in range(w):\n            if g[r][c]!=0:\n                out[r][c]=g[r][c]\n            else:\n                dists=[(abs(r-sr)+abs(c-sc), color) for sr,sc,color in seeds]\n                if not dists:\n                    continue\n                dists.sort()\n                if len(dists)>=2 and dists[0][0]==dists[1][0]:\n                    out[r][c]=0\n                else:\n                    out[r][c]=dists[0][1]\n    return out"
  },
  {
    "id": "H94",
    "title": "Transform Analogy Transfer",
    "difficulty": "hard",
    "skills": [
      "analogy",
      "geometric transform transfer",
      "panel reasoning"
    ],
    "staged_hint": "Use the first two panels only to infer a transform. Then apply the same transform to the query object in the third panel.",
    "written_solution": "Split the input into three panels. Determine which geometric transform maps the first panel's cropped object to the second panel's cropped object, then apply that same transform to the third panel's object.",
    "uses_new_primitive": false,
    "program_name": "rule_h94",
    "train": [
      {
        "input": [
          "00000100000100000",
          "02000102220103330",
          "02000102000100300",
          "02220102000100300",
          "00000100000100000"
        ],
        "output": [
          "003",
          "333",
          "003"
        ]
      },
      {
        "input": [
          "00000100000100000",
          "00440104400105000",
          "04400100440100500",
          "04000100040100050",
          "00000100000100000"
        ],
        "output": [
          "005",
          "050",
          "500"
        ]
      },
      {
        "input": [
          "00000100000100000",
          "06060100000107700",
          "06660106660107700",
          "00000106060107000",
          "00000100000100000"
        ],
        "output": [
          "07",
          "77",
          "77"
        ]
      },
      {
        "input": [
          "00000010000001000000",
          "08888010800001020000",
          "00000010800001020000",
          "00000010800001022200",
          "00000010800001000000"
        ],
        "output": [
          "222",
          "200",
          "200"
        ]
      }
    ],
    "test": {
      "input": [
        "00000100000100000",
        "05000105550102220",
        "05000100050100200",
        "05550100050100200",
        "00000100000100000"
      ],
      "output": [
        "020",
        "020",
        "222"
      ]
    },
    "program_source": "def rule_h94(g):\n    panels,_=split_panels(g, divider=1)\n    a = crop_nonzero([[0 if v==1 else v for v in row] for row in panels[0]])\n    b = crop_nonzero([[0 if v==1 else v for v in row] for row in panels[1]])\n    q = crop_nonzero([[0 if v==1 else v for v in row] for row in panels[2]])\n    for name,fn in transform_candidates().items():\n        if fn(a)==b:\n            return fn(q)\n    return q"
  },
  {
    "id": "H95",
    "title": "Nested Depth Borders",
    "difficulty": "hard",
    "skills": [
      "nesting depth",
      "frame detection",
      "recolor by depth"
    ],
    "staged_hint": "List the nested rectangular borders from outside to inside. A border's output color depends only on how deeply nested it is.",
    "written_solution": "Detect all nested rectangular borders. Recolor each border by its nesting depth: outermost becomes 2, next becomes 3, and so on inward.",
    "uses_new_primitive": false,
    "program_name": "rule_h95",
    "train": [
      {
        "input": [
          "111111111",
          "100000001",
          "101111101",
          "101000101",
          "101010101",
          "101000101",
          "101111101",
          "100000001",
          "111111111"
        ],
        "output": [
          "222222222",
          "200000002",
          "203333302",
          "203000302",
          "203040302",
          "203000302",
          "203333302",
          "200000002",
          "222222222"
        ]
      },
      {
        "input": [
          "11111111111",
          "10000000001",
          "10111111101",
          "10100000101",
          "10101110101",
          "10101010101",
          "10101110101",
          "10100000101",
          "10111111101",
          "10000000001",
          "11111111111"
        ],
        "output": [
          "22222222222",
          "20000000002",
          "20333333302",
          "20300000302",
          "20304440302",
          "20304040302",
          "20304440302",
          "20300000302",
          "20333333302",
          "20000000002",
          "22222222222"
        ]
      },
      {
        "input": [
          "00000000000000",
          "01111111111110",
          "01000000000010",
          "01011111111010",
          "01010000001010",
          "01010000001010",
          "01011111111010",
          "01000000000010",
          "01111111111110",
          "00000000000000"
        ],
        "output": [
          "00000000000000",
          "02222222222220",
          "02000000000020",
          "02033333333020",
          "02030000003020",
          "02030000003020",
          "02033333333020",
          "02000000000020",
          "02222222222220",
          "00000000000000"
        ]
      },
      {
        "input": [
          "1111111111111",
          "1000000000001",
          "1011111111101",
          "1010000000101",
          "1010111110101",
          "1010100010101",
          "1010101010101",
          "1010100010101",
          "1010111110101",
          "1010000000101",
          "1011111111101",
          "1000000000001",
          "1111111111111"
        ],
        "output": [
          "2222222222222",
          "2000000000002",
          "2033333333302",
          "2030000000302",
          "2030444440302",
          "2030400040302",
          "2030405040302",
          "2030400040302",
          "2030444440302",
          "2030000000302",
          "2033333333302",
          "2000000000002",
          "2222222222222"
        ]
      }
    ],
    "test": {
      "input": [
        "111111111111",
        "100000000001",
        "101111111101",
        "101000000101",
        "101011110101",
        "101010010101",
        "101010010101",
        "101011110101",
        "101000000101",
        "101111111101",
        "100000000001",
        "111111111111"
      ],
      "output": [
        "222222222222",
        "200000000002",
        "203333333302",
        "203000000302",
        "203044440302",
        "203040040302",
        "203040040302",
        "203044440302",
        "203000000302",
        "203333333302",
        "200000000002",
        "222222222222"
      ]
    },
    "program_source": "def rule_h95(g):\n    h,w=size(g)\n    out=blank(h,w)\n    # frames are nonzero borders, possibly same color 1\n    # Determine depth of each nonzero border cell by count of containing rectangles.\n    comps=components_by_color(g)\n    rects=[]\n    for comp in comps:\n        cells=comp[\"cells\"]\n        r0,c0,r1,c1=bbox(cells)\n        border={(r,c) for r in range(r0,r1+1) for c in range(c0,c1+1) if r in (r0,r1) or c in (c0,c1)}\n        if set(cells)==border:\n            rects.append((r0,c0,r1,c1))\n    for r in range(h):\n        for c in range(w):\n            if g[r][c]==0:\n                continue\n            depth=sum(1 for r0,c0,r1,c1 in rects if (r in (r0,r1) and c0<=c<=c1) or (c in (c0,c1) and r0<=r<=r1))\n            # But cell on multiple overlapping borders only possible corners. need depth by smallest containing frame rank\n            containing=[(r0,c0,r1,c1) for r0,c0,r1,c1 in rects if r0<=r<=r1 and c0<=c<=c1]\n            depth=len(containing)\n            out[r][c]=depth+1\n    return out"
  },
  {
    "id": "H96",
    "title": "Command Strip Replay",
    "difficulty": "hard",
    "skills": [
      "command composition",
      "template replay",
      "variable-size output"
    ],
    "staged_hint": "Extract the left motif once. Then read the command strip and append transformed copies in that order.",
    "written_solution": "Use the 3\u00d73 motif on the left as a template. Read the command strip across the top and concatenate transformed copies of that motif in command order.",
    "uses_new_primitive": false,
    "program_name": "rule_h96",
    "train": [
      {
        "input": [
          "00012340",
          "22000000",
          "02000000",
          "22200000"
        ],
        "output": [
          "220202022222",
          "020222020020",
          "222200222022"
        ]
      },
      {
        "input": [
          "0002210",
          "0330000",
          "0030000",
          "0030000"
        ],
        "output": [
          "000000033",
          "003003003",
          "333333003"
        ]
      },
      {
        "input": [
          "0003140",
          "0400000",
          "4440000",
          "0400000"
        ],
        "output": [
          "040040040",
          "444444444",
          "040040040"
        ]
      },
      {
        "input": [
          "00042130",
          "55000000",
          "05500000",
          "00500000"
        ],
        "output": [
          "500005550055",
          "550055055550",
          "055550005500"
        ]
      }
    ],
    "test": {
      "input": [
        "0002410",
        "6600000",
        "0600000",
        "6660000"
      ],
      "output": [
        "606666660",
        "666060060",
        "600066666"
      ]
    },
    "program_source": "def rule_h96(g):\n    h,w=size(g)\n    motif=[row[:3] for row in g[1:4]]\n    cmds=[v for v in g[0][3:] if v!=0]\n    mapping={1: lambda x: clone(x), 2: rotate90, 3: flip_h, 4: rotate180}\n    tiles=[mapping[c](motif) for c in cmds]\n    out=blank(3, sum(len(t[0]) for t in tiles))\n    c0=0\n    for tile in tiles:\n        place_shape(out, tile, 0, c0)\n        c0 += len(tile[0])\n    return out"
  },
  {
    "id": "H97",
    "title": "Shape Equivalence Matrix",
    "difficulty": "hard",
    "skills": [
      "object comparison",
      "shape normalization",
      "relation matrix"
    ],
    "staged_hint": "Crop and normalize every object, keeping only its shape. The output is a comparison matrix over those normalized shapes.",
    "written_solution": "Order the disconnected objects by position, normalize each one by translation only, and fill an N\u00d7N matrix with 8 exactly when two normalized shapes are identical.",
    "uses_new_primitive": false,
    "program_name": "rule_h97",
    "train": [
      {
        "input": [
          "00000000000000",
          "02000000030000",
          "02000000030000",
          "02220000033300",
          "00000000000000",
          "00000000000000",
          "00004440000000",
          "00000400000000",
          "00000400000000",
          "00000000000000"
        ],
        "output": [
          "880",
          "880",
          "008"
        ]
      },
      {
        "input": [
          "000000000000000",
          "050000000000000",
          "050000000000000",
          "055500000000000",
          "000007700000000",
          "000007700000000",
          "000000000060000",
          "000000000060000",
          "088000000066600",
          "088000000000000",
          "000000000000000"
        ],
        "output": [
          "8080",
          "0808",
          "8080",
          "0808"
        ]
      },
      {
        "input": [
          "0000000000000000",
          "0022000000303000",
          "0022000000333000",
          "0020000000000000",
          "0000000000000000",
          "0000000000000000",
          "0000044000000000",
          "0000044000000000",
          "0000040000000000",
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
          "00000000000000",
          "00000000000000",
          "00060000000000",
          "00666000000770",
          "00060000007700",
          "00000000007000",
          "00000000000000",
          "00000000000000",
          "00000800000000",
          "00008880000000",
          "00000800000000",
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
        "000000000000000",
        "022200000000000",
        "002000000000000",
        "002000000000000",
        "000000000000000",
        "000000000044400",
        "000060000004000",
        "000060000004000",
        "000066600000000",
        "000000000000000"
      ],
      "output": [
        "880",
        "880",
        "008"
      ]
    },
    "program_source": "def rule_h97(g):\n    comps=components_by_color(g)\n    # order by bbox top-left\n    comps.sort(key=lambda comp: bbox(comp[\"cells\"])[:2])\n    norms=[normalize_binary_shape(comp[\"cells\"]) for comp in comps]\n    n=len(comps)\n    out=blank(n,n)\n    for i in range(n):\n        for j in range(n):\n            out[i][j]=8 if norms[i]==norms[j] else 0\n    return out"
  },
  {
    "id": "H98",
    "title": "Color Analogy Transfer",
    "difficulty": "hard",
    "skills": [
      "analogy",
      "color mapping",
      "panel reasoning"
    ],
    "staged_hint": "The first two panels show a pure color relabeling with identical geometry. Learn that color map and apply it to the query panel.",
    "written_solution": "Split the three panels, crop away padding, and compare the first two panels to infer a color substitution table. Apply that same color map to the cropped query object in the third panel.",
    "uses_new_primitive": false,
    "program_name": "rule_h98",
    "train": [
      {
        "input": [
          "00000010000001000000",
          "02200010440001022000",
          "00230010047001020300",
          "00033010007701003300",
          "00000010000001000000",
          "00000010000001000000"
        ],
        "output": [
          "440",
          "407",
          "077"
        ]
      },
      {
        "input": [
          "00000010000001000000",
          "00550010088001055000",
          "00055010008801005500",
          "00005010000801000000",
          "00000010000001000000",
          "00000010000001000000"
        ],
        "output": [
          "880",
          "088"
        ]
      },
      {
        "input": [
          "00000010000001000000",
          "06600010220001060700",
          "00600010020001006700",
          "00770010099001000700",
          "00000010000001000000",
          "00000010000001000000"
        ],
        "output": [
          "209",
          "029",
          "009"
        ]
      },
      {
        "input": [
          "00000010000001000000",
          "03300010550001030300",
          "03030010505001003300",
          "00033010005501030000",
          "00000010000001000000",
          "00000010000001000000"
        ],
        "output": [
          "505",
          "055",
          "500"
        ]
      }
    ],
    "test": {
      "input": [
        "00000010000001000000",
        "02200010660001020300",
        "02020010606001022300",
        "00033010004401003300",
        "00000010000001000000",
        "00000010000001000000"
      ],
      "output": [
        "604",
        "664",
        "044"
      ]
    },
    "program_source": "def rule_h98(g):\n    panels,_=split_panels(g, divider=1)\n    a = crop_nonzero([[0 if v==1 else v for v in row] for row in panels[0]])\n    b = crop_nonzero([[0 if v==1 else v for v in row] for row in panels[1]])\n    q = crop_nonzero([[0 if v==1 else v for v in row] for row in panels[2]])\n    cmap=color_mapping_from_pair(a,b)\n    if cmap is None:\n        return q\n    return apply_color_map(q,cmap)"
  }
]''')

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
