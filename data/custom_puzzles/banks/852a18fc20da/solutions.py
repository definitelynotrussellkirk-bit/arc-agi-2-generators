from __future__ import annotations

from collections import defaultdict, deque
from pprint import pprint
import inspect

DIR4 = [(-1,0),(1,0),(0,-1),(0,1)]
DIRMAP = {1:(-1,0), 2:(0,1), 3:(1,0), 4:(0,-1)}
KERNELS_M85 = {
    2:[(0,0),(-1,0),(1,0),(0,-1),(0,1)],
    3:[(0,0),(-1,-1),(-1,1),(1,-1),(1,1)],
    4:[(dr,dc) for dr in (-1,0,1) for dc in (-1,0,1)],
}
TOKEN_MAP_H88 = {9:1, 2:2, 3:3, 4:4}
TOKEN_MAP_H91 = {9:1, 2:2, 3:3, 4:4}

def blank(h,w,val=0):
    return [[val]*w for _ in range(h)]


def clone(g):
    return [row[:] for row in g]


def size(g):
    return (len(g), len(g[0]) if g else 0)


def in_bounds(g,r,c):
    h,w=size(g)
    return 0<=r<h and 0<=c<w


def grid_from_strings(rows):
    return [[int(ch) for ch in row] for row in rows]


def strings_from_grid(g):
    return ["".join(str(v) for v in row) for row in g]


def paint_cells(g, cells, color=None):
    for item in cells:
        if len(item)==2:
            r,c=item
            v=color
        else:
            r,c,v=item
        if in_bounds(g,r,c):
            g[r][c]=v
    return g


def bbox(cells):
    rs=[r for r,c in cells]
    cs=[c for r,c in cells]
    return min(rs), min(cs), max(rs), max(cs)


def crop_bbox(g, cells=None):
    if cells is None:
        cells=[(r,c) for r,row in enumerate(g) for c,v in enumerate(row) if v!=0]
    if not cells:
        return [[0]]
    r0,c0,r1,c1=bbox(cells)
    return [row[c0:c1+1] for row in g[r0:r1+1]]


def normalize_cells(cells):
    if not cells:
        return []
    r0,c0,_,_=bbox(cells)
    return sorted((r-r0,c-c0) for r,c in cells)


def rotate90(g):
    h,w=size(g)
    return [[g[h-1-r][c] for r in range(h)] for c in range(w)]


def rotate180(g):
    return [row[::-1] for row in g[::-1]]


def rotate270(g):
    h,w=size(g)
    return [[g[r][w-1-c] for r in range(h)] for c in range(w-1,-1,-1)]


def flip_h(g):
    return [row[::-1] for row in g]


def flip_v(g):
    return g[::-1]


def components4(g, allowed=None):
    h,w=size(g)
    seen=set()
    out=[]
    for r in range(h):
        for c,v in enumerate(g[r]):
            if v==0 or (r,c) in seen or (allowed is not None and v not in allowed):
                continue
            q=[(r,c)]
            seen.add((r,c))
            cells=[]
            while q:
                rr,cc=q.pop()
                cells.append((rr,cc))
                for dr,dc in DIR4:
                    nr,nc=rr+dr,cc+dc
                    if in_bounds(g,nr,nc) and (nr,nc) not in seen and g[nr][nc]==v and (allowed is None or g[nr][nc] in allowed):
                        seen.add((nr,nc))
                        q.append((nr,nc))
            out.append((v,sorted(cells)))
    return out


def find_rectangular_frames(g, color=1):
    comps=components4(g, allowed={color})
    frames=[]
    for v,cells in comps:
        r0,c0,r1,c1=bbox(cells)
        outline={(r,c) for r in range(r0,r1+1) for c in range(c0,c1+1) if r in (r0,r1) or c in (c0,c1)}
        if set(cells)==outline and r1-r0>=2 and c1-c0>=2:
            frames.append((r0,c0,r1,c1))
    return sorted(frames)


def flood_region(g, start, blocked={1}):
    h,w=size(g)
    q=[start]
    seen={start}
    cells=[]
    while q:
        r,c=q.pop()
        cells.append((r,c))
        for dr,dc in DIR4:
            nr,nc=r+dr,c+dc
            if 0<=nr<h and 0<=nc<w and (nr,nc) not in seen and g[nr][nc] not in blocked:
                seen.add((nr,nc))
                q.append((nr,nc))
    return cells


def shortest_path(g, start, goal, blocked={8}, order=DIR4):
    h,w=size(g)
    q=deque([start])
    prev={start:None}
    while q:
        cur=q.popleft()
        if cur==goal:
            break
        r,c=cur
        for dr,dc in order:
            nr,nc=r+dr,c+dc
            if 0<=nr<h and 0<=nc<w and (nr,nc) not in prev and (g[nr][nc] not in blocked or (nr,nc)==goal):
                prev[(nr,nc)]=cur
                q.append((nr,nc))
    if goal not in prev:
        raise ValueError("no path")
    path=[]
    cur=goal
    while cur is not None:
        path.append(cur)
        cur=prev[cur]
    return path[::-1]


def crop_nonzero(g, ignore=None):
    ignore=set(ignore or [])
    cells=[(r,c) for r,row in enumerate(g) for c,v in enumerate(row) if v!=0 and v not in ignore]
    return crop_bbox(g,cells)


def render_shape(pattern, color=None):
    # pattern list[str] using # for filled, . for empty, or digits to preserve multi-color
    cells=[]
    for r,row in enumerate(pattern):
        for c,ch in enumerate(row):
            if ch in ".0":
                continue
            if ch=="#":
                cells.append((r,c,color if color is not None else 1))
            else:
                cells.append((r,c,int(ch)))
    return cells


def place_shape(g, pattern, top_left, color=None):
    r0,c0=top_left
    for dr,dc,v in render_shape(pattern, color):
        if in_bounds(g,r0+dr,c0+dc):
            g[r0+dr][c0+dc]=v
    return g


def transform_grid(g, token):
    # 1 none, 2 rot90, 3 rot180, 4 rot270, 5 flip_h, 6 flip_v
    if token==1: return clone(g)
    if token==2: return rotate90(g)
    if token==3: return rotate180(g)
    if token==4: return rotate270(g)
    if token==5: return flip_h(g)
    if token==6: return flip_v(g)
    raise ValueError(token)


def symmetry_class(g):
    # on cropped binary/multicolor motif
    h= g==flip_h(g)
    v= g==flip_v(g)
    if h and v: return "both"
    if h: return "h"
    if v: return "v"
    return "none"


def sprout_kernel(seed_cells, offsets, color_lookup=None, allowed=None, priority=None):
    """
    seed_cells: iterable of (r,c,color)
    offsets: list[(dr,dc)]
    color_lookup: optional function(seed)->color
    allowed: optional set of cells allowed to be painted
    priority: optional dict color->rank (lower wins) for conflict resolution
    returns dict[(r,c)] = color
    """
    allowed = None if allowed is None else set(allowed)
    result={}
    prio_for = (lambda color: priority.get(color, 10**9)) if priority else (lambda color: 0)
    for seed in seed_cells:
        r,c,color = seed
        out_color = color_lookup(seed) if color_lookup else color
        for dr,dc in offsets:
            nr,nc=r+dr,c+dc
            if allowed is not None and (nr,nc) not in allowed:
                continue
            if (nr,nc) not in result or prio_for(out_color) < prio_for(result[(nr,nc)]):
                result[(nr,nc)] = out_color
    return result


def draw_frame(g, box, color=1):
    r0,c0,r1,c1=box
    for c in range(c0,c1+1):
        g[r0][c]=color; g[r1][c]=color
    for r in range(r0,r1+1):
        g[r][c0]=color; g[r][c1]=color
    return g


def crop_from_cells(g, cells):
    if not cells:
        return [[0]]
    r0,c0,r1,c1=bbox(cells)
    out=blank(r1-r0+1,c1-c0+1)
    for r,c in cells:
        out[r-r0][c-c0]=g[r][c]
    return out


def apply_transform_by_id(g, tid):
    return TRANSFORMS[tid](g)


def infer_transform(a,b):
    for tid,fn in TRANSFORMS.items():
        if fn(a)==b:
            return tid
    raise ValueError("no matching transform")


def extract_box_interior(g, box):
    r0,c0,r1,c1=box
    return [row[c0+1:c1] for row in g[r0+1:r1]]


def binary_crop_from_interior(interior):
    cells=[(r,c) for r,row in enumerate(interior) for c,v in enumerate(row) if v!=0]
    crop=crop_from_cells([[1 if v!=0 else 0 for v in row] for row in interior], cells)
    return crop


def transform_coords(coords, tid):
    # coords within crop; transform via grid conversion simpler
    if not coords:
        return []
    r1=max(r for r,c in coords)+1
    c1=max(c for r,c in coords)+1
    g=blank(r1,c1)
    for r,c in coords:
        g[r][c]=1
    tg=apply_transform_by_id(g, tid)
    return [(r,c) for r,row in enumerate(tg) for c,v in enumerate(row) if v]


def rule_e85(g):
    h,w=size(g)
    seeds=[(r,c,v) for r,row in enumerate(g) for c,v in enumerate(row) if v!=0]
    painted=sprout_kernel(seeds, [(0,0),(-1,0),(1,0),(0,-1),(0,1)])
    out=blank(h,w)
    for (r,c),v in painted.items():
        if 0<=r<h and 0<=c<w:
            out[r][c]=v
    return out


def build_e85(case):
    h,w=case['size']
    g=blank(h,w)
    for r,c,v in case['seeds']:
        g[r][c]=v
    return g


def rule_e86(g):
    h,w=size(g)
    pos=defaultdict(list)
    for r,row in enumerate(g):
        for c,v in enumerate(row):
            if v!=0:
                pos[v].append((r,c))
    out=blank(h,w)
    for color,cells in pos.items():
        if len(cells)!=2:
            # preserve weird cases
            for r,c in cells:
                out[r][c]=color
            continue
        (r1,c1),(r2,c2)=cells
        if r1==r2:
            for c in range(min(c1,c2), max(c1,c2)+1):
                out[r1][c]=color
        elif c1==c2:
            for r in range(min(r1,r2), max(r1,r2)+1):
                out[r][c1]=color
        else:
            # preserve
            out[r1][c1]=color
            out[r2][c2]=color
    return out


def build_e86(case):
    h,w=case['size']
    g=blank(h,w)
    for color,(r1,c1),(r2,c2) in case['segments']:
        g[r1][c1]=color
        g[r2][c2]=color
    return g


def rule_e87(g):
    h,w=size(g)
    pos=defaultdict(list)
    for r,row in enumerate(g):
        for c,v in enumerate(row):
            if v!=0:
                pos[v].append((r,c))
    out=blank(h,w)
    for color,cells in pos.items():
        if len(cells)!=2:
            for r,c in cells:
                out[r][c]=color
            continue
        (r1,c1),(r2,c2)=cells
        r0,r1s=sorted((r1,r2))
        c0,c1s=sorted((c1,c2))
        for c in range(c0,c1s+1):
            out[r0][c]=color
            out[r1s][c]=color
        for r in range(r0,r1s+1):
            out[r][c0]=color
            out[r][c1s]=color
    return out


def build_e87(case):
    h,w=case['size']
    g=blank(h,w)
    for color,p1,p2 in case['pairs']:
        g[p1[0]][p1[1]]=color
        g[p2[0]][p2[1]]=color
    return g


def rule_e88(g):
    h,w=size(g)
    # find full guide line of 8
    guide_row = next((r for r in range(h) if all(v==8 for v in g[r])), None)
    guide_col = next((c for c in range(w) if all(g[r][c]==8 for r in range(h))), None)
    out=clone(g)
    if guide_row is not None:
        for r,row in enumerate(g):
            for c,v in enumerate(row):
                if v!=0 and v!=8:
                    rr=2*guide_row-r
                    if 0<=rr<h:
                        out[rr][c]=v
    elif guide_col is not None:
        for r,row in enumerate(g):
            for c,v in enumerate(row):
                if v!=0 and v!=8:
                    cc=2*guide_col-c
                    if 0<=cc<w:
                        out[r][cc]=v
    return out


def build_e88(case):
    h,w=case['size']
    g=blank(h,w)
    if case['axis']=='h':
        for c in range(w): g[case['guide']][c]=8
    else:
        for r in range(h): g[r][case['guide']]=8
    for r,c,v in case['shape']:
        g[r][c]=v
    return g


def rule_e89(g):
    counts=defaultdict(int)
    for row in g:
        for v in row:
            if v!=0:
                counts[v]+=1
    out=[]
    for color in sorted(counts):
        out.extend([color]*counts[color])
    return [out] if out else [[0]]


def build_e89(case):
    h,w=case['size']
    g=blank(h,w)
    for r,c,v in case['cells']:
        g[r][c]=v
    return g


def rule_e90(g):
    h,w=size(g)
    out=blank(h,w)
    for r,row in enumerate(g):
        for c,v in enumerate(row):
            if v!=0:
                for dr in (-1,0,1):
                    for dc in (-1,0,1):
                        if abs(dr)==1 or abs(dc)==1:
                            nr,nc=r+dr,c+dc
                            if 0<=nr<h and 0<=nc<w:
                                out[nr][nc]=v
    return out


def build_e90(case):
    h,w=case['size']
    g=blank(h,w)
    for r,c,v in case['seeds']:
        g[r][c]=v
    return g


def rule_e91(g):
    h,w=size(g)
    arrow=None
    cells=[]
    for r,row in enumerate(g):
        for c,v in enumerate(row):
            if v in DIRMAP:
                arrow=(r,c,v)
            elif v!=0:
                cells.append((r,c,v))
    out=blank(h,w)
    if arrow is None:
        return clone(g)
    dr,dc=DIRMAP[arrow[2]]
    for r,c,v in cells:
        nr,nc=r+dr,c+dc
        if 0<=nr<h and 0<=nc<w:
            out[nr][nc]=v
    return out


def build_e91(case):
    h,w=case['size']
    g=blank(h,w)
    ar,ac,av=case['arrow']
    g[ar][ac]=av
    for r,c,v in case['shape']:
        g[r][c]=v
    return g


def rule_m85(g):
    h,w=size(g)
    out=blank(h,w)
    # preserve frames
    for r,row in enumerate(g):
        for c,v in enumerate(row):
            if v==1:
                out[r][c]=1
    frames=find_rectangular_frames(g, color=1)
    for r0,c0,r1,c1 in frames:
        interior={(r,c) for r in range(r0+1,r1) for c in range(c0+1,c1)}
        seed=None
        token=None
        for r in range(r0+1,r1):
            for c in range(c0+1,c1):
                v=g[r][c]
                if v in KERNELS_M85:
                    token=v
                elif v!=0:
                    seed=(r,c,v)
        if seed and token:
            painted=sprout_kernel([seed], KERNELS_M85[token], allowed=interior)
            for (r,c),v in painted.items():
                out[r][c]=v
    return out


def build_m85(case):
    h,w=case['size']
    g=blank(h,w)
    for frame in case['frames']:
        box=frame['box']
        draw_frame(g, box, 1)
        sr,sc,sv=frame['seed']
        tr,tc,tv=frame['token']
        g[sr][sc]=sv
        g[tr][tc]=tv
    return g


def rule_m86(g):
    comps=[(v,cells) for v,cells in components4(g) if v not in (1,2,3,4)]
    ordered=[]
    for color,cells in comps:
        r0,c0,r1,c1=bbox(cells)
        order=None
        if r0-1 >= 0 and g[r0-1][c0] in (1,2,3,4):
            order=g[r0-1][c0]
        else:
            # fallback nearest token
            best=None
            for rr,row in enumerate(g):
                for cc,v in enumerate(row):
                    if v in (1,2,3,4):
                        d=min(abs(rr-r)+abs(cc-c) for r,c in cells)
                        if best is None or d<best[0]:
                            best=(d,v)
            order=best[1]
        crop=crop_bbox(g,cells)
        ordered.append((order,crop))
    ordered.sort(key=lambda x:x[0])
    height=max(len(c) for _,c in ordered)
    width=sum(len(c[0]) for _,c in ordered) + (len(ordered)-1)
    out=blank(height,width)
    curc=0
    for _,crop in ordered:
        ch,cw=size(crop)
        for r in range(ch):
            for c in range(cw):
                out[r][curc+c]=crop[r][c]
        curc += cw + 1
    return out


def build_m86(case):
    h,w=case['size']
    g=blank(h,w)
    for item in case['items']:
        token=item['order']
        pat=item['pattern']
        color=item['color']
        top=item['top_left']
        place_shape(g, pat, top, color)
        # token one row above bbox top-left
        g[top[0]-1][top[1]]=token
    return g


def rule_m87(g):
    out=blank(*size(g))
    h,w=size(g)
    # preserve frames
    for r,row in enumerate(g):
        for c,v in enumerate(row):
            if v==1:
                out[r][c]=1
    for r0,c0,r1,c1 in find_rectangular_frames(g,1):
        a=g[r0+1][c0+1]
        b=g[r0+1][c1-1]
        for c in range(c0+1,c1):
            color=a if ((c-(c0+1))%2==0) else b
            for r in range(r0+1,r1):
                out[r][c]=color
    return out


def build_m87(case):
    h,w=case['size']
    g=blank(h,w)
    for frame in case['frames']:
        r0,c0,r1,c1=frame['box']
        draw_frame(g, frame['box'], 1)
        a,b=frame['colors']
        g[r0+1][c0+1]=a
        g[r0+1][c1-1]=b
    return g


def rule_m88(g):
    token=1
    cells=[]
    for r,row in enumerate(g):
        for c,v in enumerate(row):
            if v in (1,2,3,4):
                token=v
            elif v!=0:
                cells.append((r,c))
    crop=crop_bbox(g,cells)
    return transform_grid(crop, token)


def build_m88(case):
    h,w=case['size']
    g=blank(h,w)
    g[case['token_pos'][0]][case['token_pos'][1]]=case['token']
    # pattern may include explicit digits
    place_shape(g, case['pattern'], case['top_left'], None)
    return g


def rule_m89(g):
    comps=[(v,cells) for v,cells in components4(g) if v!=0]
    comps_sorted=sorted(comps, key=lambda vc: len(vc[1]))
    rank_color={}
    for i,(v,cells) in enumerate(comps_sorted, start=2):
        rank_color[id(cells)]=i  # can't key by cells? use list id
    out=blank(*size(g))
    for i,(v,cells) in enumerate(comps_sorted, start=2):
        for r,c in cells:
            out[r][c]=i
    return out


def build_m89(case):
    h,w=case['size']
    g=blank(h,w)
    for item in case['items']:
        place_shape(g, item['pattern'], item['top_left'], item['color'])
    return g


def rule_m90(g):
    h,w=size(g)
    out=clone(g)
    seen=set()
    for r in range(h):
        for c in range(w):
            if g[r][c]==0 and (r,c) not in seen:
                region=flood_region(g,(r,c),blocked={1})
                seen.update(region)
                colors={g[rr][cc] for rr,cc in region if g[rr][cc]!=0}
                if len(colors)==1:
                    color=next(iter(colors))
                    for rr,cc in region:
                        if g[rr][cc]!=1:
                            out[rr][cc]=color
    return out


def build_m90(case):
    h,w=case['size']
    g=blank(h,w)
    # draw outer frame and walls
    draw_frame(g, (0,0,h-1,w-1), 1)
    for line in case['walls']:
        if line['axis']=='v':
            c=line['index']
            for r in range(line.get('r0',0), line.get('r1',h-1)+1):
                g[r][c]=1
        else:
            r=line['index']
            for c in range(line.get('c0',0), line.get('c1',w-1)+1):
                g[r][c]=1
    for r,c,v in case['seeds']:
        g[r][c]=v
    return g


def rule_m91(g):
    h,w=size(g)
    mask_cells=[(r,c) for r,row in enumerate(g) for c,v in enumerate(row) if v==5]
    if not mask_cells:
        return blank(h,w)
    norm=normalize_cells(mask_cells)
    # exclude original mask and anchors from output
    out=blank(h,w)
    for r,row in enumerate(g):
        for c,v in enumerate(row):
            if v not in (0,5):
                for dr,dc in norm:
                    nr,nc=r+dr,c+dc
                    if 0<=nr<h and 0<=nc<w:
                        out[nr][nc]=v
    return out


def build_m91(case):
    h,w=case['size']
    g=blank(h,w)
    place_shape(g, case['mask_pattern'], case['mask_top_left'], 5)
    for r,c,v in case['anchors']:
        g[r][c]=v
    return g


def rule_h85(g):
    h,w=size(g)
    priority_colors=[v for v in g[0] if v!=0]
    priority={color:i for i,color in enumerate(priority_colors)}
    seeds=[(r-1,c,v) for r in range(1,h) for c,v in enumerate(g[r]) if v!=0]  # output coordinates shift up by 1
    painted=sprout_kernel(seeds, [(0,0),(-1,0),(1,0),(0,-1),(0,1)], priority=priority)
    out=blank(h-1,w)
    for (r,c),v in painted.items():
        if 0<=r<h-1 and 0<=c<w:
            out[r][c]=v
    return out


def build_h85(case):
    body_h, body_w = case['body_size']
    g=blank(body_h+1, body_w)
    positions=case.get('priority_positions')
    if positions is None:
        # spread colors with one zero gap when possible
        positions=list(range(0, min(body_w, 2*len(case['priority'])), 2))
        if len(positions)<len(case['priority']):
            positions=list(range(len(case['priority'])))
    for pos,color in zip(positions, case['priority']):
        g[0][pos]=color
    for r,c,v in case['seeds']:
        g[r+1][c]=v
    return g


def rule_h86(g):
    frames=find_rectangular_frames(g,1)
    # sort by top-left
    frames=sorted(frames)
    if len(frames)<3:
        return [[0]]
    A_box,B_box,C_box=frames[:3]
    A=crop_nonzero(extract_box_interior(g,A_box))
    B=crop_nonzero(extract_box_interior(g,B_box))
    C=crop_nonzero(extract_box_interior(g,C_box))
    tid=infer_transform(A,B)
    return apply_transform_by_id(C, tid)


def build_h86(case):
    h,w=case['size']
    g=blank(h,w)
    boxes=case['boxes']  # dict name->box
    for box in boxes.values():
        draw_frame(g, box, 1)
    # patterns are lists[str] digits; placed inside boxes at specified offsets
    for name, box in boxes.items():
        if name not in case['patterns']:
            continue
        pat=case['patterns'][name]
        inner_top_left=(box[0]+1+case.get('offsets',{}).get(name,(0,0))[0], box[1]+1+case.get('offsets',{}).get(name,(0,0))[1])
        place_shape(g, pat, inner_top_left, None)
    return g


def build_h86_case(case):
    A=case['A_pattern']
    tid=case['transform']
    A_grid=grid_from_strings([row.replace('.', '0') for row in A])
    B_grid=apply_transform_by_id(A_grid, tid)
    B_pattern=strings_from_grid(B_grid)
    data={'size':case['size'],'boxes':case['boxes'],'patterns':{'A':A,'B':B_pattern,'C':case['C_pattern']}}
    return build_h86(data)


def rule_h87(g):
    palette=[v for v in g[0] if v!=0]
    body=[row[:] for row in g[1:]]
    frames=find_rectangular_frames(body,1)
    # outer to inner by area descending or by bbox
    frames=sorted(frames, key=lambda b: ((b[2]-b[0]+1)*(b[3]-b[1]+1)), reverse=True)
    out=blank(*size(body))
    for idx,box in enumerate(frames):
        color=palette[idx] if idx < len(palette) else palette[-1]
        r0,c0,r1,c1=box
        for c in range(c0,c1+1):
            out[r0][c]=color; out[r1][c]=color
        for r in range(r0,r1+1):
            out[r][c0]=color; out[r][c1]=color
    return out


def build_h87(case):
    body_h,body_w=case['body_size']
    g=blank(body_h+1, body_w)
    for i,color in enumerate(case['palette']):
        g[0][i]=color
    for box in case['frames']:
        r0,c0,r1,c1=box
        for c in range(c0,c1+1):
            g[r0+1][c]=1; g[r1+1][c]=1
        for r in range(r0+1,r1+2):
            g[r][c0]=1; g[r][c1]=1
    return g


def rule_h88(g):
    frames=sorted(find_rectangular_frames(g,1), key=lambda b:(b[1],b[0]))
    pieces=[]
    for box in frames:
        r0,c0,r1,c1=box
        raw = g[r0-1][c0] if r0-1 >= 0 else 9
        token = TOKEN_MAP_H88.get(raw,1)
        interior=extract_box_interior(g,box)
        cells=[(r,c) for r,row in enumerate(interior) for c,v in enumerate(row) if v!=0]
        crop=crop_from_cells(interior,cells)
        pieces.append(transform_grid(crop, token))
    height=max(len(p) for p in pieces)
    width=sum(len(p[0]) for p in pieces)+(len(pieces)-1)
    out=blank(height,width)
    cur=0
    for piece in pieces:
        ph,pw=size(piece)
        for r in range(ph):
            for c in range(pw):
                out[r][cur+c]=piece[r][c]
        cur += pw + 1
    return out


def build_h88(case):
    h,w=case['size']
    g=blank(h,w)
    for item in case['boxes']:
        box=item['box']
        draw_frame(g, box, 1)
        token_raw=item['token_raw']
        g[box[0]-1][box[1]] = token_raw
        place_shape(g, item['pattern'], item['top_left'], None)
    return g


def rule_h89(g):
    frames=sorted(find_rectangular_frames(g,1), key=lambda b:(b[1],b[0]))
    classes=[]
    for box in frames:
        interior=extract_box_interior(g,box)
        crop=binary_crop_from_interior(interior)
        classes.append(symmetry_class(crop))
    n=len(classes)
    out=blank(n,n)
    for i in range(n):
        for j in range(n):
            out[i][j]=2 if classes[i]==classes[j] else 0
    return out


def build_h89(case):
    h,w=case['size']
    g=blank(h,w)
    for item in case['boxes']:
        draw_frame(g, item['box'], 1)
        place_shape(g, item['pattern'], item['top_left'], item.get('color',5))
    return g


def build_h89_case(case):
    return build_h89(case)


def rule_h90(g):
    h,w=size(g)
    out=clone(g)
    pos=defaultdict(list)
    for r,row in enumerate(g):
        for c,v in enumerate(row):
            if v not in (0,8):
                pos[v].append((r,c))
    for color in sorted(pos):
        cells=pos[color]
        if len(cells)!=2:
            continue
        start,goal=cells
        blocked={(r,c) for r,row in enumerate(out) for c,v in enumerate(row) if v==8 or (v not in (0,color,8))}
        temp=blank(h,w)
        for r,c in blocked:
            temp[r][c]=8
        path=shortest_path(temp,start,goal,blocked={8},order=[(0,1),(1,0),(0,-1),(-1,0)])
        for r,c in path:
            out[r][c]=color
    return out


def build_h90(case):
    h,w=case['size']
    g=blank(h,w)
    for r,c in case['walls']:
        g[r][c]=8
    for color,p1,p2 in case['pairs']:
        g[p1[0]][p1[1]]=color
        g[p2[0]][p2[1]]=color
    return g


def rule_h91(g):
    h,w=size(g)
    # parse legend from first two rows: columns with row1 nonzero => mapping color -> token row0 same col
    mapping={}
    for c in range(w):
        color=g[1][c]
        token=g[0][c]
        if color!=0 and token in TOKEN_MAP_H91:
            mapping[color]=TOKEN_MAP_H91[token]
    source_cells=[(r-2,c) for r in range(2,h) for c,v in enumerate(g[r]) if v==5]
    if not source_cells:
        return blank(h-2,w)
    norm=normalize_cells(source_cells)
    out=blank(h-2,w)
    for r in range(2,h):
        for c,v in enumerate(g[r]):
            if v!=0 and v!=5:
                tid=mapping[v]
                coords=transform_coords(norm, tid)
                for dr,dc in coords:
                    nr,nc=(r-2)+dr,c+dc
                    if 0<=nr<h-2 and 0<=nc<w:
                        out[nr][nc]=v
    return out


def build_h91(case):
    body_h,body_w=case['body_size']
    g=blank(body_h+2, body_w)
    for col,(token_raw,color) in case['legend'].items():
        g[0][col]=token_raw
        g[1][col]=color
    place_shape(g, case['source_pattern'], (case['source_top_left'][0]+2, case['source_top_left'][1]), 5)
    for r,c,v in case['anchors']:
        g[r+2][c]=v
    return g


TRANSFORMS = {
    1: lambda g: clone(g),
    2: rotate90,
    3: rotate180,
    4: rotate270,
    5: flip_h,
    6: flip_v,
}


PUZZLE_SPECS = {'E85': {'train': [{'size': (7, 7), 'seeds': [(2, 2, 5), (4, 5, 7)]},
                   {'size': (8, 8), 'seeds': [(1, 5, 6), (5, 2, 4)]},
                   {'size': (6, 9), 'seeds': [(1, 1, 3), (3, 6, 8)]},
                   {'size': (9, 6), 'seeds': [(2, 3, 2), (6, 1, 9)]}],
         'test': {'size': (8, 9), 'seeds': [(2, 2, 6), (5, 6, 4), (1, 7, 7)]},
         'title': 'Sprout Plus Seeds',
         'difficulty': 'easy',
         'skills': ['local expansion', 'seed-based transform', 'same-size'],
         'staged_hint': 'Treat every nonzero cell as a seed. Then apply the same tiny offset pattern around it.',
         'written_solution': 'Every nonzero seed cell grows into a plus: keep the center and add the four cardinal '
                             'neighbors in the same color, clipped by the grid edges.',
         'uses_new_primitive': True},
 'E86': {'train': [{'size': (7, 9), 'segments': [(2, (1, 1), (1, 6)), (6, (2, 7), (5, 7))]},
                   {'size': (8, 8), 'segments': [(5, (6, 1), (2, 1)), (7, (4, 3), (4, 6))]},
                   {'size': (6, 10), 'segments': [(3, (0, 2), (4, 2)), (8, (5, 5), (5, 8))]},
                   {'size': (9, 7), 'segments': [(4, (2, 4), (7, 4)), (9, (1, 0), (1, 3))]}],
         'test': {'size': (8, 10), 'segments': [(5, (0, 4), (6, 4)), (7, (3, 1), (3, 8))]},
         'title': 'Bridge Matching Endpoints',
         'difficulty': 'easy',
         'skills': ['line completion', 'pair matching', 'row/column reasoning'],
         'staged_hint': 'Find colors that appear exactly twice. If the pair is aligned, fill the straight path between '
                        'them.',
         'written_solution': 'Each color forms exactly one aligned pair. Fill the full horizontal or vertical segment '
                             'between the two endpoints, inclusive.',
         'uses_new_primitive': False},
 'E87': {'train': [{'size': (8, 9), 'pairs': [(2, (1, 1), (5, 4)), (6, (2, 6), (4, 8))]},
                   {'size': (9, 9), 'pairs': [(5, (0, 5), (3, 8)), (7, (4, 1), (8, 4))]},
                   {'size': (7, 10), 'pairs': [(3, (1, 2), (5, 6)), (8, (0, 8), (2, 9))]},
                   {'size': (10, 8), 'pairs': [(4, (2, 0), (6, 3)), (9, (5, 5), (8, 7))]}],
         'test': {'size': (9, 10), 'pairs': [(2, (1, 1), (6, 5)), (7, (3, 7), (8, 9))]},
         'title': 'Diagonal Corners to Outline',
         'difficulty': 'easy',
         'skills': ['rectangle inference', 'outline drawing', 'group by color'],
         'staged_hint': 'Each color gives two diagonal corners. Recover the rectangle they imply, then draw just the '
                        'border.',
         'written_solution': 'For each color, interpret the two cells as opposite corners of an axis-aligned rectangle '
                             'and draw that rectangle’s outline.',
         'uses_new_primitive': False},
 'E88': {'train': [{'size': (7, 9), 'axis': 'v', 'guide': 4, 'shape': [(1, 2, 5), (2, 2, 5), (2, 3, 5)]},
                   {'size': (9, 8), 'axis': 'h', 'guide': 4, 'shape': [(1, 1, 6), (1, 2, 6), (2, 2, 6), (3, 2, 6)]},
                   {'size': (8, 10), 'axis': 'v', 'guide': 6, 'shape': [(4, 2, 7), (5, 2, 7), (5, 3, 7), (6, 3, 7)]},
                   {'size': (10, 9), 'axis': 'h', 'guide': 6, 'shape': [(2, 5, 3), (3, 4, 3), (3, 5, 3), (3, 6, 3)]}],
         'test': {'size': (9, 11), 'axis': 'v', 'guide': 5, 'shape': [(2, 2, 4), (3, 2, 4), (3, 3, 4), (4, 3, 4)]},
         'title': 'Mirror Across the Guide',
         'difficulty': 'easy',
         'skills': ['reflection', 'guide detection', 'same-size'],
         'staged_hint': 'First find the full guide line of 8s. Then copy every colored cell to the symmetric location '
                        'across that line.',
         'written_solution': 'The all-8 row or column is a mirror. Keep the original shape and add its reflected copy '
                             'across the guide.',
         'uses_new_primitive': False},
 'E89': {'train': [{'size': (5, 6), 'cells': [(0, 0, 4), (1, 4, 2), (2, 2, 4), (4, 5, 3)]},
                   {'size': (6, 7), 'cells': [(0, 6, 5), (2, 1, 2), (3, 4, 5), (5, 0, 2), (4, 6, 3)]},
                   {'size': (7, 7), 'cells': [(1, 1, 6), (1, 5, 4), (3, 3, 4), (5, 2, 6), (6, 6, 2)]},
                   {'size': (5, 8), 'cells': [(0, 7, 3), (2, 2, 7), (2, 5, 7), (4, 0, 3), (4, 4, 5)]}],
         'test': {'size': (6, 8), 'cells': [(0, 1, 4), (1, 6, 2), (2, 3, 4), (3, 0, 5), (4, 7, 2), (5, 4, 5)]},
         'title': 'Count and Sort Colors',
         'difficulty': 'easy',
         'skills': ['counting', 'sorting', 'dynamic-width output'],
         'staged_hint': 'Ignore position and just count how often each color appears. The output is a single row in '
                        'ascending color order.',
         'written_solution': 'Count every nonzero color, then output one row containing each color repeated by its '
                             'count, sorted from smallest color number to largest.',
         'uses_new_primitive': False},
 'E90': {'train': [{'size': (7, 7), 'seeds': [(2, 2, 5), (4, 5, 7)]},
                   {'size': (8, 9), 'seeds': [(1, 6, 3), (5, 2, 8)]},
                   {'size': (6, 8), 'seeds': [(3, 4, 6), (1, 1, 2)]},
                   {'size': (9, 6), 'seeds': [(2, 3, 9), (6, 1, 4)]}],
         'test': {'size': (8, 8), 'seeds': [(2, 2, 6), (5, 5, 3)]},
         'title': 'Seed to 3x3 Frame',
         'difficulty': 'easy',
         'skills': ['local geometry', 'outline generation', 'same-size'],
         'staged_hint': 'Around each seed, think of the surrounding 3×3 box. Paint only its border, not the center.',
         'written_solution': 'Every seed becomes the outline of a 3×3 square centered on that seed, using the seed’s '
                             'color and clipping at the edges.',
         'uses_new_primitive': False},
 'E91': {'train': [{'size': (8, 9), 'arrow': (0, 0, 2), 'shape': [(3, 2, 5), (3, 3, 5), (4, 2, 5)]},
                   {'size': (9, 8), 'arrow': (8, 7, 1), 'shape': [(5, 3, 6), (6, 2, 6), (6, 3, 6), (6, 4, 6)]},
                   {'size': (7, 10), 'arrow': (0, 9, 3), 'shape': [(1, 5, 7), (2, 5, 7), (2, 6, 7)]},
                   {'size': (10, 7), 'arrow': (9, 0, 4), 'shape': [(4, 4, 8), (5, 4, 8), (5, 5, 8), (6, 5, 8)]}],
         'test': {'size': (8, 10), 'arrow': (0, 0, 2), 'shape': [(2, 3, 4), (3, 3, 4), (3, 4, 4), (4, 4, 4)]},
         'title': 'One-Step Shift',
         'difficulty': 'easy',
         'skills': ['direction token', 'rigid motion', 'same-size'],
         'staged_hint': 'Read the arrow cell first. Then move the whole non-arrow shape by exactly one step in that '
                        'direction.',
         'written_solution': 'Ignore the arrow in the output and shift the entire colored component by one cell in the '
                             'arrow’s direction.',
         'uses_new_primitive': False},
 'M85': {'train': [{'size': (11, 13),
                    'frames': [{'box': (1, 1, 5, 5), 'seed': (3, 3, 6), 'token': (2, 2, 2)},
                               {'box': (1, 8, 5, 11), 'seed': (3, 9, 5), 'token': (2, 10, 4)}]},
                   {'size': (10, 14),
                    'frames': [{'box': (1, 2, 6, 6), 'seed': (3, 4, 7), 'token': (2, 3, 3)},
                               {'box': (2, 9, 7, 12), 'seed': (5, 10, 8), 'token': (4, 11, 2)}]},
                   {'size': (12, 15),
                    'frames': [{'box': (1, 1, 6, 5), 'seed': (4, 3, 5), 'token': (2, 4, 4)},
                               {'box': (1, 9, 6, 13), 'seed': (3, 11, 6), 'token': (4, 10, 3)}]},
                   {'size': (11, 14),
                    'frames': [{'box': (2, 1, 7, 5), 'seed': (4, 3, 8), 'token': (3, 2, 2)},
                               {'box': (2, 8, 8, 12), 'seed': (5, 10, 7), 'token': (4, 11, 4)}]}],
         'test': {'size': (12, 15),
                  'frames': [{'box': (1, 2, 6, 6), 'seed': (4, 4, 6), 'token': (2, 3, 2)},
                             {'box': (2, 9, 8, 13), 'seed': (5, 11, 5), 'token': (4, 10, 3)}]},
         'title': 'Token-Specific Kernels in Frames',
         'difficulty': 'medium',
         'skills': ['frame localization', 'seed expansion', 'symbol-conditioned rule'],
         'staged_hint': 'Work frame by frame. Inside each frame, find the seed color and the token that selects which '
                        'local kernel to paint.',
         'written_solution': 'Each border-1 frame contains one seed and one token. The token chooses a kernel '
                             'shape—plus, X, or full 3×3—and that kernel is painted in the seed color, clipped to the '
                             'frame interior.',
         'uses_new_primitive': True},
 'M86': {'train': [{'size': (9, 15),
                    'items': [{'order': 2, 'pattern': ['#..', '###'], 'color': 5, 'top_left': (3, 6)},
                              {'order': 1, 'pattern': ['#.#', '###'], 'color': 6, 'top_left': (5, 1)},
                              {'order': 3, 'pattern': ['##.', '.##'], 'color': 7, 'top_left': (2, 11)}]},
                   {'size': (10, 16),
                    'items': [{'order': 3, 'pattern': ['#..', '##.', '###'], 'color': 8, 'top_left': (4, 11)},
                              {'order': 1, 'pattern': ['##.', '#..', '#..'], 'color': 5, 'top_left': (3, 2)},
                              {'order': 2, 'pattern': ['###', '.#.'], 'color': 6, 'top_left': (6, 7)}]},
                   {'size': (9, 17),
                    'items': [{'order': 2, 'pattern': ['.##', '##.'], 'color': 7, 'top_left': (2, 7)},
                              {'order': 1, 'pattern': ['#..', '.#.', '..#'], 'color': 8, 'top_left': (5, 1)},
                              {'order': 3, 'pattern': ['###', '#.#', '###'], 'color': 5, 'top_left': (3, 12)}]},
                   {'size': (10, 15),
                    'items': [{'order': 1, 'pattern': ['#..', '##.', '###'], 'color': 6, 'top_left': (2, 2)},
                              {'order': 3, 'pattern': ['#.#', '###'], 'color': 7, 'top_left': (5, 10)},
                              {'order': 2, 'pattern': ['##.', '#..', '#..'], 'color': 5, 'top_left': (4, 6)}]}],
         'test': {'size': (10, 16),
                  'items': [{'order': 3, 'pattern': ['#..', '###'], 'color': 8, 'top_left': (4, 11)},
                            {'order': 1, 'pattern': ['.#.', '###', '.#.'], 'color': 5, 'top_left': (3, 2)},
                            {'order': 2, 'pattern': ['.##', '##.'], 'color': 6, 'top_left': (6, 7)}]},
         'title': 'Ordered Normalized Pack',
         'difficulty': 'medium',
         'skills': ['component extraction', 'token ordering', 'packing'],
         'staged_hint': 'Ignore location first and crop each component to its own tight box. Then sort those crops by '
                        'the nearby order token.',
         'written_solution': 'Every component has an order token placed one row above its top-left corner. Crop each '
                             'component to its minimal box, sort by token value, and pack the crops left to right with '
                             'one empty column between them.',
         'uses_new_primitive': False},
 'M87': {'train': [{'size': (10, 14),
                    'frames': [{'box': (1, 1, 5, 6), 'colors': (5, 6)}, {'box': (2, 8, 8, 12), 'colors': (2, 7)}]},
                   {'size': (11, 15),
                    'frames': [{'box': (1, 2, 6, 7), 'colors': (3, 8)}, {'box': (3, 10, 9, 13), 'colors': (6, 4)}]},
                   {'size': (12, 16),
                    'frames': [{'box': (2, 1, 8, 5), 'colors': (7, 2)}, {'box': (1, 9, 6, 14), 'colors': (5, 3)}]},
                   {'size': (10, 15),
                    'frames': [{'box': (1, 1, 6, 6), 'colors': (8, 4)}, {'box': (2, 9, 8, 13), 'colors': (6, 2)}]}],
         'test': {'size': (11, 16),
                  'frames': [{'box': (1, 2, 7, 7), 'colors': (7, 5)}, {'box': (2, 10, 9, 14), 'colors': (3, 8)}]},
         'title': 'Corner-Marker Stripe Fill',
         'difficulty': 'medium',
         'skills': ['frame reasoning', 'interior fill', 'alternating pattern'],
         'staged_hint': 'Inside each frame, read the two marker colors at the top corners. Then extend them as '
                        'alternating vertical stripes.',
         'written_solution': 'For each border-1 frame, the two cells just inside the top corners specify two colors. '
                             'Fill the frame interior with alternating vertical stripes starting with the left marker '
                             'color.',
         'uses_new_primitive': False},
 'M88': {'train': [{'size': (8, 8),
                    'token': 2,
                    'token_pos': (0, 0),
                    'pattern': ['56.', '.6.', '.77'],
                    'top_left': (3, 2)},
                   {'size': (9, 9),
                    'token': 3,
                    'token_pos': (8, 8),
                    'pattern': ['5.6', '556', '..7'],
                    'top_left': (2, 3)},
                   {'size': (8, 10),
                    'token': 4,
                    'token_pos': (0, 9),
                    'pattern': ['67.', '.75', '..5'],
                    'top_left': (3, 4)},
                   {'size': (9, 8),
                    'token': 1,
                    'token_pos': (8, 0),
                    'pattern': ['5..', '565', '.77'],
                    'top_left': (2, 2)}],
         'test': {'size': (9, 10), 'token': 2, 'token_pos': (0, 0), 'pattern': ['57', '65', '55'], 'top_left': (3, 4)},
         'title': 'Crop and Rotate by Token',
         'difficulty': 'medium',
         'skills': ['cropping', 'rotation', 'symbol decoding'],
         'staged_hint': 'Separate the token from the actual motif. Crop the motif tightly, then rotate it according to '
                        'the token.',
         'written_solution': 'Ignore the token cell when finding the motif. Crop the motif to its bounding box and '
                             'rotate it: 1 means none, 2 means 90°, 3 means 180°, and 4 means 270°.',
         'uses_new_primitive': False},
 'M89': {'train': [{'size': (10, 12),
                    'items': [{'pattern': ['##', '#.'], 'top_left': (6, 8), 'color': 7},
                              {'pattern': ['##', '##'], 'top_left': (1, 1), 'color': 5},
                              {'pattern': ['###', '.##'], 'top_left': (1, 6), 'color': 6}]},
                   {'size': (11, 13),
                    'items': [{'pattern': ['#', '#', '#'], 'top_left': (2, 2), 'color': 5},
                              {'pattern': ['##', '##'], 'top_left': (2, 8), 'color': 6},
                              {'pattern': ['###', '.##'], 'top_left': (7, 8), 'color': 7}]},
                   {'size': (10, 14),
                    'items': [{'pattern': ['#', '#', '#'], 'top_left': (1, 2), 'color': 8},
                              {'pattern': ['###', '..#'], 'top_left': (5, 1), 'color': 5},
                              {'pattern': ['###', '.##'], 'top_left': (4, 8), 'color': 6}]},
                   {'size': (12, 12),
                    'items': [{'pattern': ['##', '#.'], 'top_left': (2, 2), 'color': 7},
                              {'pattern': ['###', '.##'], 'top_left': (6, 7), 'color': 5},
                              {'pattern': ['##', '##'], 'top_left': (1, 8), 'color': 6}]}],
         'test': {'size': (11, 13),
                  'items': [{'pattern': ['#', '#', '#'], 'top_left': (2, 1), 'color': 8},
                            {'pattern': ['##', '##'], 'top_left': (6, 3), 'color': 5},
                            {'pattern': ['###', '##.'], 'top_left': (4, 8), 'color': 6}]},
         'title': 'Area-Rank Recoloring',
         'difficulty': 'medium',
         'skills': ['component area', 'ranking', 'recolor'],
         'staged_hint': 'Do not care about original colors. Measure component sizes first, then replace colors by size '
                        'rank.',
         'written_solution': 'Find the separate components, sort them by area from smallest to largest, and recolor '
                             'them with 2, 3, 4 in that order while keeping the shapes in place.',
         'uses_new_primitive': False},
 'M90': {'train': [{'size': (9, 11),
                    'walls': [{'axis': 'v', 'index': 5}, {'axis': 'h', 'index': 4, 'c0': 5, 'c1': 10}],
                    'seeds': [(2, 2, 5), (2, 8, 6), (6, 8, 7)]},
                   {'size': (10, 12),
                    'walls': [{'axis': 'v', 'index': 4},
                              {'axis': 'v', 'index': 8},
                              {'axis': 'h', 'index': 5, 'c0': 4, 'c1': 8}],
                    'seeds': [(2, 2, 3), (2, 6, 5), (7, 10, 7)]},
                   {'size': (11, 11),
                    'walls': [{'axis': 'h', 'index': 5}, {'axis': 'v', 'index': 5, 'r0': 5, 'r1': 10}],
                    'seeds': [(2, 2, 6), (2, 8, 4), (8, 8, 9)]},
                   {'size': (9, 13),
                    'walls': [{'axis': 'v', 'index': 6}, {'axis': 'h', 'index': 3, 'c0': 6, 'c1': 12}],
                    'seeds': [(1, 2, 5), (6, 2, 8), (6, 9, 4)]}],
         'test': {'size': (10, 13),
                  'walls': [{'axis': 'v', 'index': 6}, {'axis': 'h', 'index': 5, 'c0': 6, 'c1': 12}],
                  'seeds': [(2, 2, 3), (2, 9, 7), (7, 9, 5)]},
         'title': 'Fill Chambers from Seeds',
         'difficulty': 'medium',
         'skills': ['flood fill', 'wall constraints', 'region ownership'],
         'staged_hint': 'Treat the 1-cells as walls. Each chamber with exactly one seed should be flood-filled in the '
                        'seed’s color.',
         'written_solution': 'The walls split the board into chambers. Any chamber that contains one seed gets filled '
                             'completely with that seed’s color, while the walls remain unchanged.',
         'uses_new_primitive': False},
 'M91': {'train': [{'size': (10, 14),
                    'mask_pattern': ['##.', '.##'],
                    'mask_top_left': (1, 1),
                    'anchors': [(1, 9, 2), (5, 7, 3)]},
                   {'size': (11, 15),
                    'mask_pattern': ['###', '.#.'],
                    'mask_top_left': (2, 2),
                    'anchors': [(1, 10, 4), (6, 8, 6)]},
                   {'size': (9, 13),
                    'mask_pattern': ['##', '#.'],
                    'mask_top_left': (1, 1),
                    'anchors': [(2, 8, 7), (5, 9, 3), (6, 5, 2)]},
                   {'size': (10, 16),
                    'mask_pattern': ['#.#', '###'],
                    'mask_top_left': (2, 1),
                    'anchors': [(1, 11, 8), (6, 10, 4)]}],
         'test': {'size': (11, 15),
                  'mask_pattern': ['##.', '.##'],
                  'mask_top_left': (1, 1),
                  'anchors': [(2, 9, 2), (6, 10, 6), (7, 4, 3)]},
         'title': 'Stamp the Mask at Anchors',
         'difficulty': 'medium',
         'skills': ['mask extraction', 'translation', 'recoloring'],
         'staged_hint': 'First isolate the 5-mask and normalize it to its top-left corner. Then stamp that shape at '
                        'every anchor cell in the anchor’s color.',
         'written_solution': 'Extract the pattern made by the 5-cells, normalize it, remove it, and stamp that same '
                             'pattern at each nonzero anchor using the anchor’s color and position as the top-left '
                             'origin.',
         'uses_new_primitive': False},
 'H85': {'train': [{'body_size': (7, 9), 'priority': [6, 4, 5], 'seeds': [(2, 2, 5), (2, 4, 4), (4, 3, 6)]},
                   {'body_size': (8, 10), 'priority': [7, 5, 3], 'seeds': [(1, 2, 3), (3, 4, 5), (3, 6, 7), (5, 5, 3)]},
                   {'body_size': (9, 9), 'priority': [8, 6, 4], 'seeds': [(2, 2, 4), (2, 4, 6), (2, 6, 8), (5, 4, 4)]},
                   {'body_size': (8, 11),
                    'priority': [5, 7, 2],
                    'seeds': [(2, 3, 2), (3, 5, 7), (5, 4, 5), (5, 6, 2)]}],
         'test': {'body_size': (9, 10), 'priority': [6, 3, 8], 'seeds': [(2, 2, 8), (3, 4, 3), (4, 6, 6), (6, 4, 8)]},
         'title': 'Priority Sprouts',
         'difficulty': 'hard',
         'skills': ['conflict resolution', 'kernel expansion', 'legend priority'],
         'staged_hint': 'Ignore overlaps at first: every seed sprouts a plus. Then resolve conflicts using the '
                        'priority strip from left to right.',
         'written_solution': 'The top row gives a priority ordering of colors. In the body, each seed grows a plus of '
                             'radius 1, and whenever two sprouts compete for the same cell, the higher-priority color '
                             'wins. The output drops the priority row.',
         'uses_new_primitive': True},
 'H86': {'train': [{'size': (13, 15),
                    'boxes': {'A': (0, 0, 4, 4), 'B': (0, 8, 4, 12), 'C': (7, 0, 11, 4)},
                    'A_pattern': ['56.', '.6.', '.77'],
                    'C_pattern': ['5.', '55', '65'],
                    'transform': 2},
                   {'size': (13, 16),
                    'boxes': {'A': (0, 1, 5, 5), 'B': (0, 10, 5, 14), 'C': (7, 1, 11, 5)},
                    'A_pattern': ['5.6', '556', '..7'],
                    'C_pattern': ['67.', '.75', '..5'],
                    'transform': 3},
                   {'size': (13, 15),
                    'boxes': {'A': (0, 0, 4, 4), 'B': (0, 8, 4, 12), 'C': (7, 0, 11, 4)},
                    'A_pattern': ['5..', '565', '.77'],
                    'C_pattern': ['57', '65', '55'],
                    'transform': 5},
                   {'size': (14, 16),
                    'boxes': {'A': (0, 1, 5, 5), 'B': (0, 10, 5, 14), 'C': (8, 1, 12, 5)},
                    'A_pattern': ['67.', '.75', '..5'],
                    'C_pattern': ['56.', '.6.', '.77'],
                    'transform': 4}],
         'test': {'size': (13, 15),
                  'boxes': {'A': (0, 0, 4, 4), 'B': (0, 8, 4, 12), 'C': (7, 0, 11, 4)},
                  'A_pattern': ['57', '65', '55'],
                  'C_pattern': ['5.6', '556', '..7'],
                  'transform': 2},
         'title': 'A:B::C Transform Analogy',
         'difficulty': 'hard',
         'skills': ['analogy', 'transform inference', 'cropping'],
         'staged_hint': 'Do not use the bottom motif first. Infer the transformation from A to B, then apply exactly '
                        'that transformation to C.',
         'written_solution': 'The top pair demonstrates a transformation such as rotation or reflection. Infer that '
                             'transform from A→B, crop C tightly, and output the transformed version of C.',
         'uses_new_primitive': False},
 'H87': {'train': [{'body_size': (11, 11),
                    'palette': [2, 3, 4],
                    'frames': [(0, 0, 10, 10), (2, 2, 8, 8), (4, 4, 6, 6)]},
                   {'body_size': (15, 15),
                    'palette': [5, 7, 2, 3],
                    'frames': [(0, 0, 14, 14), (2, 2, 12, 12), (4, 4, 10, 10), (6, 6, 8, 8)]},
                   {'body_size': (12, 12),
                    'palette': [8, 4, 6],
                    'frames': [(0, 0, 11, 11), (2, 2, 9, 9), (4, 4, 7, 7)]},
                   {'body_size': (14, 10),
                    'palette': [3, 5, 7],
                    'frames': [(0, 0, 13, 9), (2, 2, 11, 7), (4, 3, 9, 6)]}],
         'test': {'body_size': (13, 11), 'palette': [4, 6, 8], 'frames': [(0, 0, 12, 10), (2, 2, 10, 8), (4, 3, 8, 7)]},
         'title': 'Palette-Depth Nested Frames',
         'difficulty': 'hard',
         'skills': ['nesting depth', 'palette mapping', 'frame detection'],
         'staged_hint': 'First identify the nested frame layers in the body. Then map outermost to innermost layers '
                        'onto the palette order from the top strip.',
         'written_solution': 'The top strip lists colors in depth order. Recolor the nested border-1 frames from '
                             'outermost to innermost using that palette, and output only the body.',
         'uses_new_primitive': False},
 'H88': {'train': [{'size': (9, 21),
                    'boxes': [{'box': (2, 1, 7, 5), 'token_raw': 2, 'pattern': ['56.', '.67'], 'top_left': (4, 2)},
                              {'box': (2, 9, 7, 13), 'token_raw': 3, 'pattern': ['7.', '77'], 'top_left': (4, 10)},
                              {'box': (2, 16, 7, 19), 'token_raw': 9, 'pattern': ['55', '65'], 'top_left': (4, 17)}]},
                   {'size': (10, 23),
                    'boxes': [{'box': (3, 1, 8, 5),
                               'token_raw': 4,
                               'pattern': ['5.6', '556', '..7'],
                               'top_left': (5, 2)},
                              {'box': (3, 9, 8, 13),
                               'token_raw': 2,
                               'pattern': ['57', '65', '55'],
                               'top_left': (5, 10)},
                              {'box': (3, 17, 8, 21),
                               'token_raw': 9,
                               'pattern': ['67.', '.75', '..5'],
                               'top_left': (5, 18)}]},
                   {'size': (9, 22),
                    'boxes': [{'box': (2, 1, 7, 5),
                               'token_raw': 9,
                               'pattern': ['5..', '565', '.77'],
                               'top_left': (4, 2)},
                              {'box': (2, 9, 7, 13),
                               'token_raw': 4,
                               'pattern': ['56.', '.6.', '.77'],
                               'top_left': (4, 10)},
                              {'box': (2, 17, 7, 20), 'token_raw': 3, 'pattern': ['55', '65'], 'top_left': (4, 18)}]},
                   {'size': (10, 22),
                    'boxes': [{'box': (3, 1, 8, 5),
                               'token_raw': 2,
                               'pattern': ['67.', '.75', '..5'],
                               'top_left': (5, 2)},
                              {'box': (3, 9, 8, 13), 'token_raw': 9, 'pattern': ['56.', '.67'], 'top_left': (5, 10)},
                              {'box': (3, 17, 8, 20), 'token_raw': 4, 'pattern': ['55', '65'], 'top_left': (5, 18)}]}],
         'test': {'size': (9, 21),
                  'boxes': [{'box': (2, 1, 7, 5), 'token_raw': 4, 'pattern': ['57', '65', '55'], 'top_left': (4, 2)},
                            {'box': (2, 9, 7, 13),
                             'token_raw': 2,
                             'pattern': ['5..', '565', '.77'],
                             'top_left': (4, 10)},
                            {'box': (2, 16, 7, 19), 'token_raw': 9, 'pattern': ['55', '65'], 'top_left': (4, 17)}]},
         'title': 'Rotate, Crop, and Pack the Boxes',
         'difficulty': 'hard',
         'skills': ['box parsing', 'tokened transforms', 'packing'],
         'staged_hint': 'Solve each box independently first: token → rotate → crop. Only after that should you pack '
                        'the results left to right.',
         'written_solution': 'Each framed box has a transform token just above it. Crop the motif inside each box, '
                             'apply that box’s rotation token (9 means none), then pack the transformed crops left to '
                             'right with a one-column gap.',
         'uses_new_primitive': False},
 'H89': {'train': [{'size': (9, 23),
                    'boxes': [{'box': (2, 1, 7, 6), 'pattern': ['.#.', '###', '.#.'], 'top_left': (4, 3), 'color': 5},
                              {'box': (2, 9, 7, 14), 'pattern': ['##.', '.##'], 'top_left': (4, 11), 'color': 5},
                              {'box': (2, 17, 7, 22), 'pattern': ['##', '##'], 'top_left': (4, 19), 'color': 5}]},
                   {'size': (9, 23),
                    'boxes': [{'box': (2, 1, 7, 6), 'pattern': ['###', '.#.'], 'top_left': (4, 2), 'color': 5},
                              {'box': (2, 9, 7, 14), 'pattern': ['##.', '###'], 'top_left': (4, 10), 'color': 5},
                              {'box': (2, 17, 7, 22),
                               'pattern': ['.#.', '###', '.#.'],
                               'top_left': (4, 19),
                               'color': 5}]},
                   {'size': (9, 23),
                    'boxes': [{'box': (2, 1, 7, 6), 'pattern': ['##.', '.##'], 'top_left': (4, 3), 'color': 5},
                              {'box': (2, 9, 7, 14), 'pattern': ['###', '.#.'], 'top_left': (4, 10), 'color': 5},
                              {'box': (2, 17, 7, 22), 'pattern': ['###', '###'], 'top_left': (4, 19), 'color': 5}]},
                   {'size': (9, 23),
                    'boxes': [{'box': (2, 1, 7, 6), 'pattern': ['##.', '###'], 'top_left': (4, 2), 'color': 5},
                              {'box': (2, 9, 7, 14), 'pattern': ['##.', '.##'], 'top_left': (4, 10), 'color': 5},
                              {'box': (2, 17, 7, 22), 'pattern': ['##.', '###'], 'top_left': (4, 18), 'color': 5}]}],
         'test': {'size': (9, 23),
                  'boxes': [{'box': (2, 1, 7, 6), 'pattern': ['###', '.#.'], 'top_left': (4, 2), 'color': 5},
                            {'box': (2, 9, 7, 14), 'pattern': ['##.', '###'], 'top_left': (4, 10), 'color': 5},
                            {'box': (2, 17, 7, 22), 'pattern': ['##.', '.##'], 'top_left': (4, 19), 'color': 5}]},
         'title': 'Symmetry-Class Equality Matrix',
         'difficulty': 'hard',
         'skills': ['symmetry classification', 'comparison matrix', 'shape analysis'],
         'staged_hint': 'Classify each motif first: horizontal-symmetric, vertical-symmetric, both, or neither. Then '
                        'compare the classes pairwise.',
         'written_solution': 'The three framed motifs must be classified by symmetry. Output a 3×3 matrix with 2 '
                             'wherever two motifs share the same symmetry class and 0 otherwise.',
         'uses_new_primitive': False},
 'H90': {'train': [{'size': (11, 11),
                    'walls': [(0, 5), (1, 5), (3, 5), (4, 5), (5, 5), (6, 5), (7, 5), (9, 5), (10, 5)],
                    'pairs': [(2, (1, 1), (1, 9)), (3, (9, 1), (9, 9))]},
                   {'size': (11, 12),
                    'walls': [(0, 6), (1, 6), (2, 6), (4, 6), (5, 6), (6, 6), (8, 6), (9, 6), (10, 6)],
                    'pairs': [(2, (1, 2), (1, 10)), (4, (9, 2), (9, 10))]},
                   {'size': (10, 11),
                    'walls': [(0, 5), (2, 5), (3, 5), (4, 5), (5, 5), (7, 5), (8, 5), (9, 5)],
                    'pairs': [(3, (2, 1), (2, 9)), (7, (8, 1), (8, 9))]},
                   {'size': (12, 12),
                    'walls': [(0, 6), (1, 6), (3, 6), (4, 6), (5, 6), (6, 6), (7, 6), (8, 6), (10, 6), (11, 6)],
                    'pairs': [(2, (1, 1), (1, 10)), (5, (10, 1), (10, 10))]}],
         'test': {'size': (11, 11),
                  'walls': [(0, 5), (1, 5), (2, 5), (4, 5), (5, 5), (6, 5), (8, 5), (9, 5), (10, 5)],
                  'pairs': [(2, (1, 1), (1, 9)), (6, (9, 1), (9, 9))]},
         'title': 'Route Pairs Around the Wall',
         'difficulty': 'hard',
         'skills': ['path finding', 'obstacles', 'multi-object routing'],
         'staged_hint': 'Treat the 8-cells as blocked. For each color pair, find the shortest open route connecting '
                        'the endpoints and paint that route.',
         'written_solution': 'The matching colored terminals must be connected through empty cells while avoiding the '
                             '8-wall. Draw the shortest path for each pair, preserving walls and terminals.',
         'uses_new_primitive': False},
 'H91': {'train': [{'body_size': (10, 14),
                    'legend': {0: (9, 2), 2: (2, 3), 4: (3, 4)},
                    'source_pattern': ['##.', '.##'],
                    'source_top_left': (0, 7),
                    'anchors': [(4, 1, 2), (5, 8, 3), (7, 10, 4)]},
                   {'body_size': (11, 15),
                    'legend': {0: (4, 2), 2: (9, 5), 4: (2, 7)},
                    'source_pattern': ['###', '.#.'],
                    'source_top_left': (0, 8),
                    'anchors': [(4, 1, 2), (6, 8, 5), (7, 11, 7)]},
                   {'body_size': (10, 16),
                    'legend': {0: (3, 3), 2: (2, 6), 4: (9, 8)},
                    'source_pattern': ['#.#', '###'],
                    'source_top_left': (1, 9),
                    'anchors': [(4, 2, 3), (5, 9, 6), (7, 12, 8)]},
                   {'body_size': (11, 14),
                    'legend': {0: (9, 4), 2: (4, 6), 4: (2, 7)},
                    'source_pattern': ['##', '#.'],
                    'source_top_left': (1, 7),
                    'anchors': [(5, 1, 4), (6, 8, 6), (8, 10, 7)]}],
         'test': {'body_size': (11, 15),
                  'legend': {0: (2, 2), 2: (3, 4), 4: (9, 7)},
                  'source_pattern': ['##.', '.##'],
                  'source_top_left': (0, 8),
                  'anchors': [(4, 1, 2), (6, 9, 4), (7, 11, 7)]},
         'title': 'Legend-Driven Transform Stamping',
         'difficulty': 'hard',
         'skills': ['legend decoding', 'transform application', 'multi-target stamping'],
         'staged_hint': 'Learn the source motif once, then use the two-row legend to decide which transform belongs to '
                        'each anchor color.',
         'written_solution': 'The top two rows map anchor colors to transforms. Extract the 5-motif, normalize it, '
                             'then for each anchor stamp the appropriately transformed motif in the anchor’s color. '
                             'The output excludes the legend and the source.',
         'uses_new_primitive': False}}

BUILDERS = {
    'E85': build_e85,
    'E86': build_e86,
    'E87': build_e87,
    'E88': build_e88,
    'E89': build_e89,
    'E90': build_e90,
    'E91': build_e91,
    'M85': build_m85,
    'M86': build_m86,
    'M87': build_m87,
    'M88': build_m88,
    'M89': build_m89,
    'M90': build_m90,
    'M91': build_m91,
    'H85': build_h85,
    'H86': build_h86_case,
    'H87': build_h87,
    'H88': build_h88,
    'H89': build_h89_case,
    'H90': build_h90,
    'H91': build_h91
}

RULES = {
    'E85': rule_e85,
    'E86': rule_e86,
    'E87': rule_e87,
    'E88': rule_e88,
    'E89': rule_e89,
    'E90': rule_e90,
    'E91': rule_e91,
    'M85': rule_m85,
    'M86': rule_m86,
    'M87': rule_m87,
    'M88': rule_m88,
    'M89': rule_m89,
    'M90': rule_m90,
    'M91': rule_m91,
    'H85': rule_h85,
    'H86': rule_h86,
    'H87': rule_h87,
    'H88': rule_h88,
    'H89': rule_h89,
    'H90': rule_h90,
    'H91': rule_h91
}

def puzzle_sort_key(pid):
    prefix_order = {'E':0, 'M':1, 'H':2}
    return (prefix_order[pid[0]], int(pid[1:]))

def generate_records():
    records = []
    for pid in sorted(PUZZLE_SPECS, key=puzzle_sort_key):
        spec = PUZZLE_SPECS[pid]
        build = BUILDERS[pid]
        rule = RULES[pid]
        train = []
        for case in spec['train']:
            inp = build(case)
            out = rule(inp)
            train.append({'input': strings_from_grid(inp), 'output': strings_from_grid(out)})
        test_inp = build(spec['test'])
        test_out = rule(test_inp)
        records.append({
            'id': pid,
            'title': spec['title'],
            'difficulty': spec['difficulty'],
            'skills': spec['skills'],
            'staged_hint': spec['staged_hint'],
            'written_solution': spec['written_solution'],
            'uses_new_primitive': spec['uses_new_primitive'],
            'program_name': rule.__name__,
            'train': train,
            'test': {'input': strings_from_grid(test_inp), 'output': strings_from_grid(test_out)},
            'program_source': inspect.getsource(rule),
        })
    return records

def validate_records(records):
    problems = []
    for rec in records:
        pid = rec['id']
        build = BUILDERS[pid]
        rule = RULES[pid]
        spec = PUZZLE_SPECS[pid]
        for idx, pair in enumerate(rec['train']):
            got = strings_from_grid(rule(build(spec['train'][idx])))
            if got != pair['output']:
                problems.append((pid, 'train', idx+1))
        got = strings_from_grid(rule(build(spec['test'])))
        if got != rec['test']['output']:
            problems.append((pid, 'test', 1))
    return problems

def main():
    records = generate_records()
    problems = validate_records(records)
    pair_count = sum(len(r['train']) + 1 for r in records)
    train_count = sum(len(r['train']) for r in records)
    print(f'generated {len(records)} puzzles / {train_count} train pairs / {pair_count} total pairs')
    if problems:
        print('validation problems:', problems)
        raise SystemExit(1)
    print('validation: clean')
    return records

if __name__ == '__main__':
    main()
