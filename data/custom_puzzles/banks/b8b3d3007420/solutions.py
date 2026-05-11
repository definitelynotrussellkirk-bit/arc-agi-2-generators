"""ARC additional puzzle bank (21 puzzles, set 2): reference solvers + data.

This file accompanies arc_additional_puzzles_21_set2.md.
Programs are written as trustworthy Python reference implementations.
They are intended to be easy to translate into your solver DSL.
"""
from __future__ import annotations
from typing import List, Dict, Any

Grid = List[List[int]]

def blank(h,w,val=0):
    return [[val]*w for _ in range(h)]

def grid_from_strings(*rows):
    return [[int(ch) for ch in row] for row in rows]

def strings_from_grid(g: Grid):
    return ["".join(str(c) for c in row) for row in g]

def size(g):
    return len(g), len(g[0])

def clone(g):
    return [row[:] for row in g]

def orth_neighbors(r,c,h,w):
    for dr,dc in [(-1,0),(1,0),(0,-1),(0,1)]:
        nr,nc=r+dr,c+dc
        if 0<=nr<h and 0<=nc<w:
            yield nr,nc

def components(g, colors=None):
    h,w=size(g)
    vis=[[False]*w for _ in range(h)]
    comps=[]
    for r in range(h):
        for c in range(w):
            if vis[r][c]:
                continue
            val=g[r][c]
            if val==0 or (colors is not None and val not in colors):
                vis[r][c]=True
                continue
            stack=[(r,c)]
            vis[r][c]=True
            cells=[]
            while stack:
                rr,cc=stack.pop()
                cells.append((rr,cc))
                for nr,nc in orth_neighbors(rr,cc,h,w):
                    if not vis[nr][nc] and g[nr][nc]==val:
                        vis[nr][nc]=True
                        stack.append((nr,nc))
            comps.append((val,cells))
    return comps

def bbox(cells):
    rs=[r for r,c in cells]; cs=[c for r,c in cells]
    return min(rs),max(rs),min(cs),max(cs)

def crop_bbox(g, cells):
    rs=[r for r,c in cells]; cs=[c for r,c in cells]
    r0,r1=min(rs),max(rs); c0,c1=min(cs),max(cs)
    return [row[c0:c1+1] for row in g[r0:r1+1]]

def is_rect_frame(cells):
    r0,r1,c0,c1=bbox(cells)
    cellset=set(cells)
    expected=set()
    for c in range(c0,c1+1):
        expected.add((r0,c)); expected.add((r1,c))
    for r in range(r0,r1+1):
        expected.add((r,c0)); expected.add((r,c1))
    return cellset==expected and r1-r0>=2 and c1-c0>=2

def is_solid_rect(cells):
    r0,r1,c0,c1=bbox(cells)
    cellset=set(cells)
    expected={(r,c) for r in range(r0,r1+1) for c in range(c0,c1+1)}
    return cellset==expected

def is_vert_symmetric_crop(crop):
    h,w=size(crop)
    for r in range(h):
        for c in range(w):
            if crop[r][c]!=crop[r][w-1-c]:
                return False
    return True

def find_single(g, color):
    for r,row in enumerate(g):
        for c,v in enumerate(row):
            if v==color:
                return (r,c)
    return None

def crop_component(g, cells):
    return crop_bbox(g,cells)

def rule_e8(g):
    h,w=size(g); out=clone(g)
    for r in range(h):
        for c in range(w):
            if g[r][c]==2:
                for nr,nc in orth_neighbors(r,c,h,w):
                    if out[nr][nc]==0:
                        out[nr][nc]=6
    return out

def rule_e9(g):
    h,w=size(g); out=clone(g)
    for r in range(h):
        cols=[c for c in range(w) if g[r][c]==5]
        if len(cols)==2:
            c1,c2=cols
            if c2>c1+1 and all(g[r][c]==0 for c in range(c1+1,c2)):
                for c in range(c1+1,c2):
                    out[r][c]=3
    return out

def rule_e10(g):
    h,w=size(g); out=clone(g)
    for r in range(h-1):
        for c in range(w-1):
            block=[g[r][c],g[r][c+1],g[r+1][c],g[r+1][c+1]]
            if sum(v==4 for v in block)==3 and sum(v==0 for v in block)==1:
                if g[r][c]==0: out[r][c]=9
                if g[r][c+1]==0: out[r][c+1]=9
                if g[r+1][c]==0: out[r+1][c]=9
                if g[r+1][c+1]==0: out[r+1][c+1]=9
    return out

def rule_e11(g):
    h,w=size(g); out=clone(g)
    for r in range(1,h-1):
        for c in range(1,w-1):
            if g[r][c]==0 and g[r-1][c]==1 and g[r+1][c]==1 and g[r][c-1]==1 and g[r][c+1]==1:
                out[r][c]=8
    return out

def rule_e12(g):
    h,w=size(g); out=clone(g)
    for r in range(h):
        for c in range(w-2):
            if g[r][c]==2 and g[r][c+1]==3 and g[r][c+2]==0:
                out[r][c+2]=8
    return out

def rule_e13(g):
    h,w=size(g); out=clone(g)
    for c in range(w):
        rows=[r for r in range(h) if g[r][c]==7]
        if len(rows)==2:
            r1,r2=rows
            if r2>r1+1 and all(g[r][c]==0 for r in range(r1+1,r2)):
                for r in range(r1+1,r2):
                    out[r][c]=4
    return out

def rule_e14(g):
    h,w=size(g); out=clone(g)
    for r in range(h):
        cols=[c for c in range(w) if g[r][c]==8]
        if len(cols)==2:
            c1,c2=cols
            if (c1+c2)%2==0:
                mid=(c1+c2)//2
                if g[r][mid]==0:
                    out[r][mid]=2
    return out

def rule_m8(g):
    comps=components(g)
    comps_sorted=sorted(comps, key=lambda vc: (len(vc[1]), bbox(vc[1])[0], bbox(vc[1])[2]))
    val,cells=comps_sorted[0]
    return crop_bbox(g,cells)

def rule_m9(g):
    h,w=size(g); out=clone(g)
    for val,cells in components(g, colors={1}):
        if is_rect_frame(cells):
            r0,r1,c0,c1=bbox(cells)
            has_seed=any(g[r][c]==2 for r in range(r0+1,r1) for c in range(c0+1,c1))
            if has_seed:
                for r in range(r0+1,r1):
                    for c in range(c0+1,c1):
                        if out[r][c]==0:
                            out[r][c]=3
    return out

def rule_m10(g):
    out=clone(g)
    frames=[cells for val,cells in components(g, colors={1}) if is_rect_frame(cells)]
    for cells in frames:
        r0,r1,c0,c1=bbox(cells)
        for r in range(r0+1,r1):
            for c in range(c0+1,c1):
                if g[r][c]==4:
                    mc=c0+c1-c
                    if c0<mc<c1 and out[r][mc]==0:
                        out[r][mc]=7
    return out

def rule_m11(g):
    marker_color=None
    for c,v in enumerate(g[0]):
        if v!=0:
            marker_color=v
            break
    comps=[(val,cells) for val,cells in components(g) if val==marker_color and len(cells)>1]
    comps_sorted=sorted(comps, key=lambda vc: (bbox(vc[1])[0], bbox(vc[1])[2]))
    return crop_bbox(g, comps_sorted[0][1])

def rule_m12(g):
    h,w=size(g); out=clone(g)
    for val,cells in components(g, colors={6}):
        r0,r1,c0,c1=bbox(cells)
        for c in range(c0,c1+1):
            out[r0][c]=2; out[r1][c]=2
        for r in range(r0,r1+1):
            out[r][c0]=2; out[r][c1]=2
    return out

def rule_m13(g):
    out=clone(g)
    frames=[bbox(cells) for val,cells in components(g, colors={1}) if is_rect_frame(cells)]
    for r,row in enumerate(g):
        for c,val in enumerate(row):
            if val==2:
                inside=False
                for r0,r1,c0,c1 in frames:
                    if r0<r<r1 and c0<c<c1:
                        inside=True
                        break
                if inside:
                    out[r][c]=4
    return out

def rule_m14(g):
    comps=components(g)
    cand=[]
    for val,cells in comps:
        cr=crop_component(g,cells)
        if is_vert_symmetric_crop(cr):
            cand.append((bbox(cells)[0], bbox(cells)[2], cells))
    cand=sorted(cand)
    return crop_component(g,cand[0][2])

def rule_h8(g):
    comps=components(g)
    items=[]
    for val,cells in comps:
        cr=crop_component(g,cells)
        items.append((len(cells), bbox(cells)[0], bbox(cells)[2], cr))
    items.sort(key=lambda x: (-x[0], x[1], x[2]))
    crops=[it[3] for it in items]
    heights=[len(cr) for cr in crops]
    widths=[len(cr[0]) for cr in crops]
    H=max(heights)
    W=sum(widths)+max(0,len(crops)-1)
    out=blank(H,W)
    c=0
    for cr in crops:
        h,w=size(cr)
        for r in range(h):
            for cc in range(w):
                out[r][c+cc]=cr[r][cc]
        c+=w+1
    return out

def rule_h9(g):
    w=len(g[0])
    mapping={}
    for c in range(w):
        a,b=g[0][c],g[1][c]
        if a!=0 and b!=0:
            mapping[a]=b
    body=[row[:] for row in g[2:]]
    out=[]
    for row in body:
        out.append([mapping.get(v,v) for v in row])
    return out

def rule_h10(g):
    comps=components(g)
    items=[]
    for val,cells in comps:
        cr=crop_component(g,cells)
        items.append((val,cr))
    items.sort(key=lambda x:x[0])
    # assume four items
    tl,tr,bl,br=[cr for _,cr in items]
    row_heights=[max(len(tl),len(tr)), max(len(bl),len(br))]
    col_widths=[max(len(tl[0]),len(bl[0])), max(len(tr[0]),len(br[0]))]
    H=row_heights[0]+1+row_heights[1]
    W=col_widths[0]+1+col_widths[1]
    out=blank(H,W)
    positions=[(0,0),(0,col_widths[0]+1),(row_heights[0]+1,0),(row_heights[0]+1,col_widths[0]+1)]
    for cr,(r0,c0) in zip([tl,tr,bl,br], positions):
        h,w=size(cr)
        for r in range(h):
            for c in range(w):
                out[r0+r][c0+c]=cr[r][c]
    return out

def rule_h11(g):
    out=clone(g)
    comps=components(g)
    proto=None
    proto_crop=None
    # choose color 3 component as prototype (non-rectangular or first)
    for val,cells in comps:
        if val==3:
            proto=cells
            proto_crop=crop_component(g,cells)
            break
    ph,pw=size(proto_crop)
    mask=[[1 if proto_crop[r][c]==3 else 0 for c in range(pw)] for r in range(ph)]
    canvas=None
    for val,cells in comps:
        if val==8 and is_solid_rect(cells):
            r0,r1,c0,c1=bbox(cells)
            if (r1-r0+1, c1-c0+1)==(ph,pw):
                canvas=cells
                break
    r0,r1,c0,c1=bbox(canvas)
    for r in range(ph):
        for c in range(pw):
            out[r0+r][c0+c]=8 if mask[r][c] else 0
    return out

def rule_h12(g):
    h,w=size(g)
    out=blank(h,w)
    p8=find_single(g,8); p9=find_single(g,9)
    dr,dc=p9[0]-p8[0], p9[1]-p8[1]
    for r in range(h):
        for c in range(w):
            if g[r][c]==3:
                nr,nc=r+dr,c+dc
                if 0<=nr<h and 0<=nc<w and g[nr][nc]==4:
                    out[nr][nc]=7
    return out

def rule_h13(g):
    candidates=[]
    for val,cells in components(g, colors={1}):
        if is_rect_frame(cells):
            r0,r1,c0,c1=bbox(cells)
            seed_count=sum(g[r][c]==2 for r in range(r0+1,r1) for c in range(c0+1,c1))
            candidates.append((seed_count, r0, c0, (r0,r1,c0,c1)))
    candidates.sort(key=lambda t: (-t[0], t[1], t[2]))
    _,_,_,(r0,r1,c0,c1)=candidates[0]
    out=[row[c0:c1+1] for row in g[r0:r1+1]]
    h,w=size(out)
    for r in range(1,h-1):
        for c in range(1,w-1):
            if out[r][c]==0:
                out[r][c]=3
    return out

def rule_h14(g):
    out=clone(g)
    frames=[bbox(cells) for val,cells in components(g, colors={1}) if is_rect_frame(cells)]
    for r,row in enumerate(g):
        for c,val in enumerate(row):
            if val==0:
                depth=sum(1 for r0,r1,c0,c1 in frames if r0<r<r1 and c0<c<c1)
                if depth>0:
                    out[r][c]=depth+1
    return out

RULES = {
    "rule_e8": rule_e8,
    "rule_e9": rule_e9,
    "rule_e10": rule_e10,
    "rule_e11": rule_e11,
    "rule_e12": rule_e12,
    "rule_e13": rule_e13,
    "rule_e14": rule_e14,
    "rule_m8": rule_m8,
    "rule_m9": rule_m9,
    "rule_m10": rule_m10,
    "rule_m11": rule_m11,
    "rule_m12": rule_m12,
    "rule_m13": rule_m13,
    "rule_m14": rule_m14,
    "rule_h8": rule_h8,
    "rule_h9": rule_h9,
    "rule_h10": rule_h10,
    "rule_h11": rule_h11,
    "rule_h12": rule_h12,
    "rule_h13": rule_h13,
    "rule_h14": rule_h14,
}

PUZZLES: Dict[str, Any] = {'metadata': {'title': 'ARC Additional Puzzle Bank (21 puzzles, set 2)',
              'tiers': {'easy': 7, 'medium': 7, 'hard': 7},
              'numbering_continues_from_previous_bank': True,
              'note': 'Reference programs are in Python for trustworthiness and easy translation. This set continues '
                      'the prior bank with E8–E14, M8–M14, H8–H14.'},
 'puzzles': [{'id': 'E8',
              'title': 'Orthogonal Halo',
              'difficulty': 'easy',
              'skills': ['orthogonal neighborhood', 'edge clipping', 'copy-preserve'],
              'staged_hint': 'First mark the 2-cells, then add only their four orthogonal neighbors.',
              'written_solution': 'Each 2 behaves like a beacon. Keep the 2 itself, and paint each orthogonal neighbor '
                                  'with 6 when that neighbor lies inside the grid. Leave all other cells unchanged.',
              'program_name': 'rule_e8',
              'train': [{'input': ['000000', '002000', '000000', '000020', '000000', '200000'],
                         'output': ['006000', '062600', '006060', '000626', '600060', '260000']},
                        {'input': ['0000000', '0200020', '0000000', '0000000', '0002000', '0000000', '0000000'],
                         'output': ['0600060', '6260626', '0600060', '0006000', '0062600', '0006000', '0000000']}],
              'test_input': ['00000000',
                             '00002000',
                             '00000000',
                             '02000000',
                             '00000000',
                             '00000020',
                             '00000000',
                             '00200000'],
              'test_output': ['00006000',
                              '00062600',
                              '06006000',
                              '62600000',
                              '06000060',
                              '00000626',
                              '00600060',
                              '06260000']},
             {'id': 'E9',
              'title': 'Horizontal Span Fill',
              'difficulty': 'easy',
              'skills': ['rowwise pairing', 'gap filling', 'same-row reasoning'],
              'staged_hint': 'Find rows with exactly two 5s, then decide what happens only between them.',
              'written_solution': 'Look at each row separately. If a row has exactly two 5s, fill every 0 strictly '
                                  'between those two 5s with 3. Keep the endpoint 5s as they are.',
              'program_name': 'rule_e9',
              'train': [{'input': ['05000050', '00000000', '00500050', '00000000', '05050000', '00000000'],
                         'output': ['05333350', '00000000', '00533350', '00000000', '05350000', '00000000']},
                        {'input': ['000000000',
                                   '500050000',
                                   '000000000',
                                   '005000050',
                                   '000000000',
                                   '000050005',
                                   '000000000'],
                         'output': ['000000000',
                                    '533350000',
                                    '000000000',
                                    '005333350',
                                    '000000000',
                                    '000053335',
                                    '000000000']}],
              'test_input': ['0050000050',
                             '0000000000',
                             '0500050000',
                             '0000000000',
                             '0005000005',
                             '0000000000',
                             '5050000000',
                             '0000000000'],
              'test_output': ['0053333350',
                              '0000000000',
                              '0533350000',
                              '0000000000',
                              '0005333335',
                              '0000000000',
                              '5350000000',
                              '0000000000']},
             {'id': 'E10',
              'title': 'Missing L Corner',
              'difficulty': 'easy',
              'skills': ['2x2 scanning', 'L-pattern completion', 'local completion'],
              'staged_hint': 'Search 2×2 windows and count how many 4s they contain.',
              'written_solution': 'Inspect every 2×2 block. Whenever three cells are 4 and the fourth cell is 0, turn '
                                  'the missing corner into 9. The original 4s stay unchanged.',
              'program_name': 'rule_e10',
              'train': [{'input': ['0000000', '0440000', '0400000', '0000040', '0000440', '0000000', '0000000'],
                         'output': ['0000000', '0440000', '0490000', '0000940', '0000440', '0000000', '0000000']},
                        {'input': ['00000000',
                                   '00004400',
                                   '00000400',
                                   '00000000',
                                   '04000000',
                                   '04400440',
                                   '00000400',
                                   '00000000'],
                         'output': ['00000000',
                                    '00004400',
                                    '00009400',
                                    '00000000',
                                    '04900000',
                                    '04400440',
                                    '00000490',
                                    '00000000']}],
              'test_input': ['000000000',
                             '044000400',
                             '004000440',
                             '000000000',
                             '000000000',
                             '000440000',
                             '000400000',
                             '000000000',
                             '000000000'],
              'test_output': ['000000000',
                              '044000490',
                              '094000440',
                              '000000000',
                              '000000000',
                              '000440000',
                              '000490000',
                              '000000000',
                              '000000000']},
             {'id': 'E11',
              'title': 'Plus Center Insert',
              'difficulty': 'easy',
              'skills': ['orthogonal pattern detection', 'center inference', 'same-size recolor'],
              'staged_hint': 'Do not recolor the arms. Only ask which empty cells are surrounded up, down, left, and '
                             'right.',
              'written_solution': 'Any 0-cell whose four orthogonal neighbors are all 1 becomes 8. The surrounding '
                                  '1-cells remain 1, and every other cell stays the same.',
              'program_name': 'rule_e11',
              'train': [{'input': ['0000000', '0010000', '0101000', '0010000', '0000100', '0001010', '0000100'],
                         'output': ['0000000', '0010000', '0181000', '0010000', '0000100', '0001810', '0000100']},
                        {'input': ['00000000',
                                   '00000100',
                                   '00001010',
                                   '00000100',
                                   '00100000',
                                   '01010000',
                                   '00100000',
                                   '00000000'],
                         'output': ['00000000',
                                    '00000100',
                                    '00001810',
                                    '00000100',
                                    '00100000',
                                    '01810000',
                                    '00100000',
                                    '00000000']}],
              'test_input': ['000000000',
                             '001000100',
                             '010101010',
                             '001000100',
                             '000000000',
                             '000010000',
                             '000101000',
                             '000010000',
                             '000000000'],
              'test_output': ['000000000',
                              '001000100',
                              '018101810',
                              '001000100',
                              '000000000',
                              '000010000',
                              '000181000',
                              '000010000',
                              '000000000']},
             {'id': 'E12',
              'title': 'Directed Pair Extension',
              'difficulty': 'easy',
              'skills': ['oriented local pattern', 'contiguous triples', 'directionality'],
              'staged_hint': 'Treat `2,3` as a little arrow. Then ask what should appear immediately after it.',
              'written_solution': 'Scan each row for the pattern `2,3,0` in consecutive cells. When that exact '
                                  'left-to-right pattern appears, replace the trailing 0 with 8. Other arrangements, '
                                  'including `3,2`, do not change.',
              'program_name': 'rule_e12',
              'train': [{'input': ['00000000', '02300000', '00002300', '00000000', '32000000', '00023000', '00000000'],
                         'output': ['00000000',
                                    '02380000',
                                    '00002380',
                                    '00000000',
                                    '32000000',
                                    '00023800',
                                    '00000000']},
                        {'input': ['002300000',
                                   '000000000',
                                   '000000000',
                                   '023003200',
                                   '000000000',
                                   '000000000',
                                   '000023000',
                                   '000000000'],
                         'output': ['002380000',
                                    '000000000',
                                    '000000000',
                                    '023803200',
                                    '000000000',
                                    '000000000',
                                    '000023800',
                                    '000000000']}],
              'test_input': ['0000000000',
                             '0230002300',
                             '0000000000',
                             '0000000000',
                             '0002300000',
                             '0000000000',
                             '3200000000',
                             '0000023000',
                             '0000000000'],
              'test_output': ['0000000000',
                              '0238002380',
                              '0000000000',
                              '0000000000',
                              '0002380000',
                              '0000000000',
                              '3200000000',
                              '0000023800',
                              '0000000000']},
             {'id': 'E13',
              'title': 'Vertical Span Fill',
              'difficulty': 'easy',
              'skills': ['columnwise pairing', 'vertical gap filling', 'same-column reasoning'],
              'staged_hint': 'This is the column version of a between-two-markers task: inspect one column at a time.',
              'written_solution': 'Look at each column separately. If a column has exactly two 7s, fill every 0 '
                                  'strictly between those two 7s with 4. Keep the 7s themselves unchanged.',
              'program_name': 'rule_e13',
              'train': [{'input': ['0007000',
                                   '0000000',
                                   '0000000',
                                   '0007000',
                                   '7000007',
                                   '0000000',
                                   '0000000',
                                   '7000007'],
                         'output': ['0007000',
                                    '0004000',
                                    '0004000',
                                    '0007000',
                                    '7000007',
                                    '4000004',
                                    '4000004',
                                    '7000007']},
                        {'input': ['00000070',
                                   '07000000',
                                   '00070000',
                                   '00000000',
                                   '00000070',
                                   '07000000',
                                   '00000000',
                                   '00000000',
                                   '00070000'],
                         'output': ['00000070',
                                    '07000040',
                                    '04070040',
                                    '04040040',
                                    '04040070',
                                    '07040000',
                                    '00040000',
                                    '00040000',
                                    '00070000']}],
              'test_input': ['007000000',
                             '000000070',
                             '000000000',
                             '000070000',
                             '007000000',
                             '000000000',
                             '000070000',
                             '000000000',
                             '000000070',
                             '000000000'],
              'test_output': ['007000000',
                              '004000070',
                              '004000040',
                              '004070040',
                              '007040040',
                              '000040040',
                              '000070040',
                              '000000040',
                              '000000070',
                              '000000000']},
             {'id': 'E14',
              'title': 'Midpoint Marker',
              'difficulty': 'easy',
              'skills': ['midpoint detection', 'row geometry', 'pair reasoning'],
              'staged_hint': 'First find rows with two 8s. Then ask whether there is a single exact middle cell.',
              'written_solution': 'For each row with exactly two 8s, find the midpoint between them when it lands on a '
                                  'single cell. If that midpoint cell is 0, change it to 2. The two 8 endpoints remain '
                                  '8.',
              'program_name': 'rule_e14',
              'train': [{'input': ['08000800', '00000000', '00800080', '00000000', '80008000', '00000000'],
                         'output': ['08020800', '00000000', '00802080', '00000000', '80208000', '00000000']},
                        {'input': ['000000000',
                                   '080000080',
                                   '000000000',
                                   '008080000',
                                   '000000000',
                                   '000080008',
                                   '000000000'],
                         'output': ['000000000',
                                    '080020080',
                                    '000000000',
                                    '008280000',
                                    '000000000',
                                    '000080208',
                                    '000000000']}],
              'test_input': ['0080000080',
                             '0000000000',
                             '0800080000',
                             '0000000000',
                             '0008000008',
                             '0000000000',
                             '8000800000',
                             '0000000000'],
              'test_output': ['0080020080',
                              '0000000000',
                              '0802080000',
                              '0000000000',
                              '0008002008',
                              '0000000000',
                              '8020800000',
                              '0000000000']},
             {'id': 'M8',
              'title': 'Crop the Smallest Object',
              'difficulty': 'medium',
              'skills': ['connected components', 'size comparison', 'tight cropping'],
              'staged_hint': 'Separate the nonzero objects first. Only after that compare their areas.',
              'written_solution': 'Find all connected nonzero objects. Choose the one with the fewest cells, then '
                                  'output only its tight bounding-box crop, preserving its original color pattern.',
              'program_name': 'rule_m8',
              'train': [{'input': ['0000000000',
                                   '0220003330',
                                   '0200000300',
                                   '0000003330',
                                   '0000000000',
                                   '0000444400',
                                   '0000000000',
                                   '0000000000'],
                         'output': ['22', '20']},
                        {'input': ['00000000000',
                                   '05500000000',
                                   '05000066600',
                                   '00000066600',
                                   '00000000000',
                                   '00000000000',
                                   '00077700000',
                                   '00007000000',
                                   '00000000000'],
                         'output': ['55', '50']}],
              'test_input': ['000000000000',
                             '008800022220',
                             '008000000000',
                             '000000000000',
                             '000000000000',
                             '000003330000',
                             '000003030000',
                             '000003330000',
                             '000000000000',
                             '000000000000'],
              'test_output': ['88', '80']},
             {'id': 'M9',
              'title': 'Seeded Frame Interior Fill',
              'difficulty': 'medium',
              'skills': ['frame detection', 'interior filling', 'conditional object selection'],
              'staged_hint': 'Identify the rectangular frames first; the seed only tells you which frames should '
                             'activate.',
              'written_solution': 'Locate every hollow rectangular frame made of 1s. If a frame contains at least one '
                                  '2 inside it, fill its interior 0-cells with 3 while leaving the border 1s and any 2 '
                                  'seeds unchanged. Frames without a seed stay untouched.',
              'program_name': 'rule_m9',
              'train': [{'input': ['000000000000',
                                   '011111000000',
                                   '010201000000',
                                   '010001000000',
                                   '011111000000',
                                   '000000111110',
                                   '000000100010',
                                   '000000100010',
                                   '000000111110',
                                   '000000000000'],
                         'output': ['000000000000',
                                    '011111000000',
                                    '013231000000',
                                    '013331000000',
                                    '011111000000',
                                    '000000111110',
                                    '000000100010',
                                    '000000100010',
                                    '000000111110',
                                    '000000000000']},
                        {'input': ['0000000000000',
                                   '0111111000000',
                                   '0102001000000',
                                   '0100001011110',
                                   '0100201010010',
                                   '0111111010010',
                                   '0000000011110',
                                   '0000000000000',
                                   '0000000000000',
                                   '0000000000000',
                                   '0000000000000'],
                         'output': ['0000000000000',
                                    '0111111000000',
                                    '0132331000000',
                                    '0133331011110',
                                    '0133231010010',
                                    '0111111010010',
                                    '0000000011110',
                                    '0000000000000',
                                    '0000000000000',
                                    '0000000000000',
                                    '0000000000000']}],
              'test_input': ['00000000000000',
                             '01111100111100',
                             '01000100100100',
                             '01020100100100',
                             '01000100111100',
                             '01111100000000',
                             '00000001111110',
                             '00000001020010',
                             '00000001002010',
                             '00000001000010',
                             '00000001111110',
                             '00000000000000'],
              'test_output': ['00000000000000',
                              '01111100111100',
                              '01333100100100',
                              '01323100100100',
                              '01333100111100',
                              '01111100000000',
                              '00000001111110',
                              '00000001323310',
                              '00000001332310',
                              '00000001333310',
                              '00000001111110',
                              '00000000000000']},
             {'id': 'M10',
              'title': 'Mirror Inside the Frame',
              'difficulty': 'medium',
              'skills': ['frame-local coordinates', 'vertical symmetry', 'copy with recolor'],
              'staged_hint': 'Work in coordinates relative to the frame interior, not the whole grid.',
              'written_solution': 'Inside each 1-frame, take every 4-cell and reflect it across the frame’s vertical '
                                  'axis. Put a 7 at the mirrored location when that location is empty. Keep the '
                                  'original 4s and the frame itself.',
              'program_name': 'rule_m10',
              'train': [{'input': ['00000000000',
                                   '01111111110',
                                   '01400000010',
                                   '01040000010',
                                   '01000000010',
                                   '01400000010',
                                   '01004000010',
                                   '01111111110',
                                   '00000000000'],
                         'output': ['00000000000',
                                    '01111111110',
                                    '01400000710',
                                    '01040007010',
                                    '01000000010',
                                    '01400000710',
                                    '01004070010',
                                    '01111111110',
                                    '00000000000']},
                        {'input': ['000000000000',
                                   '001111111100',
                                   '001400000100',
                                   '001000000100',
                                   '001040000100',
                                   '001000000100',
                                   '001400000100',
                                   '001004000100',
                                   '001111111100',
                                   '000000000000'],
                         'output': ['000000000000',
                                    '001111111100',
                                    '001400007100',
                                    '001000000100',
                                    '001040070100',
                                    '001000000100',
                                    '001400007100',
                                    '001004700100',
                                    '001111111100',
                                    '000000000000']}],
              'test_input': ['0000000000000',
                             '0111111111110',
                             '0140000000010',
                             '0100400000010',
                             '0100000000010',
                             '0104000000010',
                             '0100000000010',
                             '0140000000010',
                             '0100040000010',
                             '0111111111110',
                             '0000000000000'],
              'test_output': ['0000000000000',
                              '0111111111110',
                              '0140000000710',
                              '0100400070010',
                              '0100000000010',
                              '0104000007010',
                              '0100000000010',
                              '0140000000710',
                              '0100040700010',
                              '0111111111110',
                              '0000000000000']},
             {'id': 'M11',
              'title': 'Marker-Selected Object Crop',
              'difficulty': 'medium',
              'skills': ['external marker use', 'color matching', 'tight cropping'],
              'staged_hint': 'Read the top-row marker first. Only then decide which object matters.',
              'written_solution': 'The single nonzero marker in the top row tells you the target color. Among the '
                                  'larger objects in the main field, select the object of that same color and output '
                                  'its tight bounding-box crop.',
              'program_name': 'rule_m11',
              'train': [{'input': ['400000000000',
                                   '000000000000',
                                   '003300044400',
                                   '003000004000',
                                   '000000000000',
                                   '000000000000',
                                   '000005555000',
                                   '000000000000',
                                   '000000000000'],
                         'output': ['444', '040']},
                        {'input': ['0000060000000',
                                   '0000000000000',
                                   '0220000000000',
                                   '0200000066000',
                                   '0000000006000',
                                   '0000000000000',
                                   '0000000000000',
                                   '0000000003330',
                                   '0000000000000',
                                   '0000000000000'],
                         'output': ['66', '06']}],
              'test_input': ['00000000500000',
                             '00000000000000',
                             '04440000000000',
                             '00400000550000',
                             '00000000500000',
                             '00000000000000',
                             '00000000000000',
                             '00000222200000',
                             '00000000000000',
                             '00000000000000',
                             '00000000000000'],
              'test_output': ['55', '50']},
             {'id': 'M12',
              'title': 'Bounding Box Outline',
              'difficulty': 'medium',
              'skills': ['component analysis', 'bounding boxes', 'outline drawing'],
              'staged_hint': 'Do not try to redraw the object. Just find the smallest rectangle that contains it.',
              'written_solution': 'For each connected object of color 6, compute its tight bounding box and draw that '
                                  'box’s border in color 2. Everything else remains unchanged.',
              'program_name': 'rule_m12',
              'train': [{'input': ['000000000000',
                                   '066000000000',
                                   '006000000000',
                                   '066000000000',
                                   '000000000000',
                                   '000000006000',
                                   '000000066600',
                                   '000000006000',
                                   '000000000000',
                                   '000000000000'],
                         'output': ['000000000000',
                                    '022000000000',
                                    '022000000000',
                                    '022000000000',
                                    '000000000000',
                                    '000000022200',
                                    '000000026200',
                                    '000000022200',
                                    '000000000000',
                                    '000000000000']},
                        {'input': ['0000000000000',
                                   '0000000000000',
                                   '0066600000000',
                                   '0006000000000',
                                   '0000000000000',
                                   '0000000000000',
                                   '0000000066000',
                                   '0000000060000',
                                   '0000000066000',
                                   '0000000000000',
                                   '0000000000000'],
                         'output': ['0000000000000',
                                    '0000000000000',
                                    '0022200000000',
                                    '0022200000000',
                                    '0000000000000',
                                    '0000000000000',
                                    '0000000022000',
                                    '0000000022000',
                                    '0000000022000',
                                    '0000000000000',
                                    '0000000000000']}],
              'test_input': ['00000000000000',
                             '00060000000000',
                             '00666000000000',
                             '00060000000000',
                             '00000000000000',
                             '00000000000000',
                             '00000000066600',
                             '00000000060600',
                             '00000000066600',
                             '00000000000000',
                             '00000000000000',
                             '00000000000000'],
              'test_output': ['00000000000000',
                              '00222000000000',
                              '00262000000000',
                              '00222000000000',
                              '00000000000000',
                              '00000000000000',
                              '00000000022200',
                              '00000000020200',
                              '00000000022200',
                              '00000000000000',
                              '00000000000000',
                              '00000000000000']},
             {'id': 'M13',
              'title': 'Recolor Only the Enclosed Cells',
              'difficulty': 'medium',
              'skills': ['enclosure', 'inside-vs-outside distinction', 'frame reasoning'],
              'staged_hint': 'Classify every 2-cell by whether it lies strictly inside a 1-frame.',
              'written_solution': 'Any cell of color 2 that lies strictly inside a rectangular 1-frame becomes 4. '
                                  'Cells of color 2 outside all frames do not change.',
              'program_name': 'rule_m13',
              'train': [{'input': ['000000000002',
                                   '011111000000',
                                   '010201000000',
                                   '010001000000',
                                   '011111000000',
                                   '000000111110',
                                   '000000100010',
                                   '000000102010',
                                   '000000111110',
                                   '200000000000'],
                         'output': ['000000000002',
                                    '011111000000',
                                    '010401000000',
                                    '010001000000',
                                    '011111000000',
                                    '000000111110',
                                    '000000100010',
                                    '000000104010',
                                    '000000111110',
                                    '200000000000']},
                        {'input': ['2000000000000',
                                   '0011111100000',
                                   '0010200100000',
                                   '0010020100000',
                                   '0010000101111',
                                   '0011111101201',
                                   '0000000001001',
                                   '0000000001111',
                                   '0000000000000',
                                   '0000000000000',
                                   '0000000000002'],
                         'output': ['2000000000000',
                                    '0011111100000',
                                    '0010400100000',
                                    '0010040100000',
                                    '0010000101111',
                                    '0011111101401',
                                    '0000000001001',
                                    '0000000001111',
                                    '0000000000000',
                                    '0000000000000',
                                    '0000000000002']}],
              'test_input': ['00000000000002',
                             '01111100000000',
                             '01200100000000',
                             '01000100000000',
                             '01002100000000',
                             '01111100000000',
                             '00000000111110',
                             '00000000102010',
                             '00000000120010',
                             '00000000100010',
                             '00000000111110',
                             '20000000000000'],
              'test_output': ['00000000000002',
                              '01111100000000',
                              '01400100000000',
                              '01000100000000',
                              '01004100000000',
                              '01111100000000',
                              '00000000111110',
                              '00000000104010',
                              '00000000140010',
                              '00000000100010',
                              '00000000111110',
                              '20000000000000']},
             {'id': 'M14',
              'title': 'Crop the Vertically Symmetric Object',
              'difficulty': 'medium',
              'skills': ['component extraction', 'symmetry testing', 'object selection'],
              'staged_hint': 'Crop each object first. Symmetry is easiest to test in its own local box.',
              'written_solution': 'Find all connected nonzero objects and take each one’s tight crop. Choose the '
                                  'object whose crop is vertically symmetric, then output that crop by itself.',
              'program_name': 'rule_m14',
              'train': [{'input': ['000000000000',
                                   '033000000000',
                                   '030000004000',
                                   '000000044400',
                                   '000000004000',
                                   '000000000000',
                                   '000055000000',
                                   '000005000000',
                                   '000005000000',
                                   '000000000000'],
                         'output': ['040', '444', '040']},
                        {'input': ['0000000000000',
                                   '0022200000000',
                                   '0002000000000',
                                   '0000000006000',
                                   '0000000066600',
                                   '0000000006000',
                                   '0000000000000',
                                   '0770000000000',
                                   '0070000000000',
                                   '0000000000000',
                                   '0000000000000'],
                         'output': ['222', '020']}],
              'test_input': ['00000000000000',
                             '04400000000000',
                             '04000000005000',
                             '00000000055500',
                             '00000000005000',
                             '00000000000000',
                             '00000000000000',
                             '00000000000000',
                             '00000220000000',
                             '00000020000000',
                             '00000020000000',
                             '00000000000000'],
              'test_output': ['050', '555', '050']},
             {'id': 'H8',
              'title': 'Pack Components by Area',
              'difficulty': 'hard',
              'skills': ['component extraction', 'sorting', 'layout synthesis'],
              'staged_hint': 'Solve it in three stages: crop each object, rank them by size, then lay them out left to '
                             'right.',
              'written_solution': 'Extract every connected nonzero object and crop it tightly. Sort the crops by '
                                  'decreasing cell count, then place them left-to-right in a new grid, top-aligned, '
                                  'with a single zero column separating neighboring crops.',
              'program_name': 'rule_h8',
              'train': [{'input': ['000000000000000',
                                   '022000003330000',
                                   '022000000300000',
                                   '020000003330000',
                                   '000000000000000',
                                   '000000000000000',
                                   '000004444000000',
                                   '000000000000000',
                                   '000000000000000',
                                   '000000000000000'],
                         'output': ['33302204444', '03002200000', '33302000000']},
                        {'input': ['0000000000000000',
                                   '0055000000000000',
                                   '0055000000666000',
                                   '0050000000060000',
                                   '0000000000666000',
                                   '0000000000000000',
                                   '0000000000000000',
                                   '0000000000000000',
                                   '0000007770000000',
                                   '0000000000000000',
                                   '0000000000000000'],
                         'output': ['6660550777', '0600550000', '6660500000']}],
              'test_input': ['00000000000000000',
                             '08800000000000000',
                             '08800000022220000',
                             '08000000000000000',
                             '00000000000000000',
                             '00000000000000000',
                             '00000000000000000',
                             '00000000000033300',
                             '00000000000003000',
                             '00000000000033300',
                             '00000000000000000',
                             '00000000000000000'],
              'test_output': ['33308802222', '03008800000', '33308000000']},
             {'id': 'H9',
              'title': 'Two-Row Legend Recolor',
              'difficulty': 'hard',
              'skills': ['legend decoding', 'mapping application', 'resize by header removal'],
              'staged_hint': 'The top two rows are not part of the picture; they encode a color map.',
              'written_solution': 'Use the first two rows as a legend: each nonzero color in row 0 maps to the color '
                                  'directly beneath it in row 1. Remove those two legend rows, and recolor the '
                                  'remaining grid according to that mapping.',
              'program_name': 'rule_h9',
              'train': [{'input': ['2046000', '7068000', '0204600', '4440000', '0002200', '0060000', '0000000'],
                         'output': ['0706800', '6660000', '0007700', '0080000', '0000000']},
                        {'input': ['3050000', '9070000', '0035000', '5550000', '0003300', '0000000', '0503000'],
                         'output': ['0097000', '7770000', '0009900', '0000000', '0709000']}],
              'test_input': ['20350000',
                             '60870000',
                             '02035000',
                             '33300000',
                             '00022000',
                             '00500000',
                             '00000300',
                             '00000000'],
              'test_output': ['06087000', '88800000', '00066000', '00700000', '00000800', '00000000']},
             {'id': 'H10',
              'title': 'Quadrant Pack by Color',
              'difficulty': 'hard',
              'skills': ['object sorting', 'packing into quadrants', 'variable-size output'],
              'staged_hint': 'First crop the four objects. Then sort them by color before you think about the output '
                             'layout.',
              'written_solution': 'Crop the four colored objects tightly and order them by increasing color value. '
                                  'Place the first two crops in the top row of a new 2×2 arrangement and the next two '
                                  'in the bottom row, using a single zero row and a single zero column as separators.',
              'program_name': 'rule_h10',
              'train': [{'input': ['0000000000000000',
                                   '0220000033300000',
                                   '0200000000000000',
                                   '0000000000000000',
                                   '0000000000000000',
                                   '0000000000000000',
                                   '0040000000000000',
                                   '0044000000550000',
                                   '0000000000550000',
                                   '0000000000000000',
                                   '0000000000000000',
                                   '0000000000000000'],
                         'output': ['220333', '200000', '000000', '400550', '440550']},
                        {'input': ['00000000000000000',
                                   '00330000000000000',
                                   '00030000002222000',
                                   '00000000000000000',
                                   '00000000000000000',
                                   '00000000000000000',
                                   '00000000000000000',
                                   '00004000000000000',
                                   '00044400000055000',
                                   '00000000000050000',
                                   '00000000000050000',
                                   '00000000000000000',
                                   '00000000000000000'],
                         'output': ['2222033', '0000003', '0000000', '0400055', '4440050', '0000050']}],
              'test_input': ['000000000000000000',
                             '022200000000000000',
                             '002000000033000000',
                             '000000000003000000',
                             '000000000000000000',
                             '000000000000000000',
                             '000000000000000000',
                             '000000000000000000',
                             '004400000000000000',
                             '004400000000050000',
                             '000000000000555000',
                             '000000000000050000',
                             '000000000000000000',
                             '000000000000000000'],
              'test_output': ['2220330', '0200030', '0000000', '4400050', '4400555', '0000050']},
             {'id': 'H11',
              'title': 'Stencil Transfer to the Solid Canvas',
              'difficulty': 'hard',
              'skills': ['template extraction', 'mask transfer', 'paired-object reasoning'],
              'staged_hint': 'One object gives you the shape; the other gives you the target location and target '
                             'color.',
              'written_solution': 'Take the tight crop of the color-3 prototype as a binary mask. Find the solid '
                                  'color-8 rectangle with the same dimensions, and keep only those 8-cells whose '
                                  'positions match nonzero cells in the prototype mask. Everything else in that canvas '
                                  'becomes 0.',
              'program_name': 'rule_h11',
              'train': [{'input': ['00000000000000',
                                   '03300000000000',
                                   '00300000000000',
                                   '03330000000000',
                                   '00000000000000',
                                   '00000000888000',
                                   '00000000888000',
                                   '00000000888000',
                                   '00000000000000',
                                   '00000000000000'],
                         'output': ['00000000000000',
                                    '03300000000000',
                                    '00300000000000',
                                    '03330000000000',
                                    '00000000000000',
                                    '00000000880000',
                                    '00000000080000',
                                    '00000000888000',
                                    '00000000000000',
                                    '00000000000000']},
                        {'input': ['000000000000000',
                                   '000000000000000',
                                   '003030000000000',
                                   '003333000000000',
                                   '000030000000000',
                                   '000000000000000',
                                   '000000000888800',
                                   '000000000888800',
                                   '000000000888800',
                                   '000000000000000',
                                   '000000000000000'],
                         'output': ['000000000000000',
                                    '000000000000000',
                                    '003030000000000',
                                    '003333000000000',
                                    '000030000000000',
                                    '000000000000000',
                                    '000000000808000',
                                    '000000000888800',
                                    '000000000008000',
                                    '000000000000000',
                                    '000000000000000']}],
              'test_input': ['0000000000000000',
                             '0003300000000000',
                             '0000300000000000',
                             '0033330000000000',
                             '0000000000000000',
                             '0000000000000000',
                             '0000000000000000',
                             '0000000000888800',
                             '0000000000888800',
                             '0000000000888800',
                             '0000000000000000',
                             '0000000000000000'],
              'test_output': ['0000000000000000',
                              '0003300000000000',
                              '0000300000000000',
                              '0033330000000000',
                              '0000000000000000',
                              '0000000000000000',
                              '0000000000000000',
                              '0000000000088000',
                              '0000000000008000',
                              '0000000000888800',
                              '0000000000000000',
                              '0000000000000000']},
             {'id': 'H12',
              'title': 'Vector Overlap Highlight',
              'difficulty': 'hard',
              'skills': ['vector inference', 'translation', 'intersection reasoning'],
              'staged_hint': 'First read the displacement from 8 to 9. Then apply exactly that displacement to the '
                             '3-cells.',
              'written_solution': 'The vector from the single 8 to the single 9 is the movement rule. Shift every '
                                  '3-cell by that vector, and whenever a shifted 3 lands on a 4-cell, mark that '
                                  'landing cell with 7 in an otherwise empty output grid.',
              'program_name': 'rule_h12',
              'train': [{'input': ['300000000000',
                                   '080000000000',
                                   '003400000000',
                                   '000090000000',
                                   '030004000000',
                                   '000000000000',
                                   '000040000000',
                                   '000000000000',
                                   '000000004000'],
                         'output': ['000000000000',
                                    '000000000000',
                                    '000700000000',
                                    '000000000000',
                                    '000007000000',
                                    '000000000000',
                                    '000070000000',
                                    '000000000000',
                                    '000000000000']},
                        {'input': ['0080000000000',
                                   '0300000000000',
                                   '0000030000000',
                                   '0009000000000',
                                   '0040000000000',
                                   '0000304000000',
                                   '0000000000000',
                                   '0000000040000',
                                   '0000040000000',
                                   '0000000000000'],
                         'output': ['0000000000000',
                                    '0000000000000',
                                    '0000000000000',
                                    '0000000000000',
                                    '0070000000000',
                                    '0000007000000',
                                    '0000000000000',
                                    '0000000000000',
                                    '0000070000000',
                                    '0000000000000']}],
              'test_input': ['03000000000000',
                             '80000000000000',
                             '00003000000000',
                             '00040000000000',
                             '00900000000000',
                             '00030040000000',
                             '00000000300000',
                             '00000000000000',
                             '00000400000000',
                             '00000000004000',
                             '00000000000000'],
              'test_output': ['00000000000000',
                              '00000000000000',
                              '00000000000000',
                              '00070000000000',
                              '00000000000000',
                              '00000070000000',
                              '00000000000000',
                              '00000000000000',
                              '00000700000000',
                              '00000000007000',
                              '00000000000000']},
             {'id': 'H13',
              'title': 'Select the Seed-Rich Frame',
              'difficulty': 'hard',
              'skills': ['frame ranking', 'count comparison', 'cropped transformation'],
              'staged_hint': 'Count seeds inside each frame before doing any filling.',
              'written_solution': 'Among the rectangular 1-frames, choose the one whose interior contains the most 2 '
                                  'seeds. Output that frame’s tight crop, and fill its interior 0-cells with 3 while '
                                  'keeping both the border 1s and the 2 seeds.',
              'program_name': 'rule_h13',
              'train': [{'input': ['00000000000000',
                                   '01111100000000',
                                   '01020100000000',
                                   '01000100000000',
                                   '01111100000000',
                                   '00000000000000',
                                   '00000001111110',
                                   '00000001200010',
                                   '00000001002010',
                                   '00000001020010',
                                   '00000001111110',
                                   '00000000000000'],
                         'output': ['111111', '123331', '133231', '132331', '111111']},
                        {'input': ['000000000000000',
                                   '001111100000000',
                                   '001200100000000',
                                   '001000100000000',
                                   '001002100000000',
                                   '001111100000000',
                                   '000000000000000',
                                   '000000001111100',
                                   '000000001020100',
                                   '000000001000100',
                                   '000000001111100',
                                   '000000000000000',
                                   '000000000000000'],
                         'output': ['11111', '12331', '13331', '13321', '11111']}],
              'test_input': ['0000000000000000',
                             '0111111000000000',
                             '0102001000111100',
                             '0100021000120100',
                             '0120001000111100',
                             '0111111000000000',
                             '0000000000000000',
                             '0000000001111100',
                             '0000000001020100',
                             '0000000001000100',
                             '0000000001200100',
                             '0000000001111100',
                             '0000000000000000',
                             '0000000000000000'],
              'test_output': ['111111', '132331', '133321', '123331', '111111']},
             {'id': 'H14',
              'title': 'Nested Depth Fill',
              'difficulty': 'hard',
              'skills': ['nesting depth', 'region analysis', 'multi-level filling'],
              'staged_hint': 'Do not think in terms of one frame at a time; think in terms of how many frames enclose '
                             'each cell.',
              'written_solution': 'Keep all frame borders as 1. For every 0-cell, count how many rectangular 1-frames '
                                  'strictly enclose it. A cell inside one frame becomes 2, inside two frames becomes '
                                  '3, inside three frames becomes 4, and so on; cells outside all frames stay 0.',
              'program_name': 'rule_h14',
              'train': [{'input': ['0000000000000',
                                   '0111111111110',
                                   '0100000000010',
                                   '0101111111010',
                                   '0101000001010',
                                   '0101011101010',
                                   '0101010101010',
                                   '0101011101010',
                                   '0101000001010',
                                   '0101111111010',
                                   '0100000000010',
                                   '0111111111110',
                                   '0000000000000'],
                         'output': ['0000000000000',
                                    '0111111111110',
                                    '0122222222210',
                                    '0121111111210',
                                    '0121333331210',
                                    '0121311131210',
                                    '0121314131210',
                                    '0121311131210',
                                    '0121333331210',
                                    '0121111111210',
                                    '0122222222210',
                                    '0111111111110',
                                    '0000000000000']},
                        {'input': ['000000000000',
                                   '011111111110',
                                   '010000000010',
                                   '010111111010',
                                   '010100001010',
                                   '010100001010',
                                   '010100001010',
                                   '010100001010',
                                   '010111111010',
                                   '010000000010',
                                   '011111111110',
                                   '000000000000'],
                         'output': ['000000000000',
                                    '011111111110',
                                    '012222222210',
                                    '012111111210',
                                    '012133331210',
                                    '012133331210',
                                    '012133331210',
                                    '012133331210',
                                    '012111111210',
                                    '012222222210',
                                    '011111111110',
                                    '000000000000']}],
              'test_input': ['000000000000000',
                             '011111111111110',
                             '010000000000010',
                             '010111111111010',
                             '010100000001010',
                             '010101111101010',
                             '010101000101010',
                             '010101000101010',
                             '010101000101010',
                             '010101111101010',
                             '010100000001010',
                             '010111111111010',
                             '010000000000010',
                             '011111111111110',
                             '000000000000000'],
              'test_output': ['000000000000000',
                              '011111111111110',
                              '012222222222210',
                              '012111111111210',
                              '012133333331210',
                              '012131111131210',
                              '012131444131210',
                              '012131444131210',
                              '012131444131210',
                              '012131111131210',
                              '012133333331210',
                              '012111111111210',
                              '012222222222210',
                              '011111111111110',
                              '000000000000000']}]}

def apply_rule(rule_name: str, grid_strings: List[str]) -> List[str]:
    g = grid_from_strings(*grid_strings)
    return strings_from_grid(RULES[rule_name](g))


def validate() -> None:
    for puzzle in PUZZLES["puzzles"]:
        rule_name = puzzle["program_name"]
        for pair in puzzle["train"]:
            got = apply_rule(rule_name, pair["input"])
            assert got == pair["output"], (puzzle["id"], "train", got, pair["output"])
        got_test = apply_rule(rule_name, puzzle["test_input"])
        assert got_test == puzzle["test_output"], (puzzle["id"], "test", got_test, puzzle["test_output"])


if __name__ == "__main__":
    validate()
    print("validated", len(PUZZLES["puzzles"]), "puzzles")
