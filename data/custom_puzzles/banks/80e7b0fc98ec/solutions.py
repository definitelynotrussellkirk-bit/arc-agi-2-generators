"""Reference solvers for the nineteenth 21-task ARC-style puzzle bank.

This batch emphasizes interval completion, broadcast, diagonal symmetry, run kernels, topology, ranking, selection, galleries, keyed transforms, portal pathfinding, matching-by-area, Boolean shape algebra, state timelines, contact graphs, and mirror raytracing.
"""

from typing import List, Dict, Tuple
from collections import deque, defaultdict


Grid = List[List[int]]
DIR4 = [(-1,0),(1,0),(0,-1),(0,1)]
DIR8 = [(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]


NEW_PRIMITIVES = {
    "row_span_fill": "Fill an inclusive row segment between matching same-color endpoints when the interior is empty.",
    "crosshair_broadcast": "Broadcast a seed color across its entire row and column.",
    "diagonal_union": "Copy every nonzero cell across the main diagonal and keep the originals.",
    "odd_run_kernel": "Reduce each odd-length monochrome run to its center cell.",
    "ring_center_fill": "Fill the center of a hollow 3x3 monochrome ring.",
    "column_gravity": "Drop every column\u2019s nonzero cells to the bottom while preserving order.",
    "rectangle_corner_vote": "Infer the missing fourth corner of a three-corner rectangle.",
    "area_rank_recolor": "Recolor objects by ordering them from smallest area to largest.",
    "bbox_fill": "Replace each object by the solid fill of its axis-aligned bounding box.",
    "corner_color_select": "Use a corner key color to select which object to crop.",
    "frame_gallery": "Extract frame interiors and concatenate them as a gallery.",
    "marker_count_rotate": "Use the number of marker cells to choose a rotation.",
    "column_histogram": "Summarize an object by bottom-aligned column counts inside its bounding box.",
    "hole_fill": "Fill zero regions that are fully enclosed by one surrounding color.",
    "dual_key_select_transform": "One key chooses the object; another key chooses the transform.",
    "portal_bfs": "Find a shortest path in a maze with teleport portals.",
    "frame_pack_by_area": "Match objects to frames by ascending area and center them inside.",
    "shape_boolean": "Align two cropped shapes and apply a keyed Boolean set operation.",
    "transform_timeline": "Emit each intermediate transformed state in a left-to-right timeline.",
    "contact_degree": "Build an object contact graph and recolor by node degree.",
    "mirror_raytrace": "Trace a beam through slash and backslash mirrors until it exits or hits a wall."
}


def blank(h,w,val=0):
    return [[val]*w for _ in range(h)]


def deepcopy_grid(g):
    return [row[:] for row in g]


def dims(g):
    return len(g), len(g[0]) if g else 0


def crop_bbox(g, bg=0):
    h,w=dims(g)
    cells=[(r,c) for r in range(h) for c in range(w) if g[r][c]!=bg]
    if not cells:
        return [[bg]]
    r0=min(r for r,_ in cells); r1=max(r for r,_ in cells)
    c0=min(c for _,c in cells); c1=max(c for _,c in cells)
    return [row[c0:c1+1] for row in g[r0:r1+1]]


def bbox_of_cells(cells):
    r0=min(r for r,c in cells); r1=max(r for r,c in cells)
    c0=min(c for r,c in cells); c1=max(c for r,c in cells)
    return r0,r1,c0,c1


def rotate90(g):
    h,w=dims(g)
    return [[g[h-1-r][c] for r in range(h)] for c in range(w)]


def rotate180(g):
    return [row[::-1] for row in g[::-1]]


def rotate270(g):
    return rotate90(rotate180(g))


def flip_h(g):
    return [row[::-1] for row in g]


def transpose(g):
    h,w=dims(g)
    return [[g[r][c] for r in range(h)] for c in range(w)]


def components(g, bg=0, diag=False):
    h,w=dims(g)
    dirs=DIR8 if diag else DIR4
    seen=[[False]*w for _ in range(h)]
    comps=[]
    for r in range(h):
        for c in range(w):
            if g[r][c]!=bg and not seen[r][c]:
                color=g[r][c]
                q=[(r,c)]
                seen[r][c]=True
                cells=[]
                while q:
                    rr,cc=q.pop()
                    cells.append((rr,cc))
                    for dr,dc in dirs:
                        nr,nc=rr+dr,cc+dc
                        if 0<=nr<h and 0<=nc<w and not seen[nr][nc] and g[nr][nc]==color:
                            seen[nr][nc]=True
                            q.append((nr,nc))
                comps.append({"color":color,"cells":cells})
    return comps


def normalize_object(cells):
    r0=min(r for r,c in cells); c0=min(c for r,c in cells)
    return sorted((r-r0,c-c0) for r,c in cells)


def object_to_grid(cells, color=1):
    if not cells:
        return [[0]]
    r0,r1,c0,c1=bbox_of_cells(cells)
    h,w=r1-r0+1,c1-c0+1
    g=blank(h,w)
    for r,c in cells:
        g[r-r0][c-c0]=color
    return g


def neighbors4(r,c,h,w):
    for dr,dc in DIR4:
        nr,nc=r+dr,c+dc
        if 0<=nr<h and 0<=nc<w:
            yield nr,nc


def is_frame_component(comp_cells, color, g):
    r0,r1,c0,c1=bbox_of_cells(comp_cells)
    # all bbox border cells same color and every component cell on border and border complete
    border={(r0,c) for c in range(c0,c1+1)} | {(r1,c) for c in range(c0,c1+1)} | {(r,c0) for r in range(r0,r1+1)} | {(r,c1) for r in range(r0,r1+1)}
    cellset=set(comp_cells)
    return cellset==border and r1-r0>=2 and c1-c0>=2


def apply_transform_code(g, code):
    if code==1:
        return rotate90(g)
    elif code==2:
        return rotate180(g)
    elif code==3:
        return flip_h(g)
    elif code==4:
        return transpose(g)
    else:
        return g


def portal_pairs(g):
    h,w=dims(g)
    portals=defaultdict(list)
    for r in range(h):
        for c in range(w):
            if g[r][c] in (4,5,6):
                portals[g[r][c]].append((r,c))
    pair={}
    for color,pts in portals.items():
        if len(pts)==2:
            a,b=pts
            pair[a]=b; pair[b]=a
    return pair


def solve_easy_p01(g:Grid)->Grid:
    out=deepcopy_grid(g)
    h,w=dims(g)
    for r in range(h):
        # for each color, find positions
        positions=defaultdict(list)
        for c,v in enumerate(g[r]):
            if v!=0:
                positions[v].append(c)
        for color, cols in positions.items():
            if len(cols)==2:
                c1,c2=cols
                if all(g[r][c]==0 for c in range(c1+1,c2)):
                    for c in range(c1,c2+1):
                        out[r][c]=color
    return out


def solve_easy_p02(g:Grid)->Grid:
    out=deepcopy_grid(g)
    h,w=dims(g)
    seeds=[(r,c,g[r][c]) for r in range(h) for c in range(w) if g[r][c]!=0]
    # assume one or multiple same-color non-conflicting seeds
    for r,c,color in seeds:
        for cc in range(w):
            out[r][cc]=color
        for rr in range(h):
            out[rr][c]=color
    return out


def solve_easy_p03(g:Grid)->Grid:
    h,w=dims(g)
    assert h==w
    out=deepcopy_grid(g)
    for r in range(h):
        for c in range(w):
            if g[r][c]!=0:
                out[c][r]=g[r][c]
    return out


def solve_easy_p04(g:Grid)->Grid:
    h,w=dims(g)
    out=blank(h,w)
    for r in range(h):
        c=0
        while c<w:
            if g[r][c]==0:
                c+=1; continue
            color=g[r][c]
            c2=c
            while c2<w and g[r][c2]==color:
                c2+=1
            length=c2-c
            if length>=3 and length%2==1:
                out[r][c+length//2]=color
            c=c2
    return out


def solve_easy_p05(g:Grid)->Grid:
    h,w=dims(g)
    out=deepcopy_grid(g)
    for r in range(h-2):
        for c in range(w-2):
            vals=[g[r+dr][c+dc] for dr in range(3) for dc in range(3) if not (dr==1 and dc==1)]
            center=g[r+1][c+1]
            nz=[v for v in vals if v!=0]
            if center==0 and len(nz)==8 and len(set(nz))==1:
                out[r+1][c+1]=nz[0]
    return out


def solve_easy_p06(g:Grid)->Grid:
    h,w=dims(g)
    out=blank(h,w)
    for c in range(w):
        vals=[g[r][c] for r in range(h) if g[r][c]!=0]
        start=h-len(vals)
        for i,v in enumerate(vals):
            out[start+i][c]=v
    return out


def solve_easy_p07(g:Grid)->Grid:
    out=deepcopy_grid(g)
    h,w=dims(g)
    positions=defaultdict(set)
    for r in range(h):
        for c in range(w):
            v=g[r][c]
            if v!=0:
                positions[v].add((r,c))
    for color,cells in positions.items():
        cells=list(cells)
        # iterate possible rectangles
        for i in range(len(cells)):
            for j in range(i+1,len(cells)):
                r1,c1=cells[i]; r2,c2=cells[j]
                if r1==r2 or c1==c2: 
                    continue
                corners={(r1,c1),(r1,c2),(r2,c1),(r2,c2)}
                present=sum(1 for p in corners if p in positions[color])
                if present==3:
                    for rr,cc in corners:
                        if out[rr][cc]==0:
                            out[rr][cc]=color
    return out


def solve_medium_p01(g:Grid)->Grid:
    comps=components(g,bg=0,diag=False)
    # distinct sizes expected
    comps_sorted=sorted(comps, key=lambda comp: len(comp["cells"]))
    color_map={}
    # smallest->2, middle->3, largest->4 (or sequential starting 2)
    for idx,comp in enumerate(comps_sorted):
        color_map[id(comp)] = idx+2
    out=blank(*dims(g))
    for idx,comp in enumerate(comps_sorted):
        newc=idx+2
        for r,c in comp["cells"]:
            out[r][c]=newc
    return out


def solve_medium_p02(g:Grid)->Grid:
    h,w=dims(g)
    out=blank(h,w)
    for comp in components(g,bg=0,diag=False):
        color=comp["color"]
        r0,r1,c0,c1=bbox_of_cells(comp["cells"])
        for r in range(r0,r1+1):
            for c in range(c0,c1+1):
                out[r][c]=color
    return out


def solve_medium_p03(g:Grid)->Grid:
    # key cell in one corner gives target color
    h,w=dims(g)
    key_positions=[(0,0),(0,w-1),(h-1,0),(h-1,w-1)]
    key_color=None
    for r,c in key_positions:
        if g[r][c]!=0:
            key_color=g[r][c]
            break
    # find object of that color excluding corner key cells
    cells=[(r,c) for r in range(h) for c in range(w) if g[r][c]==key_color and (r,c) not in key_positions]
    return object_to_grid(cells,key_color)


def solve_medium_p04(g:Grid)->Grid:
    comps=components(g,bg=0,diag=False)
    frames=[]
    for comp in comps:
        if is_frame_component(comp["cells"], comp["color"], g):
            r0,r1,c0,c1=bbox_of_cells(comp["cells"])
            interior=[row[c0+1:c1] for row in g[r0+1:r1]]
            frames.append((comp["color"], interior))
    frames.sort(key=lambda x:x[0])
    if not frames:
        return [[0]]
    heights=[len(interior) for _,interior in frames]
    widths=[len(interior[0]) if interior else 0 for _,interior in frames]
    out_h=max(heights)
    out_w=sum(widths)+(len(frames)-1)
    out=blank(out_h,out_w)
    x=0
    for i,(color,interior) in enumerate(frames):
        ih=len(interior); iw=len(interior[0]) if interior else 0
        top=(out_h-ih)//2
        for r in range(ih):
            for c in range(iw):
                out[top+r][x+c]=interior[r][c]
        x+=iw
        if i!=len(frames)-1:
            x+=1
    return out


def solve_medium_p05(g:Grid)->Grid:
    # marker count = number of 9s in top row
    h,w=dims(g)
    count=sum(1 for v in g[0] if v==9)%4
    g2=deepcopy_grid(g)
    for c in range(w):
        if g2[0][c]==9:
            g2[0][c]=0
    obj=crop_bbox(g2)
    if count==1:
        return rotate90(obj)
    elif count==2:
        return rotate180(obj)
    elif count==3:
        return rotate270(obj)
    else:
        return obj


def solve_medium_p06(g:Grid)->Grid:
    # one object summarized as bottom aligned histogram by bbox columns
    comps=components(g,bg=0,diag=False)
    if not comps:
        return [[0]]
    # largest object maybe
    comp=max(comps, key=lambda comp: len(comp["cells"]))
    color=comp["color"]
    r0,r1,c0,c1=bbox_of_cells(comp["cells"])
    # count in bbox each col how many cells of object
    counts=[]
    cellset=set(comp["cells"])
    for c in range(c0,c1+1):
        cnt=sum((r,c) in cellset for r in range(r0,r1+1))
        counts.append(cnt)
    h=max(counts) if counts else 1
    w=len(counts)
    out=blank(h,w)
    for c,cnt in enumerate(counts):
        for r in range(h-cnt,h):
            out[r][c]=color
    return out


def solve_medium_p07(g:Grid)->Grid:
    # fill every enclosed zero region with adjacent surrounding color if unique
    h,w=dims(g)
    out=deepcopy_grid(g)
    seen=[[False]*w for _ in range(h)]
    for r in range(h):
        for c in range(w):
            if g[r][c]==0 and not seen[r][c]:
                q=[(r,c)]; seen[r][c]=True; cells=[]; touches_border=False; neigh_colors=set()
                while q:
                    rr,cc=q.pop()
                    cells.append((rr,cc))
                    if rr in (0,h-1) or cc in (0,w-1):
                        touches_border=True
                    for nr,nc in neighbors4(rr,cc,h,w):
                        if g[nr][nc]==0 and not seen[nr][nc]:
                            seen[nr][nc]=True
                            q.append((nr,nc))
                        elif g[nr][nc]!=0:
                            neigh_colors.add(g[nr][nc])
                if not touches_border and len(neigh_colors)==1:
                    color=next(iter(neigh_colors))
                    for rr,cc in cells:
                        out[rr][cc]=color
    return out


def solve_hard_p01(g:Grid)->Grid:
    h,w=dims(g)
    key_color=g[0][0]
    marker_count=sum(1 for c in range(1,w) if g[0][c]==9)
    transform_code=marker_count  # 1..4
    key_positions={(0,0)} | {(0,c) for c in range(1,w) if g[0][c]==9}
    cells=[(r,c) for r in range(h) for c in range(w) if g[r][c]==key_color and (r,c) not in key_positions]
    obj=object_to_grid(cells,key_color)
    out=apply_transform_code(obj, transform_code)
    return out


def solve_hard_p02(g:Grid)->Grid:
    h,w=dims(g)
    start=goal=None
    for r in range(h):
        for c in range(w):
            if g[r][c]==2: start=(r,c)
            elif g[r][c]==3: goal=(r,c)
    pair=portal_pairs(g)
    q=deque([start]); prev={start:None}
    while q:
        cur=q.popleft()
        if cur==goal: break
        r,c=cur
        for nr,nc in neighbors4(r,c,h,w):
            cell=g[nr][nc]
            if cell==8:  # wall
                continue
            nxt=(nr,nc)
            # stepping onto portal teleports
            if nxt in pair:
                nxt=pair[nxt]
            if nxt not in prev:
                prev[nxt]=cur
                q.append(nxt)
    out=deepcopy_grid(g)
    if goal not in prev:
        return out
    path=[]
    cur=goal
    while cur is not None:
        path.append(cur); cur=prev[cur]
    path=path[::-1]
    for r,c in path:
        if out[r][c]==0:
            out[r][c]=7
    return out


def solve_hard_p03(g:Grid)->Grid:
    h,w=dims(g)
    comps=components(g,bg=0,diag=False)
    frames=[]; objs=[]
    for comp in comps:
        if is_frame_component(comp["cells"], comp["color"], g):
            r0,r1,c0,c1=bbox_of_cells(comp["cells"])
            frames.append({"color":comp["color"],"cells":comp["cells"],"bbox":(r0,r1,c0,c1),"area":(r1-r0-1)*(c1-c0-1)})
        else:
            objs.append({"color":comp["color"],"cells":comp["cells"],"bbox":bbox_of_cells(comp["cells"]),"area":len(comp["cells"])})
    frames=sorted(frames,key=lambda x:x["area"])
    objs=sorted(objs,key=lambda x:x["area"])
    out=blank(h,w)
    # draw frames only
    for fr in frames:
        for r,c in fr["cells"]:
            out[r][c]=fr["color"]
    for fr,obj in zip(frames,objs):
        r0,r1,c0,c1=fr["bbox"]
        interior_h=r1-r0-1; interior_w=c1-c0-1
        obj_grid=object_to_grid(obj["cells"],obj["color"])
        oh,ow=dims(obj_grid)
        top=r0+1+(interior_h-oh)//2
        left=c0+1+(interior_w-ow)//2
        for r in range(oh):
            for c in range(ow):
                if obj_grid[r][c]!=0:
                    out[top+r][left+c]=obj["color"]
    return out


def solve_hard_p04(g:Grid)->Grid:
    h,w=dims(g)
    op=g[0][0]
    # shapes colors 2 and 3
    cells2=[(r,c) for r in range(h) for c in range(w) if g[r][c]==2 and not (r==0 and c==0)]
    cells3=[(r,c) for r in range(h) for c in range(w) if g[r][c]==3]
    a=set(normalize_object(cells2))
    b=set(normalize_object(cells3))
    # common bbox size
    h1=max((r for r,c in a), default=0)+1 if a else 1
    w1=max((c for r,c in a), default=0)+1 if a else 1
    h2=max((r for r,c in b), default=0)+1 if b else 1
    w2=max((c for r,c in b), default=0)+1 if b else 1
    H=max(h1,h2); W=max(w1,w2)
    aa={(r,c) for r,c in a}
    bb={(r,c) for r,c in b}
    # note: shapes aligned top-left within common canvas
    if op==1:
        res=aa|bb
    elif op==2:
        res=aa&bb
    elif op==3:
        res=(aa^bb)
    else:
        # difference a-b
        res=aa-bb
    out=blank(H,W)
    for r,c in res:
        out[r][c]=4
    return out


def solve_hard_p05(g:Grid)->Grid:
    h,w=dims(g)
    codes=[v for v in g[0] if v in (1,2,3,4)]
    g2=deepcopy_grid(g)
    g2[0]=[0]*w
    obj=crop_bbox(g2)
    states=[]
    cur=obj
    for code in codes:
        cur=apply_transform_code(cur, code)
        states.append(cur)
    if not states:
        return obj
    out_h=max(len(s) for s in states)
    out_w=sum(len(s[0]) for s in states)+(len(states)-1)
    out=blank(out_h,out_w)
    x=0
    for i,s in enumerate(states):
        sh,sw=dims(s)
        top=(out_h-sh)//2
        for r in range(sh):
            for c in range(sw):
                if s[r][c]!=0:
                    out[top+r][x+c]=s[r][c]
        x+=sw
        if i!=len(states)-1:
            x+=1
    return out


def solve_hard_p06(g:Grid)->Grid:
    comps=components(g,bg=0,diag=False)
    # adjacency if orthogonal neighboring cells of different colors
    comp_index={}
    for idx,comp in enumerate(comps):
        for cell in comp["cells"]:
            comp_index[cell]=idx
    adj=[set() for _ in comps]
    h,w=dims(g)
    for r in range(h):
        for c in range(w):
            if g[r][c]==0: continue
            i=comp_index[(r,c)]
            for nr,nc in neighbors4(r,c,h,w):
                if g[nr][nc]!=0 and comp_index[(nr,nc)]!=i:
                    adj[i].add(comp_index[(nr,nc)])
    degree_to_color={0:1,1:2,2:3}
    out=blank(h,w)
    for i,comp in enumerate(comps):
        color=degree_to_color.get(len(adj[i]),4)
        for r,c in comp["cells"]:
            out[r][c]=color
    return out


def solve_hard_p07(g:Grid)->Grid:
    h,w=dims(g)
    # emitter 2 on border, direction inferred pointing inward
    start=None; direction=None
    for r in range(h):
        for c in range(w):
            if g[r][c]==2:
                start=(r,c)
                if r==0: direction=(1,0)
                elif r==h-1: direction=(-1,0)
                elif c==0: direction=(0,1)
                elif c==w-1: direction=(0,-1)
    out=deepcopy_grid(g)
    r,c=start
    dr,dc=direction
    while True:
        r+=dr; c+=dc
        if not (0<=r<h and 0<=c<w):
            break
        cell=g[r][c]
        if cell==8:
            break
        if cell==4:  # slash /
            dr,dc = -dc,-dr
        elif cell==5:  # backslash \
            dr,dc = dc,dr
        else:
            if cell==0:
                out[r][c]=7
            # pass through start/goal? there is no goal
    return out


SOLVERS = {
    'easy_p01': solve_easy_p01,
    'easy_p02': solve_easy_p02,
    'easy_p03': solve_easy_p03,
    'easy_p04': solve_easy_p04,
    'easy_p05': solve_easy_p05,
    'easy_p06': solve_easy_p06,
    'easy_p07': solve_easy_p07,
    'medium_p01': solve_medium_p01,
    'medium_p02': solve_medium_p02,
    'medium_p03': solve_medium_p03,
    'medium_p04': solve_medium_p04,
    'medium_p05': solve_medium_p05,
    'medium_p06': solve_medium_p06,
    'medium_p07': solve_medium_p07,
    'hard_p01': solve_hard_p01,
    'hard_p02': solve_hard_p02,
    'hard_p03': solve_hard_p03,
    'hard_p04': solve_hard_p04,
    'hard_p05': solve_hard_p05,
    'hard_p06': solve_hard_p06,
    'hard_p07': solve_hard_p07
}
