from __future__ import annotations
from typing import List, Dict, Callable
from collections import deque, Counter, defaultdict

Grid = List[List[int]]

def clone(g: Grid) -> Grid:
    return [row[:] for row in g]


def zeros(h: int, w: int, val: int=0) -> Grid:
    return [[val]*w for _ in range(h)]


def dims(g): return len(g), len(g[0])


def place_cells(g: Grid, cells: List[Tuple[int,int]], color: int):
    h,w=dims(g)
    for r,c in cells:
        assert 0<=r<h and 0<=c<w, (r,c,h,w)
        g[r][c]=color
    return g


def components_by_color(g: Grid, target_colors=None):
    h,w=dims(g)
    seen=[[False]*w for _ in range(h)]
    comps=[]
    for r in range(h):
        for c in range(w):
            if seen[r][c] or g[r][c]==0: 
                continue
            col=g[r][c]
            if target_colors is not None and col not in target_colors:
                seen[r][c]=True
                continue
            q=deque([(r,c)]); seen[r][c]=True; cells=[]
            while q:
                rr,cc=q.popleft(); cells.append((rr,cc))
                for dr,dc in [(-1,0),(1,0),(0,-1),(0,1)]:
                    nr,nc=rr+dr,cc+dc
                    if 0<=nr<h and 0<=nc<w and not seen[nr][nc] and g[nr][nc]==col:
                        seen[nr][nc]=True; q.append((nr,nc))
            comps.append({'color':col,'cells':cells})
    return comps


def bbox(cells):
    rs=[r for r,c in cells]; cs=[c for r,c in cells]
    return min(rs), min(cs), max(rs), max(cs)


def norm(cells):
    r0,c0,_,_=bbox(cells)
    return sorted((r-r0,c-c0) for r,c in cells)


def touches_border(cells, h, w):
    return any(r==0 or c==0 or r==h-1 or c==w-1 for r,c in cells)


def is_L_triomino(cells):
    if len(cells)!=3: return False
    r0,c0,r1,c1=bbox(cells)
    if r1-r0!=1 or c1-c0!=1: return False
    # 3 of 4 cells in 2x2 box
    return len(set(cells))==3


def is_plus5(cells):
    if len(cells)!=5: return False
    pts=set(norm(cells))
    return pts=={(1,1),(0,1),(2,1),(1,0),(1,2)}


def mirror_across_col(cells, bar_col):
    return [(r, 2*bar_col-c) for r,c in cells]


def rotate_offsets(offsets, k):
    # k times 90 clockwise around (0,0)
    pts=offsets
    out=[]
    for r,c in pts:
        rr,cc=r,c
        for _ in range(k%4):
            rr,cc=cc,-rr
        out.append((rr,cc))
    return out


def is_vertically_symmetric(cells):
    r0,c0,r1,c1=bbox(cells)
    pts={(r-r0,c-c0) for r,c in cells}
    width=c1-c0
    return pts == {(r, width-c) for r,c in pts}


def solve_easy_01_exact_horizontal_triples(g: Grid) -> Grid:
    out=clone(g)
    h,w=dims(g)
    for r in range(h):
        c=0
        while c<w:
            if g[r][c]!=2:
                c+=1; continue
            s=c
            while c<w and g[r][c]==2:
                c+=1
            if c-s==3:
                for cc in range(s,c):
                    out[r][cc]=7
    return out


def solve_easy_02_frame_2x2_blocks(g: Grid) -> Grid:
    out=clone(g)
    h,w=dims(g)
    for r in range(h-1):
        for c in range(w-1):
            if g[r][c]==g[r+1][c]==g[r][c+1]==g[r+1][c+1]==3:
                for rr in range(r-1,r+3):
                    for cc in range(c-1,c+3):
                        if 0<=rr<h and 0<=cc<w and not (r<=rr<=r+1 and c<=cc<=c+1):
                            if out[rr][cc]==0:
                                out[rr][cc]=5
    return out


def solve_easy_03_recolor_L_by_key(g: Grid) -> Grid:
    out=clone(g)
    key=None
    counts=Counter(v for row in g for v in row if v!=0)
    # key is singleton color not 3
    for color,count in counts.items():
        if color!=3 and count==1:
            key=color
            break
    assert key is not None
    for comp in components_by_color(g, {3}):
        if is_L_triomino(comp['cells']):
            for r,c in comp['cells']:
                out[r][c]=key
    return out


def solve_easy_04_intersections_from_markers(g: Grid) -> Grid:
    out=clone(g)
    h,w=dims(g)
    rows=[r for r in range(1,h) if g[r][0]==2]
    cols=[c for c in range(1,w) if g[0][c]==1]
    for r in rows:
        for c in cols:
            if out[r][c]==0:
                out[r][c]=4
    return out


def solve_easy_05_complete_rectangle_borders_from_corners(g: Grid) -> Grid:
    out=clone(g)
    h,w=dims(g)
    colors=sorted({v for row in g for v in row if v!=0})
    for color in colors:
        cells=[(r,c) for r in range(h) for c in range(w) if g[r][c]==color]
        # look for rectangles by corner quadruples
        rows=sorted({r for r,c in cells}); cols=sorted({c for r,c in cells})
        for i,r1 in enumerate(rows):
            for r2 in rows[i+1:]:
                for j,c1 in enumerate(cols):
                    for c2 in cols[j+1:]:
                        corners={(r1,c1),(r1,c2),(r2,c1),(r2,c2)}
                        if corners.issubset(cells):
                            for cc in range(c1,c2+1):
                                out[r1][cc]=color
                                out[r2][cc]=color
                            for rr in range(r1,r2+1):
                                out[rr][c1]=color
                                out[rr][c2]=color
    return out


def solve_easy_06_mirror_object_across_bar(g: Grid) -> Grid:
    out=clone(g)
    h,w=dims(g)
    bar_col=None
    for c in range(w):
        if all(g[r][c]==5 for r in range(h)):
            bar_col=c
            break
    assert bar_col is not None
    cells=[(r,c) for r in range(h) for c in range(w) if g[r][c]==2]
    for r,c in cells:
        mc=2*bar_col-c
        if 0<=mc<w and out[r][mc]==0:
            out[r][mc]=8
    return out


def solve_easy_07_keep_largest_component_recolor(g: Grid) -> Grid:
    h,w=dims(g)
    out=zeros(h,w)
    comps=components_by_color(g,{3})
    largest=max(comps, key=lambda comp: len(comp['cells']))
    for r,c in largest['cells']:
        out[r][c]=9
    return out


def solve_medium_01_connect_matching_endpoints(g: Grid) -> Grid:
    out=clone(g)
    h,w=dims(g)
    colors=sorted({v for row in g for v in row if v!=0})
    for color in colors:
        cells=[(r,c) for r in range(h) for c in range(w) if g[r][c]==color]
        if len(cells)!=2:
            continue
        (r1,c1),(r2,c2)=cells
        if r1==r2:
            for cc in range(min(c1,c2), max(c1,c2)+1):
                out[r1][cc]=color
        elif c1==c2:
            for rr in range(min(r1,r2), max(r1,r2)+1):
                out[rr][c1]=color
    return out


def solve_medium_02_translate_object_by_vector(g: Grid) -> Grid:
    h,w=dims(g)
    out=zeros(h,w)
    pos1=pos2=None
    obj=[]
    for r in range(h):
        for c in range(w):
            if g[r][c]==1: pos1=(r,c)
            elif g[r][c]==2: pos2=(r,c)
            elif g[r][c]==3: obj.append((r,c))
    dr=pos2[0]-pos1[0]
    dc=pos2[1]-pos1[1]
    for r,c in obj:
        nr,nc=r+dr,c+dc
        if 0<=nr<h and 0<=nc<w:
            out[nr][nc]=8
    return out


def solve_medium_03_fill_keyed_rectangle_holes(g: Grid) -> Grid:
    out=clone(g)
    h,w=dims(g)
    comps=components_by_color(g)
    key=None
    by_color=defaultdict(list)
    for comp in comps:
        by_color[comp['color']].append(comp)
    for color, lst in by_color.items():
        if any(len(comp['cells'])==1 for comp in lst) and any(len(comp['cells'])>1 for comp in lst):
            key=color
            break
    assert key is not None
    for comp in by_color[key]:
        if len(comp['cells'])==1:
            continue
        r0,c0,r1,c1=bbox(comp['cells'])
        good=True
        for cc in range(c0,c1+1):
            if g[r0][cc]!=key or g[r1][cc]!=key: good=False
        for rr in range(r0,r1+1):
            if g[rr][c0]!=key or g[rr][c1]!=key: good=False
        if good and r1-r0>=2 and c1-c0>=2:
            for rr in range(r0+1,r1):
                for cc in range(c0+1,c1):
                    if out[rr][cc]==0:
                        out[rr][cc]=8
    return out


def solve_medium_04_mark_bbox_corners(g: Grid) -> Grid:
    out=clone(g)
    h,w=dims(g)
    for comp in components_by_color(g,{4}):
        r0,c0,r1,c1=bbox(comp['cells'])
        for r,c in [(r0,c0),(r0,c1),(r1,c0),(r1,c1)]:
            out[r][c]=1
    return out


def solve_medium_05_stamp_exemplar_at_targets(g: Grid) -> Grid:
    out=clone(g)
    h,w=dims(g)
    # find exemplar component containing 1 and 3
    seen=[[False]*w for _ in range(h)]
    exemplar_anchor=None
    offsets=None
    for r in range(h):
        for c in range(w):
            if seen[r][c] or g[r][c]==0:
                continue
            # flood any nonzero comp
            q=deque([(r,c)]); seen[r][c]=True; cells=[]
            while q:
                rr,cc=q.popleft(); cells.append((rr,cc))
                for dr,dc in [(-1,0),(1,0),(0,-1),(0,1)]:
                    nr,nc=rr+dr,cc+dc
                    if 0<=nr<h and 0<=nc<w and not seen[nr][nc] and g[nr][nc]!=0:
                        seen[nr][nc]=True; q.append((nr,nc))
            vals=[g[rr][cc] for rr,cc in cells]
            if 1 in vals and 3 in vals:
                exemplar_anchor=next((rr,cc) for rr,cc in cells if g[rr][cc]==1)
                offsets=[(rr-exemplar_anchor[0], cc-exemplar_anchor[1]) for rr,cc in cells if g[rr][cc]==3]
                break
        if exemplar_anchor: break
    assert exemplar_anchor is not None
    targets=[(r,c) for r in range(h) for c in range(w) if g[r][c]==1 and (r,c)!=exemplar_anchor]
    for tr,tc in targets:
        for dr,dc in offsets:
            nr,nc=tr+dr, tc+dc
            if 0<=nr<h and 0<=nc<w and out[nr][nc]==0:
                out[nr][nc]=3
    return out


def solve_medium_06_recolor_border_touching_objects(g: Grid) -> Grid:
    out=clone(g)
    h,w=dims(g)
    for comp in components_by_color(g,{4}):
        if touches_border(comp['cells'], h,w):
            for r,c in comp['cells']:
                out[r][c]=2
    return out


def solve_medium_07_raycast_cross_from_centers(g: Grid) -> Grid:
    out=clone(g)
    h,w=dims(g)
    centers=[(r,c) for r in range(h) for c in range(w) if g[r][c]==6]
    blockers={(r,c) for r in range(h) for c in range(w) if g[r][c]==5}
    for r,c in centers:
        for dr,dc in [(-1,0),(1,0),(0,-1),(0,1)]:
            nr,nc=r+dr,c+dc
            while 0<=nr<h and 0<=nc<w and (nr,nc) not in blockers:
                out[nr][nc]=6
                nr+=dr; nc+=dc
    return out


def solve_hard_01_rotate_exemplar_by_target_color(g: Grid) -> Grid:
    out=clone(g)
    h,w=dims(g)
    # exemplar comp with anchor 1 and body 3
    seen=[[False]*w for _ in range(h)]
    anchor=None
    body_offsets=None
    for r in range(h):
        for c in range(w):
            if seen[r][c] or g[r][c]==0:
                continue
            q=deque([(r,c)]); seen[r][c]=True; cells=[]
            while q:
                rr,cc=q.popleft(); cells.append((rr,cc))
                for dr,dc in [(-1,0),(1,0),(0,-1),(0,1)]:
                    nr,nc=rr+dr,cc+dc
                    if 0<=nr<h and 0<=nc<w and not seen[nr][nc] and g[nr][nc]!=0:
                        seen[nr][nc]=True; q.append((nr,nc))
            vals=[g[rr][cc] for rr,cc in cells]
            if 1 in vals and 3 in vals:
                anchor=next((rr,cc) for rr,cc in cells if g[rr][cc]==1)
                body_offsets=[(rr-anchor[0], cc-anchor[1]) for rr,cc in cells if g[rr][cc]==3]
                break
        if anchor: break
    assert anchor
    rot_map={2:0,4:1,6:2,8:3}
    targets=[(r,c,g[r][c]) for r in range(h) for c in range(w) if g[r][c] in rot_map and (r,c)!=anchor]
    for tr,tc,color in targets:
        roffs=rotate_offsets(body_offsets, rot_map[color])
        for dr,dc in roffs:
            nr,nc=tr+dr, tc+dc
            if 0<=nr<h and 0<=nc<w and out[nr][nc]==0:
                out[nr][nc]=3
    return out


def solve_hard_02_scale_smallest_object_2x(g: Grid) -> Grid:
    h,w=dims(g)
    out=zeros(h,w)
    comps=components_by_color(g,{3})
    smallest=min(comps, key=lambda comp: len(comp['cells']))
    r0,c0,r1,c1=bbox(smallest['cells'])
    pts=[(r-r0,c-c0) for r,c in smallest['cells']]
    for r,c in pts:
        base_r=r0+2*r
        base_c=c0+2*c
        for dr in [0,1]:
            for dc in [0,1]:
                nr,nc=base_r+dr, base_c+dc
                if 0<=nr<h and 0<=nc<w:
                    out[nr][nc]=8
    return out


def solve_hard_03_dual_key_select_and_recolor(g: Grid) -> Grid:
    out=clone(g)
    counts=Counter(v for row in g for v in row if v!=0)
    color_key=None
    shape_key=None
    # color key among {2,6,8} with singleton
    for color in [2,6,8]:
        if counts[color]==1:
            color_key=color
    # shape key among {1,4} with singleton
    for color in [1,4]:
        if counts[color]==1:
            shape_key=color
    assert color_key is not None and shape_key is not None
    for comp in components_by_color(g,{3}):
        fam='L' if is_L_triomino(comp['cells']) else 'PLUS' if is_plus5(comp['cells']) else None
        if (shape_key==1 and fam=='L') or (shape_key==4 and fam=='PLUS'):
            for r,c in comp['cells']:
                out[r][c]=color_key
    return out


def solve_hard_04_row_col_intersections_within_bbox(g: Grid) -> Grid:
    out=clone(g)
    h,w=dims(g)
    frame_cells=[(r,c) for r in range(h) for c in range(w) if g[r][c]==7]
    r0,c0,r1,c1=bbox(frame_cells)
    rows=[r for r in range(1,h) if g[r][0]==2 and r0<r<r1]
    cols=[c for c in range(1,w) if g[0][c]==1 and c0<c<c1]
    for r in rows:
        for c in cols:
            if out[r][c]==0:
                out[r][c]=8
    return out


def solve_hard_05_symmetric_object_mirror(g: Grid) -> Grid:
    out=clone(g)
    h,w=dims(g)
    bar_col=None
    for c in range(w):
        if all(g[r][c]==5 for r in range(h)):
            bar_col=c; break
    assert bar_col is not None
    target=None
    for comp in components_by_color(g,{4}):
        if is_vertically_symmetric(comp['cells']):
            target=comp['cells']; break
    assert target is not None
    for r,c in target:
        mc=2*bar_col-c
        if 0<=mc<w and out[r][mc]==0:
            out[r][mc]=8
    return out


def solve_hard_06_rank_components_by_area_recolor(g: Grid) -> Grid:
    out=clone(g)
    comps=components_by_color(g,{3})
    ordered=sorted(comps, key=lambda comp: len(comp['cells']))
    rank_colors=[2,4,6]
    assert len(ordered)==3
    for rank,comp in enumerate(ordered):
        for r,c in comp['cells']:
            out[r][c]=rank_colors[rank]
    return out


def solve_hard_07_fill_ring_by_repeated_corner_color(g: Grid) -> Grid:
    out=clone(g)
    h,w=dims(g)
    corners=[g[0][0], g[0][w-1], g[h-1][0], g[h-1][w-1]]
    counts=Counter(c for c in corners if c!=0)
    fill_color=max(counts, key=lambda c: counts[c])
    # fill interiors of rectangular rings of color 3
    for comp in components_by_color(g,{3}):
        r0,c0,r1,c1=bbox(comp['cells'])
        good=True
        for cc in range(c0,c1+1):
            if g[r0][cc]!=3 or g[r1][cc]!=3: good=False
        for rr in range(r0,r1+1):
            if g[rr][c0]!=3 or g[rr][c1]!=3: good=False
        if good and r1-r0>=2 and c1-c0>=2:
            for rr in range(r0+1,r1):
                for cc in range(c0+1,c1):
                    if out[rr][cc]==0:
                        out[rr][cc]=fill_color
    return out


SOLVERS: Dict[str, Callable[[Grid], Grid]] = {
    "easy_01_exact_horizontal_triples": solve_easy_01_exact_horizontal_triples,
    "easy_02_frame_2x2_blocks": solve_easy_02_frame_2x2_blocks,
    "easy_03_recolor_L_by_key": solve_easy_03_recolor_L_by_key,
    "easy_04_intersections_from_markers": solve_easy_04_intersections_from_markers,
    "easy_05_complete_rectangle_borders_from_corners": solve_easy_05_complete_rectangle_borders_from_corners,
    "easy_06_mirror_object_across_bar": solve_easy_06_mirror_object_across_bar,
    "easy_07_keep_largest_component_recolor": solve_easy_07_keep_largest_component_recolor,
    "medium_01_connect_matching_endpoints": solve_medium_01_connect_matching_endpoints,
    "medium_02_translate_object_by_vector": solve_medium_02_translate_object_by_vector,
    "medium_03_fill_keyed_rectangle_holes": solve_medium_03_fill_keyed_rectangle_holes,
    "medium_04_mark_bbox_corners": solve_medium_04_mark_bbox_corners,
    "medium_05_stamp_exemplar_at_targets": solve_medium_05_stamp_exemplar_at_targets,
    "medium_06_recolor_border_touching_objects": solve_medium_06_recolor_border_touching_objects,
    "medium_07_raycast_cross_from_centers": solve_medium_07_raycast_cross_from_centers,
    "hard_01_rotate_exemplar_by_target_color": solve_hard_01_rotate_exemplar_by_target_color,
    "hard_02_scale_smallest_object_2x": solve_hard_02_scale_smallest_object_2x,
    "hard_03_dual_key_select_and_recolor": solve_hard_03_dual_key_select_and_recolor,
    "hard_04_row_col_intersections_within_bbox": solve_hard_04_row_col_intersections_within_bbox,
    "hard_05_symmetric_object_mirror": solve_hard_05_symmetric_object_mirror,
    "hard_06_rank_components_by_area_recolor": solve_hard_06_rank_components_by_area_recolor,
    "hard_07_fill_ring_by_repeated_corner_color": solve_hard_07_fill_ring_by_repeated_corner_color,
}


def verify_task_bank(task_bank: List[dict]) -> list[tuple[str, str, int]]:
    failures = []
    for puzzle in task_bank:
        solver = SOLVERS[puzzle["id"]]
        for split in ("train", "test"):
            for i, example in enumerate(puzzle[split]):
                got = solver(example["input"])
                if got != example["output"]:
                    failures.append((puzzle["id"], split, i))
    return failures

if __name__ == "__main__":
    import json
    from pathlib import Path
    path = Path(__file__).with_name("arc_puzzle_bank_21.json")
    task_bank = json.loads(path.read_text())
    failures = verify_task_bank(task_bank)
    if failures:
        print("Verification failures:")
        for item in failures:
            print("  ", item)
    else:
        print(f"All {len(task_bank)} puzzles verified.")
