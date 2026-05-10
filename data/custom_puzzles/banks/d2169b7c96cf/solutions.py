"""
ARC Additional Puzzle Bank — Set 22

Contains 21 reference puzzles:
  E148–E154, M148–M154, H148–H154

Run this file directly to validate the listed train/test pairs against the
reference rule functions.
"""

from __future__ import annotations
import json
import collections

DIR4 = [(-1,0),(1,0),(0,-1),(0,1)]

def blank(h,w,val=0): return [[val for _ in range(w)] for _ in range(h)]

def clone(g): return [row[:] for row in g]

def size(g): return (len(g), len(g[0]) if g else 0)

def bbox(cells):
    rs=[r for r,c in cells]; cs=[c for r,c in cells]
    return min(rs), min(cs), max(rs), max(cs)

def crop_bbox(g, cells=None, ignore={0}):
    if cells is None:
        cells=[(r,c) for r,row in enumerate(g) for c,v in enumerate(row) if v not in ignore]
    if not cells:
        return [[0]]
    r0,c0,r1,c1=bbox(cells)
    return [row[c0:c1+1] for row in g[r0:r1+1]]

def from_strings(lines): return [[int(ch) for ch in line] for line in lines]

def to_strings(g): return ["".join(str(x) for x in row) for row in g]

def place(base, top,left, pattern):
    out=clone(base)
    if isinstance(pattern[0], str): pattern=from_strings(pattern)
    for r,row in enumerate(pattern):
        for c,v in enumerate(row):
            if v!=0:
                out[top+r][left+c]=v
    return out

def rotate90(g):
    h,w=size(g)
    return [[g[h-1-r][c] for r in range(h)] for c in range(w)]

def rotate180(g): return [list(reversed(row)) for row in reversed(g)]

def rotate270(g): return rotate90(rotate180(g))

def flip_h(g): return [list(reversed(row)) for row in g]

def flip_v(g): return [row[:] for row in reversed(g)]

def apply_transform(g, code):
    # 1=id,2=rot90,3=rot180,4=rot270,5=flip_h,6=flip_v
    if code==1: return clone(g)
    if code==2: return rotate90(g)
    if code==3: return rotate180(g)
    if code==4: return rotate270(g)
    if code==5: return flip_h(g)
    if code==6: return flip_v(g)
    raise ValueError(code)

def components(g, ignore={0}, color_sensitive=True):
    h,w=size(g)
    seen=set(); comps=[]
    for r in range(h):
        for c in range(w):
            v=g[r][c]
            if v in ignore or (r,c) in seen: continue
            q=[(r,c)]; seen.add((r,c)); cells=[]
            while q:
                rr,cc=q.pop()
                cells.append((rr,cc))
                for dr,dc in DIR4:
                    nr,nc=rr+dr,cc+dc
                    if not (0<=nr<h and 0<=nc<w) or (nr,nc) in seen: continue
                    vv=g[nr][nc]
                    if vv in ignore: continue
                    if color_sensitive and vv!=v: continue
                    seen.add((nr,nc)); q.append((nr,nc))
            comps.append({"color":v,"cells":cells})
    return comps

def normalize_cells(cells):
    r0=min(r for r,c in cells); c0=min(c for r,c in cells)
    return tuple(sorted((r-r0,c-c0) for r,c in cells))

def all_dihedral_shapes(g):
    mats=[]; cur=g
    for _ in range(4):
        mats.append(cur); mats.append(flip_h(cur)); cur=rotate90(cur)
    res=set()
    for m in mats:
        cells=[(r,c) for r,row in enumerate(m) for c,v in enumerate(row) if v!=0]
        res.add(normalize_cells(cells))
    return res

def span_markers(markers):
    markers=list(markers)
    if len(markers)!=2: raise ValueError(markers)
    (r1,c1),(r2,c2)=markers
    cells=[]
    if r1==r2:
        a,b=sorted([c1,c2]); cells=[(r1,c) for c in range(a,b+1)]
    elif c1==c2:
        a,b=sorted([r1,r2]); cells=[(r,c1) for r in range(a,b+1)]
    else:
        raise ValueError("not axis-aligned")
    return cells

def fill_chamber(grid, wall=8):
    h,w=size(grid)
    out=clone(grid)
    seen=set()
    for r in range(h):
        for c in range(w):
            if out[r][c]!=0 or (r,c) in seen:
                continue
            q=[(r,c)]
            seen.add((r,c))
            cells=[]
            seed_colors=set()
            while q:
                rr,cc=q.pop()
                cells.append((rr,cc))
                for dr,dc in DIR4:
                    nr,nc=rr+dr,cc+dc
                    if not (0<=nr<h and 0<=nc<w): 
                        continue
                    if (nr,nc) in seen: 
                        continue
                    v=out[nr][nc]
                    if v==wall:
                        continue
                    if v==0:
                        seen.add((nr,nc)); q.append((nr,nc))
                    else:
                        seed_colors.add(v)
            if len(seed_colors)==1:
                color=next(iter(seed_colors))
                for rr,cc in cells:
                    out[rr][cc]=color
    return out

def components_of_color(g, color):
    h,w=size(g); seen=set(); comps=[]
    for r in range(h):
        for c in range(w):
            if g[r][c]!=color or (r,c) in seen: continue
            q=[(r,c)]; seen.add((r,c)); cells=[]
            while q:
                rr,cc=q.pop(); cells.append((rr,cc))
                for dr,dc in DIR4:
                    nr,nc=rr+dr,cc+dc
                    if 0<=nr<h and 0<=nc<w and g[nr][nc]==color and (nr,nc) not in seen:
                        seen.add((nr,nc)); q.append((nr,nc))
            comps.append(cells)
    return comps

def find_rect_frames(g, color=8):
    frames=[]
    for cells in components_of_color(g, color):
        r0,c0,r1,c1=bbox(cells)
        border={(r,c) for r in range(r0,r1+1) for c in range(c0,c1+1) if r in (r0,r1) or c in (c0,c1)}
        if set(cells)==border and r1-r0>=2 and c1-c0>=2:
            frames.append((r0,c0,r1,c1))
    return frames

def split_panels_by_sep(g, sep=9):
    h,w=size(g)
    sep_cols=[c for c in range(w) if all(g[r][c]==sep for r in range(h))]
    # assume two separator columns
    panels=[]
    last=0
    for sc in sep_cols + [w]:
        panel=[row[last:sc] for row in g]
        panels.append(panel)
        last=sc+1
    return panels

def detect_transform(a,b):
    ca=crop_bbox(a)
    cb=crop_bbox(b)
    for code in range(1,7):
        if apply_transform(ca, code)==cb:
            return code
    raise ValueError("no transform")

def rule_e148(g):
    pts=[(r,c,v) for r,row in enumerate(g) for c,v in enumerate(row) if v!=0]
    color=pts[0][2]
    out=blank(*size(g),0)
    cells=span_markers([(pts[0][0],pts[0][1]),(pts[1][0],pts[1][1])])
    for r,c in cells:
        out[r][c]=color
    return out

def rule_e149(g):
    return crop_bbox(g)

def rule_e150(g):
    n,m=size(g)
    assert n==m
    out=clone(g)
    for r in range(n):
        for c in range(m):
            v=g[r][c]
            if v!=0:
                out[c][r]=v
    return out

def rule_e151(g):
    code=g[0][0]
    cells=[(r,c) for r,row in enumerate(g) for c,v in enumerate(row) if v!=0 and not (r==0 and c==0)]
    motif=crop_bbox(g, cells=cells, ignore=set())
    return apply_transform(motif, code)

def rule_e152(g):
    pts=[(r,c) for r,row in enumerate(g) for c,v in enumerate(row) if v!=0]
    r0,c0,r1,c1=bbox(pts)
    color=g[pts[0][0]][pts[0][1]]
    out=blank(*size(g),0)
    for r in range(r0,r1+1):
        for c in range(c0,c1+1):
            out[r][c]=color
    return out

def rule_e153(g):
    pts=[(r,c,v) for r,row in enumerate(g) for c,v in enumerate(row) if v!=0]
    color=pts[0][2]
    coords=[(r,c) for r,c,v in pts]
    r0,c0,r1,c1=bbox(coords)
    side=r1-r0
    out=blank(*size(g),0)
    for i in range(side+1):
        out[r0+i][c0+i]=color
        out[r0+i][c1-i]=color
    return out

def rule_e154(g):
    return [row[:] for row in g if any(v!=0 for v in row)]

def rule_m148(g):
    comps=components(g, ignore={0}, color_sensitive=False)
    best=max(comps, key=lambda comp: len(comp["cells"]))
    return crop_bbox(g, cells=best["cells"], ignore=set())

def rule_m149(g):
    order=[v for v in g[0] if v!=0]
    below=[row[:] for row in g[1:]]
    comps=components(below, ignore={0}, color_sensitive=True)
    keyed={}
    for comp in comps:
        color=comp["color"]
        crop=crop_bbox(below, cells=comp["cells"], ignore=set())
        keyed[color]=crop
    pieces=[keyed[c] for c in order]
    h=max(size(p)[0] for p in pieces)
    gap=1
    total_w=sum(size(p)[1] for p in pieces)+gap*(len(pieces)-1)
    out=blank(h,total_w,0)
    c0=0
    for idx,p in enumerate(pieces):
        ph,pw=size(p)
        for r in range(ph):
            for c in range(pw):
                if p[r][c]!=0:
                    out[r][c0+c]=p[r][c]
        c0 += pw
        if idx < len(pieces)-1:
            c0 += gap
    return out

def rule_m150(g):
    return fill_chamber(g, wall=8)

def rule_m151(g):
    h,w=size(g)
    src=dst=None
    payload=[]
    for r,row in enumerate(g):
        for c,v in enumerate(row):
            if v==2:
                src=(r,c)
            elif v==3:
                dst=(r,c)
            elif v!=0:
                payload.append((r,c,v))
    dr=dst[0]-src[0]; dc=dst[1]-src[1]
    out=blank(h,w,0)
    for r,c,v in payload:
        rr,cc=r+dr,c+dc
        if 0<=rr<h and 0<=cc<w:
            out[rr][cc]=v
    return out

def rule_m152(g):
    h,w=size(g)
    by_color=collections.defaultdict(list)
    for r,row in enumerate(g):
        for c,v in enumerate(row):
            if v!=0:
                by_color[v].append((r,c))
    cover=collections.defaultdict(list)
    for color, pts in by_color.items():
        cells=span_markers(pts)
        for cell in cells:
            cover[cell].append(color)
    out=blank(h,w,0)
    for (r,c), colors in cover.items():
        out[r][c]=9 if len(colors)>1 else colors[0]
    return out

def rule_m153(g):
    counts=collections.Counter()
    h,w=size(g)
    # Count connected components per color
    seen=set()
    for r in range(h):
        for c in range(w):
            v=g[r][c]
            if v==0 or (r,c) in seen:
                continue
            q=[(r,c)]; seen.add((r,c)); cells=[]
            while q:
                rr,cc=q.pop(); cells.append((rr,cc))
                for dr,dc in DIR4:
                    nr,nc=rr+dr,cc+dc
                    if 0<=nr<h and 0<=nc<w and (nr,nc) not in seen and g[nr][nc]==v:
                        seen.add((nr,nc)); q.append((nr,nc))
            counts[v]+=1
    colors=sorted(counts)
    width=max(counts.values()) if counts else 1
    out=blank(len(colors), width, 0)
    for r,color in enumerate(colors):
        for c in range(counts[color]):
            out[r][c]=color
    return out

def rule_m154(g):
    out=clone(g)
    # template: all nonzero non-8 cells
    temp_cells=[(r,c) for r,row in enumerate(g) for c,v in enumerate(row) if v not in (0,8)]
    temp=crop_bbox(g, cells=temp_cells, ignore=set())
    th,tw=size(temp)
    for r0,c0,r1,c1 in find_rect_frames(g, color=8):
        ih,iw=r1-r0-1,c1-c0-1
        if (ih,iw)==(th,tw):
            for r in range(th):
                for c in range(tw):
                    if temp[r][c]!=0:
                        out[r0+1+r][c0+1+c]=temp[r][c]
            break
    return out

def rule_h148(g):
    panels=split_panels_by_sep(g, sep=9)
    a,b,c=panels
    code=detect_transform(a,b)
    return apply_transform(crop_bbox(c), code)

def rule_h149(g):
    comps=components_of_color(g, 1)
    ordered=sorted(comps, key=lambda cells: ((bbox(cells)[2]-bbox(cells)[0]+1)*(bbox(cells)[3]-bbox(cells)[1]+1)), reverse=True)
    out=blank(*size(g),0)
    for idx,cells in enumerate(ordered, start=2):
        for r,c in cells:
            out[r][c]=idx
    return out

def rule_h150(g):
    h,w=size(g)
    out=clone(g)
    seeds=[(r,c,v) for r,row in enumerate(g) for c,v in enumerate(row) if v not in (0,5)]
    for r in range(h):
        for c in range(w):
            if g[r][c]!=0:
                continue
            best=min(abs(sr-r)+abs(sc-c) for sr,sc,_ in seeds)
            colors=[v for sr,sc,v in seeds if abs(sr-r)+abs(sc-c)==best]
            out[r][c]=colors[0] if len(colors)==1 else 8
    return out

def rule_h151(g):
    comps=sorted(components(g, ignore={0}, color_sensitive=False), key=lambda comp: bbox(comp["cells"])[:2])
    shape_sets=[all_dihedral_shapes(crop_bbox(g, cells=comp["cells"], ignore=set())) for comp in comps]
    n=len(shape_sets)
    out=blank(n,n,0)
    for i in range(n):
        for j in range(n):
            out[i][j]=2 if shape_sets[i] & shape_sets[j] else 0
    return out

def rule_h152(g):
    h,w=size(g)
    by_color=collections.defaultdict(list)
    for r,row in enumerate(g):
        for c,v in enumerate(row):
            if v!=0:
                by_color[v].append((r,c))
    cover=collections.Counter()
    for color,pts in by_color.items():
        for cell in span_markers(pts):
            cover[cell]+=1
    out=blank(h,w,0)
    for (r,c), n in cover.items():
        if n==2:
            out[r][c]=8
        elif n>=3:
            out[r][c]=9
    return out

def rule_h153(g):
    panels=split_panels_by_sep(g, sep=9)
    a,b,c=panels
    # derive color map from overlapping nonzero cells in cropped panels? better use full panels same size
    mapping={}
    for r in range(len(a)):
        for col in range(len(a[0])):
            va=a[r][col]; vb=b[r][col]
            if va!=0:
                mapping[va]=vb
    out=crop_bbox(c)
    for r,row in enumerate(out):
        for col,v in enumerate(row):
            if v!=0:
                out[r][col]=mapping[v]
    return out

def rule_h154(g):
    code1,code2=[v for v in g[0] if v!=0][:2]
    motif=[row[:] for row in g[1:]]
    motif=crop_bbox(motif)
    return apply_transform(apply_transform(motif, code1), code2)

RULES = {
    "E148": rule_e148,
    "E149": rule_e149,
    "E150": rule_e150,
    "E151": rule_e151,
    "E152": rule_e152,
    "E153": rule_e153,
    "E154": rule_e154,
    "M148": rule_m148,
    "M149": rule_m149,
    "M150": rule_m150,
    "M151": rule_m151,
    "M152": rule_m152,
    "M153": rule_m153,
    "M154": rule_m154,
    "H148": rule_h148,
    "H149": rule_h149,
    "H150": rule_h150,
    "H151": rule_h151,
    "H152": rule_h152,
    "H153": rule_h153,
    "H154": rule_h154,
}

PUZZLES = json.loads(r'''[
  {
    "id": "E148",
    "title": "Complete the Axis Span",
    "difficulty": "easy",
    "skills": [
      "endpoint detection",
      "axis-aligned completion",
      "same-color fill"
    ],
    "suggested_staged_path": "Ignore the empty space and look only at the two matching markers. Decide whether they share a row or a column, then fill the closed interval between them.",
    "written_solution": "There are exactly two nonzero markers of the same color. They lie on one row or one column. Fill every cell from one marker to the other, inclusive, with that same color.",
    "program_name": "rule_e148",
    "program_source": "def rule_e148(g):\n    pts=[(r,c,v) for r,row in enumerate(g) for c,v in enumerate(row) if v!=0]\n    color=pts[0][2]\n    out=blank(*size(g),0)\n    cells=span_markers([(pts[0][0],pts[0][1]),(pts[1][0],pts[1][1])])\n    for r,c in cells:\n        out[r][c]=color\n    return out\n",
    "train": [
      {
        "input": [
          "000000000",
          "000000000",
          "080000080",
          "000000000",
          "000000000",
          "000000000"
        ],
        "output": [
          "000000000",
          "000000000",
          "088888880",
          "000000000",
          "000000000",
          "000000000"
        ]
      },
      {
        "input": [
          "000000",
          "000400",
          "000000",
          "000000",
          "000000",
          "000000",
          "000400",
          "000000"
        ],
        "output": [
          "000000",
          "000400",
          "000400",
          "000400",
          "000400",
          "000400",
          "000400",
          "000000"
        ]
      },
      {
        "input": [
          "0000000000",
          "0000000000",
          "0000000000",
          "0000000000",
          "0000000000",
          "0060000060",
          "0000000000"
        ],
        "output": [
          "0000000000",
          "0000000000",
          "0000000000",
          "0000000000",
          "0000000000",
          "0066666660",
          "0000000000"
        ]
      },
      {
        "input": [
          "0000000",
          "0000000",
          "0000030",
          "0000000",
          "0000000",
          "0000000",
          "0000000",
          "0000030",
          "0000000"
        ],
        "output": [
          "0000000",
          "0000000",
          "0000030",
          "0000030",
          "0000030",
          "0000030",
          "0000030",
          "0000030",
          "0000000"
        ]
      }
    ],
    "test": [
      {
        "input": [
          "00000000000",
          "00000000000",
          "00000000000",
          "07000000070",
          "00000000000",
          "00000000000",
          "00000000000",
          "00000000000"
        ],
        "output": [
          "00000000000",
          "00000000000",
          "00000000000",
          "07777777770",
          "00000000000",
          "00000000000",
          "00000000000",
          "00000000000"
        ]
      }
    ]
  },
  {
    "id": "E149",
    "title": "Tight Crop of the Motif",
    "difficulty": "easy",
    "skills": [
      "bounding box detection",
      "output resizing",
      "motif extraction"
    ],
    "suggested_staged_path": "First forget the surrounding black area. Find the smallest rectangle that contains every nonzero cell, then output only that rectangle.",
    "written_solution": "All black padding is irrelevant. Compute the tight bounding box of the nonzero pattern and return just that cropped subgrid.",
    "program_name": "rule_e149",
    "program_source": "def rule_e149(g):\n    return crop_bbox(g)\n",
    "train": [
      {
        "input": [
          "000000000",
          "000000000",
          "000023000",
          "000020300",
          "000000000",
          "000000000",
          "000000000",
          "000000000"
        ],
        "output": [
          "230",
          "203"
        ]
      },
      {
        "input": [
          "0000000000",
          "0000000000",
          "0000000000",
          "0045000000",
          "0400400000",
          "0000000000",
          "0000000000"
        ],
        "output": [
          "0450",
          "4004"
        ]
      },
      {
        "input": [
          "000000000",
          "000000670",
          "000006070",
          "000007700",
          "000000000",
          "000000000",
          "000000000",
          "000000000",
          "000000000"
        ],
        "output": [
          "067",
          "607",
          "770"
        ]
      },
      {
        "input": [
          "00000000000",
          "00000000000",
          "00000000000",
          "00000000000",
          "00028000000",
          "00020200000",
          "00002200000",
          "00000000000"
        ],
        "output": [
          "280",
          "202",
          "022"
        ]
      }
    ],
    "test": [
      {
        "input": [
          "000000000000",
          "000000000000",
          "000000000000",
          "000000000000",
          "000000000000",
          "000000340000",
          "000000304000",
          "000000044000",
          "000000000000",
          "000000000000"
        ],
        "output": [
          "340",
          "304",
          "044"
        ]
      }
    ]
  },
  {
    "id": "E150",
    "title": "Mirror Across the Main Diagonal",
    "difficulty": "easy",
    "skills": [
      "diagonal symmetry",
      "same-size completion",
      "coordinate transposition"
    ],
    "suggested_staged_path": "Treat each colored cell as an instruction to also color its transposed position. Keep originals and add the reflected copy across the main diagonal.",
    "written_solution": "For every nonzero cell at row r and column c, copy the same color to position c,r. The result is the original pattern plus its mirror across the main diagonal.",
    "program_name": "rule_e150",
    "program_source": "def rule_e150(g):\n    n,m=size(g)\n    assert n==m\n    out=clone(g)\n    for r in range(n):\n        for c in range(m):\n            v=g[r][c]\n            if v!=0:\n                out[c][r]=v\n    return out\n",
    "train": [
      {
        "input": [
          "004000",
          "000420",
          "000000",
          "000000",
          "000000",
          "000000"
        ],
        "output": [
          "004000",
          "000420",
          "400000",
          "040000",
          "020000",
          "000000"
        ]
      },
      {
        "input": [
          "0000600",
          "0003000",
          "0000060",
          "0000000",
          "0000000",
          "0000000",
          "0000000"
        ],
        "output": [
          "0000600",
          "0003000",
          "0000060",
          "0300000",
          "6000000",
          "0060000",
          "0000000"
        ]
      },
      {
        "input": [
          "08020",
          "00008",
          "00000",
          "00000",
          "00000"
        ],
        "output": [
          "08020",
          "80008",
          "00000",
          "20000",
          "08000"
        ]
      },
      {
        "input": [
          "00005000",
          "00000070",
          "00000700",
          "00000000",
          "00000000",
          "00000000",
          "00000000",
          "00000000"
        ],
        "output": [
          "00005000",
          "00000070",
          "00000700",
          "00000000",
          "50000000",
          "00700000",
          "07000000",
          "00000000"
        ]
      }
    ],
    "test": [
      {
        "input": [
          "000003",
          "006030",
          "000600",
          "000000",
          "000000",
          "000000"
        ],
        "output": [
          "000003",
          "006030",
          "060600",
          "006000",
          "030000",
          "300000"
        ]
      }
    ]
  },
  {
    "id": "E151",
    "title": "Rotate the Motif by the Corner Command",
    "difficulty": "easy",
    "skills": [
      "legend decoding",
      "rotation",
      "cropped output"
    ],
    "suggested_staged_path": "Separate the command cell from the motif. Crop the motif first, then interpret the command value as which rotation to apply.",
    "written_solution": "The top-left command chooses a rotation: 1 means leave the motif as-is, 2 means rotate 90 degrees clockwise, 3 means rotate 180 degrees, and 4 means rotate 270 degrees. Ignore the command cell itself, crop the remaining motif tightly, and output the rotated crop.",
    "program_name": "rule_e151",
    "program_source": "def rule_e151(g):\n    code=g[0][0]\n    cells=[(r,c) for r,row in enumerate(g) for c,v in enumerate(row) if v!=0 and not (r==0 and c==0)]\n    motif=crop_bbox(g, cells=cells, ignore=set())\n    return apply_transform(motif, code)\n",
    "train": [
      {
        "input": [
          "200000000",
          "000000000",
          "000000000",
          "000023000",
          "000020300",
          "000000000",
          "000000000",
          "000000000"
        ],
        "output": [
          "22",
          "03",
          "30"
        ]
      },
      {
        "input": [
          "30000000",
          "00000000",
          "00450000",
          "00045000",
          "00005000",
          "00000000",
          "00000000"
        ],
        "output": [
          "500",
          "540",
          "054"
        ]
      },
      {
        "input": [
          "400000000",
          "000000000",
          "000000000",
          "000000000",
          "000000000",
          "000006700",
          "000006070",
          "000000000",
          "000000000"
        ],
        "output": [
          "07",
          "70",
          "66"
        ]
      },
      {
        "input": [
          "1000000000",
          "0000000000",
          "0000000000",
          "0000002800",
          "0000002820",
          "0000002200",
          "0000000000",
          "0000000000"
        ],
        "output": [
          "280",
          "282",
          "220"
        ]
      }
    ],
    "test": [
      {
        "input": [
          "2000000000",
          "0000000000",
          "0000000000",
          "0000000000",
          "0034000000",
          "0030400000",
          "0004400000",
          "0000000000",
          "0000000000"
        ],
        "output": [
          "033",
          "404",
          "440"
        ]
      }
    ]
  },
  {
    "id": "E152",
    "title": "Fill the Hollow Rectangle",
    "difficulty": "easy",
    "skills": [
      "rectangle inference",
      "interior fill",
      "same-size completion"
    ],
    "suggested_staged_path": "Recognize that the nonzero cells are the border of one rectangle. Once the bounding box is clear, fill the whole box with that color.",
    "written_solution": "The colored cells form a hollow axis-aligned rectangle. Keep the same bounding box, but fill its entire interior and border with the rectangle's color.",
    "program_name": "rule_e152",
    "program_source": "def rule_e152(g):\n    pts=[(r,c) for r,row in enumerate(g) for c,v in enumerate(row) if v!=0]\n    r0,c0,r1,c1=bbox(pts)\n    color=g[pts[0][0]][pts[0][1]]\n    out=blank(*size(g),0)\n    for r in range(r0,r1+1):\n        for c in range(c0,c1+1):\n            out[r][c]=color\n    return out\n",
    "train": [
      {
        "input": [
          "0000000000",
          "0044444400",
          "0040000400",
          "0040000400",
          "0040000400",
          "0044444400",
          "0000000000",
          "0000000000"
        ],
        "output": [
          "0000000000",
          "0044444400",
          "0044444400",
          "0044444400",
          "0044444400",
          "0044444400",
          "0000000000",
          "0000000000"
        ]
      },
      {
        "input": [
          "000000000",
          "000000000",
          "066666600",
          "060000600",
          "060000600",
          "066666600",
          "000000000"
        ],
        "output": [
          "000000000",
          "000000000",
          "066666600",
          "066666600",
          "066666600",
          "066666600",
          "000000000"
        ]
      },
      {
        "input": [
          "000000000",
          "033333330",
          "030000030",
          "030000030",
          "030000030",
          "030000030",
          "030000030",
          "033333330",
          "000000000"
        ],
        "output": [
          "000000000",
          "033333330",
          "033333330",
          "033333330",
          "033333330",
          "033333330",
          "033333330",
          "033333330",
          "000000000"
        ]
      },
      {
        "input": [
          "00000000000",
          "00007777770",
          "00007000070",
          "00007000070",
          "00007777770",
          "00000000000"
        ],
        "output": [
          "00000000000",
          "00007777770",
          "00007777770",
          "00007777770",
          "00007777770",
          "00000000000"
        ]
      }
    ],
    "test": [
      {
        "input": [
          "000000000000",
          "000000000000",
          "000555555550",
          "000500000050",
          "000500000050",
          "000500000050",
          "000555555550",
          "000000000000"
        ],
        "output": [
          "000000000000",
          "000000000000",
          "000555555550",
          "000555555550",
          "000555555550",
          "000555555550",
          "000555555550",
          "000000000000"
        ]
      }
    ]
  },
  {
    "id": "E153",
    "title": "Draw the X from Square Corners",
    "difficulty": "easy",
    "skills": [
      "corner inference",
      "diagonal drawing",
      "square geometry"
    ],
    "suggested_staged_path": "Use the four markers only to recover the square they define. Then draw both diagonals of that square in the same color.",
    "written_solution": "The four colored cells are the corners of a square. Draw both diagonals connecting opposite corners, using the same color as the markers, and leave everything else black.",
    "program_name": "rule_e153",
    "program_source": "def rule_e153(g):\n    pts=[(r,c,v) for r,row in enumerate(g) for c,v in enumerate(row) if v!=0]\n    color=pts[0][2]\n    coords=[(r,c) for r,c,v in pts]\n    r0,c0,r1,c1=bbox(coords)\n    side=r1-r0\n    out=blank(*size(g),0)\n    for i in range(side+1):\n        out[r0+i][c0+i]=color\n        out[r0+i][c1-i]=color\n    return out\n",
    "train": [
      {
        "input": [
          "00000000",
          "02000200",
          "00000000",
          "00000000",
          "00000000",
          "02000200",
          "00000000",
          "00000000"
        ],
        "output": [
          "00000000",
          "02000200",
          "00202000",
          "00020000",
          "00202000",
          "02000200",
          "00000000",
          "00000000"
        ]
      },
      {
        "input": [
          "000000000",
          "000000000",
          "000600600",
          "000000000",
          "000000000",
          "000600600",
          "000000000",
          "000000000",
          "000000000"
        ],
        "output": [
          "000000000",
          "000000000",
          "000600600",
          "000066000",
          "000066000",
          "000600600",
          "000000000",
          "000000000",
          "000000000"
        ]
      },
      {
        "input": [
          "0000000000",
          "0000700007",
          "0000000000",
          "0000000000",
          "0000000000",
          "0000000000",
          "0000700007",
          "0000000000",
          "0000000000",
          "0000000000"
        ],
        "output": [
          "0000000000",
          "0000700007",
          "0000070070",
          "0000007700",
          "0000007700",
          "0000070070",
          "0000700007",
          "0000000000",
          "0000000000",
          "0000000000"
        ]
      },
      {
        "input": [
          "4000004",
          "0000000",
          "0000000",
          "0000000",
          "0000000",
          "0000000",
          "4000004"
        ],
        "output": [
          "4000004",
          "0400040",
          "0040400",
          "0004000",
          "0040400",
          "0400040",
          "4000004"
        ]
      }
    ],
    "test": [
      {
        "input": [
          "000000000",
          "008000800",
          "000000000",
          "000000000",
          "000000000",
          "008000800",
          "000000000",
          "000000000",
          "000000000"
        ],
        "output": [
          "000000000",
          "008000800",
          "000808000",
          "000080000",
          "000808000",
          "008000800",
          "000000000",
          "000000000",
          "000000000"
        ]
      }
    ]
  },
  {
    "id": "E154",
    "title": "Keep Only the Nonempty Rows",
    "difficulty": "easy",
    "skills": [
      "row filtering",
      "output resizing",
      "order preservation"
    ],
    "suggested_staged_path": "Look row by row and ignore any row that is completely black. Stack the remaining rows in their original top-to-bottom order.",
    "written_solution": "Delete every all-zero row. The output is just the nonempty rows, preserved in the same order and with the same width as before.",
    "program_name": "rule_e154",
    "program_source": "def rule_e154(g):\n    return [row[:] for row in g if any(v!=0 for v in row)]\n",
    "train": [
      {
        "input": [
          "00000000",
          "02200000",
          "00000000",
          "00440000",
          "00000000",
          "00000000",
          "00006600"
        ],
        "output": [
          "02200000",
          "00440000",
          "00006600"
        ]
      },
      {
        "input": [
          "0300000",
          "0000000",
          "0000000",
          "0000000",
          "0005500",
          "0000000",
          "0000000",
          "7000007"
        ],
        "output": [
          "0300000",
          "0005500",
          "7000007"
        ]
      },
      {
        "input": [
          "000000000",
          "000000000",
          "000888000",
          "000000000",
          "000000000",
          "404000404"
        ],
        "output": [
          "000888000",
          "404000404"
        ]
      },
      {
        "input": [
          "000000",
          "066000",
          "000033",
          "000000",
          "000000",
          "000000",
          "000000",
          "000000",
          "222000"
        ],
        "output": [
          "066000",
          "000033",
          "222000"
        ]
      }
    ],
    "test": [
      {
        "input": [
          "00500000",
          "00000000",
          "00000000",
          "77000000",
          "00000000",
          "00002220",
          "00000000",
          "00000000"
        ],
        "output": [
          "00500000",
          "77000000",
          "00002220"
        ]
      }
    ]
  },
  {
    "id": "M148",
    "title": "Crop the Largest Component",
    "difficulty": "medium",
    "skills": [
      "connected components",
      "size comparison",
      "bounding box crop"
    ],
    "suggested_staged_path": "First split the grid into disconnected objects. Compare their areas, keep only the largest one, and crop it tightly.",
    "written_solution": "Treat each disconnected nonzero object as one component. Select the component with the most cells and output its tight bounding box, preserving its colors.",
    "program_name": "rule_m148",
    "program_source": "def rule_m148(g):\n    comps=components(g, ignore={0}, color_sensitive=False)\n    best=max(comps, key=lambda comp: len(comp[\"cells\"]))\n    return crop_bbox(g, cells=best[\"cells\"], ignore=set())\n",
    "train": [
      {
        "input": [
          "000000000000",
          "022000000000",
          "020000000000",
          "000000000000",
          "000000033000",
          "000000003300",
          "004000000300",
          "004400000000",
          "000000000000"
        ],
        "output": [
          "330",
          "033",
          "003"
        ]
      },
      {
        "input": [
          "0000000000",
          "0000055000",
          "0000050500",
          "0000055500",
          "0000000700",
          "0000000000",
          "0660000000",
          "0600000000",
          "0000000000",
          "0000000000"
        ],
        "output": [
          "550",
          "505",
          "555",
          "007"
        ]
      },
      {
        "input": [
          "0000000000000",
          "0280000000000",
          "0282000033000",
          "0220000030000",
          "0000000000000",
          "0000044000000",
          "0000004400000",
          "0000000000000"
        ],
        "output": [
          "280",
          "282",
          "220"
        ]
      },
      {
        "input": [
          "67000000000",
          "60700000000",
          "00000000000",
          "00000000000",
          "00000023000",
          "00000020300",
          "00000022000",
          "00800000000",
          "00000000000"
        ],
        "output": [
          "23",
          "20",
          "22"
        ]
      }
    ],
    "test": [
      {
        "input": [
          "000000000000",
          "000000000330",
          "004500000000",
          "004050000000",
          "004440000000",
          "000000000000",
          "000000000000",
          "000000280000",
          "000000202000",
          "000000000000"
        ],
        "output": [
          "450",
          "405",
          "444"
        ]
      }
    ]
  },
  {
    "id": "M149",
    "title": "Assemble Components by Legend Order",
    "difficulty": "medium",
    "skills": [
      "legend reading",
      "component extraction",
      "horizontal packing"
    ],
    "suggested_staged_path": "Use the top row only as an ordering legend. Find the component matching each legend color, crop each one, and then place those crops left-to-right in the legend order.",
    "written_solution": "The top row lists the colors in the desired order. Below it, each listed color appears as exactly one component. Crop each component tightly and concatenate the crops from left to right with a single black column between neighbors.",
    "program_name": "rule_m149",
    "program_source": "def rule_m149(g):\n    order=[v for v in g[0] if v!=0]\n    below=[row[:] for row in g[1:]]\n    comps=components(below, ignore={0}, color_sensitive=True)\n    keyed={}\n    for comp in comps:\n        color=comp[\"color\"]\n        crop=crop_bbox(below, cells=comp[\"cells\"], ignore=set())\n        keyed[color]=crop\n    pieces=[keyed[c] for c in order]\n    h=max(size(p)[0] for p in pieces)\n    gap=1\n    total_w=sum(size(p)[1] for p in pieces)+gap*(len(pieces)-1)\n    out=blank(h,total_w,0)\n    c0=0\n    for idx,p in enumerate(pieces):\n        ph,pw=size(p)\n        for r in range(ph):\n            for c in range(pw):\n                if p[r][c]!=0:\n                    out[r][c0+c]=p[r][c]\n        c0 += pw\n        if idx < len(pieces)-1:\n            c0 += gap\n    return out\n",
    "train": [
      {
        "input": [
          "04020700000000",
          "00000000000000",
          "02200440000000",
          "02000044007000",
          "00000000007700"
        ],
        "output": [
          "440022070",
          "044020077"
        ]
      },
      {
        "input": [
          "060308000000000",
          "000000000000000",
          "000000808000000",
          "033000888006000",
          "003000000006600"
        ],
        "output": [
          "600330808",
          "660030888"
        ]
      },
      {
        "input": [
          "0507020000000000",
          "0000000000000000",
          "0022000000005550",
          "0020200070005000",
          "0000000077000000",
          "0000000007000000"
        ],
        "output": [
          "55507002",
          "50007700",
          "00000700"
        ]
      },
      {
        "input": [
          "080406000000000",
          "000000000000000",
          "040000000008080",
          "044000660000800",
          "000000600000000",
          "000000660000000"
        ],
        "output": [
          "8040066",
          "0044060",
          "0000066"
        ]
      }
    ],
    "test": [
      {
        "input": [
          "0705030000000000",
          "0000000000000000",
          "0330000000070700",
          "0003000500007700",
          "0000000550000000"
        ],
        "output": [
          "0705003",
          "7705500"
        ]
      }
    ]
  },
  {
    "id": "M150",
    "title": "Flood Each Chamber from Its Seed",
    "difficulty": "medium",
    "skills": [
      "chamber detection",
      "wall-aware flood fill",
      "seed propagation"
    ],
    "suggested_staged_path": "Treat the wall color as blocking cells and identify the empty regions it creates. Each region touches one colored seed; fill that region with the seed color.",
    "written_solution": "The wall color partitions the grid into chambers. Every chamber contains exactly one colored seed. Replace the zeros in that chamber with the seed color while leaving the walls unchanged.",
    "program_name": "rule_m150",
    "program_source": "def rule_m150(g):\n    return fill_chamber(g, wall=8)\n",
    "train": [
      {
        "input": [
          "88888888888",
          "80000800008",
          "80200800008",
          "80000800008",
          "80000800008",
          "80000800008",
          "80000800408",
          "80000800008",
          "88888888888"
        ],
        "output": [
          "88888888888",
          "82222844448",
          "82222844448",
          "82222844448",
          "82222844448",
          "82222844448",
          "82222844448",
          "82222844448",
          "88888888888"
        ]
      },
      {
        "input": [
          "8888888888",
          "8000000008",
          "8000000308",
          "8000000008",
          "8000000008",
          "8888888888",
          "8000000008",
          "8060000008",
          "8000000008",
          "8888888888"
        ],
        "output": [
          "8888888888",
          "8333333338",
          "8333333338",
          "8333333338",
          "8333333338",
          "8888888888",
          "8666666668",
          "8666666668",
          "8666666668",
          "8888888888"
        ]
      },
      {
        "input": [
          "8888888888888",
          "8000800080008",
          "8000800080008",
          "8050800080008",
          "8000800080008",
          "8000800080008",
          "8000802080008",
          "8000800080008",
          "8000800080708",
          "8000800080008",
          "8888888888888"
        ],
        "output": [
          "8888888888888",
          "8555822287778",
          "8555822287778",
          "8555822287778",
          "8555822287778",
          "8555822287778",
          "8555822287778",
          "8555822287778",
          "8555822287778",
          "8555822287778",
          "8888888888888"
        ]
      },
      {
        "input": [
          "888888888888",
          "800000800008",
          "804000806008",
          "800000800008",
          "888888888888",
          "800000800008",
          "800000800008",
          "800300800508",
          "800000800008",
          "888888888888"
        ],
        "output": [
          "888888888888",
          "844444866668",
          "844444866668",
          "844444866668",
          "888888888888",
          "833333855558",
          "833333855558",
          "833333855558",
          "833333855558",
          "888888888888"
        ]
      }
    ],
    "test": [
      {
        "input": [
          "888888888888",
          "800080008008",
          "802080008008",
          "800080008008",
          "800080708008",
          "800080008008",
          "800080008038",
          "800080008008",
          "888888888888"
        ],
        "output": [
          "888888888888",
          "822287778338",
          "822287778338",
          "822287778338",
          "822287778338",
          "822287778338",
          "822287778338",
          "822287778338",
          "888888888888"
        ]
      }
    ]
  },
  {
    "id": "M151",
    "title": "Translate the Payload by the Anchor Vector",
    "difficulty": "medium",
    "skills": [
      "vector extraction",
      "translation",
      "object isolation"
    ],
    "suggested_staged_path": "Ignore the payload at first and compute the vector from the source anchor to the target anchor. Then apply that same vector to every payload cell.",
    "written_solution": "One anchor marks the starting point and another marks the destination. Compute the offset from the first anchor to the second, remove the anchors, and copy the payload component after translating every one of its cells by that offset.",
    "program_name": "rule_m151",
    "program_source": "def rule_m151(g):\n    h,w=size(g)\n    src=dst=None\n    payload=[]\n    for r,row in enumerate(g):\n        for c,v in enumerate(row):\n            if v==2:\n                src=(r,c)\n            elif v==3:\n                dst=(r,c)\n            elif v!=0:\n                payload.append((r,c,v))\n    dr=dst[0]-src[0]; dc=dst[1]-src[1]\n    out=blank(h,w,0)\n    for r,c,v in payload:\n        rr,cc=r+dr,c+dc\n        if 0<=rr<h and 0<=cc<w:\n            out[rr][cc]=v\n    return out\n",
    "train": [
      {
        "input": [
          "0000000000",
          "0200000000",
          "0044000000",
          "0040000000",
          "0000030000",
          "0000000000",
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
          "0000004400",
          "0000004000",
          "0000000000",
          "0000000000"
        ]
      },
      {
        "input": [
          "00000000000",
          "00000000000",
          "00000000200",
          "00000002300",
          "00000002030",
          "00000000000",
          "00003000000",
          "00000000000",
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
          "00000000000",
          "00000000000"
        ]
      },
      {
        "input": [
          "000000000000",
          "067000000020",
          "060700000000",
          "000000000000",
          "000000000000",
          "000000300000",
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
          "000000000000"
        ]
      },
      {
        "input": [
          "00000000000",
          "00000000000",
          "00000000000",
          "00000000000",
          "00000300000",
          "00000000000",
          "00550000000",
          "00505000000",
          "02000000000",
          "00000000000",
          "00000000000"
        ],
        "output": [
          "00000000000",
          "00000000000",
          "00000055000",
          "00000050500",
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
    "test": [
      {
        "input": [
          "000000000000",
          "002000000000",
          "028000000000",
          "028200000000",
          "022000000000",
          "000000000000",
          "000000003000",
          "000000000000",
          "000000000000",
          "000000000000"
        ],
        "output": [
          "000000000000",
          "000000000000",
          "000000000000",
          "000000000000",
          "000000008000",
          "000000008000",
          "000000000000",
          "000000000000",
          "000000000000",
          "000000000000"
        ]
      }
    ]
  },
  {
    "id": "M152",
    "title": "Span Overlay with Crossings",
    "difficulty": "medium",
    "skills": [
      "pairwise span inference",
      "overlap handling",
      "same-size synthesis"
    ],
    "suggested_staged_path": "Recover each axis-aligned span independently from its matching marker pair. Only after that should you merge the spans and mark any shared cells specially.",
    "written_solution": "Each color appears exactly twice and those two markers define one horizontal or vertical span. Draw all such spans. Cells covered by only one span keep that span's color, while cells where two or more spans overlap become 9.",
    "program_name": "rule_m152",
    "program_source": "def rule_m152(g):\n    h,w=size(g)\n    by_color=collections.defaultdict(list)\n    for r,row in enumerate(g):\n        for c,v in enumerate(row):\n            if v!=0:\n                by_color[v].append((r,c))\n    cover=collections.defaultdict(list)\n    for color, pts in by_color.items():\n        cells=span_markers(pts)\n        for cell in cells:\n            cover[cell].append(color)\n    out=blank(h,w,0)\n    for (r,c), colors in cover.items():\n        out[r][c]=9 if len(colors)>1 else colors[0]\n    return out\n",
    "train": [
      {
        "input": [
          "0000400000",
          "0200000200",
          "0000000000",
          "0000000000",
          "0000000000",
          "0000000000",
          "0000400000",
          "0000000000"
        ],
        "output": [
          "0000400000",
          "0222922200",
          "0000400000",
          "0000400000",
          "0000400000",
          "0000400000",
          "0000400000",
          "0000000000"
        ]
      },
      {
        "input": [
          "000000000",
          "000000700",
          "030000000",
          "000000000",
          "000000000",
          "600000006",
          "000000000",
          "030000700",
          "000000000"
        ],
        "output": [
          "000000000",
          "000000700",
          "030000700",
          "030000700",
          "030000700",
          "696666966",
          "030000700",
          "030000700",
          "000000000"
        ]
      },
      {
        "input": [
          "000000000000",
          "000005000000",
          "000000000000",
          "002000000020",
          "000000000000",
          "000000000000",
          "070000000700",
          "000000000000",
          "000005000000",
          "000000000000"
        ],
        "output": [
          "000000000000",
          "000005000000",
          "000005000000",
          "002229222220",
          "000005000000",
          "000005000000",
          "077779777700",
          "000005000000",
          "000005000000",
          "000000000000"
        ]
      },
      {
        "input": [
          "00000200000",
          "00000000040",
          "00000000000",
          "00000000000",
          "00600000006",
          "00000000000",
          "00000000040",
          "00000200000"
        ],
        "output": [
          "00000200000",
          "00000200040",
          "00000200040",
          "00000200040",
          "00666966696",
          "00000200040",
          "00000200040",
          "00000200000"
        ]
      }
    ],
    "test": [
      {
        "input": [
          "0000005000000",
          "0000000000000",
          "0300000000030",
          "0000000000000",
          "0000000000000",
          "0007000000700",
          "0000000000000",
          "0000000000000",
          "0000005000000"
        ],
        "output": [
          "0000005000000",
          "0000005000000",
          "0333339333330",
          "0000005000000",
          "0000005000000",
          "0007779777700",
          "0000005000000",
          "0000005000000",
          "0000005000000"
        ]
      }
    ]
  },
  {
    "id": "M153",
    "title": "Histogram of Component Colors",
    "difficulty": "medium",
    "skills": [
      "component counting",
      "color grouping",
      "structured output"
    ],
    "suggested_staged_path": "Do not count cells; count disconnected components for each color. Then build one output row per present color, ordered from smallest color to largest.",
    "written_solution": "Count how many connected components exist for each nonzero color. Sort the colors in ascending order. For each color, output a row containing that color repeated once per component, padded on the right with zeros to the maximum row length.",
    "program_name": "rule_m153",
    "program_source": "def rule_m153(g):\n    counts=collections.Counter()\n    h,w=size(g)\n    # Count connected components per color\n    seen=set()\n    for r in range(h):\n        for c in range(w):\n            v=g[r][c]\n            if v==0 or (r,c) in seen:\n                continue\n            q=[(r,c)]; seen.add((r,c)); cells=[]\n            while q:\n                rr,cc=q.pop(); cells.append((rr,cc))\n                for dr,dc in DIR4:\n                    nr,nc=rr+dr,cc+dc\n                    if 0<=nr<h and 0<=nc<w and (nr,nc) not in seen and g[nr][nc]==v:\n                        seen.add((nr,nc)); q.append((nr,nc))\n            counts[v]+=1\n    colors=sorted(counts)\n    width=max(counts.values()) if counts else 1\n    out=blank(len(colors), width, 0)\n    for r,color in enumerate(colors):\n        for c in range(counts[color]):\n            out[r][c]=color\n    return out\n",
    "train": [
      {
        "input": [
          "00000000000",
          "02002000000",
          "00000000000",
          "00330000000",
          "00000000000",
          "00000003000",
          "00000000044",
          "00000000040"
        ],
        "output": [
          "22",
          "33",
          "40"
        ]
      },
      {
        "input": [
          "0000000000",
          "0550005000",
          "0000000000",
          "0000000000",
          "0020000000",
          "0000000000",
          "0000020000",
          "0000000020",
          "0000000000"
        ],
        "output": [
          "222",
          "550"
        ]
      },
      {
        "input": [
          "000000000000",
          "060000004400",
          "000000004000",
          "000600000000",
          "000000000000",
          "000006000000",
          "000000000000",
          "000000000400",
          "000000000000",
          "000000000000"
        ],
        "output": [
          "440",
          "666"
        ]
      },
      {
        "input": [
          "00000000000",
          "00000000000",
          "00700007700",
          "00000000000",
          "00000000000",
          "03000300030",
          "00000000000",
          "00000000000",
          "00000000000"
        ],
        "output": [
          "333",
          "770"
        ]
      }
    ],
    "test": [
      {
        "input": [
          "0000000000",
          "0200020020",
          "0000000000",
          "0000000000",
          "0044000000",
          "0000000000",
          "0000005000",
          "0000000000",
          "0000000000",
          "0000000000"
        ],
        "output": [
          "222",
          "400",
          "500"
        ]
      }
    ]
  },
  {
    "id": "M154",
    "title": "Copy the Template into the Matching Frame",
    "difficulty": "medium",
    "skills": [
      "template extraction",
      "frame detection",
      "size matching"
    ],
    "suggested_staged_path": "First isolate the multicolor template and measure its cropped size. Then scan the empty frames and choose the one whose interior has exactly the same height and width.",
    "written_solution": "Crop the non-frame template tightly. Among the empty rectangular frames, exactly one has an interior whose size matches the template. Copy the template into that frame's interior, aligned to the interior's top-left corner, and leave everything else unchanged.",
    "program_name": "rule_m154",
    "program_source": "def rule_m154(g):\n    out=clone(g)\n    # template: all nonzero non-8 cells\n    temp_cells=[(r,c) for r,row in enumerate(g) for c,v in enumerate(row) if v not in (0,8)]\n    temp=crop_bbox(g, cells=temp_cells, ignore=set())\n    th,tw=size(temp)\n    for r0,c0,r1,c1 in find_rect_frames(g, color=8):\n        ih,iw=r1-r0-1,c1-c0-1\n        if (ih,iw)==(th,tw):\n            for r in range(th):\n                for c in range(tw):\n                    if temp[r][c]!=0:\n                        out[r0+1+r][c0+1+c]=temp[r][c]\n            break\n    return out\n",
    "train": [
      {
        "input": [
          "00000000000000",
          "02300000888880",
          "02030000800080",
          "00000000800080",
          "00000000888880",
          "00000008888800",
          "00000008000800",
          "00000008000800",
          "00000008000800",
          "00000008888800"
        ],
        "output": [
          "00000000000000",
          "02300000888880",
          "02030000800080",
          "00000000800080",
          "00000000888880",
          "00000008888800",
          "00000008000800",
          "00000008000800",
          "00000008000800",
          "00000008888800"
        ]
      },
      {
        "input": [
          "000000000000000",
          "000000000888880",
          "045000000800080",
          "040500000800080",
          "044400000800080",
          "000000000888880",
          "000000008888800",
          "000000008000800",
          "000000008000800",
          "000000008888800",
          "000000000000000"
        ],
        "output": [
          "000000000000000",
          "000000000888880",
          "045000000800080",
          "040500000800080",
          "044400000800080",
          "000000000888880",
          "000000008888800",
          "000000008000800",
          "000000008000800",
          "000000008888800",
          "000000000000000"
        ]
      },
      {
        "input": [
          "00000000000000",
          "00000000888800",
          "00000000800800",
          "00000000800800",
          "00000000888800",
          "00000000888880",
          "06700000800080",
          "06070000800080",
          "00000000800080",
          "00000000888880"
        ],
        "output": [
          "00000000000000",
          "00000000888800",
          "00000000800800",
          "00000000800800",
          "00000000888800",
          "00000000888880",
          "06700000800080",
          "06070000800080",
          "00000000800080",
          "00000000888880"
        ]
      },
      {
        "input": [
          "0000000000000000",
          "0000000000888880",
          "0280000000800080",
          "0282000000800080",
          "0220000000800080",
          "0000000000888880",
          "0000000008888800",
          "0000000008000800",
          "0000000008000800",
          "0000000008888800",
          "0000000000000000",
          "0000000000000000"
        ],
        "output": [
          "0000000000000000",
          "0000000000888880",
          "0280000000800080",
          "0282000000800080",
          "0220000000800080",
          "0000000000888880",
          "0000000008888800",
          "0000000008000800",
          "0000000008000800",
          "0000000008888800",
          "0000000000000000",
          "0000000000000000"
        ]
      }
    ],
    "test": [
      {
        "input": [
          "000000000000000",
          "000000000888880",
          "000000000800080",
          "000000000800080",
          "000000000800080",
          "000000000888880",
          "034000000888888",
          "030400000800008",
          "004400000800008",
          "000000000800008",
          "000000000888888"
        ],
        "output": [
          "000000000000000",
          "000000000888880",
          "000000000800080",
          "000000000800080",
          "000000000800080",
          "000000000888880",
          "034000000888888",
          "030400000800008",
          "004400000800008",
          "000000000800008",
          "000000000888888"
        ]
      }
    ]
  },
  {
    "id": "H148",
    "title": "Transform Analogy Across Panels",
    "difficulty": "hard",
    "skills": [
      "panel parsing",
      "transform inference",
      "analogy transfer"
    ],
    "suggested_staged_path": "Split the input into the three separator-defined panels. Infer which geometric transform turns panel A into panel B, then apply that same transform to panel C.",
    "written_solution": "The first two panels show an example transform: panel B is panel A after a rotation or reflection. Detect which transform was used by comparing the cropped nonzero shapes in those panels, then apply that transform to the cropped shape in panel C and output the result.",
    "program_name": "rule_h148",
    "program_source": "def rule_h148(g):\n    panels=split_panels_by_sep(g, sep=9)\n    a,b,c=panels\n    code=detect_transform(a,b)\n    return apply_transform(crop_bbox(c), code)\n",
    "train": [
      {
        "input": [
          "00000922000900000",
          "02300903000904400",
          "02030930000904040",
          "00000900000900000",
          "00000900000900000"
        ],
        "output": [
          "44",
          "04",
          "40"
        ]
      },
      {
        "input": [
          "00000906500900000",
          "56000960500907700",
          "50600900500907070",
          "50000900000900000",
          "00000900000900000"
        ],
        "output": [
          "077",
          "707"
        ]
      },
      {
        "input": [
          "03400904400900000",
          "03040940400966000",
          "00440933000906000",
          "00000900000900000",
          "00000900000900000"
        ],
        "output": [
          "66",
          "60"
        ]
      },
      {
        "input": [
          "00000902200904500",
          "02800920200904050",
          "02020908200900000",
          "02200900000900000",
          "00000900000900000"
        ],
        "output": [
          "504",
          "054"
        ]
      }
    ],
    "test": [
      {
        "input": [
          "00000966000900000",
          "06700907000903300",
          "06070970000903030",
          "00000900000903000",
          "00000900000900000"
        ],
        "output": [
          "333",
          "003",
          "030"
        ]
      }
    ]
  },
  {
    "id": "H149",
    "title": "Recolor Nested Frames by Depth",
    "difficulty": "hard",
    "skills": [
      "nested-object reasoning",
      "area ranking",
      "depth encoding"
    ],
    "suggested_staged_path": "Treat each rectangular border as a separate object and order them from outside to inside. Once the nesting order is clear, recolor by depth.",
    "written_solution": "The grid contains several nested rectangular borders, all initially in color 1. Sort those frame borders by decreasing bounding-box area so the outermost frame comes first. Recolor the outermost frame to 2, the next one to 3, then 4, and so on inward.",
    "program_name": "rule_h149",
    "program_source": "def rule_h149(g):\n    comps=components_of_color(g, 1)\n    ordered=sorted(comps, key=lambda cells: ((bbox(cells)[2]-bbox(cells)[0]+1)*(bbox(cells)[3]-bbox(cells)[1]+1)), reverse=True)\n    out=blank(*size(g),0)\n    for idx,cells in enumerate(ordered, start=2):\n        for r,c in cells:\n            out[r][c]=idx\n    return out\n",
    "train": [
      {
        "input": [
          "00000000000",
          "01111111110",
          "01000000010",
          "01011111010",
          "01010001010",
          "01010101010",
          "01010001010",
          "01011111010",
          "01000000010",
          "01111111110",
          "00000000000"
        ],
        "output": [
          "00000000000",
          "02222222220",
          "02000000020",
          "02033333020",
          "02030003020",
          "02030403020",
          "02030003020",
          "02033333020",
          "02000000020",
          "02222222220",
          "00000000000"
        ]
      },
      {
        "input": [
          "0000000000000",
          "0111111111110",
          "0100000000010",
          "0101111111010",
          "0101000001010",
          "0101011101010",
          "0101010101010",
          "0101011101010",
          "0101000001010",
          "0101111111010",
          "0100000000010",
          "0111111111110",
          "0000000000000"
        ],
        "output": [
          "0000000000000",
          "0222222222220",
          "0200000000020",
          "0203333333020",
          "0203000003020",
          "0203044403020",
          "0203040403020",
          "0203044403020",
          "0203000003020",
          "0203333333020",
          "0200000000020",
          "0222222222220",
          "0000000000000"
        ]
      },
      {
        "input": [
          "00000000000000",
          "00111111111100",
          "00100000000100",
          "00101111110100",
          "00101000010100",
          "00101000010100",
          "00101000010100",
          "00101000010100",
          "00101111110100",
          "00100000000100",
          "00111111111100",
          "00000000000000"
        ],
        "output": [
          "00000000000000",
          "00222222222200",
          "00200000000200",
          "00203333330200",
          "00203000030200",
          "00203000030200",
          "00203000030200",
          "00203000030200",
          "00203333330200",
          "00200000000200",
          "00222222222200",
          "00000000000000"
        ]
      },
      {
        "input": [
          "000000000000000",
          "011111111111110",
          "010000000000010",
          "010111111111010",
          "010100000001010",
          "010101111101010",
          "010101000101010",
          "010101010101010",
          "010101000101010",
          "010101111101010",
          "010100000001010",
          "010111111111010",
          "010000000000010",
          "011111111111110",
          "000000000000000"
        ],
        "output": [
          "000000000000000",
          "022222222222220",
          "020000000000020",
          "020333333333020",
          "020300000003020",
          "020304444403020",
          "020304000403020",
          "020304050403020",
          "020304000403020",
          "020304444403020",
          "020300000003020",
          "020333333333020",
          "020000000000020",
          "022222222222220",
          "000000000000000"
        ]
      }
    ],
    "test": [
      {
        "input": [
          "000000000000000",
          "001111111111100",
          "001000000000100",
          "001011111110100",
          "001010000010100",
          "001010111010100",
          "001010101010100",
          "001010111010100",
          "001010000010100",
          "001011111110100",
          "001000000000100",
          "001111111111100",
          "000000000000000"
        ],
        "output": [
          "000000000000000",
          "002222222222200",
          "002000000000200",
          "002033333330200",
          "002030000030200",
          "002030444030200",
          "002030404030200",
          "002030444030200",
          "002030000030200",
          "002033333330200",
          "002000000000200",
          "002222222222200",
          "000000000000000"
        ]
      }
    ]
  },
  {
    "id": "H150",
    "title": "Voronoi Fill Inside the Frame",
    "difficulty": "hard",
    "skills": [
      "distance reasoning",
      "tie handling",
      "region partitioning"
    ],
    "suggested_staged_path": "Leave the wall cells alone and reason only about the interior. For each empty interior cell, compare its Manhattan distance to the seeds and handle ties explicitly.",
    "written_solution": "The boundary color 5 forms a closed frame. Interior zeros are assigned to the nearest seed by Manhattan distance. If a cell is tied between two or more seeds, color it 8. Keep the seeds and the frame as they are.",
    "program_name": "rule_h150",
    "program_source": "def rule_h150(g):\n    h,w=size(g)\n    out=clone(g)\n    seeds=[(r,c,v) for r,row in enumerate(g) for c,v in enumerate(row) if v not in (0,5)]\n    for r in range(h):\n        for c in range(w):\n            if g[r][c]!=0:\n                continue\n            best=min(abs(sr-r)+abs(sc-c) for sr,sc,_ in seeds)\n            colors=[v for sr,sc,v in seeds if abs(sr-r)+abs(sc-c)==best]\n            out[r][c]=colors[0] if len(colors)==1 else 8\n    return out\n",
    "train": [
      {
        "input": [
          "555555555",
          "500000005",
          "502000405",
          "500000005",
          "500000005",
          "500000005",
          "500070005",
          "500000005",
          "555555555"
        ],
        "output": [
          "555555555",
          "522284445",
          "522284445",
          "522284445",
          "522878445",
          "588777885",
          "577777775",
          "577777775",
          "555555555"
        ]
      },
      {
        "input": [
          "55555555555",
          "50000000005",
          "50300000605",
          "50000000005",
          "50000000005",
          "50000000005",
          "50000000005",
          "50000200005",
          "50000000005",
          "55555555555"
        ],
        "output": [
          "55555555555",
          "53333866665",
          "53333866665",
          "53333866665",
          "53338286665",
          "53382228665",
          "58822222885",
          "52222222225",
          "52222222225",
          "55555555555"
        ]
      },
      {
        "input": [
          "55555555555",
          "50000000005",
          "50000000005",
          "50040007005",
          "50000000005",
          "50000000005",
          "50000000005",
          "50020006005",
          "50000000005",
          "50000000005",
          "55555555555"
        ],
        "output": [
          "55555555555",
          "54444877775",
          "54444877775",
          "54444877775",
          "54444877775",
          "58888888885",
          "52222866665",
          "52222866665",
          "52222866665",
          "52222866665",
          "55555555555"
        ]
      },
      {
        "input": [
          "555555555555",
          "500000000005",
          "500300002005",
          "500000000005",
          "500000000005",
          "500000000005",
          "500004000005",
          "500000000005",
          "555555555555"
        ],
        "output": [
          "555555555555",
          "533333222225",
          "533333222225",
          "533338222225",
          "533384422225",
          "588844442225",
          "544444444445",
          "544444444445",
          "555555555555"
        ]
      }
    ],
    "test": [
      {
        "input": [
          "5555555555",
          "5000000005",
          "5020000605",
          "5000000005",
          "5000000005",
          "5000000005",
          "5000000005",
          "5000400005",
          "5000000005",
          "5555555555"
        ],
        "output": [
          "5555555555",
          "5222266665",
          "5222266665",
          "5222266665",
          "5222486665",
          "5224448665",
          "5444444885",
          "5444444445",
          "5444444445",
          "5555555555"
        ]
      }
    ]
  },
  {
    "id": "H151",
    "title": "Dihedral Equality Matrix",
    "difficulty": "hard",
    "skills": [
      "shape normalization",
      "rotation/flip equivalence",
      "matrix output"
    ],
    "suggested_staged_path": "First split the input into its separate objects and ignore their colors. For each object, compute its shape up to rotation and reflection, then compare every pair.",
    "written_solution": "Each disconnected object is one shape. Two shapes count as equal if one can be rotated or reflected to match the other. Order the objects by their top-left positions and output a square matrix with 2 where a pair of shapes is dihedrally equivalent and 0 otherwise.",
    "program_name": "rule_h151",
    "program_source": "def rule_h151(g):\n    comps=sorted(components(g, ignore={0}, color_sensitive=False), key=lambda comp: bbox(comp[\"cells\"])[:2])\n    shape_sets=[all_dihedral_shapes(crop_bbox(g, cells=comp[\"cells\"], ignore=set())) for comp in comps]\n    n=len(shape_sets)\n    out=blank(n,n,0)\n    for i in range(n):\n        for j in range(n):\n            out[i][j]=2 if shape_sets[i] & shape_sets[j] else 0\n    return out\n",
    "train": [
      {
        "input": [
          "000000000000000",
          "022000200003330",
          "020000220000300",
          "000000000000000",
          "000000000000000",
          "000000000000000",
          "000000000000000"
        ],
        "output": [
          "220",
          "220",
          "002"
        ]
      },
      {
        "input": [
          "00000000000000000",
          "00000000040000000",
          "04400000440005500",
          "00440000000005000",
          "00000000000005000",
          "00000000000000000",
          "00000000000000000",
          "00000000000000000"
        ],
        "output": [
          "200",
          "020",
          "002"
        ]
      },
      {
        "input": [
          "000000000000000000",
          "000000000000077000",
          "066000006000007000",
          "006000066000000000",
          "000000000000000000",
          "000000000000000000",
          "000000000000000000",
          "000000000000000000",
          "000000000000000000"
        ],
        "output": [
          "222",
          "222",
          "222"
        ]
      },
      {
        "input": [
          "0000000000000000",
          "0280000000003300",
          "0220000022003000",
          "0000000082000000",
          "0000000000000000",
          "0000000000000000",
          "0000000000000000",
          "0000000000000000"
        ],
        "output": [
          "202",
          "020",
          "202"
        ]
      }
    ],
    "test": [
      {
        "input": [
          "00000000000000000",
          "04500000000006600",
          "04450005440000600",
          "00000004500000000",
          "00000000000000000",
          "00000000000000000",
          "00000000000000000",
          "00000000000000000"
        ],
        "output": [
          "202",
          "020",
          "202"
        ]
      }
    ]
  },
  {
    "id": "H152",
    "title": "Overlap Count of Multiple Spans",
    "difficulty": "hard",
    "skills": [
      "multi-span reasoning",
      "coverage counting",
      "special-case overlap colors"
    ],
    "suggested_staged_path": "Recover every axis-aligned span first, exactly as in the easier span task. Then ignore the individual colors and count how many spans cover each cell.",
    "written_solution": "Each repeated color defines one horizontal or vertical span between its two markers. Count, for every cell, how many of these spans pass through it. Cells covered by exactly two spans become 8, cells covered by three or more spans become 9, and all other cells stay 0.",
    "program_name": "rule_h152",
    "program_source": "def rule_h152(g):\n    h,w=size(g)\n    by_color=collections.defaultdict(list)\n    for r,row in enumerate(g):\n        for c,v in enumerate(row):\n            if v!=0:\n                by_color[v].append((r,c))\n    cover=collections.Counter()\n    for color,pts in by_color.items():\n        for cell in span_markers(pts):\n            cover[cell]+=1\n    out=blank(h,w,0)\n    for (r,c), n in cover.items():\n        if n==2:\n            out[r][c]=8\n        elif n>=3:\n            out[r][c]=9\n    return out\n",
    "train": [
      {
        "input": [
          "00000400000",
          "02000000020",
          "00000000000",
          "00000000000",
          "00600000600",
          "00000000000",
          "00000000000",
          "00000000000",
          "00000400000"
        ],
        "output": [
          "00000000000",
          "00000800000",
          "00000000000",
          "00000000000",
          "00000800000",
          "00000000000",
          "00000000000",
          "00000000000",
          "00000000000"
        ]
      },
      {
        "input": [
          "0000000000",
          "0000000000",
          "0300000700",
          "0000000000",
          "0000000000",
          "5000000005",
          "0000000000",
          "0000000000",
          "0300000700",
          "0000000000"
        ],
        "output": [
          "0000000000",
          "0000000000",
          "0000000000",
          "0000000000",
          "0000000000",
          "0800000800",
          "0000000000",
          "0000000000",
          "0000000000",
          "0000000000"
        ]
      },
      {
        "input": [
          "0000004000000",
          "0006000000000",
          "0000000000000",
          "0020000000200",
          "0000000000000",
          "0700000000070",
          "0000000000000",
          "0006000000000",
          "0000004000000"
        ],
        "output": [
          "0000000000000",
          "0000000000000",
          "0000000000000",
          "0008008000000",
          "0000000000000",
          "0008008000000",
          "0000000000000",
          "0000000000000",
          "0000000000000"
        ]
      },
      {
        "input": [
          "00000000000",
          "03000400000",
          "00000000700",
          "00000000000",
          "00000000000",
          "60000000006",
          "00000000000",
          "00000000000",
          "00000000700",
          "03000400000",
          "00000000000"
        ],
        "output": [
          "00000000000",
          "00000000000",
          "00000000000",
          "00000000000",
          "00000000000",
          "08000800800",
          "00000000000",
          "00000000000",
          "00000000000",
          "00000000000",
          "00000000000"
        ]
      }
    ],
    "test": [
      {
        "input": [
          "000000400000",
          "000070000000",
          "020000000020",
          "000000000000",
          "000000000000",
          "006000000600",
          "000000000000",
          "000000000000",
          "000070000000",
          "000000400000"
        ],
        "output": [
          "000000000000",
          "000000000000",
          "000080800000",
          "000000000000",
          "000000000000",
          "000080800000",
          "000000000000",
          "000000000000",
          "000000000000",
          "000000000000"
        ]
      }
    ]
  },
  {
    "id": "H153",
    "title": "Transfer a Color Mapping",
    "difficulty": "hard",
    "skills": [
      "palette inference",
      "panel analogy",
      "recoloring"
    ],
    "suggested_staged_path": "Use the first two panels only to infer a color-to-color mapping. Once that mapping is known, apply it to the third panel's cropped motif.",
    "written_solution": "Panels A and B have the same shape layout, but B recolors A by a consistent palette mapping. Infer that mapping from corresponding nonzero cells, then apply the same color substitution to panel C's cropped pattern and output the recolored crop.",
    "program_name": "rule_h153",
    "program_source": "def rule_h153(g):\n    panels=split_panels_by_sep(g, sep=9)\n    a,b,c=panels\n    # derive color map from overlapping nonzero cells in cropped panels? better use full panels same size\n    mapping={}\n    for r in range(len(a)):\n        for col in range(len(a[0])):\n            va=a[r][col]; vb=b[r][col]\n            if va!=0:\n                mapping[va]=vb\n    out=crop_bbox(c)\n    for r,row in enumerate(out):\n        for col,v in enumerate(row):\n            if v!=0:\n                out[r][col]=mapping[v]\n    return out\n",
    "train": [
      {
        "input": [
          "00000900000900000",
          "02300904700903200",
          "02030904070903020",
          "00000900000900000",
          "00000900000900000"
        ],
        "output": [
          "740",
          "704"
        ]
      },
      {
        "input": [
          "00000900000900000",
          "45000962000905400",
          "40500960200900050",
          "04400906600900000",
          "00000900000900000"
        ],
        "output": [
          "260",
          "002"
        ]
      },
      {
        "input": [
          "00000900000907600",
          "06700903800907070",
          "06070903080900000",
          "00000900000900000",
          "00000900000900000"
        ],
        "output": [
          "830",
          "808"
        ]
      },
      {
        "input": [
          "00000900000900000",
          "02800905400982000",
          "02020905050928200",
          "02200905500900000",
          "00000900000900000"
        ],
        "output": [
          "450",
          "545"
        ]
      }
    ],
    "test": [
      {
        "input": [
          "00000900000900000",
          "03400907200904300",
          "03040907020904040",
          "00440900220900000",
          "00000900000900000"
        ],
        "output": [
          "270",
          "202"
        ]
      }
    ]
  },
  {
    "id": "H154",
    "title": "Compose Two Transform Commands",
    "difficulty": "hard",
    "skills": [
      "command composition",
      "geometric transforms",
      "cropped output"
    ],
    "suggested_staged_path": "Treat the two command cells as an ordered sequence rather than a single code. Crop the motif, apply the first transform, then apply the second to the result.",
    "written_solution": "The two command values on the top row specify two geometric transforms in order. Crop the motif below them, apply the first transform, then apply the second. Commands use the same code system as the single-command rotation task, extended with 5 for horizontal flip and 6 for vertical flip.",
    "program_name": "rule_h154",
    "program_source": "def rule_h154(g):\n    code1,code2=[v for v in g[0] if v!=0][:2]\n    motif=[row[:] for row in g[1:]]\n    motif=crop_bbox(motif)\n    return apply_transform(apply_transform(motif, code1), code2)\n",
    "train": [
      {
        "input": [
          "250000000",
          "000000000",
          "000000000",
          "000023000",
          "000020300"
        ],
        "output": [
          "22",
          "30",
          "03"
        ]
      },
      {
        "input": [
          "4300000000",
          "0000000000",
          "0000045000",
          "0000004500",
          "0000000500"
        ],
        "output": [
          "004",
          "045",
          "550"
        ]
      },
      {
        "input": [
          "520000000",
          "000000000",
          "000000000",
          "000000000",
          "006700000",
          "006070000"
        ],
        "output": [
          "70",
          "07",
          "66"
        ]
      },
      {
        "input": [
          "34000000000",
          "00000000000",
          "00000000000",
          "00000028000",
          "00000028200",
          "00000022000"
        ],
        "output": [
          "222",
          "288",
          "020"
        ]
      }
    ],
    "test": [
      {
        "input": [
          "2600000000",
          "0000000000",
          "0000000000",
          "0003400000",
          "0003040000",
          "0000440000"
        ],
        "output": [
          "440",
          "404",
          "033"
        ]
      }
    ]
  }
]''')

def validate():
    details = []
    ok = True
    pair_total = 0
    train_total = 0
    for puzzle in PUZZLES:
        pid = puzzle["id"]
        fn = RULES[pid]
        puzzle_ok = True
        for split_name in ("train", "test"):
            if split_name == "train":
                train_total += len(puzzle["train"])
            for idx, pair in enumerate(puzzle[split_name], start=1):
                pair_total += 1
                got = to_strings(fn(from_strings(pair["input"])))
                exp = pair["output"]
                if got != exp:
                    ok = False
                    puzzle_ok = False
                    details.append({
                        "id": pid,
                        "split": split_name,
                        "index": idx,
                        "expected": exp,
                        "got": got,
                    })
        if puzzle_ok:
            details.append({"id": pid, "status": "ok"})
    return {
        "status": "ok" if ok else "error",
        "puzzles": len(PUZZLES),
        "train_pairs": train_total,
        "total_pairs": pair_total,
        "details": details,
    }

if __name__ == "__main__":
    result = validate()
    print(json.dumps(result, indent=2))
