"""ARC additional puzzle bank (21 puzzles, set 3).

This companion file provides trustworthy Python reference implementations,
the full puzzle data, and a validation routine.
Set 3 raises the average number of train pairs per puzzle to improve
supervision density for iterative ARC solvers.
"""
from __future__ import annotations
from typing import List, Dict, Any

Grid = List[List[int]]

def blank(h,w,val=0):
    return [[val]*w for _ in range(h)]

def clone(g):
    return [row[:] for row in g]

def size(g):
    return len(g), len(g[0])

def strings(g):
    return ["".join(str(x) for x in row) for row in g]

def grid_from_strings(*rows):
    return [[int(ch) for ch in row] for row in rows]

def place_point(g, r, c, color):
    h,w=size(g)
    assert 0 <= r < h and 0 <= c < w
    assert g[r][c] == 0 or g[r][c] == color
    g[r][c] = color

def stamp_shape(g, top, left, cells, color):
    h,w=size(g)
    for dr,dc in cells:
        r,c = top+dr, left+dc
        assert 0 <= r < h and 0 <= c < w
        assert g[r][c] == 0 or g[r][c] == color
        g[r][c] = color

def add_frame(g, top, left, hgt, wid, color=1):
    h,w=size(g)
    assert top >=0 and left>=0 and top+hgt<=h and left+wid<=w
    assert hgt>=3 and wid>=3
    for c in range(left, left+wid):
        assert g[top][c] == 0 or g[top][c] == color
        assert g[top+hgt-1][c] == 0 or g[top+hgt-1][c] == color
        g[top][c] = color
        g[top+hgt-1][c] = color
    for r in range(top, top+hgt):
        assert g[r][left] == 0 or g[r][left] == color
        assert g[r][left+wid-1] == 0 or g[r][left+wid-1] == color
        g[r][left] = color
        g[r][left+wid-1] = color

def add_rect(g, top, left, hgt, wid, color):
    h,w=size(g)
    assert top >=0 and left>=0 and top+hgt<=h and left+wid<=w
    for r in range(top, top+hgt):
        for c in range(left, left+wid):
            assert g[r][c] == 0 or g[r][c] == color
            g[r][c] = color

def orth_neighbors(r,c,h,w):
    for dr,dc in [(-1,0),(1,0),(0,-1),(0,1)]:
        nr,nc=r+dr,c+dc
        if 0<=nr<h and 0<=nc<w:
            yield nr,nc

def components(g, colors=None, ignore_zero=True):
    h,w=size(g)
    vis=[[False]*w for _ in range(h)]
    comps=[]
    for r in range(h):
        for c in range(w):
            if vis[r][c]:
                continue
            vis[r][c]=True
            val=g[r][c]
            if (ignore_zero and val==0) or (colors is not None and val not in colors):
                continue
            q=[(r,c)]
            cells=[(r,c)]
            while q:
                rr,cc=q.pop()
                for nr,nc in orth_neighbors(rr,cc,h,w):
                    if not vis[nr][nc] and g[nr][nc]==val:
                        vis[nr][nc]=True
                        q.append((nr,nc))
                        cells.append((nr,nc))
            comps.append((val,cells))
    return comps

def bbox(cells):
    rs=[r for r,c in cells]; cs=[c for r,c in cells]
    return min(rs),max(rs),min(cs),max(cs)

def crop_bbox(g, cells):
    r0,r1,c0,c1 = bbox(cells)
    return [row[c0:c1+1] for row in g[r0:r1+1]]

def is_rect_frame(cells):
    r0,r1,c0,c1=bbox(cells)
    if r1-r0<2 or c1-c0<2:
        return False
    s=set(cells)
    exp=set()
    for c in range(c0,c1+1):
        exp.add((r0,c)); exp.add((r1,c))
    for r in range(r0,r1+1):
        exp.add((r,c0)); exp.add((r,c1))
    return s==exp

def is_solid_rect(cells):
    r0,r1,c0,c1=bbox(cells)
    s=set(cells)
    exp={(r,c) for r in range(r0,r1+1) for c in range(c0,c1+1)}
    return s==exp

SHAPES = {'DOM2': [(0, 0), (0, 1)],
 'J5': [(0, 1), (1, 1), (2, 0), (2, 1), (2, 2)],
 'L': [(0, 0), (1, 0), (2, 0), (2, 1)],
 'LINE3': [(0, 0), (0, 1), (0, 2)],
 'P5': [(0, 0), (0, 1), (1, 0), (1, 1), (2, 0)],
 'RECT6': [(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2)],
 'S5': [(0, 0), (1, 0), (1, 1), (1, 2), (2, 2)],
 'SQ4': [(0, 0), (0, 1), (1, 0), (1, 1)],
 'T': [(0, 1), (1, 0), (1, 1), (1, 2)],
 'U': [(0, 0), (0, 2), (1, 0), (1, 1), (1, 2)],
 'Z': [(0, 0), (0, 1), (1, 1), (1, 2)]}

def rule_e15(g):
    h,w=size(g); out=clone(g)
    for r in range(h):
        for c in range(w):
            if g[r][c]==2:
                for dr,dc in [(-1,-1),(-1,1),(1,-1),(1,1)]:
                    nr,nc=r+dr,c+dc
                    if 0<=nr<h and 0<=nc<w and out[nr][nc]==0:
                        out[nr][nc]=6
    return out

def rule_e16(g):
    h,w=size(g); out=clone(g)
    for r in range(1,h-1):
        for c in range(1,w-1):
            if g[r][c]==0 and g[r-1][c-1]==1 and g[r-1][c+1]==1 and g[r+1][c-1]==1 and g[r+1][c+1]==1:
                out[r][c]=8
    return out

def rule_e17(g):
    h,w=size(g); out=clone(g)
    for r in range(h):
        for c in range(1,w-1):
            if g[r][c]==0 and g[r][c-1]==5 and g[r][c+1]==5:
                out[r][c]=3
    return out

def rule_e18(g):
    h,w=size(g); out=clone(g)
    for r in range(1,h-1):
        for c in range(w):
            if g[r][c]==0 and g[r-1][c]==7 and g[r+1][c]==7:
                out[r][c]=4
    return out

def rule_e19(g):
    h,w=size(g); out=clone(g)
    for r in range(h-1):
        for c in range(w-1):
            block=[g[r][c],g[r][c+1],g[r+1][c],g[r+1][c+1]]
            if block[0]==8 and block[3]==8 and block[1]==0 and block[2]==0:
                out[r][c+1]=1; out[r+1][c]=1
            if block[1]==8 and block[2]==8 and block[0]==0 and block[3]==0:
                out[r][c]=1; out[r+1][c+1]=1
    return out

def rule_e20(g):
    h,w=size(g); out=clone(g)
    for r in range(h):
        for c in range(w-1):
            if g[r][c]==4 and g[r][c+1]==4:
                if c-1 >= 0 and g[r][c-1]==0:
                    out[r][c-1]=9
                if c+2 < w and g[r][c+2]==0:
                    out[r][c+2]=9
    return out

def rule_e21(g):
    h,w=size(g); out=clone(g)
    for r in range(h):
        colors={v for v in g[r] if v not in (0,9)}
        has9=any(v==9 for v in g[r])
        if len(colors)==1 and has9:
            color=next(iter(colors))
            for c in range(w):
                if g[r][c]==9:
                    out[r][c]=color
    return out

def rule_m15(g):
    h,w=size(g)
    marker_cells=[(r,c) for r in range(h) for c in range(w) if g[r][c]==2]
    comps=[cells for val,cells in components(g, colors={3})]
    marker_set=set(marker_cells)
    chosen=None
    for cells in comps:
        s=set(cells)
        for r,c in cells:
            for nr,nc in orth_neighbors(r,c,h,w):
                if (nr,nc) in marker_set:
                    chosen=cells
                    break
            if chosen is not None:
                break
        if chosen is not None:
            break
    assert chosen is not None
    r0,r1,c0,c1=bbox(chosen)
    out=blank(r1-r0+1,c1-c0+1)
    for r,c in chosen:
        out[r-r0][c-c0]=3
    return out

def rule_m16(g):
    h,w=size(g); out=clone(g)
    frames=[cells for val,cells in components(g, colors={1}) if is_rect_frame(cells)]
    for cells in frames:
        r0,r1,c0,c1=bbox(cells)
        interior_colors={g[r][c] for r in range(r0+1,r1) for c in range(c0+1,c1) if g[r][c] not in (0,1)}
        if len(interior_colors)==1:
            color=next(iter(interior_colors))
            for r,c in cells:
                out[r][c]=color
    return out

def rule_m17(g):
    h,w=size(g); out=clone(g)
    frames=[cells for val,cells in components(g, colors={1}) if is_rect_frame(cells)]
    for cells in frames:
        r0,r1,c0,c1=bbox(cells)
        for r in range(r0+1,r1):
            for c in range(c0+1,c1):
                if g[r][c]==4:
                    mr = r0 + r1 - r
                    if out[mr][c]==0:
                        out[mr][c]=7
    return out

def rule_m18(g):
    h,w=size(g); out=clone(g)
    for val,cells in components(g, colors={6}):
        if not is_solid_rect(cells):
            continue
        r0,r1,c0,c1=bbox(cells)
        for rr,cc in [(r0-1,c0-1),(r0-1,c1+1),(r1+1,c0-1),(r1+1,c1+1)]:
            if 0<=rr<h and 0<=cc<w and out[rr][cc]==0:
                out[rr][cc]=2
    return out

def rule_m19(g):
    h,w=size(g); out=blank(h,w)
    comps=[cells for val,cells in components(g, colors={8})]
    comps_sorted=sorted(comps, key=lambda cells: len(cells))
    recolors=[2,3,4]
    assert len(comps_sorted)==3
    for color,cells in zip(recolors, comps_sorted):
        for r,c in cells:
            out[r][c]=color
    return out

def rule_m20(g):
    h,w=size(g)
    legend_colors=[v for v in g[0] if v!=0]
    assert len(legend_colors)==1
    target=legend_colors[0]
    candidates=[]
    for val,cells in components(g):
        if val==target and all(r>0 for r,c in cells):
            candidates.append(cells)
    assert len(candidates)>=1
    chosen=sorted(candidates, key=lambda cells: (bbox(cells)[0], bbox(cells)[2]))[0]
    return crop_bbox(g, chosen)

def rule_m21(g):
    h,w=size(g)
    comps=[cells for val,cells in components(g, colors={5})]
    assert len(comps)==1
    cells=comps[0]
    marker=[(r,c) for r in range(h) for c in range(w) if g[r][c]==2]
    assert len(marker)==1
    mr,mc=marker[0]
    r0,r1,c0,c1=bbox(cells)
    dr,dc=mr-r0, mc-c0
    out=blank(h,w)
    for r,c in cells:
        nr,nc=r+dr,c+dc
        assert 0<=nr<h and 0<=nc<w
        out[nr][nc]=5
    return out

def rule_h15(g):
    h,w=size(g); out=clone(g)
    top_markers=[c for c,v in enumerate(g[0]) if v==2]
    left_markers=[r for r in range(h) if g[r][0]==2]
    if top_markers:
        axis_c=top_markers[0]
        for r in range(h):
            for c in range(w):
                if g[r][c]==5:
                    mc=2*axis_c - c
                    if 0<=mc<w and out[r][mc]==0:
                        out[r][mc]=7
    else:
        axis_r=left_markers[0]
        for r in range(h):
            for c in range(w):
                if g[r][c]==5:
                    mr=2*axis_r - r
                    if 0<=mr<h and out[mr][c]==0:
                        out[mr][c]=7
    return out

def rule_h16(g):
    h,w=size(g); out=clone(g)
    frames=[bbox(cells) for val,cells in components(g, colors={1}) if is_rect_frame(cells)]
    for r in range(h):
        for c in range(w):
            if g[r][c]==0:
                depth=sum(1 for r0,r1,c0,c1 in frames if r0<r<r1 and c0<c<c1)
                if depth>0:
                    out[r][c]=depth+1
    return out

def rule_h17(g):
    h,w=size(g)
    comps=[cells for val,cells in components(g, colors={6})]
    # choose the non-singleton or largest component as template
    template=max(comps, key=len)
    r0,r1,c0,c1=bbox(template)
    rel=[(r-r0,c-c0) for r,c in template]
    markers=[(r,c) for r in range(h) for c in range(w) if g[r][c]==2]
    out=blank(h,w)
    for mr,mc in markers:
        for dr,dc in rel:
            nr,nc=mr+dr,mc+dc
            if 0<=nr<h and 0<=nc<w:
                out[nr][nc]=6
    return out

def rule_h18(g):
    h,w=size(g); out=blank(h,w)
    # preserve original 4 component
    for r in range(h):
        for c in range(w):
            if g[r][c]==4:
                out[r][c]=4
    src=[(r,c) for r in range(h) for c in range(w) if g[r][c]==2][0]
    dst=[(r,c) for r in range(h) for c in range(w) if g[r][c]==3][0]
    dr,dc=dst[0]-src[0], dst[1]-src[1]
    for r in range(h):
        for c in range(w):
            if g[r][c]==4:
                nr,nc=r+dr,c+dc
                if 0<=nr<h and 0<=nc<w:
                    out[nr][nc]=8
    return out

def rule_h19(g):
    comps=[(val,cells) for val,cells in components(g) if val!=0]
    # ignore singleton markers? there are none
    comps_sorted=sorted(comps, key=lambda vc: (-len(vc[1]), vc[0]))
    total=sum(len(cells) for val,cells in comps_sorted)+max(0,len(comps_sorted)-1)
    out=blank(1,total)
    c=0
    for i,(val,cells) in enumerate(comps_sorted):
        for _ in range(len(cells)):
            out[0][c]=val
            c+=1
        if i!=len(comps_sorted)-1:
            c+=1
    return out

def rule_h20(g):
    h,w=size(g)
    legend=[v for v in g[0] if v!=0]
    parts=[]
    for color in legend:
        comps=[cells for val,cells in components(g, colors={color}) if all(r>0 for r,c in cells)]
        assert len(comps)==1
        cells=comps[0]
        crop=crop_bbox(g,cells)
        parts.append(crop)
    out_h=max(len(p) for p in parts)
    out_w=sum(len(p[0]) for p in parts)+len(parts)-1
    out=blank(out_h,out_w)
    x=0
    for i,p in enumerate(parts):
        ph,pw=size(p)
        for r in range(ph):
            for c in range(pw):
                out[r][x+c]=p[r][c]
        x += pw
        if i != len(parts)-1:
            x += 1
    return out

def rule_h21(g):
    h,w=size(g); out=clone(g)
    comps6=[cells for val,cells in components(g, colors={6})]
    template=max(comps6, key=len)
    tr0,tr1,tc0,tc1=bbox(template)
    th,tw=tr1-tr0+1,tc1-tc0+1
    rel={(r-tr0,c-tc0) for r,c in template}
    target=None
    for val,cells in components(g, colors={3}):
        r0,r1,c0,c1=bbox(cells)
        if is_solid_rect(cells) and (r1-r0+1, c1-c0+1)==(th,tw):
            target=(r0,r1,c0,c1,cells)
            break
    assert target is not None
    r0,r1,c0,c1,cells=target
    for r,c in cells:
        out[r][c]=0
    for dr,dc in rel:
        out[r0+dr][c0+dc]=8
    return out

SOLVERS = {
    "rule_e15": rule_e15,
    "rule_e16": rule_e16,
    "rule_e17": rule_e17,
    "rule_e18": rule_e18,
    "rule_e19": rule_e19,
    "rule_e20": rule_e20,
    "rule_e21": rule_e21,
    "rule_m15": rule_m15,
    "rule_m16": rule_m16,
    "rule_m17": rule_m17,
    "rule_m18": rule_m18,
    "rule_m19": rule_m19,
    "rule_m20": rule_m20,
    "rule_m21": rule_m21,
    "rule_h15": rule_h15,
    "rule_h16": rule_h16,
    "rule_h17": rule_h17,
    "rule_h18": rule_h18,
    "rule_h19": rule_h19,
    "rule_h20": rule_h20,
    "rule_h21": rule_h21,
}

PUZZLES: List[Dict[str, Any]] = [
    {
        "id": "E15",
        "title": 'Diagonal Halo',
        "difficulty": "easy",
        "skills": ['diagonal neighborhood', 'edge clipping', 'copy-preserve'],
        "staged_hint": 'First locate the 2-cells, then consider only their four diagonal neighbors.',
        "written_solution": 'Each 2 acts like a diagonal beacon. Keep the 2 itself, and paint each in-bounds diagonal neighbor with 6. Leave all other cells unchanged.',
        "program_name": "rule_e15",
        "program_source": 'def rule_e15(g):\n    h,w=size(g); out=clone(g)\n    for r in range(h):\n        for c in range(w):\n            if g[r][c]==2:\n                for dr,dc in [(-1,-1),(-1,1),(1,-1),(1,1)]:\n                    nr,nc=r+dr,c+dc\n                    if 0<=nr<h and 0<=nc<w and out[nr][nc]==0:\n                        out[nr][nc]=6\n    return out',
        "train": [
            {
                "input": ['000000', '020000', '000000', '000020', '000000', '200000'],
                "output": ['606000', '020000', '606606', '000020', '060606', '200000'],
            },
            {
                "input": ['0000000', '0002000', '0000000', '2000000', '0000020', '0000000', '0000000'],
                "output": ['0060600', '0002000', '0660600', '2000606', '0600020', '0000606', '0000000'],
            },
            {
                "input": ['00000000', '00000000', '00200020', '00000000', '00000000', '00000000', '00002000', '00000000'],
                "output": ['00000000', '06060606', '00200020', '06060606', '00000000', '00060600', '00002000', '00060600'],
            },
        ],
        "test": {
            "input": ['000000000', '000000020', '000000000', '000000000', '020000000', '000000000', '000000200', '000000000', '000000000'],
            "output": ['000000606', '000000020', '000000606', '606000000', '020000000', '606006060', '000000200', '000006060', '000000000'],
        },
    },
    {
        "id": "E16",
        "title": 'X-Center Fill',
        "difficulty": "easy",
        "skills": ['diagonal pattern detection', 'same-size recolor', 'local motifs'],
        "staged_hint": 'Ignore the outer 1s at first. Ask which empty cell sits exactly in the middle of an X made of four diagonal 1s.',
        "written_solution": 'Whenever a 0 cell has 1s on all four diagonal neighbors, change that center cell to 8. Everything else stays as it was.',
        "program_name": "rule_e16",
        "program_source": 'def rule_e16(g):\n    h,w=size(g); out=clone(g)\n    for r in range(1,h-1):\n        for c in range(1,w-1):\n            if g[r][c]==0 and g[r-1][c-1]==1 and g[r-1][c+1]==1 and g[r+1][c-1]==1 and g[r+1][c+1]==1:\n                out[r][c]=8\n    return out',
        "train": [
            {
                "input": ['0000000', '0101000', '0000000', '0101101', '0000000', '0000101', '0000000'],
                "output": ['0000000', '0101000', '0080000', '0101101', '0000080', '0000101', '0000000'],
            },
            {
                "input": ['00000000', '00001010', '00000000', '00001010', '01010000', '00000000', '01010000', '00000000'],
                "output": ['00000000', '00001010', '00000800', '00001010', '01010000', '00800000', '01010000', '00000000'],
            },
            {
                "input": ['000000000', '000000000', '001010101', '000000000', '001010101', '000010100', '000000000', '000010100', '000000000'],
                "output": ['000000000', '000000000', '001010101', '000808080', '001010101', '000010100', '000008000', '000010100', '000000000'],
            },
        ],
        "test": {
            "input": ['0000000000', '0101000000', '0000000000', '0101000000', '0000010100', '0000000000', '0010110100', '0000000000', '0010100000'],
            "output": ['0000000000', '0101000000', '0080000000', '0101000000', '0000010100', '0000008000', '0010110100', '0008000000', '0010100000'],
        },
    },
    {
        "id": "E17",
        "title": 'Horizontal Sandwich',
        "difficulty": "easy",
        "skills": ['rowwise local rule', 'flanking cells', 'pattern completion'],
        "staged_hint": 'Work row by row. Only look for 5-0-5 triples and ignore every other arrangement.',
        "written_solution": 'If a cell is 0 and its immediate left and right neighbors are both 5, recolor that middle cell to 3. Keep the two 5s and everything else unchanged.',
        "program_name": "rule_e17",
        "program_source": 'def rule_e17(g):\n    h,w=size(g); out=clone(g)\n    for r in range(h):\n        for c in range(1,w-1):\n            if g[r][c]==0 and g[r][c-1]==5 and g[r][c+1]==5:\n                out[r][c]=3\n    return out',
        "train": [
            {
                "input": ['00000000', '05050000', '00000000', '00000000', '00005050', '00000000'],
                "output": ['00000000', '05350000', '00000000', '00000000', '00005350', '00000000'],
            },
            {
                "input": ['000000000', '000000000', '505005050', '000000000', '000000000', '000505000', '000000000'],
                "output": ['000000000', '000000000', '535005350', '000000000', '000000000', '000535000', '000000000'],
            },
            {
                "input": ['0000000000', '0000005050', '0000000000', '0050500000', '0000000000', '0000000000', '5050000000', '0000000000'],
                "output": ['0000000000', '0000005350', '0000000000', '0053500000', '0000000000', '0000000000', '5350000000', '0000000000'],
            },
        ],
        "test": {
            "input": ['0000000000', '0005050000', '0000000000', '0000000000', '0505000000', '0000000000', '0000000000', '0000005050', '0000000000'],
            "output": ['0000000000', '0005350000', '0000000000', '0000000000', '0535000000', '0000000000', '0000000000', '0000005350', '0000000000'],
        },
    },
    {
        "id": "E18",
        "title": 'Vertical Sandwich',
        "difficulty": "easy",
        "skills": ['columnwise local rule', 'flanking cells', 'pattern completion'],
        "staged_hint": 'Work column by column. Only cells with a 7 directly above and below can change.',
        "written_solution": 'If a cell is 0 and the cells immediately above and below it are both 7, recolor that middle cell to 4. Leave all other cells alone.',
        "program_name": "rule_e18",
        "program_source": 'def rule_e18(g):\n    h,w=size(g); out=clone(g)\n    for r in range(1,h-1):\n        for c in range(w):\n            if g[r][c]==0 and g[r-1][c]==7 and g[r+1][c]==7:\n                out[r][c]=4\n    return out',
        "train": [
            {
                "input": ['000000', '070000', '000000', '070070', '000000', '000070', '000000'],
                "output": ['000000', '070000', '040000', '070070', '000040', '000070', '000000'],
            },
            {
                "input": ['00000070', '00000000', '00000070', '00000000', '00700000', '00000000', '00700000', '00000000'],
                "output": ['00000070', '00000040', '00000070', '00000000', '00700000', '00400000', '00700000', '00000000'],
            },
            {
                "input": ['000000000', '000000000', '000700000', '000000000', '000700000', '000000070', '000000000', '000000070', '000000000'],
                "output": ['000000000', '000000000', '000700000', '000400000', '000700000', '000000070', '000000040', '000000070', '000000000'],
            },
        ],
        "test": {
            "input": ['000000000', '000070000', '000000000', '000070000', '070000000', '000000000', '070000070', '000000000', '000000070', '000000000'],
            "output": ['000000000', '000070000', '000040000', '000070000', '070000000', '040000000', '070000070', '000000040', '000000070', '000000000'],
        },
    },
    {
        "id": "E19",
        "title": 'Diagonal Square Completion',
        "difficulty": "easy",
        "skills": ['2x2 reasoning', 'diagonal relations', 'local completion'],
        "staged_hint": 'Look only at 2x2 windows. Ask whether two opposite corners already contain 8 and the other two are empty.',
        "written_solution": 'In any 2x2 block where the two 8s occupy one diagonal and the other diagonal is empty, fill the two empty cells with 1. Leave the 8s as they are.',
        "program_name": "rule_e19",
        "program_source": 'def rule_e19(g):\n    h,w=size(g); out=clone(g)\n    for r in range(h-1):\n        for c in range(w-1):\n            block=[g[r][c],g[r][c+1],g[r+1][c],g[r+1][c+1]]\n            if block[0]==8 and block[3]==8 and block[1]==0 and block[2]==0:\n                out[r][c+1]=1; out[r+1][c]=1\n            if block[1]==8 and block[2]==8 and block[0]==0 and block[3]==0:\n                out[r][c]=1; out[r+1][c+1]=1\n    return out',
        "train": [
            {
                "input": ['000000', '080000', '008000', '000008', '000080', '000000'],
                "output": ['000000', '081000', '018000', '000018', '000081', '000000'],
            },
            {
                "input": ['0008000', '0080000', '0000000', '0000080', '0800008', '0080000', '0000000'],
                "output": ['0018000', '0081000', '0000000', '0000081', '0810018', '0180000', '0000000'],
            },
            {
                "input": ['00000000', '00000800', '00000080', '00000000', '00080000', '00800000', '08000000', '80000000'],
                "output": ['00000000', '00000810', '00000180', '00000000', '00180000', '01810000', '18100000', '81000000'],
            },
        ],
        "test": {
            "input": ['000000000', '008000000', '080000800', '000000080', '000000000', '000800000', '000080000', '000000000'],
            "output": ['000000000', '018000000', '081000810', '000000180', '000000000', '000810000', '000180000', '000000000'],
        },
    },
    {
        "id": "E20",
        "title": 'Horizontal Bar Caps',
        "difficulty": "easy",
        "skills": ['adjacent-pair detection', 'rowwise extension', 'edge clipping'],
        "staged_hint": 'Find the horizontal 4-4 dominos first. Then add only the immediate zero cells just outside those dominos.',
        "written_solution": 'Each horizontal 4-4 bar gets capped with 9 on its immediate left and right whenever those cells exist and are 0. The original 4s stay in place.',
        "program_name": "rule_e20",
        "program_source": 'def rule_e20(g):\n    h,w=size(g); out=clone(g)\n    for r in range(h):\n        for c in range(w-1):\n            if g[r][c]==4 and g[r][c+1]==4:\n                if c-1 >= 0 and g[r][c-1]==0:\n                    out[r][c-1]=9\n                if c+2 < w and g[r][c+2]==0:\n                    out[r][c+2]=9\n    return out',
        "train": [
            {
                "input": ['00000000', '04400000', '00000000', '00000000', '00004400', '00000000'],
                "output": ['00000000', '94490000', '00000000', '00000000', '00094490', '00000000'],
            },
            {
                "input": ['000000000', '000000000', '000440000', '000000000', '000000000', '440000000', '000000000'],
                "output": ['000000000', '000000000', '009449000', '000000000', '000000000', '449000000', '000000000'],
            },
            {
                "input": ['0000000000', '0000004400', '0000000000', '0440000000', '0000000000', '0000000000', '0000440000', '0000000000'],
                "output": ['0000000000', '0000094490', '0000000000', '9449000000', '0000000000', '0000000000', '0009449000', '0000000000'],
            },
        ],
        "test": {
            "input": ['0000000000', '0044000000', '0000000000', '0000000000', '0000004400', '0000000000', '0000000000', '4400000000', '0000000000'],
            "output": ['0000000000', '0944900000', '0000000000', '0000000000', '0000094490', '0000000000', '0000000000', '4490000000', '0000000000'],
        },
    },
    {
        "id": "E21",
        "title": 'Marker Takes the Row Color',
        "difficulty": "easy",
        "skills": ['row aggregation', 'marker replacement', 'single-color rows'],
        "staged_hint": 'Treat each row separately. First identify the unique nonzero color in that row, then use it to replace the 9 marker.',
        "written_solution": 'If a row contains exactly one distinct nonzero color besides 9, replace every 9 in that row with that color. Rows that do not meet that condition stay unchanged.',
        "program_name": "rule_e21",
        "program_source": 'def rule_e21(g):\n    h,w=size(g); out=clone(g)\n    for r in range(h):\n        colors={v for v in g[r] if v not in (0,9)}\n        has9=any(v==9 for v in g[r])\n        if len(colors)==1 and has9:\n            color=next(iter(colors))\n            for c in range(w):\n                if g[r][c]==9:\n                    out[r][c]=color\n    return out',
        "train": [
            {
                "input": ['00000000', '03300090', '00000000', '00000000', '50009000', '00000000'],
                "output": ['00000000', '03300030', '00000000', '00000000', '50005000', '00000000'],
            },
            {
                "input": ['000000000', '000000000', '900700000', '000000000', '000000000', '009000220', '000000000'],
                "output": ['000000000', '000000000', '700700000', '000000000', '000000000', '002000220', '000000000'],
            },
            {
                "input": ['0000000000', '0444000090', '0000000000', '6000090000', '0000000000', '0000000000', '0900000800', '0000000000'],
                "output": ['0000000000', '0444000040', '0000000000', '6000060000', '0000000000', '0000000000', '0800000800', '0000000000'],
            },
        ],
        "test": {
            "input": ['0000000000', '0022000090', '0000000000', '0000000000', '0900060000', '0000000000', '0000000000', '0000009440', '0000000000'],
            "output": ['0000000000', '0022000020', '0000000000', '0000000000', '0600060000', '0000000000', '0000000000', '0000004440', '0000000000'],
        },
    },
    {
        "id": "M15",
        "title": 'Crop the Marked Component',
        "difficulty": "medium",
        "skills": ['component detection', 'marker-object association', 'bbox crop'],
        "staged_hint": 'First find which 3-object touches the 2 marker. Only after that should you crop anything.',
        "written_solution": 'Among all 3-colored components, choose the one that is orthogonally adjacent to the 2 marker. Output the bounding-box crop of that component alone.',
        "program_name": "rule_m15",
        "program_source": 'def rule_m15(g):\n    h,w=size(g)\n    marker_cells=[(r,c) for r in range(h) for c in range(w) if g[r][c]==2]\n    comps=[cells for val,cells in components(g, colors={3})]\n    marker_set=set(marker_cells)\n    chosen=None\n    for cells in comps:\n        s=set(cells)\n        for r,c in cells:\n            for nr,nc in orth_neighbors(r,c,h,w):\n                if (nr,nc) in marker_set:\n                    chosen=cells\n                    break\n            if chosen is not None:\n                break\n        if chosen is not None:\n            break\n    assert chosen is not None\n    r0,r1,c0,c1=bbox(chosen)\n    out=blank(r1-r0+1,c1-c0+1)\n    for r,c in chosen:\n        out[r-r0][c-c0]=3\n    return out',
        "train": [
            {
                "input": ['0000000000', '0300000000', '0300000030', '0330000333', '0000000000', '0000023300', '0000000330', '0000000000', '0000000000', '0000000000'],
                "output": ['330', '033'],
            },
            {
                "input": ['00000000000', '00000030000', '00000333000', '00000000000', '00000000000', '00000000000', '23030000000', '03330000300', '00000000300', '00000000330', '00000000000'],
                "output": ['303', '333'],
            },
            {
                "input": ['000000000000', '000000000200', '000000000300', '003300003330', '000330000000', '000000000000', '000000000000', '000000000000', '000000030000', '000000030000', '000000033000', '000000000000'],
                "output": ['030', '333'],
            },
        ],
        "test": {
            "input": ['0000000000000', '0000000000000', '0003000000000', '0033300000000', '0000000000000', '0000000003300', '0000000000330', '2303000000000', '0333000000000', '0000000000000', '0000000000000', '0000000000000'],
            "output": ['303', '333'],
        },
    },
    {
        "id": "M16",
        "title": 'Frame Border Recolor from Seed',
        "difficulty": "medium",
        "skills": ['frame detection', 'inside/outside reasoning', 'color transfer'],
        "staged_hint": 'Find each rectangular 1-frame first. Then read the single seed color inside it and copy that color to the whole border.',
        "written_solution": 'Every 1-colored rectangular frame contains one nonzero seed color in its interior. Recolor the entire border of that frame to the seed color, while leaving the interior seed and zeros unchanged.',
        "program_name": "rule_m16",
        "program_source": 'def rule_m16(g):\n    h,w=size(g); out=clone(g)\n    frames=[cells for val,cells in components(g, colors={1}) if is_rect_frame(cells)]\n    for cells in frames:\n        r0,r1,c0,c1=bbox(cells)\n        interior_colors={g[r][c] for r in range(r0+1,r1) for c in range(c0+1,c1) if g[r][c] not in (0,1)}\n        if len(interior_colors)==1:\n            color=next(iter(interior_colors))\n            for r,c in cells:\n                out[r][c]=color\n    return out',
        "train": [
            {
                "input": ['000000000000', '011111000000', '010401000000', '010001000000', '011111000000', '000000011110', '000000016010', '000000010010', '000000011110', '000000000000'],
                "output": ['000000000000', '044444000000', '040404000000', '040004000000', '044444000000', '000000066660', '000000066060', '000000060060', '000000066660', '000000000000'],
            },
            {
                "input": ['00000000111', '00000000121', '00111111101', '00100001111', '00100801000', '00100001000', '00111111000', '00000000000', '00000000000', '00000000000', '00000000000'],
                "output": ['00000000111', '00000000121', '00111111101', '00100001111', '00100801000', '00100001000', '00111111000', '00000000000', '00000000000', '00000000000', '00000000000'],
            },
            {
                "input": ['000000000000', '011110000000', '013010001110', '010010001510', '011110001010', '000000001110', '001111110000', '001000010000', '001007010000', '001000010000', '001111110000', '000000000000'],
                "output": ['000000000000', '033330000000', '033030005550', '030030005550', '033330005050', '000000005550', '007777770000', '007000070000', '007007070000', '007000070000', '007777770000', '000000000000'],
            },
        ],
        "test": {
            "input": ['0000000000000', '0011111000000', '0010001000000', '0010601000000', '0010001000000', '0011111000000', '0000000111110', '0111100104010', '0180100100010', '0111100111110', '0000000000000', '0000000000000'],
            "output": ['0000000000000', '0066666000000', '0060006000000', '0060606000000', '0060006000000', '0066666000000', '0000000444440', '0888800404040', '0880800400040', '0888800444440', '0000000000000', '0000000000000'],
        },
    },
    {
        "id": "M17",
        "title": 'Horizontal Mirror Inside the Frame',
        "difficulty": "medium",
        "skills": ['frame-local symmetry', 'horizontal reflection', 'object augmentation'],
        "staged_hint": "Ignore the border once you have found it. Focus on where each 4 would land if reflected across the frame's horizontal axis.",
        "written_solution": "Inside each rectangular 1-frame, every 4-cell gets a mirrored partner across the frame's horizontal axis. Add that partner as 7 if the mirrored spot is empty; keep the original 4s and the frame.",
        "program_name": "rule_m17",
        "program_source": 'def rule_m17(g):\n    h,w=size(g); out=clone(g)\n    frames=[cells for val,cells in components(g, colors={1}) if is_rect_frame(cells)]\n    for cells in frames:\n        r0,r1,c0,c1=bbox(cells)\n        for r in range(r0+1,r1):\n            for c in range(c0+1,c1):\n                if g[r][c]==4:\n                    mr = r0 + r1 - r\n                    if out[mr][c]==0:\n                        out[mr][c]=7\n    return out',
        "train": [
            {
                "input": ['0000000000', '0111111110', '0104000010', '0100040010', '0100000010', '0100000010', '0100000010', '0100000010', '0111111110', '0000000000'],
                "output": ['0000000000', '0111111110', '0104000010', '0100040010', '0100000010', '0100000010', '0100070010', '0107000010', '0111111110', '0000000000'],
            },
            {
                "input": ['000000000000', '000000000000', '001111111100', '001040000100', '001000040100', '001000000100', '001000000100', '001004000100', '001111111100', '000000000000', '000000000000'],
                "output": ['000000000000', '000000000000', '001111111100', '001047000100', '001000040100', '001000000100', '001000070100', '001074000100', '001111111100', '000000000000', '000000000000'],
            },
            {
                "input": ['00000000000', '00011111100', '00014000100', '00010000100', '00010000100', '00010040100', '00010000100', '00010000100', '00010004100', '00010000100', '00011111100', '00000000000'],
                "output": ['00000000000', '00011111100', '00014000100', '00010007100', '00010000100', '00010040100', '00010070100', '00010000100', '00010004100', '00017000100', '00011111100', '00000000000'],
            },
        ],
        "test": {
            "input": ['000000000000', '011111111110', '014000000010', '010000040010', '010000000010', '010000000010', '010000000010', '010000000010', '010004000010', '010000000010', '011111111110', '000000000000'],
            "output": ['000000000000', '011111111110', '014000000010', '010007040010', '010000000010', '010000000010', '010000000010', '010000000010', '010004070010', '017000000010', '011111111110', '000000000000'],
        },
    },
    {
        "id": "M18",
        "title": 'Outer Corner Markers',
        "difficulty": "medium",
        "skills": ['solid-rectangle detection', 'bounding boxes', 'edge clipping'],
        "staged_hint": 'Find each solid 6-rectangle, then step one cell outward from each bbox corner.',
        "written_solution": 'For every solid rectangular 6-object, place a 2 one cell outside each of its four bounding-box corners whenever that outside cell lies inside the grid. Keep the rectangles themselves unchanged.',
        "program_name": "rule_m18",
        "program_source": 'def rule_m18(g):\n    h,w=size(g); out=clone(g)\n    for val,cells in components(g, colors={6}):\n        if not is_solid_rect(cells):\n            continue\n        r0,r1,c0,c1=bbox(cells)\n        for rr,cc in [(r0-1,c0-1),(r0-1,c1+1),(r1+1,c0-1),(r1+1,c1+1)]:\n            if 0<=rr<h and 0<=cc<w and out[rr][cc]==0:\n                out[rr][cc]=2\n    return out',
        "train": [
            {
                "input": ['0000000000', '0666000000', '0666000000', '0000000000', '0000000000', '0000006600', '0000006600', '0000006600', '0000000000', '0000000000'],
                "output": ['2000200000', '0666000000', '0666000000', '2000200000', '0000020020', '0000006600', '0000006600', '0000006600', '0000020020', '0000000000'],
            },
            {
                "input": ['000066000000', '000066000000', '000000000000', '000000000000', '066660000000', '066660000000', '066660000000', '000000000660', '000000000660'],
                "output": ['000066000000', '000066000000', '000200200000', '200002000000', '066660000000', '066660000000', '066660002002', '200002000660', '000000000660'],
            },
            {
                "input": ['00000000000', '00000000660', '00666000660', '00666000660', '00666000000', '00666000000', '00000000000', '00000000000', '00006666000', '00006666000', '00000000000'],
                "output": ['00000002002', '02000200660', '00666000660', '00666000660', '00666002002', '00666000000', '02000200000', '00020000200', '00006666000', '00006666000', '00020000200'],
            },
        ],
        "test": {
            "input": ['000000000000', '066600000000', '066600000000', '066600000000', '000000000000', '000000066000', '000000066000', '000000066000', '000000066000', '006666600000', '006666600000', '000000000000'],
            "output": ['200020000000', '066600000000', '066600000000', '066600000000', '200020200200', '000000066000', '000000066000', '000000066000', '020000066000', '006666600200', '006666600000', '020000020000'],
        },
    },
    {
        "id": "M19",
        "title": 'Recolor by Size Rank',
        "difficulty": "medium",
        "skills": ['component sizing', 'sorting', 'shape preservation'],
        "staged_hint": 'Do not change shapes. Only compare component sizes and assign the three output colors by rank.',
        "written_solution": "There are exactly three 8-colored components. Recolor the smallest one to 2, the middle-sized one to 3, and the largest one to 4, preserving every component's shape and position.",
        "program_name": "rule_m19",
        "program_source": 'def rule_m19(g):\n    h,w=size(g); out=blank(h,w)\n    comps=[cells for val,cells in components(g, colors={8})]\n    comps_sorted=sorted(comps, key=lambda cells: len(cells))\n    recolors=[2,3,4]\n    assert len(comps_sorted)==3\n    for color,cells in zip(recolors, comps_sorted):\n        for r,c in cells:\n            out[r][c]=color\n    return out',
        "train": [
            {
                "input": ['0000000000', '0880000000', '0000000000', '0000000000', '0880000000', '0880000000', '0000008880', '0000008880', '0000000000', '0000000000'],
                "output": ['0000000000', '0220000000', '0000000000', '0000000000', '0330000000', '0330000000', '0000004440', '0000004440', '0000000000', '0000000000'],
            },
            {
                "input": ['00000000000', '00000008880', '00000000000', '00000000000', '00000000000', '08800000000', '08800000000', '08000000000', '00008880000', '00008880000', '00000000000'],
                "output": ['00000000000', '00000002220', '00000000000', '00000000000', '00000000000', '03300000000', '03300000000', '03000000000', '00004440000', '00004440000', '00000000000'],
            },
            {
                "input": ['000000000000', '000000000000', '000000000880', '000000000000', '000000000000', '000000000000', '080800000000', '088800000000', '000000088800', '000000088800', '000000000000', '000000000000'],
                "output": ['000000000000', '000000000000', '000000000220', '000000000000', '000000000000', '000000000000', '030300000000', '033300000000', '000000044400', '000000044400', '000000000000', '000000000000'],
            },
        ],
        "test": {
            "input": ['0000000000000', '0888000000000', '0000000000000', '0000000000000', '0000000000000', '0000000088000', '0000000088000', '0000000000000', '0088800000000', '0088800000000', '0000000000000', '0000000000000'],
            "output": ['0000000000000', '0222000000000', '0000000000000', '0000000000000', '0000000000000', '0000000033000', '0000000033000', '0000000000000', '0044400000000', '0044400000000', '0000000000000', '0000000000000'],
        },
    },
    {
        "id": "M20",
        "title": 'Legend-Selected Crop',
        "difficulty": "medium",
        "skills": ['legend decoding', 'component selection', 'bbox crop'],
        "staged_hint": 'Read the single nonzero legend color in the top row before looking at any lower objects.',
        "written_solution": 'The top row contains one nonzero legend color. Among the components below, select the component of that color and output its bounding-box crop.',
        "program_name": "rule_m20",
        "program_source": 'def rule_m20(g):\n    h,w=size(g)\n    legend_colors=[v for v in g[0] if v!=0]\n    assert len(legend_colors)==1\n    target=legend_colors[0]\n    candidates=[]\n    for val,cells in components(g):\n        if val==target and all(r>0 for r,c in cells):\n            candidates.append(cells)\n    assert len(candidates)>=1\n    chosen=sorted(candidates, key=lambda cells: (bbox(cells)[0], bbox(cells)[2]))[0]\n    return crop_bbox(g, chosen)',
        "train": [
            {
                "input": ['0004000000', '0000000000', '0300000660', '0300000660', '0330000000', '0000000400', '0000004440', '0000000000', '0000000000', '0000000000'],
                "output": ['040', '444'],
            },
            {
                "input": ['00000600000', '00000000000', '00000000000', '02020000000', '02220000440', '00000000440', '00000066000', '00000006600', '00000000000', '00000000000', '00000000000'],
                "output": ['660', '066'],
            },
            {
                "input": ['000000000300', '000000000000', '000000050000', '000000555000', '000000000000', '003300000000', '003300000000', '003000000000', '000000007700', '000000000770', '000000000000', '000000000000'],
                "output": ['33', '33', '30'],
            },
        ],
        "test": {
            "input": ['0000700000000', '0000000000000', '0000000002200', '0400000000220', '0400000000000', '0440000000000', '0000000707000', '0000000777000', '0000000000000', '0000000000000', '0000000000000', '0000000000000'],
            "output": ['707', '777'],
        },
    },
    {
        "id": "M21",
        "title": 'Translate the Component to the Marker',
        "difficulty": "medium",
        "skills": ['component translation', 'bbox anchoring', 'same-size output'],
        "staged_hint": "Find the top-left corner of the 5-object's bounding box. The marker tells you where that corner should move.",
        "written_solution": 'Take the single 5-colored component and translate it so that the top-left corner of its bounding box lands exactly on the 2 marker. Output only the translated component on a blank grid of the same size.',
        "program_name": "rule_m21",
        "program_source": 'def rule_m21(g):\n    h,w=size(g)\n    comps=[cells for val,cells in components(g, colors={5})]\n    assert len(comps)==1\n    cells=comps[0]\n    marker=[(r,c) for r in range(h) for c in range(w) if g[r][c]==2]\n    assert len(marker)==1\n    mr,mc=marker[0]\n    r0,r1,c0,c1=bbox(cells)\n    dr,dc=mr-r0, mc-c0\n    out=blank(h,w)\n    for r,c in cells:\n        nr,nc=r+dr,c+dc\n        assert 0<=nr<h and 0<=nc<w\n        out[nr][nc]=5\n    return out',
        "train": [
            {
                "input": ['0000000000', '0000000000', '0050000000', '0050000000', '0055000000', '0000000000', '0000020000', '0000000000', '0000000000', '0000000000'],
                "output": ['0000000000', '0000000000', '0000000000', '0000000000', '0000000000', '0000000000', '0000050000', '0000050000', '0000055000', '0000000000'],
            },
            {
                "input": ['00000000000', '02000000000', '00000000000', '00000000000', '00000000000', '00000055000', '00000005500', '00000000000', '00000000000', '00000000000', '00000000000'],
                "output": ['00000000000', '05500000000', '00550000000', '00000000000', '00000000000', '00000000000', '00000000000', '00000000000', '00000000000', '00000000000', '00000000000'],
            },
            {
                "input": ['000000000000', '000000000000', '000000000000', '000000005000', '000000055500', '000000000000', '000000000000', '000000000000', '002000000000', '000000000000', '000000000000', '000000000000'],
                "output": ['000000000000', '000000000000', '000000000000', '000000000000', '000000000000', '000000000000', '000000000000', '000000000000', '000500000000', '005550000000', '000000000000', '000000000000'],
            },
        ],
        "test": {
            "input": ['0000000000000', '0000000000000', '0200000000000', '0000000000000', '0000000000000', '0000000000000', '0000000050500', '0000000055500', '0000000000000', '0000000000000', '0000000000000', '0000000000000'],
            "output": ['0000000000000', '0000000000000', '0505000000000', '0555000000000', '0000000000000', '0000000000000', '0000000000000', '0000000000000', '0000000000000', '0000000000000', '0000000000000', '0000000000000'],
        },
    },
    {
        "id": "H15",
        "title": 'Axis-Chosen Reflection',
        "difficulty": "hard",
        "skills": ['conditional axis choice', 'reflection', 'same-size synthesis'],
        "staged_hint": 'Find whether the 2 marker sits on the top edge or the left edge. That decides whether the mirror axis is vertical or horizontal.',
        "written_solution": 'If the 2 marker is in the top row, its column is a vertical mirror axis. If the 2 marker is in the left column, its row is a horizontal mirror axis. Keep the original 5-object, and add its reflected copy in color 7 across that axis.',
        "program_name": "rule_h15",
        "program_source": 'def rule_h15(g):\n    h,w=size(g); out=clone(g)\n    top_markers=[c for c,v in enumerate(g[0]) if v==2]\n    left_markers=[r for r in range(h) if g[r][0]==2]\n    if top_markers:\n        axis_c=top_markers[0]\n        for r in range(h):\n            for c in range(w):\n                if g[r][c]==5:\n                    mc=2*axis_c - c\n                    if 0<=mc<w and out[r][mc]==0:\n                        out[r][mc]=7\n    else:\n        axis_r=left_markers[0]\n        for r in range(h):\n            for c in range(w):\n                if g[r][c]==5:\n                    mr=2*axis_r - r\n                    if 0<=mr<h and out[mr][c]==0:\n                        out[mr][c]=7\n    return out',
        "train": [
            {
                "input": ['00000200000', '00000000000', '00000000000', '05000000000', '05000000000', '05500000000', '00000000000', '00000000000', '00000000000', '00000000000', '00000000000'],
                "output": ['00000200000', '00000000000', '00000000000', '05000000070', '05000000070', '05500000770', '00000000000', '00000000000', '00000000000', '00000000000', '00000000000'],
            },
            {
                "input": ['000000000000', '000000000000', '000000000000', '000000000000', '200000000000', '000000000000', '000005500000', '000000550000', '000000000000', '000000000000'],
                "output": ['000000000000', '000000770000', '000007700000', '000000000000', '200000000000', '000000000000', '000005500000', '000000550000', '000000000000', '000000000000'],
            },
            {
                "input": ['0000200000', '0000000000', '0000000000', '0000000000', '0000000500', '0000005550', '0000000000', '0000000000', '0000000000', '0000000000', '0000000000', '0000000000'],
                "output": ['0000200000', '0000000000', '0000000000', '0000000000', '0700000500', '7770005550', '0000000000', '0000000000', '0000000000', '0000000000', '0000000000', '0000000000'],
            },
            {
                "input": ['00000000000', '00000000000', '00000505000', '00000555000', '00000000000', '00000000000', '20000000000', '00000000000', '00000000000', '00000000000', '00000000000'],
                "output": ['00000000000', '00000000000', '00000505000', '00000555000', '00000000000', '00000000000', '20000000000', '00000000000', '00000000000', '00000777000', '00000707000'],
            },
        ],
        "test": {
            "input": ['000000200000', '000000000000', '000000000000', '000000000000', '005500000000', '005500000000', '005000000000', '000000000000', '000000000000', '000000000000', '000000000000', '000000000000'],
            "output": ['000000200000', '000000000000', '000000000000', '000000000000', '005500000770', '005500000770', '005000000070', '000000000000', '000000000000', '000000000000', '000000000000', '000000000000'],
        },
    },
    {
        "id": "H16",
        "title": 'Nested Frame Depth Fill',
        "difficulty": "hard",
        "skills": ['nested objects', 'depth counting', 'region filling'],
        "staged_hint": 'Treat the 1-borders as frames, not as filled rectangles. Then count how many frames strictly contain each empty cell.',
        "written_solution": 'Every empty cell inside at least one rectangular 1-frame is recolored by its nesting depth: cells inside one frame become 2, cells inside two nested frames become 3, inside three become 4, and so on. The 1-borders remain unchanged.',
        "program_name": "rule_h16",
        "program_source": 'def rule_h16(g):\n    h,w=size(g); out=clone(g)\n    frames=[bbox(cells) for val,cells in components(g, colors={1}) if is_rect_frame(cells)]\n    for r in range(h):\n        for c in range(w):\n            if g[r][c]==0:\n                depth=sum(1 for r0,r1,c0,c1 in frames if r0<r<r1 and c0<c<c1)\n                if depth>0:\n                    out[r][c]=depth+1\n    return out',
        "train": [
            {
                "input": ['000000000', '011111110', '010000010', '010111010', '010101010', '010111010', '010000010', '011111110', '000000000'],
                "output": ['000000000', '011111110', '012222210', '012111210', '012131210', '012111210', '012222210', '011111110', '000000000'],
            },
            {
                "input": ['00000000000', '00000000000', '00111111100', '00100000100', '00100000100', '00100000100', '00100000100', '00100000100', '00111111100', '00000000000', '00000000000'],
                "output": ['00000000000', '00000000000', '00111111100', '00122222100', '00122222100', '00122222100', '00122222100', '00122222100', '00111111100', '00000000000', '00000000000'],
            },
            {
                "input": ['0000000000000', '0111111111110', '0100000000010', '0101111111010', '0101000001010', '0101011101010', '0101010101010', '0101011101010', '0101000001010', '0101111111010', '0100000000010', '0111111111110', '0000000000000'],
                "output": ['0000000000000', '0111111111110', '0122222222210', '0121111111210', '0121333331210', '0121311131210', '0121314131210', '0121311131210', '0121333331210', '0121111111210', '0122222222210', '0111111111110', '0000000000000'],
            },
            {
                "input": ['00000000000', '00111111100', '00100000100', '00101110100', '00101010100', '00101010100', '00101010100', '00101010100', '00101110100', '00100000100', '00111111100', '00000000000'],
                "output": ['00000000000', '00111111100', '00122222100', '00121112100', '00121312100', '00121312100', '00121312100', '00121312100', '00121112100', '00122222100', '00111111100', '00000000000'],
            },
        ],
        "test": {
            "input": ['000000000000', '011111111110', '010000000010', '010111111010', '010100001010', '010101111010', '010101001010', '010101111010', '010100001010', '010111111010', '010000000010', '011111111110', '000000000000'],
            "output": ['000000000000', '011111111110', '012222222210', '012111111210', '012122221210', '012121111210', '012121221210', '012121111210', '012122221210', '012111111210', '012222222210', '011111111110', '000000000000'],
        },
    },
    {
        "id": "H17",
        "title": 'Template Stamping from Markers',
        "difficulty": "hard",
        "skills": ['template extraction', 'repetition', 'translation'],
        "staged_hint": 'Find the single 6-template first and record it relative to its own top-left corner. Then stamp that same pattern at every 2 marker.',
        "written_solution": 'The non-singleton 6-object is a template. Ignore its absolute position, keep only its shape relative to its bounding box, and stamp that shape in color 6 with its top-left corner aligned to every 2 marker. Output only the stamped copies on a blank grid.',
        "program_name": "rule_h17",
        "program_source": 'def rule_h17(g):\n    h,w=size(g)\n    comps=[cells for val,cells in components(g, colors={6})]\n    # choose the non-singleton or largest component as template\n    template=max(comps, key=len)\n    r0,r1,c0,c1=bbox(template)\n    rel=[(r-r0,c-c0) for r,c in template]\n    markers=[(r,c) for r in range(h) for c in range(w) if g[r][c]==2]\n    out=blank(h,w)\n    for mr,mc in markers:\n        for dr,dc in rel:\n            nr,nc=mr+dr,mc+dc\n            if 0<=nr<h and 0<=nc<w:\n                out[nr][nc]=6\n    return out',
        "train": [
            {
                "input": ['000000000000', '066000000000', '006600000000', '000000000000', '000000000000', '000000020000', '000000000000', '002000000000', '000000000000', '000000000000'],
                "output": ['000000000000', '000000000000', '000000000000', '000000000000', '000000000000', '000000066000', '000000006600', '006600000000', '000660000000', '000000000000'],
            },
            {
                "input": ['00000000000', '00600000000', '00600000000', '00660000000', '00000000000', '00000200000', '00000000000', '00000000000', '02000000000', '00000000000', '00000000000'],
                "output": ['00000000000', '00000000000', '00000000000', '00000000000', '00000000000', '00000600000', '00000600000', '00000660000', '06000000000', '06000000000', '06600000000'],
            },
            {
                "input": ['000000000000', '000000000000', '006000000000', '066600002000', '000000000000', '000000000000', '000000020000', '000000000000', '000000000000', '000200000000', '000000000000', '000000000000'],
                "output": ['000000000000', '000000000000', '000000000000', '000000000600', '000000006660', '000000000000', '000000006000', '000000066600', '000000000000', '000060000000', '000666000000', '000000000000'],
            },
            {
                "input": ['0000000000000', '0606000000000', '0666000000000', '0000000000000', '0000000000000', '0000000002000', '0000000000000', '0000000000000', '0000200000000', '0000000000000', '0000000000000'],
                "output": ['0000000000000', '0000000000000', '0000000000000', '0000000000000', '0000000000000', '0000000006060', '0000000006660', '0000000000000', '0000606000000', '0000666000000', '0000000000000'],
            },
        ],
        "test": {
            "input": ['0000000000000', '0066000000000', '0066000000000', '0060000002000', '0000000000000', '0000000000000', '0000000020000', '0000000000000', '0200000000000', '0000000000000', '0000000000000', '0000000000000'],
            "output": ['0000000000000', '0000000000000', '0000000000000', '0000000006600', '0000000006600', '0000000006000', '0000000066000', '0000000066000', '0660000060000', '0660000000000', '0600000000000', '0000000000000'],
        },
    },
    {
        "id": "H18",
        "title": 'Vector Copy by Marker Pair',
        "difficulty": "hard",
        "skills": ['translation vectors', 'copying', 'same-size synthesis'],
        "staged_hint": 'Do not guess the destination from the object. First compute the vector from 2 to 3, then apply that vector to every 4-cell.',
        "written_solution": 'The vector from the 2 marker to the 3 marker tells you how far to copy the 4-object. Keep the original 4-object, remove the markers, and add a translated copy in color 8 at that offset.',
        "program_name": "rule_h18",
        "program_source": 'def rule_h18(g):\n    h,w=size(g); out=blank(h,w)\n    # preserve original 4 component\n    for r in range(h):\n        for c in range(w):\n            if g[r][c]==4:\n                out[r][c]=4\n    src=[(r,c) for r in range(h) for c in range(w) if g[r][c]==2][0]\n    dst=[(r,c) for r in range(h) for c in range(w) if g[r][c]==3][0]\n    dr,dc=dst[0]-src[0], dst[1]-src[1]\n    for r in range(h):\n        for c in range(w):\n            if g[r][c]==4:\n                nr,nc=r+dr,c+dc\n                if 0<=nr<h and 0<=nc<w:\n                    out[nr][nc]=8\n    return out',
        "train": [
            {
                "input": ['0000000000', '0200000000', '0040000000', '0040000000', '0044000000', '0000030000', '0000000000', '0000000000', '0000000000', '0000000000'],
                "output": ['0000000000', '0000000000', '0040000000', '0040000000', '0044000000', '0000000000', '0000008000', '0000008000', '0000008800', '0000000000'],
            },
            {
                "input": ['000000000000', '000000000000', '000000000000', '000000030000', '000000000000', '000000000000', '004400000000', '000440000000', '000000000000', '020000000000', '000000000000'],
                "output": ['000000008800', '000000000880', '000000000000', '000000000000', '000000000000', '000000000000', '004400000000', '000440000000', '000000000000', '000000000000', '000000000000'],
            },
            {
                "input": ['000000000000', '000000000000', '002000000000', '000000040000', '000000444000', '000000000000', '000000000000', '030000000000', '000000000000', '000000000000', '000000000000', '000000000000'],
                "output": ['000000000000', '000000000000', '000000000000', '000000040000', '000000444000', '000000000000', '000000000000', '000000000000', '000000800000', '000008880000', '000000000000', '000000000000'],
            },
            {
                "input": ['0000000000000', '0000000020000', '0000000000000', '0000000000000', '0000404000000', '0000444000000', '0000000000300', '0000000000000', '0000000000000', '0000000000000', '0000000000000', '0000000000000', '0000000000000'],
                "output": ['0000000000000', '0000000000000', '0000000000000', '0000000000000', '0000404000000', '0000444000000', '0000000000000', '0000000000000', '0000000000000', '0000008080000', '0000008880000', '0000000000000', '0000000000000'],
            },
        ],
        "test": {
            "input": ['0000000000000', '0200000000000', '0000000000000', '0000000000000', '0040000000000', '0044400000000', '0000400000000', '0000030000000', '0000000000000', '0000000000000', '0000000000000', '0000000000000'],
            "output": ['0000000000000', '0000000000000', '0000000000000', '0000000000000', '0040000000000', '0044400000000', '0000400000000', '0000000000000', '0000000000000', '0000000000000', '0000008000000', '0000008880000'],
        },
    },
    {
        "id": "H19",
        "title": 'Component Size Bars',
        "difficulty": "hard",
        "skills": ['component sizing', 'sorting', 'dynamic output size'],
        "staged_hint": 'Forget the original layout after measuring. The output is just the component sizes, written as colored bars from largest to smallest.',
        "written_solution": "Measure every nonzero component, sort the components from largest to smallest, and output a single row of solid bars whose lengths equal those sizes. Preserve each component's color and separate consecutive bars by one 0.",
        "program_name": "rule_h19",
        "program_source": 'def rule_h19(g):\n    comps=[(val,cells) for val,cells in components(g) if val!=0]\n    # ignore singleton markers? there are none\n    comps_sorted=sorted(comps, key=lambda vc: (-len(vc[1]), vc[0]))\n    total=sum(len(cells) for val,cells in comps_sorted)+max(0,len(comps_sorted)-1)\n    out=blank(1,total)\n    c=0\n    for i,(val,cells) in enumerate(comps_sorted):\n        for _ in range(len(cells)):\n            out[0][c]=val\n            c+=1\n        if i!=len(comps_sorted)-1:\n            c+=1\n    return out',
        "train": [
            {
                "input": ['0000000000', '0220000000', '0000000000', '0000000000', '0440000000', '0440000000', '0000006600', '0000006600', '0000006000', '0000000000'],
                "output": ['6666604444022'],
            },
            {
                "input": ['000000000000', '000000033300', '000000000000', '000000000000', '000000000000', '000000000000', '055500000000', '055500000000', '000000000000', '000000008800', '000000000000', '000000000000'],
                "output": ['5555550333088'],
            },
            {
                "input": ['0000000000000', '0110000000000', '0110000000000', '0000000000000', '0000000077000', '0000000077000', '0000000070000', '0000000000000', '0000440000000', '0000000000000'],
                "output": ['7777701111044'],
            },
            {
                "input": ['000000000000', '000000000000', '002220000000', '000000000000', '000000000000', '000000060000', '000000060000', '000000666000', '099000000000', '099000000000', '000000000000'],
                "output": ['66666099990222'],
            },
        ],
        "test": {
            "input": ['0000000000000', '0000000003300', '0000000000000', '0000000000000', '0000000000000', '0555000000000', '0555000000000', '0000000000000', '0000000880000', '0000000880000', '0000000800000', '0000000000000'],
            "output": ['555555088888033'],
        },
    },
    {
        "id": "H20",
        "title": 'Legend-Order Assembly',
        "difficulty": "hard",
        "skills": ['legend decoding', 'component cropping', 'ordered composition'],
        "staged_hint": 'Read the legend order in the top row first. Then crop each matching object and pack those crops side by side in that order.',
        "written_solution": 'The nonzero cells in the top row define an order of colors. For each listed color, find the matching component below, crop it to its bounding box, and assemble those crops left-to-right in legend order, separated by one blank column.',
        "program_name": "rule_h20",
        "program_source": 'def rule_h20(g):\n    h,w=size(g)\n    legend=[v for v in g[0] if v!=0]\n    parts=[]\n    for color in legend:\n        comps=[cells for val,cells in components(g, colors={color}) if all(r>0 for r,c in cells)]\n        assert len(comps)==1\n        cells=comps[0]\n        crop=crop_bbox(g,cells)\n        parts.append(crop)\n    out_h=max(len(p) for p in parts)\n    out_w=sum(len(p[0]) for p in parts)+len(parts)-1\n    out=blank(out_h,out_w)\n    x=0\n    for i,p in enumerate(parts):\n        ph,pw=size(p)\n        for r in range(ph):\n            for c in range(pw):\n                out[r][x+c]=p[r][c]\n        x += pw\n        if i != len(parts)-1:\n            x += 1\n    return out',
        "train": [
            {
                "input": ['040020070000', '000000000000', '004000000000', '044400000000', '000000007700', '000000007700', '000000000000', '020000000000', '020000000000', '022000000000', '000000000000', '000000000000'],
                "output": ['040020077', '444020077', '000022000'],
            },
            {
                "input": ['6003000080000', '0000000000000', '0660000000000', '0066000000000', '0000000000000', '0000000008800', '0000303008800', '0000333008000', '0000000000000', '0000000000000', '0000000000000'],
                "output": ['6600303088', '0660333088', '0000000080'],
            },
            {
                "input": ['005000700000', '000000000000', '000000000000', '050000000000', '050000002220', '055000002220', '000000000000', '007000000000', '077700006600', '000000006600', '000000000000', '000000000000'],
                "output": ['500070', '500777', '550000'],
            },
            {
                "input": ['0800030006000', '0000000000000', '0000000000000', '0808000000000', '0888000000600', '0000000006660', '0000000000000', '0000000000000', '0033000000000', '0003300000000', '0000000000000', '0000000000000', '0000000000000'],
                "output": ['80803300060', '88800330666'],
            },
        ],
        "test": {
            "input": ['07002000600000', '00000000000000', '00000000000000', '07700000000000', '07700000066000', '07000000066000', '00000000000000', '00000000000000', '02000000000000', '02000000000000', '02200000000000', '00000000000000', '00000000000000'],
            "output": ['77020066', '77020066', '70022000'],
        },
    },
    {
        "id": "H21",
        "title": 'Mask Transfer to the Rectangle',
        "difficulty": "hard",
        "skills": ['template extraction', 'mask transfer', 'bbox alignment'],
        "staged_hint": "First understand the 6-shape only as a binary mask inside its own bbox. Then apply that mask inside the 3-rectangle's bbox.",
        "written_solution": "Take the 6-component's occupied cells relative to its bounding box as a mask. Find the solid 3-rectangle with the same bbox size, clear that rectangle, and redraw the mask there using color 8. Keep the original 6-template unchanged.",
        "program_name": "rule_h21",
        "program_source": 'def rule_h21(g):\n    h,w=size(g); out=clone(g)\n    comps6=[cells for val,cells in components(g, colors={6})]\n    template=max(comps6, key=len)\n    tr0,tr1,tc0,tc1=bbox(template)\n    th,tw=tr1-tr0+1,tc1-tc0+1\n    rel={(r-tr0,c-tc0) for r,c in template}\n    target=None\n    for val,cells in components(g, colors={3}):\n        r0,r1,c0,c1=bbox(cells)\n        if is_solid_rect(cells) and (r1-r0+1, c1-c0+1)==(th,tw):\n            target=(r0,r1,c0,c1,cells)\n            break\n    assert target is not None\n    r0,r1,c0,c1,cells=target\n    for r,c in cells:\n        out[r][c]=0\n    for dr,dc in rel:\n        out[r0+dr][c0+dc]=8\n    return out',
        "train": [
            {
                "input": ['000000000000', '060000000000', '060000000000', '066000000000', '000000000000', '000000003300', '000000003300', '000000003300', '000000000000', '000000000000'],
                "output": ['000000000000', '060000000000', '060000000000', '066000000000', '000000000000', '000000008000', '000000008000', '000000008800', '000000000000', '000000000000'],
            },
            {
                "input": ['00000000000', '00000000000', '00000006600', '00000000660', '00000000000', '00000000000', '03330000000', '03330000000', '00000000000', '00000000000', '00000000000'],
                "output": ['00000000000', '00000000000', '00000006600', '00000000660', '00000000000', '00000000000', '08800000000', '00880000000', '00000000000', '00000000000', '00000000000'],
            },
            {
                "input": ['000000000000', '000006000000', '000066600000', '000000000000', '000000000000', '000000000000', '000000000000', '000000000000', '000000003330', '000000003330', '000000000000', '000000000000'],
                "output": ['000000000000', '000006000000', '000066600000', '000000000000', '000000000000', '000000000000', '000000000000', '000000000000', '000000000800', '000000008880', '000000000000', '000000000000'],
            },
            {
                "input": ['0000000000000', '0000000003330', '0000000003330', '0000000000000', '0000000000000', '0606000000000', '0666000000000', '0000000000000', '0000000000000', '0000000000000', '0000000000000', '0000000000000'],
                "output": ['0000000000000', '0000000008080', '0000000008880', '0000000000000', '0000000000000', '0606000000000', '0666000000000', '0000000000000', '0000000000000', '0000000000000', '0000000000000', '0000000000000'],
            },
        ],
        "test": {
            "input": ['0000000000000', '0000000000000', '0066000000000', '0066000000000', '0060000000000', '0000000000000', '0000000000000', '0000000000000', '0000000033000', '0000000033000', '0000000033000', '0000000000000', '0000000000000'],
            "output": ['0000000000000', '0000000000000', '0066000000000', '0066000000000', '0060000000000', '0000000000000', '0000000000000', '0000000000000', '0000000088000', '0000000088000', '0000000080000', '0000000000000', '0000000000000'],
        },
    },
]


def validate_bank() -> None:
    """Recompute every listed output from its reference solver."""
    for puzzle in PUZZLES:
        solver = SOLVERS[puzzle["program_name"]]
        for idx, pair in enumerate(puzzle["train"], 1):
            inp = grid_from_strings(*pair["input"])
            expected = grid_from_strings(*pair["output"])
            got = solver(inp)
            assert strings(got) == pair["output"], (
                f"{puzzle['id']} train {idx} failed\n"
                f"expected={pair['output']}\n"
                f"got={strings(got)}"
            )
        test_inp = grid_from_strings(*puzzle["test"]["input"])
        got_test = solver(test_inp)
        assert strings(got_test) == puzzle["test"]["output"], (
            f"{puzzle['id']} test failed\n"
            f"expected={puzzle['test']['output']}\n"
            f"got={strings(got_test)}"
        )
    print(f"validated {len(PUZZLES)} puzzles, 70 train pairs, set 3")

if __name__ == "__main__":
    validate_bank()
