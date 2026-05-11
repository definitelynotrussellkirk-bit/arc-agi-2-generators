from __future__ import annotations

import json
from pathlib import Path
from typing import List
from collections import deque, defaultdict

Grid = List[List[int]]


def zeros(h,w,val=0):
    return [[val for _ in range(w)] for _ in range(h)]


def clone(g):
    return [row[:] for row in g]


def dims(g):
    return len(g), len(g[0])


def paste(g, pat, top, left, transparent=0, allow_overlap=False):
    h,w=dims(g); ph,pw=dims(pat)
    if top<0 or left<0 or top+ph>h or left+pw>w:
        return False
    for r in range(ph):
        for c in range(pw):
            v=pat[r][c]
            if v!=transparent and not allow_overlap and g[top+r][left+c]!=0:
                return False
    for r in range(ph):
        for c in range(pw):
            v=pat[r][c]
            if v!=transparent:
                g[top+r][left+c]=v
    return True


def bbox(cells):
    rs=[r for r,c in cells]; cs=[c for r,c in cells]
    return min(rs), min(cs), max(rs), max(cs)


def crop_bbox(g, box):
    r0,c0,r1,c1=box
    return [row[c0:c1+1] for row in g[r0:r1+1]]


def nonzero_cells(g):
    h,w=dims(g)
    return [(r,c) for r in range(h) for c in range(w) if g[r][c]!=0]


def crop_nonzero(g):
    cells=nonzero_cells(g)
    if not cells:
        return [[0]]
    return crop_bbox(g, bbox(cells))


def connected_components(g, colors=None):
    h,w=dims(g)
    colors = None if colors is None else set(colors)
    seen=[[False]*w for _ in range(h)]
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
                    if 0<=nr<h and 0<=nc<w and not seen[nr][nc] and g[nr][nc]==v and (colors is None or v in colors):
                        seen[nr][nc]=True
                        q.append((nr,nc))
            comps.append({'color':v,'cells':cells,'bbox':bbox(cells),'area':len(cells)})
    return comps


def recolor(g, color):
    return [[color if v!=0 else 0 for v in row] for row in g]


def scale2(g):
    h,w=dims(g)
    out=zeros(h*2,w*2)
    for r in range(h):
        for c in range(w):
            v=g[r][c]
            out[2*r][2*c]=out[2*r+1][2*c]=out[2*r][2*c+1]=out[2*r+1][2*c+1]=v
    return out


def rotate_cw(g):
    h,w=dims(g)
    return [[g[h-1-r][c] for r in range(h)] for c in range(w)]


def rotate_ccw(g):
    h,w=dims(g)
    return [[g[r][w-1-c] for r in range(h)] for c in range(w)]


def rotate_180(g):
    return [row[::-1] for row in g[::-1]]


def flip_h(g):  # horizontal mirror left-right
    return [row[::-1] for row in g]


def flip_v(g):
    return g[::-1]


def hstack(grids, gap=1, bg=0):
    if not grids:
        return [[]]
    h=max(len(g) for g in grids)
    total=sum(len(g[0]) for g in grids)+gap*(len(grids)-1)
    out=zeros(h,total,bg)
    x=0
    for i,g in enumerate(grids):
        gh,gw=dims(g)
        paste(out,g,(h-gh)//2,x,transparent=bg,allow_overlap=False)
        x+=gw
        if i!=len(grids)-1:
            x+=gap
    return out


def vstack(grids, gap=1, bg=0):
    if not grids:
        return [[]]
    w=max(len(g[0]) for g in grids)
    total=sum(len(g) for g in grids)+gap*(len(grids)-1)
    out=zeros(total,w,bg)
    y=0
    for i,g in enumerate(grids):
        gh,gw=dims(g)
        paste(out,g,y,(w-gw)//2,transparent=bg,allow_overlap=False)
        y+=gh
        if i!=len(grids)-1:
            y+=gap
    return out


def draw_rect_border(g,r0,c0,r1,c1,color):
    for c in range(c0,c1+1):
        g[r0][c]=color; g[r1][c]=color
    for r in range(r0,r1+1):
        g[r][c0]=color; g[r][c1]=color


def normalize_binary(g):
    return tuple(tuple(1 if v!=0 else 0 for v in row) for row in crop_nonzero(g))


def dihedral_variants(g):
    vars=[]
    cur=g
    for _ in range(4):
        vars.append(normalize_binary(cur))
        vars.append(normalize_binary(flip_h(cur)))
        cur=rotate_cw(cur)
    # unique preserving order
    out=[]
    seen=set()
    for v in vars:
        if v not in seen:
            seen.add(v)
            out.append(v)
    return out


def is_vertically_symmetric(g):
    b=normalize_binary(g)
    return b == tuple(tuple(reversed(row)) for row in b)


def hole_count(g):
    b=[[1 if v!=0 else 0 for v in row] for row in crop_nonzero(g)]
    h,w=len(b),len(b[0])
    seen=[[False]*w for _ in range(h)]
    holes=0
    for r in range(h):
        for c in range(w):
            if b[r][c]==0 and not seen[r][c]:
                q=deque([(r,c)]); seen[r][c]=True
                touches=False
                while q:
                    rr,cc=q.popleft()
                    if rr==0 or rr==h-1 or cc==0 or cc==w-1:
                        touches=True
                    for dr,dc in [(1,0),(-1,0),(0,1),(0,-1)]:
                        nr,nc=rr+dr,cc+dc
                        if 0<=nr<h and 0<=nc<w and not seen[nr][nc] and b[nr][nc]==0:
                            seen[nr][nc]=True
                            q.append((nr,nc))
                if not touches:
                    holes+=1
    return holes


def panel_positions_2x2(panel_h, panel_w, gap=1, top=0, left=0):
    # return positions for 4 panels row-major
    return [
        (top, left),
        (top, left+panel_w+gap),
        (top+panel_h+gap, left),
        (top+panel_h+gap, left+panel_w+gap),
    ]


def crop_panel(g, top,left,h,w):
    return [row[left:left+w] for row in g[top:top+h]]


def apply_transform(g, code):
    if code==1:
        return g
    if code==2:
        return rotate_cw(g)
    if code==3:
        return rotate_180(g)
    if code==4:
        return rotate_ccw(g)
    if code==5:
        return flip_h(g)
    raise ValueError(code)


def clear_line(g, r1,c1,r2,c2, color):
    # inclusive line on same row or col; all cells 0 or color
    if r1==r2:
        for c in range(min(c1,c2), max(c1,c2)+1):
            if g[r1][c] not in (0,color):
                return False
        return True
    if c1==c2:
        for r in range(min(r1,r2), max(r1,r2)+1):
            if g[r][c1] not in (0,color):
                return False
        return True
    return False


def draw_line(out, r1,c1,r2,c2,color):
    if r1==r2:
        for c in range(min(c1,c2), max(c1,c2)+1):
            out[r1][c]=color
    elif c1==c2:
        for r in range(min(r1,r2), max(r1,r2)+1):
            out[r][c1]=color


def boolean_combine(a,b,op):
    h,w=dims(a)
    out=zeros(h,w)
    for r in range(h):
        for c in range(w):
            x=a[r][c]!=0; y=b[r][c]!=0
            if op==1:
                z=x and y
            elif op==2:
                z=x or y
            elif op==3:
                z=(x!=y)
            else:
                raise ValueError(op)
            out[r][c]=8 if z else 0
    return out



def solve_easy_78_fill_axis_spans_between_matching_endpoints(g):
    out=clone(g)
    pos=defaultdict(list)
    h,w=dims(g)
    for r in range(h):
        for c in range(w):
            v=g[r][c]
            if v!=0:
                pos[v].append((r,c))
    for color, cells in pos.items():
        if len(cells)!=2:
            continue
        (r1,c1),(r2,c2)=cells
        if r1==r2:
            for c in range(min(c1,c2), max(c1,c2)+1):
                out[r1][c]=color
        elif c1==c2:
            for r in range(min(r1,r2), max(r1,r2)+1):
                out[r][c1]=color
    return out


def solve_easy_79_fill_rectangles_from_diagonal_corners(g):
    out=clone(g)
    pos=defaultdict(list)
    h,w=dims(g)
    for r in range(h):
        for c in range(w):
            v=g[r][c]
            if v!=0:
                pos[v].append((r,c))
    for color,cells in pos.items():
        if len(cells)!=2:
            continue
        (r1,c1),(r2,c2)=cells
        r0,r1s=sorted([r1,r2]); c0,c1s=sorted([c1,c2])
        for r in range(r0,r1s+1):
            for c in range(c0,c1s+1):
                out[r][c]=color
    return out


def solve_easy_80_compact_columns_downward(g):
    h,w=dims(g)
    out=zeros(h,w)
    for c in range(w):
        vals=[g[r][c] for r in range(h) if g[r][c]!=0]
        start=h-len(vals)
        for i,v in enumerate(vals):
            out[start+i][c]=v
    return out


def solve_easy_81_mirror_left_half_across_divider(g):
    out=clone(g)
    h,w=dims(g)
    divider=None
    # find uniform nonzero full column
    for c in range(w):
        vals=[g[r][c] for r in range(h)]
        nz=[v for v in vals if v!=0]
        if len(nz)==h and len(set(nz))==1:
            divider=c
            break
    if divider is None:
        divider=w//2
    for r in range(h):
        for c in range(divider):
            v=g[r][c]
            if v!=0:
                out[r][2*divider-c]=v
    return out


def solve_easy_82_draw_object_bounding_boxes(g):
    out=clone(g)
    for comp in connected_components(g):
        r0,c0,r1,c1=comp['bbox']
        draw_rect_border(out,r0,c0,r1,c1,comp['color'])
    return out


def solve_easy_83_complete_l_trominoes_to_2x2(g):
    out=clone(g)
    for comp in connected_components(g):
        if comp['area']!=3:
            continue
        r0,c0,r1,c1=comp['bbox']
        if r1-r0==1 and c1-c0==1:
            cells=set(comp['cells'])
            for rr in range(r0,r1+1):
                for cc in range(c0,c1+1):
                    if (rr,cc) not in cells:
                        out[rr][cc]=comp['color']
    return out


def solve_easy_84_recolor_border_touching_components(g):
    h,w=dims(g)
    out=clone(g)
    for comp in connected_components(g):
        r0,c0,r1,c1=comp['bbox']
        if r0==0 or c0==0 or r1==h-1 or c1==w-1:
            for r,c in comp['cells']:
                out[r][c]=7
    return out


def solve_medium_78_recolor_canvas_via_two_row_legend(g):
    h,w=dims(g)
    mapping={}
    for c in range(w):
        a=g[0][c]; b=g[1][c]
        if a!=0 and b!=0:
            mapping[a]=b
    canvas=[row[:] for row in g[3:]]
    out=zeros(len(canvas), len(canvas[0]))
    for r in range(len(canvas)):
        for c in range(len(canvas[0])):
            v=canvas[r][c]
            out[r][c]=mapping.get(v, v)
    return out


def solve_medium_79_rotate_cropped_object_by_control_color(g):
    code=g[0][0]
    work=clone(g)
    work[0][0]=0
    obj=crop_nonzero(work)
    return apply_transform(obj, code)


def solve_medium_80_connect_pairs_with_clear_elbow_path(g):
    out=clone(g)
    pos=defaultdict(list)
    h,w=dims(g)
    for r in range(h):
        for c in range(w):
            v=g[r][c]
            if v not in (0,5):
                pos[v].append((r,c))
    for color,cells in pos.items():
        if len(cells)!=2:
            continue
        (r1,c1),(r2,c2)=cells
        elbows=[(r1,c2),(r2,c1)]
        chosen=None
        for er,ec in elbows:
            if clear_line(g,r1,c1,er,ec,color) and clear_line(g,er,ec,r2,c2,color):
                chosen=(er,ec)
                break
        if chosen is None:
            continue
        er,ec=chosen
        draw_line(out,r1,c1,er,ec,color)
        draw_line(out,er,ec,r2,c2,color)
    return out


def solve_medium_81_select_area_matched_component_scale2(g):
    k=sum(1 for v in g[0] if v==1)
    work=[row[:] for row in g[1:]]
    comps=connected_components(work)
    target=min([c for c in comps if c['area']==k], key=lambda c:(c['bbox'][0],c['bbox'][1]))
    return scale2(crop_bbox(work, target['bbox']))


def solve_medium_82_stack_cropped_objects_by_left_to_right_order(g):
    comps=sorted(connected_components(g), key=lambda c:(c['bbox'][1], c['bbox'][0]))
    pieces=[crop_bbox(g, comp['bbox']) for comp in comps]
    return vstack(pieces, gap=1)


def solve_medium_83_select_vertically_symmetric_object_and_recolor(g):
    target_color=g[0][0]
    work=clone(g)
    work[0][0]=0
    comps=connected_components(work)
    candidates=[]
    for comp in comps:
        cropped=crop_bbox(work, comp['bbox'])
        if is_vertically_symmetric(cropped):
            candidates.append(comp)
    target=min(candidates, key=lambda c:(c['bbox'][0], c['bbox'][1]))
    return recolor(crop_bbox(work, target['bbox']), target_color)


def solve_medium_84_project_2x2_blocks_to_mini_grid(g):
    h,w=dims(g)
    blocks=[]
    used=set()
    for r in range(h-1):
        for c in range(w-1):
            vals=[g[r+i][c+j] for i in range(2) for j in range(2)]
            if vals[0]!=0 and len(set(vals))==1:
                cells={(r+i,c+j) for i in range(2) for j in range(2)}
                if not any(cell in used for cell in cells):
                    blocks.append((r,c,vals[0]))
                    used |= cells
    rows=sorted({r for r,c,color in blocks})
    cols=sorted({c for r,c,color in blocks})
    out=zeros(len(rows), len(cols))
    rix={r:i for i,r in enumerate(rows)}
    cix={c:i for i,c in enumerate(cols)}
    for r,c,color in blocks:
        out[rix[r]][cix[c]]=color
    return out


def solve_hard_78_library_decode_select_transform_recolor_shape(g):
    # row0: blue markers count -> 1..4 panel index; col5 transform code; col7 target color
    index=sum(1 for v in g[0][:4] if v==1)
    code=g[0][5]
    target=g[0][7]
    positions=panel_positions_2x2(4,4,gap=1,top=2,left=0)
    top,left=positions[index-1]
    panel=crop_panel(g, top,left,4,4)
    obj=crop_nonzero(panel)
    transformed=apply_transform(obj, code)
    return recolor(transformed, target)


def solve_hard_79_dihedral_equivalence_matrix_ignoring_color(g):
    positions=panel_positions_2x2(4,4,gap=1,top=0,left=0)
    objs=[crop_nonzero(crop_panel(g,top,left,4,4)) for top,left in positions]
    variants=[set(dihedral_variants(obj)) for obj in objs]
    out=zeros(4,4)
    for i in range(4):
        for j in range(4):
            if normalize_binary(objs[j]) in variants[i]:
                out[i][j]=8
    return out


def solve_hard_80_select_object_by_holes_and_symmetry_scale2(g):
    holes_req=sum(1 for v in g[0] if v==1)-1
    sym_req=(g[0][4]==2)
    target_color=g[0][6]
    work=[row[:] for row in g[1:]]
    comps=connected_components(work)
    choices=[]
    for comp in comps:
        cropped=crop_bbox(work, comp['bbox'])
        if hole_count(cropped)==holes_req and is_vertically_symmetric(cropped)==sym_req:
            choices.append(comp)
    target=min(choices, key=lambda c:(c['bbox'][0], c['bbox'][1]))
    return recolor(scale2(crop_bbox(work, target['bbox'])), target_color)


def solve_hard_81_fill_partitioned_chambers_by_internal_keys(g):
    h,w=dims(g)
    out=clone(g)
    seen=[[False]*w for _ in range(h)]
    for r in range(h):
        for c in range(w):
            if g[r][c]==5 or seen[r][c]:
                continue
            q=deque([(r,c)]); seen[r][c]=True
            cells=[]; colors=set()
            while q:
                rr,cc=q.popleft()
                cells.append((rr,cc))
                if g[rr][cc] not in (0,5):
                    colors.add(g[rr][cc])
                for dr,dc in [(1,0),(-1,0),(0,1),(0,-1)]:
                    nr,nc=rr+dr,cc+dc
                    if 0<=nr<h and 0<=nc<w and not seen[nr][nc] and g[nr][nc]!=5:
                        seen[nr][nc]=True
                        q.append((nr,nc))
            if len(colors)==1:
                color=next(iter(colors))
                for rr,cc in cells:
                    if out[rr][cc]==0:
                        out[rr][cc]=color
    return out


def solve_hard_82_boolean_mosaic_from_row_and_column_templates(g):
    op=g[1][1]
    row_templates=[
        crop_panel(g,0,4,3,3),
        crop_panel(g,0,8,3,3),
    ]
    col_templates=[
        crop_panel(g,4,0,3,3),
        crop_panel(g,8,0,3,3),
    ]
    rows=[]
    for ctemp in col_templates:
        panels=[]
        for rtemp in row_templates:
            panels.append(boolean_combine(rtemp, ctemp, op))
        rows.append(hstack(panels, gap=1))
    return vstack(rows, gap=1)


def solve_hard_83_sort_objects_by_holes_then_area_and_pack(g):
    comps=connected_components(g)
    comps=sorted(comps, key=lambda c:(-hole_count(crop_bbox(g, c['bbox'])), -c['area'], c['bbox'][0], c['bbox'][1]))
    pieces=[crop_bbox(g, comp['bbox']) for comp in comps]
    return hstack(pieces, gap=1)


def solve_hard_84_decode_sequence_of_transformed_library_shapes(g):
    idx_codes=[g[0][c] for c in (0,2,4)]
    tf_codes=[g[1][c] for c in (0,2,4)]
    colors=[g[2][c] for c in (0,2,4)]
    panels=[crop_panel(g,4,0,4,4), crop_panel(g,4,5,4,4), crop_panel(g,4,10,4,4)]
    pieces=[]
    for idx, tf, color in zip(idx_codes, tf_codes, colors):
        obj=crop_nonzero(panels[idx-1])
        transformed=apply_transform(obj, tf)
        pieces.append(recolor(transformed, color))
    return hstack(pieces, gap=1)



SOLVERS = {
    "solve_easy_78_fill_axis_spans_between_matching_endpoints": solve_easy_78_fill_axis_spans_between_matching_endpoints,
    "solve_easy_79_fill_rectangles_from_diagonal_corners": solve_easy_79_fill_rectangles_from_diagonal_corners,
    "solve_easy_80_compact_columns_downward": solve_easy_80_compact_columns_downward,
    "solve_easy_81_mirror_left_half_across_divider": solve_easy_81_mirror_left_half_across_divider,
    "solve_easy_82_draw_object_bounding_boxes": solve_easy_82_draw_object_bounding_boxes,
    "solve_easy_83_complete_l_trominoes_to_2x2": solve_easy_83_complete_l_trominoes_to_2x2,
    "solve_easy_84_recolor_border_touching_components": solve_easy_84_recolor_border_touching_components,
    "solve_medium_78_recolor_canvas_via_two_row_legend": solve_medium_78_recolor_canvas_via_two_row_legend,
    "solve_medium_79_rotate_cropped_object_by_control_color": solve_medium_79_rotate_cropped_object_by_control_color,
    "solve_medium_80_connect_pairs_with_clear_elbow_path": solve_medium_80_connect_pairs_with_clear_elbow_path,
    "solve_medium_81_select_area_matched_component_scale2": solve_medium_81_select_area_matched_component_scale2,
    "solve_medium_82_stack_cropped_objects_by_left_to_right_order": solve_medium_82_stack_cropped_objects_by_left_to_right_order,
    "solve_medium_83_select_vertically_symmetric_object_and_recolor": solve_medium_83_select_vertically_symmetric_object_and_recolor,
    "solve_medium_84_project_2x2_blocks_to_mini_grid": solve_medium_84_project_2x2_blocks_to_mini_grid,
    "solve_hard_78_library_decode_select_transform_recolor_shape": solve_hard_78_library_decode_select_transform_recolor_shape,
    "solve_hard_79_dihedral_equivalence_matrix_ignoring_color": solve_hard_79_dihedral_equivalence_matrix_ignoring_color,
    "solve_hard_80_select_object_by_holes_and_symmetry_scale2": solve_hard_80_select_object_by_holes_and_symmetry_scale2,
    "solve_hard_81_fill_partitioned_chambers_by_internal_keys": solve_hard_81_fill_partitioned_chambers_by_internal_keys,
    "solve_hard_82_boolean_mosaic_from_row_and_column_templates": solve_hard_82_boolean_mosaic_from_row_and_column_templates,
    "solve_hard_83_sort_objects_by_holes_then_area_and_pack": solve_hard_83_sort_objects_by_holes_then_area_and_pack,
    "solve_hard_84_decode_sequence_of_transformed_library_shapes": solve_hard_84_decode_sequence_of_transformed_library_shapes,
}


def verify_against_json(json_path: Path | None = None) -> None:
    if json_path is None:
        json_path = Path(__file__).with_name("arc_puzzle_bank_twelfth_21.json")
    data = json.loads(json_path.read_text())
    for task in data:
        solver = SOLVERS[task["solver_name"]]
        for section in ("train", "test"):
            for pair in task[section]:
                got = solver(pair["input"])
                if got != pair["output"]:
                    raise AssertionError(f"Mismatch for {task['id']} in {section}")
    print(f"verified {len(data)} tasks against {json_path.name}")


if __name__ == "__main__":
    verify_against_json()
