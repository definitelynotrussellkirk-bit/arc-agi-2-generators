from __future__ import annotations
import collections
import json
from pathlib import Path

DIR4 = [(-1,0),(1,0),(0,-1),(0,1)]

def blank(h,w,val=0):
    return [[val for _ in range(w)] for _ in range(h)]

def clone(g): return [row[:] for row in g]

def size(g): return len(g), len(g[0]) if g else 0

def strings_from_grid(g): return ["".join(str(c) for c in row) for row in g]

def grid_from_strings(rows): return [[int(ch) for ch in row] for row in rows]

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

def draw_rect_border(g,r0,c0,r1,c1,color):
    for c in range(c0,c1+1):
        g[r0][c]=color; g[r1][c]=color
    for r in range(r0,r1+1):
        g[r][c0]=color; g[r][c1]=color

def orth_neighbors(r,c,h,w):
    for dr,dc in DIR4:
        nr,nc=r+dr,c+dc
        if 0<=nr<h and 0<=nc<w:
            yield nr,nc

def components_nonzero(g, treat_colors_separately=False):
    h,w=size(g)
    vis=[[False]*w for _ in range(h)]
    comps=[]
    for r in range(h):
        for c in range(w):
            if vis[r][c]: 
                continue
            vis[r][c]=True
            if g[r][c]==0:
                continue
            color=g[r][c]
            stack=[(r,c)]
            cells=[(r,c)]
            while stack:
                rr,cc=stack.pop()
                for nr,nc in orth_neighbors(rr,cc,h,w):
                    if not vis[nr][nc] and g[nr][nc]!=0 and (not treat_colors_separately or g[nr][nc]==color):
                        vis[nr][nc]=True
                        stack.append((nr,nc))
                        cells.append((nr,nc))
            comps.append((color,cells))
    return comps

def components_zero(g):
    h,w=size(g)
    vis=[[False]*w for _ in range(h)]
    comps=[]
    for r in range(h):
        for c in range(w):
            if vis[r][c]:
                continue
            vis[r][c]=True
            if g[r][c]!=0:
                continue
            stack=[(r,c)]
            cells=[(r,c)]
            touch_border = r in (0,h-1) or c in (0,w-1)
            while stack:
                rr,cc=stack.pop()
                for nr,nc in orth_neighbors(rr,cc,h,w):
                    if not vis[nr][nc] and g[nr][nc]==0:
                        vis[nr][nc]=True
                        stack.append((nr,nc))
                        cells.append((nr,nc))
                        if nr in (0,h-1) or nc in (0,w-1):
                            touch_border=True
            comps.append((cells, touch_border))
    return comps

def perimeter_of_cells(cells):
    s=set(cells)
    p=0
    for r,c in cells:
        for dr,dc in DIR4:
            if (r+dr,c+dc) not in s:
                p+=1
    return p

def mirror_v(g):  # vertical axis left-right
    h,w=size(g)
    out=clone(g)
    for r in range(h):
        for c in range(w):
            if g[r][c]!=0:
                out[r][w-1-c]=g[r][c]
    return out

def mirror_h(g):
    h,w=size(g)
    out=clone(g)
    for r in range(h):
        for c in range(w):
            if g[r][c]!=0:
                out[h-1-r][c]=g[r][c]
    return out

def stamp_template(base_grid, anchors, template, center=None, substitute=None, respect_original_nonzero=True, keep_anchor=True):
    g=clone(base_grid)
    th,tw=size(template)
    if center is None:
        center=(th//2, tw//2)
    cr,cc=center
    substitute=dict(substitute or {})
    h,w=size(base_grid)
    for item in anchors:
        if len(item)==2:
            r,c=item
            acol=base_grid[r][c]
        else:
            r,c,acol=item
        for tr in range(th):
            for tc in range(tw):
                tv=template[tr][tc]
                if tv==0:
                    continue
                rr=r+(tr-cr); cc2=c+(tc-cc)
                if not (0<=rr<h and 0<=cc2<w):
                    continue
                if keep_anchor and rr==r and cc2==c:
                    continue
                paint=substitute.get(tv,tv)
                if paint=='anchor':
                    paint=acol
                if respect_original_nonzero and base_grid[rr][cc2]!=0:
                    continue
                g[rr][cc2]=paint
        if keep_anchor:
            g[r][c]=acol
    return g

def binary_shape_from_cells(cells):
    r0,c0,r1,c1=bbox(cells)
    sh=blank(r1-r0+1, c1-c0+1)
    for r,c in cells:
        sh[r-r0][c-c0]=1
    return sh

def rule_e29(g):
    template=[[7,0,7],[0,0,0],[7,0,7]]
    anchors=[(r,c) for r,row in enumerate(g) for c,v in enumerate(row) if v==2]
    return stamp_template(g, anchors, template, center=(1,1), keep_anchor=True)

def rule_e30(g):
    h,w=size(g)
    groups=collections.defaultdict(list)
    for r,row in enumerate(g):
        for c,v in enumerate(row):
            if v!=0:
                groups[v].append((r,c))
    out=blank(h,w)
    for color,cells in groups.items():
        if len(cells)!=2:
            continue
        r0,c0,r1,c1=bbox(cells)
        draw_rect_border(out, r0,c0,r1,c1, color)
    return out

def rule_e31(g):
    return mirror_v(g)

def rule_e32(g):
    n=sum(1 for row in g for v in row if v==2)
    return [[2]*n]

def rule_e33(g):
    h,w=size(g)
    out=blank(h,w)
    for c,v in enumerate(g[0]):
        if v!=0:
            for r in range(h):
                out[r][c]=v
    return out

def rule_e34(g):
    h,w=size(g)
    out=clone(g)
    for r in range(1,h-1):
        for c in range(1,w-1):
            if g[r][c]!=0:
                continue
            vals=[g[r-1][c], g[r+1][c], g[r][c-1], g[r][c+1]]
            if vals[0]!=0 and vals.count(vals[0])==4:
                out[r][c]=vals[0]
    return out

def rule_e35(g):
    cells=[(r,c) for r,row in enumerate(g) for c,v in enumerate(row) if v!=0]
    return crop_bbox(g, cells)

def rule_m29(g):
    comps=components_nonzero(g, treat_colors_separately=False)
    best=max(comps, key=lambda item: len(item[1]))
    return crop_bbox(g, best[1])

def rule_m30(g):
    frame_color=g[0][0]
    cells=[(r,c) for r,row in enumerate(g) for c,v in enumerate(row) if v!=0 and not (r==0 and c==0)]
    core=crop_bbox(g, cells)
    ch,cw=size(core)
    out=blank(ch+2, cw+2, frame_color)
    for r in range(ch):
        for c in range(cw):
            out[r+1][c+1]=core[r][c]
    return out

def rule_m31(g):
    out=clone(g)
    for cells,touch in components_zero(g):
        if touch:
            continue
        for r,c in cells:
            out[r][c]=7
    return out

def rule_m32(g):
    comps=components_nonzero(g, treat_colors_separately=True)
    items=sorted(((len(cells), color) for color,cells in comps), key=lambda x:(x[0], x[1]))
    return [[color for _,color in items]]

def rule_m33(g):
    h,w=size(g)
    cmd=g[0][0]
    work=blank(h,w)
    for r,row in enumerate(g):
        for c,v in enumerate(row):
            if v!=0 and not (r==0 and c==0):
                work[r][c]=v
    out = mirror_v(work) if cmd==1 else mirror_h(work)
    out[0][0]=cmd
    return out

def rule_m34(g):
    template=[row[:3] for row in g[:3]]
    anchors=[(r,c) for r,row in enumerate(g) for c,v in enumerate(row)
             if v==2 and not (0<=r<3 and 0<=c<3)]
    return stamp_template(g, anchors, template, center=(1,1), keep_anchor=True)

def rule_m35(g):
    out=clone(g)
    groups=collections.defaultdict(list)
    for r,row in enumerate(g):
        for c,v in enumerate(row):
            if v!=0:
                groups[v].append((r,c))
    for color,cells in groups.items():
        if len(cells)!=2:
            continue
        (r0,c0),(r1,c1)=cells
        if r0==r1 and abs(c1-c0)%2==0:
            out[r0][(c0+c1)//2]=9
        elif c0==c1 and abs(r1-r0)%2==0:
            out[(r0+r1)//2][c0]=9
    return out

def rule_h29(g):
    h,w=size(g)
    comps=components_nonzero(g, treat_colors_separately=False)
    items=[]
    for _,cells in comps:
        r0,c0,r1,c1=bbox(cells)
        area=(r1-r0+1)*(c1-c0+1)
        items.append((-(area), cells))
    items.sort(key=lambda x:x[0])
    out=blank(h,w)
    for idx,(_,cells) in enumerate(items):
        color=2+idx
        for r,c in cells:
            out[r][c]=color
    return out

def rule_h30(g):
    h,w=size(g)
    guides=[(r,c) for r,row in enumerate(g) for c,v in enumerate(row) if v==5]
    work=blank(h,w)
    for r,row in enumerate(g):
        for c,v in enumerate(row):
            if v!=0 and v!=5:
                work[r][c]=v
    if len(guides)==2 and guides[0][0]==guides[1][0]:
        out=mirror_h(work)
    else:
        out=mirror_v(work)
    for r,c in guides:
        out[r][c]=5
    return out

def rule_h31(g):
    counts=collections.Counter(v for row in g for v in row if v!=0)
    order=sorted(counts.items(), key=lambda kv:(-kv[1], kv[0]))
    return [[color for color,_ in order]]

def rule_h32(g):
    cells1=[(r,c) for r,row in enumerate(g) for c,v in enumerate(row) if v==1]
    cells2=[(r,c) for r,row in enumerate(g) for c,v in enumerate(row) if v==2]
    s1=binary_shape_from_cells(cells1)
    s2=binary_shape_from_cells(cells2)
    h=max(len(s1), len(s2))
    w=max(len(s1[0]), len(s2[0]))
    out=blank(h,w)
    for r in range(h):
        for c in range(w):
            a = r < len(s1) and c < len(s1[0]) and s1[r][c] == 1
            b = r < len(s2) and c < len(s2[0]) and s2[r][c] == 1
            if bool(a) ^ bool(b):
                out[r][c]=7
    return out

def rule_h33(g):
    comps=components_nonzero(g, treat_colors_separately=True)
    items=[]
    for color,cells in comps:
        shape=crop_bbox(g, cells)
        per=perimeter_of_cells(cells)
        items.append((-per, color, shape))
    items.sort(key=lambda x:(x[0], x[1]))
    width=max(len(shape[0]) for _,_,shape in items)
    height=sum(len(shape) for _,_,shape in items) + (len(items)-1)
    out=blank(height, width)
    cur=0
    for i,(_,color,shape) in enumerate(items):
        sh,sw=size(shape)
        for r in range(sh):
            for c in range(sw):
                out[cur+r][c]=shape[r][c]
        cur += sh
        if i != len(items)-1:
            cur += 1
    return out

def rule_h34(g):
    template=[row[:3] for row in g[:3]]
    anchors=[(r,c,g[r][c]) for r,row in enumerate(g) for c,v in enumerate(row)
             if v!=0 and not (0<=r<3 and 0<=c<3)]
    return stamp_template(g, anchors, template, center=(1,1), substitute={9:'anchor'}, keep_anchor=True)

def rule_h35(g):
    h,w=size(g)
    horiz=blank(h,w)
    vert=blank(h,w)
    for r,row in enumerate(g):
        for c,v in enumerate(row):
            if v==2:
                for dc in (-1,1):
                    cc=c+dc
                    while 0<=cc<w and g[r][cc]==0:
                        horiz[r][cc]=1
                        cc += dc
            elif v==3:
                for dr in (-1,1):
                    rr=r+dr
                    while 0<=rr<h and g[rr][c]==0:
                        vert[rr][c]=1
                        rr += dr
    out=blank(h,w)
    for r in range(h):
        for c in range(w):
            if horiz[r][c] and vert[r][c]:
                out[r][c]=8
    return out

RULES = {
    "E29": rule_e29,
    "E30": rule_e30,
    "E31": rule_e31,
    "E32": rule_e32,
    "E33": rule_e33,
    "E34": rule_e34,
    "E35": rule_e35,
    "M29": rule_m29,
    "M30": rule_m30,
    "M31": rule_m31,
    "M32": rule_m32,
    "M33": rule_m33,
    "M34": rule_m34,
    "M35": rule_m35,
    "H29": rule_h29,
    "H30": rule_h30,
    "H31": rule_h31,
    "H32": rule_h32,
    "H33": rule_h33,
    "H34": rule_h34,
    "H35": rule_h35
}

SUMMARY = {'set': 5,
 'puzzle_count': 21,
 'train_pair_count': 84,
 'avg_train_pairs': 4.0,
 'difficulty_counts': {'easy': 7, 'medium': 7, 'hard': 7},
 'new_primitive': {'name': 'stamp_template',
                   'purpose': 'Stamp a small template around anchor cells, optionally substituting '
                              'one template token with the anchor color.'}}

PAYLOAD = json.loads(r'''
{
  "set": 5,
  "summary": {
    "set": 5,
    "puzzle_count": 21,
    "train_pair_count": 84,
    "avg_train_pairs": 4.0,
    "difficulty_counts": {
      "easy": 7,
      "medium": 7,
      "hard": 7
    },
    "new_primitive": {
      "name": "stamp_template",
      "purpose": "Stamp a small template around anchor cells, optionally substituting one template token with the anchor color."
    }
  },
  "puzzles": [
    {
      "id": "E29",
      "title": "Diagonal Halo Stamp",
      "difficulty": "easy",
      "skills": [
        "template stamping",
        "diagonal offsets",
        "new primitive"
      ],
      "staged_hint": "Ignore colors first. Around each 2, the changed cells always sit at the same four relative offsets.",
      "written_solution": "Each red(2) anchor keeps its value and stamps orange(7) onto its four diagonal neighbors, clipped by the grid boundary.",
      "uses_new_primitive": true,
      "program_name": "rule_e29",
      "program_source": "def rule_e29(g):\n    template=[[7,0,7],[0,0,0],[7,0,7]]\n    anchors=[(r,c) for r,row in enumerate(g) for c,v in enumerate(row) if v==2]\n    return stamp_template(g, anchors, template, center=(1,1), keep_anchor=True)",
      "train": [
        {
          "input": [
            "00000000",
            "00200000",
            "00000000",
            "00000000",
            "00000200",
            "00000000",
            "00000000"
          ],
          "output": [
            "07070000",
            "00200000",
            "07070000",
            "00007070",
            "00000200",
            "00007070",
            "00000000"
          ]
        },
        {
          "input": [
            "000020000",
            "000000000",
            "000000000",
            "000000000",
            "000000000",
            "000000000",
            "020000020",
            "000000000"
          ],
          "output": [
            "000020000",
            "000707000",
            "000000000",
            "000000000",
            "000000000",
            "707000707",
            "020000020",
            "707000707"
          ]
        },
        {
          "input": [
            "0000000000",
            "0000000000",
            "0020000000",
            "0000000200",
            "0000000000",
            "0000000000"
          ],
          "output": [
            "0000000000",
            "0707000000",
            "0020007070",
            "0707000200",
            "0000007070",
            "0000000000"
          ]
        },
        {
          "input": [
            "000000000",
            "020000000",
            "000000000",
            "000000000",
            "000020000",
            "000000000",
            "000000000",
            "000000020",
            "000000000"
          ],
          "output": [
            "707000000",
            "020000000",
            "707000000",
            "000707000",
            "000020000",
            "000707000",
            "000000707",
            "000000020",
            "000000707"
          ]
        }
      ],
      "test": {
        "input": [
          "0000000000",
          "0000000020",
          "0000000000",
          "0000000000",
          "0020000000",
          "0000000000",
          "0000020000",
          "0000000000"
        ],
        "output": [
          "0000000707",
          "0000000020",
          "0000000707",
          "0707000000",
          "0020000000",
          "0707707000",
          "0000020000",
          "0000707000"
        ]
      }
    },
    {
      "id": "E30",
      "title": "Corner-To-Rectangle Border",
      "difficulty": "easy",
      "skills": [
        "bounding boxes",
        "opposite corners",
        "same-size drawing"
      ],
      "staged_hint": "Each color gives you only two cells, so treat them as the extremal points of one larger object.",
      "written_solution": "For each nonzero color, the two input cells are opposite corners of an axis-aligned rectangle. Draw the full border of that rectangle in the same color.",
      "uses_new_primitive": false,
      "program_name": "rule_e30",
      "program_source": "def rule_e30(g):\n    h,w=size(g)\n    groups=collections.defaultdict(list)\n    for r,row in enumerate(g):\n        for c,v in enumerate(row):\n            if v!=0:\n                groups[v].append((r,c))\n    out=blank(h,w)\n    for color,cells in groups.items():\n        if len(cells)!=2:\n            continue\n        r0,c0,r1,c1=bbox(cells)\n        draw_rect_border(out, r0,c0,r1,c1, color)\n    return out",
      "train": [
        {
          "input": [
            "000000000",
            "010000000",
            "000000000",
            "000000000",
            "000000000",
            "000000100",
            "000000000",
            "000000000"
          ],
          "output": [
            "000000000",
            "011111100",
            "010000100",
            "010000100",
            "010000100",
            "011111100",
            "000000000",
            "000000000"
          ]
        },
        {
          "input": [
            "0000000000",
            "0000003000",
            "0200000000",
            "0000000000",
            "0000000030",
            "0000000000",
            "0000000000",
            "0000200000",
            "0000000000"
          ],
          "output": [
            "0000000000",
            "0000003330",
            "0222203030",
            "0200203030",
            "0200203330",
            "0200200000",
            "0200200000",
            "0222200000",
            "0000000000"
          ]
        },
        {
          "input": [
            "00000000000",
            "00040000000",
            "00000000000",
            "00000000000",
            "00000000000",
            "00000000040",
            "00000000000"
          ],
          "output": [
            "00000000000",
            "00044444440",
            "00040000040",
            "00040000040",
            "00040000040",
            "00044444440",
            "00000000000"
          ]
        },
        {
          "input": [
            "0000000000",
            "0000000000",
            "0600000000",
            "0000000000",
            "0000008000",
            "0000000000",
            "0000000080",
            "0000000000",
            "0000600000",
            "0000000000"
          ],
          "output": [
            "0000000000",
            "0000000000",
            "0666600000",
            "0600600000",
            "0600608880",
            "0600608080",
            "0600608880",
            "0600600000",
            "0666600000",
            "0000000000"
          ]
        }
      ],
      "test": {
        "input": [
          "000000000000",
          "002000000000",
          "000000000000",
          "000040000000",
          "000000000000",
          "000000000000",
          "000000400000",
          "000000000200",
          "000000000000"
        ],
        "output": [
          "000000000000",
          "002222222200",
          "002000000200",
          "002044400200",
          "002040400200",
          "002040400200",
          "002044400200",
          "002222222200",
          "000000000000"
        ]
      }
    },
    {
      "id": "E31",
      "title": "Vertical Mirror Add",
      "difficulty": "easy",
      "skills": [
        "reflection",
        "symmetry",
        "same-size completion"
      ],
      "staged_hint": "Nothing is deleted or moved. The output just adds the symmetric counterpart of each colored cell.",
      "written_solution": "Mirror every nonzero cell across the vertical center line of the grid, keeping the originals. The result is the union of the input and its left-right reflection.",
      "uses_new_primitive": false,
      "program_name": "rule_e31",
      "program_source": "def rule_e31(g):\n    return mirror_v(g)",
      "train": [
        {
          "input": [
            "000000000",
            "000000000",
            "010000000",
            "000000000",
            "000200000",
            "400000000",
            "000000000"
          ],
          "output": [
            "000000000",
            "000000000",
            "010000010",
            "000000000",
            "000202000",
            "400000004",
            "000000000"
          ]
        },
        {
          "input": [
            "0000000000",
            "0030000000",
            "0000000000",
            "0000500000",
            "0000000000",
            "0000000000",
            "0200000000",
            "0000000000"
          ],
          "output": [
            "0000000000",
            "0030000300",
            "0000000000",
            "0000550000",
            "0000000000",
            "0000000000",
            "0200000020",
            "0000000000"
          ]
        },
        {
          "input": [
            "60000000",
            "00000000",
            "00100000",
            "00000000",
            "00000000",
            "00070000"
          ],
          "output": [
            "60000006",
            "00000000",
            "00100100",
            "00000000",
            "00000000",
            "00077000"
          ]
        },
        {
          "input": [
            "00000000000",
            "00000000000",
            "00080000000",
            "00000000000",
            "02000000000",
            "00000000000",
            "00000000000",
            "00004000000",
            "00000000000"
          ],
          "output": [
            "00000000000",
            "00000000000",
            "00080008000",
            "00000000000",
            "02000000020",
            "00000000000",
            "00000000000",
            "00004040000",
            "00000000000"
          ]
        }
      ],
      "test": {
        "input": [
          "000000000000",
          "030000000000",
          "000000000000",
          "000060000000",
          "000000000000",
          "000000000000",
          "008000000000",
          "000000000000"
        ],
        "output": [
          "000000000000",
          "030000000030",
          "000000000000",
          "000060060000",
          "000000000000",
          "000000000000",
          "008000000800",
          "000000000000"
        ]
      }
    },
    {
      "id": "E32",
      "title": "Count-To-Bar",
      "difficulty": "easy",
      "skills": [
        "counting",
        "resize",
        "serialization"
      ],
      "staged_hint": "All positions are irrelevant. Only one global quantity survives into the output.",
      "written_solution": "Count how many red(2) cells appear anywhere in the input. Output a single row whose length equals that count, filled entirely with red(2).",
      "uses_new_primitive": false,
      "program_name": "rule_e32",
      "program_source": "def rule_e32(g):\n    n=sum(1 for row in g for v in row if v==2)\n    return [[2]*n]",
      "train": [
        {
          "input": [
            "000000",
            "020000",
            "000020",
            "000000",
            "002000",
            "000000"
          ],
          "output": [
            "222"
          ]
        },
        {
          "input": [
            "00200000",
            "00000000",
            "00000000",
            "00000200",
            "00000000",
            "02000000",
            "00000020"
          ],
          "output": [
            "2222"
          ]
        },
        {
          "input": [
            "000000000",
            "020000020",
            "000020000",
            "000202000",
            "000000000"
          ],
          "output": [
            "22222"
          ]
        },
        {
          "input": [
            "20000000",
            "00000000",
            "00200000",
            "00000000",
            "00000000",
            "00000000",
            "00000000",
            "00000000"
          ],
          "output": [
            "22"
          ]
        }
      ],
      "test": {
        "input": [
          "0000200000",
          "0200000000",
          "0000000020",
          "0000000000",
          "0002000000",
          "2000000000",
          "0000002000"
        ],
        "output": [
          "222222"
        ]
      }
    },
    {
      "id": "E33",
      "title": "Top-Row Column Fill",
      "difficulty": "easy",
      "skills": [
        "column propagation",
        "same-size transform",
        "command row"
      ],
      "staged_hint": "Read the first row as instructions and ignore the zeros beneath it.",
      "written_solution": "Every nonzero cell in the top row controls its whole column. Copy that color straight down through the entire column, leaving unmarked columns black(0).",
      "uses_new_primitive": false,
      "program_name": "rule_e33",
      "program_source": "def rule_e33(g):\n    h,w=size(g)\n    out=blank(h,w)\n    for c,v in enumerate(g[0]):\n        if v!=0:\n            for r in range(h):\n                out[r][c]=v\n    return out",
      "train": [
        {
          "input": [
            "01002030",
            "00000000",
            "00000000",
            "00000000",
            "00000000",
            "00000000"
          ],
          "output": [
            "01002030",
            "01002030",
            "01002030",
            "01002030",
            "01002030",
            "01002030"
          ]
        },
        {
          "input": [
            "400600000",
            "000000000",
            "000000000",
            "000000000",
            "000000000",
            "000000000",
            "000000000"
          ],
          "output": [
            "400600000",
            "400600000",
            "400600000",
            "400600000",
            "400600000",
            "400600000",
            "400600000"
          ]
        },
        {
          "input": [
            "0020050070",
            "0000000000",
            "0000000000",
            "0000000000",
            "0000000000"
          ],
          "output": [
            "0020050070",
            "0020050070",
            "0020050070",
            "0020050070",
            "0020050070"
          ]
        },
        {
          "input": [
            "08000030",
            "00000000",
            "00000000",
            "00000000",
            "00000000",
            "00000000",
            "00000000",
            "00000000"
          ],
          "output": [
            "08000030",
            "08000030",
            "08000030",
            "08000030",
            "08000030",
            "08000030",
            "08000030",
            "08000030"
          ]
        }
      ],
      "test": {
        "input": [
          "60002000004",
          "00000000000",
          "00000000000",
          "00000000000",
          "00000000000",
          "00000000000",
          "00000000000"
        ],
        "output": [
          "60002000004",
          "60002000004",
          "60002000004",
          "60002000004",
          "60002000004",
          "60002000004",
          "60002000004"
        ]
      }
    },
    {
      "id": "E34",
      "title": "Center Completion",
      "difficulty": "easy",
      "skills": [
        "local neighborhoods",
        "pattern completion",
        "same-size repair"
      ],
      "staged_hint": "Check zero cells only. Ask when a zero is surrounded by a perfect four-arm pattern of one color.",
      "written_solution": "Whenever a black(0) cell has the same nonzero color directly above, below, left, and right, fill that center cell with that color. Everything else stays unchanged.",
      "uses_new_primitive": false,
      "program_name": "rule_e34",
      "program_source": "def rule_e34(g):\n    h,w=size(g)\n    out=clone(g)\n    for r in range(1,h-1):\n        for c in range(1,w-1):\n            if g[r][c]!=0:\n                continue\n            vals=[g[r-1][c], g[r+1][c], g[r][c-1], g[r][c+1]]\n            if vals[0]!=0 and vals.count(vals[0])==4:\n                out[r][c]=vals[0]\n    return out",
      "train": [
        {
          "input": [
            "00000000",
            "00300030",
            "03030030",
            "00300030",
            "00000400",
            "00004040",
            "00000400"
          ],
          "output": [
            "00000000",
            "00300030",
            "03330030",
            "00300030",
            "00000400",
            "00004440",
            "00000400"
          ]
        },
        {
          "input": [
            "000000000",
            "000000050",
            "000000050",
            "000200050",
            "002020000",
            "000200000",
            "000000000",
            "000000000"
          ],
          "output": [
            "000000000",
            "000000050",
            "000000050",
            "000200050",
            "002220000",
            "000200000",
            "000000000",
            "000000000"
          ]
        },
        {
          "input": [
            "0000000000",
            "0000000600",
            "0010006060",
            "0101000600",
            "0010550000",
            "0000500000"
          ],
          "output": [
            "0000000000",
            "0000000600",
            "0010006660",
            "0111000600",
            "0010550000",
            "0000500000"
          ]
        },
        {
          "input": [
            "000000000",
            "003000000",
            "033000000",
            "000080000",
            "000808000",
            "000080000",
            "000000000",
            "000000000",
            "000000000"
          ],
          "output": [
            "000000000",
            "003000000",
            "033000000",
            "000080000",
            "000888000",
            "000080000",
            "000000000",
            "000000000",
            "000000000"
          ]
        }
      ],
      "test": {
        "input": [
          "0000000000",
          "0004000000",
          "0040400000",
          "0004000000",
          "0000000200",
          "0000002020",
          "0660000200",
          "0060000000"
        ],
        "output": [
          "0000000000",
          "0004000000",
          "0044400000",
          "0004000000",
          "0000000200",
          "0000002220",
          "0660000200",
          "0060000000"
        ]
      }
    },
    {
      "id": "E35",
      "title": "Crop The Nonzero Object",
      "difficulty": "easy",
      "skills": [
        "bounding-box crop",
        "resize",
        "object extraction"
      ],
      "staged_hint": "The output never invents or edits cells; it only removes surrounding empty space.",
      "written_solution": "Take the bounding box of all nonzero cells and crop the input down to exactly that rectangle, preserving the internal multicolor pattern.",
      "uses_new_primitive": false,
      "program_name": "rule_e35",
      "program_source": "def rule_e35(g):\n    cells=[(r,c) for r,row in enumerate(g) for c,v in enumerate(row) if v!=0]\n    return crop_bbox(g, cells)",
      "train": [
        {
          "input": [
            "000000000",
            "000000000",
            "000012000",
            "000010200",
            "000022200",
            "000000000",
            "000000000",
            "000000000"
          ],
          "output": [
            "120",
            "102",
            "222"
          ]
        },
        {
          "input": [
            "0000000000",
            "0000000000",
            "0000000000",
            "0000000000",
            "0340000000",
            "0304400000",
            "0034000000",
            "0000000000",
            "0000000000"
          ],
          "output": [
            "3400",
            "3044",
            "0340"
          ]
        },
        {
          "input": [
            "00000000000",
            "00000056000",
            "00000050600",
            "00000055600",
            "00000005000",
            "00000000000",
            "00000000000"
          ],
          "output": [
            "560",
            "506",
            "556",
            "050"
          ]
        },
        {
          "input": [
            "0000000000",
            "0000000000",
            "0000000000",
            "0000000000",
            "0000000000",
            "0002300000",
            "0002030000",
            "0002220000",
            "0000200000",
            "0000000000"
          ],
          "output": [
            "230",
            "203",
            "222",
            "020"
          ]
        }
      ],
      "test": {
        "input": [
          "000000000000",
          "000000000000",
          "000000000000",
          "000000078000",
          "000000070880",
          "000000007800",
          "000000000000",
          "000000000000",
          "000000000000"
        ],
        "output": [
          "7800",
          "7088",
          "0780"
        ]
      }
    },
    {
      "id": "M29",
      "title": "Largest Component Crop",
      "difficulty": "medium",
      "skills": [
        "connected components",
        "size comparison",
        "cropping"
      ],
      "staged_hint": "Separate the nonzero regions first, then compare them before thinking about the output size.",
      "written_solution": "Find the largest connected nonzero component in the grid and crop the output to that component's bounding box. Smaller components are discarded.",
      "uses_new_primitive": false,
      "program_name": "rule_m29",
      "program_source": "def rule_m29(g):\n    comps=components_nonzero(g, treat_colors_separately=False)\n    best=max(comps, key=lambda item: len(item[1]))\n    return crop_bbox(g, best[1])",
      "train": [
        {
          "input": [
            "000000000000",
            "020000000000",
            "020000000000",
            "022000000000",
            "000000000000",
            "000000777700",
            "000000777700",
            "000000000000",
            "000000000000",
            "000000000000"
          ],
          "output": [
            "7777",
            "7777"
          ]
        },
        {
          "input": [
            "00002000000",
            "00002000100",
            "00002201110",
            "00000000100",
            "05000000000",
            "05000000000",
            "05000000000",
            "05550000000",
            "00000000000"
          ],
          "output": [
            "500",
            "500",
            "500",
            "555"
          ]
        },
        {
          "input": [
            "0000000000000",
            "0033300000000",
            "0030300000000",
            "0033300000000",
            "0000000000000",
            "0000000000000",
            "0000000000000",
            "0000000099900",
            "0000000099900",
            "0000000000000",
            "0000000000000"
          ],
          "output": [
            "333",
            "303",
            "333"
          ]
        },
        {
          "input": [
            "000000000000",
            "080800000000",
            "088800000000",
            "000000666600",
            "000000666600",
            "000000666600",
            "000000000000",
            "000000000000"
          ],
          "output": [
            "6666",
            "6666",
            "6666"
          ]
        }
      ],
      "test": {
        "input": [
          "0000000000000",
          "0000000004000",
          "0000033304400",
          "0000030300440",
          "0050033300000",
          "0050000000000",
          "0050000000000",
          "0055500000000",
          "0000000000000",
          "0000000000000"
        ],
        "output": [
          "333",
          "303",
          "333"
        ]
      }
    },
    {
      "id": "M30",
      "title": "Marker-Framed Crop",
      "difficulty": "medium",
      "skills": [
        "command marker",
        "cropping",
        "padding"
      ],
      "staged_hint": "One cell is not part of the object at all: it tells you how to package the object.",
      "written_solution": "Use the top-left marker color as the border color. Crop the rest of the nonzero object to its bounding box, then surround that crop with a one-cell frame of the marker color.",
      "uses_new_primitive": false,
      "program_name": "rule_m30",
      "program_source": "def rule_m30(g):\n    frame_color=g[0][0]\n    cells=[(r,c) for r,row in enumerate(g) for c,v in enumerate(row) if v!=0 and not (r==0 and c==0)]\n    core=crop_bbox(g, cells)\n    ch,cw=size(core)\n    out=blank(ch+2, cw+2, frame_color)\n    for r in range(ch):\n        for c in range(cw):\n            out[r+1][c+1]=core[r][c]\n    return out",
      "train": [
        {
          "input": [
            "80000000000",
            "00000000000",
            "00000000000",
            "00000012000",
            "00000010200",
            "00000022200",
            "00000000000",
            "00000000000",
            "00000000000"
          ],
          "output": [
            "88888",
            "81208",
            "81028",
            "82228",
            "88888"
          ]
        },
        {
          "input": [
            "4000000000",
            "0000000000",
            "0000000000",
            "0000000000",
            "0000000000",
            "0056000000",
            "0050600000",
            "0055600000",
            "0005000000",
            "0000000000"
          ],
          "output": [
            "44444",
            "45604",
            "45064",
            "45564",
            "40504",
            "44444"
          ]
        },
        {
          "input": [
            "300000000000",
            "000000000000",
            "000000078000",
            "000000070880",
            "000000007800",
            "000000000000",
            "000000000000",
            "000000000000"
          ],
          "output": [
            "333333",
            "378003",
            "370883",
            "307803",
            "333333"
          ]
        },
        {
          "input": [
            "60000000000",
            "00000000000",
            "00000000000",
            "00000000000",
            "00000000000",
            "00000000000",
            "00003400000",
            "00003044000",
            "00000340000",
            "00000000000",
            "00000000000"
          ],
          "output": [
            "666666",
            "634006",
            "630446",
            "603406",
            "666666"
          ]
        }
      ],
      "test": {
        "input": [
          "500000000000",
          "000000000000",
          "000000000000",
          "000000000000",
          "000000023000",
          "000000020300",
          "000000022200",
          "000000002000",
          "000000000000",
          "000000000000"
        ],
        "output": [
          "55555",
          "52305",
          "52035",
          "52225",
          "50205",
          "55555"
        ]
      }
    },
    {
      "id": "M31",
      "title": "Fill Enclosed Holes",
      "difficulty": "medium",
      "skills": [
        "enclosure",
        "flood fill",
        "interior detection"
      ],
      "staged_hint": "Think in terms of zero-regions, not colored regions. The key question is whether a zero region can escape to the outer border.",
      "written_solution": "Any black(0) region that is completely enclosed and does not touch the outer border is filled with orange(7). Border-connected zero regions remain black.",
      "uses_new_primitive": false,
      "program_name": "rule_m31",
      "program_source": "def rule_m31(g):\n    out=clone(g)\n    for cells,touch in components_zero(g):\n        if touch:\n            continue\n        for r,c in cells:\n            out[r][c]=7\n    return out",
      "train": [
        {
          "input": [
            "00000000000",
            "02222000000",
            "02002004440",
            "02002004040",
            "02002004040",
            "02222004040",
            "00000004440",
            "03000000000",
            "00000000000"
          ],
          "output": [
            "00000000000",
            "02222000000",
            "02772004440",
            "02772004740",
            "02772004740",
            "02222004740",
            "00000004440",
            "03000000000",
            "00000000000"
          ]
        },
        {
          "input": [
            "0000000000",
            "0066666600",
            "0060000600",
            "0060000600",
            "0066666600",
            "0000000000",
            "0000000005",
            "0000000000"
          ],
          "output": [
            "0000000000",
            "0066666600",
            "0067777600",
            "0067777600",
            "0066666600",
            "0000000000",
            "0000000005",
            "0000000000"
          ]
        },
        {
          "input": [
            "000000000000",
            "000000008880",
            "003333008080",
            "003003008080",
            "003003008880",
            "003003000000",
            "003003000000",
            "003333000000",
            "000000000000",
            "000000000000"
          ],
          "output": [
            "000000000000",
            "000000008880",
            "003333008780",
            "003773008780",
            "003773008880",
            "003773000000",
            "003773000000",
            "003333000000",
            "000000000000",
            "000000000000"
          ]
        },
        {
          "input": [
            "000000002",
            "055555550",
            "050000050",
            "050000050",
            "050000050",
            "050000050",
            "050000050",
            "055555550",
            "000000000"
          ],
          "output": [
            "000000002",
            "055555550",
            "057777750",
            "057777750",
            "057777750",
            "057777750",
            "057777750",
            "055555550",
            "000000000"
          ]
        }
      ],
      "test": {
        "input": [
          "00000000006",
          "04444000000",
          "04004000000",
          "04004022220",
          "04004020020",
          "04004020020",
          "04444020020",
          "00000020020",
          "00000022220",
          "00000000000"
        ],
        "output": [
          "00000000006",
          "04444000000",
          "04774000000",
          "04774022220",
          "04774027720",
          "04774027720",
          "04444027720",
          "00000027720",
          "00000022220",
          "00000000000"
        ]
      }
    },
    {
      "id": "M32",
      "title": "Area-Sorted Color Row",
      "difficulty": "medium",
      "skills": [
        "component area",
        "ranking",
        "symbolic output"
      ],
      "staged_hint": "The output forgets geometry but remembers object size order.",
      "written_solution": "Measure the area of each connected colored component. Output a single row containing their colors sorted from smallest component to largest component.",
      "uses_new_primitive": false,
      "program_name": "rule_m32",
      "program_source": "def rule_m32(g):\n    comps=components_nonzero(g, treat_colors_separately=True)\n    items=sorted(((len(cells), color) for color,cells in comps), key=lambda x:(x[0], x[1]))\n    return [[color for _,color in items]]",
      "train": [
        {
          "input": [
            "000000000000",
            "088880000000",
            "088880000000",
            "000000000000",
            "000060000000",
            "000060000000",
            "000060000100",
            "000066600100",
            "000000000110",
            "000000000000"
          ],
          "output": [
            "168"
          ]
        },
        {
          "input": [
            "0000100000000",
            "0000100040000",
            "0000110044000",
            "0000000004400",
            "0555500000000",
            "0555500000000",
            "0555500000000",
            "0000000000000",
            "0000000000000"
          ],
          "output": [
            "145"
          ]
        },
        {
          "input": [
            "00000000000",
            "03330000000",
            "03000000000",
            "03330000000",
            "00000000000",
            "00000000000",
            "00000004000",
            "00000004400",
            "08888000440",
            "08888000000",
            "00000000000"
          ],
          "output": [
            "438"
          ]
        },
        {
          "input": [
            "00000000000000",
            "00000000006000",
            "00000000006000",
            "00000000006000",
            "00000333006660",
            "00000300000000",
            "01000333000000",
            "01000000888800",
            "01100000888800",
            "00000000000000"
          ],
          "output": [
            "1638"
          ]
        }
      ],
      "test": {
        "input": [
          "0000000000000",
          "0000000003330",
          "0040000003000",
          "0044000003330",
          "0004400000000",
          "0000000555500",
          "0000000555500",
          "0000000555500",
          "0000000000000",
          "0000000000000",
          "0000000000000",
          "0000000000000"
        ],
        "output": [
          "435"
        ]
      }
    },
    {
      "id": "M33",
      "title": "Axis Command Mirror",
      "difficulty": "medium",
      "skills": [
        "command decoding",
        "reflection",
        "same-size duplication"
      ],
      "staged_hint": "The nonzero corner cell is a literal command: decode it before touching the object.",
      "written_solution": "Read the top-left command cell. If it is blue(1), mirror the non-command pattern across the vertical axis; if it is red(2), mirror it across the horizontal axis. Keep the command cell.",
      "uses_new_primitive": false,
      "program_name": "rule_m33",
      "program_source": "def rule_m33(g):\n    h,w=size(g)\n    cmd=g[0][0]\n    work=blank(h,w)\n    for r,row in enumerate(g):\n        for c,v in enumerate(row):\n            if v!=0 and not (r==0 and c==0):\n                work[r][c]=v\n    out = mirror_v(work) if cmd==1 else mirror_h(work)\n    out[0][0]=cmd\n    return out",
      "train": [
        {
          "input": [
            "1000000000",
            "0000000000",
            "0120000000",
            "0102000000",
            "0222000000",
            "0000000000",
            "0000000000",
            "0000000000"
          ],
          "output": [
            "1000000000",
            "0000000000",
            "0120000210",
            "0102002010",
            "0222002220",
            "0000000000",
            "0000000000",
            "0000000000"
          ]
        },
        {
          "input": [
            "20000000000",
            "00000034000",
            "00000030400",
            "00000004400",
            "00000000000",
            "00000000000",
            "00000000000",
            "00000000000",
            "00000000000"
          ],
          "output": [
            "20000000000",
            "00000034000",
            "00000030400",
            "00000004400",
            "00000000000",
            "00000004400",
            "00000030400",
            "00000034000",
            "00000000000"
          ]
        },
        {
          "input": [
            "100000000000",
            "000000000000",
            "000000000000",
            "000000000000",
            "005600000000",
            "005066000000",
            "000560000000",
            "000000000000",
            "000000000000",
            "000000000000"
          ],
          "output": [
            "100000000000",
            "000000000000",
            "000000000000",
            "000000000000",
            "005600006500",
            "005066660500",
            "000560065000",
            "000000000000",
            "000000000000",
            "000000000000"
          ]
        },
        {
          "input": [
            "200000000",
            "078000000",
            "070800000",
            "088800000",
            "000000000",
            "000000000",
            "000000000",
            "000000000"
          ],
          "output": [
            "200000000",
            "078000000",
            "070800000",
            "088800000",
            "088800000",
            "070800000",
            "078000000",
            "000000000"
          ]
        }
      ],
      "test": {
        "input": [
          "10000000000",
          "00000000000",
          "00000000000",
          "00000000000",
          "00000000000",
          "00340000000",
          "00304000000",
          "00044000000",
          "00000000000",
          "00000000000"
        ],
        "output": [
          "10000000000",
          "00000000000",
          "00000000000",
          "00000000000",
          "00000000000",
          "00340004300",
          "00304040300",
          "00044044000",
          "00000000000",
          "00000000000"
        ]
      }
    },
    {
      "id": "M34",
      "title": "Template Broadcast",
      "difficulty": "medium",
      "skills": [
        "template extraction",
        "broadcast",
        "new primitive"
      ],
      "staged_hint": "The top-left 3\u00d73 patch is an exemplar. The lone 2s elsewhere tell you where to replay it.",
      "written_solution": "Treat the top-left 3\u00d73 motif as a template whose center is the digit 2. Stamp that exact 3\u00d73 motif, centered, at every other red(2) anchor in the grid.",
      "uses_new_primitive": true,
      "program_name": "rule_m34",
      "program_source": "def rule_m34(g):\n    template=[row[:3] for row in g[:3]]\n    anchors=[(r,c) for r,row in enumerate(g) for c,v in enumerate(row)\n             if v==2 and not (0<=r<3 and 0<=c<3)]\n    return stamp_template(g, anchors, template, center=(1,1), keep_anchor=True)",
      "train": [
        {
          "input": [
            "0300000000",
            "3230000000",
            "0300000000",
            "0000000000",
            "0000000000",
            "0000020000",
            "0000000000",
            "0000000020",
            "0000000000"
          ],
          "output": [
            "0300000000",
            "3230000000",
            "0300000000",
            "0000000000",
            "0000030000",
            "0000323000",
            "0000030030",
            "0000000323",
            "0000000030"
          ]
        },
        {
          "input": [
            "40400000000",
            "02000000000",
            "40400000000",
            "00000000000",
            "00000002000",
            "00000000000",
            "00000000000",
            "00002000000",
            "00000000000",
            "00000000000"
          ],
          "output": [
            "40400000000",
            "02000000000",
            "40400000000",
            "00000040400",
            "00000002000",
            "00000040400",
            "00040400000",
            "00002000000",
            "00040400000",
            "00000000000"
          ]
        },
        {
          "input": [
            "050000000000",
            "252000000000",
            "050000000000",
            "000000000200",
            "000000000000",
            "000000000000",
            "000000200000",
            "000000000000"
          ],
          "output": [
            "050000000000",
            "252000000000",
            "050000000500",
            "000000002220",
            "000000000500",
            "000000500000",
            "000002220000",
            "000000500000"
          ]
        },
        {
          "input": [
            "60600000000",
            "02000000000",
            "60600000000",
            "00000000000",
            "00000000020",
            "00000200000",
            "00000000000",
            "00000000000",
            "00000000200",
            "00000000000",
            "00000000000"
          ],
          "output": [
            "60600000000",
            "02000000000",
            "60600000000",
            "00000000606",
            "00006060020",
            "00000200606",
            "00006060000",
            "00000006060",
            "00000000200",
            "00000006060",
            "00000000000"
          ]
        }
      ],
      "test": {
        "input": [
          "070000000000",
          "727000000000",
          "070000000000",
          "000000000000",
          "000002000000",
          "000000000000",
          "000000000000",
          "000000000200",
          "000000000000",
          "000000000000"
        ],
        "output": [
          "070000000000",
          "727000000000",
          "070000000000",
          "000007000000",
          "000072700000",
          "000007000000",
          "000000000700",
          "000000007270",
          "000000000700",
          "000000000000"
        ]
      }
    },
    {
      "id": "M35",
      "title": "Midpoint Dots",
      "difficulty": "medium",
      "skills": [
        "pairing",
        "alignment",
        "midpoint inference"
      ],
      "staged_hint": "Group cells by color. Each group forms one aligned pair whose halfway point is what matters.",
      "written_solution": "For each color, the two input cells define a horizontal or vertical segment of odd length. Mark the exact midpoint of that segment with maroon(9), keeping the endpoints unchanged.",
      "uses_new_primitive": false,
      "program_name": "rule_m35",
      "program_source": "def rule_m35(g):\n    out=clone(g)\n    groups=collections.defaultdict(list)\n    for r,row in enumerate(g):\n        for c,v in enumerate(row):\n            if v!=0:\n                groups[v].append((r,c))\n    for color,cells in groups.items():\n        if len(cells)!=2:\n            continue\n        (r0,c0),(r1,c1)=cells\n        if r0==r1 and abs(c1-c0)%2==0:\n            out[r0][(c0+c1)//2]=9\n        elif c0==c1 and abs(r1-r0)%2==0:\n            out[(r0+r1)//2][c0]=9\n    return out",
      "train": [
        {
          "input": [
            "0000000000",
            "0000000000",
            "0100000100",
            "0000000000",
            "0000000000",
            "0000300000",
            "0000000000",
            "0000300000"
          ],
          "output": [
            "0000000000",
            "0000000000",
            "0100900100",
            "0000000000",
            "0000000000",
            "0000300000",
            "0000900000",
            "0000300000"
          ]
        },
        {
          "input": [
            "000000000",
            "004000000",
            "000000000",
            "000000000",
            "000000000",
            "004000000",
            "060000060",
            "000000000",
            "000000000"
          ],
          "output": [
            "000000000",
            "004000000",
            "000000000",
            "009000000",
            "000000000",
            "004000000",
            "060090060",
            "000000000",
            "000000000"
          ]
        },
        {
          "input": [
            "00000000000",
            "00000080000",
            "00000000000",
            "02000000020",
            "00000000000",
            "00000080000",
            "00000000000"
          ],
          "output": [
            "00000000000",
            "00000080000",
            "00000000000",
            "02000990020",
            "00000000000",
            "00000080000",
            "00000000000"
          ]
        },
        {
          "input": [
            "000000000000",
            "000000000300",
            "005000000000",
            "000000000000",
            "000000070070",
            "000000000300",
            "000000000000",
            "000000000000",
            "005000000000",
            "000000000000"
          ],
          "output": [
            "000000000000",
            "000000000300",
            "005000000000",
            "000000000900",
            "000000070070",
            "009000000300",
            "000000000000",
            "000000000000",
            "005000000000",
            "000000000000"
          ]
        }
      ],
      "test": {
        "input": [
          "000000000000",
          "000100000100",
          "000000000000",
          "000000006000",
          "000000000000",
          "040000040000",
          "000000000000",
          "000000006000",
          "000000000000"
        ],
        "output": [
          "000000000000",
          "000100900100",
          "000000000000",
          "000000006000",
          "000000000000",
          "040090049000",
          "000000000000",
          "000000006000",
          "000000000000"
        ]
      }
    },
    {
      "id": "H29",
      "title": "Depth-Colored Nested Frames",
      "difficulty": "hard",
      "skills": [
        "nested containment",
        "ordering",
        "recoloring"
      ],
      "staged_hint": "Do not treat all frames equally. Their relative containment determines the output colors.",
      "written_solution": "The input consists of nested rectangular frames. Recolor the outermost frame to red(2), the next nested frame to green(3), the next to yellow(4), and so on in depth order, preserving the frame shapes.",
      "uses_new_primitive": false,
      "program_name": "rule_h29",
      "program_source": "def rule_h29(g):\n    h,w=size(g)\n    comps=components_nonzero(g, treat_colors_separately=False)\n    items=[]\n    for _,cells in comps:\n        r0,c0,r1,c1=bbox(cells)\n        area=(r1-r0+1)*(c1-c0+1)\n        items.append((-(area), cells))\n    items.sort(key=lambda x:x[0])\n    out=blank(h,w)\n    for idx,(_,cells) in enumerate(items):\n        color=2+idx\n        for r,c in cells:\n            out[r][c]=color\n    return out",
      "train": [
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
            "000000000000",
            "011111111110",
            "010000000010",
            "010111111010",
            "010100001010",
            "010100001010",
            "010111111010",
            "010000000010",
            "011111111110",
            "000000000000"
          ],
          "output": [
            "000000000000",
            "022222222220",
            "020000000020",
            "020333333020",
            "020300003020",
            "020300003020",
            "020333333020",
            "020000000020",
            "022222222220",
            "000000000000"
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
        }
      ],
      "test": {
        "input": [
          "000000000000",
          "011111111110",
          "010000000010",
          "010111111010",
          "010100001010",
          "010101101010",
          "010101101010",
          "010100001010",
          "010111111010",
          "010000000010",
          "011111111110",
          "000000000000"
        ],
        "output": [
          "000000000000",
          "022222222220",
          "020000000020",
          "020333333020",
          "020300003020",
          "020304403020",
          "020304403020",
          "020300003020",
          "020333333020",
          "020000000020",
          "022222222220",
          "000000000000"
        ]
      }
    },
    {
      "id": "H30",
      "title": "Guide-Selected Mirror",
      "difficulty": "hard",
      "skills": [
        "relational command",
        "axis inference",
        "reflection"
      ],
      "staged_hint": "There is no symbolic command value. The two guide cells communicate the axis through their alignment.",
      "written_solution": "Find the two gray(5) guide cells. If they share a row, mirror the non-guide pattern across the horizontal axis; if they share a column, mirror it across the vertical axis. Keep the guides.",
      "uses_new_primitive": false,
      "program_name": "rule_h30",
      "program_source": "def rule_h30(g):\n    h,w=size(g)\n    guides=[(r,c) for r,row in enumerate(g) for c,v in enumerate(row) if v==5]\n    work=blank(h,w)\n    for r,row in enumerate(g):\n        for c,v in enumerate(row):\n            if v!=0 and v!=5:\n                work[r][c]=v\n    if len(guides)==2 and guides[0][0]==guides[1][0]:\n        out=mirror_h(work)\n    else:\n        out=mirror_v(work)\n    for r,c in guides:\n        out[r][c]=5\n    return out",
      "train": [
        {
          "input": [
            "00500000500",
            "00000000000",
            "01200000000",
            "01020000000",
            "02220000000",
            "00000000000",
            "00000000000",
            "00000000000",
            "00000000000"
          ],
          "output": [
            "00500000500",
            "00000000000",
            "01200000000",
            "01020000000",
            "02220000000",
            "01020000000",
            "01200000000",
            "00000000000",
            "00000000000"
          ]
        },
        {
          "input": [
            "000000000000",
            "500000000000",
            "000000034000",
            "000000030400",
            "000000004400",
            "000000000000",
            "000000000000",
            "000000000000",
            "500000000000",
            "000000000000"
          ],
          "output": [
            "000000000000",
            "500000000000",
            "000430034000",
            "004030030400",
            "004400004400",
            "000000000000",
            "000000000000",
            "000000000000",
            "500000000000",
            "000000000000"
          ]
        },
        {
          "input": [
            "00000000000",
            "00000000000",
            "00000000000",
            "00560000000",
            "00506600000",
            "00056000000",
            "00000000000",
            "00000000000",
            "00000000000",
            "00000000000",
            "00050000500"
          ],
          "output": [
            "00000000000",
            "00000000000",
            "00000000000",
            "00560006000",
            "00506660000",
            "00056060000",
            "00000000000",
            "00000000000",
            "00000000000",
            "00000000000",
            "00050000500"
          ]
        },
        {
          "input": [
            "0000000000",
            "0780000005",
            "0708000000",
            "0888000000",
            "0000000000",
            "0000000000",
            "0000000005",
            "0000000000"
          ],
          "output": [
            "0000000000",
            "0780000875",
            "0708008070",
            "0888008880",
            "0000000000",
            "0000000000",
            "0000000005",
            "0000000000"
          ]
        }
      ],
      "test": {
        "input": [
          "00000500000",
          "00000000000",
          "00000000000",
          "00000000000",
          "03400000000",
          "03040000000",
          "00440000000",
          "00000000000",
          "00000000000",
          "00000500000"
        ],
        "output": [
          "00000500000",
          "00000000000",
          "00000000000",
          "00000000000",
          "03400000430",
          "03040004030",
          "00440004400",
          "00000000000",
          "00000000000",
          "00000500000"
        ]
      }
    },
    {
      "id": "H31",
      "title": "Color-Frequency Ranking",
      "difficulty": "hard",
      "skills": [
        "global counting",
        "aggregation by color",
        "symbolic output"
      ],
      "staged_hint": "Same-color pieces may be split across the grid. Aggregate by color before ranking.",
      "written_solution": "Count the total number of cells of each nonzero color across the whole grid, combining all components of that color. Output one row of colors ordered from highest total count to lowest.",
      "uses_new_primitive": false,
      "program_name": "rule_h31",
      "program_source": "def rule_h31(g):\n    counts=collections.Counter(v for row in g for v in row if v!=0)\n    order=sorted(counts.items(), key=lambda kv:(-kv[1], kv[0]))\n    return [[color for color,_ in order]]",
      "train": [
        {
          "input": [
            "000000000000",
            "022220000000",
            "022220000000",
            "000000400000",
            "000000440000",
            "000000044000",
            "000000003000",
            "000000003000",
            "000000003300",
            "000000000000"
          ],
          "output": [
            "243"
          ]
        },
        {
          "input": [
            "0000000000000",
            "0555500000000",
            "0555500000000",
            "0555500000000",
            "0000000000000",
            "0000600000000",
            "0000600000100",
            "0000600001110",
            "0000666000100",
            "0101010000000",
            "0000000000000"
          ],
          "output": [
            "516"
          ]
        },
        {
          "input": [
            "00000000000",
            "08880000070",
            "08000000000",
            "08880000000",
            "00000000000",
            "08080800000",
            "00000070700",
            "00000077700",
            "00000000000",
            "00000000000"
          ],
          "output": [
            "87"
          ]
        },
        {
          "input": [
            "00000000000009",
            "00000000004000",
            "00000000004409",
            "00000000000440",
            "09990000000009",
            "09990000000000",
            "00000000000009",
            "00000000000000",
            "00000000000000"
          ],
          "output": [
            "94"
          ]
        }
      ],
      "test": {
        "input": [
          "202020000000",
          "060000000000",
          "060000000000",
          "060000000000",
          "066600000000",
          "000000022200",
          "000000022200",
          "000000000000",
          "000000000000",
          "000000000000"
        ],
        "output": [
          "26"
        ]
      }
    },
    {
      "id": "H32",
      "title": "Normalized Shape XOR",
      "difficulty": "hard",
      "skills": [
        "shape normalization",
        "boolean composition",
        "resize"
      ],
      "staged_hint": "The two shapes are compared after cropping away their surrounding whitespace.",
      "written_solution": "Crop the color-1 shape and the color-2 shape to their own bounding boxes, align both cropped binaries to the top-left corner of a common canvas, and output their XOR silhouette in orange(7).",
      "uses_new_primitive": false,
      "program_name": "rule_h32",
      "program_source": "def rule_h32(g):\n    cells1=[(r,c) for r,row in enumerate(g) for c,v in enumerate(row) if v==1]\n    cells2=[(r,c) for r,row in enumerate(g) for c,v in enumerate(row) if v==2]\n    s1=binary_shape_from_cells(cells1)\n    s2=binary_shape_from_cells(cells2)\n    h=max(len(s1), len(s2))\n    w=max(len(s1[0]), len(s2[0]))\n    out=blank(h,w)\n    for r in range(h):\n        for c in range(w):\n            a = r < len(s1) and c < len(s1[0]) and s1[r][c] == 1\n            b = r < len(s2) and c < len(s2[0]) and s2[r][c] == 1\n            if bool(a) ^ bool(b):\n                out[r][c]=7\n    return out",
      "train": [
        {
          "input": [
            "0000000000",
            "0110000000",
            "0011000000",
            "0000000000",
            "0000000000",
            "0000000000",
            "0000002220",
            "0000002000",
            "0000000000",
            "0000000000"
          ],
          "output": [
            "007",
            "777"
          ]
        },
        {
          "input": [
            "000000000000",
            "000000000100",
            "000000001110",
            "000000000100",
            "000000000000",
            "022000000000",
            "002200000000",
            "000000000000",
            "000000000000"
          ],
          "output": [
            "700",
            "700",
            "070"
          ]
        },
        {
          "input": [
            "00000000000",
            "00000000000",
            "00111000000",
            "00101000000",
            "00000000000",
            "00000000000",
            "00000000000",
            "00000002200",
            "00000022000",
            "00000000000",
            "00000000000"
          ],
          "output": [
            "700",
            "077"
          ]
        },
        {
          "input": [
            "0000000000000",
            "0100000000000",
            "0111000000000",
            "0000000000000",
            "0000000022200",
            "0000000002000",
            "0000000000000",
            "0000000000000"
          ],
          "output": [
            "077",
            "707"
          ]
        }
      ],
      "test": {
        "input": [
          "000000000000",
          "011100000000",
          "000110000000",
          "000000000000",
          "000000000000",
          "000000000000",
          "000000022200",
          "000000220000",
          "000000000000",
          "000000000000"
        ],
        "output": [
          "7007",
          "7777"
        ]
      }
    },
    {
      "id": "H33",
      "title": "Perimeter-Sorted Shape Stack",
      "difficulty": "hard",
      "skills": [
        "perimeter computation",
        "sorting",
        "shape serialization"
      ],
      "staged_hint": "The output keeps whole shapes, but their order comes from a geometric statistic, not from position or color alone.",
      "written_solution": "Compute the perimeter of each connected colored component. Crop each component to its own bounding box, sort the cropped shapes from largest perimeter to smallest, and stack them top-to-bottom with one blank row between them.",
      "uses_new_primitive": false,
      "program_name": "rule_h33",
      "program_source": "def rule_h33(g):\n    comps=components_nonzero(g, treat_colors_separately=True)\n    items=[]\n    for color,cells in comps:\n        shape=crop_bbox(g, cells)\n        per=perimeter_of_cells(cells)\n        items.append((-per, color, shape))\n    items.sort(key=lambda x:(x[0], x[1]))\n    width=max(len(shape[0]) for _,_,shape in items)\n    height=sum(len(shape) for _,_,shape in items) + (len(items)-1)\n    out=blank(height, width)\n    cur=0\n    for i,(_,color,shape) in enumerate(items):\n        sh,sw=size(shape)\n        for r in range(sh):\n            for c in range(sw):\n                out[cur+r][c]=shape[r][c]\n        cur += sh\n        if i != len(items)-1:\n            cur += 1\n    return out",
      "train": [
        {
          "input": [
            "0000000000000",
            "0200000000000",
            "0200000088800",
            "0220000080000",
            "0000000088800",
            "0060000000000",
            "0060000000000",
            "0060000000000",
            "0066600000000",
            "0000000000000",
            "0000000000000"
          ],
          "output": [
            "888",
            "800",
            "888",
            "000",
            "600",
            "600",
            "600",
            "666",
            "000",
            "200",
            "200",
            "220"
          ]
        },
        {
          "input": [
            "000000000000",
            "000000040000",
            "000000044000",
            "000000004400",
            "000006000000",
            "000006000000",
            "020006000000",
            "020006660000",
            "022000000000",
            "000000000000"
          ],
          "output": [
            "600",
            "600",
            "600",
            "666",
            "000",
            "400",
            "440",
            "044",
            "000",
            "200",
            "200",
            "220"
          ]
        },
        {
          "input": [
            "00000000000000",
            "08880000000000",
            "08000000000000",
            "08880000000000",
            "00000000000000",
            "00000000000000",
            "00000000000000",
            "00000000004000",
            "00020000004400",
            "00020000000440",
            "00022000000000",
            "00000000000000"
          ],
          "output": [
            "888",
            "800",
            "888",
            "000",
            "400",
            "440",
            "044",
            "000",
            "200",
            "200",
            "220"
          ]
        },
        {
          "input": [
            "00000000000",
            "00000060000",
            "00000060000",
            "00000060000",
            "00000066600",
            "00004000000",
            "00004400000",
            "02000448880",
            "02000008000",
            "02200008880",
            "00000000000"
          ],
          "output": [
            "888",
            "800",
            "888",
            "000",
            "600",
            "600",
            "600",
            "666",
            "000",
            "400",
            "440",
            "044",
            "000",
            "200",
            "200",
            "220"
          ]
        }
      ],
      "test": {
        "input": [
          "0000000000000",
          "0400000088800",
          "0440000080000",
          "0044000088800",
          "0000000000000",
          "0000000000000",
          "0000002000000",
          "0000002000000",
          "0000002200000",
          "0000000000000"
        ],
        "output": [
          "888",
          "800",
          "888",
          "000",
          "400",
          "440",
          "044",
          "000",
          "200",
          "200",
          "220"
        ]
      }
    },
    {
      "id": "H34",
      "title": "Anchor Motif Substitution",
      "difficulty": "hard",
      "skills": [
        "template substitution",
        "broadcast",
        "new primitive"
      ],
      "staged_hint": "The top-left motif is not literal everywhere: one token inside it stands for the anchor's color.",
      "written_solution": "Use the top-left 3\u00d73 motif as a template. Wherever the template contains 9, substitute the color of the current anchor cell; all other template colors stay literal. Stamp that substituted motif around every anchor outside the template block.",
      "uses_new_primitive": true,
      "program_name": "rule_h34",
      "program_source": "def rule_h34(g):\n    template=[row[:3] for row in g[:3]]\n    anchors=[(r,c,g[r][c]) for r,row in enumerate(g) for c,v in enumerate(row)\n             if v!=0 and not (0<=r<3 and 0<=c<3)]\n    return stamp_template(g, anchors, template, center=(1,1), substitute={9:'anchor'}, keep_anchor=True)",
      "train": [
        {
          "input": [
            "79700000000",
            "90900000000",
            "79700000000",
            "00000000000",
            "00000000000",
            "00000200000",
            "00000000000",
            "00000000400",
            "00000000000",
            "00000000000"
          ],
          "output": [
            "79700000000",
            "90900000000",
            "79700000000",
            "00000000000",
            "00007270000",
            "00002220000",
            "00007277470",
            "00000004440",
            "00000007470",
            "00000000000"
          ]
        },
        {
          "input": [
            "090000000000",
            "979000000000",
            "090000000000",
            "000000000000",
            "000000003000",
            "000000000000",
            "000060000000",
            "000000000000",
            "000000000000"
          ],
          "output": [
            "090000000000",
            "979000000000",
            "090000000000",
            "000000003000",
            "000000033300",
            "000060003000",
            "000666000000",
            "000060000000",
            "000000000000"
          ]
        },
        {
          "input": [
            "70700000000",
            "99900000000",
            "70700000000",
            "00000000000",
            "00000000000",
            "00000600000",
            "00000000000",
            "00000000000",
            "00000000800",
            "00000000000",
            "00000000000"
          ],
          "output": [
            "70700000000",
            "99900000000",
            "70700000000",
            "00000000000",
            "00007070000",
            "00006660000",
            "00007070000",
            "00000007070",
            "00000008880",
            "00000007070",
            "00000000000"
          ]
        },
        {
          "input": [
            "9790000000000",
            "7070000000000",
            "9790000000000",
            "0000000080000",
            "0000000000000",
            "0000000000200",
            "0000000000000",
            "0000060000000",
            "0000000000000",
            "0000000000000"
          ],
          "output": [
            "9790000000000",
            "7070000000000",
            "9790000878000",
            "0000000787000",
            "0000000872720",
            "0000000007270",
            "0000676002720",
            "0000767000000",
            "0000676000000",
            "0000000000000"
          ]
        }
      ],
      "test": {
        "input": [
          "797000000000",
          "090000000000",
          "797000000000",
          "000000000000",
          "000004000000",
          "000000000000",
          "000000000000",
          "000000000600",
          "000000000000",
          "000000000000"
        ],
        "output": [
          "797000000000",
          "090000000000",
          "797000000000",
          "000074700000",
          "000004000000",
          "000074700000",
          "000000007670",
          "000000000600",
          "000000007670",
          "000000000000"
        ]
      }
    },
    {
      "id": "H35",
      "title": "Ray Intersections With Blockers",
      "difficulty": "hard",
      "skills": [
        "line of sight",
        "set intersection",
        "blockers"
      ],
      "staged_hint": "First think of horizontal visibility from the 2s and vertical visibility from the 3s. The answer is where those two sets overlap.",
      "written_solution": "Red(2) sources project horizontally through zeros until blocked by any nonzero cell, and blue(3) sources project vertically the same way. Output cyan(8) only at cells reached by both a red horizontal ray and a blue vertical ray.",
      "uses_new_primitive": false,
      "program_name": "rule_h35",
      "program_source": "def rule_h35(g):\n    h,w=size(g)\n    horiz=blank(h,w)\n    vert=blank(h,w)\n    for r,row in enumerate(g):\n        for c,v in enumerate(row):\n            if v==2:\n                for dc in (-1,1):\n                    cc=c+dc\n                    while 0<=cc<w and g[r][cc]==0:\n                        horiz[r][cc]=1\n                        cc += dc\n            elif v==3:\n                for dr in (-1,1):\n                    rr=r+dr\n                    while 0<=rr<h and g[rr][c]==0:\n                        vert[rr][c]=1\n                        rr += dr\n    out=blank(h,w)\n    for r in range(h):\n        for c in range(w):\n            if horiz[r][c] and vert[r][c]:\n                out[r][c]=8\n    return out",
      "train": [
        {
          "input": [
            "0000300000",
            "0200050000",
            "0000000000",
            "0050000000",
            "0000000000",
            "0000000200",
            "0030000000",
            "0000000000"
          ],
          "output": [
            "0000000000",
            "0000800000",
            "0000000000",
            "0000000000",
            "0000000000",
            "0080800000",
            "0000000000",
            "0000000000"
          ]
        },
        {
          "input": [
            "000000000",
            "000030000",
            "050000000",
            "000000000",
            "020000020",
            "000000000",
            "000000000",
            "000000300",
            "000000005"
          ],
          "output": [
            "000000000",
            "000000000",
            "000000000",
            "000000000",
            "000080800",
            "000000000",
            "000000000",
            "000000000",
            "000000000"
          ]
        },
        {
          "input": [
            "000000000000",
            "000000300000",
            "002000000000",
            "000000000000",
            "000000000000",
            "000500000000",
            "000000000000",
            "020000000000",
            "000300000000",
            "000000000500"
          ],
          "output": [
            "000000000000",
            "000000000000",
            "000000800000",
            "000000000000",
            "000000000000",
            "000000000000",
            "000000000000",
            "000800800000",
            "000000000000",
            "000000000000"
          ]
        },
        {
          "input": [
            "00000000000",
            "00000300000",
            "00000000000",
            "02000000000",
            "00000000500",
            "00500000000",
            "00000000200",
            "00300000000",
            "00000000000"
          ],
          "output": [
            "00000000000",
            "00000000000",
            "00000000000",
            "00000800000",
            "00000000000",
            "00000000000",
            "00800800000",
            "00000000000",
            "00000000000"
          ]
        }
      ],
      "test": {
        "input": [
          "0000000300",
          "0000000000",
          "0200000000",
          "0000000050",
          "0000000000",
          "0005000000",
          "0000000000",
          "0000002000",
          "0003000000",
          "0000000000"
        ],
        "output": [
          "0000000000",
          "0000000000",
          "0000000800",
          "0000000000",
          "0000000000",
          "0000000000",
          "0000000000",
          "0008000800",
          "0000000000",
          "0000000000"
        ]
      }
    }
  ]
}
''')

PUZZLES = PAYLOAD['puzzles']

def validate():
    problems = []
    for puzzle in PUZZLES:
        fn = RULES[puzzle["id"]]
        for i, pair in enumerate(puzzle["train"], start=1):
            inp = grid_from_strings(pair["input"])
            expected = pair["output"]
            got = strings_from_grid(fn(inp))
            if got != expected:
                problems.append((puzzle["id"], f"train_{i}", expected, got))
        test_inp = grid_from_strings(puzzle["test"]["input"])
        test_expected = puzzle["test"]["output"]
        test_got = strings_from_grid(fn(test_inp))
        if test_got != test_expected:
            problems.append((puzzle["id"], "test", test_expected, test_got))
    return problems

def write_json(path: str | Path):
    Path(path).write_text(json.dumps({
        "set": SUMMARY["set"],
        "summary": SUMMARY,
        "puzzles": PUZZLES,
    }, indent=2))

if __name__ == "__main__":
    issues = validate()
    if issues:
        print(f"Validation failed: {len(issues)} mismatches")
        for item in issues[:10]:
            print(item[0], item[1])
        raise SystemExit(1)
    print(f"Validated {len(PUZZLES)} puzzles ({SUMMARY['train_pair_count']} train pairs).")
