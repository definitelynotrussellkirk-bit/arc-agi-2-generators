from __future__ import annotations

import json
from pathlib import Path
from typing import List, Tuple, Iterable
from collections import deque, defaultdict

Grid = List[List[int]]

def clone(g: Grid) -> Grid:
    return [row[:] for row in g]

def zeros(h:int, w:int, val:int=0) -> Grid:
    return [[val for _ in range(w)] for _ in range(h)]

def dims(g:Grid)->Tuple[int,int]:
    return len(g), len(g[0])

def paste(g:Grid, pat:Grid, top:int, left:int, transparent:int=0)->Grid:
    h,w = dims(g)
    ph,pw = dims(pat)
    for r in range(ph):
        for c in range(pw):
            v = pat[r][c]
            if v != transparent:
                rr,cc = top+r,left+c
                assert 0 <= rr < h and 0 <= cc < w, (rr,cc,h,w)
                g[rr][cc] = v
    return g

def bbox(cells: Iterable[Tuple[int,int]]) -> Tuple[int,int,int,int]:
    cells = list(cells)
    rs = [r for r,c in cells]
    cs = [c for r,c in cells]
    return min(rs), min(cs), max(rs), max(cs)

def crop_bbox(g:Grid, box:Tuple[int,int,int,int]) -> Grid:
    r0,c0,r1,c1 = box
    return [row[c0:c1+1] for row in g[r0:r1+1]]

def nonzero_cells(g:Grid):
    h,w = dims(g)
    return [(r,c) for r in range(h) for c in range(w) if g[r][c]!=0]

def connected_components(g:Grid, colors=None):
    h,w=dims(g)
    seen=[[False]*w for _ in range(h)]
    if colors is not None:
        colors=set(colors)
    comps=[]
    for r in range(h):
        for c in range(w):
            v=g[r][c]
            if v==0 or seen[r][c] or (colors is not None and v not in colors):
                continue
            seen[r][c]=True
            q=deque([(r,c)])
            cells=[]
            while q:
                rr,cc=q.popleft()
                cells.append((rr,cc))
                for dr,dc in [(1,0),(-1,0),(0,1),(0,-1)]:
                    nr,nc=rr+dr,cc+dc
                    if 0<=nr<h and 0<=nc<w and not seen[nr][nc] and g[nr][nc]==v:
                        if colors is None or v in colors:
                            seen[nr][nc]=True
                            q.append((nr,nc))
            comps.append({"color":v,"cells":cells,"bbox":bbox(cells)})
    return comps

def rotate_cw(g:Grid)->Grid:
    h,w=dims(g)
    return [[g[h-1-r][c] for r in range(h)] for c in range(w)]

def rotate_ccw(g:Grid)->Grid:
    h,w=dims(g)
    return [[g[r][w-1-c] for r in range(h)] for c in range(w-1,-1,-1)]

def rotate_180(g:Grid)->Grid:
    return [row[::-1] for row in g[::-1]]

def flip_h(g:Grid)->Grid:
    return [row[::-1] for row in g]

def flip_v(g:Grid)->Grid:
    return g[::-1]

def scale2(g:Grid)->Grid:
    out=[]
    for row in g:
        big=[]
        for v in row:
            big.extend([v,v])
        out.append(big[:]); out.append(big[:])
    return out

def march_until_block(g:Grid, start:Tuple[int,int], dr:int, dc:int, blocker_colors:set[int]|set):
    h,w=dims(g)
    r,c=start
    out=[]
    while True:
        r+=dr; c+=dc
        if not (0<=r<h and 0<=c<w):
            break
        if g[r][c] in blocker_colors:
            break
        out.append((r,c))
    return out

def frame_boxes_from_color(g:Grid,color:int)->List[Tuple[int,int,int,int]]:
    boxes=[]
    for comp in connected_components(g,[color]):
        r0,c0,r1,c1=comp["bbox"]
        ok=True
        for cc in range(c0,c1+1):
            ok &= g[r0][cc]==color and g[r1][cc]==color
        for rr in range(r0,r1+1):
            ok &= g[rr][c0]==color and g[rr][c1]==color
        if ok and r1-r0>=2 and c1-c0>=2:
            boxes.append((r0,c0,r1,c1))
    return sorted(boxes)

def normalize_shape(cells:Iterable[Tuple[int,int]]):
    cells=list(cells)
    r0,c0,r1,c1=bbox(cells)
    return sorted((r-r0,c-c0) for r,c in cells)

def rotations_of_offsets(offsets):
    # offsets relative grid
    pts=list(offsets)
    if not pts:
        return [()]
    rs=[r for r,c in pts]; cs=[c for r,c in pts]
    h=max(rs)+1; w=max(cs)+1
    # convert to grid then rotations
    g=zeros(h,w,0)
    for r,c in pts: g[r][c]=1
    outs=[]
    cur=g
    for _ in range(4):
        cells=nonzero_cells(cur)
        outs.append(tuple(normalize_shape(cells)))
        cur=rotate_cw(cur)
    return outs

def canonical_shape_under_rot(offsets):
    return min(rotations_of_offsets(offsets))

def component_hole_count(comp_grid:Grid)->int:
    h,w=dims(comp_grid)
    solid=[[1 if comp_grid[r][c]!=0 else 0 for c in range(w)] for r in range(h)]
    seen=[[False]*w for _ in range(h)]
    holes=0
    for r in range(h):
        for c in range(w):
            if solid[r][c]==0 and not seen[r][c]:
                seen[r][c]=True
                q=deque([(r,c)])
                touches=r in (0,h-1) or c in (0,w-1)
                while q:
                    rr,cc=q.popleft()
                    for dr,dc in [(1,0),(-1,0),(0,1),(0,-1)]:
                        nr,nc=rr+dr,cc+dc
                        if 0<=nr<h and 0<=nc<w and solid[nr][nc]==0 and not seen[nr][nc]:
                            seen[nr][nc]=True
                            if nr in (0,h-1) or nc in (0,w-1):
                                touches=True
                            q.append((nr,nc))
                if not touches:
                    holes+=1
    return holes

def center_place(canvas_h, canvas_w, obj:Grid):
    out=zeros(canvas_h, canvas_w, 0)
    oh,ow=dims(obj)
    top=(canvas_h-oh)//2
    left=(canvas_w-ow)//2
    paste(out,obj,top,left,transparent=0)
    return out

def solve_easy_50_diagonal_bridge(g:Grid)->Grid:
    out=clone(g)
    pos=defaultdict(list)
    for r,row in enumerate(g):
        for c,v in enumerate(row):
            if v!=0:
                pos[v].append((r,c))
    for color,cells in pos.items():
        if len(cells)>=2:
            # pair farthest apart if same diagonal
            (r0,c0),(r1,c1)=cells[0],cells[-1]
            dr=r1-r0; dc=c1-c0
            if abs(dr)==abs(dc) and dr!=0:
                sr=1 if dr>0 else -1
                sc=1 if dc>0 else -1
                for k in range(abs(dr)+1):
                    out[r0+sr*k][c0+sc*k]=color
    return out

def solve_easy_51_crop_nonzero_bbox(g:Grid)->Grid:
    cells=nonzero_cells(g)
    return crop_bbox(g,bbox(cells))

def solve_easy_52_markers_to_hollow_squares(g:Grid)->Grid:
    h,w=dims(g)
    out=zeros(h,w,0)
    for r in range(1,h-1):
        for c in range(1,w-1):
            v=g[r][c]
            if v!=0:
                for rr in range(r-1,r+2):
                    for cc in range(c-1,c+2):
                        if rr in (r-1,r+1) or cc in (c-1,c+1):
                            out[rr][cc]=v
    return out

def solve_easy_53_keep_tallest_bar(g:Grid)->Grid:
    h,w=dims(g)
    out=zeros(h,w,0)
    best=None
    for c in range(w):
        cells=[r for r in range(h) if g[r][c]!=0]
        if not cells:
            continue
        color=g[cells[0]][c]
        if all(g[r][c]==color for r in cells) and max(cells)-min(cells)+1==len(cells):
            height=len(cells)
            cand=(height,-min(cells),c,color,min(cells),max(cells))
            if best is None or cand>best:
                best=cand
    if best:
        _,_,c,color,r0,r1=best
        for r in range(r0,r1+1):
            out[r][c]=color
    return out

def solve_easy_54_reflect_main_diagonal(g:Grid)->Grid:
    h,w=dims(g)
    assert h==w
    out=clone(g)
    for r in range(h):
        for c in range(w):
            if g[r][c]!=0:
                out[c][r]=g[r][c]
    return out

def solve_easy_55_move_object_to_marker(g:Grid)->Grid:
    h,w=dims(g)
    marker_color=9
    marker=None
    cells=[]
    for r in range(h):
        for c in range(w):
            v=g[r][c]
            if v==marker_color:
                marker=(r,c)
            elif v!=0:
                cells.append((r,c))
    r0,c0,r1,c1=bbox(cells)
    obj=crop_bbox(g,(r0,c0,r1,c1))
    # clear object and marker
    out=zeros(h,w,0)
    paste(out,obj,marker[0],marker[1],transparent=0)
    return out

def solve_easy_56_pack_nonempty_rows(g:Grid)->Grid:
    rows=[row[:] for row in g if any(v!=0 for v in row)]
    return rows if rows else [[0]*len(g[0])]

def solve_medium_50_emit_rays(g:Grid)->Grid:
    h,w=dims(g)
    out=clone(g)
    dirs={1:(-1,0),2:(0,1),3:(1,0),4:(0,-1)}
    blockers={5}
    for r in range(h):
        for c in range(w):
            v=g[r][c]
            if v in dirs:
                dr,dc=dirs[v]
                for rr,cc in march_until_block(g,(r,c),dr,dc,blockers):
                    if out[rr][cc]==0:
                        out[rr][cc]=v
    return out

def solve_medium_51_keyed_component_rotate(g:Grid)->Grid:
    h,w=dims(g)
    # key is singleton in last row
    key=None
    for c,v in enumerate(g[-1]):
        if v!=0:
            key=v; break
    comps=connected_components(g)
    # ignore key singleton on last row (component of size1 at last row)
    target=None
    for comp in comps:
        if comp["color"]==key and not (len(comp["cells"])==1 and comp["cells"][0][0]==h-1):
            target=comp
            break
    return rotate_cw(crop_bbox(g,target["bbox"]))

def solve_medium_52_sort_components_by_area(g:Grid)->Grid:
    comps=connected_components(g)
    comps_sorted=sorted(comps,key=lambda comp:(len(comp["cells"]), comp["bbox"][0], comp["bbox"][1]))
    pieces=[crop_bbox(g,comp["bbox"]) for comp in comps_sorted]
    heights=[len(p) for p in pieces]
    widths=[len(p[0]) for p in pieces]
    H=max(heights)
    W=sum(widths)+max(0,len(pieces)-1)
    out=zeros(H,W,0)
    x=0
    for p in pieces:
        paste(out,p,0,x,transparent=0)
        x+=len(p[0])+1
    return out

def solve_medium_53_equality_matrix(g:Grid)->Grid:
    h,w=dims(g)
    top=g[0][1:]
    left=[g[r][0] for r in range(1,h)]
    out=zeros(h-1,w-1,0)
    for r,a in enumerate(left):
        for c,b in enumerate(top):
            if a!=0 and a==b:
                out[r][c]=a
    return out

def solve_medium_54_checker_fill_bboxes(g:Grid)->Grid:
    h,w=dims(g)
    out=zeros(h,w,0)
    for comp in connected_components(g):
        color=comp["color"]
        r0,c0,r1,c1=comp["bbox"]
        for r in range(r0,r1+1):
            for c in range(c0,c1+1):
                if (r-r0 + c-c0)%2==0:
                    out[r][c]=color
    return out

def solve_medium_55_recolor_template_stamp(g:Grid)->Grid:
    h,w=dims(g)
    # template is the only color-1 component, markers are singletons of colors !=1
    comps=connected_components(g)
    template_comp=None
    markers=[]
    for comp in comps:
        if comp["color"]==1 and len(comp["cells"])>1:
            template_comp=comp
        elif len(comp["cells"])==1:
            markers.append((comp["cells"][0], comp["color"]))
    tmpl=crop_bbox(g,template_comp["bbox"])
    # normalize template to color 1 footprint with zeros preserved
    mask=[[1 if v==1 else 0 for v in row] for row in tmpl]
    out=zeros(h,w,0)
    for (r,c),color in markers:
        pat=[[color if cell==1 else 0 for cell in row] for row in mask]
        paste(out,pat,r,c,transparent=0)
    return out

def solve_medium_56_frame_majority_centers(g:Grid)->Grid:
    out=zeros(*dims(g),0)
    for box in frame_boxes_from_color(g,8):
        r0,c0,r1,c1=box
        for c in range(c0,c1+1):
            out[r0][c]=8; out[r1][c]=8
        for r in range(r0,r1+1):
            out[r][c0]=8; out[r][c1]=8
        counts=defaultdict(int)
        for r in range(r0+1,r1):
            for c in range(c0+1,c1):
                v=g[r][c]
                if v not in (0,8):
                    counts[v]+=1
        if counts:
            color=sorted(counts.items(), key=lambda kv:(-kv[1], kv[0]))[0][0]
            cr=(r0+r1)//2; cc=(c0+c1)//2
            out[cr][cc]=color
    return out

def solve_hard_50_frame_direction_rays(g:Grid)->Grid:
    h,w=dims(g)
    out=zeros(h,w,0)
    dirs={1:(-1,0),2:(0,1),3:(1,0),4:(0,-1)}
    for box in frame_boxes_from_color(g,8):
        r0,c0,r1,c1=box
        # copy frame and blockers/emitter
        for c in range(c0,c1+1):
            out[r0][c]=8; out[r1][c]=8
        for r in range(r0,r1+1):
            out[r][c0]=8; out[r][c1]=8
        emitter=None; key=None
        blockers=[]
        for r in range(r0+1,r1):
            for c in range(c0+1,c1):
                v=g[r][c]
                if v==6:
                    emitter=(r,c)
                    out[r][c]=6
                elif v==7:
                    out[r][c]=7
                elif v in dirs:
                    key=v
                    out[r][c]=v
        dr,dc=dirs[key]
        r,c=emitter
        while True:
            r+=dr; c+=dc
            if not (r0<r<r1 and c0<c<c1):
                break
            if g[r][c]==7:
                break
            if out[r][c] in (0,):
                out[r][c]=6
    return out

def solve_hard_51_dual_template_rotation_mosaic(g:Grid)->Grid:
    comps=connected_components(g)
    t6=max([comp for comp in comps if comp["color"]==6], key=lambda comp: len(comp["cells"]))
    t7=max([comp for comp in comps if comp["color"]==7], key=lambda comp: len(comp["cells"]))
    A=crop_bbox(g,t6["bbox"])
    B=crop_bbox(g,t7["bbox"])
    # code cells are values 1..8 not part of template bboxes
    used=set(t6["cells"])|set(t7["cells"])
    code_cells=[(r,c,g[r][c]) for r,row in enumerate(g) for c,v in enumerate(row) if v in range(1,9) and (r,c) not in used]
    r0=min(r for r,c,v in code_cells); c0=min(c for r,c,v in code_cells)
    r1=max(r for r,c,v in code_cells); c1=max(c for r,c,v in code_cells)
    code=[[0]*(c1-c0+1) for _ in range(r1-r0+1)]
    for r,c,v in code_cells:
        code[r-r0][c-c0]=v
    th,tw=dims(A)
    ch,cw=dims(code)
    out=zeros(ch*th, cw*tw, 0)
    for rr in range(ch):
        for cc in range(cw):
            v=code[rr][cc]
            if 1<=v<=4:
                pat=A
                k=v-1
            else:
                pat=B
                k=v-5
            cur=pat
            for _ in range(k):
                cur=rotate_cw(cur)
            paste(out,cur,rr*th,cc*tw,transparent=0)
    return out

def solve_hard_52_shape_similarity_matrix(g:Grid)->Grid:
    comps=connected_components(g)
    comps=sorted(comps,key=lambda comp:(comp["bbox"][0],comp["bbox"][1]))
    canons=[]
    for comp in comps:
        offs=normalize_shape(comp["cells"])
        canons.append(canonical_shape_under_rot(offs))
    n=len(comps)
    out=zeros(n,n,0)
    for i in range(n):
        for j in range(n):
            if i==j:
                out[i][j]=5
            elif canons[i]==canons[j]:
                out[i][j]=8
    return out

def solve_hard_53_frame_select_rank_center(g:Grid)->Grid:
    h,w=dims(g)
    out=zeros(h,w,0)
    for frame_color in (8,9):
        for box in frame_boxes_from_color(g,frame_color):
            r0,c0,r1,c1=box
            # copy frame
            for c in range(c0,c1+1):
                out[r0][c]=frame_color; out[r1][c]=frame_color
            for r in range(r0,r1+1):
                out[r][c0]=frame_color; out[r][c1]=frame_color
            key=None
            interior=zeros(r1-r0-1,c1-c0-1,0)
            for r in range(r0+1,r1):
                for c in range(c0+1,c1):
                    v=g[r][c]
                    if v in (1,2) and key is None:
                        key=v
                    elif v!=0:
                        interior[r-(r0+1)][c-(c0+1)]=v
            comps=connected_components(interior)
            # choose by size
            comps=sorted(comps,key=lambda comp:(len(comp["cells"]),comp["bbox"][0],comp["bbox"][1]))
            chosen=comps[0] if key==1 else comps[-1]
            obj=crop_bbox(interior,chosen["bbox"])
            if frame_color==9:
                obj=rotate_180(obj)
            canvas_h=r1-r0-1; canvas_w=c1-c0-1
            placed=center_place(canvas_h,canvas_w,obj)
            paste(out,placed,r0+1,c0+1,transparent=0)
    return out

def solve_hard_54_boolean_ops_panel(g:Grid)->Grid:
    comps=connected_components(g)
    A=crop_bbox(g,max([comp for comp in comps if comp["color"]==2], key=lambda comp: len(comp["cells"]))["bbox"])
    B=crop_bbox(g,max([comp for comp in comps if comp["color"]==3], key=lambda comp: len(comp["cells"]))["bbox"])
    h,w=dims(A)
    assert dims(B)==(h,w)
    def mask(grid,color):
        return [[1 if v==color else 0 for v in row] for row in grid]
    ma=mask(A,2); mb=mask(B,3)
    def build(kind):
        out=zeros(h,w,0)
        for r in range(h):
            for c in range(w):
                a=ma[r][c]; b=mb[r][c]
                on=False
                if kind=="union": on=a or b
                elif kind=="inter": on=a and b
                elif kind=="a_minus_b": on=a and not b
                elif kind=="b_minus_a": on=b and not a
                if on: out[r][c]=8
        return out
    tl=build("union"); tr=build("inter"); bl=build("a_minus_b"); br=build("b_minus_a")
    out=zeros(h*2+1,w*2+1,0)
    paste(out,tl,0,0); paste(out,tr,0,w+1); paste(out,bl,h+1,0); paste(out,br,h+1,w+1)
    return out

def solve_hard_55_sort_by_holes(g:Grid)->Grid:
    comps=connected_components(g)
    pieces=[]
    for comp in comps:
        piece=crop_bbox(g,comp["bbox"])
        holes=component_hole_count(piece)
        pieces.append(( -holes, comp["bbox"][0], comp["bbox"][1], piece))
    pieces.sort()
    pats=[p[-1] for p in pieces]
    H=max(len(p) for p in pats)
    W=sum(len(p[0]) for p in pats)+len(pats)-1
    out=zeros(H,W,0)
    x=0
    for pat in pats:
        paste(out,pat,0,x,transparent=0)
        x+=len(pat[0])+1
    return out

def solve_hard_56_frame_transform_gallery(g:Grid)->Grid:
    # frames color 8, 4 frames with 3x3 interior object bbox and one key cell color 1-4 at interior bottom-right
    boxes=sorted(frame_boxes_from_color(g,8), key=lambda box:(box[0],box[1]))
    tiles=[]
    for box in boxes:
        r0,c0,r1,c1=box
        interior=zeros(r1-r0-1,c1-c0-1,0)
        key=None
        for r in range(r0+1,r1):
            for c in range(c0+1,c1):
                v=g[r][c]
                if (r,c)==(r1-1,c1-1):
                    key=v
                else:
                    interior[r-(r0+1)][c-(c0+1)]=v
        # crop object bbox within interior
        cells=nonzero_cells(interior)
        obj=crop_bbox(interior,bbox(cells))
        if key==1:
            trans=obj
        elif key==2:
            trans=flip_h(obj)
        elif key==3:
            trans=flip_v(obj)
        elif key==4:
            trans=rotate_cw(obj)
        else:
            raise ValueError(key)
        # embed in 3x3 tile (or max 3x3)
        tile=zeros(3,3,0)
        oh,ow=dims(trans)
        paste(tile,trans,(3-oh)//2,(3-ow)//2,transparent=0)
        tiles.append(tile)
    out=zeros(3*2+1,3*2+1,0)
    paste(out,tiles[0],0,0); paste(out,tiles[1],0,4); paste(out,tiles[2],4,0); paste(out,tiles[3],4,4)
    return out

SOLVERS = {
    "solve_easy_50_diagonal_bridge": solve_easy_50_diagonal_bridge,
    "solve_easy_51_crop_nonzero_bbox": solve_easy_51_crop_nonzero_bbox,
    "solve_easy_52_markers_to_hollow_squares": solve_easy_52_markers_to_hollow_squares,
    "solve_easy_53_keep_tallest_bar": solve_easy_53_keep_tallest_bar,
    "solve_easy_54_reflect_main_diagonal": solve_easy_54_reflect_main_diagonal,
    "solve_easy_55_move_object_to_marker": solve_easy_55_move_object_to_marker,
    "solve_easy_56_pack_nonempty_rows": solve_easy_56_pack_nonempty_rows,
    "solve_medium_50_emit_rays": solve_medium_50_emit_rays,
    "solve_medium_51_keyed_component_rotate": solve_medium_51_keyed_component_rotate,
    "solve_medium_52_sort_components_by_area": solve_medium_52_sort_components_by_area,
    "solve_medium_53_equality_matrix": solve_medium_53_equality_matrix,
    "solve_medium_54_checker_fill_bboxes": solve_medium_54_checker_fill_bboxes,
    "solve_medium_55_recolor_template_stamp": solve_medium_55_recolor_template_stamp,
    "solve_medium_56_frame_majority_centers": solve_medium_56_frame_majority_centers,
    "solve_hard_50_frame_direction_rays": solve_hard_50_frame_direction_rays,
    "solve_hard_51_dual_template_rotation_mosaic": solve_hard_51_dual_template_rotation_mosaic,
    "solve_hard_52_shape_similarity_matrix": solve_hard_52_shape_similarity_matrix,
    "solve_hard_53_frame_select_rank_center": solve_hard_53_frame_select_rank_center,
    "solve_hard_54_boolean_ops_panel": solve_hard_54_boolean_ops_panel,
    "solve_hard_55_sort_by_holes": solve_hard_55_sort_by_holes,
    "solve_hard_56_frame_transform_gallery": solve_hard_56_frame_transform_gallery,
}

def verify_bank(json_path: str | Path | None = None) -> None:
    if json_path is None:
        json_path = Path(__file__).with_name("arc_puzzle_bank_eighth_21.json")
    json_path = Path(json_path)
    tasks = json.loads(json_path.read_text())
    for task in tasks:
        solver = SOLVERS[task["solver_name"]]
        for pair in task["train"] + task["test"]:
            got = solver(pair["input"])
            if got != pair["output"]:
                raise AssertionError(f"Mismatch in {task['id']} via {task['solver_name']}")
    print(f"verified {len(tasks)} tasks from {json_path.name}")

if __name__ == "__main__":
    verify_bank()