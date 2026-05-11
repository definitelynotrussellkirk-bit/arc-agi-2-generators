"""Reference solvers for the sixteenth 21-task ARC-style puzzle bank.

This batch pushes into a different slice of the ARC space: diagonal and vertical gap logic, directed border beams, crop-transpose moves, bounding-box abstractions, rank-based recoloring, frame interiors, normalized overlays, scripted transform galleries, portal routing, dihedral shape matching, relative-offset transfer, contact graphs, and crosshair docking.
"""
from typing import List
from collections import deque, defaultdict
from itertools import combinations

Grid = List[List[int]]
DIR4 = [(-1,0),(1,0),(0,-1),(0,1)]

NEW_PRIMITIVES = {'area_rank_frame_assignment': 'Assign solid objects to hollow frames by matching their area '
                               'ranks.',
 'bbox_outline': 'Replace each object by the outline of its tight bounding box.',
 'bottom_pack_gallery': 'Pack object crops side by side, bottom-aligned, in discovery order.',
 'color_crosshair_dock': 'Dock each color-matched object at the crosshair defined by its row and '
                         'column markers.',
 'column_last_nonzero': 'Keep only the bottommost nonzero cell in every column.',
 'contact_degree': 'Build a contact graph after one-step dilation and recolor objects by graph '
                   'degree.',
 'corner_color_select_crop': 'Use a corner marker color to select and crop the matching object.',
 'crop_transpose': 'Crop to the active bounding box and transpose the cropped pattern.',
 'diagonal_gap_fill': 'Fill a zero cell when it sits between two matching diagonal neighbors.',
 'dihedral_match_stamp': 'Find the candidate shape matching the guide up to dihedral symmetry and '
                         'stamp it at anchors.',
 'horizontal_brush': 'Expand each singleton into a three-cell horizontal brush centered on the '
                     'seed.',
 'left_border_beam': 'Paint rightward from each left-border seed until the first original blocker.',
 'normalized_overlay': 'Normalize two objects to a shared origin and overlay them with overlap '
                       'color 8.',
 'portal_bfs': 'Route a shortest path through a maze with teleporting portal pairs.',
 'rank_recolor_vertical': 'Recolor objects by their top-to-bottom order.',
 'relative_offset_copy': 'Copy a template using the same marker-to-template offset at a new '
                         'marker.',
 'script_transform_gallery': 'Use a script row of codes to transform a base object and emit a '
                             'gallery.',
 'seed_fill_frame': 'Fill each rectangular frame interior with the seed found inside it.',
 'solid3_to_corners': 'Reduce each solid 3x3 monochrome square to just its four corners.',
 'transpose_stack': 'Transpose each object crop and stack the results vertically.',
 'vertical_gap_fill': 'Fill a zero cell when it sits between two matching vertical neighbors.'}

def blank(h,w,v=0):
    return [[v for _ in range(w)] for _ in range(h)]

def copy_grid(g):
    return [row[:] for row in g]

def dims(g):
    return len(g), len(g[0]) if g else 0

def crop_nonzero(g):
    h,w=dims(g)
    rs=[r for r in range(h) for c in range(w) if g[r][c]!=0]
    cs=[c for r in range(h) for c in range(w) if g[r][c]!=0]
    if not rs:
        return [[0]]
    r0,r1=min(rs),max(rs); c0,c1=min(cs),max(cs)
    return [row[c0:c1+1] for row in g[r0:r1+1]]

def transpose(g):
    h,w=dims(g)
    return [[g[r][c] for r in range(h)] for c in range(w)]

def components_by_color(g, connectivity=4, nonzero_only=True):
    h,w=dims(g)
    dirs=DIR4 if connectivity==4 else DIR8
    seen=[[False]*w for _ in range(h)]
    comps=[]
    for r in range(h):
        for c in range(w):
            if seen[r][c]: 
                continue
            val=g[r][c]
            if nonzero_only and val==0:
                seen[r][c]=True
                continue
            if not nonzero_only and val is None:
                pass
            seen[r][c]=True
            if val==0 and nonzero_only:
                continue
            stack=[(r,c)]
            cells=[]
            while stack:
                rr,cc=stack.pop()
                cells.append((rr,cc))
                for dr,dc in dirs:
                    nr,nc=rr+dr,cc+dc
                    if 0<=nr<h and 0<=nc<w and not seen[nr][nc] and g[nr][nc]==val:
                        seen[nr][nc]=True
                        stack.append((nr,nc))
            comps.append({'color':val,'cells':cells})
    return comps

def bbox(cells):
    rs=[r for r,c in cells]; cs=[c for r,c in cells]
    return min(rs), min(cs), max(rs), max(cs)

def crop_component(g, cells):
    r0,c0,r1,c1 = bbox(cells)
    return [row[c0:c1+1] for row in g[r0:r1+1]], (r0,c0,r1,c1)

def normalize_occupancy(cells):
    r0,c0,r1,c1 = bbox(cells)
    occ={(r-r0,c-c0) for r,c in cells}
    return occ, (r1-r0+1,c1-c0+1)

def rotate90(g):
    h,w=dims(g)
    return [[g[h-1-r][c] for r in range(h)] for c in range(w)]

def rotate180(g):
    return [row[::-1] for row in g[::-1]]

def rotate270(g):
    return rotate90(rotate180(g))

def flip_h(g):
    return [row[::-1] for row in g]

def flip_v(g):
    return g[::-1]

def find_rectangular_frames(g):
    comps=components_by_color(g)
    frames=[]
    others=[]
    for comp in comps:
        col=comp['color']
        r0,c0,r1,c1=bbox(comp['cells'])
        cells=set(comp['cells'])
        border=set()
        for c in range(c0,c1+1):
            border.add((r0,c)); border.add((r1,c))
        for r in range(r0,r1+1):
            border.add((r,c0)); border.add((r,c1))
        if cells==border and r1-r0>=2 and c1-c0>=2:
            frames.append({'color':col,'cells':comp['cells'],'bbox':(r0,c0,r1,c1)})
        else:
            others.append(comp)
    return frames, others

def portal_pairs(g):
    pos=defaultdict(list)
    h,w=dims(g)
    for r in range(h):
        for c in range(w):
            if g[r][c] >= 4:
                pos[g[r][c]].append((r,c))
    return {color:tuple(cells) for color,cells in pos.items() if len(cells)==2}

def dihedral_variants_occ(occ):
    # occ set coords normalized
    coords=list(occ)
    # convert to grid minimal, then transform
    maxr=max(r for r,c in occ); maxc=max(c for r,c in occ)
    g=blank(maxr+1,maxc+1)
    for r,c in occ: g[r][c]=1
    vars=[]
    cur=g
    for rot in [lambda x:x, rotate90, rotate180, rotate270]:
        rg=rot(g)
        vars.append(rg)
        vars.append(flip_h(rg))
    out=[]
    seen=set()
    for vg in vars:
        occ2={(r,c) for r,row in enumerate(vg) for c,v in enumerate(row) if v}
        if not occ2: 
            continue
        rmin=min(r for r,c in occ2); cmin=min(c for r,c in occ2)
        norm=frozenset((r-rmin,c-cmin) for r,c in occ2)
        if norm not in seen:
            seen.add(norm); out.append(norm)
    return out

TRANSFORM_CODES = {
    1: rotate90,
    2: rotate180,
    3: rotate270,
    4: flip_h,
    5: flip_v,
}

def solve_easy_p01(g):
    h,w=dims(g)
    out=copy_grid(g)
    for r in range(h):
        for c in range(w):
            if g[r][c]!=0:
                continue
            fill=0
            if 0<=r-1<h and 0<=c-1<w and 0<=r+1<h and 0<=c+1<w:
                a,b=g[r-1][c-1], g[r+1][c+1]
                if a!=0 and a==b:
                    fill=a
            if fill==0 and 0<=r-1<h and 0<=c+1<w and 0<=r+1<h and 0<=c-1<w:
                a,b=g[r-1][c+1], g[r+1][c-1]
                if a!=0 and a==b:
                    fill=a
            out[r][c]=fill
    return out

def solve_easy_p02(g):
    h,w=dims(g)
    out=blank(h,w)
    for r in range(h):
        for c in range(w):
            if g[r][c]!=0:
                col=g[r][c]
                for dc in (-1,0,1):
                    nc=c+dc
                    if 0<=nc<w:
                        out[r][nc]=col
    return out

def solve_easy_p03(g):
    h,w=dims(g)
    out=copy_grid(g)
    for r in range(h):
        seed=g[r][0]
        if seed==0:
            continue
        stop=w
        for c in range(1,w):
            if g[r][c]!=0:
                stop=c
                break
        for c in range(1,stop):
            if g[r][c]==0:
                out[r][c]=seed
    return out

def solve_easy_p04(g):
    h,w=dims(g)
    out=blank(h,w)
    used=set()
    for r in range(h-2):
        for c in range(w-2):
            col=g[r][c]
            if col==0:
                continue
            ok=True
            cells=[]
            for rr in range(r,r+3):
                for cc in range(c,c+3):
                    if g[rr][cc]!=col:
                        ok=False
                    cells.append((rr,cc))
            if ok:
                # ensure exact isolated 3x3? not necessary with our examples
                for rr,cc in [(r,c),(r,c+2),(r+2,c),(r+2,c+2)]:
                    out[rr][cc]=col
                used.update(cells)
    return out

def solve_easy_p05(g):
    h,w=dims(g)
    out=copy_grid(g)
    for r in range(1,h-1):
        for c in range(w):
            if g[r][c]==0 and g[r-1][c]!=0 and g[r-1][c]==g[r+1][c]:
                out[r][c]=g[r-1][c]
    return out

def solve_easy_p06(g):
    h,w=dims(g)
    out=blank(h,w)
    for c in range(w):
        for r in range(h-1,-1,-1):
            if g[r][c]!=0:
                out[r][c]=g[r][c]
                break
    return out

def solve_easy_p07(g):
    return transpose(crop_nonzero(g))

def solve_medium_p01(g):
    h,w=dims(g)
    out=blank(h,w)
    for comp in components_by_color(g):
        col=comp['color']
        r0,c0,r1,c1=bbox(comp['cells'])
        for c in range(c0,c1+1):
            out[r0][c]=col
            out[r1][c]=col
        for r in range(r0,r1+1):
            out[r][c0]=col
            out[r][c1]=col
    return out

def solve_medium_p02(g):
    comps=components_by_color(g)
    comps.sort(key=lambda comp: (min(r for r,c in comp['cells']), min(c for r,c in comp['cells'])))
    palette=[2,3,4,5,6,7,8,9,1]
    h,w=dims(g)
    out=blank(h,w)
    for i,comp in enumerate(comps):
        col=palette[i]
        for r,c in comp['cells']:
            out[r][c]=col
    return out

def solve_medium_p03(g):
    h,w=dims(g)
    marker=0
    corners=[g[0][0],g[0][w-1],g[h-1][0],g[h-1][w-1]]
    for v in corners:
        if v!=0:
            marker=v
            break
    cells=[(r,c) for r in range(h) for c in range(w) if g[r][c]==marker and (r,c) not in [(0,0),(0,w-1),(h-1,0),(h-1,w-1)]]
    # if object touches corner and corner marker same color, exclude only actual corner marker
    if not cells:
        cells=[(r,c) for r in range(h) for c in range(w) if g[r][c]==marker]
    r0,c0,r1,c1=bbox(cells)
    return [row[c0:c1+1] for row in g[r0:r1+1]]

def solve_medium_p04(g):
    comps=components_by_color(g)
    comps.sort(key=lambda comp: min(c for r,c in comp['cells']))
    pieces=[]
    maxw=0
    totalh=0
    for comp in comps:
        crop,_=crop_component(g, comp['cells'])
        tr=transpose(crop)
        pieces.append(tr)
        ph,pw=dims(tr)
        maxw=max(maxw,pw)
        totalh += ph
    totalh += max(0,len(pieces)-1)
    out=blank(totalh,maxw)
    r=0
    for idx,p in enumerate(pieces):
        ph,pw=dims(p)
        for i in range(ph):
            for j in range(pw):
                out[r+i][j]=p[i][j]
        r += ph + 1
    return out

def solve_medium_p05(g):
    h,w=dims(g)
    out=blank(h,w)
    frames, others = find_rectangular_frames(g)
    # preserve frames
    for fr in frames:
        for r,c in fr['cells']:
            out[r][c]=fr['color']
        r0,c0,r1,c1=fr['bbox']
        # find unique seed inside bbox excluding frame color, from original grid
        seed=0
        for r in range(r0+1,r1):
            for c in range(c0+1,c1):
                if g[r][c]!=0 and g[r][c]!=fr['color']:
                    seed=g[r][c]
        for r in range(r0+1,r1):
            for c in range(c0+1,c1):
                out[r][c]=seed
    return out

def solve_medium_p06(g):
    comps=components_by_color(g)
    comps.sort(key=lambda comp: min(c for r,c in comp['cells']))
    pieces=[]
    maxh=0
    totalw=0
    for comp in comps:
        crop,_=crop_component(g, comp['cells'])
        pieces.append(crop)
        ph,pw=dims(crop)
        maxh=max(maxh,ph)
        totalw += pw
    totalw += max(0,len(pieces)-1)
    out=blank(maxh,totalw)
    c=0
    for p in pieces:
        ph,pw=dims(p)
        top=maxh-ph
        for i in range(ph):
            for j in range(pw):
                out[top+i][c+j]=p[i][j]
        c += pw + 1
    return out

def solve_medium_p07(g):
    comps=components_by_color(g)
    assert len(comps)==2
    pieces=[]
    cols=[]
    maxh=maxw=0
    for comp in comps:
        occ,(h,w)=normalize_occupancy(comp['cells'])
        pieces.append(occ); cols.append(comp['color']); maxh=max(maxh,h); maxw=max(maxw,w)
    out=blank(maxh,maxw)
    for idx,occ in enumerate(pieces):
        for r,c in occ:
            if out[r][c]==0:
                out[r][c]=cols[idx]
            else:
                out[r][c]=8
    return out

def solve_hard_p01(g):
    codes=[v for v in g[0] if v!=0]
    base=crop_nonzero(g[2:]) if len(g)>2 else [[0]]
    pieces=[]
    totalw=0
    maxh=0
    for code in codes:
        p=TRANSFORM_CODES[code](base)
        pieces.append(p)
        ph,pw=dims(p)
        totalw += pw
        maxh=max(maxh,ph)
    totalw += max(0,len(pieces)-1)
    out=blank(maxh,totalw)
    c=0
    for p in pieces:
        ph,pw=dims(p)
        for r in range(ph):
            for j in range(pw):
                out[r][c+j]=p[r][j]
        c += pw + 1
    return out

def solve_hard_p02(g):
    h,w=dims(g)
    start=goal=None
    for r in range(h):
        for c in range(w):
            if g[r][c]==2: start=(r,c)
            elif g[r][c]==3: goal=(r,c)
    pairs=portal_pairs(g)
    portal_lookup={}
    for color,(a,b) in pairs.items():
        portal_lookup[a]=b
        portal_lookup[b]=a
    def neighbors(pos):
        r,c=pos
        for dr,dc in DIR4:
            nr,nc=r+dr,c+dc
            if 0<=nr<h and 0<=nc<w and g[nr][nc]!=1:
                nxt=(nr,nc)
                if g[nr][nc] >= 4 and nxt in portal_lookup:
                    yield portal_lookup[nxt], nxt  # state position after teleport, stepped portal cell
                else:
                    yield nxt, nxt
    prev={start:(None,None)}  # state -> (prev_state, stepped_cell_before_tp)
    dq=deque([start])
    while dq:
        cur=dq.popleft()
        if cur==goal:
            break
        for nxt, stepped in neighbors(cur):
            if nxt not in prev:
                prev[nxt]=(cur, stepped)
                dq.append(nxt)
    if goal not in prev:
        return copy_grid(g)
    path_states=[]
    cur=goal
    while cur is not None:
        path_states.append(cur)
        cur=prev[cur][0]
    path_states=path_states[::-1]
    out=copy_grid(g)
    # reconstruct traversed cells including intermediate stepped portal cells
    cur=goal
    traversed=[]
    while cur!=start:
        prv, stepped=prev[cur]
        if stepped is not None:
            traversed.append(stepped)
        cur=prv
    traversed.append(start)
    traversed=set(traversed+[goal])
    for r,c in traversed:
        if out[r][c]==0:
            out[r][c]=8
    return out

def solve_hard_p03(g):
    h,w=dims(g)
    frames, others = find_rectangular_frames(g)
    # solids are non-frame components
    solids=others
    solids.sort(key=lambda comp: len(comp['cells']))
    frames.sort(key=lambda fr: (fr['bbox'][2]-fr['bbox'][0]-1)*(fr['bbox'][3]-fr['bbox'][1]-1))
    out=blank(h,w)
    for fr in frames:
        for r,c in fr['cells']:
            out[r][c]=fr['color']
    for comp, fr in zip(solids, frames):
        crop,_=crop_component(g, comp['cells'])
        ph,pw=dims(crop)
        r0,c0,r1,c1=fr['bbox']
        ih,iw=r1-r0-1,c1-c0-1
        top=r0+1 + (ih-ph)//2
        left=c0+1 + (iw-pw)//2
        for i in range(ph):
            for j in range(pw):
                if crop[i][j]!=0:
                    out[top+i][left+j]=crop[i][j]
    return out

def solve_hard_p04(g):
    h,w=dims(g)
    comps=components_by_color(g)
    guide=None
    anchors=[]
    candidates=[]
    for comp in comps:
        if comp['color']==2:
            guide=comp
        elif comp['color']==9:
            anchors.extend(comp['cells'])
        else:
            candidates.append(comp)
    guide_occ,_=normalize_occupancy(guide['cells'])
    guide_variants=set(dihedral_variants_occ(guide_occ))
    chosen=None
    for comp in candidates:
        occ,_=normalize_occupancy(comp['cells'])
        if frozenset(occ) in guide_variants:
            chosen=comp; break
    crop,_=crop_component(g, chosen['cells'])
    ph,pw=dims(crop)
    out=blank(h,w)
    for ar,ac in anchors:
        for i in range(ph):
            for j in range(pw):
                if crop[i][j]!=0:
                    rr,cc=ar+i, ac+j
                    if 0<=rr<h and 0<=cc<w:
                        out[rr][cc]=chosen['color']
    return out

def solve_hard_p05(g):
    h,w=dims(g)
    ref=target=None
    template_cells=[]
    for r in range(h):
        for c in range(w):
            if g[r][c]==2: ref=(r,c)
            elif g[r][c]==3: target=(r,c)
    # template is all nonzero cells except markers 2,3
    template_cells=[(r,c) for r in range(h) for c in range(w) if g[r][c]!=0 and g[r][c] not in (2,3)]
    r0,c0,r1,c1=bbox(template_cells)
    top_offset=(r0-ref[0], c0-ref[1])
    crop=[row[c0:c1+1] for row in g[r0:r1+1]]
    new_top=target[0]+top_offset[0]
    new_left=target[1]+top_offset[1]
    out=copy_grid(g)
    for i,row in enumerate(crop):
        for j,v in enumerate(row):
            if v!=0:
                rr,cc=new_top+i,new_left+j
                if 0<=rr<h and 0<=cc<w:
                    out[rr][cc]=v
    return out

def solve_hard_p06(g):
    comps=components_by_color(g)
    # any nonzero components, graph edge if min manhattan distance <= 2
    n=len(comps)
    deg=[0]*n
    cell_sets=[comp['cells'] for comp in comps]
    for i,j in combinations(range(n),2):
        touch=False
        for r1,c1 in cell_sets[i]:
            for r2,c2 in cell_sets[j]:
                if abs(r1-r2)+abs(c1-c2)<=2:
                    touch=True; break
            if touch: break
        if touch:
            deg[i]+=1; deg[j]+=1
    palette={0:2,1:3,2:4,3:5,4:6,5:7}
    h,w=dims(g)
    out=blank(h,w)
    for comp,d in zip(comps,deg):
        col=palette.get(d,7)
        for r,c in comp['cells']:
            out[r][c]=col
    return out

def solve_hard_p07(g):
    h,w=dims(g)
    # objects are nonzero comps excluding top row and left column markers
    row_markers={}
    col_markers={}
    for r in range(1,h):
        if g[r][0]!=0:
            row_markers[g[r][0]]=r
    for c in range(1,w):
        if g[0][c]!=0:
            col_markers[g[0][c]]=c
    comps=components_by_color(g)
    out=blank(h,w)
    for comp in comps:
        col=comp['color']
        # skip border markers singletons on top row or left col
        cells=comp['cells']
        if all(r==0 or c==0 for r,c in cells):
            continue
        crop,_=crop_component(g, cells)
        ph,pw=dims(crop)
        cr=row_markers[col]
        cc=col_markers[col]
        top=cr - ph//2
        left=cc - pw//2
        for i in range(ph):
            for j in range(pw):
                if crop[i][j]!=0:
                    rr,cc2=top+i,left+j
                    if 0<=rr<h and 0<=cc2<w:
                        out[rr][cc2]=crop[i][j]
    return out

