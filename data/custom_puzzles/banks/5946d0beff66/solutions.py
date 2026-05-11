
from __future__ import annotations

import collections
import inspect
import json
from pathlib import Path

DIR4=[(-1,0),(1,0),(0,-1),(0,1)]

def blank(h,w,val=0):
    return [[val]*w for _ in range(h)]

def clone(g):
    return [row[:] for row in g]

def size(g):
    return len(g), len(g[0]) if g else 0

def strings_from_grid(g):
    return ["".join(str(c) for c in row) for row in g]

def bbox(cells):
    rs=[r for r,c in cells]; cs=[c for r,c in cells]
    return min(rs), min(cs), max(rs), max(cs)

def add_cells(g, cells):
    for r,c,v in cells:
        g[r][c]=v
    return g

def add_pattern(g, top, left, pattern):
    for r,row in enumerate(pattern):
        for c,v in enumerate(row):
            if isinstance(v,str):
                v=int(v)
            if v!=0:
                g[top+r][left+c]=v
    return g

def draw_rect_border(g,r0,c0,r1,c1,color):
    for c in range(c0,c1+1):
        g[r0][c]=color; g[r1][c]=color
    for r in range(r0,r1+1):
        g[r][c0]=color; g[r][c1]=color

def fill_rect(g,r0,c0,r1,c1,color):
    for r in range(r0,r1+1):
        for c in range(c0,c1+1):
            g[r][c]=color

def orth_neighbors(r,c,h,w):
    for dr,dc in DIR4:
        nr,nc=r+dr,c+dc
        if 0<=nr<h and 0<=nc<w:
            yield nr,nc

def components_nonzero(g, treat_colors_separately=False, exclude=None):
    h,w=size(g)
    ex=set(exclude or [])
    vis=[[False]*w for _ in range(h)]
    comps=[]
    for r in range(h):
        for c in range(w):
            if vis[r][c] or g[r][c]==0 or (r,c) in ex:
                continue
            color=g[r][c]
            vis[r][c]=True
            q=[(r,c)]
            cells=[]
            while q:
                rr,cc=q.pop()
                cells.append((rr,cc))
                for nr,nc in orth_neighbors(rr,cc,h,w):
                    if vis[nr][nc] or (nr,nc) in ex or g[nr][nc]==0:
                        continue
                    if treat_colors_separately and g[nr][nc]!=color:
                        continue
                    vis[nr][nc]=True
                    q.append((nr,nc))
            comps.append((color,cells))
    return comps

def crop_bbox(g, cells=None):
    if cells is None:
        cells=[(r,c) for r,row in enumerate(g) for c,v in enumerate(row) if v!=0]
    if not cells:
        return [[0]]
    r0,c0,r1,c1=bbox(cells)
    return [row[c0:c1+1] for row in g[r0:r1+1]]

def grid_from_component(g, cells, recolor=None):
    r0,c0,r1,c1=bbox(cells)
    out=blank(r1-r0+1, c1-c0+1)
    for r,c in cells:
        out[r-r0][c-c0]=g[r][c] if recolor is None else recolor
    return out

def rotate_cw(g):
    h,w=size(g)
    return [[g[h-1-r][c] for r in range(h)] for c in range(w)]

def rotate_times(g, k):
    k%=4
    out=g
    for _ in range(k):
        out=rotate_cw(out)
    return out

def flip_h(g):
    return g[::-1]

def flip_v(g):
    return [row[::-1] for row in g]

def pad_to_height(g, H):
    h,w=size(g)
    out=blank(H,w)
    for r in range(h):
        for c in range(w):
            out[r][c]=g[r][c]
    return out

def pack_horiz(grids, sep=1):
    H=max(size(g)[0] for g in grids)
    widths=[size(g)[1] for g in grids]
    W=sum(widths)+sep*(len(grids)-1)
    out=blank(H,W)
    c0=0
    for idx,g in enumerate(grids):
        h,w=size(g)
        for r in range(h):
            for c in range(w):
                out[r][c0+c]=g[r][c]
        c0+=w+sep
    return out

def find_unique(g, val):
    pts=[(r,c) for r,row in enumerate(g) for c,v in enumerate(row) if v==val]
    if len(pts)!=1:
        raise ValueError((val, pts))
    return pts[0]

# new primitive
def orbit_cells(base_grid, cells, pivot, turns=(0,1,2,3), keep_original=True, recolor_by_turn=None):
    out=clone(base_grid)
    h,w=size(out)
    pr,pc=pivot
    if not keep_original:
        for r,c,_ in cells:
            if 0<=r<h and 0<=c<w:
                out[r][c]=0
    for t in turns:
        for r,c,v in cells:
            dr,dc=r-pr,c-pc
            if t==0:
                nr,nc=pr+dr,pc+dc
            elif t==1:
                nr,nc=pr+dc,pc-dr
            elif t==2:
                nr,nc=pr-dr,pc-dc
            elif t==3:
                nr,nc=pr-dc,pc+dr
            else:
                raise ValueError(t)
            if 0<=nr<h and 0<=nc<w:
                nv = recolor_by_turn[t] if recolor_by_turn and t in recolor_by_turn else v
                out[nr][nc]=nv
    return out

def fill_holes_selected(g, target):
    h,w=size(g)
    out=clone(g)
    for color,cells in components_nonzero(g, treat_colors_separately=True):
        if color!=target:
            continue
        r0,c0,r1,c1=bbox(cells)
        H,W=r1-r0+1,c1-c0+1
        mask=[[0]*W for _ in range(H)]
        for r,c in cells:
            mask[r-r0][c-c0]=1
        vis=[[False]*W for _ in range(H)]
        from collections import deque
        dq=deque()
        for r in range(H):
            for c in range(W):
                if r in (0,H-1) or c in (0,W-1):
                    if mask[r][c]==0 and not vis[r][c]:
                        vis[r][c]=True
                        dq.append((r,c))
        while dq:
            r,c=dq.popleft()
            for nr,nc in orth_neighbors(r,c,H,W):
                if not vis[nr][nc] and mask[nr][nc]==0:
                    vis[nr][nc]=True
                    dq.append((nr,nc))
        for r in range(H):
            for c in range(W):
                if mask[r][c]==0 and not vis[r][c]:
                    out[r0+r][c0+c]=target
    return out

def is_rect_border(cells):
    r0,c0,r1,c1=bbox(cells)
    if r1-r0<2 or c1-c0<2:
        return False
    expected=set()
    for c in range(c0,c1+1):
        expected.add((r0,c)); expected.add((r1,c))
    for r in range(r0,r1+1):
        expected.add((r,c0)); expected.add((r,c1))
    return set(cells)==expected

def frame_info_by_color(g, color):
    infos=[]
    for col,cells in components_nonzero(g, treat_colors_separately=True):
        if col==color and is_rect_border(cells):
            infos.append((bbox(cells), cells))
    return infos

def subgrid(g, r0,c0,r1,c1):
    return [row[c0:c1+1] for row in g[r0:r1+1]]

def count_area(cells):
    return len(cells)

def component_top_left(cells):
    r0,c0,r1,c1=bbox(cells)
    return r0,c0

# rules
def rule_e57(g):
    pivot=find_unique(g,5)
    cells=[(r,c,v) for r,row in enumerate(g) for c,v in enumerate(row) if v not in (0,5)]
    return orbit_cells(g, cells, pivot, turns=(0,1,2,3), keep_original=True)

def rule_e58(g):
    out=clone(g)
    by=collections.defaultdict(list)
    for r,row in enumerate(g):
        for c,v in enumerate(row):
            if v!=0:
                by[v].append((r,c))
    for color,pts in by.items():
        if len(pts)!=2:
            continue
        (r1,c1),(r2,c2)=pts
        dr=r2-r1; dc=c2-c1
        if abs(dr)!=abs(dc):
            continue
        sr=0 if dr==0 else (1 if dr>0 else -1)
        sc=0 if dc==0 else (1 if dc>0 else -1)
        steps=abs(dr)
        for k in range(steps+1):
            out[r1+k*sr][c1+k*sc]=color
    return out

def rule_e59(g):
    h,w=size(g)
    out=blank(h,w)
    for r,row in enumerate(g):
        for c,v in enumerate(row):
            if v!=0:
                out[r][c]=v
                for nr,nc in orth_neighbors(r,c,h,w):
                    out[nr][nc]=v
    return out

def rule_e60(g):
    out=blank(*size(g))
    by=collections.defaultdict(list)
    for r,row in enumerate(g):
        for c,v in enumerate(row):
            if v!=0:
                by[v].append((r,c))
    for color,pts in by.items():
        if len(pts)!=4:
            continue
        rs=sorted(set(r for r,c in pts)); cs=sorted(set(c for r,c in pts))
        if len(rs)==2 and len(cs)==2 and set(pts)=={(rs[0],cs[0]),(rs[0],cs[1]),(rs[1],cs[0]),(rs[1],cs[1])}:
            draw_rect_border(out, rs[0], cs[0], rs[1], cs[1], color)
    return out

def rule_e61(g):
    counts=collections.Counter(v for row in g for v in row if v!=0)
    col=[]
    for color in sorted(counts):
        col.extend([color]*counts[color])
    return [[v] for v in col] if col else [[0]]

def rule_e62(g):
    cols=[c for c,v in enumerate(g[0]) if v==8]
    if not cols:
        return [[0]]
    return [[row[c] for c in cols] for row in g[1:]]

def rule_e63(g):
    comps=components_nonzero(g, treat_colors_separately=True)
    comps.sort(key=lambda t:(-len(t[1]), t[0], component_top_left(t[1])))
    color,cells=comps[0]
    return crop_bbox(g, cells)

def rule_m57(g):
    target=g[0][0]
    pivot=find_unique(g,5)
    cells=[(r,c,v) for r,row in enumerate(g) for c,v in enumerate(row) if v==target and (r,c)!=(0,0)]
    return orbit_cells(g, cells, pivot, turns=(0,1,2,3), keep_original=True)

def rule_m58(g):
    rows=[r for r in range(1,len(g)) if g[r][0]==8]
    cols=[c for c in range(1,len(g[0])) if g[0][c]==8]
    if not rows or not cols:
        return [[0]]
    return [[g[r][c] for c in cols] for r in rows]

def rule_m59(g):
    k=g[0][0]
    comps=components_nonzero(g, treat_colors_separately=True, exclude={(0,0)})
    comps.sort(key=lambda t:(len(t[1]), t[0], component_top_left(t[1])))
    color,cells=comps[k-1]
    return crop_bbox(g, cells)

def transform_code(g, code):
    if code==1:
        return g
    if code==2:
        return rotate_times(g,1)
    if code==3:
        return rotate_times(g,2)
    if code==4:
        return flip_h(g)
    raise ValueError(code)

def rule_m60(g):
    codes=[v for v in g[0] if v in (1,2,3,4)]
    motif=crop_bbox(g[1:])
    outs=[transform_code(motif, code) for code in codes]
    return pack_horiz(outs, sep=1)

def rule_m61(g):
    target=g[0][0]
    gg=clone(g)
    gg[0][0]=0
    return fill_holes_selected(gg, target)

def rule_m62(g):
    code=g[0][0]
    # find full 5 column below row 1
    h,w=size(g)
    split=None
    for c in range(w):
        if all(g[r][c]==5 for r in range(1,h)):
            split=c
            break
    left=[row[:split] for row in g[1:]]
    right=[row[split+1:] for row in g[1:]]
    H=len(left); W=len(left[0])
    out=blank(H,W)
    for r in range(H):
        for c in range(W):
            a = left[r][c]!=0
            b = right[r][c]!=0
            cond = (a or b) if code==1 else (a and b) if code==2 else (a ^ b)
            if cond:
                out[r][c]=7
    return out

def rule_m63(g):
    h,w=size(g)
    out=blank(h,w)
    for color,cells in components_nonzero(g, treat_colors_separately=True):
        r0,c0,r1,c1=bbox(cells)
        cr=(r0+r1)//2; cc=(c0+c1)//2
        out[cr][cc]=color
    return out

def rule_h57(g):
    legend=[v for v in g[0] if v!=0][:4]
    pivot=find_unique(g,5)
    cells=[(r,c,v) for r,row in enumerate(g[1:], start=1) for c,v in enumerate(row) if v not in (0,5)]
    base=blank(*size(g))
    for c,v in enumerate(legend):
        base[0][c]=v
    pr,pc=pivot
    base[pr][pc]=5
    return orbit_cells(base, cells, pivot, turns=(0,1,2,3), keep_original=False, recolor_by_turn={i:legend[i] for i in range(4)})

def rule_h58(g):
    # source motif inside 9-frame; target 8-frames have code cell above left corner
    out=clone(g)
    source=None
    for (r0,c0,r1,c1),cells in frame_info_by_color(g,9):
        source=subgrid(g,r0+1,c0+1,r1-1,c1-1)
        break
    if source is None:
        return g
    for (r0,c0,r1,c1),cells in frame_info_by_color(g,8):
        code = g[r0-1][c0] if r0-1>=0 else 1
        motif=transform_code(source, code)
        mh,mw=size(motif)
        ih,iw=r1-r0-1,c1-c0-1
        sr=r0+1+(ih-mh)//2
        sc=c0+1+(iw-mw)//2
        for r in range(sr, r1):
            for c in range(c0+1,c1):
                out[r][c]=0
        for r in range(mh):
            for c in range(mw):
                if motif[r][c]!=0:
                    out[sr+r][sc+c]=motif[r][c]
    return out

def rule_h59(g):
    out=clone(g)
    legend=[v for v in g[0] if v!=0]
    infos=[info for info in frame_info_by_color(g,8) if info[0][0]>0]  # frames below legend row
    infos.sort(key=lambda t: ((t[0][2]-t[0][0]+1)*(t[0][3]-t[0][1]+1)), reverse=True)
    bbs=[bb for bb,_ in infos]
    for idx,(r0,c0,r1,c1) in enumerate(bbs):
        inner = bbs[idx+1] if idx+1 < len(bbs) else None
        color = legend[min(idx, len(legend)-1)]
        for r in range(r0+1, r1):
            for c in range(c0+1, c1):
                if inner and (inner[0] <= r <= inner[2] and inner[1] <= c <= inner[3]):
                    continue
                out[r][c]=color
    return out

def rule_h60(g):
    h,w=size(g)
    split_cols=[c for c in range(w) if all(g[r][c]==5 for r in range(h))]
    a=subgrid(g,0,0,h-1,split_cols[0]-1)
    b=subgrid(g,0,split_cols[0]+1,h-1,split_cols[1]-1)
    cpanel=subgrid(g,0,split_cols[1]+1,h-1,w-1)
    comp_a=components_nonzero(a, treat_colors_separately=False)[0][1]
    comp_b=components_nonzero(b, treat_colors_separately=False)[0][1]
    comp_c=components_nonzero(cpanel, treat_colors_separately=False)[0][1]
    ra,ca,_,_=bbox(comp_a)
    rb,cb,_,_=bbox(comp_b)
    dr,dc=rb-ra, cb-ca
    H,W=size(cpanel)
    out=blank(H,W)
    for r,c in comp_c:
        nr,nc=r+dr,c+dc
        if 0<=nr<H and 0<=nc<W:
            out[nr][nc]=cpanel[r][c]
    return out

def rule_h61(g):
    comps=[cells for color,cells in components_nonzero(g, treat_colors_separately=True)]
    comps.sort(key=component_top_left)
    n=len(comps)
    out=blank(n,n)
    areas=[len(c) for c in comps]
    for i in range(n):
        for j in range(n):
            if areas[i]==areas[j]:
                out[i][j]=1
            elif areas[i]>areas[j]:
                out[i][j]=2
            else:
                out[i][j]=3
    return out

def path_hv(p1,p2):
    (r1,c1),(r2,c2)=p1,p2
    pts=[]
    step=1 if c2>=c1 else -1
    for c in range(c1, c2+step, step):
        pts.append((r1,c))
    step=1 if r2>=r1 else -1
    for r in range(r1+step, r2+step, step):
        pts.append((r,c2))
    return pts

def path_vh(p1,p2):
    (r1,c1),(r2,c2)=p1,p2
    pts=[]
    step=1 if r2>=r1 else -1
    for r in range(r1, r2+step, step):
        pts.append((r,c1))
    step=1 if c2>=c1 else -1
    for c in range(c1+step, c2+step, step):
        pts.append((r2,c))
    return pts

def clear_path(g, pts, color):
    for r,c in pts[1:-1]:
        if g[r][c] not in (0,color):
            return False
    return True

def rule_h62(g):
    out=clone(g)
    by=collections.defaultdict(list)
    for r,row in enumerate(g):
        for c,v in enumerate(row):
            if v not in (0,9):
                by[v].append((r,c))
    for color,pts in by.items():
        if len(pts)!=2:
            continue
        p1,p2=pts
        cand1=path_hv(p1,p2)
        cand2=path_vh(p1,p2)
        pts_use = cand1 if clear_path(g,cand1,color) else cand2
        for r,c in pts_use:
            out[r][c]=color
    return out

def rule_h63(g):
    comps=[]
    for color,cells in components_nonzero(g, treat_colors_separately=True):
        crop=grid_from_component(g,cells)
        h,w=size(crop)
        if h>w:
            crop=rotate_times(crop,1)
            h,w=size(crop)
        comps.append((len(cells), color, crop))
    comps.sort(key=lambda t:(-t[0], t[1]))
    return pack_horiz([crop for _,_,crop in comps], sep=1)

def make_puzzle(pid, title, difficulty, skills, staged_hint, written_solution, uses_new_primitive, rule_fn, train_inputs, test_input):
    return {
        'id': pid,
        'title': title,
        'difficulty': difficulty,
        'skills': skills,
        'staged_hint': staged_hint,
        'written_solution': written_solution,
        'uses_new_primitive': uses_new_primitive,
        'program_name': rule_fn.__name__,
        'program_source': inspect.getsource(rule_fn).rstrip(),
        'train': [{'input': strings_from_grid(inp), 'output': strings_from_grid(rule_fn(inp))} for inp in train_inputs],
        'test': {'input': strings_from_grid(test_input), 'output': strings_from_grid(rule_fn(test_input))},
    }

# --- Input constructors ---

def g_e57(n, points):
    g=blank(n,n)
    p=n//2
    g[p][p]=5
    add_cells(g, points)
    return g

def g_e58(h,w,pairs):
    g=blank(h,w)
    for r1,c1,r2,c2,color in pairs:
        g[r1][c1]=color
        g[r2][c2]=color
    return g

def g_e59(h,w,seeds):
    g=blank(h,w)
    add_cells(g, seeds)
    return g

def g_e60(h,w,rects):
    g=blank(h,w)
    for r0,c0,r1,c1,color in rects:
        for r,c in [(r0,c0),(r0,c1),(r1,c0),(r1,c1)]:
            g[r][c]=color
    return g

def g_e61(h,w,points):
    g=blank(h,w)
    add_cells(g, points)
    return g

def g_e62(header, data_rows):
    g=[header[:]]
    g.extend([row[:] for row in data_rows])
    return g

def g_e63(h,w,patterns):
    g=blank(h,w)
    for top,left,pat in patterns:
        add_pattern(g, top, left, pat)
    return g

def g_m57(n, target, points):
    g=blank(n,n)
    g[0][0]=target
    p=n//2
    g[p][p]=5
    add_cells(g, points)
    return g

def g_m58(top_mark_cols, left_mark_rows, data_rows):
    H=len(data_rows); W=len(data_rows[0])
    g=blank(H+1, W+1)
    for c in top_mark_cols:
        g[0][c]=8
    for r in left_mark_rows:
        g[r][0]=8
    for r in range(H):
        for c in range(W):
            g[r+1][c+1]=data_rows[r][c]
    return g

def g_m59(h,w,k,patterns):
    g=blank(h,w)
    g[0][0]=k
    for top,left,pat in patterns:
        add_pattern(g, top, left, pat)
    return g

def g_m60(codes, motif):
    W=max(len(codes), len(motif[0]))
    g=[codes + [0]*(W-len(codes))]
    for row in motif:
        g.append(row + [0]*(W-len(row)))
    return g

def g_m61(h,w,target,patterns):
    g=blank(h,w)
    g[0][0]=target
    for top,left,pat in patterns:
        add_pattern(g, top, left, pat)
    return g

def g_m62(code, left_panel, right_panel):
    H=len(left_panel); W=len(left_panel[0])
    g=blank(H+1, W*2+1)
    g[0][0]=code
    split=W
    for r in range(H):
        for c in range(W):
            g[r+1][c]=left_panel[r][c]
            g[r+1][split]=5
            g[r+1][split+1+c]=right_panel[r][c]
    return g

def g_m63(h,w,patterns):
    g=blank(h,w)
    for top,left,pat in patterns:
        add_pattern(g, top, left, pat)
    return g

def g_h57(n, legend, points):
    g=blank(n,n)
    for c,v in enumerate(legend):
        g[0][c]=v
    p=n//2
    g[p][p]=5
    add_cells(g, points)
    return g

def g_h58(h,w,source_frame, source_motif, target_frames):
    g=blank(h,w)
    sr0,sc0,sr1,sc1=source_frame
    draw_rect_border(g,sr0,sc0,sr1,sc1,9)
    add_pattern(g, sr0+1, sc0+1, source_motif)
    for code,(r0,c0,r1,c1) in target_frames:
        draw_rect_border(g,r0,c0,r1,c1,8)
        if r0-1 >= 0:
            g[r0-1][c0]=code
    return g

def g_h59(n, legend, frames):
    g=blank(n,n)
    for c,v in enumerate(legend):
        g[0][c]=v
    for r0,c0,r1,c1 in frames:
        draw_rect_border(g,r0,c0,r1,c1,8)
    return g

def g_h60(panel_a, panel_b, panel_c):
    H=len(panel_a); W=len(panel_a[0])
    g=blank(H, W*3+2)
    for r in range(H):
        for c in range(W):
            g[r][c]=panel_a[r][c]
            g[r][W]=5
            g[r][W+1+c]=panel_b[r][c]
            g[r][2*W+1]=5
            g[r][2*W+2+c]=panel_c[r][c]
    return g

def g_h61(h,w,patterns):
    g=blank(h,w)
    for top,left,pat in patterns:
        add_pattern(g, top, left, pat)
    return g

def g_h62(h,w,points,blockers):
    g=blank(h,w)
    add_cells(g, [(r,c,9) for r,c in blockers])
    add_cells(g, points)
    return g

def g_h63(h,w,patterns):
    g=blank(h,w)
    for top,left,pat in patterns:
        add_pattern(g, top, left, pat)
    return g

# pattern helpers
PAT_L_2 = [
    [2,0],
    [2,0],
    [2,2],
]
PAT_L_3 = [
    [3,0],
    [3,0],
    [3,3],
]
PAT_T_4 = [
    [4,4,4],
    [0,4,0],
    [0,4,0],
]
PAT_Z_6 = [
    [6,6,0],
    [0,6,6],
]
PAT_BOX4 = [
    [4,4,4],
    [4,0,4],
    [4,4,4],
]
PAT_BOX6 = [
    [6,6,6],
    [6,0,6],
    [6,6,6],
]
PAT_BOX7 = [
    [7,7,7],
    [7,0,7],
    [7,7,7],
]
PAT_RECT5 = [
    [5,5,5],
    [5,5,5],
]
PAT_BAR2 = [
    [2],
    [2],
    [2],
    [2],
]
PAT_DOT9 = [[9]]

PUZZLES=[]

# Easy
PUZZLES.append(make_puzzle(
    'E57', 'Orbit Copy Around Pivot', 'easy',
    ['rotational symmetry', 'pivot reasoning', 'copying'],
    'Find the unique pivot first. Then reuse the same offsets from that pivot in the other three quarter-turn positions.',
    'Locate the single pivot cell colored 5. Every other nonzero cell is copied to its 90°, 180°, and 270° rotations around that pivot.',
    True, rule_e57,
    [
        g_e57(7, [(1,2,2),(2,3,3)]),
        g_e57(9, [(2,3,4),(3,4,6),(1,4,7)]),
        g_e57(7, [(2,1,8),(1,3,2)]),
        g_e57(9, [(2,2,3),(4,3,9)]),
    ],
    g_e57(9, [(1,3,2),(2,4,7),(3,2,4)])
))

PUZZLES.append(make_puzzle(
    'E58', 'Diagonal Segment Completion', 'easy',
    ['diagonal detection', 'endpoint completion', 'same-color linking'],
    'Ignore orthogonal neighbors. Pair the matching-color endpoints that already lie on one diagonal and fill the cells between them.',
    'For each color, find its two endpoints on a 45° diagonal and fill the whole diagonal segment connecting them.',
    False, rule_e58,
    [
        g_e58(7,7, [(1,1,4,4,2),(5,1,3,3,7)]),
        g_e58(8,8, [(1,5,4,2,3),(2,1,5,4,6)]),
        g_e58(9,9, [(0,4,4,8,8),(6,1,3,4,2)]),
        g_e58(7,9, [(1,7,4,4,9),(5,2,2,5,4)]),
    ],
    g_e58(9,9, [(1,1,5,5,3),(6,7,3,4,8)])
))

PUZZLES.append(make_puzzle(
    'E59', 'Plus Expansion from Seeds', 'easy',
    ['local growth', 'orthogonal neighbors', 'same-color dilation'],
    'Treat each nonzero cell as a center. Add only the four orthogonal neighbors, not diagonals.',
    'Each nonzero seed grows into a plus of Manhattan radius 1 in the same color, clipped by the grid boundary.',
    False, rule_e59,
    [
        g_e59(7,7, [(2,2,2),(4,5,6)]),
        g_e59(8,8, [(1,5,3),(5,2,7)]),
        g_e59(7,9, [(3,4,4),(1,1,8)]),
        g_e59(9,9, [(2,6,9),(6,2,5)]),
    ],
    g_e59(9,9, [(2,2,3),(6,6,7),(4,4,2)])
))

PUZZLES.append(make_puzzle(
    'E60', 'Rectangle Border from Four Corners', 'easy',
    ['corners', 'rectangle inference', 'border drawing'],
    'Look for four equal-colored markers that already sit at rectangle corners. Use them as a frame recipe.',
    'For each color whose four cells form the corners of an axis-aligned rectangle, draw that whole rectangle border.',
    False, rule_e60,
    [
        g_e60(8,8, [(1,1,5,4,2),(2,5,6,7,7)]),
        g_e60(9,9, [(0,2,4,6,3),(5,1,8,3,8)]),
        g_e60(7,10, [(1,1,5,5,4),(0,7,6,9,9)]),
        g_e60(8,9, [(2,2,6,6,6),(1,7,5,8,2)]),
    ],
    g_e60(9,10, [(1,2,6,7,3),(0,8,8,9,7)])
))

PUZZLES.append(make_puzzle(
    'E61', 'Color Histogram Column', 'easy',
    ['counting', 'dynamic output', 'sorting by color'],
    'You do not need the positions. Only the multiset of colors matters.',
    'Count how many times each nonzero color appears. Output a single column, stacking colors in ascending color order and repeating each color by its count.',
    False, rule_e61,
    [
        g_e61(5,6, [(0,1,2),(1,2,2),(3,3,4),(4,4,7)]),
        g_e61(6,6, [(0,0,3),(2,2,3),(3,5,3),(4,1,8),(5,5,8)]),
        g_e61(5,7, [(1,1,9),(1,5,2),(2,3,2),(3,0,5)]),
        g_e61(7,7, [(0,6,4),(2,2,4),(4,4,4),(6,0,1)]),
    ],
    g_e61(6,7, [(0,2,2),(2,2,2),(5,6,6),(3,1,6),(1,5,9)])
))

PUZZLES.append(make_puzzle(
    'E62', 'Header-Selected Columns', 'easy',
    ['matrix slicing', 'header markers', 'dynamic output'],
    'Solve the first row first: it only tells you which columns survive.',
    'Use the 8s in the top row as column selectors. Remove the header row and keep only those selected columns from the remaining rows.',
    False, rule_e62,
    [
        g_e62([0,8,0,8,0,8], [
            [1,2,3,4,5,6],
            [6,5,4,3,2,1],
            [1,0,2,0,3,0],
            [7,7,8,8,9,9],
        ]),
        g_e62([8,0,8,0,0], [
            [3,1,4,1,5],
            [9,2,6,5,3],
            [5,8,9,7,9],
        ]),
        g_e62([0,8,8,0,0,8,0], [
            [2,4,6,8,1,3,5],
            [5,3,1,8,6,4,2],
            [9,0,9,0,9,0,9],
            [1,2,3,4,5,6,7],
        ]),
        g_e62([8,0,0,8], [
            [4,4,4,4],
            [1,2,3,4],
            [7,6,5,4],
            [0,1,0,1],
        ]),
    ],
    g_e62([0,8,0,8,8,0], [
        [2,7,1,8,2,8],
        [3,1,4,1,5,9],
        [2,6,5,3,5,8],
    ])
))

PUZZLES.append(make_puzzle(
    'E63', 'Crop the Largest Component', 'easy',
    ['connected components', 'area comparison', 'cropping'],
    'Compare whole components, not individual cells. Once you know the largest one, the output is just its crop.',
    'Find the largest same-color connected component and crop the output to its bounding box.',
    False, rule_e63,
    [
        g_e63(9,9, [(1,1,[[2,2,2],[2,0,0]]),(5,5,[[7,7],[7,7]])]),
        g_e63(10,10, [(1,6,[[3,3,0],[0,3,3]]),(5,1,[[4,4,4],[4,4,0],[4,0,0]])]),
        g_e63(8,11, [(0,1,[[6,6,6],[0,6,0]]),(4,7,[[8,8],[8,8],[8,0]])]),
        g_e63(9,10, [(1,1,[[5,5],[5,5],[5,0]]),(4,5,[[2,2,2],[0,2,0]])]),
    ],
    g_e63(10,10, [(1,1,[[3,3],[3,0]]),(4,4,[[7,7,7],[7,0,7],[7,7,7]])])
))

# Medium
PUZZLES.append(make_puzzle(
    'M57', 'Selector-Color Orbit Copy', 'medium',
    ['selector cell', 'pivot reasoning', 'selective copying'],
    'The pivot still governs the geometry, but only one color is allowed to orbit. Read that color from the selector first.',
    'Read the selected color from the top-left cell. Keep the whole input, and orbit only cells of that color around the pivot 5 by quarter turns.',
    True, rule_m57,
    [
        g_m57(9, 2, [(1,3,2),(2,4,2),(6,1,7)]),
        g_m57(9, 4, [(2,2,4),(3,4,4),(1,6,8)]),
        g_m57(7, 6, [(1,2,6),(2,3,6),(5,5,3)]),
        g_m57(9, 7, [(2,3,7),(3,3,7),(6,6,2)]),
    ],
    g_m57(9, 3, [(1,4,3),(2,3,3),(5,6,8),(6,2,3)])
))

PUZZLES.append(make_puzzle(
    'M58', 'Cross-Selected Submatrix', 'medium',
    ['row selection', 'column selection', 'submatrix extraction'],
    'Read the two headers separately. The left edge chooses rows; the top edge chooses columns.',
    'The 8s in the top row choose columns and the 8s in the left column choose rows. Output the cross-product submatrix from the interior data.',
    False, rule_m58,
    [
        g_m58([1,3,5], [2,4], [
            [1,2,3,4,5],
            [5,4,3,2,1],
            [9,8,7,6,5],
            [0,1,0,1,0],
        ]),
        g_m58([2,4], [1,3,5], [
            [2,7,1,8],
            [2,8,1,8],
            [1,8,2,8],
            [1,1,1,1],
            [9,9,0,0],
        ]),
        g_m58([1,2,5], [2,5], [
            [3,1,4,1,5],
            [9,2,6,5,3],
            [5,8,9,7,9],
            [3,2,3,8,4],
            [6,2,6,4,3],
        ]),
        g_m58([3,5], [1,4], [
            [7,0,7,0,7],
            [1,2,3,4,5],
            [5,4,3,2,1],
            [8,8,8,8,8],
        ]),
    ],
    g_m58([2,4,6], [2,3], [
        [1,3,5,7,9,2],
        [2,4,6,8,1,3],
        [3,5,7,9,2,4],
    ])
))

PUZZLES.append(make_puzzle(
    'M59', 'Ranked Component Crop', 'medium',
    ['component ranking', 'selector cell', 'cropping'],
    'Do not guess a component by color. Sort them by size first, then take the selector-th one.',
    'The top-left selector gives a 1-based rank. Ignore that selector cell, sort same-color components by area ascending, and output the selected component cropped to its box.',
    False, rule_m59,
    [
        g_m59(10,10, 1, [(1,2,[[2,2]]),(4,1,[[3,3,3],[3,0,0]]),(6,6,[[4,4],[4,4]])]),
        g_m59(10,10, 2, [(1,1,[[5,5,0],[0,5,5]]),(5,2,[[6,6],[6,0],[6,0]]),(4,7,[[7,7],[7,7]])]),
        g_m59(9,11, 3, [(1,4,[[2,2]]),(3,1,[[8,8,8],[0,8,0]]),(5,7,[[9,9],[9,9],[9,0]])]),
        g_m59(10,10, 2, [(1,6,[[3,3,3]]),(4,1,[[4,4],[4,0],[4,0]]),(5,6,[[7,7],[7,7]])]),
    ],
    g_m59(10,11, 2, [(1,1,[[2,2]]),(3,4,[[6,6,6],[6,0,0]]),(6,7,[[8,8],[8,8],[8,0]])])
))

PUZZLES.append(make_puzzle(
    'M60', 'Command Strip Transform', 'medium',
    ['symbolic commands', 'rotation', 'packing'],
    'Treat the top row as a program, not as part of the object.',
    'Crop the motif below the command row. For each nonzero command code in the top row, output the corresponding transformed motif and pack the results left to right with one blank column between them.',
    False, rule_m60,
    [
        g_m60([1,2,4], [
            [0,2,0],
            [2,2,2],
            [0,0,2],
        ]),
        g_m60([3,1], [
            [6,6,0],
            [0,6,6],
        ]),
        g_m60([2,2,4,1], [
            [4,0],
            [4,4],
            [4,0],
        ]),
        g_m60([4,3,2], [
            [7,7,7],
            [0,7,0],
        ]),
    ],
    g_m60([1,4,2], [
        [0,3,0],
        [3,3,3],
        [3,0,0],
    ])
))

PUZZLES.append(make_puzzle(
    'M61', 'Fill Holes Only for the Selected Color', 'medium',
    ['hole detection', 'selector cell', 'object filtering'],
    'The interior geometry matters only for one chosen color. Everything else is a distractor.',
    'Read the target color from the top-left selector. Fill enclosed holes only inside components of that color; leave all other colors unchanged.',
    False, rule_m61,
    [
        g_m61(10,10, 4, [(1,1,PAT_BOX4),(1,6,PAT_BOX6)]),
        g_m61(11,11, 6, [(2,2,PAT_BOX6),(5,6,PAT_BOX7)]),
        g_m61(10,12, 7, [(1,1,PAT_BOX7),(4,7,PAT_BOX4)]),
        g_m61(11,11, 4, [(2,5,PAT_BOX4),(6,1,PAT_BOX6)]),
    ],
    g_m61(12,12, 6, [(2,2,PAT_BOX6),(6,6,PAT_BOX7),(7,1,PAT_BOX4)])
))

PUZZLES.append(make_puzzle(
    'M62', 'Boolean Overlay of Two Panels', 'medium',
    ['panel split', 'boolean operations', 'support masks'],
    'First separate the two panels. Then ignore color identities and think in terms of occupied versus empty cells.',
    'The top-left code chooses the operation on the left and right panel supports: 1 = union, 2 = intersection, 3 = xor. Return the resulting panel as color 7 on black.',
    False, rule_m62,
    [
        g_m62(1, [
            [0,7,0,0],
            [7,7,0,0],
            [0,0,0,0],
        ], [
            [0,0,7,0],
            [0,7,7,0],
            [0,0,0,0],
        ]),
        g_m62(2, [
            [7,7,0,0],
            [0,7,0,0],
            [0,0,0,7],
        ], [
            [7,0,0,0],
            [0,7,7,0],
            [0,0,0,7],
        ]),
        g_m62(3, [
            [0,7,0],
            [7,7,7],
            [0,7,0],
        ], [
            [0,7,0],
            [0,7,0],
            [0,7,0],
        ]),
        g_m62(1, [
            [7,0,0,7],
            [0,0,0,0],
            [0,7,7,0],
        ], [
            [0,0,7,0],
            [0,7,0,0],
            [0,7,0,0],
        ]),
    ],
    g_m62(3, [
        [7,7,0,0],
        [0,7,0,0],
        [0,0,7,0],
    ], [
        [0,7,0,0],
        [0,7,7,0],
        [0,0,7,0],
    ])
))

PUZZLES.append(make_puzzle(
    'M63', 'Component Center Markers', 'medium',
    ['bounding boxes', 'object abstraction', 'centers'],
    'Do not preserve full objects. Collapse each one to a single representative cell.',
    'For every connected same-color component, compute its bounding-box center and place one cell of that color there in an otherwise blank grid of the same size.',
    False, rule_m63,
    [
        g_m63(9,9, [(1,1,[[2,2,2],[2,2,2],[2,2,2]]),(5,5,[[6,6,6],[6,6,6],[6,6,6]])]),
        g_m63(10,10, [(1,6,[[3,3,3],[3,3,3],[3,3,3]]),(5,1,[[8,8,8],[8,8,8],[8,8,8]])]),
        g_m63(9,11, [(1,1,[[4,4,4],[4,4,4],[4,4,4]]),(4,7,[[7,7,7],[7,7,7],[7,7,7]])]),
        g_m63(11,11, [(2,2,[[5,5,5],[5,5,5],[5,5,5]]),(6,6,[[9,9,9],[9,9,9],[9,9,9]])]),
    ],
    g_m63(11,11, [(1,7,[[2,2,2],[2,2,2],[2,2,2]]),(6,1,[[6,6,6],[6,6,6],[6,6,6]]),(4,4,[[4,4,4],[4,4,4],[4,4,4]])])
))

# Hard
PUZZLES.append(make_puzzle(
    'H57', 'Legend-Recolored Orbit', 'hard',
    ['rotational symmetry', 'recoloring', 'legend decoding'],
    'Separate the geometry from the palette. The source object only tells you the shape and offsets; the top row tells you the colors of the four rotations.',
    'Read the four legend colors from the top row. Orbit the source object around the pivot 5 at quarter turns, recoloring the original orientation and the three rotated copies according to legend order.',
    True, rule_h57,
    [
        g_h57(9, [2,3,4,6], [(2,3,9),(3,3,9),(3,4,9)]),
        g_h57(11, [7,8,2,4], [(3,5,1),(4,5,1),(4,6,1),(5,6,1)]),
        g_h57(9, [3,6,9,2], [(1,4,8),(2,4,8),(2,5,8)]),
        g_h57(11, [4,2,7,8], [(3,4,6),(4,4,6),(4,5,6),(5,4,6)]),
    ],
    g_h57(11, [2,8,3,7], [(3,5,9),(4,5,9),(5,4,9),(5,6,9)])
))

PUZZLES.append(make_puzzle(
    'H58', 'Commanded Multi-Frame Insertion', 'hard',
    ['template extraction', 'frame reasoning', 'local transforms'],
    'Find the source motif once. Then each empty target frame becomes a transformed copy request.',
    'Extract the motif from inside the unique 9-bordered source frame. For every 8-bordered target frame, read the command cell just above its left border and place the commanded transform of the source motif into that frame interior.',
    False, rule_h58,
    [
        g_h58(12,19, (2,1,6,5), [[2,0,0],[2,2,2],[0,0,2]], [(1,(2,8,6,12)), (2,(2,14,6,18))]),
        g_h58(13,19, (3,1,7,5), [[0,6,6],[6,6,0],[0,6,0]], [(3,(3,8,7,12)), (4,(3,14,7,18))]),
        g_h58(14,20, (4,1,8,5), [[4,4,4],[0,4,0],[0,4,0]], [(2,(4,8,8,12)), (1,(4,14,8,18))]),
        g_h58(12,20, (2,2,6,6), [[7,0,7],[7,7,7],[0,7,0]], [(4,(2,9,6,13)), (3,(2,15,6,19))]),
    ],
    g_h58(13,20, (3,1,7,5), [[3,3,0],[0,3,3],[0,0,3]], [(1,(3,8,7,12)), (2,(3,14,7,18))])
))

PUZZLES.append(make_puzzle(
    'H59', 'Nested Frame Depth Coloring', 'hard',
    ['nested structures', 'frame depth', 'legend use'],
    'Do not fill all interiors at once. Color the region between one frame and the next inner frame.',
    'Use the top-row legend as outer-to-inner fill colors. Keep the 8-colored frame borders, and fill each ring region between nested frames with the corresponding legend color; the innermost open region gets the deepest legend color.',
    False, rule_h59,
    [
        g_h59(11, [2,3], [(2,2,10,10),(4,4,8,8)]),
        g_h59(13, [4,6,2], [(2,2,12,12),(4,4,10,10),(6,6,8,8)]),
        g_h59(12, [7,3], [(2,1,10,9),(4,3,8,7)]),
        g_h59(15, [2,5,8], [(3,3,13,13),(5,5,11,11),(7,7,9,9)]),
    ],
    g_h59(13, [3,7,4], [(2,2,12,12),(4,4,10,10),(6,6,8,8)])
))

PUZZLES.append(make_puzzle(
    'H60', 'Analogical Translation Across Panels', 'hard',
    ['analogy', 'translation vectors', 'panel decomposition'],
    'The first two panels teach a motion. Measure that motion, then apply it to the third panel’s object.',
    'Compare the object positions in the first and second panels to infer one translation vector. Apply that same vector to the third panel object and return only the translated third panel.',
    False, rule_h60,
    [
        g_h60(
            [[0,2,0,0],[2,2,2,0],[0,0,0,0],[0,0,0,0]],
            [[0,0,0,0],[0,2,0,0],[2,2,2,0],[0,0,0,0]],
            [[0,0,7,0],[0,7,7,0],[0,0,0,0],[0,0,0,0]],
        ),
        g_h60(
            [[0,0,3,0],[0,3,3,0],[0,0,0,0],[0,0,0,0]],
            [[0,0,0,0],[0,0,3,0],[0,3,3,0],[0,0,0,0]],
            [[4,4,0,0],[0,4,0,0],[0,0,0,0],[0,0,0,0]],
        ),
        g_h60(
            [[0,0,0,0,0],[0,6,6,0,0],[0,6,0,0,0],[0,0,0,0,0]],
            [[0,0,0,0,0],[0,0,0,0,0],[0,6,6,0,0],[0,6,0,0,0]],
            [[0,0,8,0,0],[0,8,8,8,0],[0,0,0,0,0],[0,0,0,0,0]],
        ),
        g_h60(
            [[0,9,0,0],[0,9,9,0],[0,0,0,0],[0,0,0,0]],
            [[0,0,9,0],[0,0,9,9],[0,0,0,0],[0,0,0,0]],
            [[5,5,0,0],[5,0,0,0],[0,0,0,0],[0,0,0,0]],
        ),
    ],
    g_h60(
        [[0,0,2,0,0],[0,2,2,0,0],[0,0,0,0,0],[0,0,0,0,0]],
        [[0,0,0,0,0],[0,0,2,0,0],[0,2,2,0,0],[0,0,0,0,0]],
        [[0,7,0,0,0],[7,7,7,0,0],[0,0,0,0,0],[0,0,0,0,0]],
    )
))

PUZZLES.append(make_puzzle(
    'H61', 'Area Comparison Matrix', 'hard',
    ['component abstraction', 'pairwise relations', 'dynamic output'],
    'The output is not a picture of the input. It is a table comparing every object to every other object.',
    'Order the components by top-left position. Build an N×N matrix: 1 on ties, 2 when the row component has larger area than the column component, and 3 when it has smaller area.',
    False, rule_h61,
    [
        g_h61(9,9, [(1,1,[[2,2]]),(1,6,[[3,3,3]]),(5,3,[[4,4],[4,4]])]),
        g_h61(10,10, [(1,1,[[5,5,5],[5,0,0]]),(2,7,[[6,6]]),(6,2,[[7,7],[7,7],[7,0]])]),
        g_h61(11,11, [(1,2,[[2,2]]),(4,5,[[8,8,8],[8,8,8]]),(7,1,[[9,9,9]])]),
        g_h61(10,12, [(1,1,[[3,3,3]]),(3,8,[[4,4],[4,4]]),(6,4,[[7,7],[7,0],[7,0]])]),
    ],
    g_h61(11,11, [(1,1,[[2,2]]),(2,6,[[5,5,5]]),(6,2,[[7,7],[7,7]]),(7,7,[[8,8,8],[8,0,0]])])
))

PUZZLES.append(make_puzzle(
    'H62', 'Blocked L-Path Connector', 'hard',
    ['path selection', 'obstacle avoidance', 'multi-object routing'],
    'Try the two possible L routes separately. One of them is blocked, and the other is the intended connection.',
    'Connect each same-color endpoint pair with an L-shaped path of that color. Prefer horizontal-then-vertical if it is clear; otherwise use vertical-then-horizontal. Blocker cells colored 9 remain unchanged.',
    False, rule_h62,
    [
        g_h62(8,8, [(1,1,2),(5,4,2),(2,6,7),(6,6,7)], [(1,4),(2,4),(3,4),(4,4),(5,5)]),
        g_h62(8,8, [(1,5,3),(5,2,3),(2,1,6),(6,4,6)], [(1,2),(2,2),(3,2),(4,2),(5,3)]),
        g_h62(9,9, [(1,1,4),(6,5,4),(2,7,8),(7,7,8)], [(1,5),(2,5),(3,5),(4,5),(5,6)]),
        g_h62(8,9, [(1,6,5),(5,3,5),(2,1,7),(6,6,7)], [(1,3),(2,3),(3,3),(4,3),(5,4)]),
    ],
    g_h62(9,9, [(1,2,2),(6,6,2),(2,7,6),(7,3,6)], [(1,6),(2,6),(3,6),(4,6),(5,5)])
))

PUZZLES.append(make_puzzle(
    'H63', 'Rotate-Tall Pack by Area', 'hard',
    ['component extraction', 'conditional rotation', 'sorting and packing'],
    'Standardize each object before sorting. The key normalization is to rotate only the tall ones.',
    'Crop every same-color component. If a crop is taller than it is wide, rotate it clockwise once. Then sort components by area descending and color ascending, and pack them left to right with one blank column between them.',
    False, rule_h63,
    [
        g_h63(10,12, [(1,1,[[2],[2],[2],[2]]),(2,5,[[6,6,0],[0,6,6]]),(6,8,[[4,4],[4,4]])]),
        g_h63(11,11, [(1,7,[[3],[3],[3]]),(4,1,[[7,7,7],[7,0,0]]),(7,6,[[8,8],[8,8]])]),
        g_h63(10,13, [(1,1,[[5],[5],[5],[5]]),(2,6,[[2,2,2]]),(6,9,[[9,9],[9,0],[9,0]])]),
        g_h63(11,12, [(1,2,[[4],[4],[4]]),(3,7,[[6,6,6],[0,6,0]]),(7,1,[[7,7],[7,7]])]),
    ],
    g_h63(11,13, [(1,1,[[3],[3],[3],[3]]),(2,6,[[8,8,8],[8,0,0]]),(7,8,[[5,5],[5,5]])])
))


def validate_puzzles():
    errors=[]
    fn_map={name: obj for name,obj in globals().items() if callable(obj)}
    for puzzle in PUZZLES:
        fn=fn_map[puzzle['program_name']]
        for idx,pair in enumerate(puzzle['train']):
            inp=[[int(ch) for ch in row] for row in pair['input']]
            got=strings_from_grid(fn(inp))
            if got!=pair['output']:
                errors.append((puzzle['id'], 'train', idx, got, pair['output']))
        inp=[[int(ch) for ch in row] for row in puzzle['test']['input']]
        got=strings_from_grid(fn(inp))
        if got!=puzzle['test']['output']:
            errors.append((puzzle['id'], 'test', 0, got, puzzle['test']['output']))
    return errors

def puzzle_bank_summary():
    return {
        'n_puzzles': len(PUZZLES),
        'n_train_pairs': sum(len(p['train']) for p in PUZZLES),
        'avg_train_pairs': sum(len(p['train']) for p in PUZZLES)/len(PUZZLES),
        'ids': [p['id'] for p in PUZZLES],
    }

if __name__ == '__main__':
    errs=validate_puzzles()
    if errs:
        print('validation_failed', errs[:3])
        raise SystemExit(1)
    summary=puzzle_bank_summary()
    print(json.dumps(summary, indent=2))
