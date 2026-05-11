"""Reference solvers for the fifteenth 21-task ARC-style puzzle bank.

This batch leans into:
- run medians, diagonal consensus, beamcasting, row-frequency filters, and matrix echoes
- object summarization, galleries, border-based labeling, duplicate-shape filtering, and keyed transforms
- selection-transform-insert composition, overlayed beam systems, multi-key pathfinding, blueprint reconstruction,
  guide-based stamping, keyed Boolean shape algebra, and mirror raytracing
"""
from typing import List
from collections import deque, Counter

Grid = List[List[int]]
DIR4 = [(-1,0),(1,0),(0,-1),(0,1)]

NEW_PRIMITIVES = {'area_bar_chart': 'Encode object areas as bottom-aligned colored bars.',
 'area_sorted_gallery': 'Crop objects, sort them by area, and pack them into a horizontal gallery.',
 'bbox_centers': 'Mark each object by the center of its tight bounding box.',
 'corner_key_transform_crop': 'Use a corner key to choose a transform and output the transformed '
                              'object crop.',
 'diagonal_consensus_fill': 'Fill a zero cell when all four diagonal neighbors agree on the same '
                            'nonzero color.',
 'duplicate_shape_filter': 'Keep only shapes whose translated form appears at least twice.',
 'guide_match_stamp': 'Choose the candidate matching a guide up to dihedral symmetry, then stamp '
                      'it at anchor cells.',
 'horizontal_beam': 'Broadcast a seed left and right through zeros until an original blocker or '
                    'the grid edge.',
 'in_bbox_mirror_h': 'Mirror each object horizontally inside its own tight bounding box.',
 'keyed_normalized_boolean': 'Transform one normalized shape and combine it with another by a '
                             'keyed Boolean operator.',
 'mirror_raytrace': 'Trace a right-moving ray through slash and backslash mirrors until it exits '
                    'or hits a wall.',
 'missing_corner_completion': 'Complete a 2x2 block when three corners already contain the same '
                              'nonzero color.',
 'multikey_bfs_path': 'Search over position plus collected-key state to route through multiple '
                      'locked doors.',
 'nearest_border_label': 'Assign a label color based on which outer border is uniquely nearest to '
                         "an object's bounding box.",
 'odd_run_median': 'Reduce each odd horizontal run to its central cell.',
 'orthogonal_beam_overlay': 'Overlay horizontal and vertical beam systems and recolor '
                            'intersections distinctly.',
 'row_singleton_filter': 'Within each row, keep only colors that occur exactly once.',
 'select_transform_insert': 'Select an object by color key, transform it by a second key, and '
                            'insert it centered into a frame.',
 'singleton_blueprint_place': 'Interpret singleton markers as a blueprint for placing reusable '
                              'prototype objects.',
 'upper_triangle_echo': 'Copy the upper-triangular content to the mirrored lower-triangular '
                        'positions.',
 'vertical_trio_rotate': 'Replace a vertical run of length three by a horizontal run centered on '
                         'the same middle cell.'}

def blank(h,w,v=0): return [[v]*w for _ in range(h)]


def dims(g): return (len(g), len(g[0]) if g else 0)


def copy_grid(g): return [row[:] for row in g]


def bbox(cells):
    rs=[r for r,c in cells]; cs=[c for r,c in cells]
    return min(rs), min(cs), max(rs), max(cs)


def crop_bbox(g, cells=None):
    if cells is None:
        cells=[(r,c) for r,row in enumerate(g) for c,v in enumerate(row) if v!=0]
    if not cells: return [[0]]
    r0,c0,r1,c1=bbox(cells)
    return [row[c0:c1+1] for row in g[r0:r1+1]]


def find_components(g, ignore_colors=None):
    ignore=set(ignore_colors or [])
    h,w=dims(g)
    seen=[[False]*w for _ in range(h)]
    comps=[]
    for r in range(h):
        for c in range(w):
            if seen[r][c] or g[r][c]==0 or g[r][c] in ignore:
                continue
            col=g[r][c]
            q=[(r,c)]; seen[r][c]=True; cells=[]
            while q:
                x,y=q.pop()
                cells.append((x,y))
                for dx,dy in DIR4:
                    nx,ny=x+dx,y+dy
                    if 0<=nx<h and 0<=ny<w and not seen[nx][ny] and g[nx][ny]==col:
                        seen[nx][ny]=True; q.append((nx,ny))
            comps.append({'color':col,'cells':cells,'bbox':bbox(cells),'area':len(cells)})
    return comps


def normalize_shape(cells):
    r0,c0,r1,c1=bbox(cells)
    return frozenset((r-r0,c-c0) for r,c in cells)


def rotate90(g):
    h,w=dims(g)
    return [[g[h-1-r][c] for r in range(h)] for c in range(w)]


def rotate180(g): return rotate90(rotate90(g))


def flip_h(g): return [list(reversed(row)) for row in g]


def flip_v(g): return list(reversed([row[:] for row in g]))


def all_dihedral(g):
    out=[]; seen=set(); cur=[row[:] for row in g]
    for _ in range(4):
        for x in [cur, flip_h(cur)]:
            t=tuple(map(tuple,x))
            if t not in seen:
                seen.add(t); out.append(x)
        cur=rotate90(cur)
    return out


def place_shape(out, shape, top, left, color=None):
    for r,row in enumerate(shape):
        for c,v in enumerate(row):
            if v!=0:
                out[top+r][left+c]= color if color is not None else v


def scan_frames(g, frame_color=8):
    h,w=dims(g)
    frames=[]
    seen=set()
    for r0 in range(h):
        for c0 in range(w):
            if g[r0][c0]!=frame_color: continue
            for r1 in range(r0+2,h):
                for c1 in range(c0+2,w):
                    if g[r0][c1]!=frame_color or g[r1][c0]!=frame_color or g[r1][c1]!=frame_color:
                        continue
                    ok=True
                    for c in range(c0,c1+1):
                        if g[r0][c]!=frame_color or g[r1][c]!=frame_color:
                            ok=False; break
                    if not ok: continue
                    for r in range(r0,r1+1):
                        if g[r][c0]!=frame_color or g[r][c1]!=frame_color:
                            ok=False; break
                    if not ok: continue
                    key=(r0,c0,r1,c1)
                    if key not in seen:
                        seen.add(key)
                        frames.append({'bbox':key,'color':frame_color,'interior_h':r1-r0-1,'interior_w':c1-c0-1})
    # keep maximal frames unique by bbox
    return sorted(frames, key=lambda f:(f['bbox'][0],f['bbox'][1], -(f['bbox'][2]-f['bbox'][0]), -(f['bbox'][3]-f['bbox'][1])))


def center_paste(out, crop, bbox_, keep_zeros=False):
    r0,c0,r1,c1=bbox_
    ih,iw=r1-r0-1,c1-c0-1
    ch,cw=dims(crop)
    top=r0+1+(ih-ch)//2
    left=c0+1+(iw-cw)//2
    for r,row in enumerate(crop):
        for c,v in enumerate(row):
            if v!=0 or keep_zeros:
                out[top+r][left+c]=v


def transform_by_key(crop, key):
    if key==1: return rotate90(crop)
    if key==2: return flip_h(crop)
    if key==3: return flip_v(crop)
    if key==4: return rotate180(crop)
    return [row[:] for row in crop]


def binarize(g):
    return [[1 if v!=0 else 0 for v in row] for row in g]


def apply_boolean(A, B, op):
    ha,wa=dims(A); hb,wb=dims(B)
    H=max(ha,hb); W=max(wa,wb)
    out=blank(H,W)
    for r in range(H):
        for c in range(W):
            a = (r<ha and c<wa and A[r][c]!=0)
            b = (r<hb and c<wb and B[r][c]!=0)
            if op==4: keep=a or b
            elif op==5: keep=a and b
            elif op==6: keep=(a ^ b)
            else: keep=False
            if keep: out[r][c]=8
    # crop
    cells=[(r,c) for r,row in enumerate(out) for c,v in enumerate(row) if v!=0]
    return crop_bbox(out,cells) if cells else [[0]]


def solve_easy_o01(g):
    h,w=dims(g)
    out=blank(h,w)
    for r in range(h):
        c=0
        while c<w:
            if g[r][c]==0:
                c+=1; continue
            col=g[r][c]
            c2=c
            while c2<w and g[r][c2]==col:
                c2+=1
            L=c2-c
            if L%2==1:
                out[r][c+L//2]=col
            c=c2
    return out


def solve_easy_o02(g):
    h,w=dims(g)
    out=copy_grid(g)
    for r in range(1,h-1):
        for c in range(1,w-1):
            if g[r][c]!=0: 
                continue
            vals=[g[r-1][c-1],g[r-1][c+1],g[r+1][c-1],g[r+1][c+1]]
            if vals[0]!=0 and vals.count(vals[0])==4:
                out[r][c]=vals[0]
    return out


def solve_easy_o03(g):
    h,w=dims(g)
    out=copy_grid(g)
    for r in range(h):
        for c in range(w):
            col=g[r][c]
            if col==0: 
                continue
            # left
            cc=c-1
            while cc>=0 and g[r][cc]==0:
                out[r][cc]=col
                cc-=1
            cc=c+1
            while cc<w and g[r][cc]==0:
                out[r][cc]=col
                cc+=1
    return out


def solve_easy_o04(g):
    h,w=dims(g)
    out=blank(h,w)
    for r,row in enumerate(g):
        cnt=Counter(v for v in row if v!=0)
        for c,v in enumerate(row):
            if v!=0 and cnt[v]==1:
                out[r][c]=v
    return out


def solve_easy_o05(g):
    h,w=dims(g)
    assert h==w
    out=copy_grid(g)
    for r in range(h):
        for c in range(w):
            if r>c:
                out[r][c]=g[c][r]
    return out


def solve_easy_o06(g):
    h,w=dims(g)
    out=copy_grid(g)
    for r in range(h-1):
        for c in range(w-1):
            vals=[g[r][c],g[r][c+1],g[r+1][c],g[r+1][c+1]]
            nz=[v for v in vals if v!=0]
            if len(nz)==3 and len(set(nz))==1:
                col=nz[0]
                if vals[0]==0: out[r][c]=col
                if vals[1]==0: out[r][c+1]=col
                if vals[2]==0: out[r+1][c]=col
                if vals[3]==0: out[r+1][c+1]=col
    return out


def solve_easy_o07(g):
    h,w=dims(g)
    out=blank(h,w)
    for c in range(w):
        r=0
        while r<h:
            if g[r][c]==0:
                r+=1; continue
            col=g[r][c]
            r2=r
            while r2<h and g[r2][c]==col:
                r2+=1
            if r2-r==3:
                mr=r+1
                if 0< c < w-1:
                    out[mr][c-1]=out[mr][c]=out[mr][c+1]=col
            r=r2
    return out


def solve_medium_o01(g):
    out=blank(*dims(g))
    for comp in find_components(g):
        r0,c0,r1,c1=comp['bbox']
        cr=(r0+r1)//2; cc=(c0+c1)//2
        out[cr][cc]=comp['color']
    return out


def solve_medium_o02(g):
    comps=find_components(g)
    items=[]
    for comp in comps:
        crop=crop_bbox(g, comp['cells'])
        items.append((comp['area'], comp['bbox'][1], comp['bbox'][0], comp['color'], crop))
    items.sort(key=lambda x:(-x[0], x[1], x[2], x[3]))
    height=max(len(crop) for *_,crop in items)
    width=sum(len(crop[0]) for *_,crop in items)+max(0,len(items)-1)
    out=blank(height,width)
    cur=0
    for *_,crop in items:
        for r,row in enumerate(crop):
            for c,v in enumerate(row):
                if v!=0: out[r][cur+c]=v
        cur+=len(crop[0])+1
    return out


def solve_medium_o03(g):
    h,w=dims(g)
    out=blank(h,w)
    for comp in find_components(g):
        r0,c0,r1,c1=comp['bbox']
        dists=[r0, h-1-r1, c0, w-1-c1] # top,bottom,left,right
        k=min(range(4), key=lambda i:dists[i])
        if dists.count(dists[k])!=1:
            # skip ambiguous by keeping original color? but examples unique
            new=comp['color']
        else:
            new=[1,2,3,4][k]
        for r,c in comp['cells']:
            out[r][c]=new
    return out


def solve_medium_o04(g):
    comps=sorted(find_components(g), key=lambda comp:(comp['bbox'][1], comp['bbox'][0], comp['color']))
    heights=[comp['area'] for comp in comps]
    H=max(heights)
    W=2*len(comps)-1
    out=blank(H,W)
    for i,comp in enumerate(comps):
        col=comp['color']; hgt=comp['area']; c=2*i
        for r in range(H-hgt,H):
            out[r][c]=col
    return out


def solve_medium_o05(g):
    h,w=dims(g)
    out=blank(h,w)
    for comp in find_components(g):
        r0,c0,r1,c1=comp['bbox']
        crop=crop_bbox(g, comp['cells'])
        fc=flip_h(crop)
        for r,row in enumerate(fc):
            for c,v in enumerate(row):
                if v!=0: out[r0+r][c0+c]=v
    return out


def solve_medium_o06(g):
    comps=find_components(g)
    sigs=[normalize_shape(comp['cells']) for comp in comps]
    cnt=Counter(sigs)
    h,w=dims(g); out=blank(h,w)
    for comp,sig in zip(comps,sigs):
        if cnt[sig]>=2:
            for r,c in comp['cells']:
                out[r][c]=comp['color']
    return out


def solve_medium_o07(g):
    key=g[0][0]
    comps=find_components(g, ignore_colors={key})
    # But marker cell at (0,0) might connect to nothing due corner. Better ignore exact cell.
    # easiest: pick largest component excluding (0,0)
    best=None
    for comp in find_components([[0 if (r==0 and c==0) else g[r][c] for c in range(len(g[0]))] for r in range(len(g))]):
        if best is None or comp['area']>best['area']:
            best=comp
    crop=crop_bbox(g, best['cells'])
    if key==1: out=rotate90(crop)
    elif key==2: out=flip_h(crop)
    elif key==3: out=flip_v(crop)
    else: out=[row[:] for row in crop]
    return out


def solve_hard_o01(g):
    h,w=dims(g)
    key=g[0][0]
    selector=None
    # top row excluding 0 and frame color and key; choose rightmost nonzero maybe
    for c,v in enumerate(g[0]):
        if c==0: continue
        if v!=0:
            selector=v
    # frame color 8
    frames=scan_frames(g,8)
    frame=max(frames, key=lambda f:(f['bbox'][2]-f['bbox'][0])*(f['bbox'][3]-f['bbox'][1]))
    # components excluding frame color and selector cells/key row? exclude top row markers
    temp=copy_grid(g)
    temp[0][0]=0
    for c in range(w):
        if g[0][c]==selector:
            temp[0][c]=0
    # remove frame border
    r0,c0,r1,c1=frame['bbox']
    for c in range(c0,c1+1):
        temp[r0][c]=0; temp[r1][c]=0
    for r in range(r0,r1+1):
        temp[r][c0]=0; temp[r][c1]=0
    comps=find_components(temp)
    target=max([comp for comp in comps if comp['color']==selector], key=lambda comp: comp['area'])
    crop=crop_bbox(temp, target['cells'])
    crop=transform_by_key(crop, key)
    out=blank(h,w)
    # keep frame
    for c in range(c0,c1+1):
        out[r0][c]=out[r1][c]=8
    for r in range(r0,r1+1):
        out[r][c0]=out[r][c1]=8
    center_paste(out, crop, frame['bbox'])
    return out


def solve_hard_o02(g):
    h,w=dims(g)
    out=copy_grid(g)
    horiz=set()
    vert=set()
    blockers={(r,c) for r,row in enumerate(g) for c,v in enumerate(row) if v not in (0,2,3)}
    for r in range(h):
        for c in range(w):
            if g[r][c]==2:
                cc=c-1
                while cc>=0 and g[r][cc]==0:
                    horiz.add((r,cc)); cc-=1
                cc=c+1
                while cc<w and g[r][cc]==0:
                    horiz.add((r,cc)); cc+=1
            elif g[r][c]==3:
                rr=r-1
                while rr>=0 and g[rr][c]==0:
                    vert.add((rr,c)); rr-=1
                rr=r+1
                while rr<h and g[rr][c]==0:
                    vert.add((rr,c)); rr+=1
    for cell in horiz|vert:
        if cell in blockers: 
            continue
        if cell in horiz and cell in vert: out[cell[0]][cell[1]]=4
        elif cell in horiz: out[cell[0]][cell[1]]=2
        elif cell in vert: out[cell[0]][cell[1]]=3
    return out


def solve_hard_o03(g):
    h,w=dims(g)
    # 0 empty, 8 wall, 2 start, 3 goal, 4 keyA,5 keyB, 6 doorA,7 doorB
    start=goal=None
    for r in range(h):
        for c in range(w):
            if g[r][c]==2: start=(r,c)
            if g[r][c]==3: goal=(r,c)
    start_state=(start[0],start[1],0,0)
    q=deque([start_state]); prev={start_state:None}
    def passable(r,c,ka,kb):
        if not (0<=r<h and 0<=c<w): return False
        v=g[r][c]
        if v==8: return False
        if v==6 and not ka: return False
        if v==7 and not kb: return False
        return True
    end_state=None
    while q:
        r,c,ka,kb=q.popleft()
        if (r,c)==goal:
            end_state=(r,c,ka,kb); break
        nka,nkb=ka,kb
        if g[r][c]==4: nka=1
        if g[r][c]==5: nkb=1
        # important: from current state after collecting key maybe explore
        if (r,c,nka,nkb)!=(r,c,ka,kb) and (r,c,nka,nkb) not in prev:
            prev[(r,c,nka,nkb)] = (r,c,ka,kb)
            q.appendleft((r,c,nka,nkb))
            continue
        for dr,dc in DIR4:
            nr,nc=r+dr,c+dc
            if passable(nr,nc,nka,nkb):
                st=(nr,nc,nka,nkb)
                if st not in prev:
                    prev[st]=(r,c,ka,kb)
                    q.append(st)
    if end_state is None:
        return blank(h,w)
    # reconstruct
    out=blank(h,w)
    st=end_state
    while st is not None:
        r,c,ka,kb=st
        out[r][c]=9
        st=prev[st]
    return out


def solve_hard_o04(g):
    # singleton comps = blueprint; others = prototypes keyed by color
    comps=find_components(g)
    singles=[comp for comp in comps if comp['area']==1]
    protos=[comp for comp in comps if comp['area']>1]
    br0,bc0,br1,bc1=bbox([cell for comp in singles for cell in comp['cells']])
    bh,bw=br1-br0+1, bc1-bc0+1
    proto_by_color={}
    maxh=maxw=0
    for comp in protos:
        crop=crop_bbox(g, comp['cells'])
        proto_by_color[comp['color']]=crop
        hh,ww=dims(crop); maxh=max(maxh,hh); maxw=max(maxw,ww)
    out_h=bh*maxh + (bh-1)
    out_w=bw*maxw + (bw-1)
    out=blank(out_h,out_w)
    for comp in singles:
        r,c=comp['cells'][0]
        color=comp['color']
        slot_r=r-br0; slot_c=c-bc0
        crop=proto_by_color[color]
        top=slot_r*(maxh+1)
        left=slot_c*(maxw+1)
        place_shape(out, crop, top, left)
    return out


def solve_hard_o05(g):
    comps=find_components(g)
    guide=max([comp for comp in comps if comp['color']==9], key=lambda c:c['area'])
    guide_crop=crop_bbox(g, guide['cells'])
    guide_ds={tuple(map(tuple,binarize(x))) for x in all_dihedral(guide_crop)}
    anchors=[comp['cells'][0] for comp in comps if comp['color']==8 and comp['area']==1]
    candidates=[comp for comp in comps if comp['color'] not in (8,9)]
    matching=[comp for comp in candidates if tuple(map(tuple,binarize(crop_bbox(g, comp['cells'])))) in guide_ds]
    target=max(matching, key=lambda c:c['area'])
    stamp=crop_bbox(g, target['cells'])
    h,w=dims(g)
    out=blank(h,w)
    for ar,ac in anchors:
        for r,row in enumerate(stamp):
            for c,v in enumerate(row):
                if v!=0 and 0<=ar+r<h and 0<=ac+c<w:
                    out[ar+r][ac+c]=v
    return out


def solve_hard_o06(g):
    h,w=dims(g)
    tkey=None; okey=None
    for c,v in enumerate(g[0]):
        if v in (1,2,3): tkey=v
        if v in (4,5,6): okey=v
    temp=copy_grid(g)
    for c,v in enumerate(g[0]):
        if v in (1,2,3,4,5,6): temp[0][c]=0
    comps=find_components(temp)
    objs=sorted(comps, key=lambda comp:(comp['bbox'][1], comp['bbox'][0], comp['color']))
    A=crop_bbox(temp, objs[0]['cells'])
    B=crop_bbox(temp, objs[1]['cells'])
    A=transform_by_key(A, tkey)
    return apply_boolean(A,B,okey)


def solve_hard_o07(g):
    h,w=dims(g)
    out=blank(h,w)
    turn_slash={(0,1):(-1,0),(-1,0):(0,1),(0,-1):(1,0),(1,0):(0,-1)}
    turn_back={(0,1):(1,0),(1,0):(0,1),(0,-1):(-1,0),(-1,0):(0,-1)}
    emitters=[(r,c) for r,row in enumerate(g) for c,v in enumerate(row) if v==2]
    for sr,sc in emitters:
        r,c=sr,sc
        dr,dc=(0,1)
        while True:
            nr,nc=r+dr,c+dc
            if not (0<=nr<h and 0<=nc<w): break
            cell=g[nr][nc]
            if cell==6 or cell==2:
                break
            out[nr][nc]=8
            if cell==4:
                dr,dc=turn_slash[(dr,dc)]
            elif cell==5:
                dr,dc=turn_back[(dr,dc)]
            r,c=nr,nc
    # keep mirrors and walls maybe for context? maybe no, output path only
    return out


