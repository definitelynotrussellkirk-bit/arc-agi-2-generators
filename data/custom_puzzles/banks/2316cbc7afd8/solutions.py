from __future__ import annotations
import json
from typing import List, Tuple

Grid = List[List[int]]
DIR4 = [(-1,0),(1,0),(0,-1),(0,1)]
def blank(h,w,val=0):
    return [[val]*w for _ in range(h)]

def clone(g):
    return [row[:] for row in g]

def size(g):
    return (len(g), len(g[0]) if g else 0)

def in_bounds(g,r,c):
    h,w=size(g)
    return 0<=r<h and 0<=c<w

def bbox(cells):
    rs=[r for r,c in cells]; cs=[c for r,c in cells]
    return min(rs), min(cs), max(rs), max(cs)

def crop_bbox(g,cells=None):
    if cells is None:
        cells=[(r,c) for r,row in enumerate(g) for c,v in enumerate(row) if v!=0]
    if not cells:
        return [[0]]
    r0,c0,r1,c1=bbox(cells)
    return [row[c0:c1+1] for row in g[r0:r1+1]]

def crop_nonzero(g):
    return crop_bbox(g)

def grid_from_strings(rows):
    return [[int(ch) for ch in row] for row in rows]

def strings_from_grid(g):
    return [''.join(str(x) for x in row) for row in g]

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

def anti_transpose(g):
    return rotate180(transpose(g))

def infer_dihedral(a,b,candidates=None):
    if candidates is None:
        candidates = range(1,9)
    for code in candidates:
        try:
            if TRANSFORMS[code](a)==b:
                return code
        except Exception:
            pass
    return None

def components(g, colors=None, exclude=None):
    if exclude is None: exclude=set()
    h,w=size(g)
    seen=set()
    out=[]
    for r in range(h):
        for c in range(w):
            v=g[r][c]
            if v==0 or v in exclude or (colors is not None and v not in colors) or (r,c) in seen:
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
            out.append({"color":v,"cells":cells})
    return out

def draw_rect_border(g, r0,c0,r1,c1, color):
    for c in range(c0,c1+1):
        g[r0][c]=color; g[r1][c]=color
    for r in range(r0,r1+1):
        g[r][c0]=color; g[r][c1]=color
    return g

def hcat(panels, gap=1, fill=0):
    hs=[len(p) for p in panels]
    maxh=max(hs)
    widths=[len(p[0]) if p else 0 for p in panels]
    out=blank(maxh, sum(widths)+gap*(len(panels)-1), fill)
    c=0
    for p in panels:
        h,w=size(p)
        for r in range(h):
            for cc in range(w):
                out[r][c+cc]=p[r][cc]
        c += w+gap
    return out

def vcat(panels, gap=1, fill=0):
    ws=[len(p[0]) for p in panels]
    maxw=max(ws)
    out=blank(sum(len(p) for p in panels)+gap*(len(panels)-1), maxw, fill)
    r0=0
    for p in panels:
        h,w=size(p)
        for r in range(h):
            for c in range(w):
                out[r0+r][c]=p[r][c]
        r0 += h+gap
    return out

def hole_count_component(cells):
    r0,c0,r1,c1=bbox(cells)
    H=r1-r0+3; W=c1-c0+3
    occ=set((r-r0+1,c-c0+1) for r,c in cells)
    seen=set(); holes=0
    for r in range(H):
        for c in range(W):
            if (r,c) in occ or (r,c) in seen:
                continue
            q=[(r,c)]; seen.add((r,c)); touch=False
            while q:
                rr,cc=q.pop()
                if rr in (0,H-1) or cc in (0,W-1):
                    touch=True
                for dr,dc in DIR4:
                    nr,nc=rr+dr,cc+dc
                    if 0<=nr<H and 0<=nc<W and (nr,nc) not in occ and (nr,nc) not in seen:
                        seen.add((nr,nc)); q.append((nr,nc))
            if not touch:
                holes += 1
    return holes

def split_by_blank_cols(g):
    h,w=size(g)
    blank_cols=[c for c in range(w) if all(g[r][c]==0 for r in range(h))]
    panels=[]; start=0
    for c in blank_cols+[w]:
        if c>start:
            panels.append([row[start:c] for row in g])
        start=c+1
    return panels

def split_by_full_color_cols(g, color):
    h,w=size(g)
    divs=[c for c in range(w) if all(g[r][c]==color for r in range(h))]
    panels=[]; start=0
    for c in divs+[w]:
        if c>start:
            panels.append([row[start:c] for row in g])
        start=c+1
    return panels

def split_2x2_panels(g, divider=9):
    h,w=size(g)
    div_rows=[r for r in range(h) if all(v==divider for v in g[r])]
    div_cols=[c for c in range(w) if all(g[r][c]==divider for r in range(h))]
    if len(div_rows)!=1 or len(div_cols)!=1:
        raise ValueError("expected one divider row and col")
    dr,dc=div_rows[0], div_cols[0]
    tl=[row[:dc] for row in g[:dr]]
    tr=[row[dc+1:] for row in g[:dr]]
    bl=[row[:dc] for row in g[dr+1:]]
    br=[row[dc+1:] for row in g[dr+1:]]
    return tl,tr,bl,br

def crop_inside_frame(panel, frame_color=5):
    # panel expected framed with outer border frame_color
    h,w=size(panel)
    # remove outer border if it is frame_color around
    if h>=3 and w>=3 and all(panel[0][c]==frame_color for c in range(w)) and all(panel[h-1][c]==frame_color for c in range(w)) \
       and all(panel[r][0]==frame_color for r in range(h)) and all(panel[r][w-1]==frame_color for r in range(h)):
        return [row[1:w-1] for row in panel[1:h-1]]
    return crop_nonzero(panel)

def draw_line_segment(out, p1, p2, color):
    r1,c1=p1; r2,c2=p2
    if r1==r2:
        for c in range(min(c1,c2), max(c1,c2)+1):
            if out[r1][c]!=5: out[r1][c]=color
    elif c1==c2:
        for r in range(min(r1,r2), max(r1,r2)+1):
            if out[r][c1]!=5: out[r][c1]=color
    else:
        raise ValueError("not orth")
    return out

def canonical_crop(shape):
    best=None
    for code,fn in TRANSFORMS.items():
        gg=fn(shape)
        cc=crop_nonzero(gg)
        s=tuple(strings_from_grid(cc))
        if best is None or s<best[0]:
            best=(s,cc)
    return best[1]

def crop_comp_grid(g, comp):
    return crop_bbox(g, comp["cells"])

TRANSFORMS = {
    1: lambda g: clone(g),
    2: rotate90,
    3: rotate180,
    4: rotate270,
    5: flip_h,
    6: flip_v,
    7: transpose,
    8: anti_transpose,
}

def rule_e106(g):
    a,b,c=split_by_full_color_cols(g,9)
    t=infer_dihedral(a,b)
    return TRANSFORMS[t](c)

def rule_e107(g):
    pts=[(r,c,v) for r,row in enumerate(g) for c,v in enumerate(row) if v!=0]
    if not pts:
        return clone(g)
    color=pts[0][2]
    cells=[(r,c) for r,c,v in pts]
    r0,c0,r1,c1=bbox(cells)
    out=blank(*size(g))
    return draw_rect_border(out,r0,c0,r1,c1,color)

def rule_e108(g):
    best_row=max(range(len(g)), key=lambda r: (sum(v!=0 for v in g[r]), -r))  # tie topmost
    return [g[best_row][:]]

def rule_e109(g):
    comps=components(g)
    by_color={}
    for comp in comps:
        by_color.setdefault(comp["color"], []).append(comp)
    chosen=None
    for color, lst in by_color.items():
        if len(lst)==1:
            chosen=lst[0]; break
    if chosen is None:
        # fallback max unique color
        chosen=max(comps, key=lambda comp:(comp["color"], len(comp["cells"])))
    return crop_bbox(g, chosen["cells"])

def rule_e110(g):
    h,w=size(g)
    # find full divider col (5)
    div=[c for c in range(w) if all(g[r][c]==5 for r in range(h))]
    if not div: return clone(g)
    d=div[0]
    out=clone(g)
    for r in range(h):
        for c in range(w):
            v=g[r][c]
            if c==d or v==0 or v==5: 
                continue
            mc=2*d-c
            if 0<=mc<w and out[r][mc]==0:
                out[r][mc]=v
    return out

def rule_e111(g):
    out=clone(g)
    h,w=size(g)
    changed=True
    while changed:
        changed=False
        for r in range(h-1):
            for c in range(w-1):
                vals=[g[r][c],g[r][c+1],g[r+1][c],g[r+1][c+1]]
                nz=[v for v in vals if v!=0]
                if len(nz)==3 and len(set(nz))==1 and vals.count(0)==1:
                    idx=vals.index(0)
                    rr=r + idx//2
                    cc=c + idx%2
                    out[rr][cc]=nz[0]
                    changed=True
        g=clone(out)
    return out

def rule_e112(g):
    vals=[v for row in g for v in row if v!=0]
    return [vals] if vals else [[0]]

def rule_m106(g):
    panels=split_by_blank_cols(g)  # maybe framed panels separated by blank columns
    # but internal frames don't have blank full cols because frame border nonzero, okay
    a,b,c=panels
    A=crop_inside_frame(a,5)
    B=crop_inside_frame(b,5)
    C=crop_inside_frame(c,5)
    t=infer_dihedral(A,B)
    return TRANSFORMS[t](C)

def rule_m107(g):
    comps=components(g)
    comps_sorted=sorted(comps, key=lambda comp:(-len(comp["cells"]), bbox(comp["cells"])[0], bbox(comp["cells"])[1], comp["color"]))
    crops=[crop_bbox(g, comp["cells"]) for comp in comps_sorted]
    return hcat(crops, gap=1, fill=0)

def rule_m108(g):
    out=clone(g)
    comps=components(g, colors={5})
    for comp in comps:
        cells=comp["cells"]
        r0,c0,r1,c1=bbox(cells)
        # confirm rectangle border
        if all(g[r0][c]==5 for c in range(c0,c1+1)) and all(g[r1][c]==5 for c in range(c0,c1+1)) and all(g[r][c0]==5 for r in range(r0,r1+1)) and all(g[r][c1]==5 for r in range(r0,r1+1)):
            seeds=set(g[r][c] for r in range(r0+1,r1) for c in range(c0+1,c1) if g[r][c] not in (0,5))
            if len(seeds)==1:
                color=next(iter(seeds))
                for r in range(r0+1,r1):
                    for c in range(c0+1,c1):
                        out[r][c]=color
    return out

def rule_m109(g):
    cmd=g[0][0]
    temp=clone(g)
    temp[0][0]=0
    obj=crop_nonzero(temp)
    return TRANSFORMS[cmd](obj)

def rule_m110(g):
    comps=components(g)
    chosen=max(comps, key=lambda comp:(hole_count_component(comp["cells"]), len(comp["cells"]), -bbox(comp["cells"])[0], -bbox(comp["cells"])[1]))
    return crop_bbox(g, chosen["cells"])

def rule_m111(g):
    comps=components(g)
    comps_sorted=sorted(comps, key=lambda comp:(bbox(comp["cells"])[0], bbox(comp["cells"])[1]))
    shapes=[]
    for comp in comps_sorted:
        crop=crop_bbox(g, comp["cells"])
        shape=[[1 if v!=0 else 0 for v in row] for row in crop]
        shapes.append(shape)
    n=len(shapes)
    out=blank(n,n)
    for i in range(n):
        for j in range(n):
            out[i][j]=8 if infer_dihedral(shapes[i], shapes[j]) is not None else 0
    return out

def rule_m112(g):
    h,w=size(g)
    out=clone(g)
    seen=set()
    for r in range(h):
        for c in range(w):
            if g[r][c]==5 or (r,c) in seen:
                continue
            q=[(r,c)]; seen.add((r,c)); region=[]
            seed_colors=set()
            while q:
                rr,cc=q.pop(); region.append((rr,cc))
                if g[rr][cc] not in (0,5):
                    seed_colors.add(g[rr][cc])
                for dr,dc in DIR4:
                    nr,nc=rr+dr,cc+dc
                    if in_bounds(g,nr,nc) and g[nr][nc]!=5 and (nr,nc) not in seen:
                        seen.add((nr,nc)); q.append((nr,nc))
            if len(seed_colors)==1:
                color=next(iter(seed_colors))
                for rr,cc in region:
                    if g[rr][cc]==0:
                        out[rr][cc]=color
    return out

def rule_h106(g):
    tl,tr,bl,br=split_2x2_panels(g, divider=9)
    t_row=infer_dihedral(tl,tr)
    t_col=infer_dihedral(tl,bl)
    return TRANSFORMS[t_row](bl)  # equivalent to col then row on tl -> on bl
    # could also return TRANSFORMS[t_col](tr)

def rule_h107(g):
    h,w=size(g)
    out=clone(g)
    # preserve frame/walls 5
    seeds=[(r,c,v) for r,row in enumerate(g) for c,v in enumerate(row) if v not in (0,5)]
    for r in range(h):
        for c in range(w):
            if g[r][c]==5:
                continue
            if g[r][c]!=0:
                continue
            dists=[(abs(r-sr)+abs(c-sc), color) for sr,sc,color in seeds]
            mind=min(d for d,color in dists)
            colors={color for d,color in dists if d==mind}
            if len(colors)==1:
                out[r][c]=next(iter(colors))
    return out

def rule_h108(g):
    legend=[v for v in g[0] if v not in (0,5)]
    body=[row[:] for row in g[1:]]
    comps=components(body, colors={5})
    rects=[]
    for comp in comps:
        r0,c0,r1,c1=bbox(comp["cells"])
        if all(body[r0][c]==5 for c in range(c0,c1+1)) and all(body[r1][c]==5 for c in range(c0,c1+1)) and all(body[r][c0]==5 for r in range(r0,r1+1)) and all(body[r][c1]==5 for r in range(r0,r1+1)):
            rects.append((r0,c0,r1,c1,comp))
    rects_sorted=sorted(rects, key=lambda x: ((x[2]-x[0]+1)*(x[3]-x[1]+1)), reverse=True)
    out=[row[:] for row in g]
    for i,(r0,c0,r1,c1,comp) in enumerate(rects_sorted):
        color=legend[i] if i<len(legend) else legend[-1]
        for c in range(c0,c1+1):
            out[r0+1][c]=color; out[r1+1][c]=color
        for r in range(r0,r1+1):
            out[r+1][c0]=color; out[r+1][c1]=color
    return out

def rule_h109(g):
    cmd=g[0][0]
    left=[row[0:3] for row in g[1:4]]
    right=[row[4:7] for row in g[1:4]]
    tr=TRANSFORMS[cmd](right)
    out=blank(3,3)
    for r in range(3):
        for c in range(3):
            if left[r][c]!=0 and tr[r][c]!=0:
                out[r][c]=7
    return out

def rule_h110(g):
    pts2=[(r,c) for r,row in enumerate(g) for c,v in enumerate(row) if v==2]
    elbow=[(r,c) for r,row in enumerate(g) for c,v in enumerate(row) if v==3]
    if len(pts2)!=2 or len(elbow)!=1:
        return clone(g)
    a,b=pts2; e=elbow[0]
    out=clone(g)
    # overwrite elbow and terminals with 2 along L legs via elbow coordinates
    draw_line_segment(out, a, (a[0], e[1]), 2)
    draw_line_segment(out, (a[0], e[1]), e, 2)
    draw_line_segment(out, e, (b[0], e[1]), 2)
    draw_line_segment(out, (b[0], e[1]), b, 2)
    out[e[0]][e[1]]=2
    return out

def rule_h111(g):
    legend=[v for v in g[0] if v!=0]
    body=clone(g); body[0]=[0]*len(g[0])
    comps=components(body)
    # map color to canonical crop
    color_to_crop={}
    for comp in comps:
        color=comp["color"]
        crop=crop_comp_grid(g, comp)
        color_to_crop[color]=canonical_crop(crop)
    crops=[color_to_crop[c] for c in legend]
    return hcat(crops, gap=1, fill=0)

def rule_h112(g):
    row_cmds=[g[3][0], g[5][0]]
    col_cmds=[g[0][3], g[0][5]]
    src=[row[3:6] for row in g[3:6]]
    panels=[]
    for rcmd in row_cmds:
        row_panels=[]
        for ccmd in col_cmds:
            panel=TRANSFORMS[ccmd](TRANSFORMS[rcmd](src))
            row_panels.append(panel)
        panels.append(hcat(row_panels,gap=1,fill=0))
    return vcat(panels,gap=1,fill=0)

RULES = {
    'E106': rule_e106,
    'E107': rule_e107,
    'E108': rule_e108,
    'E109': rule_e109,
    'E110': rule_e110,
    'E111': rule_e111,
    'E112': rule_e112,
    'M106': rule_m106,
    'M107': rule_m107,
    'M108': rule_m108,
    'M109': rule_m109,
    'M110': rule_m110,
    'M111': rule_m111,
    'M112': rule_m112,
    'H106': rule_h106,
    'H107': rule_h107,
    'H108': rule_h108,
    'H109': rule_h109,
    'H110': rule_h110,
    'H111': rule_h111,
    'H112': rule_h112
}

PUZZLES = json.loads(r'''
[
  {
    "id": "E106",
    "title": "Three-Panel Transform Transfer",
    "difficulty": "easy",
    "skills": [
      "dihedral transform",
      "panel analogy",
      "motif transfer"
    ],
    "suggested_staged_path": "First isolate the three panels. Infer how the first panel changed into the second, then apply exactly that same transform to the third.",
    "written_solution": "Read the three 3\u00d73 panels as A, B, and C. Infer the dihedral transform that maps A to B, then apply that same transform to C and return only the transformed third panel.",
    "reference_program": "def rule_e106(g):\n    a,b,c=split_by_full_color_cols(g,9)\n    t=infer_dihedral(a,b)\n    return TRANSFORMS[t](c)",
    "train": [
      {
        "input": [
          "12090119030",
          "10090029033",
          "00090009003"
        ],
        "output": [
          "000",
          "033",
          "330"
        ]
      },
      {
        "input": [
          "44090449060",
          "00494009660",
          "04090409600"
        ],
        "output": [
          "060",
          "066",
          "006"
        ]
      },
      {
        "input": [
          "70097709080",
          "77090779008",
          "07090009088"
        ],
        "output": [
          "000",
          "808",
          "088"
        ]
      },
      {
        "input": [
          "03093009120",
          "03393309100",
          "00390309000"
        ],
        "output": [
          "000",
          "001",
          "021"
        ]
      }
    ],
    "test": {
      "input": [
        "08098809440",
        "00898089004",
        "08890009040"
      ],
      "output": [
        "040",
        "404",
        "004"
      ]
    }
  },
  {
    "id": "E107",
    "title": "Rectangle from Three Corners",
    "difficulty": "easy",
    "skills": [
      "bbox",
      "rectangle completion",
      "same-size border drawing"
    ],
    "suggested_staged_path": "Ignore that one corner is missing. Use the bounding box of the colored cells, then draw the full rectangle border of that box.",
    "written_solution": "The three nonzero cells are three corners of one axis-aligned rectangle. Take their bounding box and draw the full border in the same color.",
    "reference_program": "def rule_e107(g):\n    pts=[(r,c,v) for r,row in enumerate(g) for c,v in enumerate(row) if v!=0]\n    if not pts:\n        return clone(g)\n    color=pts[0][2]\n    cells=[(r,c) for r,c,v in pts]\n    r0,c0,r1,c1=bbox(cells)\n    out=blank(*size(g))\n    return draw_rect_border(out,r0,c0,r1,c1,color)",
    "train": [
      {
        "input": [
          "0000000",
          "0200020",
          "0000000",
          "0000000",
          "0000000",
          "0200000",
          "0000000"
        ],
        "output": [
          "0000000",
          "0222220",
          "0200020",
          "0200020",
          "0200020",
          "0222220",
          "0000000"
        ]
      },
      {
        "input": [
          "00000000",
          "00000000",
          "00300030",
          "00000000",
          "00000000",
          "00000000",
          "00000030",
          "00000000"
        ],
        "output": [
          "00000000",
          "00000000",
          "00333330",
          "00300030",
          "00300030",
          "00300030",
          "00333330",
          "00000000"
        ]
      },
      {
        "input": [
          "000000000",
          "000400000",
          "000000000",
          "000000000",
          "000400040",
          "000000000"
        ],
        "output": [
          "000000000",
          "000444440",
          "000400040",
          "000400040",
          "000444440",
          "000000000"
        ]
      },
      {
        "input": [
          "0000000000",
          "0000000600",
          "0000000000",
          "0000000000",
          "0000000000",
          "0060000600",
          "0000000000"
        ],
        "output": [
          "0000000000",
          "0066666600",
          "0060000600",
          "0060000600",
          "0060000600",
          "0066666600",
          "0000000000"
        ]
      }
    ],
    "test": {
      "input": [
        "000000000",
        "000000000",
        "080000000",
        "000000000",
        "000000000",
        "000000000",
        "080000800",
        "000000000",
        "000000000"
      ],
      "output": [
        "000000000",
        "000000000",
        "088888800",
        "080000800",
        "080000800",
        "080000800",
        "088888800",
        "000000000",
        "000000000"
      ]
    }
  },
  {
    "id": "E108",
    "title": "Extract the Densest Row",
    "difficulty": "easy",
    "skills": [
      "row statistics",
      "selection",
      "dynamic-size output"
    ],
    "suggested_staged_path": "Count how many nonzero cells each row contains. Keep only the row with the largest count and output that row by itself.",
    "written_solution": "Scan the rows and count nonzero cells. Select the row with the highest count, breaking ties by the earliest row, and output that row alone.",
    "reference_program": "def rule_e108(g):\n    best_row=max(range(len(g)), key=lambda r: (sum(v!=0 for v in g[r]), -r))  # tie topmost\n    return [g[best_row][:]]",
    "train": [
      {
        "input": [
          "0000000",
          "0202000",
          "0033300",
          "0000000",
          "4000004"
        ],
        "output": [
          "0033300"
        ]
      },
      {
        "input": [
          "1000100",
          "0222200",
          "0030300",
          "0000000",
          "0404040"
        ],
        "output": [
          "0222200"
        ]
      },
      {
        "input": [
          "000000",
          "005500",
          "066660",
          "000070",
          "700007"
        ],
        "output": [
          "066660"
        ]
      },
      {
        "input": [
          "8000080",
          "0000000",
          "0909090",
          "0000000",
          "0077700"
        ],
        "output": [
          "0909090"
        ]
      }
    ],
    "test": {
      "input": [
        "00000000",
        "02020200",
        "00330030",
        "00000000",
        "44444000"
      ],
      "output": [
        "44444000"
      ]
    }
  },
  {
    "id": "E109",
    "title": "Crop the Unique-Color Object",
    "difficulty": "easy",
    "skills": [
      "component counting by color",
      "object selection",
      "cropping"
    ],
    "suggested_staged_path": "Group components by color. Find the color that appears in exactly one component, then crop tightly to that object.",
    "written_solution": "Count connected components separately for each color. Exactly one color occurs only once; crop to that lone object\u2019s bounding box and output it.",
    "reference_program": "def rule_e109(g):\n    comps=components(g)\n    by_color={}\n    for comp in comps:\n        by_color.setdefault(comp[\"color\"], []).append(comp)\n    chosen=None\n    for color, lst in by_color.items():\n        if len(lst)==1:\n            chosen=lst[0]; break\n    if chosen is None:\n        # fallback max unique color\n        chosen=max(comps, key=lambda comp:(comp[\"color\"], len(comp[\"cells\"])))\n    return crop_bbox(g, chosen[\"cells\"])",
    "train": [
      {
        "input": [
          "0000000000",
          "0220000300",
          "0000000000",
          "0000400000",
          "0000440000",
          "0200000300",
          "0000000000"
        ],
        "output": [
          "40",
          "44"
        ]
      },
      {
        "input": [
          "0000000000",
          "0200000500",
          "0000000500",
          "0000700000",
          "0000770000",
          "0000070050",
          "0220000000",
          "0000000000"
        ],
        "output": [
          "70",
          "77",
          "07"
        ]
      },
      {
        "input": [
          "00000000000",
          "03000000400",
          "03000000000",
          "00006600000",
          "00000600000",
          "03000000440",
          "00000000000"
        ],
        "output": [
          "66",
          "06"
        ]
      },
      {
        "input": [
          "000000000000",
          "002200000000",
          "000000000800",
          "000006000000",
          "000006600000",
          "000000600800",
          "002000000000",
          "000000000000"
        ],
        "output": [
          "60",
          "66",
          "06"
        ]
      }
    ],
    "test": {
      "input": [
        "0000000000",
        "0400000300",
        "0000900000",
        "0000990000",
        "0000090000",
        "0440000300",
        "0000000000"
      ],
      "output": [
        "90",
        "99",
        "09"
      ]
    }
  },
  {
    "id": "E110",
    "title": "Reflect Across the Guide Bar",
    "difficulty": "easy",
    "skills": [
      "reflection",
      "divider detection",
      "same-size completion"
    ],
    "suggested_staged_path": "Find the full vertical guide bar. Mirror every nonzero non-guide cell across that column into the empty side.",
    "written_solution": "The solid column of 5s is a mirror guide. Reflect the existing pattern across it, preserving the original cells and the guide itself.",
    "reference_program": "def rule_e110(g):\n    h,w=size(g)\n    # find full divider col (5)\n    div=[c for c in range(w) if all(g[r][c]==5 for r in range(h))]\n    if not div: return clone(g)\n    d=div[0]\n    out=clone(g)\n    for r in range(h):\n        for c in range(w):\n            v=g[r][c]\n            if c==d or v==0 or v==5: \n                continue\n            mc=2*d-c\n            if 0<=mc<w and out[r][mc]==0:\n                out[r][mc]=v\n    return out",
    "train": [
      {
        "input": [
          "0005000",
          "0205000",
          "0025000",
          "0005000",
          "0405000",
          "0045000",
          "0005000"
        ],
        "output": [
          "0005000",
          "0205020",
          "0025200",
          "0005000",
          "0405040",
          "0045400",
          "0005000"
        ]
      },
      {
        "input": [
          "000050000",
          "000050030",
          "000050300",
          "000050030",
          "000050000",
          "000050600",
          "000050000"
        ],
        "output": [
          "000050000",
          "030050030",
          "003050300",
          "030050030",
          "000050000",
          "006050600",
          "000050000"
        ]
      },
      {
        "input": [
          "000050000",
          "070050000",
          "007050000",
          "070050000",
          "000050000",
          "008050000",
          "080050000",
          "000050000"
        ],
        "output": [
          "000050000",
          "070050070",
          "007050700",
          "070050070",
          "000050000",
          "008050800",
          "080050080",
          "000050000"
        ]
      },
      {
        "input": [
          "0005000",
          "0005020",
          "0005200",
          "0005000",
          "0005040",
          "0005400",
          "0005000"
        ],
        "output": [
          "0005000",
          "0205020",
          "0025200",
          "0005000",
          "0405040",
          "0045400",
          "0005000"
        ]
      }
    ],
    "test": {
      "input": [
        "000050000",
        "000050000",
        "006050300",
        "000653000",
        "006050000",
        "000050000",
        "008050000",
        "000850000",
        "000050000"
      ],
      "output": [
        "000050000",
        "000050000",
        "006050300",
        "000653000",
        "006050600",
        "000050000",
        "008050800",
        "000858000",
        "000050000"
      ]
    }
  },
  {
    "id": "E111",
    "title": "Finish the 2\u00d72 Squares",
    "difficulty": "easy",
    "skills": [
      "local completion",
      "2x2 pattern",
      "same-size repair"
    ],
    "suggested_staged_path": "Scan every 2\u00d72 window. Whenever three cells are the same color and the fourth is empty, fill the missing corner.",
    "written_solution": "Each target pattern is an almost-complete 2\u00d72 monochrome block. Fill the missing cell wherever a 2\u00d72 window has three equal nonzero cells and one zero.",
    "reference_program": "def rule_e111(g):\n    out=clone(g)\n    h,w=size(g)\n    changed=True\n    while changed:\n        changed=False\n        for r in range(h-1):\n            for c in range(w-1):\n                vals=[g[r][c],g[r][c+1],g[r+1][c],g[r+1][c+1]]\n                nz=[v for v in vals if v!=0]\n                if len(nz)==3 and len(set(nz))==1 and vals.count(0)==1:\n                    idx=vals.index(0)\n                    rr=r + idx//2\n                    cc=c + idx%2\n                    out[rr][cc]=nz[0]\n                    changed=True\n        g=clone(out)\n    return out",
    "train": [
      {
        "input": [
          "00000000",
          "00200000",
          "02200000",
          "00000440",
          "00000400",
          "00000000"
        ],
        "output": [
          "00000000",
          "02200000",
          "02200000",
          "00000440",
          "00000440",
          "00000000"
        ]
      },
      {
        "input": [
          "0000000",
          "0003000",
          "0003300",
          "0000000",
          "0660000",
          "0060000",
          "0000000"
        ],
        "output": [
          "0000000",
          "0003300",
          "0003300",
          "0000000",
          "0660000",
          "0660000",
          "0000000"
        ]
      },
      {
        "input": [
          "000000000",
          "000000770",
          "000000070",
          "000204000",
          "002204400",
          "000000000"
        ],
        "output": [
          "000000000",
          "000000770",
          "000000770",
          "002204400",
          "002204400",
          "000000000"
        ]
      },
      {
        "input": [
          "00000000",
          "00000000",
          "08800000",
          "08000000",
          "00000050",
          "00000550",
          "00000000"
        ],
        "output": [
          "00000000",
          "00000000",
          "08800000",
          "08800000",
          "00000550",
          "00000550",
          "00000000"
        ]
      }
    ],
    "test": {
      "input": [
        "00000000",
        "06000000",
        "06600000",
        "00000000",
        "00003300",
        "00200300",
        "02200000",
        "00000000"
      ],
      "output": [
        "00000000",
        "06600000",
        "06600000",
        "00000000",
        "00003300",
        "02203300",
        "02200000",
        "00000000"
      ]
    }
  },
  {
    "id": "E112",
    "title": "Row-Major Compaction",
    "difficulty": "easy",
    "skills": [
      "serialization",
      "row-major order",
      "dynamic-size output"
    ],
    "suggested_staged_path": "Ignore zeros. Read the remaining colors left-to-right, top-to-bottom, then write them into one output row.",
    "written_solution": "Traverse the input in row-major order, collect all nonzero values, and output them as a single compact row in that same order.",
    "reference_program": "def rule_e112(g):\n    vals=[v for row in g for v in row if v!=0]\n    return [vals] if vals else [[0]]",
    "train": [
      {
        "input": [
          "0000000",
          "0200003",
          "0004000",
          "0050000",
          "0000006"
        ],
        "output": [
          "23456"
        ]
      },
      {
        "input": [
          "1000000",
          "0002000",
          "0000000",
          "0304000",
          "0005000"
        ],
        "output": [
          "12345"
        ]
      },
      {
        "input": [
          "000000",
          "600700",
          "000000",
          "080000",
          "000900"
        ],
        "output": [
          "6789"
        ]
      },
      {
        "input": [
          "2000002",
          "0003000",
          "0000000",
          "0400000",
          "0000050"
        ],
        "output": [
          "22345"
        ]
      }
    ],
    "test": {
      "input": [
        "00000000",
        "02030400",
        "00000000",
        "50060070",
        "00000000"
      ],
      "output": [
        "234567"
      ]
    }
  },
  {
    "id": "M106",
    "title": "Framed Transform Transfer",
    "difficulty": "medium",
    "skills": [
      "infer_dihedral",
      "frame extraction",
      "panel analogy"
    ],
    "suggested_staged_path": "First strip the frame from each panel and compare only the interiors. Infer the transform from the first interior to the second, then apply it to the third interior.",
    "written_solution": "Each large panel is only a frame around a smaller motif. Remove the frames, infer the dihedral transform from the first interior to the second, and apply it to the third interior.",
    "reference_program": "def rule_m106(g):\n    panels=split_by_blank_cols(g)  # maybe framed panels separated by blank columns\n    # but internal frames don't have blank full cols because frame border nonzero, okay\n    a,b,c=panels\n    A=crop_inside_frame(a,5)\n    B=crop_inside_frame(b,5)\n    C=crop_inside_frame(c,5)\n    t=infer_dihedral(A,B)\n    return TRANSFORMS[t](C)",
    "train": [
      {
        "input": [
          "55555505555550555555",
          "51200505001150503005",
          "51000505010250503305",
          "50110505010050500305",
          "50000505000050500005",
          "55555505555550555555"
        ],
        "output": [
          "0000",
          "0033",
          "0330",
          "0000"
        ]
      },
      {
        "input": [
          "55555505555550555555",
          "54400505004450550005",
          "50040505040050555005",
          "50440505044050505005",
          "50000505000050500505",
          "55555505555550555555"
        ],
        "output": [
          "0005",
          "0055",
          "0050",
          "0500"
        ]
      },
      {
        "input": [
          "55555505555550555555",
          "50600505066050570005",
          "56600505660050507705",
          "56000505000050500705",
          "50000505000050500005",
          "55555505555550555555"
        ],
        "output": [
          "7000",
          "0700",
          "0770",
          "0000"
        ]
      },
      {
        "input": [
          "55555505555550555555",
          "50300505000050512005",
          "50330505030050510005",
          "50030505033050501105",
          "50000505003050500005",
          "55555505555550555555"
        ],
        "output": [
          "0000",
          "0110",
          "0001",
          "0021"
        ]
      }
    ],
    "test": {
      "input": [
        "55555505555550555555",
        "57000505000050544005",
        "50770505077050500405",
        "50070505007050504405",
        "50000505000750500005",
        "55555505555550555555"
      ],
      "output": [
        "0000",
        "0440",
        "0404",
        "0004"
      ]
    }
  },
  {
    "id": "M107",
    "title": "Area-Sorted Component Packing",
    "difficulty": "medium",
    "skills": [
      "connected components",
      "area ranking",
      "packing"
    ],
    "suggested_staged_path": "Split the image into separate objects and crop each one. Sort the crops by area descending, then pack them left-to-right with one blank column between them.",
    "written_solution": "Find every connected component, crop each to its own bounding box, sort by component area from largest to smallest, and concatenate the crops in that order.",
    "reference_program": "def rule_m107(g):\n    comps=components(g)\n    comps_sorted=sorted(comps, key=lambda comp:(-len(comp[\"cells\"]), bbox(comp[\"cells\"])[0], bbox(comp[\"cells\"])[1], comp[\"color\"]))\n    crops=[crop_bbox(g, comp[\"cells\"]) for comp in comps_sorted]\n    return hcat(crops, gap=1, fill=0)",
    "train": [
      {
        "input": [
          "00000000000000",
          "02000033300000",
          "02200003000000",
          "00000000000000",
          "00000000004400",
          "00000000004400",
          "00000000000000",
          "00000000000000"
        ],
        "output": [
          "333044020",
          "030044022"
        ]
      },
      {
        "input": [
          "000000000000000",
          "070000000000000",
          "070000044000000",
          "077000044000000",
          "000000000000000",
          "000000000000000",
          "000000000033330",
          "000000000000000",
          "000000000000000"
        ],
        "output": [
          "7004403333",
          "7004400000",
          "7700000000"
        ]
      },
      {
        "input": [
          "00000000000000",
          "08880000000000",
          "00080000000600",
          "00000000006660",
          "00000020000000",
          "00000022000000",
          "00000000000000",
          "00000000000000"
        ],
        "output": [
          "8880060020",
          "0080666022"
        ]
      },
      {
        "input": [
          "0000000000000000",
          "0440000000000000",
          "0440000000033300",
          "0000000000003000",
          "0000007000000000",
          "0000007000000000",
          "0000007700000000",
          "0000000000000000",
          "0000000000000000"
        ],
        "output": [
          "440333070",
          "440030070",
          "000000077"
        ]
      }
    ],
    "test": {
      "input": [
        "000000000000000",
        "020000000000000",
        "022000000044000",
        "000008880044000",
        "000000080000000",
        "000000000000000",
        "000000000000000",
        "000000000000000"
      ],
      "output": [
        "440888020",
        "440008022"
      ]
    }
  },
  {
    "id": "M108",
    "title": "Seeded Frame Fill",
    "difficulty": "medium",
    "skills": [
      "frame detection",
      "seed propagation",
      "same-size fill"
    ],
    "suggested_staged_path": "Detect each rectangular frame of 5s. Read the single seed color inside, then fill the interior of that frame with the seed color.",
    "written_solution": "Each 5-colored rectangle is a frame containing one seed. Preserve the border and flood the interior with that seed color.",
    "reference_program": "def rule_m108(g):\n    out=clone(g)\n    comps=components(g, colors={5})\n    for comp in comps:\n        cells=comp[\"cells\"]\n        r0,c0,r1,c1=bbox(cells)\n        # confirm rectangle border\n        if all(g[r0][c]==5 for c in range(c0,c1+1)) and all(g[r1][c]==5 for c in range(c0,c1+1)) and all(g[r][c0]==5 for r in range(r0,r1+1)) and all(g[r][c1]==5 for r in range(r0,r1+1)):\n            seeds=set(g[r][c] for r in range(r0+1,r1) for c in range(c0+1,c1) if g[r][c] not in (0,5))\n            if len(seeds)==1:\n                color=next(iter(seeds))\n                for r in range(r0+1,r1):\n                    for c in range(c0+1,c1):\n                        out[r][c]=color\n    return out",
    "train": [
      {
        "input": [
          "00000000000000",
          "05555000555550",
          "05205000500050",
          "05005000503050",
          "05555000500050",
          "00000000555550",
          "00000000000000",
          "00000000000000",
          "00000000000000"
        ],
        "output": [
          "00000000000000",
          "05555000555550",
          "05225000533350",
          "05225000533350",
          "05555000533350",
          "00000000555550",
          "00000000000000",
          "00000000000000",
          "00000000000000"
        ]
      },
      {
        "input": [
          "000000000000000",
          "055555000000000",
          "050005000555550",
          "050405000500050",
          "050005000500050",
          "055555000507050",
          "000000000500050",
          "000000000555550",
          "000000000000000",
          "000000000000000"
        ],
        "output": [
          "000000000000000",
          "055555000000000",
          "054445000555550",
          "054445000577750",
          "054445000577750",
          "055555000577750",
          "000000000577750",
          "000000000555550",
          "000000000000000",
          "000000000000000"
        ]
      },
      {
        "input": [
          "0000000000000000",
          "0055555005555550",
          "0050605005000050",
          "0050005005000050",
          "0055555005003050",
          "0000000005000050",
          "0000000005555550",
          "0000000000000000",
          "0000000000000000"
        ],
        "output": [
          "0000000000000000",
          "0055555005555550",
          "0056665005333350",
          "0056665005333350",
          "0055555005333350",
          "0000000005333350",
          "0000000005555550",
          "0000000000000000",
          "0000000000000000"
        ]
      },
      {
        "input": [
          "00000000000000",
          "00000000555550",
          "05555000500050",
          "05005000502050",
          "05805000500050",
          "05005000555550",
          "05005000000000",
          "05555000000000",
          "00000000000000",
          "00000000000000"
        ],
        "output": [
          "00000000000000",
          "00000000555550",
          "05555000522250",
          "05885000522250",
          "05885000522250",
          "05885000555550",
          "05885000000000",
          "05555000000000",
          "00000000000000",
          "00000000000000"
        ]
      }
    ],
    "test": {
      "input": [
        "0000000000000000",
        "0555550000000000",
        "0503050000000000",
        "0500050005555550",
        "0555550005000050",
        "0000000005006050",
        "0000000005000050",
        "0000000005000050",
        "0000000005555550",
        "0000000000000000"
      ],
      "output": [
        "0000000000000000",
        "0555550000000000",
        "0533350000000000",
        "0533350005555550",
        "0555550005666650",
        "0000000005666650",
        "0000000005666650",
        "0000000005666650",
        "0000000005555550",
        "0000000000000000"
      ]
    }
  },
  {
    "id": "M109",
    "title": "Token-Selected Object Rotation",
    "difficulty": "medium",
    "skills": [
      "command token",
      "cropping",
      "rotation"
    ],
    "suggested_staged_path": "Read the command token first. Then ignore it, crop the remaining object, and rotate it according to the token.",
    "written_solution": "The top-left token selects one of the basic rotations. Remove the token from consideration, crop the object, and rotate the crop as commanded.",
    "reference_program": "def rule_m109(g):\n    cmd=g[0][0]\n    temp=clone(g)\n    temp[0][0]=0\n    obj=crop_nonzero(temp)\n    return TRANSFORMS[cmd](obj)",
    "train": [
      {
        "input": [
          "20000000",
          "00000000",
          "00002000",
          "00002200",
          "00000000",
          "00000000",
          "00000000"
        ],
        "output": [
          "22",
          "20"
        ]
      },
      {
        "input": [
          "3000000",
          "0000000",
          "0030000",
          "0033300",
          "0003000",
          "0000000",
          "0000000"
        ],
        "output": [
          "030",
          "333",
          "003"
        ]
      },
      {
        "input": [
          "40000000",
          "00000000",
          "00044000",
          "00004000",
          "00044000",
          "00000000",
          "00000000",
          "00000000"
        ],
        "output": [
          "404",
          "444"
        ]
      },
      {
        "input": [
          "10000000",
          "00000000",
          "00000000",
          "00050000",
          "00055000",
          "00005000",
          "00000000",
          "00000000"
        ],
        "output": [
          "50",
          "55",
          "05"
        ]
      }
    ],
    "test": {
      "input": [
        "20000000",
        "00000000",
        "00066000",
        "00060000",
        "00066000",
        "00000000",
        "00000000",
        "00000000"
      ],
      "output": [
        "666",
        "606"
      ]
    }
  },
  {
    "id": "M110",
    "title": "Crop the Most-Holed Object",
    "difficulty": "medium",
    "skills": [
      "topology",
      "hole counting",
      "object selection"
    ],
    "suggested_staged_path": "Separate the components, then compare how many enclosed holes each has. Output the tight crop of the component with the highest hole count.",
    "written_solution": "Among the components, one has the most enclosed voids. Count holes per component and crop to the maximal one.",
    "reference_program": "def rule_m110(g):\n    comps=components(g)\n    chosen=max(comps, key=lambda comp:(hole_count_component(comp[\"cells\"]), len(comp[\"cells\"]), -bbox(comp[\"cells\"])[0], -bbox(comp[\"cells\"])[1]))\n    return crop_bbox(g, chosen[\"cells\"])",
    "train": [
      {
        "input": [
          "000000000000000000",
          "033000444406666666",
          "033300400406006006",
          "000000400406006006",
          "000000444406006006",
          "000000000006666666",
          "000000000000000000",
          "000000000000000000",
          "000000000000000000"
        ],
        "output": [
          "6666666",
          "6006006",
          "6006006",
          "6006006",
          "6666666"
        ]
      },
      {
        "input": [
          "000000000000000000",
          "044440000000000000",
          "040040006666666000",
          "040040006006006000",
          "044440006006006000",
          "000000006006006000",
          "000000006666663300",
          "000000000000003330",
          "000000000000000000",
          "000000000000000000"
        ],
        "output": [
          "6666666",
          "6006006",
          "6006006",
          "6006006",
          "6666663"
        ]
      },
      {
        "input": [
          "0000000000000000000",
          "0666666600330000000",
          "0600600600333000000",
          "0600600600000000000",
          "0600600600000044440",
          "0666666600000040040",
          "0000000000000040040",
          "0000000000000044440",
          "0000000000000000000"
        ],
        "output": [
          "6666666",
          "6006006",
          "6006006",
          "6006006",
          "6666666"
        ]
      },
      {
        "input": [
          "00000000000000000000",
          "03300000000000000000",
          "03330006666666000000",
          "00000006006006000000",
          "00000006006006000000",
          "00000006006006044440",
          "00000006666666040040",
          "00000000000000040040",
          "00000000000000044440",
          "00000000000000000000"
        ],
        "output": [
          "6666666",
          "6006006",
          "6006006",
          "6006006",
          "6666666"
        ]
      }
    ],
    "test": {
      "input": [
        "000000000000000000",
        "044440000066666660",
        "040040000060060060",
        "040040000060060060",
        "044440003360060060",
        "000000003366666660",
        "000000000000000000",
        "000000000000000000",
        "000000000000000000"
      ],
      "output": [
        "6666666",
        "6006006",
        "6006006",
        "6006006",
        "6666666"
      ]
    }
  },
  {
    "id": "M111",
    "title": "Dihedral Shape-Equivalence Matrix",
    "difficulty": "medium",
    "skills": [
      "shape normalization",
      "dihedral equivalence",
      "relational output"
    ],
    "suggested_staged_path": "Order the three objects by position, ignore color, and compare their shapes up to rotation and reflection. Mark matches in a 3\u00d73 matrix.",
    "written_solution": "Treat each object as a binary shape. After ordering them by location, fill a 3\u00d73 matrix with 8 wherever two shapes are equivalent under a dihedral transform, otherwise 0.",
    "reference_program": "def rule_m111(g):\n    comps=components(g)\n    comps_sorted=sorted(comps, key=lambda comp:(bbox(comp[\"cells\"])[0], bbox(comp[\"cells\"])[1]))\n    shapes=[]\n    for comp in comps_sorted:\n        crop=crop_bbox(g, comp[\"cells\"])\n        shape=[[1 if v!=0 else 0 for v in row] for row in crop]\n        shapes.append(shape)\n    n=len(shapes)\n    out=blank(n,n)\n    for i in range(n):\n        for j in range(n):\n            out[i][j]=8 if infer_dihedral(shapes[i], shapes[j]) is not None else 0\n    return out",
    "train": [
      {
        "input": [
          "000000000000000",
          "020000033000000",
          "022000030000000",
          "000000000000000",
          "000000000004400",
          "000000000004400",
          "000000000000000",
          "000000000000000"
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
          "022200000000000",
          "002000006000000",
          "000000006600000",
          "000000006000440",
          "000000000000400",
          "000000000000000",
          "000000000000000"
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
          "077000000000000",
          "077000000000000",
          "000000030000000",
          "000000033004400",
          "000000000000400",
          "000000000000000",
          "000000000000000"
        ],
        "output": [
          "800",
          "088",
          "088"
        ]
      },
      {
        "input": [
          "000000000000000",
          "022000000000000",
          "020000005500000",
          "000000000500000",
          "000000000000880",
          "000000000000880",
          "000000000000000",
          "000000000000000"
        ],
        "output": [
          "880",
          "880",
          "008"
        ]
      }
    ],
    "test": {
      "input": [
        "000000000000000",
        "044400000000000",
        "004000000000000",
        "000000006000000",
        "000000006600200",
        "000000000002220",
        "000000000000000",
        "000000000000000"
      ],
      "output": [
        "808",
        "080",
        "808"
      ]
    }
  },
  {
    "id": "M112",
    "title": "Chamber Flood Fill",
    "difficulty": "medium",
    "skills": [
      "region segmentation",
      "wall handling",
      "seed fill"
    ],
    "suggested_staged_path": "Use the 5s as walls to partition the board into chambers. Any chamber with a single seed color gets filled with that color.",
    "written_solution": "The wall color partitions the board. For each connected non-wall chamber, if all nonzero cells inside share one color, fill the empty cells of that chamber with that color.",
    "reference_program": "def rule_m112(g):\n    h,w=size(g)\n    out=clone(g)\n    seen=set()\n    for r in range(h):\n        for c in range(w):\n            if g[r][c]==5 or (r,c) in seen:\n                continue\n            q=[(r,c)]; seen.add((r,c)); region=[]\n            seed_colors=set()\n            while q:\n                rr,cc=q.pop(); region.append((rr,cc))\n                if g[rr][cc] not in (0,5):\n                    seed_colors.add(g[rr][cc])\n                for dr,dc in DIR4:\n                    nr,nc=rr+dr,cc+dc\n                    if in_bounds(g,nr,nc) and g[nr][nc]!=5 and (nr,nc) not in seen:\n                        seen.add((nr,nc)); q.append((nr,nc))\n            if len(seed_colors)==1:\n                color=next(iter(seed_colors))\n                for rr,cc in region:\n                    if g[rr][cc]==0:\n                        out[rr][cc]=color\n    return out",
    "train": [
      {
        "input": [
          "55555555555",
          "50000500005",
          "50200500005",
          "50000500005",
          "50000500005",
          "50000500005",
          "50000500305",
          "50000500005",
          "55555555555"
        ],
        "output": [
          "55555555555",
          "52222533335",
          "52222533335",
          "52222533335",
          "52222533335",
          "52222533335",
          "52222533335",
          "52222533335",
          "55555555555"
        ]
      },
      {
        "input": [
          "555555555555",
          "500000000005",
          "500400000005",
          "500000000005",
          "555555555555",
          "500000000005",
          "500000007005",
          "500000000005",
          "555555555555"
        ],
        "output": [
          "555555555555",
          "544444444445",
          "544444444445",
          "544444444445",
          "555555555555",
          "577777777775",
          "577777777775",
          "577777777775",
          "555555555555"
        ]
      },
      {
        "input": [
          "555555555555",
          "500050005005",
          "506050005005",
          "500050005005",
          "500050005005",
          "500050305005",
          "500050005005",
          "500050005085",
          "500050005005",
          "555555555555"
        ],
        "output": [
          "555555555555",
          "566653335885",
          "566653335885",
          "566653335885",
          "566653335885",
          "566653335885",
          "566653335885",
          "566653335885",
          "566653335885",
          "555555555555"
        ]
      },
      {
        "input": [
          "5555555555555",
          "5000005000005",
          "5020005004005",
          "5000005000005",
          "5555555555555",
          "5000005000005",
          "5006005000805",
          "5000005000005",
          "5555555555555"
        ],
        "output": [
          "5555555555555",
          "5222225444445",
          "5222225444445",
          "5222225444445",
          "5555555555555",
          "5666665888885",
          "5666665888885",
          "5666665888885",
          "5555555555555"
        ]
      }
    ],
    "test": {
      "input": [
        "555555555555",
        "500005000005",
        "503005000005",
        "500005000005",
        "500005000005",
        "500005000005",
        "500005000005",
        "500005007005",
        "500005000005",
        "555555555555"
      ],
      "output": [
        "555555555555",
        "533335777775",
        "533335777775",
        "533335777775",
        "533335777775",
        "533335777775",
        "533335777775",
        "533335777775",
        "533335777775",
        "555555555555"
      ]
    }
  },
  {
    "id": "H106",
    "title": "Two-Axis Analogy Mosaic",
    "difficulty": "hard",
    "skills": [
      "dual analogy",
      "infer_dihedral",
      "2x2 panel reasoning"
    ],
    "suggested_staged_path": "Infer the horizontal transform from the top row and the vertical transform from the left column. Use them together to generate the missing bottom-right panel.",
    "written_solution": "The four panels form an analogy grid: top-left maps to top-right by one transform, and top-left maps to bottom-left by another. Apply the row transform to the bottom-left panel to produce the missing result.",
    "reference_program": "def rule_h106(g):\n    tl,tr,bl,br=split_2x2_panels(g, divider=9)\n    t_row=infer_dihedral(tl,tr)\n    t_col=infer_dihedral(tl,bl)\n    return TRANSFORMS[t_row](bl)  # equivalent to col then row on tl -> on bl\n    # could also return TRANSFORMS[t_col](tr)",
    "train": [
      {
        "input": [
          "1209011",
          "1009002",
          "0009000",
          "9999999",
          "0219000",
          "0019000",
          "0009000"
        ],
        "output": [
          "000",
          "002",
          "011"
        ]
      },
      {
        "input": [
          "0309300",
          "0339330",
          "0039030",
          "9999999",
          "0009000",
          "3309000",
          "0339000"
        ],
        "output": [
          "330",
          "033",
          "000"
        ]
      },
      {
        "input": [
          "4409044",
          "0049400",
          "0409040",
          "9999999",
          "0409000",
          "0049000",
          "4409000"
        ],
        "output": [
          "040",
          "400",
          "044"
        ]
      },
      {
        "input": [
          "7009000",
          "7709770",
          "0709077",
          "9999999",
          "0779000",
          "7709000",
          "0009000"
        ],
        "output": [
          "007",
          "077",
          "070"
        ]
      }
    ],
    "test": {
      "input": [
        "0809000",
        "0089808",
        "0889088",
        "9999999",
        "8809000",
        "8009000",
        "0809000"
      ],
      "output": [
        "880",
        "808",
        "000"
      ]
    }
  },
  {
    "id": "H107",
    "title": "Manhattan Voronoi Frame",
    "difficulty": "hard",
    "skills": [
      "distance fields",
      "partitioning",
      "tie handling"
    ],
    "suggested_staged_path": "Keep the frame fixed and focus only on the interior. For each empty cell, compare Manhattan distances to the seeds; ties stay blank, unique minima take the winning seed color.",
    "written_solution": "Inside the border, color each empty cell by the nearest seed under Manhattan distance. When two or more seeds are tied for nearest, leave that cell 0.",
    "reference_program": "def rule_h107(g):\n    h,w=size(g)\n    out=clone(g)\n    # preserve frame/walls 5\n    seeds=[(r,c,v) for r,row in enumerate(g) for c,v in enumerate(row) if v not in (0,5)]\n    for r in range(h):\n        for c in range(w):\n            if g[r][c]==5:\n                continue\n            if g[r][c]!=0:\n                continue\n            dists=[(abs(r-sr)+abs(c-sc), color) for sr,sc,color in seeds]\n            mind=min(d for d,color in dists)\n            colors={color for d,color in dists if d==mind}\n            if len(colors)==1:\n                out[r][c]=next(iter(colors))\n    return out",
    "train": [
      {
        "input": [
          "555555555",
          "500000005",
          "502000305",
          "500000005",
          "500000005",
          "500000005",
          "500040005",
          "500000005",
          "555555555"
        ],
        "output": [
          "555555555",
          "522203335",
          "522203335",
          "522203335",
          "522040335",
          "500444005",
          "544444445",
          "544444445",
          "555555555"
        ]
      },
      {
        "input": [
          "5555555555",
          "5000000005",
          "5060000305",
          "5000000005",
          "5000000005",
          "5000000005",
          "5000000005",
          "5000080005",
          "5000000005",
          "5555555555"
        ],
        "output": [
          "5555555555",
          "5666633335",
          "5666633335",
          "5666633335",
          "5666083335",
          "5660888335",
          "5008888885",
          "5888888885",
          "5888888885",
          "5555555555"
        ]
      },
      {
        "input": [
          "55555555555",
          "50000000005",
          "50020000005",
          "50000000005",
          "50000000405",
          "50000000005",
          "50000700005",
          "50000000005",
          "55555555555"
        ],
        "output": [
          "55555555555",
          "52222224445",
          "52222224445",
          "52222044445",
          "52220744445",
          "50007774445",
          "57777777445",
          "57777777445",
          "55555555555"
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
          "50000000005",
          "50000200005",
          "50000000005",
          "55555555555"
        ],
        "output": [
          "55555555555",
          "53333066665",
          "53333066665",
          "53333066665",
          "53333266665",
          "53332226665",
          "53322222665",
          "52222222225",
          "52222222225",
          "52222222225",
          "55555555555"
        ]
      }
    ],
    "test": {
      "input": [
        "555555555555",
        "500000000005",
        "500400000005",
        "500000000705",
        "500000000005",
        "500000000005",
        "500000000005",
        "500000200005",
        "500000000005",
        "555555555555"
      ],
      "output": [
        "555555555555",
        "544444477775",
        "544444477775",
        "544444777775",
        "544440277775",
        "544402227775",
        "500022222775",
        "522222222225",
        "522222222225",
        "555555555555"
      ]
    }
  },
  {
    "id": "H108",
    "title": "Nested Depth Recoloring",
    "difficulty": "hard",
    "skills": [
      "nested rectangles",
      "legend decoding",
      "depth order"
    ],
    "suggested_staged_path": "Read the legend row as the colors for outer, middle, and inner frames. Sort the nested rectangles by size and recolor them from outside to inside.",
    "written_solution": "The top row is a depth legend. Detect the nested 5-colored rectangles below, order them from largest to smallest, and recolor each border by its depth using the legend colors.",
    "reference_program": "def rule_h108(g):\n    legend=[v for v in g[0] if v not in (0,5)]\n    body=[row[:] for row in g[1:]]\n    comps=components(body, colors={5})\n    rects=[]\n    for comp in comps:\n        r0,c0,r1,c1=bbox(comp[\"cells\"])\n        if all(body[r0][c]==5 for c in range(c0,c1+1)) and all(body[r1][c]==5 for c in range(c0,c1+1)) and all(body[r][c0]==5 for r in range(r0,r1+1)) and all(body[r][c1]==5 for r in range(r0,r1+1)):\n            rects.append((r0,c0,r1,c1,comp))\n    rects_sorted=sorted(rects, key=lambda x: ((x[2]-x[0]+1)*(x[3]-x[1]+1)), reverse=True)\n    out=[row[:] for row in g]\n    for i,(r0,c0,r1,c1,comp) in enumerate(rects_sorted):\n        color=legend[i] if i<len(legend) else legend[-1]\n        for c in range(c0,c1+1):\n            out[r0+1][c]=color; out[r1+1][c]=color\n        for r in range(r0,r1+1):\n            out[r+1][c0]=color; out[r+1][c1]=color\n    return out",
    "train": [
      {
        "input": [
          "23400000000",
          "55555555555",
          "50000000005",
          "50555555505",
          "50500000505",
          "50505550505",
          "50505050505",
          "50505550505",
          "50500000505",
          "50555555505",
          "50000000005",
          "55555555555"
        ],
        "output": [
          "23400000000",
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
          "6780000000000",
          "0555555555550",
          "0500000000050",
          "0505555555050",
          "0505000005050",
          "0505055505050",
          "0505050505050",
          "0505055505050",
          "0505000005050",
          "0505555555050",
          "0500000000050",
          "0555555555550"
        ],
        "output": [
          "6780000000000",
          "0666666666660",
          "0600000000060",
          "0607777777060",
          "0607000007060",
          "0607088807060",
          "0607080807060",
          "0607088807060",
          "0607000007060",
          "0607777777060",
          "0600000000060",
          "0666666666660"
        ]
      },
      {
        "input": [
          "352000000000",
          "555555555555",
          "500000000005",
          "505555555505",
          "505000000505",
          "505055550505",
          "505050050505",
          "505050050505",
          "505055550505",
          "505000000505",
          "505555555505",
          "500000000005",
          "555555555555"
        ],
        "output": [
          "352000000000",
          "333333333333",
          "300000000003",
          "302222222203",
          "302000000203",
          "302022220203",
          "302020020203",
          "302020020203",
          "302022220203",
          "302000000203",
          "302222222203",
          "300000000003",
          "333333333333"
        ]
      },
      {
        "input": [
          "84600000000000",
          "05555555555550",
          "05000000000050",
          "05055555555050",
          "05050000005050",
          "05050555505050",
          "05050500505050",
          "05050555505050",
          "05050000005050",
          "05055555555050",
          "05000000000050",
          "05555555555550"
        ],
        "output": [
          "84600000000000",
          "08888888888880",
          "08000000000080",
          "08044444444080",
          "08040000004080",
          "08040666604080",
          "08040600604080",
          "08040666604080",
          "08040000004080",
          "08044444444080",
          "08000000000080",
          "08888888888880"
        ]
      }
    ],
    "test": {
      "input": [
        "7250000000000",
        "5555555555555",
        "5000000000005",
        "5055555555505",
        "5050000000505",
        "5050555550505",
        "5050500050505",
        "5050500050505",
        "5050555550505",
        "5050000000505",
        "5055555555505",
        "5000000000005",
        "5555555555555"
      ],
      "output": [
        "7250000000000",
        "7777777777777",
        "7000000000007",
        "7022222222207",
        "7020000000207",
        "7020222220207",
        "7020200020207",
        "7020200020207",
        "7020222220207",
        "7020000000207",
        "7022222222207",
        "7000000000007",
        "7777777777777"
      ]
    }
  },
  {
    "id": "H109",
    "title": "Overlap After Guided Transform",
    "difficulty": "hard",
    "skills": [
      "command token",
      "transform composition",
      "intersection"
    ],
    "suggested_staged_path": "Read the command, transform the right motif, then compare it cellwise with the left motif. Output only the overlap mask in color 7.",
    "written_solution": "The token selects a dihedral transform for the right 3\u00d73 motif. Transform that motif, intersect it with the left motif, and paint the overlapping nonzero cells with 7.",
    "reference_program": "def rule_h109(g):\n    cmd=g[0][0]\n    left=[row[0:3] for row in g[1:4]]\n    right=[row[4:7] for row in g[1:4]]\n    tr=TRANSFORMS[cmd](right)\n    out=blank(3,3)\n    for r in range(3):\n        for c in range(3):\n            if left[r][c]!=0 and tr[r][c]!=0:\n                out[r][c]=7\n    return out",
    "train": [
      {
        "input": [
          "2000000",
          "1200003",
          "0200033",
          "0000000"
        ],
        "output": [
          "000",
          "070",
          "000"
        ]
      },
      {
        "input": [
          "5000000",
          "4000050",
          "4400055",
          "0400005"
        ],
        "output": [
          "000",
          "770",
          "000"
        ]
      },
      {
        "input": [
          "8000000",
          "6600070",
          "0600007",
          "0060077"
        ],
        "output": [
          "770",
          "000",
          "000"
        ]
      },
      {
        "input": [
          "3000000",
          "8000090",
          "8800099",
          "0080009"
        ],
        "output": [
          "700",
          "770",
          "000"
        ]
      }
    ],
    "test": {
      "input": [
        "7000000",
        "2200330",
        "2020300",
        "0000333"
      ],
      "output": [
        "770",
        "707",
        "000"
      ]
    }
  },
  {
    "id": "H110",
    "title": "Elbow-Guided Terminal Route",
    "difficulty": "hard",
    "skills": [
      "routing",
      "guide usage",
      "orthogonal geometry"
    ],
    "suggested_staged_path": "Do not search for an arbitrary shortest path. Use the single elbow marker as the forced turn point and draw the orthogonal route through it.",
    "written_solution": "The 3-valued marker fixes the bend of the path. Connect the two terminal cells with an orthogonal polyline that passes through that elbow, painting the route in color 2.",
    "reference_program": "def rule_h110(g):\n    pts2=[(r,c) for r,row in enumerate(g) for c,v in enumerate(row) if v==2]\n    elbow=[(r,c) for r,row in enumerate(g) for c,v in enumerate(row) if v==3]\n    if len(pts2)!=2 or len(elbow)!=1:\n        return clone(g)\n    a,b=pts2; e=elbow[0]\n    out=clone(g)\n    # overwrite elbow and terminals with 2 along L legs via elbow coordinates\n    draw_line_segment(out, a, (a[0], e[1]), 2)\n    draw_line_segment(out, (a[0], e[1]), e, 2)\n    draw_line_segment(out, e, (b[0], e[1]), 2)\n    draw_line_segment(out, (b[0], e[1]), b, 2)\n    out[e[0]][e[1]]=2\n    return out",
    "train": [
      {
        "input": [
          "000000000",
          "020000055",
          "000000005",
          "000000000",
          "000030000",
          "000000000",
          "000000000",
          "000000020",
          "000000000"
        ],
        "output": [
          "000000000",
          "022220055",
          "000020005",
          "000020000",
          "000020000",
          "000020000",
          "000020000",
          "000022220",
          "000000000"
        ]
      },
      {
        "input": [
          "0000000000",
          "0550000000",
          "0500000200",
          "0000000000",
          "0000000000",
          "0000030000",
          "0000000000",
          "0000000000",
          "0020000000",
          "0000000000"
        ],
        "output": [
          "0000000000",
          "0550000000",
          "0500022200",
          "0000020000",
          "0000020000",
          "0000020000",
          "0000020000",
          "0000020000",
          "0022220000",
          "0000000000"
        ]
      },
      {
        "input": [
          "00000000000",
          "00000000200",
          "00000000000",
          "00000000000",
          "00000300000",
          "00000000000",
          "00000000000",
          "00200000055",
          "00000000005"
        ],
        "output": [
          "00000000000",
          "00000222200",
          "00000200000",
          "00000200000",
          "00000200000",
          "00000200000",
          "00000200000",
          "00222200055",
          "00000000005"
        ]
      },
      {
        "input": [
          "000000000000",
          "000000000000",
          "002000000000",
          "000000000050",
          "000000000050",
          "000000300050",
          "000000000000",
          "000000000000",
          "000000000200",
          "000000000000"
        ],
        "output": [
          "000000000000",
          "000000000000",
          "002222200000",
          "000000200050",
          "000000200050",
          "000000200050",
          "000000200000",
          "000000200000",
          "000000222200",
          "000000000000"
        ]
      }
    ],
    "test": {
      "input": [
        "00000000000",
        "00000000000",
        "00000000200",
        "00000000000",
        "00000000000",
        "00000300000",
        "00000000000",
        "00000000000",
        "00020000000",
        "05500000000",
        "00500000000"
      ],
      "output": [
        "00000000000",
        "00000000000",
        "00000222200",
        "00000200000",
        "00000200000",
        "00000200000",
        "00000200000",
        "00000200000",
        "00022200000",
        "05500000000",
        "00500000000"
      ]
    }
  },
  {
    "id": "H111",
    "title": "Legend-Ordered Canonical Gallery",
    "difficulty": "hard",
    "skills": [
      "legend ordering",
      "canonicalization",
      "dihedral normalization"
    ],
    "suggested_staged_path": "Read the legend colors in order. For each matching object below, normalize it to a canonical orientation, then pack those canonical crops in legend order.",
    "written_solution": "The top row specifies the order of colors to output. For each color, find its object, normalize that object to its lexicographically minimal dihedral orientation, and concatenate the canonical crops in legend order.",
    "reference_program": "def rule_h111(g):\n    legend=[v for v in g[0] if v!=0]\n    body=clone(g); body[0]=[0]*len(g[0])\n    comps=components(body)\n    # map color to canonical crop\n    color_to_crop={}\n    for comp in comps:\n        color=comp[\"color\"]\n        crop=crop_comp_grid(g, comp)\n        color_to_crop[color]=canonical_crop(crop)\n    crops=[color_to_crop[c] for c in legend]\n    return hcat(crops, gap=1, fill=0)",
    "train": [
      {
        "input": [
          "040207000000000000",
          "000000000000000000",
          "022000044400000000",
          "020000004000000000",
          "000000000000077000",
          "000000000000077000",
          "000000000000000000",
          "000000000000000000",
          "000000000000000000"
        ],
        "output": [
          "04002077",
          "44022077",
          "04000000"
        ]
      },
      {
        "input": [
          "060308000000000000",
          "000000000000000000",
          "030000000000000000",
          "033000066000000000",
          "030000006000088000",
          "000000000000088000",
          "000000000000000000",
          "000000000000000000",
          "000000000000000000"
        ],
        "output": [
          "06003088",
          "66033088",
          "00003000"
        ]
      },
      {
        "input": [
          "070402000000000000",
          "000000000000000000",
          "022000000000000000",
          "022000040000000000",
          "000000044000070000",
          "000000000000777000",
          "000000000000000000",
          "000000000000000000",
          "000000000000000000"
        ],
        "output": [
          "07004022",
          "77044022",
          "07000000"
        ]
      },
      {
        "input": [
          "080605000000000000",
          "000000000000000000",
          "005000000000000000",
          "055000006600000000",
          "005000006600088000",
          "000000000000008000",
          "000000000000000000",
          "000000000000000000",
          "000000000000000000"
        ],
        "output": [
          "08066005",
          "88066055",
          "00000005"
        ]
      }
    ],
    "test": {
      "input": [
        "020509000000000000",
        "000000000000000000",
        "022000050000000000",
        "020000055000000000",
        "000000050000099000",
        "000000000000099000",
        "000000000000000000",
        "000000000000000000",
        "000000000000000000"
      ],
      "output": [
        "02005099",
        "22055099",
        "00005000"
      ]
    }
  },
  {
    "id": "H112",
    "title": "Row/Column Command Mosaic",
    "difficulty": "hard",
    "skills": [
      "command composition",
      "mosaic assembly",
      "panel generation"
    ],
    "suggested_staged_path": "Extract the source motif and the two row commands plus two column commands. Each output panel is row-transform first, then column-transform, arranged as a 2\u00d72 mosaic.",
    "written_solution": "The input encodes a tiny transform table. Apply each row command and each column command to the source motif, compose them, and place the four resulting motifs into a 2\u00d72 mosaic.",
    "reference_program": "def rule_h112(g):\n    row_cmds=[g[3][0], g[5][0]]\n    col_cmds=[g[0][3], g[0][5]]\n    src=[row[3:6] for row in g[3:6]]\n    panels=[]\n    for rcmd in row_cmds:\n        row_panels=[]\n        for ccmd in col_cmds:\n            panel=TRANSFORMS[ccmd](TRANSFORMS[rcmd](src))\n            row_panels.append(panel)\n        panels.append(hcat(row_panels,gap=1,fill=0))\n    return vcat(panels,gap=1,fill=0)",
    "train": [
      {
        "input": [
          "000307",
          "000000",
          "000000",
          "200120",
          "000100",
          "500000"
        ],
        "output": [
          "0000000",
          "2000100",
          "1100120",
          "0000000",
          "0000000",
          "1000200",
          "1200110"
        ]
      },
      {
        "input": [
          "000208",
          "000000",
          "000000",
          "400030",
          "000033",
          "600003"
        ],
        "output": [
          "0300300",
          "3300330",
          "3000030",
          "0000000",
          "0000033",
          "3300330",
          "0330000"
        ]
      },
      {
        "input": [
          "000507",
          "000000",
          "000000",
          "100440",
          "000004",
          "300040"
        ],
        "output": [
          "0440400",
          "4000404",
          "0400040",
          "0000000",
          "0400040",
          "0040404",
          "4400004"
        ]
      },
      {
        "input": [
          "000406",
          "000000",
          "000000",
          "700060",
          "000660",
          "200600"
        ],
        "output": [
          "0600000",
          "6600660",
          "6000066",
          "0000000",
          "6000000",
          "6600066",
          "0600660"
        ]
      }
    ],
    "test": {
      "input": [
        "000103",
        "000000",
        "000000",
        "800700",
        "000770",
        "500070"
      ],
      "output": [
        "0000770",
        "7700077",
        "0770000",
        "0000000",
        "0070070",
        "0770770",
        "0700700"
      ]
    }
  }
]
''')

def validate():
    train_pairs = sum(len(p['train']) for p in PUZZLES)
    total_pairs = train_pairs + len(PUZZLES)
    for puzzle in PUZZLES:
        rule = RULES[puzzle['id']]
        for pair in puzzle['train']:
            inp = grid_from_strings(pair['input'])
            out = grid_from_strings(pair['output'])
            got = rule(inp)
            assert got == out, f"{puzzle['id']} train mismatch"
        inp = grid_from_strings(puzzle['test']['input'])
        out = grid_from_strings(puzzle['test']['output'])
        got = rule(inp)
        assert got == out, f"{puzzle['id']} test mismatch"
    print(f"validated {len(PUZZLES)} puzzles / {train_pairs} train pairs / {total_pairs} total pairs")

if __name__ == "__main__":
    validate()
