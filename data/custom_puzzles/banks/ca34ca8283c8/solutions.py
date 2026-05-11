"""
ARC Additional Puzzle Bank — Set 21

Contains 21 reference puzzles:
  E141–E147, M141–M147, H141–H147

Run this file directly to validate the listed train/test pairs against the
reference rule functions.
"""

from __future__ import annotations
from collections import Counter, defaultdict, deque
import json

DIR4 = [(-1,0),(1,0),(0,-1),(0,1)]
DIR8 = DIR4 + [(-1,-1),(-1,1),(1,-1),(1,1)]

def blank(h,w,val=0):
    return [[val]*w for _ in range(h)]


def clone(g):
    return [row[:] for row in g]


def size(g):
    return (len(g), len(g[0]) if g else 0)


def to_strings(g):
    return ["".join(str(x) for x in row) for row in g]


def from_strings(lines):
    return [[int(ch) for ch in line] for line in lines]


def inb(g,r,c):
    h,w=size(g)
    return 0<=r<h and 0<=c<w


def paint_cells(g, cells, val=None):
    for item in cells:
        if val is None:
            r,c,v=item
        else:
            r,c=item; v=val
        if 0<=r<len(g) and 0<=c<len(g[0]):
            g[r][c]=v
    return g


def draw_hline(g, r, c0, c1, v):
    if c0>c1: c0,c1=c1,c0
    for c in range(c0,c1+1):
        if inb(g,r,c): g[r][c]=v


def draw_vline(g, c, r0, r1, v):
    if r0>r1: r0,r1=r1,r0
    for r in range(r0,r1+1):
        if inb(g,r,c): g[r][c]=v


def draw_rect_border(g, r0,c0,r1,c1,v):
    draw_hline(g,r0,c0,c1,v); draw_hline(g,r1,c0,c1,v)
    draw_vline(g,c0,r0,r1,v); draw_vline(g,c1,r0,r1,v)


def fill_rect(g, r0,c0,r1,c1,v):
    if r0>r1: r0,r1=r1,r0
    if c0>c1: c0,c1=c1,c0
    for r in range(r0,r1+1):
        for c in range(c0,c1+1):
            if inb(g,r,c): g[r][c]=v


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


def components(g, ignore={0}, color_sensitive=True, dirs=DIR4):
    h,w=size(g)
    seen=set()
    comps=[]
    for r in range(h):
        for c in range(w):
            v=g[r][c]
            if v in ignore or (r,c) in seen:
                continue
            q=deque([(r,c)])
            seen.add((r,c))
            cells=[]
            while q:
                rr,cc=q.popleft()
                cells.append((rr,cc))
                for dr,dc in dirs:
                    nr,nc=rr+dr,cc+dc
                    if 0<=nr<h and 0<=nc<w and (nr,nc) not in seen:
                        if color_sensitive:
                            cond=g[nr][nc]==v
                        else:
                            cond=g[nr][nc] not in ignore
                        if cond:
                            seen.add((nr,nc)); q.append((nr,nc))
            comps.append({"color":v,"cells":cells})
    return comps


def rotate90(g):
    h,w=size(g)
    return [[g[h-1-r][c] for r in range(h)] for c in range(w)]


def rotate180(g):
    return [row[::-1] for row in g[::-1]]


def rotate270(g):
    return rotate90(rotate180(g))


def flip_h(g):
    return [row[::-1] for row in g]


def flip_v(g):
    return g[::-1]


def transpose(g):
    h,w=size(g)
    return [[g[r][c] for r in range(h)] for c in range(w)]


TRANSFORMS = {
    1: lambda g: [row[:] for row in g],
    2: rotate90,
    3: rotate180,
    4: rotate270,
    5: flip_h,
    6: flip_v,
    7: transpose,
}


def apply_transform(g, code):
    return TRANSFORMS[code](g)


def manhattan(a,b):
    return abs(a[0]-b[0])+abs(a[1]-b[1])


def phase_weave(anchor, directions, palette, h, w, mask=None, include_anchor=False):
    out=[]
    if include_anchor:
        out.append((anchor[0],anchor[1],palette[0]))
    for dr,dc in directions:
        step=1
        r,c=anchor[0]+dr, anchor[1]+dc
        while 0<=r<h and 0<=c<w and (mask is None or (r,c) in mask):
            out.append((r,c,palette[(step-1)%len(palette)]))
            step+=1
            r+=dr; c+=dc
    return out


def hole_count_component(comp_cells):
    # count enclosed zero regions inside bbox of component
    r0,c0,r1,c1=bbox(comp_cells)
    H,W=r1-r0+3,c1-c0+3
    occ={(r-r0+1,c-c0+1) for r,c in comp_cells}
    seen=set()
    holes=0
    for r in range(H):
        for c in range(W):
            if (r,c) in seen or (r,c) in occ:
                continue
            q=deque([(r,c)]); seen.add((r,c))
            reaches_border=False
            while q:
                rr,cc=q.popleft()
                if rr in (0,H-1) or cc in (0,W-1):
                    reaches_border=True
                for dr,dc in DIR4:
                    nr,nc=rr+dr,cc+dc
                    if 0<=nr<H and 0<=nc<W and (nr,nc) not in seen and (nr,nc) not in occ:
                        seen.add((nr,nc)); q.append((nr,nc))
            if not reaches_border:
                holes+=1
    return holes


def hconcat(panels, sep=1, val=0):
    h=max(len(p) for p in panels)
    ws=[len(p[0]) for p in panels]
    out=blank(h, sum(ws)+sep*(len(panels)-1), val)
    x=0
    for p in panels:
        ph,pw=size(p)
        for r in range(ph):
            for c in range(pw):
                out[r][x+c]=p[r][c]
        x += pw + sep
    return out


def vconcat(panels, sep=1, val=0):
    w=max(len(p[0]) for p in panels)
    hs=[len(p) for p in panels]
    out=blank(sum(hs)+sep*(len(panels)-1), w, val)
    y=0
    for p in panels:
        ph,pw=size(p)
        for r in range(ph):
            for c in range(pw):
                out[y+r][c]=p[r][c]
        y += ph + sep
    return out


def all_zero_cols(g):
    h,w=size(g)
    return [c for c in range(w) if all(g[r][c]==0 for r in range(h))]


def split_by_zero_cols(g):
    h,w=size(g)
    zero_cols = set(all_zero_cols(g))
    parts=[]
    start=None
    for c in range(w):
        if c not in zero_cols and start is None:
            start=c
        if start is not None and (c==w-1 or (c+1) in zero_cols):
            end=c
            parts.append([row[start:end+1] for row in g])
            start=None
    return parts


def panel_pad(panel, h=5, w=5, top=0,left=0):
    out=blank(h,w,0)
    ph,pw=size(panel)
    for r in range(ph):
        for c in range(pw):
            out[top+r][left+c]=panel[r][c]
    return out


def nonzero_cells(g, ignore={0}):
    return [(r,c) for r,row in enumerate(g) for c,v in enumerate(row) if v not in ignore]


def normalize_component(comp):
    cells=comp["cells"]
    r0,c0,r1,c1=bbox(cells)
    out=blank(r1-r0+1, c1-c0+1, 0)
    for r,c in cells:
        out[r-r0][c-c0]=comp["color"]
    return out


def sort_comps_left_to_right(comps):
    return sorted(comps, key=lambda comp: min(c for r,c in comp["cells"]))


def chamber_from_seed(g, seed, wall=1):
    h,w=size(g)
    q=deque([seed]); seen={seed}
    while q:
        r,c=q.popleft()
        for dr,dc in DIR4:
            nr,nc=r+dr,c+dc
            if 0<=nr<h and 0<=nc<w and (nr,nc) not in seen and g[nr][nc]!=wall:
                seen.add((nr,nc)); q.append((nr,nc))
    return seen


def strip_zero_border(g):
    return crop_bbox(g)


def eq_grid(a,b):
    return to_strings(a)==to_strings(b)


def l_path(a,b):
    (r0,c0),(r1,c1)=a,b
    cells=[]
    step=1 if c1>=c0 else -1
    for c in range(c0,c1+step,step):
        cells.append((r0,c))
    step=1 if r1>=r0 else -1
    for r in range(r0+step,r1+step,step):
        cells.append((r,c1))
    return cells


def rule_e141(g):
    h,w=size(g)
    palette=[v for v in g[0] if v!=0][:2]
    sr=sc=None
    for r in range(1,h):
        for c in range(w):
            if g[r][c]==9:
                sr,sc=r,c
    out=clone(g)
    for r,c,v in phase_weave((sr,sc), DIR4, palette, h,w):
        if out[r][c]==0:
            out[r][c]=v
    return out


def rule_e142(g):
    h,w=size(g)
    out=clone(g)
    for r in range(h):
        row=g[r]
        for color in sorted(set(row)-{0}):
            pos=[c for c,v in enumerate(row) if v==color]
            if len(pos)==2:
                for c in range(min(pos), max(pos)+1):
                    out[r][c]=color
    return out


def rule_e143(g):
    h,w=size(g)
    guide=None
    for r,row in enumerate(g):
        vals=set(row)
        if len(vals)==1 and 0 not in vals:
            guide=r; break
    out=clone(g)
    for r in range(guide):
        rr=2*guide-r
        if rr<h:
            for c,v in enumerate(g[r]):
                if v!=0:
                    out[rr][c]=v
    return out


def rule_e144(g):
    return crop_bbox(g)


def rule_e145(g):
    out=clone(g)
    by=defaultdict(list)
    for r,row in enumerate(g):
        for c,v in enumerate(row):
            if v!=0:
                by[v].append((r,c))
    for color,cells in by.items():
        if len(cells)==3:
            r0,c0,r1,c1=bbox(cells)
            corners={(r0,c0),(r0,c1),(r1,c0),(r1,c1)}
            missing=list(corners-set(cells))
            if len(missing)==1:
                r,c=missing[0]
                out[r][c]=color
    return out


def rule_e146(g):
    h,w=size(g)
    out=clone(g)
    cmd=None
    seed=None
    for r,row in enumerate(g):
        for c,v in enumerate(row):
            if v in {1,2,3,4}:
                cmd=(r,c,v)
            elif v!=0:
                seed=(r,c,v)
    sr,sc,color=seed
    code=cmd[2]
    drdc={1:(-1,0),2:(1,0),3:(0,-1),4:(0,1)}[code]
    r,c=sr+drdc[0], sc+drdc[1]
    while 0<=r<h and 0<=c<w:
        if out[r][c]==0:
            out[r][c]=color
        r+=drdc[0]; c+=drdc[1]
    return out


def rule_e147(g):
    comps=components(g)
    best=max(comps, key=lambda comp:(len(comp["cells"]), -min(r for r,c in comp["cells"]), -min(c for r,c in comp["cells"])))
    out=blank(*size(g),0)
    for r,c in best["cells"]:
        out[r][c]=best["color"]
    return out


def rule_m141(g):
    h,w=size(g)
    palette=[v for v in g[0] if v!=0][:2]
    seed=None
    for r in range(h):
        for c in range(w):
            if g[r][c]==9:
                seed=(r,c)
    mask=chamber_from_seed(g, seed, wall=1)
    out=clone(g)
    for r,c,v in phase_weave(seed, DIR4, palette, h,w, mask=mask-{seed}):
        if out[r][c]==0:
            out[r][c]=v
    return out


def rule_m142(g):
    h,w=size(g)
    out=clone(g)
    markers=[(r,c,v) for r,row in enumerate(g) for c,v in enumerate(row) if v not in {0,1}]
    for r,c,color in markers:
        q=deque([(r,c)]); seen={(r,c)}
        while q:
            rr,cc=q.popleft()
            out[rr][cc]=color
            for dr,dc in DIR4:
                nr,nc=rr+dr,cc+dc
                if 0<=nr<h and 0<=nc<w and (nr,nc) not in seen and g[nr][nc]!=1:
                    seen.add((nr,nc)); q.append((nr,nc))
    return out


def rule_m143(g):
    target=g[0][0]
    g2=clone(g); g2[0][0]=0
    comps=[comp for comp in components(g2) if comp["color"]==target]
    comp=max(comps, key=lambda comp: len(comp["cells"]))
    return normalize_component(comp)


def rule_m144(g):
    code=g[0][0]
    g2=clone(g); g2[0][0]=0
    obj=crop_bbox(g2)
    return apply_transform(obj, code)


def rule_m145(g):
    out=blank(*size(g),0)
    for comp in components(g):
        holes=hole_count_component(comp["cells"])
        color={0:3,1:4,2:5}.get(holes, 6)
        for r,c in comp["cells"]:
            out[r][c]=color
    return out


def rule_m146(g):
    comps=sort_comps_left_to_right(components(g))
    areas=[len(comp["cells"]) for comp in comps]
    n=len(comps)
    out=blank(n,n,0)
    for i in range(n):
        for j in range(n):
            if i==j:
                out[i][j]=2
            else:
                out[i][j]=5 if areas[i]>areas[j] else 0
    return out


def rule_m147(g):
    h,w=size(g)
    markers=[(r,c) for r,row in enumerate(g) for c,v in enumerate(row) if v==9]
    non9=[[v if v!=9 else 0 for v in row] for row in g]
    template=crop_bbox(non9)
    # original template top-left from bbox of non9 cells
    cells=nonzero_cells(non9)
    r0,c0,r1,c1=bbox(cells)
    out=blank(h,w,0)
    positions=[(r0,c0)] + markers
    th,tw=size(template)
    for top,left in positions:
        for r in range(th):
            for c in range(tw):
                v=template[r][c]
                if v!=0 and 0<=top+r<h and 0<=left+c<w:
                    out[top+r][left+c]=v
    return out


def rule_h141(g):
    h,w=size(g)
    palette=[v for v in g[0] if v!=0][:3]
    seed=None
    for r in range(h):
        for c in range(w):
            if g[r][c]==9:
                seed=(r,c)
    mask=chamber_from_seed(g, seed, wall=1)
    out=clone(g)
    for r,c,v in phase_weave(seed, DIR8, palette, h,w, mask=mask-{seed}):
        if out[r][c]==0:
            out[r][c]=v
    return out


def rule_h142(g):
    panels=split_by_zero_cols(g)
    assert len(panels)==3
    A,B,C=panels
    A=strip_zero_border(A); B=strip_zero_border(B); C=strip_zero_border(C)
    code=None
    for k,tf in TRANSFORMS.items():
        if eq_grid(strip_zero_border(apply_transform(A,k)), B):
            code=k; break
    if code is None:
        raise ValueError("no transform")
    return strip_zero_border(apply_transform(C, code))


def rule_h143(g):
    comps=components(g)
    # sort outer to inner by bbox area descending
    comps=sorted(comps, key=lambda comp: ((bbox(comp["cells"])[2]-bbox(comp["cells"])[0]+1)*(bbox(comp["cells"])[3]-bbox(comp["cells"])[1]+1)), reverse=True)
    out=blank(*size(g),0)
    for i,comp in enumerate(comps):
        color=2+i
        for r,c in comp["cells"]:
            out[r][c]=color
    return out


def rule_h144(g):
    h,w=size(g)
    out=blank(h,w,0)
    paths=[]
    by=defaultdict(list)
    for r,row in enumerate(g):
        for c,v in enumerate(row):
            if v!=0:
                by[v].append((r,c))
    for color,pts in by.items():
        pts=sorted(pts)
        cells=l_path(pts[0], pts[1])
        paths.append((color,cells))
    counts=Counter(cell for _,cells in paths for cell in cells)
    for color,cells in paths:
        for r,c in cells:
            out[r][c]=8 if counts[(r,c)]>1 else color
    return out


def rule_h145(g):
    parts=split_by_zero_cols(g)
    assert len(parts)==2
    template=strip_zero_border(parts[0])
    codes=parts[1]
    mh,mw=size(codes)
    th,tw=size(template)
    out=blank(mh*th, mw*tw, 0)
    for rr in range(mh):
        for cc in range(mw):
            code=codes[rr][cc]
            tf=apply_transform(template, code)
            tf=strip_zero_border(tf)
            # assume same square size
            for r in range(th):
                for c in range(tw):
                    v=tf[r][c]
                    if v!=0:
                        out[rr*th+r][cc*tw+c]=v
    return out


def rule_h146(g):
    comps=components(g)
    items=[]
    for comp in comps:
        norm=normalize_component(comp)
        items.append((hole_count_component(comp["cells"]), len(comp["cells"]), norm))
    items.sort(key=lambda x:(x[0], x[1]))
    maxh=max(len(norm) for _,_,norm in items)
    totalw=sum(len(norm[0]) for _,_,norm in items)+(len(items)-1)
    out=blank(maxh,totalw,0)
    x=0
    for _,_,norm in items:
        nh,nw=size(norm)
        for r in range(nh):
            for c in range(nw):
                v=norm[r][c]
                if v!=0:
                    out[r][x+c]=v
        x += nw + 1
    return out


def rule_h147(g):
    code=g[0][0]
    src=[v for v in g[0][2:] if v!=0]
    tgt=[v for v in g[1][2:] if v!=0]
    mapping=dict(zip(src,tgt))
    obj=[row[:] for row in g[2:]]
    obj=crop_bbox(obj)
    remapped=[[mapping.get(v,v) if v!=0 else 0 for v in row] for row in obj]
    return strip_zero_border(apply_transform(remapped, code))


PUZZLES = json.loads(r'''[
  {
    "id": "E141",
    "title": "Alternating Seed Rays",
    "difficulty": "easy",
    "skills": [
      "periodic painting",
      "cardinal rays",
      "legend reading"
    ],
    "suggested_staged_path": "First isolate the legend colors on the top row. Then start from the seed and walk outward in the four cardinal directions, cycling those legend colors.",
    "written_solution": "The top row provides a two-color palette. Keep the input as-is, then from the unique seed cell draw rays up, down, left, and right. Color the first step with the first legend color, the second step with the second legend color, then repeat that two-color cycle until the border.",
    "program_name": "rule_e141",
    "program_source": "def rule_e141(g):\n    h,w=size(g)\n    palette=[v for v in g[0] if v!=0][:2]\n    sr=sc=None\n    for r in range(1,h):\n        for c in range(w):\n            if g[r][c]==9:\n                sr,sc=r,c\n    out=clone(g)\n    for r,c,v in phase_weave((sr,sc), DIR4, palette, h,w):\n        if out[r][c]==0:\n            out[r][c]=v\n    return out\n",
    "train": [
      {
        "input": [
          "028000000",
          "000000000",
          "000000000",
          "000009000",
          "000000000",
          "000000000",
          "000000000"
        ],
        "output": [
          "028002000",
          "000008000",
          "000002000",
          "282829282",
          "000002000",
          "000008000",
          "000002000"
        ]
      },
      {
        "input": [
          "03400000",
          "00000000",
          "00000000",
          "00000000",
          "00000000",
          "00900000",
          "00000000",
          "00000000"
        ],
        "output": [
          "03400000",
          "00400000",
          "00300000",
          "00400000",
          "00300000",
          "43934343",
          "00300000",
          "00400000"
        ]
      },
      {
        "input": [
          "0760000000",
          "0000000000",
          "0000000900",
          "0000000000",
          "0000000000",
          "0000000000"
        ],
        "output": [
          "0760000600",
          "0000000700",
          "7676767976",
          "0000000700",
          "0000000600",
          "0000000700"
        ]
      },
      {
        "input": [
          "0520000",
          "0000000",
          "0000000",
          "0000000",
          "0000000",
          "0000000",
          "0009000",
          "0000000",
          "0000000"
        ],
        "output": [
          "0522000",
          "0005000",
          "0002000",
          "0005000",
          "0002000",
          "0005000",
          "5259525",
          "0005000",
          "0002000"
        ]
      }
    ],
    "test": [
      {
        "input": [
          "04700000000",
          "00000000000",
          "00000000000",
          "00000000000",
          "00000000900",
          "00000000000",
          "00000000000",
          "00000000000"
        ],
        "output": [
          "04700000700",
          "00000000400",
          "00000000700",
          "00000000400",
          "74747474947",
          "00000000400",
          "00000000700",
          "00000000400"
        ]
      }
    ]
  },
  {
    "id": "E142",
    "title": "Fill the Gap",
    "difficulty": "easy",
    "skills": [
      "row reasoning",
      "endpoint completion",
      "same-color segments"
    ],
    "suggested_staged_path": "Treat each row independently. When a color appears exactly twice on a row, everything between those two endpoints should match it.",
    "written_solution": "On each row, find colors that appear exactly twice. Fill every cell between the left and right occurrence of that color, inclusive, with that same color. Leave all other rows and cells unchanged.",
    "program_name": "rule_e142",
    "program_source": "def rule_e142(g):\n    h,w=size(g)\n    out=clone(g)\n    for r in range(h):\n        row=g[r]\n        for color in sorted(set(row)-{0}):\n            pos=[c for c,v in enumerate(row) if v==color]\n            if len(pos)==2:\n                for c in range(min(pos), max(pos)+1):\n                    out[r][c]=color\n    return out\n",
    "train": [
      {
        "input": [
          "0000000000",
          "0200200000",
          "0000000000",
          "0070000070",
          "0000000000",
          "0000000000"
        ],
        "output": [
          "0000000000",
          "0222200000",
          "0000000000",
          "0077777770",
          "0000000000",
          "0000000000"
        ]
      },
      {
        "input": [
          "300300000",
          "000000000",
          "000006006",
          "000000000",
          "000000000",
          "040000400",
          "000000000"
        ],
        "output": [
          "333300000",
          "000000000",
          "000006666",
          "000000000",
          "000000000",
          "044444400",
          "000000000"
        ]
      },
      {
        "input": [
          "00000000000",
          "00800000080",
          "00000000000",
          "00000000000",
          "50005000000"
        ],
        "output": [
          "00000000000",
          "00888888880",
          "00000000000",
          "00000000000",
          "55555000000"
        ]
      },
      {
        "input": [
          "00000000",
          "00000000",
          "09000090",
          "00000000",
          "00000000",
          "00000000",
          "20020000",
          "00000000"
        ],
        "output": [
          "00000000",
          "00000000",
          "09999990",
          "00000000",
          "00000000",
          "00000000",
          "22220000",
          "00000000"
        ]
      }
    ],
    "test": [
      {
        "input": [
          "000000000000",
          "000400000040",
          "000000000000",
          "000000000000",
          "700007000000",
          "000000000000",
          "000000020002"
        ],
        "output": [
          "000000000000",
          "000444444440",
          "000000000000",
          "000000000000",
          "777777000000",
          "000000000000",
          "000000022222"
        ]
      }
    ]
  },
  {
    "id": "E143",
    "title": "Mirror Across the Guide",
    "difficulty": "easy",
    "skills": [
      "reflection",
      "guide detection",
      "same-size copy"
    ],
    "suggested_staged_path": "The solid nonzero row is not part of the object. It is the mirror line.",
    "written_solution": "Find the full-width guide row made of a single nonzero color. Copy every nonzero cell above that guide to the symmetric position below it, preserving color. Keep the original cells and the guide row.",
    "program_name": "rule_e143",
    "program_source": "def rule_e143(g):\n    h,w=size(g)\n    guide=None\n    for r,row in enumerate(g):\n        vals=set(row)\n        if len(vals)==1 and 0 not in vals:\n            guide=r; break\n    out=clone(g)\n    for r in range(guide):\n        rr=2*guide-r\n        if rr<h:\n            for c,v in enumerate(g[r]):\n                if v!=0:\n                    out[rr][c]=v\n    return out\n",
    "train": [
      {
        "input": [
          "000000000",
          "003000000",
          "000007000",
          "060000000",
          "555555555",
          "000000000",
          "000000000",
          "000000000",
          "000000000"
        ],
        "output": [
          "000000000",
          "003000000",
          "000007000",
          "060000000",
          "555555555",
          "060000000",
          "000007000",
          "003000000",
          "000000000"
        ]
      },
      {
        "input": [
          "2000000000",
          "0000800000",
          "0000000040",
          "5555555555",
          "0000000000",
          "0000000000",
          "0000000000",
          "0000000000"
        ],
        "output": [
          "2000000000",
          "0000800000",
          "0000000040",
          "5555555555",
          "0000000040",
          "0000800000",
          "2000000000",
          "0000000000"
        ]
      },
      {
        "input": [
          "0000060",
          "0900000",
          "0000000",
          "0000000",
          "0002000",
          "5555555",
          "0000000",
          "0000000",
          "0000000",
          "0000000"
        ],
        "output": [
          "0000060",
          "0900000",
          "0000000",
          "0000000",
          "0002000",
          "5555555",
          "0002000",
          "0000000",
          "0000000",
          "0900000"
        ]
      },
      {
        "input": [
          "00700000000",
          "00000000300",
          "55555555555",
          "00000000000",
          "00000000000",
          "00000000000",
          "00000000000"
        ],
        "output": [
          "00700000000",
          "00000000300",
          "55555555555",
          "00000000300",
          "00700000000",
          "00000000000",
          "00000000000"
        ]
      }
    ],
    "test": [
      {
        "input": [
          "000000000000",
          "080000000000",
          "000000300000",
          "000000000070",
          "555555555555",
          "000000000000",
          "000000000000",
          "000000000000",
          "000000000000"
        ],
        "output": [
          "000000000000",
          "080000000000",
          "000000300000",
          "000000000070",
          "555555555555",
          "000000000070",
          "000000300000",
          "080000000000",
          "000000000000"
        ]
      }
    ]
  },
  {
    "id": "E144",
    "title": "Crop the Action",
    "difficulty": "easy",
    "skills": [
      "bounding box",
      "size change",
      "object extraction"
    ],
    "suggested_staged_path": "Ignore the empty border. The answer is just the tightest rectangle that still contains every nonzero cell.",
    "written_solution": "Take the tight bounding box around all nonzero cells in the input and output exactly that cropped subgrid.",
    "program_name": "rule_e144",
    "program_source": "def rule_e144(g):\n    return crop_bbox(g)\n",
    "train": [
      {
        "input": [
          "0000000000",
          "0000000000",
          "0004000000",
          "0004000000",
          "0004400000",
          "0000000000",
          "0000000000",
          "0000000000"
        ],
        "output": [
          "40",
          "40",
          "44"
        ]
      },
      {
        "input": [
          "000000000",
          "000008880",
          "000000800",
          "000000800",
          "060000000",
          "006000000",
          "000000000"
        ],
        "output": [
          "0000888",
          "0000080",
          "0000080",
          "6000000",
          "0600000"
        ]
      },
      {
        "input": [
          "000000000000",
          "000000000000",
          "000000000000",
          "000000000000",
          "000000000000",
          "000000030000",
          "000000033000",
          "000000033300",
          "000000000000"
        ],
        "output": [
          "300",
          "330",
          "333"
        ]
      },
      {
        "input": [
          "0000000000",
          "0550000000",
          "0050000000",
          "0055000000",
          "0000004440",
          "0000000000"
        ],
        "output": [
          "55000000",
          "05000000",
          "05500000",
          "00000444"
        ]
      }
    ],
    "test": [
      {
        "input": [
          "00000000000",
          "00000000777",
          "00000000000",
          "00002200000",
          "00000220000",
          "00000020000",
          "00000000000",
          "00000000000",
          "00000000000"
        ],
        "output": [
          "0000777",
          "0000000",
          "2200000",
          "0220000",
          "0020000"
        ]
      }
    ]
  },
  {
    "id": "E145",
    "title": "Fourth Corner",
    "difficulty": "easy",
    "skills": [
      "axis-aligned rectangles",
      "corner completion",
      "color grouping"
    ],
    "suggested_staged_path": "Group by color and look for three corners of an axis-aligned rectangle. The missing output cell is the fourth corner.",
    "written_solution": "For each color, the input gives three of the four corners of an axis-aligned rectangle. Add the missing fourth corner of that same color and leave everything else unchanged.",
    "program_name": "rule_e145",
    "program_source": "def rule_e145(g):\n    out=clone(g)\n    by=defaultdict(list)\n    for r,row in enumerate(g):\n        for c,v in enumerate(row):\n            if v!=0:\n                by[v].append((r,c))\n    for color,cells in by.items():\n        if len(cells)==3:\n            r0,c0,r1,c1=bbox(cells)\n            corners={(r0,c0),(r0,c1),(r1,c0),(r1,c1)}\n            missing=list(corners-set(cells))\n            if len(missing)==1:\n                r,c=missing[0]\n                out[r][c]=color\n    return out\n",
    "train": [
      {
        "input": [
          "000000000",
          "030003000",
          "000000000",
          "000000000",
          "030000000",
          "000000000",
          "000000000"
        ],
        "output": [
          "000000000",
          "030003000",
          "000000000",
          "000000000",
          "030003000",
          "000000000",
          "000000000"
        ]
      },
      {
        "input": [
          "0000000000",
          "0000000044",
          "0000000600",
          "0000000000",
          "0000000000",
          "0000000004",
          "0060000600",
          "0000000000"
        ],
        "output": [
          "0000000000",
          "0000000044",
          "0060000600",
          "0000000000",
          "0000000000",
          "0000000044",
          "0060000600",
          "0000000000"
        ]
      },
      {
        "input": [
          "07000000",
          "00000000",
          "00000000",
          "07007000",
          "00000000",
          "00000000"
        ],
        "output": [
          "07007000",
          "00000000",
          "00000000",
          "07007000",
          "00000000",
          "00000000"
        ]
      },
      {
        "input": [
          "000000000",
          "000000800",
          "005000050",
          "000000000",
          "000000808",
          "000000000",
          "000000000",
          "000000050",
          "000000000"
        ],
        "output": [
          "000000000",
          "000000808",
          "005000050",
          "000000000",
          "000000808",
          "000000000",
          "000000000",
          "005000050",
          "000000000"
        ]
      }
    ],
    "test": [
      {
        "input": [
          "00000000000",
          "00000020000",
          "00000000707",
          "00000000000",
          "00000000000",
          "02000020000",
          "00000000700",
          "00000000000"
        ],
        "output": [
          "00000000000",
          "02000020000",
          "00000000707",
          "00000000000",
          "00000000000",
          "02000020000",
          "00000000707",
          "00000000000"
        ]
      }
    ]
  },
  {
    "id": "E146",
    "title": "Commanded Trail",
    "difficulty": "easy",
    "skills": [
      "symbol command",
      "directional extension",
      "same-size painting"
    ],
    "suggested_staged_path": "One cell is a command, not part of the trail. The other nonzero cell is the color to extend.",
    "written_solution": "The command cell encodes a direction: 1 up, 2 down, 3 left, 4 right. Starting from the unique non-command colored seed, extend that seed color in the commanded direction until the border. Keep the command and seed cells.",
    "program_name": "rule_e146",
    "program_source": "def rule_e146(g):\n    h,w=size(g)\n    out=clone(g)\n    cmd=None\n    seed=None\n    for r,row in enumerate(g):\n        for c,v in enumerate(row):\n            if v in {1,2,3,4}:\n                cmd=(r,c,v)\n            elif v!=0:\n                seed=(r,c,v)\n    sr,sc,color=seed\n    code=cmd[2]\n    drdc={1:(-1,0),2:(1,0),3:(0,-1),4:(0,1)}[code]\n    r,c=sr+drdc[0], sc+drdc[1]\n    while 0<=r<h and 0<=c<w:\n        if out[r][c]==0:\n            out[r][c]=color\n        r+=drdc[0]; c+=drdc[1]\n    return out\n",
    "train": [
      {
        "input": [
          "10000000",
          "00000000",
          "00000000",
          "00000000",
          "00060000",
          "00000000",
          "00000000"
        ],
        "output": [
          "10060000",
          "00060000",
          "00060000",
          "00060000",
          "00060000",
          "00000000",
          "00000000"
        ]
      },
      {
        "input": [
          "200000000",
          "000000000",
          "000007000",
          "000000000",
          "000000000",
          "000000000",
          "000000000",
          "000000000"
        ],
        "output": [
          "200000000",
          "000000000",
          "000007000",
          "000007000",
          "000007000",
          "000007000",
          "000007000",
          "000007000"
        ]
      },
      {
        "input": [
          "3000000000",
          "0000000000",
          "0000000000",
          "0000000800",
          "0000000000",
          "0000000000"
        ],
        "output": [
          "3000000000",
          "0000000000",
          "0000000000",
          "8888888800",
          "0000000000",
          "0000000000"
        ]
      },
      {
        "input": [
          "4000000",
          "0000000",
          "0000000",
          "0000000",
          "0000000",
          "0500000",
          "0000000",
          "0000000",
          "0000000"
        ],
        "output": [
          "4000000",
          "0000000",
          "0000000",
          "0000000",
          "0000000",
          "0555555",
          "0000000",
          "0000000",
          "0000000"
        ]
      }
    ],
    "test": [
      {
        "input": [
          "1000000000",
          "0000000000",
          "0000000000",
          "0000000000",
          "0000000000",
          "0000000000",
          "0000900000",
          "0000000000"
        ],
        "output": [
          "1000900000",
          "0000900000",
          "0000900000",
          "0000900000",
          "0000900000",
          "0000900000",
          "0000900000",
          "0000000000"
        ]
      }
    ]
  },
  {
    "id": "E147",
    "title": "Keep the Largest",
    "difficulty": "easy",
    "skills": [
      "connected components",
      "ranking by area",
      "filtering"
    ],
    "suggested_staged_path": "You do not need to transform the objects. You only need to decide which connected component is largest.",
    "written_solution": "Find all nonzero connected components and keep only the largest one. Replace every other nonzero cell with black.",
    "program_name": "rule_e147",
    "program_source": "def rule_e147(g):\n    comps=components(g)\n    best=max(comps, key=lambda comp:(len(comp[\"cells\"]), -min(r for r,c in comp[\"cells\"]), -min(c for r,c in comp[\"cells\"])))\n    out=blank(*size(g),0)\n    for r,c in best[\"cells\"]:\n        out[r][c]=best[\"color\"]\n    return out\n",
    "train": [
      {
        "input": [
          "0000000000",
          "0220000000",
          "0220000000",
          "0000044400",
          "0000040400",
          "0000044400",
          "7770000000",
          "0000000000"
        ],
        "output": [
          "0000000000",
          "0000000000",
          "0000000000",
          "0000044400",
          "0000040400",
          "0000044400",
          "0000000000",
          "0000000000"
        ]
      },
      {
        "input": [
          "000000000",
          "088800000",
          "008000000",
          "008000000",
          "000000000",
          "000033300",
          "000033300",
          "000033300",
          "000000000"
        ],
        "output": [
          "000000000",
          "000000000",
          "000000000",
          "000000000",
          "000000000",
          "000033300",
          "000033300",
          "000033300",
          "000000000"
        ]
      },
      {
        "input": [
          "000000000000",
          "000000006000",
          "005500006600",
          "000500006660",
          "000550000000",
          "000000000000",
          "000004440000"
        ],
        "output": [
          "000000000000",
          "000000006000",
          "000000006600",
          "000000006660",
          "000000000000",
          "000000000000",
          "000000000000"
        ]
      },
      {
        "input": [
          "00000000000",
          "02200000000",
          "00220077770",
          "00020070070",
          "00000070070",
          "00000077770",
          "00000000000",
          "00000000000"
        ],
        "output": [
          "00000000000",
          "00000000000",
          "00000077770",
          "00000070070",
          "00000070070",
          "00000077770",
          "00000000000",
          "00000000000"
        ]
      }
    ],
    "test": [
      {
        "input": [
          "000000000000",
          "040000000000",
          "040000000000",
          "044006666000",
          "000006006000",
          "000006006000",
          "000006666022",
          "000000000022",
          "000000000000"
        ],
        "output": [
          "000000000000",
          "000000000000",
          "000000000000",
          "000006666000",
          "000006006000",
          "000006006000",
          "000006666000",
          "000000000000",
          "000000000000"
        ]
      }
    ]
  },
  {
    "id": "M141",
    "title": "Room-Limited Weave",
    "difficulty": "medium",
    "skills": [
      "masking by chamber",
      "periodic rays",
      "frame reasoning"
    ],
    "suggested_staged_path": "This is the same alternating-ray idea as the easy version, except the frame blocks the rays. Work inside the seed\u2019s chamber only.",
    "written_solution": "The top row gives a two-color palette and the frame walls are color 1. Starting at the seed, draw alternating-color rays in the four cardinal directions, but only through the interior chamber reachable from the seed without crossing the frame.",
    "program_name": "rule_m141",
    "program_source": "def rule_m141(g):\n    h,w=size(g)\n    palette=[v for v in g[0] if v!=0][:2]\n    seed=None\n    for r in range(h):\n        for c in range(w):\n            if g[r][c]==9:\n                seed=(r,c)\n    mask=chamber_from_seed(g, seed, wall=1)\n    out=clone(g)\n    for r,c,v in phase_weave(seed, DIR4, palette, h,w, mask=mask-{seed}):\n        if out[r][c]==0:\n            out[r][c]=v\n    return out\n",
    "train": [
      {
        "input": [
          "0280000000",
          "0111111110",
          "0100000010",
          "0100000010",
          "0100090010",
          "0100000010",
          "0111111110",
          "0000000000"
        ],
        "output": [
          "0280000000",
          "0111111110",
          "0100080010",
          "0100020010",
          "0128292810",
          "0100020010",
          "0111111110",
          "0000000000"
        ]
      },
      {
        "input": [
          "034000000",
          "011111110",
          "010000010",
          "010000010",
          "010000010",
          "010900010",
          "010000010",
          "011111110",
          "000000000"
        ],
        "output": [
          "034000000",
          "011111110",
          "010300010",
          "010400010",
          "010300010",
          "013934310",
          "010300010",
          "011111110",
          "000000000"
        ]
      },
      {
        "input": [
          "06700000000",
          "01111111110",
          "01000000010",
          "01000009010",
          "01000000010",
          "01111111110",
          "00000000000"
        ],
        "output": [
          "06700000000",
          "01111111110",
          "01000006010",
          "01676769610",
          "01000006010",
          "01111111110",
          "00000000000"
        ]
      },
      {
        "input": [
          "05200000",
          "01111110",
          "01000010",
          "01000010",
          "01000010",
          "01000010",
          "01009010",
          "01000010",
          "01111110",
          "00000000"
        ],
        "output": [
          "05200000",
          "01111110",
          "01002010",
          "01005010",
          "01002010",
          "01005010",
          "01259510",
          "01005010",
          "01111110",
          "00000000"
        ]
      }
    ],
    "test": [
      {
        "input": [
          "046000000000",
          "011111111110",
          "010000000010",
          "010000000010",
          "010000009010",
          "010000000010",
          "010000000010",
          "011111111110",
          "000000000000"
        ],
        "output": [
          "046000000000",
          "011111111110",
          "010000006010",
          "010000004010",
          "016464649410",
          "010000004010",
          "010000006010",
          "011111111110",
          "000000000000"
        ]
      }
    ]
  },
  {
    "id": "M142",
    "title": "Chamber Paint",
    "difficulty": "medium",
    "skills": [
      "flood fill",
      "containment",
      "multiple chambers"
    ],
    "suggested_staged_path": "The marker does not just recolor itself. It names the whole region inside its frame.",
    "written_solution": "Each non-frame marker sits inside a chamber bounded by color-1 walls. Flood fill that chamber with the marker\u2019s color, keeping the frame intact. Do this independently for every chamber.",
    "program_name": "rule_m142",
    "program_source": "def rule_m142(g):\n    h,w=size(g)\n    out=clone(g)\n    markers=[(r,c,v) for r,row in enumerate(g) for c,v in enumerate(row) if v not in {0,1}]\n    for r,c,color in markers:\n        q=deque([(r,c)]); seen={(r,c)}\n        while q:\n            rr,cc=q.popleft()\n            out[rr][cc]=color\n            for dr,dc in DIR4:\n                nr,nc=rr+dr,cc+dc\n                if 0<=nr<h and 0<=nc<w and (nr,nc) not in seen and g[nr][nc]!=1:\n                    seen.add((nr,nc)); q.append((nr,nc))\n    return out\n",
    "train": [
      {
        "input": [
          "000000000000",
          "011110000000",
          "013010000000",
          "010010000000",
          "011110000000",
          "000000011110",
          "000000017010",
          "000000010010",
          "000000011110",
          "000000000000"
        ],
        "output": [
          "000000000000",
          "011110000000",
          "013310000000",
          "013310000000",
          "011110000000",
          "000000011110",
          "000000017710",
          "000000017710",
          "000000011110",
          "000000000000"
        ]
      },
      {
        "input": [
          "00000000000",
          "01111100000",
          "01000101110",
          "01020101010",
          "01000101810",
          "01111101010",
          "00000001010",
          "00000001110",
          "00000000000"
        ],
        "output": [
          "00000000000",
          "01111100000",
          "01222101110",
          "01222101810",
          "01222101810",
          "01111101810",
          "00000001810",
          "00000001110",
          "00000000000"
        ]
      },
      {
        "input": [
          "0000000000000",
          "0011110011110",
          "0010010016010",
          "0014010010010",
          "0010010010010",
          "0010010011110",
          "0011110000000",
          "0000000000000"
        ],
        "output": [
          "0000000000000",
          "0011110011110",
          "0014410016610",
          "0014410016610",
          "0014410016610",
          "0014410011110",
          "0011110000000",
          "0000000000000"
        ]
      },
      {
        "input": [
          "00000000000",
          "01111000000",
          "01071000000",
          "01001000000",
          "01111000000",
          "00000000000",
          "00111111100",
          "00100500100",
          "00100000100",
          "00111111100",
          "00000000000"
        ],
        "output": [
          "00000000000",
          "01111000000",
          "01771000000",
          "01771000000",
          "01111000000",
          "00000000000",
          "00111111100",
          "00155555100",
          "00155555100",
          "00111111100",
          "00000000000"
        ]
      }
    ],
    "test": [
      {
        "input": [
          "00000000000000",
          "01111000000000",
          "01201000111110",
          "01001000100010",
          "01001000109010",
          "01111000100010",
          "01111100100010",
          "01040100111110",
          "01111100000000",
          "00000000000000"
        ],
        "output": [
          "00000000000000",
          "01111000000000",
          "01221000111110",
          "01221000199910",
          "01221000199910",
          "01111000199910",
          "01111100199910",
          "01444100111110",
          "01111100000000",
          "00000000000000"
        ]
      }
    ]
  },
  {
    "id": "M143",
    "title": "Legend Select Crop",
    "difficulty": "medium",
    "skills": [
      "legend lookup",
      "component selection",
      "normalization"
    ],
    "suggested_staged_path": "The top-left cell is a selector, not an object to crop.",
    "written_solution": "Read the top-left legend color. Among the remaining components, select the component of that color, crop it to its tight bounding box, and output that normalized crop.",
    "program_name": "rule_m143",
    "program_source": "def rule_m143(g):\n    target=g[0][0]\n    g2=clone(g); g2[0][0]=0\n    comps=[comp for comp in components(g2) if comp[\"color\"]==target]\n    comp=max(comps, key=lambda comp: len(comp[\"cells\"]))\n    return normalize_component(comp)\n",
    "train": [
      {
        "input": [
          "400000000000",
          "000000000000",
          "000400000000",
          "000400007770",
          "000440000700",
          "000000000700",
          "022200000000",
          "000000000000"
        ],
        "output": [
          "40",
          "40",
          "44"
        ]
      },
      {
        "input": [
          "70000000000",
          "00000000440",
          "00000000440",
          "00000777000",
          "00000707000",
          "06600777000",
          "00600000000",
          "00660000000",
          "00000000000"
        ],
        "output": [
          "777",
          "707",
          "777"
        ]
      },
      {
        "input": [
          "2000000000000",
          "0000000000000",
          "0000000002200",
          "0050000000220",
          "0055000000020",
          "0055500000000",
          "0000000000000"
        ],
        "output": [
          "220",
          "022",
          "002"
        ]
      },
      {
        "input": [
          "6000000000",
          "0333300000",
          "0300300000",
          "0300300000",
          "0333366000",
          "0000006000",
          "0000006600",
          "0000000000",
          "0000000000",
          "0000000000"
        ],
        "output": [
          "660",
          "060",
          "066"
        ]
      }
    ],
    "test": [
      {
        "input": [
          "500000000000",
          "000000000000",
          "022200000000",
          "022200000000",
          "022200050000",
          "000000055000",
          "000000055500",
          "000080000000",
          "000008000000"
        ],
        "output": [
          "500",
          "550",
          "555"
        ]
      }
    ]
  },
  {
    "id": "M144",
    "title": "Commanded Transform",
    "difficulty": "medium",
    "skills": [
      "dihedral transforms",
      "command decoding",
      "cropping"
    ],
    "suggested_staged_path": "The command cell tells you how to transform the object. The output is the transformed object only, cropped tight.",
    "written_solution": "Interpret the top-left code as a geometric transform, apply that transform to the nonzero object elsewhere in the grid, and output the transformed object cropped to its bounding box.",
    "program_name": "rule_m144",
    "program_source": "def rule_m144(g):\n    code=g[0][0]\n    g2=clone(g); g2[0][0]=0\n    obj=crop_bbox(g2)\n    return apply_transform(obj, code)\n",
    "train": [
      {
        "input": [
          "2000000000",
          "0000000000",
          "0000000000",
          "0000600000",
          "0000670000",
          "0000000000",
          "0000000000",
          "0000000000"
        ],
        "output": [
          "66",
          "70"
        ]
      },
      {
        "input": [
          "500000000",
          "000000000",
          "008800000",
          "000800000",
          "000080000",
          "000000000",
          "000000000",
          "000000000",
          "000000000"
        ],
        "output": [
          "088",
          "080",
          "800"
        ]
      },
      {
        "input": [
          "30000000000",
          "00000000000",
          "00000000000",
          "00000033000",
          "00000030300",
          "00000000000",
          "00000000000"
        ],
        "output": [
          "303",
          "033"
        ]
      },
      {
        "input": [
          "70000000",
          "00000000",
          "00070000",
          "00077000",
          "00007000",
          "00000000",
          "00000000",
          "00000000"
        ],
        "output": [
          "770",
          "077"
        ]
      }
    ],
    "test": [
      {
        "input": [
          "4000000000",
          "0000000000",
          "0000000000",
          "0000000000",
          "0000550000",
          "0000050000",
          "0000055000",
          "0000000000",
          "0000000000",
          "0000000000"
        ],
        "output": [
          "005",
          "555",
          "500"
        ]
      }
    ]
  },
  {
    "id": "M145",
    "title": "Holes Decide the Color",
    "difficulty": "medium",
    "skills": [
      "hole counting",
      "component analysis",
      "recoloring"
    ],
    "suggested_staged_path": "The shape geometry stays the same. What changes is the color assigned to each component based on its number of holes.",
    "written_solution": "For each connected component, count the number of enclosed holes in its shape. Recolor the whole component according to that count: no holes becomes one color, one hole becomes another, and so on. Keep the geometry unchanged.",
    "program_name": "rule_m145",
    "program_source": "def rule_m145(g):\n    out=blank(*size(g),0)\n    for comp in components(g):\n        holes=hole_count_component(comp[\"cells\"])\n        color={0:3,1:4,2:5}.get(holes, 6)\n        for r,c in comp[\"cells\"]:\n            out[r][c]=color\n    return out\n",
    "train": [
      {
        "input": [
          "000000000000",
          "022000000000",
          "022000000000",
          "000000222000",
          "000000202000",
          "022200222000",
          "022200000000",
          "022200000000",
          "000000000000"
        ],
        "output": [
          "000000000000",
          "033000000000",
          "033000000000",
          "000000444000",
          "000000404000",
          "033300444000",
          "033300000000",
          "033300000000",
          "000000000000"
        ]
      },
      {
        "input": [
          "00000000000",
          "02222000000",
          "02002000000",
          "02002000000",
          "02222000000",
          "00000000220",
          "00000000220",
          "00000000000"
        ],
        "output": [
          "00000000000",
          "04444000000",
          "04004000000",
          "04004000000",
          "04444000000",
          "00000000330",
          "00000000330",
          "00000000000"
        ]
      },
      {
        "input": [
          "0000000000",
          "0000000000",
          "0220000000",
          "0020000000",
          "0022000000",
          "0000022200",
          "0000020200",
          "0000022200",
          "0000000000",
          "0000000000"
        ],
        "output": [
          "0000000000",
          "0000000000",
          "0330000000",
          "0030000000",
          "0033000000",
          "0000044400",
          "0000040400",
          "0000044400",
          "0000000000",
          "0000000000"
        ]
      },
      {
        "input": [
          "0000000000000",
          "0000000022200",
          "0000000022200",
          "0000000022200",
          "0022220000000",
          "0020020000000",
          "0020020000220",
          "0022220000220",
          "0000000000000"
        ],
        "output": [
          "0000000000000",
          "0000000033300",
          "0000000033300",
          "0000000033300",
          "0044440000000",
          "0040040000000",
          "0040040000330",
          "0044440000330",
          "0000000000000"
        ]
      }
    ],
    "test": [
      {
        "input": [
          "000000000000",
          "022200000000",
          "020200022200",
          "022200022200",
          "000000022200",
          "000000000000",
          "000022000000",
          "000002000000",
          "000002200000",
          "000000000000"
        ],
        "output": [
          "000000000000",
          "044400000000",
          "040400033300",
          "044400033300",
          "000000033300",
          "000000000000",
          "000033000000",
          "000003000000",
          "000003300000",
          "000000000000"
        ]
      }
    ]
  },
  {
    "id": "M146",
    "title": "Area Comparison Table",
    "difficulty": "medium",
    "skills": [
      "object ranking",
      "relational output",
      "matrix construction"
    ],
    "suggested_staged_path": "The answer is not a transformed scene. It is a summary matrix comparing the three objects from left to right.",
    "written_solution": "Order the three components from left to right. Build a square matrix whose diagonal is a fixed self-comparison value and whose off-diagonal cells indicate whether the row object has larger area than the column object.",
    "program_name": "rule_m146",
    "program_source": "def rule_m146(g):\n    comps=sort_comps_left_to_right(components(g))\n    areas=[len(comp[\"cells\"]) for comp in comps]\n    n=len(comps)\n    out=blank(n,n,0)\n    for i in range(n):\n        for j in range(n):\n            if i==j:\n                out[i][j]=2\n            else:\n                out[i][j]=5 if areas[i]>areas[j] else 0\n    return out\n",
    "train": [
      {
        "input": [
          "00000000000000",
          "00000000004440",
          "02200333004440",
          "02200303004440",
          "00000333000000",
          "00000000000000",
          "00000000000000",
          "00000000000000"
        ],
        "output": [
          "200",
          "520",
          "552"
        ]
      },
      {
        "input": [
          "000000000000000",
          "000000000000000",
          "000006660000000",
          "000006660007700",
          "000006660000700",
          "000000000000770",
          "055500000000000",
          "000000000000000",
          "000000000000000"
        ],
        "output": [
          "200",
          "525",
          "502"
        ]
      },
      {
        "input": [
          "0000000000000",
          "0222000000000",
          "0202000004000",
          "0222008804400",
          "0000008804440",
          "0000000000000",
          "0000000000000"
        ],
        "output": [
          "255",
          "020",
          "052"
        ]
      },
      {
        "input": [
          "0000000000000000",
          "0000003333000000",
          "0660003003000000",
          "0060003003000000",
          "0066003333000990",
          "0000000000000990",
          "0000000000000000",
          "0000000000000000"
        ],
        "output": [
          "205",
          "525",
          "002"
        ]
      }
    ],
    "test": [
      {
        "input": [
          "000000000000000",
          "022200000000000",
          "022200000008880",
          "022200055008080",
          "000000005008880",
          "000000005500000",
          "000000000000000",
          "000000000000000"
        ],
        "output": [
          "255",
          "020",
          "052"
        ]
      }
    ]
  },
  {
    "id": "M147",
    "title": "Template Copies",
    "difficulty": "medium",
    "skills": [
      "template extraction",
      "anchored stamping",
      "multiple placements"
    ],
    "suggested_staged_path": "The colored shape in the top-left is the template. Every 9 tells you where another copy should start.",
    "written_solution": "Extract the non-9 template from the top-left of the input. Keep the original template and stamp identical copies with their top-left corner anchored at every 9 marker location.",
    "program_name": "rule_m147",
    "program_source": "def rule_m147(g):\n    h,w=size(g)\n    markers=[(r,c) for r,row in enumerate(g) for c,v in enumerate(row) if v==9]\n    non9=[[v if v!=9 else 0 for v in row] for row in g]\n    template=crop_bbox(non9)\n    # original template top-left from bbox of non9 cells\n    cells=nonzero_cells(non9)\n    r0,c0,r1,c1=bbox(cells)\n    out=blank(h,w,0)\n    positions=[(r0,c0)] + markers\n    th,tw=size(template)\n    for top,left in positions:\n        for r in range(th):\n            for c in range(tw):\n                v=template[r][c]\n                if v!=0 and 0<=top+r<h and 0<=left+c<w:\n                    out[top+r][left+c]=v\n    return out\n",
    "train": [
      {
        "input": [
          "240000000000",
          "024000000000",
          "000000000000",
          "000000900000",
          "000000000000",
          "090000000000",
          "000000000000",
          "000000000000"
        ],
        "output": [
          "240000000000",
          "024000000000",
          "000000000000",
          "000000240000",
          "000000024000",
          "024000000000",
          "002400000000",
          "000000000000"
        ]
      },
      {
        "input": [
          "6600000000000",
          "0600000090000",
          "0060000000000",
          "0000000000000",
          "0000000000000",
          "0000090000000",
          "0000000000000",
          "0000000000000",
          "0000000000000"
        ],
        "output": [
          "6600000000000",
          "0600000066000",
          "0060000006000",
          "0000000000600",
          "0000000000000",
          "0000066000000",
          "0000006000000",
          "0000000600000",
          "0000000000000"
        ]
      },
      {
        "input": [
          "70000000000",
          "77000000000",
          "00000000000",
          "00000009000",
          "00000000000",
          "00090000000",
          "00000000000"
        ],
        "output": [
          "70000000000",
          "77000000000",
          "00000000000",
          "00000007000",
          "00000007700",
          "00070000000",
          "00077000000"
        ]
      },
      {
        "input": [
          "808000000000",
          "080000000000",
          "000000009000",
          "000000000000",
          "000000000000",
          "000000000000",
          "000090000000",
          "000000000900",
          "000000000000",
          "000000000000"
        ],
        "output": [
          "808000000000",
          "080000000000",
          "000000008080",
          "000000000800",
          "000000000000",
          "000000000000",
          "000080800000",
          "000008000808",
          "000000000080",
          "000000000000"
        ]
      }
    ],
    "test": [
      {
        "input": [
          "24000000000000",
          "02400000000000",
          "00000000090000",
          "00000000000000",
          "00000000000000",
          "00000900000000",
          "09000000000000",
          "00000000000000",
          "00000000000000"
        ],
        "output": [
          "24000000000000",
          "02400000000000",
          "00000000024000",
          "00000000002400",
          "00000000000000",
          "00000240000000",
          "02400024000000",
          "00240000000000",
          "00000000000000"
        ]
      }
    ]
  },
  {
    "id": "H141",
    "title": "Eight-Way Room Weave",
    "difficulty": "hard",
    "skills": [
      "periodic painting",
      "eight-direction rays",
      "masked propagation"
    ],
    "suggested_staged_path": "It is the room-limited weave again, but the legend is longer and the rays go diagonally too.",
    "written_solution": "Read the three-color legend on the top row. From the seed, draw rays in all eight directions, cycling through the legend colors step by step, and clip the result to the chamber inside the frame.",
    "program_name": "rule_h141",
    "program_source": "def rule_h141(g):\n    h,w=size(g)\n    palette=[v for v in g[0] if v!=0][:3]\n    seed=None\n    for r in range(h):\n        for c in range(w):\n            if g[r][c]==9:\n                seed=(r,c)\n    mask=chamber_from_seed(g, seed, wall=1)\n    out=clone(g)\n    for r,c,v in phase_weave(seed, DIR8, palette, h,w, mask=mask-{seed}):\n        if out[r][c]==0:\n            out[r][c]=v\n    return out\n",
    "train": [
      {
        "input": [
          "02840000000",
          "01111111110",
          "01000000010",
          "01000000010",
          "01000900010",
          "01000000010",
          "01000000010",
          "01111111110",
          "00000000000"
        ],
        "output": [
          "02840000000",
          "01111111110",
          "01080808010",
          "01002220010",
          "01482928410",
          "01002220010",
          "01080808010",
          "01111111110",
          "00000000000"
        ]
      },
      {
        "input": [
          "0367000000",
          "0111111110",
          "0100000010",
          "0100000010",
          "0100000010",
          "0100000010",
          "0109000010",
          "0100000010",
          "0111111110",
          "0000000000"
        ],
        "output": [
          "0367000000",
          "0111111110",
          "0103000310",
          "0107007010",
          "0106060010",
          "0133300010",
          "0139367310",
          "0133300010",
          "0111111110",
          "0000000000"
        ]
      },
      {
        "input": [
          "052400000000",
          "011111111110",
          "010000000010",
          "010000009010",
          "010000000010",
          "010000000010",
          "011111111110",
          "000000000000"
        ],
        "output": [
          "052400000000",
          "011111111110",
          "010000055510",
          "014254259510",
          "010000055510",
          "010000202010",
          "011111111110",
          "000000000000"
        ]
      },
      {
        "input": [
          "074600000",
          "011111110",
          "010000010",
          "010000010",
          "010000010",
          "010000010",
          "010000010",
          "010090010",
          "010000010",
          "011111110",
          "000000000"
        ],
        "output": [
          "074600000",
          "011111110",
          "010040010",
          "010070010",
          "010060010",
          "014040410",
          "010777010",
          "014797410",
          "010777010",
          "011111110",
          "000000000"
        ]
      }
    ],
    "test": [
      {
        "input": [
          "0428000000000",
          "0111111111110",
          "0100000000010",
          "0100000000010",
          "0100000000010",
          "0100000009010",
          "0100000000010",
          "0100000000010",
          "0111111111110",
          "0000000000000"
        ],
        "output": [
          "0428000000000",
          "0111111111110",
          "0100008008010",
          "0100000202010",
          "0100000044410",
          "0148248249410",
          "0100000044410",
          "0100000202010",
          "0111111111110",
          "0000000000000"
        ]
      }
    ]
  },
  {
    "id": "H142",
    "title": "Transform Analogy",
    "difficulty": "hard",
    "skills": [
      "analogy",
      "panel parsing",
      "transform inference"
    ],
    "suggested_staged_path": "Do not memorize a specific transform from one example. Infer which transform turns the first panel into the second, then apply that same transform to the third.",
    "written_solution": "Split the input into three panels. Infer which geometric transform maps panel A\u2019s object to panel B\u2019s object, then apply that same transform to panel C and output the transformed object cropped tight.",
    "program_name": "rule_h142",
    "program_source": "def rule_h142(g):\n    panels=split_by_zero_cols(g)\n    assert len(panels)==3\n    A,B,C=panels\n    A=strip_zero_border(A); B=strip_zero_border(B); C=strip_zero_border(C)\n    code=None\n    for k,tf in TRANSFORMS.items():\n        if eq_grid(strip_zero_border(apply_transform(A,k)), B):\n            code=k; break\n    if code is None:\n        raise ValueError(\"no transform\")\n    return strip_zero_border(apply_transform(C, code))\n",
    "train": [
      {
        "input": [
          "00000000000000000",
          "02200000020007000",
          "00200002220007700",
          "00220002000000700",
          "00000000000000000"
        ],
        "output": [
          "077",
          "770"
        ]
      },
      {
        "input": [
          "33000000330000000",
          "00330033000008800",
          "00030030000008080",
          "00000000000008000",
          "00000000000000000"
        ],
        "output": [
          "088",
          "808",
          "008"
        ]
      },
      {
        "input": [
          "00000000000006600",
          "44000044000000060",
          "04000004000000660",
          "04400004400000000",
          "00000000000000000"
        ],
        "output": [
          "660",
          "006",
          "066"
        ]
      },
      {
        "input": [
          "00000000000000000",
          "05500005500022000",
          "05050005050002200",
          "00550000550000220",
          "00000000000000000"
        ],
        "output": [
          "2200",
          "0220",
          "0022"
        ]
      }
    ],
    "test": [
      {
        "input": [
          "00000000000000000",
          "07700000070008800",
          "00700007700008080",
          "00070007000000800",
          "00000000000000000"
        ],
        "output": [
          "080",
          "808",
          "880"
        ]
      }
    ]
  },
  {
    "id": "H143",
    "title": "Depth-Colored Frames",
    "difficulty": "hard",
    "skills": [
      "nested structure",
      "component ordering",
      "depth assignment"
    ],
    "suggested_staged_path": "Each frame is its own component. What matters is not the original color but how deeply nested the frame is.",
    "written_solution": "The input contains nested rectangular frame components. Recolor the outermost frame with one color, the next frame inward with the next color, and continue by depth while keeping the frame geometry unchanged.",
    "program_name": "rule_h143",
    "program_source": "def rule_h143(g):\n    comps=components(g)\n    # sort outer to inner by bbox area descending\n    comps=sorted(comps, key=lambda comp: ((bbox(comp[\"cells\"])[2]-bbox(comp[\"cells\"])[0]+1)*(bbox(comp[\"cells\"])[3]-bbox(comp[\"cells\"])[1]+1)), reverse=True)\n    out=blank(*size(g),0)\n    for i,comp in enumerate(comps):\n        color=2+i\n        for r,c in comp[\"cells\"]:\n            out[r][c]=color\n    return out\n",
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
          "000000000",
          "011111110",
          "010000010",
          "010111010",
          "010101010",
          "010111010",
          "010000010",
          "011111110",
          "000000000"
        ],
        "output": [
          "000000000",
          "022222220",
          "020000020",
          "020333020",
          "020303020",
          "020333020",
          "020000020",
          "022222220",
          "000000000"
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
          "0000000",
          "0111110",
          "0100010",
          "0101010",
          "0100010",
          "0111110",
          "0000000"
        ],
        "output": [
          "0000000",
          "0222220",
          "0200020",
          "0203020",
          "0200020",
          "0222220",
          "0000000"
        ]
      }
    ],
    "test": [
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
    ]
  },
  {
    "id": "H144",
    "title": "Path Overlap",
    "difficulty": "hard",
    "skills": [
      "routing",
      "pairing by color",
      "overlap resolution"
    ],
    "suggested_staged_path": "Each color defines a pair of terminals. Draw the deterministic L-shaped path for each pair, then resolve collisions with a special overlap color.",
    "written_solution": "For each color, connect its two terminals using the fixed Manhattan L-path rule. Paint each path in its own color, but any cell used by more than one path becomes the overlap color.",
    "program_name": "rule_h144",
    "program_source": "def rule_h144(g):\n    h,w=size(g)\n    out=blank(h,w,0)\n    paths=[]\n    by=defaultdict(list)\n    for r,row in enumerate(g):\n        for c,v in enumerate(row):\n            if v!=0:\n                by[v].append((r,c))\n    for color,pts in by.items():\n        pts=sorted(pts)\n        cells=l_path(pts[0], pts[1])\n        paths.append((color,cells))\n    counts=Counter(cell for _,cells in paths for cell in cells)\n    for color,cells in paths:\n        for r,c in cells:\n            out[r][c]=8 if counts[(r,c)]>1 else color\n    return out\n",
    "train": [
      {
        "input": [
          "0000000000",
          "0200003000",
          "0000000000",
          "0000000000",
          "0000000000",
          "0300002000",
          "0000000000",
          "0000000000"
        ],
        "output": [
          "0000000000",
          "0888888000",
          "0300002000",
          "0300002000",
          "0300002000",
          "0300002000",
          "0000000000",
          "0000000000"
        ]
      },
      {
        "input": [
          "000030000",
          "000000000",
          "002000000",
          "000000000",
          "000000000",
          "000000000",
          "000000030",
          "000020000",
          "000000000"
        ],
        "output": [
          "000033330",
          "000000030",
          "002220030",
          "000020030",
          "000020030",
          "000020030",
          "000020030",
          "000020000",
          "000000000"
        ]
      },
      {
        "input": [
          "000000000000",
          "000030000200",
          "000000000000",
          "000000000000",
          "000000000000",
          "000200000300",
          "000000000000"
        ],
        "output": [
          "000000000000",
          "000288888800",
          "000200000300",
          "000200000300",
          "000200000300",
          "000200000300",
          "000000000000"
        ]
      },
      {
        "input": [
          "0000000000",
          "0000000030",
          "0000000000",
          "0200000000",
          "0000000000",
          "0000000000",
          "0000000000",
          "0000000000",
          "0003000020",
          "0000000000"
        ],
        "output": [
          "0000000000",
          "0003333330",
          "0003000000",
          "0228222220",
          "0003000020",
          "0003000020",
          "0003000020",
          "0003000020",
          "0003000020",
          "0000000000"
        ]
      }
    ],
    "test": [
      {
        "input": [
          "00000000000",
          "00200000000",
          "00000000030",
          "00000000000",
          "00000000000",
          "00000000000",
          "00000000000",
          "00003000020",
          "00000000000"
        ],
        "output": [
          "00000000000",
          "00222222220",
          "00003333380",
          "00003000020",
          "00003000020",
          "00003000020",
          "00003000020",
          "00003000020",
          "00000000000"
        ]
      }
    ]
  },
  {
    "id": "H145",
    "title": "Transform Code Tiling",
    "difficulty": "hard",
    "skills": [
      "matrix-controlled transforms",
      "template tiling",
      "panel parsing"
    ],
    "suggested_staged_path": "The left panel is a template and the right panel is a matrix of commands. The output is a tiled grid of transformed template copies.",
    "written_solution": "Extract the template from the left panel. For each command in the right-hand code matrix, transform the template accordingly and place the result in the matching tile position of the output grid.",
    "program_name": "rule_h145",
    "program_source": "def rule_h145(g):\n    parts=split_by_zero_cols(g)\n    assert len(parts)==2\n    template=strip_zero_border(parts[0])\n    codes=parts[1]\n    mh,mw=size(codes)\n    th,tw=size(template)\n    out=blank(mh*th, mw*tw, 0)\n    for rr in range(mh):\n        for cc in range(mw):\n            code=codes[rr][cc]\n            tf=apply_transform(template, code)\n            tf=strip_zero_border(tf)\n            # assume same square size\n            for r in range(th):\n                for c in range(tw):\n                    v=tf[r][c]\n                    if v!=0:\n                        out[rr*th+r][cc*tw+c]=v\n    return out\n",
    "train": [
      {
        "input": [
          "60012",
          "67034"
        ],
        "output": [
          "6066",
          "6770",
          "7607",
          "0666"
        ]
      },
      {
        "input": [
          "80041",
          "08023"
        ],
        "output": [
          "0880",
          "8008",
          "0880",
          "8008"
        ]
      },
      {
        "input": [
          "23021",
          "20014"
        ],
        "output": [
          "2223",
          "0320",
          "2330",
          "2022"
        ]
      },
      {
        "input": [
          "50032",
          "55041"
        ],
        "output": [
          "5555",
          "0550",
          "0550",
          "5555"
        ]
      }
    ],
    "test": [
      {
        "input": [
          "70024",
          "77031"
        ],
        "output": [
          "7707",
          "7077",
          "7770",
          "0777"
        ]
      }
    ]
  },
  {
    "id": "H146",
    "title": "Sort by Holes and Pack",
    "difficulty": "hard",
    "skills": [
      "hole counting",
      "sorting",
      "packing normalized shapes"
    ],
    "suggested_staged_path": "You need both analysis and rearrangement: count holes first, then crop and reorder the components.",
    "written_solution": "For each component, count its holes, crop it to a tight bounding box, and then sort the components by increasing hole count. Pack the normalized shapes left to right with one blank column between them.",
    "program_name": "rule_h146",
    "program_source": "def rule_h146(g):\n    comps=components(g)\n    items=[]\n    for comp in comps:\n        norm=normalize_component(comp)\n        items.append((hole_count_component(comp[\"cells\"]), len(comp[\"cells\"]), norm))\n    items.sort(key=lambda x:(x[0], x[1]))\n    maxh=max(len(norm) for _,_,norm in items)\n    totalw=sum(len(norm[0]) for _,_,norm in items)+(len(items)-1)\n    out=blank(maxh,totalw,0)\n    x=0\n    for _,_,norm in items:\n        nh,nw=size(norm)\n        for r in range(nh):\n            for c in range(nw):\n                v=norm[r][c]\n                if v!=0:\n                    out[r][x+c]=v\n        x += nw + 1\n    return out\n",
    "train": [
      {
        "input": [
          "000000000000000",
          "022000000000000",
          "022000000000000",
          "000000444000000",
          "000000404000000",
          "000000444006600",
          "000000000000600",
          "000000000000660",
          "000000000000000"
        ],
        "output": [
          "2206600444",
          "2200600404",
          "0000660444"
        ]
      },
      {
        "input": [
          "00000000000000",
          "07777000000000",
          "07007000000000",
          "07007000000000",
          "07777000000000",
          "00000000033300",
          "00000000033300",
          "00000000033300",
          "00000000000000",
          "00000000000000"
        ],
        "output": [
          "33307777",
          "33307007",
          "33307007",
          "00007777"
        ]
      },
      {
        "input": [
          "0000000000000000",
          "0055000000000000",
          "0005000000002220",
          "0005500000002020",
          "0000000088002220",
          "0000000088000000",
          "0000000000000000",
          "0000000000000000"
        ],
        "output": [
          "8805500222",
          "8800500202",
          "0000550222"
        ]
      },
      {
        "input": [
          "0000000000000",
          "0444000000000",
          "0444000000000",
          "0444000000000",
          "0000000666000",
          "0000000606000",
          "0000000666099",
          "0000000000099",
          "0000000000000"
        ],
        "output": [
          "9904440666",
          "9904440606",
          "0004440666"
        ]
      }
    ],
    "test": [
      {
        "input": [
          "0000000000000000",
          "0222200000000000",
          "0200200000000000",
          "0200200000000000",
          "0222200000000000",
          "0000005500000000",
          "0000000500008800",
          "0000000550008800",
          "0000000000000000",
          "0000000000000000"
        ],
        "output": [
          "88055002222",
          "88005002002",
          "00005502002",
          "00000002222"
        ]
      }
    ]
  },
  {
    "id": "H147",
    "title": "Remap Then Transform",
    "difficulty": "hard",
    "skills": [
      "palette permutation",
      "command composition",
      "cropped output"
    ],
    "suggested_staged_path": "Two independent instructions are present: a color mapping and a geometric transform. Apply both.",
    "written_solution": "Read the top-row transform code and the aligned source-to-target color mapping in the first two rows. Recolor the object using that palette permutation, apply the commanded transform, and output the result cropped tight.",
    "program_name": "rule_h147",
    "program_source": "def rule_h147(g):\n    code=g[0][0]\n    src=[v for v in g[0][2:] if v!=0]\n    tgt=[v for v in g[1][2:] if v!=0]\n    mapping=dict(zip(src,tgt))\n    obj=[row[:] for row in g[2:]]\n    obj=crop_bbox(obj)\n    remapped=[[mapping.get(v,v) if v!=0 else 0 for v in row] for row in obj]\n    return strip_zero_border(apply_transform(remapped, code))\n",
    "train": [
      {
        "input": [
          "202300",
          "008600",
          "230000",
          "023000",
          "200000"
        ],
        "output": [
          "808",
          "086",
          "060"
        ]
      },
      {
        "input": [
          "504500",
          "002700",
          "450000",
          "405000",
          "044000"
        ],
        "output": [
          "072",
          "702",
          "220"
        ]
      },
      {
        "input": [
          "306700",
          "003900",
          "670000",
          "607000",
          "006000"
        ],
        "output": [
          "300",
          "903",
          "093"
        ]
      },
      {
        "input": [
          "702300",
          "004800",
          "230000",
          "203000",
          "000300"
        ],
        "output": [
          "440",
          "800",
          "080",
          "008"
        ]
      }
    ],
    "test": [
      {
        "input": [
          "402300",
          "007500",
          "230000",
          "203000",
          "033000"
        ],
        "output": [
          "055",
          "505",
          "770"
        ]
      }
    ]
  }
]''')

RULES = {
    "E141": rule_e141,
    "E142": rule_e142,
    "E143": rule_e143,
    "E144": rule_e144,
    "E145": rule_e145,
    "E146": rule_e146,
    "E147": rule_e147,
    "M141": rule_m141,
    "M142": rule_m142,
    "M143": rule_m143,
    "M144": rule_m144,
    "M145": rule_m145,
    "M146": rule_m146,
    "M147": rule_m147,
    "H141": rule_h141,
    "H142": rule_h142,
    "H143": rule_h143,
    "H144": rule_h144,
    "H145": rule_h145,
    "H146": rule_h146,
    "H147": rule_h147
}

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
