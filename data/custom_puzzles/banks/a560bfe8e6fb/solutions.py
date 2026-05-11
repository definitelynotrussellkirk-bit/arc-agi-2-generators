from __future__ import annotations
import collections
import json
from pathlib import Path

DIR4 = [(-1,0),(1,0),(0,-1),(0,1)]

def blank(h,w,val=0):
    return [[val for _ in range(w)] for _ in range(h)]

def clone(g):
    return [row[:] for row in g]

def size(g):
    return len(g), len(g[0])

def strings_from_grid(g):
    return ["".join(str(c) for c in row) for row in g]

def grid_from_strings(rows):
    return [[int(ch) for ch in row] for row in rows]

def rotate_cw(g):
    h,w=size(g)
    return [[g[h-1-r][c] for r in range(h)] for c in range(w)]

def rotate_k(g, k):
    out=clone(g)
    for _ in range(k%4):
        out=rotate_cw(out)
    return out

def project_rays(base_grid, starts, directions=DIR4, *, stop_colors=None, stop_nonzero=False, paint='source', respect_original_nonzero=True):
    """
    Invented primitive for this set.
    base_grid: source grid
    starts: iterable of (r,c)
    directions: step directions
    stop_colors: colors that stop before painting
    stop_nonzero: any nonzero stops
    paint: 'source' or fixed int color
    respect_original_nonzero: do not paint over original nonzero cells
    returns new grid with rays painted
    """
    g=clone(base_grid)
    h,w=size(base_grid)
    stop_colors=set(stop_colors or [])
    for r,c in starts:
        src=base_grid[r][c]
        for dr,dc in directions:
            nr,nc=r+dr,c+dc
            while 0<=nr<h and 0<=nc<w:
                v=base_grid[nr][nc]
                if (stop_nonzero and v!=0) or (v in stop_colors):
                    break
                if not (respect_original_nonzero and v!=0):
                    g[nr][nc] = src if paint=='source' else paint
                nr += dr; nc += dc
    return g

def orth_neighbors(r,c,h,w):
    for dr,dc in DIR4:
        nr,nc=r+dr,c+dc
        if 0<=nr<h and 0<=nc<w:
            yield nr,nc

def components_same_color(g, colors=None):
    h,w=size(g)
    vis=[[False]*w for _ in range(h)]
    comps=[]
    for r in range(h):
        for c in range(w):
            if vis[r][c]:
                continue
            vis[r][c]=True
            v=g[r][c]
            if v==0 or (colors is not None and v not in colors):
                continue
            stack=[(r,c)]
            cells=[(r,c)]
            while stack:
                rr,cc=stack.pop()
                for nr,nc in orth_neighbors(rr,cc,h,w):
                    if not vis[nr][nc] and g[nr][nc]==v:
                        vis[nr][nc]=True
                        stack.append((nr,nc))
                        cells.append((nr,nc))
            comps.append((v,cells))
    return comps

def components_nonzero(g, *, treat_colors_separately=False):
    h,w=size(g)
    vis=[[False]*w for _ in range(h)]
    comps=[]
    for r in range(h):
        for c in range(w):
            if vis[r][c]:
                continue
            vis[r][c]=True
            v=g[r][c]
            if v==0:
                continue
            stack=[(r,c)]
            cells=[(r,c)]
            while stack:
                rr,cc=stack.pop()
                for nr,nc in orth_neighbors(rr,cc,h,w):
                    if vis[nr][nc]:
                        continue
                    if g[nr][nc]==0:
                        vis[nr][nc]=True
                        continue
                    if treat_colors_separately and g[nr][nc]!=v:
                        continue
                    vis[nr][nc]=True
                    stack.append((nr,nc))
                    cells.append((nr,nc))
            comps.append(cells)
    return comps

def bbox(cells):
    rs=[r for r,c in cells]
    cs=[c for r,c in cells]
    return min(rs), max(rs), min(cs), max(cs)

def crop_to_cells(g, cells):
    r0,r1,c0,c1=bbox(cells)
    return [row[c0:c1+1] for row in g[r0:r1+1]]

def stack_horizontal(grids, gap=1):
    h=max(len(g) for g in grids)
    w=sum(len(g[0]) for g in grids)+gap*(len(grids)-1)
    out=blank(h,w)
    c0=0
    for i,g in enumerate(grids):
        for r,row in enumerate(g):
            for c,v in enumerate(row):
                out[r][c0+c]=v
        c0 += len(g[0])
        if i < len(grids)-1:
            c0 += gap
    return out

def stack_vertical(grids, gap=1):
    h=sum(len(g) for g in grids)+gap*(len(grids)-1)
    w=max(len(g[0]) for g in grids)
    out=blank(h,w)
    r0=0
    for i,g in enumerate(grids):
        for r,row in enumerate(g):
            for c,v in enumerate(row):
                out[r0+r][c]=v
        r0 += len(g)
        if i < len(grids)-1:
            r0 += gap
    return out

def normalize_mask(g, color):
    cells=[(r,c) for r,row in enumerate(g) for c,v in enumerate(row) if v==color]
    r0,r1,c0,c1=bbox(cells)
    hh,ww=r1-r0+1,c1-c0+1
    out=blank(hh,ww)
    for r,c in cells:
        out[r-r0][c-c0]=1
    return out

def component_perimeter(cells):
    s=set(cells)
    per=0
    for r,c in s:
        for dr,dc in DIR4:
            if (r+dr,c+dc) not in s:
                per += 1
    return per

def hole_count_component(cells):
    # cells is iterable of coordinates in local or global space
    r0,r1,c0,c1=bbox(cells)
    hh,ww=r1-r0+1,c1-c0+1
    s={(r-r0,c-c0) for r,c in cells}
    vis=[[False]*ww for _ in range(hh)]
    holes=0
    for r in range(hh):
        for c in range(ww):
            if vis[r][c] or (r,c) in s:
                continue
            stack=[(r,c)]
            vis[r][c]=True
            touches=False
            while stack:
                rr,cc=stack.pop()
                if rr in (0,hh-1) or cc in (0,ww-1):
                    touches=True
                for dr,dc in DIR4:
                    nr,nc=rr+dr,cc+dc
                    if 0<=nr<hh and 0<=nc<ww and not vis[nr][nc] and (nr,nc) not in s:
                        vis[nr][nc]=True
                        stack.append((nr,nc))
            if not touches:
                holes += 1
    return holes

def recolor_mask(mask, color):
    return [[color if v else 0 for v in row] for row in mask]

def trim_zeros(g):
    h,w=size(g)
    cells=[(r,c) for r,row in enumerate(g) for c,v in enumerate(row) if v!=0]
    if not cells:
        return [[0]]
    return crop_to_cells(g, cells)

def top_row_nonzeros(g):
    return [v for v in g[0] if v!=0]

def rule_e22(g):
    starts=[(r,c) for r,row in enumerate(g) for c,v in enumerate(row) if v==2]
    return project_rays(g, starts, DIR4, stop_nonzero=True, paint=7, respect_original_nonzero=True)

def rule_e23(g):
    h,w=size(g)
    out=clone(g)
    for r in range(h):
        cols=[c for c,v in enumerate(g[r]) if v==1]
        if len(cols)==2:
            a,b=min(cols),max(cols)
            for c in range(a,b+1):
                out[r][c]=1
    return out

def rule_e24(g):
    h,w=size(g)
    out=clone(g)
    for r in range(h-1):
        for c in range(w-1):
            vals=[g[r][c], g[r][c+1], g[r+1][c], g[r+1][c+1]]
            nz=[v for v in vals if v!=0]
            if len(nz)==3 and len(set(nz))==1 and vals.count(0)==1:
                fill=nz[0]
                if vals[0]==0: out[r][c]=fill
                if vals[1]==0: out[r][c+1]=fill
                if vals[2]==0: out[r+1][c]=fill
                if vals[3]==0: out[r+1][c+1]=fill
    return out

def rule_e25(g):
    h,w=size(g)
    keep=[c for c in range(w) if any(g[r][c]!=0 for r in range(h))]
    return [[row[c] for c in keep] for row in g]

def rule_e26(g):
    h,w=size(g)
    # divider is full column of 5
    div=[c for c in range(w) if all(g[r][c]==5 for r in range(h))]
    assert len(div)==1
    d=div[0]
    out=clone(g)
    for r in range(h):
        for c in range(d):
            v=g[r][c]
            if v!=0 and v!=5:
                mc=2*d-c
                if 0<=mc<w and out[r][mc]==0:
                    out[r][mc]=v
    return out

def rule_e27(g):
    cells=[(r,c) for r,row in enumerate(g) for c,v in enumerate(row) if v==3]
    r0,r1,c0,c1=bbox(cells)
    out=blank(len(g),len(g[0]))
    for r in range(r0,r1+1):
        for c in range(c0,c1+1):
            out[r][c]=3
    return out

def rule_e28(g):
    vals=[]
    for r,row in enumerate(g):
        for c,v in enumerate(row):
            if v!=0:
                vals.append(v)
    return [vals]

def rule_m22(g):
    out=clone(g)
    comps=components_same_color(g, colors={1})
    for color,cells in comps:
        r0,r1,c0,c1=bbox(cells)
        # find seed inside bbox excluding frame cells
        seed=None
        for r in range(r0+1,r1):
            for c in range(c0+1,c1):
                if g[r][c]!=0 and g[r][c]!=1:
                    seed=g[r][c]
        assert seed is not None
        for r in range(r0+1,r1):
            for c in range(c0+1,c1):
                out[r][c]=seed
    return out

def rule_m23(g):
    rects=[]
    for color,cells in components_same_color(g):
        r0,r1,c0,c1=bbox(cells)
        area=len(cells)
        rect=[row[c0:c1+1] for row in g[r0:r1+1]]
        rects.append((area, r0, c0, rect))
    rects.sort(key=lambda t:(t[0], t[1], t[2]))
    return stack_horizontal([rect for _,_,_,rect in rects], gap=1)

def rule_m24(g):
    comps=components_nonzero(g, treat_colors_separately=False)
    comps.sort(key=lambda cells:(-len(cells), bbox(cells)[0], bbox(cells)[2]))
    return crop_to_cells(g, comps[0])

def rule_m25(g):
    starts=[(r,c) for r,row in enumerate(g) for c,v in enumerate(row) if v not in (0,1)]
    return project_rays(g, starts, DIR4, stop_colors={1}, paint='source', respect_original_nonzero=True)

def rule_m26(g):
    h,w=size(g)
    out=clone(g)
    pos=collections.defaultdict(list)
    for r,row in enumerate(g):
        for c,v in enumerate(row):
            if v!=0:
                pos[v].append((r,c))
    for color, cells in pos.items():
        if len(cells)==2:
            (r1,c1),(r2,c2)=cells
            if r1==r2:
                for c in range(min(c1,c2),max(c1,c2)+1):
                    out[r1][c]=color
            elif c1==c2:
                for r in range(min(r1,r2),max(r1,r2)+1):
                    out[r][c1]=color
    return out

def rule_m27(g):
    pts2=[(r,c) for r,row in enumerate(g) for c,v in enumerate(row) if v==2]
    pts3=[(r,c) for r,row in enumerate(g) for c,v in enumerate(row) if v==3]
    r02,r12,c02,c12=bbox(pts2)
    r03,r13,c03,c13=bbox(pts3)
    r0=max(r02,r03); r1=min(r12,r13); c0=max(c02,c03); c1=min(c12,c13)
    assert r0<=r1 and c0<=c1
    out=blank(r1-r0+1,c1-c0+1,8)
    return out

def rule_m28(g):
    cmd_map={2:0,3:1,4:2,5:3}
    cmd=g[0][0]
    cleaned=clone(g)
    cleaned[0][0]=0
    comps=components_nonzero(cleaned)
    comps.sort(key=lambda cells:(-len(cells), bbox(cells)[0], bbox(cells)[2]))
    obj=crop_to_cells(cleaned, comps[0])
    return rotate_k(obj, cmd_map[cmd])

def rule_h22(g):
    palette=top_row_nonzeros(g)
    mask_cells=[(r,c) for r,row in enumerate(g[1:], start=1) for c,v in enumerate(row) if v==1]
    mask_crop=normalize_mask(g, 1)
    copies=[recolor_mask(mask_crop, color) for color in palette]
    return stack_horizontal(copies, gap=1)

def rule_h23(g):
    comps=[cells for color,cells in components_same_color(g, colors={1})]
    comps.sort(key=lambda cells:(-(bbox(cells)[1]-bbox(cells)[0]+1)*(bbox(cells)[3]-bbox(cells)[2]+1), bbox(cells)[0], bbox(cells)[2]))
    out=blank(len(g), len(g[0]))
    for depth,cells in enumerate(comps, start=2):
        for r,c in cells:
            out[r][c]=depth
    return out

def rule_h24(g):
    comps=components_same_color(g, colors={2})
    comps.sort(key=lambda vcells: bbox(vcells[1])[2])  # left-to-right by min col
    vals=[]
    for color,cells in comps:
        hc=hole_count_component(cells)
        vals.append(hc+1)
    return [vals]

def rule_h25(g):
    h,w=size(g)
    sources=[(r,c,v) for r,row in enumerate(g) for c,v in enumerate(row) if v!=0]
    hit_colors=[[set() for _ in range(w)] for _ in range(h)]
    for r,c,color in sources:
        for dr,dc in DIR4:
            nr,nc=r+dr,c+dc
            while 0<=nr<h and 0<=nc<w and g[nr][nc]==0:
                hit_colors[nr][nc].add(color)
                nr += dr; nc += dc
    out=clone(g)
    for r in range(h):
        for c in range(w):
            if g[r][c]!=0:
                continue
            if len(hit_colors[r][c])==1:
                out[r][c]=next(iter(hit_colors[r][c]))
            elif len(hit_colors[r][c])>=2:
                out[r][c]=8
    return out

def rule_h26(g):
    comps=[]
    for color,cells in components_same_color(g):
        crop=crop_to_cells(g,cells)
        comps.append((component_perimeter(cells), bbox(cells)[0], bbox(cells)[2], crop))
    comps.sort(key=lambda t:(-t[0], t[1], t[2]))
    return stack_vertical([crop for _,_,_,crop in comps], gap=1)

def rule_h27(g):
    cmd_map={2:0,3:1,4:2,5:3}
    cmds=[v for v in g[0] if v in cmd_map]
    body=clone(g)
    body[0]=[0]*len(g[0])
    comps=components_nonzero(body)
    comps.sort(key=lambda cells:(-len(cells), bbox(cells)[0], bbox(cells)[2]))
    template=crop_to_cells(body, comps[0])
    copies=[rotate_k(template, cmd_map[v]) for v in cmds]
    return stack_horizontal(copies, gap=1)

def rule_h28(g):
    mask2=normalize_mask(g,2)
    mask3=normalize_mask(g,3)
    h=max(len(mask2), len(mask3))
    w=max(len(mask2[0]), len(mask3[0]))
    out=blank(h,w)
    for r in range(h):
        for c in range(w):
            a = r < len(mask2) and c < len(mask2[0]) and mask2[r][c]==1
            b = r < len(mask3) and c < len(mask3[0]) and mask3[r][c]==1
            out[r][c] = 8 if a ^ b else 0
    return trim_zeros(out)

RULES = {
    'E22': rule_e22,
    'E23': rule_e23,
    'E24': rule_e24,
    'E25': rule_e25,
    'E26': rule_e26,
    'E27': rule_e27,
    'E28': rule_e28,
    'M22': rule_m22,
    'M23': rule_m23,
    'M24': rule_m24,
    'M25': rule_m25,
    'M26': rule_m26,
    'M27': rule_m27,
    'M28': rule_m28,
    'H22': rule_h22,
    'H23': rule_h23,
    'H24': rule_h24,
    'H25': rule_h25,
    'H26': rule_h26,
    'H27': rule_h27,
    'H28': rule_h28,
}

SUMMARY = {'set': 4, 'puzzle_count': 21, 'train_pair_count': 71, 'avg_train_pairs': 3.38, 'difficulty_counts': {'easy': 7, 'medium': 7, 'hard': 7}, 'new_primitive': {'name': 'project_rays', 'purpose': 'Project colors in straight lines from source cells until a boundary or blocker.'}}

PUZZLES = [{'id': 'E22', 'title': 'Beacon Cross Rays', 'difficulty': 'easy', 'skills': ['projection', 'edge clipping', 'invented primitive'], 'staged_hint': 'Treat each 2 as a source. First ignore the target color and just reason about where straight rays should travel.', 'written_solution': 'Each red(2) source emits straight rays up, down, left, and right. The rays pass through zeros until the grid edge and paint those cells orange(7). The source cells themselves stay red(2).', 'uses_new_primitive': True, 'program_name': 'rule_e22', 'program_source': 'def rule_e22(g):\n    starts=[(r,c) for r,row in enumerate(g) for c,v in enumerate(row) if v==2]\n    return project_rays(g, starts, DIR4, stop_nonzero=True, paint=7, respect_original_nonzero=True)', 'train': [{'input': ['00000000', '00200000', '00000000', '00000000', '00000200', '00000000', '00000000'], 'output': ['00700700', '77277777', '00700700', '00700700', '77777277', '00700700', '00700700']}, {'input': ['000000000', '000000000', '000000200', '000000000', '000000000', '020000000', '000000020', '000000000'], 'output': ['070000770', '070000770', '777777277', '070000770', '070000770', '727777777', '777777727', '070000770']}, {'input': ['0000200000', '0000000000', '0000000000', '0000000020', '0000000000', '0000000000'], 'output': ['7777277777', '0000700070', '0000700070', '7777777727', '0000700070', '0000700070']}], 'test': {'input': ['000000000', '000000020', '000000000', '000000000', '002000000', '000000000', '000000000', '000002000', '000000000'], 'output': ['007007070', '777777727', '007007070', '007007070', '772777777', '007007070', '007007070', '777772777', '007007070']}}, {'id': 'E23', 'title': 'Row Bridge', 'difficulty': 'easy', 'skills': ['row intervals', 'endpoint reasoning', 'same-size fill'], 'staged_hint': 'Look row by row. The interesting rows are the ones with exactly two blue endpoints.', 'written_solution': 'Whenever a row contains exactly two blue(1) cells, fill the entire segment between them with blue(1), including the endpoints. Leave all other rows unchanged.', 'uses_new_primitive': False, 'program_name': 'rule_e23', 'program_source': 'def rule_e23(g):\n    h,w=size(g)\n    out=clone(g)\n    for r in range(h):\n        cols=[c for c,v in enumerate(g[r]) if v==1]\n        if len(cols)==2:\n            a,b=min(cols),max(cols)\n            for c in range(a,b+1):\n                out[r][c]=1\n    return out', 'train': [{'input': ['00000000', '01000100', '00000000', '00000000', '10000001', '00000000'], 'output': ['00000000', '01111100', '00000000', '00000000', '11111111', '00000000']}, {'input': ['001000100', '000000000', '000000000', '010010000', '000000000', '000000000', '000001001'], 'output': ['001111100', '000000000', '000000000', '011110000', '000000000', '000000000', '000001111']}, {'input': ['0000000000', '0000000000', '0001000001', '0000000000', '0100000100'], 'output': ['0000000000', '0000000000', '0001111111', '0000000000', '0111111100']}], 'test': {'input': ['0000000000', '1001000000', '0000000000', '0000100001', '0000000000', '0000000000', '0010000100', '0000000000'], 'output': ['0000000000', '1111000000', '0000000000', '0000111111', '0000000000', '0000000000', '0011111100', '0000000000']}}, {'id': 'E24', 'title': 'Missing Corner', 'difficulty': 'easy', 'skills': ['2x2 local pattern', 'completion', 'non-overlapping motifs'], 'staged_hint': 'Ignore most of the board. Zoom in on each 2×2 window and ask whether it is almost complete.', 'written_solution': 'In any 2×2 block that has three copies of the same nonzero color and one empty cell, fill the empty cell with that color. The examples are spaced so these local completions do not interfere with one another.', 'uses_new_primitive': False, 'program_name': 'rule_e24', 'program_source': 'def rule_e24(g):\n    h,w=size(g)\n    out=clone(g)\n    for r in range(h-1):\n        for c in range(w-1):\n            vals=[g[r][c], g[r][c+1], g[r+1][c], g[r+1][c+1]]\n            nz=[v for v in vals if v!=0]\n            if len(nz)==3 and len(set(nz))==1 and vals.count(0)==1:\n                fill=nz[0]\n                if vals[0]==0: out[r][c]=fill\n                if vals[1]==0: out[r][c+1]=fill\n                if vals[2]==0: out[r+1][c]=fill\n                if vals[3]==0: out[r+1][c+1]=fill\n    return out', 'train': [{'input': ['0000000', '0040000', '0440000', '0000000', '0000660', '0000600', '0000000'], 'output': ['0000000', '0440000', '0440000', '0000000', '0000660', '0000660', '0000000']}, {'input': ['000002200', '000000200', '000000000', '070000000', '077000000', '000000030', '000000330', '000000000'], 'output': ['000002200', '000002200', '000000000', '077000000', '077000000', '000000330', '000000330', '000000000']}, {'input': ['0000000000', '0088000000', '0080000000', '0000000550', '0000000050', '0000000000'], 'output': ['0000000000', '0088000000', '0088000000', '0000000550', '0000000550', '0000000000']}], 'test': {'input': ['000000000', '044000200', '040000220', '000000000', '000000000', '000070000', '000770000', '000000000', '000000000'], 'output': ['000000000', '044000220', '044000220', '000000000', '000000000', '000770000', '000770000', '000000000', '000000000']}}, {'id': 'E25', 'title': 'Keep the Live Columns', 'difficulty': 'easy', 'skills': ['column filtering', 'dynamic-size output', 'preserve row structure'], 'staged_hint': 'Instead of transforming cells, ask which whole columns matter at all.', 'written_solution': 'Delete every column that is entirely zero. Keep the remaining columns in their original left-to-right order and keep all rows unchanged, so the output is a thinner version of the input.', 'uses_new_primitive': False, 'program_name': 'rule_e25', 'program_source': 'def rule_e25(g):\n    h,w=size(g)\n    keep=[c for c in range(w) if any(g[r][c]!=0 for r in range(h))]\n    return [[row[c] for c in keep] for row in g]', 'train': [{'input': ['00000000', '02040000', '00000070', '00040000', '02000000'], 'output': ['000', '240', '007', '040', '200']}, {'input': ['300000002', '000000000', '300050000', '000050000', '000000000', '300000002'], 'output': ['302', '000', '350', '050', '000', '302']}, {'input': ['0000000', '0040000', '0040060', '0000060'], 'output': ['00', '40', '46', '06']}], 'test': {'input': ['0000000000', '2000000005', '0000300000', '0000300000', '0400007000', '0000000000'], 'output': ['00000', '20005', '00300', '00300', '04070', '00000']}}, {'id': 'E26', 'title': 'Divider Mirror', 'difficulty': 'easy', 'skills': ['reflection', 'symmetry', 'copy-preserve'], 'staged_hint': 'The column of 5s is a hinge. Only one side is populated at first.', 'written_solution': 'The full column of gray(5) cells is a mirror line. Copy every nonzero cell from the left side to the equally distant position on the right side, preserving its color. Keep the original left side and the divider unchanged.', 'uses_new_primitive': False, 'program_name': 'rule_e26', 'program_source': 'def rule_e26(g):\n    h,w=size(g)\n    # divider is full column of 5\n    div=[c for c in range(w) if all(g[r][c]==5 for r in range(h))]\n    assert len(div)==1\n    d=div[0]\n    out=clone(g)\n    for r in range(h):\n        for c in range(d):\n            v=g[r][c]\n            if v!=0 and v!=5:\n                mc=2*d-c\n                if 0<=mc<w and out[r][mc]==0:\n                    out[r][mc]=v\n    return out', 'train': [{'input': ['000050000', '020050000', '000350000', '000050000', '200050000', '004050000', '000050000'], 'output': ['000050000', '020050020', '000353000', '000050000', '200050002', '004050400', '000050000']}, {'input': ['07000500000', '00000500000', '00002500000', '30000500000', '00000500000', '00000500000', '00040500000', '00000500000'], 'output': ['07000500070', '00000500000', '00002520000', '30000500003', '00000500000', '00000500000', '00040504000', '00000500000']}, {'input': ['000050000', '600050000', '002050000', '000050000', '000850000', '000050000'], 'output': ['000050000', '600050006', '002050200', '000050000', '000858000', '000050000']}], 'test': {'input': ['0000005000000', '0020005000000', '0000045000000', '0000005000000', '7000005000000', '0000005000000', '0003005000000', '0800005000000', '0000005000000'], 'output': ['0000005000000', '0020005000200', '0000045400000', '0000005000000', '7000005000007', '0000005000000', '0003005003000', '0800005000080', '0000005000000']}}, {'id': 'E27', 'title': 'Solidify the Box', 'difficulty': 'easy', 'skills': ['bounding box', 'object abstraction', 'same-size transform'], 'staged_hint': 'Forget the exact scattered pattern and keep only its extreme rows and columns.', 'written_solution': 'Find all green(3) cells. Compute the smallest axis-aligned rectangle that contains them, then fill that entire rectangle with green(3). Everything else becomes black(0).', 'uses_new_primitive': False, 'program_name': 'rule_e27', 'program_source': 'def rule_e27(g):\n    cells=[(r,c) for r,row in enumerate(g) for c,v in enumerate(row) if v==3]\n    r0,r1,c0,c1=bbox(cells)\n    out=blank(len(g),len(g[0]))\n    for r in range(r0,r1+1):\n        for c in range(c0,c1+1):\n            out[r][c]=3\n    return out', 'train': [{'input': ['00000000', '03003000', '00000000', '00300000', '00000000', '00000000', '00000000'], 'output': ['00000000', '03333000', '03333000', '03333000', '00000000', '00000000', '00000000']}, {'input': ['000000000', '000000000', '000003000', '000000300', '000300000', '000000030', '000000000', '000000000'], 'output': ['000000000', '000000000', '000333330', '000333330', '000333330', '000333330', '000000000', '000000000']}, {'input': ['0030000000', '0000000000', '0000000030', '0000000000', '0000300000', '0000000000'], 'output': ['0033333330', '0033333330', '0033333330', '0033333330', '0033333330', '0000000000']}], 'test': {'input': ['000000000', '000000300', '000000000', '003000000', '000000000', '000000030', '000003000', '000000000', '000000000'], 'output': ['000000000', '003333330', '003333330', '003333330', '003333330', '003333330', '003333330', '000000000', '000000000']}}, {'id': 'E28', 'title': 'Readout Strip', 'difficulty': 'easy', 'skills': ['serialization', 'row-major order', 'dynamic-size output'], 'staged_hint': 'Do not preserve geometry. Preserve only the scan order of the colored cells.', 'written_solution': 'Read the nonzero cells in row-major order: top row to bottom row, and within each row left to right. Output a single row containing exactly those color values with no zeros between them.', 'uses_new_primitive': False, 'program_name': 'rule_e28', 'program_source': 'def rule_e28(g):\n    vals=[]\n    for r,row in enumerate(g):\n        for c,v in enumerate(row):\n            if v!=0:\n                vals.append(v)\n    return [vals]', 'train': [{'input': ['0002000', '0000000', '0400000', '0000000', '0000060', '0000000'], 'output': ['246']}, {'input': ['00000000', '00000070', '00000000', '00300500', '00000000', '00000000', '90000000'], 'output': ['7359']}, {'input': ['800000002', '000000000', '000060000', '000000000', '030000000'], 'output': ['8263']}], 'test': {'input': ['00000000', '04000020', '00000000', '00000000', '00070000', '00000000', '50000000', '00000008'], 'output': ['42758']}}, {'id': 'M22', 'title': 'Seeded Frames', 'difficulty': 'medium', 'skills': ['frame detection', 'containment', 'interior fill'], 'staged_hint': 'Treat each 1-frame as a container and ask what single clue inside tells you how to fill it.', 'written_solution': 'Each rectangular frame made of color 1 contains exactly one colored seed cell in its interior. Keep the frame itself, and fill the entire interior of that frame with the seed’s color.', 'uses_new_primitive': False, 'program_name': 'rule_m22', 'program_source': 'def rule_m22(g):\n    out=clone(g)\n    comps=components_same_color(g, colors={1})\n    for color,cells in comps:\n        r0,r1,c0,c1=bbox(cells)\n        # find seed inside bbox excluding frame cells\n        seed=None\n        for r in range(r0+1,r1):\n            for c in range(c0+1,c1):\n                if g[r][c]!=0 and g[r][c]!=1:\n                    seed=g[r][c]\n        assert seed is not None\n        for r in range(r0+1,r1):\n            for c in range(c0+1,c1):\n                out[r][c]=seed\n    return out', 'train': [{'input': ['000000000000', '011111000000', '010001011110', '010201014010', '011111010010', '000000010010', '000000011110', '000000000000', '000000000000'], 'output': ['000000000000', '011111000000', '012221011110', '012221014410', '011111014410', '000000014410', '000000011110', '000000000000', '000000000000']}, {'input': ['0000000000000', '0011111000000', '0010001000000', '0010001000000', '0010701001110', '0010001001310', '0011111001010', '0000000001110', '0000000000000', '0000000000000'], 'output': ['0000000000000', '0011111000000', '0017771000000', '0017771000000', '0017771001110', '0017771001310', '0011111001310', '0000000001110', '0000000000000', '0000000000000']}, {'input': ['11110000000', '10010000000', '16010011111', '10010010001', '11110010001', '00000010801', '00000010001', '00000011111'], 'output': ['11110000000', '16610000000', '16610011111', '16610018881', '11110018881', '00000018881', '00000018881', '00000011111']}], 'test': {'input': ['00000000000000', '01111110000000', '01000010011110', '01002010010010', '01000010010010', '01111110017010', '00000000010010', '00001111111110', '00001030100000', '00001000100000', '00001111100000'], 'output': ['00000000000000', '01111110000000', '01222210011110', '01222333333310', '01222333333310', '01111333333310', '00000333333310', '00001333333310', '00001333333300', '00001333333300', '00001111100000']}}, {'id': 'M23', 'title': 'Rectangle Sort', 'difficulty': 'medium', 'skills': ['components', 'area ranking', 'dynamic packing'], 'staged_hint': 'First isolate each solid rectangle. Only after that should you think about ordering them.', 'written_solution': 'Each nonzero component is a solid rectangle. Crop each rectangle to its own bounding box, sort the cropped rectangles by area from smallest to largest, and place them left-to-right with one blank column between consecutive pieces.', 'uses_new_primitive': False, 'program_name': 'rule_m23', 'program_source': 'def rule_m23(g):\n    rects=[]\n    for color,cells in components_same_color(g):\n        r0,r1,c0,c1=bbox(cells)\n        area=len(cells)\n        rect=[row[c0:c1+1] for row in g[r0:r1+1]]\n        rects.append((area, r0, c0, rect))\n    rects.sort(key=lambda t:(t[0], t[1], t[2]))\n    return stack_horizontal([rect for _,_,_,rect in rects], gap=1)', 'train': [{'input': ['000000033333', '022000000000', '022000000000', '000000000000', '000000000000', '000044400000', '000044400000', '000000000000', '000000000000', '000000000000'], 'output': ['220333330444', '220000000444']}, {'input': ['0000000066660', '0000000000000', '5500000000000', '5500000000000', '5500000000000', '0000000000000', '0000007777000', '0000007777000', '0000000000000', '0000000000000', '0000000000000'], 'output': ['666605507777', '000005507777', '000005500000']}, {'input': ['00000000000000', '00888880000000', '00888880000000', '00000000000000', '00000000044000', '22200000044000', '00000000044000', '00000000000000', '00000000000000'], 'output': ['222044088888', '000044088888', '000044000000']}], 'test': {'input': ['000000000033300', '022220000000000', '022220000000000', '000000000000000', '000000000000000', '000004440000000', '000004440000000', '000004440000000', '000000000000660', '000000000000660', '000000000000000', '000000000000000'], 'output': ['333066022220444', '000066022220444', '000000000000444']}}, {'id': 'M24', 'title': 'Largest Crop', 'difficulty': 'medium', 'skills': ['component size', 'cropping', 'shape preservation'], 'staged_hint': 'Ignore colors at first and ask which connected object simply has the most cells.', 'written_solution': 'Find the largest orthogonally connected nonzero component in the grid. Output that component cropped tightly to its own bounding box, preserving its exact shape and colors.', 'uses_new_primitive': False, 'program_name': 'rule_m24', 'program_source': 'def rule_m24(g):\n    comps=components_nonzero(g, treat_colors_separately=False)\n    comps.sort(key=lambda cells:(-len(cells), bbox(cells)[0], bbox(cells)[2]))\n    return crop_to_cells(g, comps[0])', 'train': [{'input': ['000000033330', '022000030000', '002000000000', '002200000000', '000000000000', '000044400000', '000044400000', '000004000000', '000000000000', '000000000000'], 'output': ['444', '444', '040']}, {'input': ['0000000000000', '5550000000000', '0500000000000', '0500000000000', '0000000660000', '0000000660000', '0000000660000', '0000000000000', '0070700000000', '0007000000000', '0000000000000'], 'output': ['66', '66', '66']}, {'input': ['02200000000000', '02200000000000', '02000000000000', '00000000333000', '00000000303000', '00000000333000', '00004400000000', '00000400000000', '00004400000000'], 'output': ['333', '303', '333']}], 'test': {'input': ['000000000000000', '002200000000000', '000220000000000', '000022000000000', '000000000033300', '000000000033300', '000000000030300', '000000000033300', '044000000000000', '044000000000000', '000000000000000', '000000000000000'], 'output': ['333', '333', '303', '333']}}, {'id': 'M25', 'title': 'Chamber Rays', 'difficulty': 'medium', 'skills': ['projection to blocker', 'frames', 'invented primitive'], 'staged_hint': 'Use the frame as the stopping condition. The sources do not move; they emit straight lines until the wall.', 'written_solution': 'Inside the rectangular wall of 1s, each colored source cell projects rays in the four cardinal directions. The rays keep the source’s own color and extend through zeros until just before they would hit the wall.', 'uses_new_primitive': True, 'program_name': 'rule_m25', 'program_source': "def rule_m25(g):\n    starts=[(r,c) for r,row in enumerate(g) for c,v in enumerate(row) if v not in (0,1)]\n    return project_rays(g, starts, DIR4, stop_colors={1}, paint='source', respect_original_nonzero=True)", 'train': [{'input': ['00000000000', '01111111110', '01000000010', '01020000010', '01000000010', '01000004010', '01000000010', '01111111110', '00000000000'], 'output': ['00000000000', '01111111110', '01020004010', '01222224210', '01020004010', '01444444410', '01020004010', '01111111110', '00000000000']}, {'input': ['000000000000', '001111111100', '001000000100', '001030000100', '001000000100', '001000000100', '001000060100', '001000000100', '001111111100', '000000000000'], 'output': ['000000000000', '001111111100', '001030060100', '001333363100', '001030060100', '001030060100', '001666666100', '001030060100', '001111111100', '000000000000']}, {'input': ['0111111110', '0100000010', '0102000010', '0100000010', '0100000010', '0100007010', '0100000010', '0111111110'], 'output': ['0111111110', '0102007010', '0122227210', '0102007010', '0102007010', '0177777710', '0102007010', '0111111110']}], 'test': {'input': ['0000000000000', '0111111111110', '0100000000010', '0102000000010', '0100000000010', '0100000004010', '0100000000010', '0100000000010', '0100007000010', '0111111111110', '0000000000000'], 'output': ['0000000000000', '0111111111110', '0102007004010', '0122227224210', '0102007004010', '0144447444410', '0102007004010', '0102007004010', '0177777777710', '0111111111110', '0000000000000']}}, {'id': 'M26', 'title': 'Pair Connectors', 'difficulty': 'medium', 'skills': ['same-color pairing', 'row/column reasoning', 'segment fill'], 'staged_hint': 'Group cells by color. Each color tells you which two endpoints belong together.', 'written_solution': 'Each nonzero color appears exactly twice. If the two copies lie in the same row, fill the horizontal segment between them; if they lie in the same column, fill the vertical segment between them. Keep the endpoints themselves.', 'uses_new_primitive': False, 'program_name': 'rule_m26', 'program_source': 'def rule_m26(g):\n    h,w=size(g)\n    out=clone(g)\n    pos=collections.defaultdict(list)\n    for r,row in enumerate(g):\n        for c,v in enumerate(row):\n            if v!=0:\n                pos[v].append((r,c))\n    for color, cells in pos.items():\n        if len(cells)==2:\n            (r1,c1),(r2,c2)=cells\n            if r1==r2:\n                for c in range(min(c1,c2),max(c1,c2)+1):\n                    out[r1][c]=color\n            elif c1==c2:\n                for r in range(min(r1,r2),max(r1,r2)+1):\n                    out[r][c1]=color\n    return out', 'train': [{'input': ['0000000000', '0200002000', '0000000030', '0000000000', '0000000000', '0040040000', '0000000030', '0000000000'], 'output': ['0000000000', '0222222000', '0000000030', '0000000030', '0000000030', '0044440030', '0000000030', '0000000000']}, {'input': ['00050000000', '00000000000', '00000000020', '00000000000', '00050000000', '00000000000', '07000007000', '00000000020', '00000000000'], 'output': ['00050000000', '00050000000', '00050000020', '00050000020', '00050000020', '00000000020', '07777777020', '00000000020', '00000000000']}, {'input': ['000000000000', '600060000000', '000000000000', '000000300000', '000000000000', '000000000000', '000000000000', '008000000800', '000000300000', '000000000000'], 'output': ['000000000000', '666660000000', '000000000000', '000000300000', '000000300000', '000000300000', '000000300000', '008888888800', '000000300000', '000000000000']}], 'test': {'input': ['0000000000000', '0000004000000', '0200000000200', '0000000000000', '3000000000000', '0000000000000', '0000000000000', '0000000000000', '0000004000000', '0007000000070', '3000000000000'], 'output': ['0000000000000', '0000004000000', '0222222222200', '0000004000000', '3000004000000', '3000004000000', '3000004000000', '3000004000000', '3000004000000', '3007777777770', '3000000000000']}}, {'id': 'M27', 'title': 'BBox Overlap', 'difficulty': 'medium', 'skills': ['bounding boxes', 'geometric intersection', 'dynamic-size output'], 'staged_hint': 'Do not compare the exact shapes. Compare the rectangles that contain them.', 'written_solution': 'Take the bounding box of all 2-cells and the bounding box of all 3-cells. Compute the overlap of those two rectangles. Output only that overlap region as a solid block of color 8, cropped to its own size.', 'uses_new_primitive': False, 'program_name': 'rule_m27', 'program_source': 'def rule_m27(g):\n    pts2=[(r,c) for r,row in enumerate(g) for c,v in enumerate(row) if v==2]\n    pts3=[(r,c) for r,row in enumerate(g) for c,v in enumerate(row) if v==3]\n    r02,r12,c02,c12=bbox(pts2)\n    r03,r13,c03,c13=bbox(pts3)\n    r0=max(r02,r03); r1=min(r12,r13); c0=max(c02,c03); c1=min(c12,c13)\n    assert r0<=r1 and c0<=c1\n    out=blank(r1-r0+1,c1-c0+1,8)\n    return out', 'train': [{'input': ['0000000000', '0200200000', '0000000000', '0003000000', '0020000300', '0000000000', '0003000000', '0000000000'], 'output': ['88', '88']}, {'input': ['00000200000', '00000000000', '00003000000', '00200000000', '00000000030', '00000020000', '00000000000', '00003000000', '00000000000'], 'output': ['888', '888', '888', '888']}, {'input': ['000000000000', '000000000000', '020000200000', '000000000000', '000030000000', '000000000000', '000000000300', '000200000000', '000030000000', '000000000000'], 'output': ['888', '888', '888', '888']}], 'test': {'input': ['0000000000000', '0020000020000', '0000000000000', '0000000000000', '0000003000000', '0000000000000', '0000000000030', '0000000000000', '0000020000000', '0000003000000', '0000000000000'], 'output': ['888', '888', '888', '888', '888']}}, {'id': 'M28', 'title': 'Marker Rotation Crop', 'difficulty': 'medium', 'skills': ['command decoding', 'cropping', 'rotation'], 'staged_hint': 'Separate the tiny command cell from the real object. The object is the larger nonzero component.', 'written_solution': 'A single command color specifies how to rotate the main object after cropping it to its bounding box: 2 means no rotation, 3 means rotate 90° clockwise, 4 means 180°, and 5 means 270° clockwise. The command cell itself does not appear in the output.', 'uses_new_primitive': False, 'program_name': 'rule_m28', 'program_source': 'def rule_m28(g):\n    cmd_map={2:0,3:1,4:2,5:3}\n    cmd=g[0][0]\n    cleaned=clone(g)\n    cleaned[0][0]=0\n    comps=components_nonzero(cleaned)\n    comps.sort(key=lambda cells:(-len(cells), bbox(cells)[0], bbox(cells)[2]))\n    obj=crop_to_cells(cleaned, comps[0])\n    return rotate_k(obj, cmd_map[cmd])', 'train': [{'input': ['200000000', '000000000', '000600000', '000667000', '000070000', '000000000', '000000000'], 'output': ['600', '667', '070']}, {'input': ['3000000000', '0000000000', '0000000000', '0000880000', '0000008000', '0000555000', '0000000000', '0000000000'], 'output': ['50', '50', '58']}, {'input': ['4000000000', '0000000000', '0000090000', '0000099000', '0000000900', '0000000000', '0000000000'], 'output': ['99', '09']}, {'input': ['500000000', '000000000', '000000000', '004400000', '004040000', '004440000', '000000000', '000000000'], 'output': ['044', '404', '444']}], 'test': {'input': ['50000000000', '00000000000', '00000000000', '00000000000', '00000220000', '00000202000', '00000222900', '00000000000', '00000000000'], 'output': ['009', '022', '202', '222']}}, {'id': 'H22', 'title': 'Palette Mask Multiplication', 'difficulty': 'hard', 'skills': ['legend decoding', 'mask extraction', 'dynamic templating'], 'staged_hint': 'Read the top row as a sequence of colors. Then forget their geometry and focus on the 1-mask below.', 'written_solution': 'The top row gives a palette order. Elsewhere in the grid there is a single mask made of 1s. Crop that mask to its bounding box, then repeat it once for each palette color, recoloring the mask with that color and arranging the copies left-to-right with one blank column between them.', 'uses_new_primitive': False, 'program_name': 'rule_h22', 'program_source': 'def rule_h22(g):\n    palette=top_row_nonzeros(g)\n    mask_cells=[(r,c) for r,row in enumerate(g[1:], start=1) for c,v in enumerate(row) if v==1]\n    mask_crop=normalize_mask(g, 1)\n    copies=[recolor_mask(mask_crop, color) for color in palette]\n    return stack_horizontal(copies, gap=1)', 'train': [{'input': ['204060000', '000000000', '001100000', '000100000', '000110000', '000000000', '000000000'], 'output': ['22004400660', '02000400060', '02200440066']}, {'input': ['7030000000', '0000000000', '0000000000', '0000100000', '0000111000', '0000001000', '0000000000', '0000000000'], 'output': ['7000300', '7770333', '0070003']}, {'input': ['508020600000', '000000000000', '000001110000', '000000010000', '000000110000', '000000000000', '000000000000', '000000000000', '000000000000'], 'output': ['555088802220666', '005000800020006', '055008800220066']}, {'input': ['40903000000', '00000000000', '00000001000', '00000011100', '00000001000', '00000000000', '00000000000'], 'output': ['04000900030', '44409990333', '04000900030']}], 'test': {'input': ['2050708000000', '0000000000000', '0000000000000', '0001010000000', '0001110000000', '0001000000000', '0000000000000', '0000000000000', '0000000000000'], 'output': ['202050507070808', '222055507770888', '200050007000800']}}, {'id': 'H23', 'title': 'Nested Depth Paint', 'difficulty': 'hard', 'skills': ['nested frames', 'depth reasoning', 'same-size recolor'], 'staged_hint': 'Think in layers from outside to inside. The exact frame color in the input stops mattering after you identify the depth order.', 'written_solution': 'Every nonzero object is a rectangular frame of color 1 nested inside larger frames. Recolor the outermost frame to 2, the next frame to 3, then 4, then 5, and so on as depth increases inward.', 'uses_new_primitive': False, 'program_name': 'rule_h23', 'program_source': 'def rule_h23(g):\n    comps=[cells for color,cells in components_same_color(g, colors={1})]\n    comps.sort(key=lambda cells:(-(bbox(cells)[1]-bbox(cells)[0]+1)*(bbox(cells)[3]-bbox(cells)[2]+1), bbox(cells)[0], bbox(cells)[2]))\n    out=blank(len(g), len(g[0]))\n    for depth,cells in enumerate(comps, start=2):\n        for r,c in cells:\n            out[r][c]=depth\n    return out', 'train': [{'input': ['111111111', '100000001', '101111101', '101000101', '101000101', '101000101', '101111101', '100000001', '111111111'], 'output': ['222222222', '200000002', '203333302', '203000302', '203000302', '203000302', '203333302', '200000002', '222222222']}, {'input': ['1111111111111', '1000000000001', '1011111111101', '1010000000101', '1010111110101', '1010100010101', '1010100010101', '1010100010101', '1010111110101', '1010000000101', '1011111111101', '1000000000001', '1111111111111'], 'output': ['2222222222222', '2000000000002', '2033333333302', '2030000000302', '2030444440302', '2030400040302', '2030400040302', '2030400040302', '2030444440302', '2030000000302', '2033333333302', '2000000000002', '2222222222222']}, {'input': ['01111111111110', '01000000000010', '01011111111010', '01010000001010', '01010000001010', '01010000001010', '01010000001010', '01011111111010', '01000000000010', '01111111111110'], 'output': ['02222222222220', '02000000000020', '02033333333020', '02030000003020', '02030000003020', '02030000003020', '02030000003020', '02033333333020', '02000000000020', '02222222222220']}, {'input': ['111111111111111', '100000000000001', '101111111111101', '101000000000101', '101011111110101', '101010000010101', '101010111010101', '101010101010101', '101010111010101', '101010000010101', '101011111110101', '101000000000101', '101111111111101', '100000000000001', '111111111111111'], 'output': ['222222222222222', '200000000000002', '203333333333302', '203000000000302', '203044444440302', '203040000040302', '203040555040302', '203040505040302', '203040555040302', '203040000040302', '203044444440302', '203000000000302', '203333333333302', '200000000000002', '222222222222222']}], 'test': {'input': ['11111111111111111', '10000000000000001', '10111111111111101', '10100000000000101', '10101111111110101', '10101000000010101', '10101011111010101', '10101010001010101', '10101010001010101', '10101010001010101', '10101011111010101', '10101000000010101', '10101111111110101', '10100000000000101', '10111111111111101', '10000000000000001', '11111111111111111'], 'output': ['22222222222222222', '20000000000000002', '20333333333333302', '20300000000000302', '20304444444440302', '20304000000040302', '20304055555040302', '20304050005040302', '20304050005040302', '20304050005040302', '20304055555040302', '20304000000040302', '20304444444440302', '20300000000000302', '20333333333333302', '20000000000000002', '22222222222222222']}}, {'id': 'H24', 'title': 'Hole Histogram', 'difficulty': 'hard', 'skills': ['topology', 'component analysis', 'dynamic summary'], 'staged_hint': 'Do not compare component sizes first. Compare how many enclosed empty regions each component contains.', 'written_solution': 'Read the connected color-2 objects from left to right. For each object, count how many holes are enclosed inside it. Output a single row where each entry is hole-count plus one: solid objects become 1, one-hole objects become 2, two-hole objects become 3, and so on.', 'uses_new_primitive': False, 'program_name': 'rule_h24', 'program_source': 'def rule_h24(g):\n    comps=components_same_color(g, colors={2})\n    comps.sort(key=lambda vcells: bbox(vcells[1])[2])  # left-to-right by min col\n    vals=[]\n    for color,cells in comps:\n        hc=hole_count_component(cells)\n        vals.append(hc+1)\n    return [vals]', 'train': [{'input': ['0000000000022222', '0220002220020002', '0220002020022222', '0000002220020002', '0000000000022222', '0000000000000000', '0000000000000000', '0000000000000000'], 'output': ['123']}, {'input': ['000000000000000000', '000000002200222220', '222220002200200020', '200020000000222220', '222220000000200020', '200020000000222220', '222220000000200020', '000000000000222220', '000000000000000000', '000000000000000000'], 'output': ['314']}, {'input': ['022200000000000', '020200000000000', '022200000000000', '000000022222000', '000000020002000', '000000022222022', '000000020002022', '000000022222000', '000000000000000'], 'output': ['231']}, {'input': ['00000000000000000000', '00000000002220000000', '02222200002020000000', '02000200002220000000', '02222200000000000000', '02000200000000000000', '02222200000000022000', '02000200000000022000', '02222200000000000000', '00000000000000000000', '00000000000000000000', '00000000000000000000'], 'output': ['421']}], 'test': {'input': ['0000000022222000000000', '2222200020002000000000', '2000200022222000000000', '2222200020002000000000', '2000200022222000222000', '2222200020002000202000', '0000000022222000222000', '0000000000000000000000', '0000000000000000000220', '0000000000000000000220', '0000000000000000000000', '0000000000000000000000'], 'output': ['3421']}}, {'id': 'H25', 'title': 'Ray Clash Grid', 'difficulty': 'hard', 'skills': ['projection overlap', 'conflict resolution', 'invented primitive'], 'staged_hint': 'First imagine each source painting its own row-and-column rays. Only after that should you resolve collisions.', 'written_solution': 'Every nonzero source projects rays up, down, left, and right through empty space until the boundary. Empty cells reached by exactly one source take that source’s color. Empty cells reached by two or more different source colors become cyan(8). Original source cells stay unchanged.', 'uses_new_primitive': True, 'program_name': 'rule_h25', 'program_source': 'def rule_h25(g):\n    h,w=size(g)\n    sources=[(r,c,v) for r,row in enumerate(g) for c,v in enumerate(row) if v!=0]\n    hit_colors=[[set() for _ in range(w)] for _ in range(h)]\n    for r,c,color in sources:\n        for dr,dc in DIR4:\n            nr,nc=r+dr,c+dc\n            while 0<=nr<h and 0<=nc<w and g[nr][nc]==0:\n                hit_colors[nr][nc].add(color)\n                nr += dr; nc += dc\n    out=clone(g)\n    for r in range(h):\n        for c in range(w):\n            if g[r][c]!=0:\n                continue\n            if len(hit_colors[r][c])==1:\n                out[r][c]=next(iter(hit_colors[r][c]))\n            elif len(hit_colors[r][c])>=2:\n                out[r][c]=8\n    return out', 'train': [{'input': ['000000000', '000200000', '000000000', '000000000', '030000000', '000000000', '000000000'], 'output': ['030200000', '282222222', '030200000', '030200000', '333833333', '030200000', '030200000']}, {'input': ['0000000000', '0000000400', '0000000000', '0000000000', '0000000000', '0020000000', '0000000030', '0000000000'], 'output': ['0020000430', '4484444484', '0020000430', '0020000430', '0020000430', '2222222882', '3383333833', '0020000430']}, {'input': ['000000000', '000000000', '005000000', '000000000', '000000000', '000000000', '000007000', '000000000', '000000000'], 'output': ['005007000', '005007000', '555558555', '005007000', '005007000', '005007000', '778777777', '005007000', '005007000']}, {'input': ['00000000000', '00002000000', '00000000000', '00000000000', '00000000300', '00000000000', '00000000000', '04000000000', '00000000000', '00000000000'], 'output': ['04002000300', '28222222822', '04002000300', '04002000300', '38338333333', '04002000300', '04002000300', '44448444844', '04002000300', '04002000300']}], 'test': {'input': ['00000000000', '00000000200', '00000000000', '00000000000', '00000000000', '00300000000', '00000000000', '00000000000', '00000040000', '00000000000', '00000000000'], 'output': ['00300040200', '22822282222', '00300040200', '00300040200', '00300040200', '33333383833', '00300040200', '00300040200', '44844444844', '00300040200', '00300040200']}}, {'id': 'H26', 'title': 'Perimeter Sort', 'difficulty': 'hard', 'skills': ['shape perimeter', 'component ranking', 'vertical packing'], 'staged_hint': 'Area is a distraction here. Rank the pieces by how much boundary they expose.', 'written_solution': 'Crop each connected nonzero component to its bounding box. Compute its orthogonal perimeter, sort the cropped pieces from largest perimeter to smallest, and stack them top-to-bottom with one blank row between pieces.', 'uses_new_primitive': False, 'program_name': 'rule_h26', 'program_source': 'def rule_h26(g):\n    comps=[]\n    for color,cells in components_same_color(g):\n        crop=crop_to_cells(g,cells)\n        comps.append((component_perimeter(cells), bbox(cells)[0], bbox(cells)[2], crop))\n    comps.sort(key=lambda t:(-t[0], t[1], t[2]))\n    return stack_vertical([crop for _,_,_,crop in comps], gap=1)', 'train': [{'input': ['000000000555000', '080080000505000', '080080000555000', '088880000000000', '000000000000000', '000000000000000', '000033300000000', '000033300000000', '000000000000000', '000000000000000'], 'output': ['8008', '8008', '8888', '0000', '5550', '5050', '5550', '0000', '3330', '3330']}, {'input': ['0000000000000000', '4000000000000000', '4000000008008000', '4440000008008000', '0000000008888000', '0000000000000000', '0000000000000000', '0000002200000000', '0000002200000000', '0000000000000000', '0000000000000000'], 'output': ['8008', '8008', '8888', '0000', '4000', '4000', '4440', '0000', '2200', '2200']}, {'input': ['00555000000000', '00505000000000', '00555000000000', '00000000000000', '00000000000000', '33300000000000', '33300000000000', '00000000040000', '00000000040000', '00000000044400', '00000000000000', '00000000000000'], 'output': ['555', '505', '555', '000', '400', '400', '444', '000', '333', '333']}, {'input': ['00000000400000000', '02200000400000000', '02200000444000000', '00000000000000000', '00000000000000000', '00000000000080080', '00000333000080080', '00000333000088880', '00000000000000000', '00000000000000000'], 'output': ['8008', '8008', '8888', '0000', '4000', '4000', '4440', '0000', '3330', '3330', '0000', '2200', '2200']}], 'test': {'input': ['000000000000000000', '055500000000000000', '050500008008000000', '055500008008000000', '000000008888000000', '000000000000000000', '000000000000000000', '000000000000400000', '002200000000400000', '002200000000444000', '000000000000000000', '000000000000000000', '000000000000000000'], 'output': ['8008', '8008', '8888', '0000', '5550', '5050', '5550', '0000', '4000', '4000', '4440', '0000', '2200', '2200']}}, {'id': 'H27', 'title': 'Command-Rotated Template Strip', 'difficulty': 'hard', 'skills': ['command legend', 'template reuse', 'rotation sequence'], 'staged_hint': 'Read the top row as instructions, not as part of the object. Then isolate the one real template below.', 'written_solution': 'The top row contains rotation commands in order: 2 means keep the template as-is, 3 means rotate it 90° clockwise, 4 means 180°, and 5 means 270° clockwise. Crop the single template component below, apply those rotations in command order, and place the resulting copies left-to-right with one blank column between them.', 'uses_new_primitive': False, 'program_name': 'rule_h27', 'program_source': 'def rule_h27(g):\n    cmd_map={2:0,3:1,4:2,5:3}\n    cmds=[v for v in g[0] if v in cmd_map]\n    body=clone(g)\n    body[0]=[0]*len(g[0])\n    comps=components_nonzero(body)\n    comps.sort(key=lambda cells:(-len(cells), bbox(cells)[0], bbox(cells)[2]))\n    template=crop_to_cells(body, comps[0])\n    copies=[rotate_k(template, cmd_map[v]) for v in cmds]\n    return stack_horizontal(copies, gap=1)', 'train': [{'input': ['203050000000', '000000000000', '000000220000', '000000020000', '000000077000', '000000000000', '000000000000', '000000000000'], 'output': ['22000020007', '02007220227', '07707000200']}, {'input': ['4020000000000', '0000000000000', '0000000000000', '0000066000000', '0000006900000', '0000000900000', '0000000000000', '0000000000000', '0000000000000'], 'output': ['9000660', '9600069', '0660009']}, {'input': ['50304000000000', '00000000000000', '00000000000000', '00000000000000', '00000008000000', '00000008880000', '00000000088000', '00000000000000', '00000000000000', '00000000000000'], 'output': ['008008808800', '088008000888', '080088000008', '880080000000']}, {'input': ['30302050000', '00000000000', '00005500000', '00000500000', '00005550000', '00000000000', '00000000000', '00000000000'], 'output': ['505050505500005', '555055500500555', '500050005550505']}], 'test': {'input': ['502040300000000', '000000000000000', '000000000000000', '000000000000000', '000000220000000', '000000020700000', '000000007700000', '000000000000000', '000000000000000', '000000000000000'], 'output': ['22022020002', '20002022022']}}, {'id': 'H28', 'title': 'Normalized XOR', 'difficulty': 'hard', 'skills': ['shape normalization', 'boolean composition', 'dynamic-size output'], 'staged_hint': 'Crop the two objects separately before you compare them. Their original positions are irrelevant.', 'written_solution': 'Take the color-2 object and the color-3 object, crop each one to its own bounding box, and align those two cropped occupancy masks at the top-left corner of a common canvas. Mark color 8 wherever exactly one mask has a filled cell, 0 where both masks agree, and then crop the result to its nonzero bounding box.', 'uses_new_primitive': False, 'program_name': 'rule_h28', 'program_source': 'def rule_h28(g):\n    mask2=normalize_mask(g,2)\n    mask3=normalize_mask(g,3)\n    h=max(len(mask2), len(mask3))\n    w=max(len(mask2[0]), len(mask3[0]))\n    out=blank(h,w)\n    for r in range(h):\n        for c in range(w):\n            a = r < len(mask2) and c < len(mask2[0]) and mask2[r][c]==1\n            b = r < len(mask3) and c < len(mask3[0]) and mask3[r][c]==1\n            out[r][c] = 8 if a ^ b else 0\n    return trim_zeros(out)', 'train': [{'input': ['000000000000', '022000000000', '020000003300', '022000003300', '000000000000', '000000000000', '000000000000', '000000000000'], 'output': ['08', '88']}, {'input': ['0022200000000', '0002000000000', '0002000000000', '0000000000000', '0000000000330', '0000000003300', '0000000003000', '0000000000000', '0000000000000'], 'output': ['80', '80', '88']}, {'input': ['00000000000000', '00000000000000', '02220000000000', '02020000000000', '02220000000000', '00000000033300', '00000000003000', '00000000003000', '00000000000000', '00000000000000'], 'output': ['888', '808']}, {'input': ['000000000000000', '000220000000000', '000022000000000', '000002000000000', '000000000000000', '000000000000000', '000000000033000', '000000000030000', '000000000033300', '000000000000000', '000000000000000'], 'output': ['888', '880']}], 'test': {'input': ['0000000000000000', '0000000000000000', '0022200000000000', '0000200000000000', '0022200000000000', '0000000000000000', '0000000000003300', '0000000000033300', '0000000000030000', '0000000000000000', '0000000000000000', '0000000000000000'], 'output': ['800', '880', '088']}}]

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
    payload = {
        "set": SUMMARY["set"],
        "summary": SUMMARY,
        "puzzles": PUZZLES,
    }
    Path(path).write_text(json.dumps(payload, indent=2))

if __name__ == "__main__":
    issues = validate()
    if issues:
        print(f"Validation failed: {len(issues)} mismatches")
        for item in issues[:10]:
            print(item[0], item[1])
        raise SystemExit(1)
    print(f"Validated {len(PUZZLES)} puzzles ({SUMMARY['train_pair_count']} train pairs).")
