"""Reference solvers for the eighth 21-task ARC-style puzzle bank.

This batch leans into:
- contours and boundary extraction
- Voronoi-style partitioning with and without walls
- row signatures and reconstruction from compact clues
- rigid pivot motion and dihedral shape matching
- Boolean shape algebra and gallery composition
"""
from typing import List
from collections import defaultdict, deque

Grid = List[List[int]]

DIR4 = [(-1,0),(1,0),(0,-1),(0,1)]
DIR8 = [(-1,0),(1,0),(0,-1),(0,1),(-1,-1),(-1,1),(1,-1),(1,1)]

NEW_PRIMITIVES = {
    "object_contour": "Return the boundary cells of an object under 4-neighbor connectivity.",
    "voronoi_fill": "Assign each cell to its nearest marker under Manhattan distance.",
    "row_signature": "Read off the per-row nonzero counts of a cropped shape.",
    "rigid_orbit": "Move an object around a pivot by rotating all of its cells as a rigid set.",
    "geodesic_voronoi": "Partition reachable space by shortest orthogonal path distance with walls.",
    "match_under_dihedral": "Compare shapes up to rotation and reflection.",
    "shape_boolean": "Compute union, intersection, xor, or subtraction after normalization.",
    "ferrers_from_signatures": "Reconstruct a left-justified Young/Ferrers diagram from row and column counts.",
    "pack_gallery": "Pack several cropped result shapes into a new gallery with black gaps.",
    "hole_mask": "Return only the enclosed hole cells of hollow frame-like objects.",
    "slide_until_contact": "Translate an object repeatedly until a blocker, border, or another object stops it."
}

def blank(h,w,val=0):
    return [[val]*w for _ in range(h)]

def copy_grid(g): return [row[:] for row in g]

def dims(g): return len(g), len(g[0])

def inb(g,r,c):
    h,w=dims(g); return 0<=r<h and 0<=c<w

def bbox(cells):
    rs=[r for r,c in cells]; cs=[c for r,c in cells]
    return min(rs), min(cs), max(rs), max(cs)

def crop_cells(g, cells=None):
    if cells is None:
        cells=[(r,c) for r,row in enumerate(g) for c,v in enumerate(row) if v!=0]
    if not cells:
        return [[0]]
    r0,c0,r1,c1=bbox(cells)
    return [row[c0:c1+1] for row in g[r0:r1+1]]

def crop_nonzero(g): return crop_cells(g)

def paste(out, shape, top, left, transparent=True):
    h,w=dims(out); sh,sw=dims(shape)
    for r in range(sh):
        for c in range(sw):
            v=shape[r][c]
            if transparent and v==0: 
                continue
            rr,cc=top+r,left+c
            if 0<=rr<h and 0<=cc<w:
                out[rr][cc]=v
    return out

def cells_of(g, color=None, exclude=None):
    ex=set(exclude or [])
    return [(r,c) for r,row in enumerate(g) for c,v in enumerate(row) if v!=0 and v not in ex and (color is None or v==color)]

def components(g, exclude=None, colors_separate=True):
    ex=set(exclude or [])
    h,w=dims(g)
    seen=set()
    comps=[]
    for r in range(h):
        for c in range(w):
            v=g[r][c]
            if v==0 or v in ex or (r,c) in seen: 
                continue
            stack=[(r,c)]
            seen.add((r,c))
            comp=[]
            while stack:
                cr,cc=stack.pop()
                comp.append((cr,cc))
                for dr,dc in DIR4:
                    nr,nc=cr+dr,cc+dc
                    if inb(g,nr,nc) and (nr,nc) not in seen and g[nr][nc]!=0 and g[nr][nc] not in ex and ((not colors_separate) or g[nr][nc]==v):
                        seen.add((nr,nc)); stack.append((nr,nc))
            comps.append({'color':v,'cells':set(comp)})
    return comps

def object_shape(comp):
    cells=comp['cells']
    r0,c0,r1,c1=bbox(cells)
    out=blank(r1-r0+1,c1-c0+1)
    for r,c in cells: out[r-r0][c-c0]=comp['color']
    return out,(r0,c0,r1,c1)

def rotate_cw(g):
    h,w=dims(g)
    return [[g[h-1-r][c] for r in range(h)] for c in range(w)]

def rotate180(g): return rotate_cw(rotate_cw(g))

def rotate_ccw(g): return rotate_cw(rotate180(g))

def flip_h(g): return [list(reversed(row)) for row in g]

def flip_v(g): return list(reversed([row[:] for row in g]))

def transpose(g):
    h,w=dims(g)
    return [[g[r][c] for r in range(h)] for c in range(w)]

def normalize_binary(shape):
    cells=[(r,c) for r,row in enumerate(shape) for c,v in enumerate(row) if v!=0]
    if not cells: return ((0,),)
    r0,c0,r1,c1=bbox(cells)
    return tuple(tuple(1 if shape[r][c]!=0 else 0 for c in range(c0,c1+1)) for r in range(r0,r1+1))

def all_dihedral(shape):
    variants=[]
    x=shape
    for _ in range(4):
        variants.append(x)
        variants.append(flip_h(x))
        x=rotate_cw(x)
    # unique by binary
    uniq=[]
    seen=set()
    for v in variants:
        b=normalize_binary(v)
        if b not in seen:
            seen.add(b); uniq.append(v)
    return uniq

def object_contour_cells(comp):
    cells=comp['cells']
    contour=set()
    for r,c in cells:
        for dr,dc in DIR4:
            nr,nc=r+dr,c+dc
            if (nr,nc) not in cells:
                contour.add((r,c)); break
    return contour

def object_contour_shape(comp):
    contour=object_contour_cells(comp)
    color=comp['color']
    r0,c0,r1,c1=bbox(comp['cells'])
    out=blank(r1-r0+1,c1-c0+1)
    for r,c in contour:
        out[r-r0][c-c0]=color
    return out

def row_signature(shape):
    shape=crop_nonzero(shape)
    return [sum(1 for v in row if v!=0) for row in shape]

def normalize_pair(A,B):
    A=crop_nonzero(A); B=crop_nonzero(B)
    h=max(len(A), len(B)); w=max(len(A[0]), len(B[0]))
    outA=blank(h,w); outB=blank(h,w)
    paste(outA, A, 0,0); paste(outB, B, 0,0)
    return outA,outB

def recolor_shape(shape, color):
    return [[color if v!=0 else 0 for v in row] for row in shape]

def shape_boolean(A,B,op='union', color=8):
    A,B=normalize_pair(A,B)
    h,w=dims(A)
    out=blank(h,w)
    for r in range(h):
        for c in range(w):
            a=A[r][c]!=0; b=B[r][c]!=0
            keep=False
            if op=='union': keep=a or b
            elif op=='intersection': keep=a and b
            elif op=='xor': keep=(a!=b)
            elif op=='a_minus_b': keep=a and not b
            elif op=='b_minus_a': keep=b and not a
            if keep: out[r][c]=color
    return crop_nonzero(out)

def rigid_rotate_positions(cells, pivot, quarter_turns):
    # quarter_turns clockwise
    out=[]
    pr,pc=pivot
    for r,c in cells:
        y,x=r-pr,c-pc
        k=quarter_turns%4
        if k==0: ny,nx=y,x
        elif k==1: ny,nx=x,-y
        elif k==2: ny,nx=-y,-x
        else: ny,nx=-x,y
        out.append((pr+ny, pc+nx))
    return out

def geodesic_voronoi(g):
    h,w=dims(g)
    walls=set(cells_of(g,color=5))
    markers=[(r,c,g[r][c]) for r in range(h) for c in range(w) if g[r][c] not in (0,5)]
    out=copy_grid(g)
    # multi-source BFS with stable order by marker reading order
    q=deque()
    owner={}
    dist={}
    for idx,(r,c,color) in enumerate(markers):
        q.append((r,c,idx,color))
        owner[(r,c)]=idx
        dist[(r,c)]=0
    while q:
        r,c,idx,color=q.popleft()
        for dr,dc in DIR4:
            nr,nc=r+dr,c+dc
            if not (0<=nr<h and 0<=nc<w): 
                continue
            if (nr,nc) in walls: 
                continue
            nd=dist[(r,c)] + 1
            if (nr,nc) not in dist:
                dist[(nr,nc)]=nd
                owner[(nr,nc)]=idx
                q.append((nr,nc,idx,color))
            else:
                # if same distance and earlier marker wins, keep existing since bfs seeded in order
                continue
    for (r,c),idx in owner.items():
        if (r,c) not in walls:
            out[r][c]=markers[idx][2]
    return out

def pack_gallery(shapes, gap=1):
    shapes=[crop_nonzero(s) for s in shapes]
    H=max(len(s) for s in shapes)
    W=sum(len(s[0]) for s in shapes)+gap*(len(shapes)-1)
    out=blank(H,W)
    cur=0
    for s in shapes:
        paste(out, s, 0, cur)
        cur += len(s[0])+gap
    return out

def solve_h_h01_run_midpoints(g):
    h,w=dims(g); out=blank(h,w)
    for r in range(h):
        c=0
        while c<w:
            if g[r][c]==0:
                c+=1; continue
            color=g[r][c]; start=c
            while c<w and g[r][c]==color:
                c+=1
            end=c-1; L=end-start+1
            if L%2==1 and L>=3:
                out[r][start+L//2]=color
    return out

def solve_h_h02_singleton_to_hollow_ring(g):
    h,w=dims(g); out=blank(h,w)
    for r in range(h):
        for c in range(w):
            color=g[r][c]
            if color!=0:
                for dr,dc in DIR8:
                    nr,nc=r+dr,c+dc
                    if 0<=nr<h and 0<=nc<w:
                        out[nr][nc]=color
                # center stays 0
    return out

def solve_h_h03_top_seeds_diagonals(g):
    h,w=dims(g); out=blank(h,w)
    for c,color in enumerate(g[0]):
        if color!=0:
            r=0; cc=c
            while r<h and cc<w:
                out[r][cc]=color
                r+=1; cc+=1
    return out

def solve_h_h04_keep_colors_in_one_row(g):
    rows_by_color=defaultdict(set)
    h,w=dims(g)
    for r in range(h):
        for c,v in enumerate(g[r]):
            if v!=0: rows_by_color[v].add(r)
    keep={color for color,rows in rows_by_color.items() if len(rows)==1}
    return [[v if v in keep else 0 for v in row] for row in g]

def solve_h_h05_blocks_to_antidiagonals(g):
    h,w=dims(g); out=blank(h,w)
    for r in range(h-1):
        for c in range(w-1):
            color=g[r][c]
            if color!=0 and g[r][c+1]==color and g[r+1][c]==color and g[r+1][c+1]==color:
                out[r][c+1]=color
                out[r+1][c]=color
    return out

def solve_h_h06_add_gray_shadow(g):
    h,w=dims(g); out=copy_grid(g)
    for r in range(h):
        for c in range(w):
            if g[r][c]!=0:
                nr,nc=r+1,c+1
                if nr<h and nc<w and out[nr][nc]==0:
                    out[nr][nc]=5
    return out

def solve_h_h07_rectangles_to_contours(g):
    comps=components(g)
    out=blank(*dims(g))
    for comp in comps:
        color=comp['color']; cells=comp['cells']
        r0,c0,r1,c1=bbox(cells)
        # contour of bbox
        for r in range(r0,r1+1):
            for c in range(c0,c1+1):
                if r in (r0,r1) or c in (c0,c1):
                    out[r][c]=color
    return out

def solve_h_h08_extract_contour_largest(g):
    comps=components(g)
    # largest by cell count, tie top-left
    comp=max(comps, key=lambda comp:(len(comp['cells']), -bbox(comp['cells'])[0], -bbox(comp['cells'])[1]))
    return object_contour_shape(comp)

def solve_h_h09_corner_voronoi(g):
    h,w=dims(g)
    corners=[((0,0),g[0][0]), ((0,w-1),g[0][w-1]), ((h-1,0),g[h-1][0]), ((h-1,w-1),g[h-1][w-1])]
    order=[(0,0),(0,w-1),(h-1,0),(h-1,w-1)]
    out=blank(h,w)
    for r in range(h):
        for c in range(w):
            # choose nearest corner marker by manhattan; ties by order above
            dists=[(abs(r-cr)+abs(c-cc), idx, color) for idx,((cr,cc),color) in enumerate(corners)]
            _,_,color=min(dists)
            out[r][c]=color
    return out

def solve_h_h10_recolor_by_contour_rank(g):
    comps=components(g)
    # contour lengths distinct
    sorted_comps=sorted(comps, key=lambda comp:(len(object_contour_cells(comp)), bbox(comp['cells'])[0], bbox(comp['cells'])[1]))
    rank_colors=[2,3,4,6,7,8,9]
    out=blank(*dims(g))
    for i,comp in enumerate(sorted_comps):
        newc=rank_colors[i]
        for r,c in comp['cells']:
            out[r][c]=newc
    return out

def solve_h_h11_reflect_across_guide(g):
    h,w=dims(g)
    guide_color=8
    guide_cells=cells_of(g, color=guide_color)
    # detect line
    rows=sorted({r for r,c in guide_cells})
    cols=sorted({c for r,c in guide_cells})
    out=blank(h,w)
    if len(rows)==1:  # horizontal line
        gr=rows[0]
        for r in range(h):
            for c in range(w):
                v=g[r][c]
                if v!=0 and v!=guide_color:
                    rr=2*gr - r
                    if 0<=rr<h: out[rr][c]=v
    else: # vertical
        gc=cols[0]
        for r in range(h):
            for c in range(w):
                v=g[r][c]
                if v!=0 and v!=guide_color:
                    cc=2*gc - c
                    if 0<=cc<w: out[r][cc]=v
    return out

def solve_h_h12_slide_objects_left_to_blockers(g):
    h,w=dims(g)
    blockers=set(cells_of(g, color=5))
    comps=components(g, exclude={5})
    out=blank(h,w)
    for r,c in blockers: out[r][c]=5
    # move each component left as far as possible ignoring others since examples separated; to be safe account for already placed
    for comp in sorted(comps, key=lambda comp:min(c for r,c in comp['cells'])):
        cells=comp['cells']
        shift=0
        while True:
            ok=True
            for r,c in cells:
                nc=c-(shift+1)
                if nc<0 or (r,nc) in blockers or out[r][nc]!=0:
                    ok=False; break
            if ok: shift+=1
            else: break
        for r,c in cells:
            out[r][c-shift]=comp['color']
    return out

def solve_h_h13_row_signature_histogram_largest(g):
    comps=components(g)
    comp=max(comps, key=lambda comp:(len(comp['cells']), -bbox(comp['cells'])[0], -bbox(comp['cells'])[1]))
    shape,_=object_shape(comp)
    sig=row_signature(shape)
    color=comp['color']
    W=max(sig) if sig else 1
    out=blank(len(sig), W)
    for r,count in enumerate(sig):
        for c in range(count):
            out[r][c]=color
    return out

def solve_h_h14_keep_only_frame_holes(g):
    # For each rectangular frame (one-cell-thick), output only interior cells filled with frame color.
    comps=components(g)
    out=blank(*dims(g))
    for comp in comps:
        color=comp['color']; cells=comp['cells']
        r0,c0,r1,c1=bbox(cells)
        # assume rectangular frame
        for r in range(r0+1, r1):
            for c in range(c0+1, c1):
                if (r,c) not in cells:
                    out[r][c]=color
    return out

def solve_h_h15_boolean_op_by_legend(g):
    h,w=dims(g)
    key=g[0][0]
    temp=copy_grid(g); temp[0][0]=0
    comps=components(temp)
    comps=sorted(comps, key=lambda comp:(bbox(comp['cells'])[1], bbox(comp['cells'])[0]))
    A,_=object_shape(comps[0]); B,_=object_shape(comps[1])
    op_map={1:'union',2:'intersection',3:'xor',4:'a_minus_b'}
    return shape_boolean(A,B, op_map[key], color=8)

def solve_h_h16_orbit_object_about_pivot(g):
    h,w=dims(g)
    # pivot is 9, token at top-left-ish colors 1..4 map to 0,1,2,3 quarter turns clockwise
    pivot=cells_of(g,color=9)[0]
    tokens=[(r,c,g[r][c]) for r in range(h) for c in range(w) if g[r][c] in (1,2,3,4)]
    tr,tc,key=tokens[0]
    k={1:0,2:1,3:2,4:3}[key]
    temp=copy_grid(g); temp[tr][tc]=0; temp[pivot[0]][pivot[1]]=0
    comp=components(temp)[0]
    out=blank(h,w)
    for r,c in rigid_rotate_positions(comp['cells'], pivot, k):
        if 0<=r<h and 0<=c<w: out[r][c]=comp['color']
    out[pivot[0]][pivot[1]]=9
    return out

def solve_h_h17_geodesic_voronoi_walls(g):
    return geodesic_voronoi(g)

def solve_h_h18_match_slots_under_dihedral(g):
    # source objects are colored not 8; slots are 8 silhouettes. Output slots recolored to matching source colors, sources erased.
    h,w=dims(g)
    source_comps=components(g, exclude={8})
    slot_comps=components([[0 if v!=8 else 8 for v in row] for row in g], colors_separate=False)
    out=blank(h,w)
    # for each slot, find matching source under dihedral based on binary crop
    used=set()
    for slot in slot_comps:
        slot_shape,_=object_shape({'color':8,'cells':slot['cells']})
        slot_bin=normalize_binary(slot_shape)
        match_idx=None
        for i,src in enumerate(source_comps):
            if i in used: 
                continue
            src_shape,_=object_shape(src)
            ok=False
            for v in all_dihedral(src_shape):
                if normalize_binary(v)==slot_bin:
                    ok=True
                    break
            if ok:
                match_idx=i; used.add(i); break
        if match_idx is None:
            continue
        src=source_comps[match_idx]
        color=src['color']
        # paint slot cells with source color
        for r,c in slot['cells']:
            out[r][c]=color
    return out

def solve_h_h19_best_dihedral_overlap(g):
    comps=components(g)
    comps=sorted(comps, key=lambda comp:(bbox(comp['cells'])[1], bbox(comp['cells'])[0]))
    A,_=object_shape(comps[0]); B,_=object_shape(comps[1])
    best=None; best_overlap=-1
    A_norm=crop_nonzero(A)
    for v in all_dihedral(B):
        X,Y=normalize_pair(A_norm, v)
        overlap=sum(1 for r in range(len(X)) for c in range(len(X[0])) if X[r][c]!=0 and Y[r][c]!=0)
        score=(overlap, -len(X), -len(X[0]))  # overlap max, then smaller canvas? maybe fixed
        if overlap>best_overlap:
            best_overlap=overlap; best=(X,Y)
    X,Y=best
    h,w=dims(X)
    out=blank(h,w)
    for r in range(h):
        for c in range(w):
            if X[r][c]!=0 and Y[r][c]!=0:
                out[r][c]=8
    return crop_nonzero(out)

def solve_h_h20_boolean_gallery(g):
    comps=components(g)
    comps=sorted(comps, key=lambda comp:(bbox(comp['cells'])[1], bbox(comp['cells'])[0]))
    A,_=object_shape(comps[0]); B,_=object_shape(comps[1])
    ops=[('union',2),('intersection',3),('xor',4),('a_minus_b',6)]
    row1=[shape_boolean(A,B,ops[0][0],ops[0][1]), shape_boolean(A,B,ops[1][0],ops[1][1])]
    row2=[shape_boolean(A,B,ops[2][0],ops[2][1]), shape_boolean(A,B,ops[3][0],ops[3][1])]
    top=pack_gallery(row1, gap=1)
    bot=pack_gallery(row2, gap=1)
    W=max(len(top[0]), len(bot[0]))
    if len(top[0])<W:
        t=blank(len(top),W); paste(t, top, 0, 0); top=t
    if len(bot[0])<W:
        b=blank(len(bot),W); paste(b, bot, 0, 0); bot=b
    return top + [ [0]*W ] + bot

def solve_h_h21_reconstruct_ferrers_from_signatures(g):
    row_lengths=[g[r][0] for r in range(1,len(g))]
    col_heights=g[0][1:]
    H=len(row_lengths); W=len(col_heights)
    out=blank(H,W)
    for r in range(H):
        for c in range(W):
            if c < row_lengths[r] and r < col_heights[c]:
                out[r][c]=8
    return out

TASK_FUNCTIONS = {
    "easy_h01": solve_h_h01_run_midpoints,
    "easy_h02": solve_h_h02_singleton_to_hollow_ring,
    "easy_h03": solve_h_h03_top_seeds_diagonals,
    "easy_h04": solve_h_h04_keep_colors_in_one_row,
    "easy_h05": solve_h_h05_blocks_to_antidiagonals,
    "easy_h06": solve_h_h06_add_gray_shadow,
    "easy_h07": solve_h_h07_rectangles_to_contours,
    "medium_h08": solve_h_h08_extract_contour_largest,
    "medium_h09": solve_h_h09_corner_voronoi,
    "medium_h10": solve_h_h10_recolor_by_contour_rank,
    "medium_h11": solve_h_h11_reflect_across_guide,
    "medium_h12": solve_h_h12_slide_objects_left_to_blockers,
    "medium_h13": solve_h_h13_row_signature_histogram_largest,
    "medium_h14": solve_h_h14_keep_only_frame_holes,
    "hard_h15": solve_h_h15_boolean_op_by_legend,
    "hard_h16": solve_h_h16_orbit_object_about_pivot,
    "hard_h17": solve_h_h17_geodesic_voronoi_walls,
    "hard_h18": solve_h_h18_match_slots_under_dihedral,
    "hard_h19": solve_h_h19_best_dihedral_overlap,
    "hard_h20": solve_h_h20_boolean_gallery,
    "hard_h21": solve_h_h21_reconstruct_ferrers_from_signatures,
}

def validate_examples(task_bank):
    for task in task_bank:
        fn = TASK_FUNCTIONS[task["id"]]
        for pair in task["train"] + task["test"]:
            expected = pair["output"]
            got = fn(pair["input"])
            if got != expected:
                raise AssertionError(f"{task['id']} failed validation")
    return True
