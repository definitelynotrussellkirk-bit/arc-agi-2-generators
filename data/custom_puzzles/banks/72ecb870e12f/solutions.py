"""Reference solvers for the fourteenth 21-task ARC-style puzzle bank.

This batch leans into:
- run logic, transpose, rectangle completion, directional border steps, and local shape growth
- keyed cropping, axis completion, gallery packing, perimeter ranking, frame abstraction, and segmented gravity
- portal and key-door pathfinding, dihedral guide matching, two-key control, normalized overlay,
  dual-header Ferrers decoding, and area-based frame assignment
"""
from typing import List, Tuple
from collections import deque, defaultdict

Grid = List[List[int]]
DIR4 = [(-1,0),(1,0),(0,-1),(0,1)]

NEW_PRIMITIVES = {
    "vertical_run_heads": "Reduce each vertical run to its topmost cell.",
    "unit_gap_bridge": "Fill a one-cell horizontal gap between identical colors.",
    "grid_transpose": "Swap rows and columns globally.",
    "rectangle_fourth_corner": "Infer the missing corner of a same-color axis-aligned rectangle.",
    "nearest_border_step": "Move one step toward the uniquely nearest border.",
    "plus_fill_square": "Expand a plus to a filled 3x3 square.",
    "majority_color_filter": "Keep only the most frequent nonzero color.",
    "marker_selected_crop": "Use a marker color to choose which object to crop.",
    "axis_echo": "Reflect content across a detected axis line.",
    "gallery_pack_by_width": "Pack cropped objects by increasing width, bottom-aligned.",
    "perimeter_rank_recolor": "Rank components by perimeter and recolor by palette order.",
    "component_bbox_frame": "Replace each object with its tight bounding-box frame.",
    "corner_key_rotate": "Use a marked corner to choose a rotation.",
    "segmented_column_gravity": "Apply gravity independently inside blocker-separated column segments.",
    "portal_bfs_path": "Find a shortest path while allowing same-color portal teleports.",
    "guide_mask_match": "Find the candidate matching a guide mask up to rotation or reflection.",
    "rank_transform_frame_insert": "Select an object by rank, transform it by key, and place it inside a frame.",
    "normalized_overlap_palette": "Overlay normalized shapes and color only-first / only-second / overlap differently.",
    "keydoor_bfs_path": "Find a shortest path in a state space with a collectible key and locked doors.",
    "dual_header_ferrers": "Decode a Ferrers diagram from row-length and column-height headers.",
    "area_socket_assignment": "Match each object to the frame whose interior area equals its area."
}

def blank(h,w,v=0):
    return [[v]*w for _ in range(h)]


def dims(g):
    return len(g), len(g[0]) if g else 0


def copy_grid(g):
    return [row[:] for row in g]


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


def find_components(g, ignore_colors=None):
    h,w=dims(g)
    ignore=set(ignore_colors or [])
    seen=[[False]*w for _ in range(h)]
    comps=[]
    for r in range(h):
        for c in range(w):
            if seen[r][c] or g[r][c]==0 or g[r][c] in ignore:
                continue
            col=g[r][c]
            q=[(r,c)]
            seen[r][c]=True
            cells=[]
            while q:
                x,y=q.pop()
                cells.append((x,y))
                for dx,dy in DIR4:
                    nx,ny=x+dx,y+dy
                    if 0<=nx<h and 0<=ny<w and not seen[nx][ny] and g[nx][ny]==col:
                        seen[nx][ny]=True
                        q.append((nx,ny))
            comps.append({'color':col,'cells':cells,'bbox':bbox(cells),'area':len(cells)})
    return comps


def rotate90(g):
    h,w=dims(g)
    return [[g[h-1-r][c] for r in range(h)] for c in range(w)]


def rotate180(g): return rotate90(rotate90(g))


def rotate270(g): return rotate90(rotate180(g))


def flip_h(g): return [list(reversed(row)) for row in g]


def transpose(g): return [list(row) for row in zip(*g)]


def normalize_shape(cells):
    r0,c0,r1,c1=bbox(cells)
    return {(r-r0,c-c0) for r,c in cells}


def crop_nonzero(g):
    return crop_bbox(g)


def transform_grid(g, code):
    # code 0 none,1 90 cw,2 180,3 270
    if code==0: return [row[:] for row in g]
    if code==1: return rotate90(g)
    if code==2: return rotate180(g)
    if code==3: return rotate270(g)
    raise ValueError


def all_dihedral(g):
    gs=[]
    cur=[row[:] for row in g]
    for _ in range(4):
        gs.append(cur)
        gs.append(flip_h(cur))
        cur=rotate90(cur)
    # dedupe by tuple
    out=[]
    seen=set()
    for x in gs:
        t=tuple(tuple(r) for r in x)
        if t not in seen:
            seen.add(t)
            out.append(x)
    return out


def component_perimeter(g, comp):
    cells=set(comp['cells'])
    per=0
    for r,c in cells:
        for dr,dc in DIR4:
            if (r+dr,c+dc) not in cells:
                per+=1
    return per


def scan_rect_frames(g, frame_color=None):
    h,w=dims(g)
    frames=[]
    seen=set()
    for r0 in range(h):
        for c0 in range(w):
            col=g[r0][c0]
            if col==0: continue
            if frame_color is not None and col!=frame_color: continue
            for r1 in range(r0+2,h):
                for c1 in range(c0+2,w):
                    if g[r0][c1]!=col or g[r1][c0]!=col or g[r1][c1]!=col:
                        continue
                    ok=True
                    for c in range(c0,c1+1):
                        if g[r0][c]!=col or g[r1][c]!=col:
                            ok=False; break
                    if not ok: continue
                    for r in range(r0,r1+1):
                        if g[r][c0]!=col or g[r][c1]!=col:
                            ok=False; break
                    if not ok: continue
                    key=(r0,c0,r1,c1,col)
                    if key in seen: continue
                    seen.add(key)
                    frames.append({'color':col,'bbox':(r0,c0,r1,c1),'interior_area':max(0,(r1-r0-1)*(c1-c0-1))})
    # remove frames fully contained in larger same frame? maybe keep all unique
    return frames


def solve_easy_n01(g):
    h,w=dims(g)
    out=blank(h,w)
    for c in range(w):
        r=0
        while r<h:
            if g[r][c]==0:
                r+=1; continue
            col=g[r][c]
            out[r][c]=col
            r2=r+1
            while r2<h and g[r2][c]==col:
                r2+=1
            r=r2
    return out


def solve_easy_n02(g):
    h,w=dims(g)
    out=copy_grid(g)
    for r in range(h):
        for c in range(1,w-1):
            if g[r][c]==0 and g[r][c-1]==g[r][c+1] and g[r][c-1]!=0:
                out[r][c]=g[r][c-1]
    return out


def solve_easy_n03(g):
    return transpose(g)


def solve_easy_n04(g):
    out=copy_grid(g)
    pos=defaultdict(set)
    for r,row in enumerate(g):
        for c,v in enumerate(row):
            if v!=0:
                pos[v].add((r,c))
    for col,cellset in pos.items():
        rows=sorted({r for r,c in cellset})
        cols=sorted({c for r,c in cellset})
        for i,r1 in enumerate(rows):
            for r2 in rows[i+1:]:
                for j,c1 in enumerate(cols):
                    for c2 in cols[j+1:]:
                        corners=[(r1,c1),(r1,c2),(r2,c1),(r2,c2)]
                        present=sum((p in cellset) for p in corners)
                        if present==3:
                            for p in corners:
                                if p not in cellset:
                                    out[p[0]][p[1]]=col
    return out


def solve_easy_n05(g):
    h,w=dims(g)
    out=copy_grid(g)
    for r in range(h):
        for c in range(w):
            v=g[r][c]
            if v==0: continue
            # unique nearest border
            dists={'top':r, 'bottom':h-1-r, 'left':c, 'right':w-1-c}
            mind=min(dists.values())
            dirs=[k for k,vv in dists.items() if vv==mind]
            if len(dirs)!=1: 
                continue
            d=dirs[0]
            dr,dc={'top':(-1,0),'bottom':(1,0),'left':(0,-1),'right':(0,1)}[d]
            nr,nc=r+dr,c+dc
            if 0<=nr<h and 0<=nc<w:
                out[nr][nc]=v
    return out


def solve_easy_n06(g):
    h,w=dims(g)
    out=copy_grid(g)
    for r in range(1,h-1):
        for c in range(1,w-1):
            v=g[r][c]
            if v!=0 and g[r-1][c]==v and g[r+1][c]==v and g[r][c-1]==v and g[r][c+1]==v:
                for rr in range(r-1,r+2):
                    for cc in range(c-1,c+2):
                        out[rr][cc]=v
    return out


def solve_easy_n07(g):
    counts=defaultdict(int)
    for row in g:
        for v in row:
            if v!=0: counts[v]+=1
    if not counts: return copy_grid(g)
    maj=max(counts, key=lambda c:(counts[c], -c))
    return [[v if v==maj else 0 for v in row] for row in g]


def solve_medium_n01(g):
    marker=g[0][0]
    comps=find_components(g)
    target=None
    for comp in comps:
        if comp['color']==marker and (0,0) not in comp['cells']:
            target=comp
            break
    if target is None:
        # maybe marker itself forms a comp; find largest other matching color excluding cell 0,0
        same=[comp for comp in comps if comp['color']==marker and comp['cells']!=[(0,0)]]
        if same:
            target=max(same,key=lambda comp:comp['area'])
    return crop_bbox(g, target['cells']) if target else [[marker]]


def solve_medium_n02(g):
    h,w=dims(g)
    out=copy_grid(g)
    # detect vertical/horizontal axis line of color 9 spanning full extent
    axis=None
    for c in range(w):
        if all(g[r][c]==9 for r in range(h)):
            axis=('v',c); break
    if axis is None:
        for r in range(h):
            if all(g[r][c]==9 for c in range(w)):
                axis=('h',r); break
    if axis is None:
        return out
    kind,idx=axis
    for r in range(h):
        for c in range(w):
            v=g[r][c]
            if v==0 or v==9: 
                continue
            if kind=='v':
                mc=2*idx-c
                if 0<=mc<w:
                    out[r][mc]=v
            else:
                mr=2*idx-r
                if 0<=mr<h:
                    out[mr][c]=v
    return out


def solve_medium_n03(g):
    comps=find_components(g)
    objs=[]
    for comp in comps:
        sub=crop_bbox(g, comp['cells'])
        h,w=dims(sub)
        objs.append((w,h,comp['bbox'][0],sub))
    objs.sort(key=lambda t:(t[0], t[1], t[2]))  # width asc, then height, then top row
    maxh=max((h for w,h,_,sub in objs), default=1)
    totalw=sum(w for w,h,_,sub in objs) + max(0,len(objs)-1)
    out=blank(maxh, totalw)
    c0=0
    for w,h,_,sub in objs:
        r0=maxh-h
        for r in range(h):
            for c in range(w):
                if sub[r][c]!=0:
                    out[r0+r][c0+c]=sub[r][c]
        c0+=w+1
    return out


def solve_medium_n04(g):
    comps=find_components(g)
    pers=[component_perimeter(g, comp) for comp in comps]
    order=sorted(range(len(comps)), key=lambda i:(pers[i], comps[i]['area'], comps[i]['bbox']))
    palette=[2,4,8]
    rank_color={}
    for rank,i in enumerate(order):
        rank_color[i]=palette[rank]
    out=blank(*dims(g))
    for i,comp in enumerate(comps):
        col=rank_color[i]
        for r,c in comp['cells']:
            out[r][c]=col
    return out


def solve_medium_n05(g):
    comps=find_components(g)
    out=blank(*dims(g))
    for comp in comps:
        r0,c0,r1,c1=comp['bbox']
        col=comp['color']
        for c in range(c0,c1+1):
            out[r0][c]=col; out[r1][c]=col
        for r in range(r0,r1+1):
            out[r][c0]=col; out[r][c1]=col
    return out


def solve_medium_n06(g):
    h,w=dims(g)
    corners={(0,0):0,(0,w-1):1,(h-1,w-1):2,(h-1,0):3}
    code=0
    for (r,c),k in corners.items():
        if g[r][c]==9:
            code=k
            break
    # remove marker and crop object
    gg=copy_grid(g); 
    for (r,c) in corners:
        if gg[r][c]==9: gg[r][c]=0
    obj=crop_nonzero(gg)
    return transform_grid(obj, code)


def solve_medium_n07(g):
    h,w=dims(g)
    out=blank(h,w)
    # blockers fixed
    for r in range(h):
        for c in range(w):
            if g[r][c]==5:
                out[r][c]=5
    for c in range(w):
        start=0
        while start<h:
            end=start
            while end<h and g[end][c]!=5:
                end+=1
            # segment start:end without blocker
            vals=[]
            for r in range(start,end):
                if g[r][c] not in (0,5):
                    vals.append(g[r][c])
            # drop to bottom of segment
            rr=end-1
            for v in reversed(vals):
                out[rr][c]=v
                rr-=1
            start=end+1
    return out


def solve_hard_n01(g):
    h,w=dims(g)
    portals=defaultdict(list)
    start=goal=None
    for r in range(h):
        for c in range(w):
            v=g[r][c]
            if v==2: start=(r,c)
            elif v==3: goal=(r,c)
            elif v in (7,8,9):
                portals[v].append((r,c))
    portal_jump={}
    for col,pts in portals.items():
        if len(pts)==2:
            a,b=pts
            portal_jump[a]=b
            portal_jump[b]=a
    q=deque([start])
    prev={start:None}
    while q:
        cur=q.popleft()
        if cur==goal: break
        r,c=cur
        for dr,dc in DIR4:
            nr,nc=r+dr,c+dc
            if not (0<=nr<h and 0<=nc<w): continue
            v=g[nr][nc]
            if v==5: continue
            nxt=(nr,nc)
            if v in (7,8,9) and nxt in portal_jump:
                nxt=portal_jump[nxt]
            if nxt not in prev:
                prev[nxt]=cur
                q.append(nxt)
    out=copy_grid(g)
    if goal not in prev:
        return out
    cur=goal
    path=[]
    while cur is not None:
        path.append(cur); cur=prev[cur]
    path=path[::-1]
    for r,c in path:
        if out[r][c]==0:
            out[r][c]=4
    return out


def solve_hard_n02(g):
    h,w=dims(g)
    comps=find_components(g)
    guide=[comp for comp in comps if comp['color']==8]
    if not guide:
        return blank(h,w)
    guide=guide[0]
    guide_norm=normalize_shape(guide['cells'])
    guide_bbox=guide['bbox']
    best=None
    best_oriented=None
    for comp in comps:
        if comp['color']==8: 
            continue
        sub=crop_bbox(g, comp['cells'])
        for orient in all_dihedral(sub):
            cells={(r,c) for r,row in enumerate(orient) for c,v in enumerate(row) if v!=0}
            if cells==guide_norm:
                best=comp
                best_oriented=orient
                break
        if best is not None:
            break
    out=blank(h,w)
    if best is None:
        return out
    r0,c0,r1,c1=guide_bbox
    gh,gw=r1-r0+1,c1-c0+1
    # guide_norm/ oriented dimensions should match
    for r,row in enumerate(best_oriented):
        for c,v in enumerate(row):
            if v!=0:
                out[r0+r][c0+c]=best['color']
    return out


def solve_hard_n03(g):
    h,w=dims(g)
    # transform key from corner 9
    corners={(0,0):0,(0,w-1):1,(h-1,w-1):2,(h-1,0):3}
    code=0
    for (r,c),k in corners.items():
        if g[r][c]==9:
            code=k
            break
    rank=sum(1 for c in range(w) if g[0][c]==7)
    rank=max(1,min(3,rank))
    gg=copy_grid(g)
    for (r,c) in corners:
        if gg[r][c]==9: gg[r][c]=0
    for c in range(w):
        if gg[0][c]==7: gg[0][c]=0
    frames=scan_rect_frames(gg, frame_color=8)
    if not frames:
        return blank(h,w)
    frame=max(frames, key=lambda fr: fr['interior_area'])
    # remove frame cells for object search
    for r in range(frame['bbox'][0], frame['bbox'][2]+1):
        for c in range(frame['bbox'][1], frame['bbox'][3]+1):
            if r in (frame['bbox'][0], frame['bbox'][2]) or c in (frame['bbox'][1], frame['bbox'][3]):
                gg[r][c]=0
    comps=find_components(gg)
    comps=[comp for comp in comps if comp['color'] not in (7,8,9)]
    comps.sort(key=lambda comp:(comp['area'], comp['bbox']))
    chosen=comps[rank-1]
    sub=crop_bbox(gg, chosen['cells'])
    sub=transform_grid(sub, code)
    out=blank(h,w)
    r0,c0,r1,c1=frame['bbox']
    for c in range(c0,c1+1):
        out[r0][c]=8; out[r1][c]=8
    for r in range(r0,r1+1):
        out[r][c0]=8; out[r][c1]=8
    ih,iw=r1-r0-1,c1-c0-1
    ph,pw=dims(sub)
    sr=r0+1 + max(0,(ih-ph)//2)
    sc=c0+1 + max(0,(iw-pw)//2)
    for r,row in enumerate(sub):
        for c,v in enumerate(row):
            if v!=0 and sr+r<r1 and sc+c<c1:
                out[sr+r][sc+c]=v
    return out


def solve_hard_n04(g):
    comps=find_components(g)
    if len(comps)<2:
        return crop_nonzero(g)
    # choose two largest components by area then bbox
    comps.sort(key=lambda comp:(comp['bbox'][0], comp['bbox'][1]))
    a,b=comps[:2]
    suba=crop_bbox(g, a['cells']); subb=crop_bbox(g,b['cells'])
    cellsa={(r,c) for r,row in enumerate(suba) for c,v in enumerate(row) if v!=0}
    cellsb={(r,c) for r,row in enumerate(subb) for c,v in enumerate(row) if v!=0}
    h=max(len(suba), len(subb)); w=max(len(suba[0]), len(subb[0]))
    out=blank(h,w)
    for r in range(h):
        for c in range(w):
            ina=(r,c) in cellsa
            inb=(r,c) in cellsb
            out[r][c]=8 if ina and inb else 2 if ina else 3 if inb else 0
    return out


def solve_hard_n05(g):
    h,w=dims(g)
    start=goal=keypos=None
    for r in range(h):
        for c,v in enumerate(g[r]):
            if v==2: start=(r,c)
            elif v==3: goal=(r,c)
            elif v==6: keypos=(r,c)
    q=deque([(start[0],start[1],False)])
    prev={(start[0],start[1],False):None}
    end_state=None
    while q:
        r,c,has_key=q.popleft()
        if (r,c)==goal:
            end_state=(r,c,has_key); break
        for dr,dc in DIR4:
            nr,nc=r+dr,c+dc
            if not (0<=nr<h and 0<=nc<w): continue
            v=g[nr][nc]
            if v==5: continue
            if v==7 and not has_key: continue
            nk=has_key or (v==6)
            st=(nr,nc,nk)
            if st not in prev:
                prev[st]=(r,c,has_key)
                q.append(st)
    out=copy_grid(g)
    if end_state is None:
        return out
    cur=end_state
    while cur is not None:
        r,c,has_key=cur
        if out[r][c]==0:
            out[r][c]=4
        cur=prev[cur]
    return out


def solve_hard_n06(g):
    h,w=dims(g)
    H=h//2; W=w//2
    # decode row lengths from bottom-left quadrant color 3
    row_lengths=[]
    for r in range(H,2*H):
        L=0
        for c in range(W):
            if g[r][c]==3: L+=1
        row_lengths.append(L)
    out=blank(H,W)
    for r,L in enumerate(row_lengths):
        for c in range(min(L,W)):
            out[r][c]=8
    return out


def solve_hard_n07(g):
    h,w=dims(g)
    frames=scan_rect_frames(g, frame_color=8)
    out=blank(h,w)
    # remove frame cells from grid to find objects
    frame_cells=set()
    for fr in frames:
        r0,c0,r1,c1=fr['bbox']
        for c in range(c0,c1+1):
            frame_cells.add((r0,c)); frame_cells.add((r1,c))
        for r in range(r0,r1+1):
            frame_cells.add((r,c0)); frame_cells.add((r,c1))
    gg=copy_grid(g)
    for r,c in frame_cells:
        gg[r][c]=0
    objs=find_components(gg, ignore_colors={8})
    # place frames
    for fr in frames:
        r0,c0,r1,c1=fr['bbox']
        for c in range(c0,c1+1):
            out[r0][c]=8; out[r1][c]=8
        for r in range(r0,r1+1):
            out[r][c0]=8; out[r][c1]=8
    used=set()
    # match by exact area
    frames_sorted=sorted(frames, key=lambda fr:(fr['interior_area'], fr['bbox']))
    objs_sorted=sorted(objs, key=lambda ob:(ob['area'], ob['bbox']))
    for fr in frames_sorted:
        target_area=fr['interior_area']
        cand=None
        for i,ob in enumerate(objs_sorted):
            if i in used: continue
            if ob['area']==target_area:
                cand=(i,ob); break
        if cand is None: 
            continue
        i,ob=cand; used.add(i)
        sub=crop_bbox(gg, ob['cells'])
        r0,c0,r1,c1=fr['bbox']
        ih,iw=r1-r0-1,c1-c0-1
        sh,sw=dims(sub)
        sr=r0+1+max(0,(ih-sh)//2)
        sc=c0+1+max(0,(iw-sw)//2)
        for r,row in enumerate(sub):
            for c,v in enumerate(row):
                if v!=0 and sr+r<r1 and sc+c<c1:
                    out[sr+r][sc+c]=v
    return out


