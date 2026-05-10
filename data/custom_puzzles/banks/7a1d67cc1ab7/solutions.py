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

def paste(g:Grid, pat:Grid, top:int, left:int, transparent:int=0, allow_overlap:bool=False)->bool:
    h,w=dims(g); ph,pw=dims(pat)
    if top<0 or left<0 or top+ph>h or left+pw>w:
        return False
    for r in range(ph):
        for c in range(pw):
            v=pat[r][c]
            if v!=transparent:
                if not allow_overlap and g[top+r][left+c]!=0:
                    return False
    for r in range(ph):
        for c in range(pw):
            v=pat[r][c]
            if v!=transparent:
                g[top+r][left+c]=v
    return True

def bbox(cells: Iterable[Tuple[int,int]]) -> Tuple[int,int,int,int]:
    cells=list(cells)
    rs=[r for r,c in cells]; cs=[c for r,c in cells]
    return min(rs), min(cs), max(rs), max(cs)

def crop_bbox(g:Grid, box:Tuple[int,int,int,int]) -> Grid:
    r0,c0,r1,c1=box
    return [row[c0:c1+1] for row in g[r0:r1+1]]

def nonzero_cells(g:Grid):
    h,w=dims(g)
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
            comps.append({"color":v,"cells":cells,"bbox":bbox(cells),"area":len(cells)})
    return comps

def rotate_cw(g:Grid)->Grid:
    h,w=dims(g)
    return [[g[h-1-r][c] for r in range(h)] for c in range(w)]

def rotate_180(g:Grid)->Grid:
    return [row[::-1] for row in g[::-1]]

def flip_h(g:Grid)->Grid:
    return [row[::-1] for row in g]

def anti_diag_reflect(g:Grid)->Grid:
    n=len(g)
    out=clone(g)
    for r in range(n):
        for c in range(n):
            if g[r][c]!=0:
                rr,cc=n-1-c,n-1-r
                out[rr][cc]=g[r][c]
    return out

def hstack(grids:List[Grid], gap:int=1)->Grid:
    if not grids:
        return [[]]
    h=max(len(g) for g in grids)
    total=sum(len(g[0]) for g in grids)+gap*(len(grids)-1)
    out=zeros(h,total)
    x=0
    for i,g in enumerate(grids):
        gh,gw=dims(g)
        top=(h-gh)//2
        paste(out,g,top,x,transparent=0,allow_overlap=False)
        x+=gw
        if i+1<len(grids):
            x+=gap
    return out

def vstack(grids:List[Grid], gap:int=1)->Grid:
    if not grids:
        return [[]]
    w=max(len(g[0]) for g in grids)
    total=sum(len(g) for g in grids)+gap*(len(grids)-1)
    out=zeros(total,w)
    y=0
    for i,g in enumerate(grids):
        gh,gw=dims(g)
        left=(w-gw)//2
        paste(out,g,y,left,transparent=0,allow_overlap=False)
        y+=gh
        if i+1<len(grids):
            y+=gap
    return out

def scale2(g:Grid)->Grid:
    out=[]
    for row in g:
        big=[]
        for v in row:
            big.extend([v,v])
        out.append(big[:]); out.append(big[:])
    return out

def normalize_shape(g:Grid)->Grid:
    cells=nonzero_cells(g)
    if not cells:
        return [[0]]
    return [[1 if v!=0 else 0 for v in row] for row in crop_bbox(g,bbox(cells))]

def same_shape_under_rotation(a:Grid,b:Grid)->bool:
    aa=normalize_shape(a)
    bb=normalize_shape(b)
    cur=aa
    for _ in range(4):
        if cur==bb:
            return True
        cur=rotate_cw(cur)
    return False

def count_holes_binary(bin_grid:Grid)->int:
    h,w=dims(bin_grid)
    seen=[[False]*w for _ in range(h)]
    holes=0
    for r in range(h):
        for c in range(w):
            if bin_grid[r][c]!=0 or seen[r][c]:
                continue
            seen[r][c]=True
            q=deque([(r,c)])
            cells=[(r,c)]
            touches = (r==0 or c==0 or r==h-1 or c==w-1)
            while q:
                rr,cc=q.popleft()
                for dr,dc in [(1,0),(-1,0),(0,1),(0,-1)]:
                    nr,nc=rr+dr,cc+dc
                    if 0<=nr<h and 0<=nc<w and not seen[nr][nc] and bin_grid[nr][nc]==0:
                        seen[nr][nc]=True
                        q.append((nr,nc))
                        cells.append((nr,nc))
                        if nr==0 or nc==0 or nr==h-1 or nc==w-1:
                            touches=True
            if not touches:
                holes+=1
    return holes

def find_frames(g:Grid, frame_color:int=9):
    comps=connected_components(g, colors={frame_color})
    frames=[]
    for comp in comps:
        cells=set(comp["cells"])
        r0,c0,r1,c1=comp["bbox"]
        want=set()
        for c in range(c0,c1+1):
            want.add((r0,c)); want.add((r1,c))
        for r in range(r0,r1+1):
            want.add((r,c0)); want.add((r,c1))
        if cells==want and r1-r0>=2 and c1-c0>=2:
            frames.append({"bbox":(r0,c0,r1,c1),"cells":comp["cells"]})
    frames.sort(key=lambda fr:(fr["bbox"][0],fr["bbox"][1]))
    return frames

def interior_box(frame):
    r0,c0,r1,c1=frame["bbox"]
    return (r0+1,c0+1,r1-1,c1-1)

def crop_interior(g:Grid, frame):
    r0,c0,r1,c1=interior_box(frame)
    return [row[c0:c1+1] for row in g[r0:r1+1]]

def crop_nonzero(g:Grid)->Grid:
    cells=nonzero_cells(g)
    if not cells:
        return [[0]]
    return crop_bbox(g,bbox(cells))

def apply_transform(g:Grid, code:int)->Grid:
    if code==2 or code==5:  # some tasks use 2=id, some 5=id
        return clone(g)
    if code==3 or code==6:  # 3/6 -> rot_cw
        return rotate_cw(g)
    if code==4:
        return rotate_180(g)
    if code==7:
        return flip_h(g)
    if code==8:
        return flip_v(g)
    raise ValueError(code)

def recolor_nonzero(g:Grid, color:int)->Grid:
    return [[color if v!=0 else 0 for v in row] for row in g]

def solve_easy_57_complete_anti_diagonal_symmetry(g:Grid)->Grid:
    return anti_diag_reflect(g)

def solve_easy_58_vertical_shadows_to_floor(g:Grid)->Grid:
    h,w=dims(g)
    out=zeros(h,w)
    for r in range(h):
        for c in range(w):
            if g[r][c]!=0:
                for rr in range(r,h):
                    out[rr][c]=g[r][c]
    return out

def solve_easy_59_drop_single_object_to_floor(g:Grid)->Grid:
    h,w=dims(g)
    cells=nonzero_cells(g)
    if not cells:
        return clone(g)
    shift=h-1-max(r for r,c in cells)
    out=zeros(h,w)
    for r,c in cells:
        out[r+shift][c]=g[r][c]
    return out

def solve_easy_60_keep_border_touching_components(g:Grid)->Grid:
    h,w=dims(g)
    out=zeros(h,w)
    for comp in connected_components(g):
        if any(r in (0,h-1) or c in (0,w-1) for r,c in comp["cells"]):
            for r,c in comp["cells"]:
                out[r][c]=comp["color"]
    return out

def solve_easy_61_read_row_colors_into_column(g:Grid)->Grid:
    out=[]
    for row in g:
        vals=[v for v in row if v!=0]
        if vals:
            out.append([vals[0]])
    return out if out else [[0]]

def solve_easy_62_markers_to_keyed_shapes(g:Grid)->Grid:
    h,w=dims(g)
    out=zeros(h,w)
    for r in range(h):
        for c in range(w):
            v=g[r][c]
            if v==2:
                for dc in (-1,0,1):
                    out[r][c+dc]=2
            elif v==3:
                for dr in (-1,0,1):
                    out[r+dr][c]=3
            elif v==4:
                for dr,dc in [(0,0),(-1,0),(1,0),(0,-1),(0,1)]:
                    out[r+dr][c+dc]=4
    return out

def solve_easy_63_complete_2x2_from_diagonal_pairs(g:Grid)->Grid:
    h,w=dims(g)
    out=clone(g)
    for r in range(h-1):
        for c in range(w-1):
            vals=[g[r][c],g[r][c+1],g[r+1][c],g[r+1][c+1]]
            non=[v for v in vals if v!=0]
            if len(non)==2 and len(set(non))==1:
                if (g[r][c]!=0 and g[r+1][c+1]!=0 and g[r][c+1]==0 and g[r+1][c]==0) or \
                   (g[r][c+1]!=0 and g[r+1][c]!=0 and g[r][c]==0 and g[r+1][c+1]==0):
                    color=non[0]
                    out[r][c]=out[r][c+1]=out[r+1][c]=out[r+1][c+1]=color
    return out

def solve_medium_57_sort_rows_by_occupancy(g:Grid)->Grid:
    rows=sorted(g, key=lambda row: sum(v!=0 for v in row), reverse=True)
    return [row[:] for row in rows]

def solve_medium_58_fill_bbox_overlap_by_key(g:Grid)->Grid:
    h,w=dims(g)
    red=[(r,c) for r in range(h) for c in range(w) if g[r][c]==2]
    blue=[(r,c) for r in range(h) for c in range(w) if g[r][c]==1]
    key=[g[r][c] for r in range(h) for c in range(w) if g[r][c] not in (0,1,2)][0]
    rr0,rc0,rr1,rc1=bbox(red)
    br0,bc0,br1,bc1=bbox(blue)
    r0=max(rr0,br0); c0=max(rc0,bc0); r1=min(rr1,br1); c1=min(rc1,bc1)
    out=zeros(h,w)
    if r0<=r1 and c0<=c1:
        for r in range(r0,r1+1):
            for c in range(c0,c1+1):
                out[r][c]=key
    return out

def solve_medium_59_transform_strip_from_key_row(g:Grid)->Grid:
    h,w=dims(g)
    keys=[v for v in g[h-1] if v!=0]
    source=[[g[r][c] if r<h-1 else 0 for c in range(w)] for r in range(h-1)]
    source=crop_nonzero(source)
    out_parts=[]
    for k in keys:
        tg=apply_transform(source, k)
        out_parts.append(tg)
    return hstack(out_parts, gap=1)

def solve_medium_60_translate_components_to_matching_markers(g:Grid)->Grid:
    h,w=dims(g)
    comps=connected_components(g)
    by_color=defaultdict(list)
    for comp in comps:
        by_color[comp["color"]].append(comp)
    out=zeros(h,w)
    for color,items in by_color.items():
        marker=min(items, key=lambda comp: comp["area"])
        obj=max(items, key=lambda comp: comp["area"])
        mr,mc=marker["cells"][0]
        r0,c0,r1,c1=obj["bbox"]
        dr,dc=mr-r0,mc-c0
        for r,c in obj["cells"]:
            out[r+dr][c+dc]=color
    return out

def solve_medium_61_order_framed_crops_by_key(g:Grid)->Grid:
    frames=find_frames(g,9)
    parts=[]
    for fr in frames:
        r0,c0,r1,c1=fr["bbox"]
        key_cells=[g[r0-1][c] for c in range(c0,c1+1) if r0-1>=0 and g[r0-1][c]!=0 and g[r0-1][c]!=9]
        key=key_cells[0]
        interior=crop_interior(g,fr)
        part=crop_nonzero([[0 if v==9 else v for v in row] for row in interior])
        parts.append((key,part))
    parts.sort(key=lambda kp: kp[0])
    return hstack([p for _,p in parts], gap=1)

def solve_medium_62_frame_color_presence_matrix(g:Grid)->Grid:
    palette=[v for v in g[0] if v!=0 and v!=9]
    frames=find_frames(g,9)
    rows=[]
    for fr in frames:
        interior=crop_interior(g,fr)
        colors=set(v for row in interior for v in row if v not in (0,9))
        rows.append([col if col in colors else 0 for col in palette])
    return rows

def solve_medium_63_crop_unique_180_symmetric_component(g:Grid)->Grid:
    good=[]
    for comp in connected_components(g):
        crop=crop_bbox(g, comp["bbox"])
        crop=[[comp["color"] if (r+comp["bbox"][0], c+comp["bbox"][1]) in set(comp["cells"]) else 0 for c in range(len(crop[0]))] for r,row in enumerate(crop)]
        norm=normalize_shape(crop)
        if rotate_180(norm)==norm:
            good.append(crop_nonzero(crop))
    # exactly one by construction
    return good[0]

def solve_hard_57_frame_select_rank_transform_pack(g:Grid)->Grid:
    frames=find_frames(g,9)
    parts=[]
    for fr in frames:
        r0,c0,r1,c1=fr["bbox"]
        sel=[g[r0-1][c] for c in range(c0,c1+1) if r0-1>=0 and g[r0-1][c] not in (0,9)]
        tr=[g[r][c0-1] for r in range(r0,r1+1) if c0-1>=0 and g[r][c0-1] not in (0,9)]
        sel_key=sel[0]; tr_key=tr[0]
        ibox=interior_box(fr)
        ir0,ic0,ir1,ic1=ibox
        sub=[row[ic0:ic1+1] for row in g[ir0:ir1+1]]
        comps=connected_components(sub)
        comps.sort(key=lambda comp: comp["area"])
        chosen=comps[0] if sel_key==2 else comps[-1]
        part=zeros(ir1-ir0+1, ic1-ic0+1)
        for r,c in chosen["cells"]:
            part[r][c]=chosen["color"]
        part=crop_nonzero(part)
        if tr_key==4:
            part=rotate_cw(part)
        elif tr_key==5:
            part=flip_h(part)
        elif tr_key==6:
            part=rotate_180(part)
        parts.append(part)
    return hstack(parts, gap=1)

def solve_hard_58_template_code_mosaic_recolor(g:Grid)->Grid:
    h,w=dims(g)
    # source uses color 1, code cells use 2-5
    source=crop_nonzero([[1 if g[r][c]==1 else 0 for c in range(w)] for r in range(h)])
    codes=[(r,c,g[r][c]) for r in range(h) for c in range(w) if g[r][c] in (2,3,4,5)]
    rs=[r for r,c,v in codes]; cs=[c for r,c,v in codes]
    r0,c0,r1,c1=min(rs),min(cs),max(rs),max(cs)
    code_grid=[[g[r][c] if g[r][c] in (2,3,4,5) else 0 for c in range(c0,c1+1)] for r in range(r0,r1+1)]
    tiles=[]
    for row in code_grid:
        row_tiles=[]
        for code in row:
            if code==0:
                row_tiles.append(zeros(len(source), len(source[0])))
            else:
                if code==2:
                    part=clone(source)
                elif code==3:
                    part=rotate_cw(source)
                elif code==4:
                    part=rotate_180(source)
                elif code==5:
                    part=flip_h(source)
                part=recolor_nonzero(part, code)
                row_tiles.append(part)
        tiles.append(hstack(row_tiles, gap=1))
    return vstack(tiles, gap=1)

def solve_hard_59_typed_relation_matrix(g:Grid)->Grid:
    frames=find_frames(g,9)
    # classify frames: top gallery have minimal top; left gallery have minimal left, excluding corner none
    tops=sorted(set(fr["bbox"][0] for fr in frames))
    lefts=sorted(set(fr["bbox"][1] for fr in frames))
    top_band=min(tops)
    left_band=min(lefts)
    row_frames=[fr for fr in frames if fr["bbox"][0]==top_band]
    col_frames=[fr for fr in frames if fr["bbox"][1]==left_band and fr["bbox"][0]!=top_band]
    row_frames.sort(key=lambda fr: fr["bbox"][1])
    col_frames.sort(key=lambda fr: fr["bbox"][0])
    row_parts=[]; col_parts=[]
    for fr in row_frames:
        interior=crop_nonzero(crop_interior(g,fr))
        row_parts.append(interior)
    for fr in col_frames:
        interior=crop_nonzero(crop_interior(g,fr))
        col_parts.append(interior)
    out=zeros(len(col_parts), len(row_parts))
    for i,a in enumerate(col_parts):
        acol=next(v for row in a for v in row if v!=0)
        for j,b in enumerate(row_parts):
            bcol=next(v for row in b for v in row if v!=0)
            same_shape=same_shape_under_rotation(a,b)
            same_color=(acol==bcol)
            out[i][j]=8 if same_shape and same_color else 6 if same_shape else 3 if same_color else 0
    return out

def solve_hard_60_select_by_hole_count_scale_to_marker(g:Grid)->Grid:
    h,w=dims(g)
    key=next(v for row in g for v in row if v in (2,3))
    need={2:1,3:2}[key]
    marker=next((r,c) for r in range(h) for c in range(w) if g[r][c]==8)
    comps=[comp for comp in connected_components(g) if comp["color"]==4]
    chosen=None
    for comp in comps:
        part=zeros(h,w)
        for r,c in comp["cells"]:
            part[r][c]=4
        crop=crop_nonzero(part)
        holes=count_holes_binary(normalize_shape(crop))
        if holes==need:
            chosen=crop
            break
    part=scale2(chosen)
    out=zeros(h,w)
    paste(out, part, marker[0], marker[1], transparent=0, allow_overlap=False)
    return out

def solve_hard_61_local_bbox_overlap_gallery(g:Grid)->Grid:
    frames=find_frames(g,9)
    parts=[]
    for fr in frames:
        r0,c0,r1,c1=fr["bbox"]
        key=next(g[r0-1][c] for c in range(c0,c1+1) if r0-1>=0 and g[r0-1][c] not in (0,9))
        interior=crop_interior(g,fr)
        red=[(r,c) for r,row in enumerate(interior) for c,v in enumerate(row) if v==2]
        blue=[(r,c) for r,row in enumerate(interior) for c,v in enumerate(row) if v==1]
        rr0,rc0,rr1,rc1=bbox(red)
        br0,bc0,br1,bc1=bbox(blue)
        a0=max(rr0,br0); b0=max(rc0,bc0); a1=min(rr1,br1); b1=min(rc1,bc1)
        part=zeros(a1-a0+1,b1-b0+1)
        for r in range(a1-a0+1):
            for c in range(b1-b0+1):
                part[r][c]=key
        parts.append(part)
    return hstack(parts, gap=1)

def solve_hard_62_library_select_transform_gallery(g:Grid)->Grid:
    h,w=dims(g)
    frames=find_frames(g,9)
    library={}
    for fr in frames:
        r0,c0,r1,c1=fr["bbox"]
        if r1 < h-3:  # library frames above code rows
            key=next(g[r0-1][c] for c in range(c0,c1+1) if r0-1>=0 and g[r0-1][c] not in (0,9))
            library[key]=crop_nonzero(crop_interior(g,fr))
    selector_row=[v for v in g[h-2] if v in library]
    transform_row=[v for v in g[h-1] if v in (5,6,7)]
    parts=[]
    for s,t in zip(selector_row, transform_row):
        part=clone(library[s])
        if t==5:
            part=clone(part)
        elif t==6:
            part=rotate_cw(part)
        elif t==7:
            part=flip_h(part)
        parts.append(part)
    return hstack(parts, gap=1)

def solve_hard_63_boolean_gallery_from_two_templates(g:Grid)->Grid:
    h,w=dims(g)
    frames=find_frames(g,9)
    frames.sort(key=lambda fr: fr["bbox"][1])
    A=normalize_shape(crop_interior(g,frames[0]))
    B=normalize_shape(crop_interior(g,frames[1]))
    # make same dims
    hh=max(len(A),len(B)); ww=max(len(A[0]),len(B[0]))
    def pad(x):
        out=zeros(hh,ww)
        paste(out, x, (hh-len(x))//2, (ww-len(x[0]))//2)
        return out
    A=pad(A); B=pad(B)
    codes=[v for v in g[h-1] if v in (4,5,6,7)]
    parts=[]
    for code in codes:
        out=zeros(hh,ww)
        for r in range(hh):
            for c in range(ww):
                a=A[r][c]!=0; b=B[r][c]!=0
                keep=False
                if code==4: keep=a or b
                elif code==5: keep=a and b
                elif code==6: keep=a and not b
                elif code==7: keep=(a!=b)
                out[r][c]=code if keep else 0
        parts.append(crop_nonzero(out))
    return hstack(parts, gap=1)

SOLVERS = {
    "solve_easy_57_complete_anti_diagonal_symmetry": solve_easy_57_complete_anti_diagonal_symmetry,
    "solve_easy_58_vertical_shadows_to_floor": solve_easy_58_vertical_shadows_to_floor,
    "solve_easy_59_drop_single_object_to_floor": solve_easy_59_drop_single_object_to_floor,
    "solve_easy_60_keep_border_touching_components": solve_easy_60_keep_border_touching_components,
    "solve_easy_61_read_row_colors_into_column": solve_easy_61_read_row_colors_into_column,
    "solve_easy_62_markers_to_keyed_shapes": solve_easy_62_markers_to_keyed_shapes,
    "solve_easy_63_complete_2x2_from_diagonal_pairs": solve_easy_63_complete_2x2_from_diagonal_pairs,
    "solve_medium_57_sort_rows_by_occupancy": solve_medium_57_sort_rows_by_occupancy,
    "solve_medium_58_fill_bbox_overlap_by_key": solve_medium_58_fill_bbox_overlap_by_key,
    "solve_medium_59_transform_strip_from_key_row": solve_medium_59_transform_strip_from_key_row,
    "solve_medium_60_translate_components_to_matching_markers": solve_medium_60_translate_components_to_matching_markers,
    "solve_medium_61_order_framed_crops_by_key": solve_medium_61_order_framed_crops_by_key,
    "solve_medium_62_frame_color_presence_matrix": solve_medium_62_frame_color_presence_matrix,
    "solve_medium_63_crop_unique_180_symmetric_component": solve_medium_63_crop_unique_180_symmetric_component,
    "solve_hard_57_frame_select_rank_transform_pack": solve_hard_57_frame_select_rank_transform_pack,
    "solve_hard_58_template_code_mosaic_recolor": solve_hard_58_template_code_mosaic_recolor,
    "solve_hard_59_typed_relation_matrix": solve_hard_59_typed_relation_matrix,
    "solve_hard_60_select_by_hole_count_scale_to_marker": solve_hard_60_select_by_hole_count_scale_to_marker,
    "solve_hard_61_local_bbox_overlap_gallery": solve_hard_61_local_bbox_overlap_gallery,
    "solve_hard_62_library_select_transform_gallery": solve_hard_62_library_select_transform_gallery,
    "solve_hard_63_boolean_gallery_from_two_templates": solve_hard_63_boolean_gallery_from_two_templates,
}

def verify_bank(json_path: str | Path | None = None) -> None:
    if json_path is None:
        json_path = Path(__file__).with_name("arc_puzzle_bank_ninth_21.json")
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
