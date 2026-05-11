"""Reference helper library and 21 reference solve functions for the sixteenth custom ARC puzzle bank.

New primitive introduced in this set:

  span_cells(a, b, include_ends=True)


Return the lattice cells on the horizontal, vertical, or 45° diagonal segment
between two aligned points. This makes connector drawing, midpoint extraction,
rectangle synthesis, band filling, diamond edges, and alignment-based symbolic
outputs explicit.


All solve_* functions are deterministic reference programs for the synthetic
ARC-style tasks in set 16.
"""
from typing import List, Dict, Tuple
from collections import Counter, defaultdict

Grid = List[List[int]]

def blank(h,w,v=0): return [[v]*w for _ in range(h)]

def dims(g): return len(g), len(g[0])

def place(g, cells, color):
    for r,c in cells:
        assert 0 <= r < len(g) and 0 <= c < len(g[0]), (r,c,len(g),len(g[0]))
        g[r][c] = color
    return g

def bbox(cells):
    rs=[r for r,c in cells]; cs=[c for r,c in cells]
    return min(rs), min(cs), max(rs), max(cs)

def crop_cells(cells, color=8):
    r1,c1,r2,c2=bbox(cells)
    out=blank(r2-r1+1,c2-c1+1,0)
    for r,c in cells:
        out[r-r1][c-c1]=color
    return out

def components(grid, include_zero=False):
    h,w=dims(grid)
    seen=[[False]*w for _ in range(h)]
    dirs=[(-1,0),(1,0),(0,-1),(0,1)]
    out=[]
    for r in range(h):
        for c in range(w):
            if seen[r][c]: continue
            seen[r][c]=True
            v=grid[r][c]
            if v==0 and not include_zero: continue
            st=[(r,c)]; cells=[(r,c)]
            while st:
                rr,cc=st.pop()
                for dr,dc in dirs:
                    nr,nc=rr+dr,cc+dc
                    if 0<=nr<h and 0<=nc<w and not seen[nr][nc] and grid[nr][nc]==v:
                        seen[nr][nc]=True; st.append((nr,nc)); cells.append((nr,nc))
            out.append({"color":v,"cells":cells})
    return out

def span_cells(a,b, include_ends=True):
    (r1,c1),(r2,c2)=a,b
    dr = (r2>r1) - (r2<r1)
    dc = (c2>c1) - (c2<c1)
    if not (r1==r2 or c1==c2 or abs(r2-r1)==abs(c2-c1)):
        raise ValueError(f"unaligned {a} {b}")
    n=max(abs(r2-r1), abs(c2-c1))
    cells=[(r1+i*dr,c1+i*dc) for i in range(n+1)]
    return cells if include_ends else cells[1:-1]

def nonzero_cells(grid):
    return [(r,c,grid[r][c]) for r,row in enumerate(grid) for c,v in enumerate(row) if v!=0]

def points_by_color(grid):
    d=defaultdict(list)
    for r,c,v in nonzero_cells(grid):
        d[v].append((r,c))
    return dict(d)

def pair_orientation(a,b):
    if a[0]==b[0]: return 'h'
    if a[1]==b[1]: return 'v'
    return 'd'

def split_panels_by_separator(grid, sep=9):
    h,w=dims(grid)
    sep_cols=[c for c in range(w) if all(grid[r][c]==sep for r in range(h))]
    bounds=[]
    start=0
    for c in sep_cols:
        bounds.append((start,c))
        start=c+1
    bounds.append((start,w))
    panels=[]
    for a,b in bounds:
        if a<b:
            sub=[row[a:b] for row in grid]
            panels.append((a,b,sub))
    return panels

def span_signature(cells):
    assert len(cells)==2
    seg=span_cells(cells[0],cells[1])
    return pair_orientation(cells[0],cells[1]), len(seg), seg

def solve_E1(grid):
    pts=[(r,c) for r,row in enumerate(grid) for c,v in enumerate(row) if v!=0]
    assert len(pts)==2
    out=blank(*dims(grid),0)
    place(out, span_cells(pts[0], pts[1]), 8)
    return out

def solve_E2(grid):
    pts=[(r,c) for r,row in enumerate(grid) for c,v in enumerate(row) if v!=0]
    out=blank(*dims(grid),0)
    place(out, span_cells(pts[0], pts[1], include_ends=False), 8)
    return out

def solve_E3(grid):
    pts=[(r,c) for r,row in enumerate(grid) for c,v in enumerate(row) if v!=0]
    seg=span_cells(pts[0], pts[1])
    assert len(seg)%2==1
    out=blank(*dims(grid),0)
    place(out,[seg[len(seg)//2]],8)
    return out

def solve_E4(grid):
    pts=[(r,c) for r,row in enumerate(grid) for c,v in enumerate(row) if v!=0]
    r1,c1,r2,c2=bbox(pts)
    corners=[(r1,c1),(r1,c2),(r2,c1),(r2,c2)]
    out=blank(*dims(grid),0)
    # top bottom left right
    place(out, span_cells((r1,c1),(r1,c2)),8)
    place(out, span_cells((r2,c1),(r2,c2)),8)
    place(out, span_cells((r1,c1),(r2,c1)),8)
    place(out, span_cells((r1,c2),(r2,c2)),8)
    return out

def solve_E5(grid):
    pts=points_by_color(grid)
    assert set(pts)=={2,3}
    seg1=set(span_cells(*pts[2]))
    seg2=set(span_cells(*pts[3]))
    inter=list(seg1 & seg2)
    assert len(inter)==1
    out=blank(*dims(grid),0)
    place(out, inter, 8)
    return out

def solve_E6(grid):
    pts=points_by_color(grid)
    best=None
    for color,cells in pts.items():
        if len(cells)!=2: continue
        seg=span_cells(cells[0],cells[1])
        key=(len(seg),)
        if best is None or key>best[0]:
            best=(key, seg)
    out=blank(*dims(grid),0)
    place(out,best[1],8)
    return out

def solve_E7(grid):
    pts=[(r,c) for r,row in enumerate(grid) for c,v in enumerate(row) if v!=0]
    L=len(span_cells(pts[0],pts[1]))
    out=blank(1,L,0)
    place(out,[(0,c) for c in range(L)],8)
    return out

def solve_M1(grid):
    h,w=dims(grid)
    legend=grid[0][0]
    mapping={5:2,6:3,7:4}
    assert legend in mapping
    target=mapping[legend]
    pts=defaultdict(list)
    for r,row in enumerate(grid):
        for c,v in enumerate(row):
            if (r,c)==(0,0): 
                continue
            if v!=0:
                pts[v].append((r,c))
    seg=span_cells(pts[target][0], pts[target][1])
    out=blank(h,w,0)
    place(out,seg,8)
    return out

def solve_M2(grid):
    pts=points_by_color(grid)
    out=blank(*dims(grid),0)
    for color in pts:
        if len(pts[color])==2:
            place(out, span_cells(*pts[color]), 8)
    return out

def solve_M3(grid):
    pts=[(r,c) for r,row in enumerate(grid) for c,v in enumerate(row) if v!=0]
    assert len(pts)==2
    (r1,c1),(r2,c2)=pts
    rr1,rr2=sorted((r1,r2)); cc1,cc2=sorted((c1,c2))
    out=blank(rr2-rr1+1, cc2-cc1+1, 8)
    return out

def solve_M4(grid):
    pts=points_by_color(grid)
    out=blank(*dims(grid),0)
    for color,cells in pts.items():
        if len(cells)==2:
            place(out, span_cells(cells[0],cells[1]), color)
    return out

def solve_M5(grid):
    pts=points_by_color(grid)
    line=set(span_cells(pts[1][0], pts[1][1]))
    comps=[comp for comp in components(grid) if comp["color"] not in {0,1}]
    hits=[comp for comp in comps if set(comp["cells"]) & line]
    assert len(hits)==1, len(hits)
    return crop_cells(hits[0]["cells"], 8)

def solve_M6(grid):
    pts=points_by_color(grid)
    # colors 2 and 3 each form a pair, same orientation
    pairs=[pts[c] for c in sorted(pts) if len(pts[c])==2]
    assert len(pairs)==2
    (a1,a2),(b1,b2)=pairs
    o1=pair_orientation(a1,a2); o2=pair_orientation(b1,b2); assert o1==o2 and o1 in ('h','v')
    if o1=='h':
        r_top=min(a1[0],a2[0]); r_bot=min(b1[0],b2[0])
        if r_top>r_bot:
            (a1,a2),(b1,b2)=(b1,b2),(a1,a2); r_top,r_bot=r_bot,r_top
        c1=sorted([a1[1],a2[1]])[0]; c2=sorted([a1[1],a2[1]])[1]
        assert sorted([b1[1],b2[1]])==[c1,c2]
        out=blank(*dims(grid),0)
        place(out, [(r,c) for r in range(r_top, r_bot+1) for c in range(c1,c2+1)], 8)
        return out
    else:
        c_left=min(a1[1],a2[1]); c_right=min(b1[1],b2[1])
        if c_left>c_right:
            (a1,a2),(b1,b2)=(b1,b2),(a1,a2); c_left,c_right=c_right,c_left
        r1=sorted([a1[0],a2[0]])[0]; r2=sorted([a1[0],a2[0]])[1]
        assert sorted([b1[0],b2[0]])==[r1,r2]
        out=blank(*dims(grid),0)
        place(out, [(r,c) for r in range(r1,r2+1) for c in range(c_left,c_right+1)], 8)
        return out

def solve_M7(grid):
    pts=points_by_color(grid)
    shared=pts[1][0]
    other_h=pts[2][0]
    other_v=pts[3][0]
    r1,r2=sorted([shared[0], other_v[0]])
    c1,c2=sorted([shared[1], other_h[1]])
    out=blank(*dims(grid),0)
    place(out, span_cells((r1,c1),(r1,c2)), 8)
    place(out, span_cells((r2,c1),(r2,c2)), 8)
    place(out, span_cells((r1,c1),(r2,c1)), 8)
    place(out, span_cells((r1,c2),(r2,c2)), 8)
    return out

def solve_H1(grid):
    pts=points_by_color(grid)
    labels=sorted(pts)
    n=len(labels)
    out=blank(n,n,0)
    for i,a in enumerate(labels):
        for j,b in enumerate(labels):
            p=pts[a][0]; q=pts[b][0]
            if i==j or p[0]==q[0] or p[1]==q[1] or abs(p[0]-q[0])==abs(p[1]-q[1]):
                out[i][j]=8
    return out

def solve_H2(grid):
    pts=points_by_color(grid)
    sigs=[]
    for color,cells in sorted(pts.items()):
        if len(cells)==2:
            ori,L,seg=span_signature(cells)
            sigs.append((color,ori,L,seg))
    # unique orientation-length signature
    counts=Counter((ori,L) for _,ori,L,_ in sigs)
    odd=[x for x in sigs if counts[(x[1],x[2])]==1]
    assert len(odd)==1
    seg=odd[0][3]
    return crop_cells(seg,8)

def solve_H3(grid):
    pts=[(r,c) for r,row in enumerate(grid) for c,v in enumerate(row) if v!=0]
    assert len(pts)==4
    rs=sorted(r for r,c in pts); cs=sorted(c for r,c in pts)
    # north south west east by min/max
    north=min(pts,key=lambda p:(p[0],p[1]))
    south=max(pts,key=lambda p:(p[0],p[1]))
    west=min(pts,key=lambda p:(p[1],p[0]))
    east=max(pts,key=lambda p:(p[1],p[0]))
    cr=(north[0]+south[0])//2
    cc=(west[1]+east[1])//2
    rad=abs(north[0]-cr)+abs(north[1]-cc)
    h,w=dims(grid)
    out=blank(h,w,0)
    cells=[(r,c) for r in range(h) for c in range(w) if abs(r-cr)+abs(c-cc)<=rad]
    place(out,cells,8)
    return out

def solve_H4(grid):
    h,w=dims(grid)
    out=blank(h,w,0)
    for r in range(h):
        cols=[c for c,v in enumerate(grid[r]) if v!=0]
        if len(cols)==2:
            place(out, [(r,c) for c in range(cols[0], cols[1]+1)], 8)
    return out

def solve_H5(grid):
    panels=split_panels_by_separator(grid,9)
    infos=[]
    for a,b,sub in panels:
        pts=[(r,c,v) for r,row in enumerate(sub) for c,v in enumerate(row) if v and v!=9]
        assert len(pts)==2
        p1=(pts[0][0],pts[0][1]); p2=(pts[1][0],pts[1][1])
        ori=pair_orientation(p1,p2); L=len(span_cells(p1,p2))
        infos.append((ori,L,p1,p2))
    cnt=Counter(ori for ori,_,_,_ in infos)
    majority=max(cnt.items(), key=lambda kv: kv[1])[0]
    candidates=[x for x in infos if x[0]==majority]
    # if two same orientation but different lengths, choose longer
    ori,L,p1,p2=max(candidates, key=lambda x:x[1])
    seg=span_cells(p1,p2)
    return crop_cells(seg,8)

def solve_H6(grid):
    pts=points_by_color(grid)
    pairs=[pts[c] for c in sorted(pts) if c in (1,2)]  # boundary marker pairs colors 1 and 2
    (a1,a2),(b1,b2)=pairs
    ori=pair_orientation(a1,a2); assert ori==pair_orientation(b1,b2) and ori in ('h','v')
    comps=[comp for comp in components(grid) if comp["color"] not in {0,1,2}]
    inside=[]
    if ori=='h':
        r1=min(a1[0],a2[0]); r2=min(b1[0],b2[0])
        if r1>r2: r1,r2=r2,r1
        c1,c2=sorted([a1[1],a2[1]])
        for comp in comps:
            ok=all(r1<=r<=r2 and c1<=c<=c2 for r,c in comp["cells"])
            if ok:
                inside.append(comp)
    else:
        c1=min(a1[1],a2[1]); c2=min(b1[1],b2[1])
        if c1>c2: c1,c2=c2,c1
        r1,r2=sorted([a1[0],a2[0]])
        for comp in comps:
            ok=all(r1<=r<=r2 and c1<=c<=c2 for r,c in comp["cells"])
            if ok:
                inside.append(comp)
    assert len(inside)==1, len(inside)
    return crop_cells(inside[0]["cells"],8)

def solve_H7(grid):
    pts=points_by_color(grid)
    lengths=[]
    for color,cells in sorted(pts.items()):
        if len(cells)==2:
            lengths.append(len(span_cells(cells[0],cells[1])))
    lengths=sorted(lengths)
    out=blank(len(lengths), max(lengths), 0)
    for r,L in enumerate(lengths):
        for c in range(L):
            out[r][c]=8
    return out

def connect_single_pair(grid):
    return solve_E1(grid)

def segment_interior_only(grid):
    return solve_E2(grid)

def segment_midpoint(grid):
    return solve_E3(grid)

def rectangle_border_from_corners(grid):
    return solve_E4(grid)

def span_intersection_only(grid):
    return solve_E5(grid)

def longest_pair_wins(grid):
    return solve_E6(grid)

def length_bar_from_pair(grid):
    return solve_E7(grid)

def legend_chooses_orientation(grid):
    return solve_M1(grid)

def full_cross_from_pairs(grid):
    return solve_M2(grid)

def filled_rectangle_from_opposite_corners(grid):
    return solve_M3(grid)

def draw_every_pair_in_own_color(grid):
    return solve_M4(grid)

def crop_object_hit_by_connector(grid):
    return solve_M5(grid)

def fill_band_between_parallel_pairs(grid):
    return solve_M6(grid)

def complete_rectangle_from_adjacent_sides(grid):
    return solve_M7(grid)

def alignment_matrix_of_marked_points(grid):
    return solve_H1(grid)

def odd_pair_crop_by_signature(grid):
    return solve_H2(grid)

def fill_diamond_from_cardinal_markers(grid):
    return solve_H3(grid)

def row_endpoint_silhouette_fill(grid):
    return solve_H4(grid)

def majority_orientation_panels(grid):
    return solve_H5(grid)

def crop_object_between_parallel_spans(grid):
    return solve_H6(grid)

def length_ranking_bars(grid):
    return solve_H7(grid)

def solve_S16_E1(grid):
    return connect_single_pair(grid)

def solve_S16_E2(grid):
    return segment_interior_only(grid)

def solve_S16_E3(grid):
    return segment_midpoint(grid)

def solve_S16_E4(grid):
    return rectangle_border_from_corners(grid)

def solve_S16_E5(grid):
    return span_intersection_only(grid)

def solve_S16_E6(grid):
    return longest_pair_wins(grid)

def solve_S16_E7(grid):
    return length_bar_from_pair(grid)

def solve_S16_M1(grid):
    return legend_chooses_orientation(grid)

def solve_S16_M2(grid):
    return full_cross_from_pairs(grid)

def solve_S16_M3(grid):
    return filled_rectangle_from_opposite_corners(grid)

def solve_S16_M4(grid):
    return draw_every_pair_in_own_color(grid)

def solve_S16_M5(grid):
    return crop_object_hit_by_connector(grid)

def solve_S16_M6(grid):
    return fill_band_between_parallel_pairs(grid)

def solve_S16_M7(grid):
    return complete_rectangle_from_adjacent_sides(grid)

def solve_S16_H1(grid):
    return alignment_matrix_of_marked_points(grid)

def solve_S16_H2(grid):
    return odd_pair_crop_by_signature(grid)

def solve_S16_H3(grid):
    return fill_diamond_from_cardinal_markers(grid)

def solve_S16_H4(grid):
    return row_endpoint_silhouette_fill(grid)

def solve_S16_H5(grid):
    return majority_orientation_panels(grid)

def solve_S16_H6(grid):
    return crop_object_between_parallel_spans(grid)

def solve_S16_H7(grid):
    return length_ranking_bars(grid)
