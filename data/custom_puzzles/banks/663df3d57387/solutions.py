"""Reference helper library and 21 reference solve functions for the twentieth custom ARC puzzle bank.

New primitive introduced in this set:

  find_template_matches(board, template, wildcard=0, transforms=('id',))

Slide a template-sized window across a board and return every location where the
template matches. The default mode demands literal equality, but the same
framework can be widened to quarter-turn rotations, reflections, or richer
near-match checks such as one-hole or two-hole completion.

All solve_* functions are deterministic reference programs for the synthetic
ARC-style tasks in set 20.
"""
from typing import List, Tuple

Grid = List[List[int]]

def blank(h,w,v=0):
    return [[v]*w for _ in range(h)]

def dims(g):
    return len(g), len(g[0])

def copyg(g):
    return [row[:] for row in g]

def crop_nonzero(g, ignore=(0,9)):
    cells=[(r,c) for r,row in enumerate(g) for c,v in enumerate(row) if v not in ignore]
    if not cells:
        return [[0]]
    minr=min(r for r,c in cells); maxr=max(r for r,c in cells)
    minc=min(c for r,c in cells); maxc=max(c for r,c in cells)
    return [row[minc:maxc+1] for row in g[minr:maxr+1]]

def split_panels(grid, divider=9):
    h,w=dims(grid)
    panels=[]
    start=0
    c=0
    while c<w:
        if all(grid[r][c]==divider for r in range(h)):
            if start<c:
                panels.append([row[start:c] for row in grid])
            while c<w and all(grid[r][c]==divider for r in range(h)):
                c+=1
            start=c
        else:
            c+=1
    if start<w:
        panels.append([row[start:w] for row in grid])
    return panels

def rot90(g):
    h,w=dims(g)
    return [[g[h-1-r][c] for r in range(h)] for c in range(w)]

def rot180(g): return rot90(rot90(g))

def rot270(g): return rot90(rot180(g))

def flip_h(g):
    return [list(reversed(row)) for row in g]

def variants(g, mode='id'):
    out=[]
    names=[]
    if mode=='id':
        return [('id',g)]
    if mode=='rot4':
        return [('id',g),('rot90',rot90(g)),('rot180',rot180(g)),('rot270',rot270(g))]
    if mode=='dihedral':
        rots=[('id',g),('rot90',rot90(g)),('rot180',rot180(g)),('rot270',rot270(g))]
        vals=rots+[('flip_h',flip_h(g)),('flip_h_rot90',rot90(flip_h(g))),('flip_h_rot180',rot180(flip_h(g))),('flip_h_rot270',rot270(flip_h(g)))]
        # dedup by grid
        seen=set()
        out=[]
        for n,gg in vals:
            key=tuple(tuple(row) for row in gg)
            if key not in seen:
                seen.add(key)
                out.append((n,gg))
        return out
    raise ValueError(mode)

def find_template_matches(board, template, mode='id', wildcard=0):
    bh,bw=dims(board); th,tw=dims(template)
    outs=[]
    for name,t in variants(template, mode):
        th,tw=dims(t)
        for r in range(bh-th+1):
            for c in range(bw-tw+1):
                ok=True
                for i in range(th):
                    for j in range(tw):
                        tv=t[i][j]
                        if tv==wildcard:
                            continue
                        if board[r+i][c+j]!=tv:
                            ok=False; break
                    if not ok: break
                if ok:
                    outs.append((r,c,name,t))
    return outs

def exact_or_one_hole_matches(board, template, mode='id', holes=1):
    """Return matches where nonzero template cells can be either equal or zero in board, with exactly holes zeros."""
    outs=[]
    for name,t in variants(template, mode):
        th,tw=dims(t)
        bh,bw=dims(board)
        required=[(i,j,t[i][j]) for i in range(th) for j in range(tw) if t[i][j]!=0]
        for r in range(bh-th+1):
            for c in range(bw-tw+1):
                missing=[]
                ok=True
                for i,j,tv in required:
                    bv=board[r+i][c+j]
                    if bv==tv:
                        continue
                    elif bv==0:
                        missing.append((r+i,c+j,tv))
                    else:
                        ok=False; break
                if ok and len(missing)==holes:
                    # also require zero template cells stay zero? not necessary maybe noise may exist? likely require exact
                    for i in range(th):
                        for j in range(tw):
                            if t[i][j]==0 and board[r+i][c+j]!=0:
                                ok=False; break
                        if not ok: break
                if ok and len(missing)==holes:
                    outs.append((r,c,name,t,missing))
    return outs

def exact_with_border_clear(board, template):
    matches=[]
    th,tw=dims(template); bh,bw=dims(board)
    for r,c,name,t in find_template_matches(board, template, mode='id'):
        clear=True
        for i in range(r-1,r+th+1):
            for j in range(c-1,c+tw+1):
                if 0<=i<bh and 0<=j<bw:
                    if r<=i<r+th and c<=j<c+tw:
                        continue
                    if board[i][j]!=0:
                        clear=False
        if clear:
            matches.append((r,c,name,t))
    return matches

def color_pattern_match(board, template):
    """Match template up to injective color remap on nonzero colors; zeros exact 0."""
    bh,bw=dims(board); th,tw=dims(template)
    outs=[]
    tmpl_colors=sorted({template[i][j] for i in range(th) for j in range(tw) if template[i][j]!=0})
    for r in range(bh-th+1):
        for c in range(bw-tw+1):
            fwd={}
            rev={}
            ok=True
            for i in range(th):
                for j in range(tw):
                    tv=template[i][j]; bv=board[r+i][c+j]
                    if tv==0:
                        if bv!=0:
                            ok=False; break
                    else:
                        if bv==0:
                            ok=False; break
                        if tv in fwd and fwd[tv]!=bv:
                            ok=False; break
                        if bv in rev and rev[bv]!=tv:
                            ok=False; break
                        fwd[tv]=bv; rev[bv]=tv
                if not ok: break
            if ok:
                outs.append((r,c,fwd))
    return outs

def render_board(h,w,cells,color=8):
    g=blank(h,w,0)
    for r,c in cells:
        if 0<=r<h and 0<=c<w:
            g[r][c]=color
    return g

def board_union_matches(board, matches, color=8):
    h,w=dims(board); out=blank(h,w,0)
    for r,c,_,t in matches:
        th,tw=dims(t)
        for i in range(th):
            for j in range(tw):
                if t[i][j]!=0:
                    out[r+i][c+j]=color
    return out

def board_copy_matches(board, matches):
    h,w=dims(board); out=blank(h,w,0)
    for r,c,_,t in matches:
        th,tw=dims(t)
        for i in range(th):
            for j in range(tw):
                if t[i][j]!=0:
                    out[r+i][c+j]=board[r+i][c+j]
    return out

def border_boxes(board, matches, color=8):
    h,w=dims(board); out=blank(h,w,0)
    for r,c,_,t in matches:
        th,tw=dims(t)
        for j in range(c,c+tw):
            out[r][j]=color; out[r+th-1][j]=color
        for i in range(r,r+th):
            out[i][c]=color; out[i][c+tw-1]=color
    return out

def parse_template_board(grid):
    panels=split_panels(grid)
    template=crop_nonzero(panels[0])
    board=panels[1]
    return template, board

def parse_template_selector_board(grid):
    panels=split_panels(grid)
    template=crop_nonzero(panels[0])
    selector_panel=panels[1]
    color=[v for row in selector_panel for v in row if v!=0]
    color=color[0] if color else 8
    board=panels[2]
    return template, color, board

def parse_two_templates_selector_board(grid):
    panels=split_panels(grid)
    t1=crop_nonzero(panels[0]); t2=crop_nonzero(panels[1])
    color=[v for row in panels[2] for v in row if v!=0][0]
    board=panels[3]
    return t1,t2,color,board

def parse_template_candidates(grid):
    panels=split_panels(grid)
    template=crop_nonzero(panels[0])
    candidates=panels[1:]
    return template,candidates

def parse_key_values_query(grid):
    panels=split_panels(grid)
    # key1,value1,key2,value2,query
    return crop_nonzero(panels[0]), crop_nonzero(panels[1]), crop_nonzero(panels[2]), crop_nonzero(panels[3]), panels[4]

def parse_example_transform_query(grid):
    panels=split_panels(grid)
    return crop_nonzero(panels[0]), crop_nonzero(panels[1]), crop_nonzero(panels[2])

def strip_mark(n, idxs, color=8):
    row=[0]*n
    for i in idxs:
        row[i]=color
    return [row]

def dihedral_equiv(a,b):
    keyb=tuple(tuple(row) for row in crop_nonzero(b))
    for _,v in variants(crop_nonzero(a), 'dihedral'):
        if tuple(tuple(row) for row in v)==keyb:
            return True
    return False

def detect_transform(src, tgt):
    tgt_key=tuple(tuple(row) for row in crop_nonzero(tgt))
    for name,v in variants(crop_nonzero(src), 'dihedral'):
        if tuple(tuple(row) for row in v)==tgt_key:
            return name
    return 'id'

def apply_transform(g, name):
    base=crop_nonzero(g)
    mapping={'id':lambda x:x,'rot90':rot90,'rot180':rot180,'rot270':rot270,
             'flip_h':flip_h,'flip_h_rot90':lambda x:rot90(flip_h(x)),
             'flip_h_rot180':lambda x:rot180(flip_h(x)),
             'flip_h_rot270':lambda x:rot270(flip_h(x))}
    return mapping[name](base)

def solve_S20_E1(grid):
    template, board = parse_template_board(grid)
    h,w=dims(board)
    cells=[]
    th,tw=dims(template)
    for r,c,_,_ in find_template_matches(board, template, 'id'):
        cells.append((r+th//2,c+tw//2))
    return render_board(h,w,cells,8)

def solve_S20_E2(grid):
    template, board = parse_template_board(grid)
    return board_union_matches(board, find_template_matches(board, template, 'id'), 8)

def solve_S20_E3(grid):
    template, board = parse_template_board(grid)
    return board_copy_matches(board, find_template_matches(board, template, 'id'))

def solve_S20_E4(grid):
    template, color, board = parse_template_selector_board(grid)
    return board_union_matches(board, find_template_matches(board, template, 'id'), color)

def solve_S20_E5(grid):
    template, candidates = parse_template_candidates(grid)
    idxs=[]
    for i,b in enumerate(candidates):
        if find_template_matches(b, template, 'id'):
            idxs.append(i)
    return strip_mark(len(candidates), idxs, 8)

def solve_S20_E6(grid):
    template, board = parse_template_board(grid)
    h,w=dims(board)
    counts=[0]*h
    for r,c,_,_ in find_template_matches(board, template, 'id'):
        counts[r]+=1
    return [counts]

def solve_S20_E7(grid):
    template, board = parse_template_board(grid)
    h,w=dims(board); th,tw=dims(template)
    cells=[]
    for r,c,_,_ in find_template_matches(board, template, 'id'):
        cells.append((r+th-1,c+tw-1))
    return render_board(h,w,cells,8)

def solve_S20_M1(grid):
    template, board = parse_template_board(grid)
    h,w=dims(board); th,tw=dims(template)  # template dims before rot maybe 3x3
    cells=[]
    for r,c,_,t in find_template_matches(board, template, 'rot4'):
        th1,tw1=dims(t)
        cells.append((r+th1//2,c+tw1//2))
    # dedup
    return render_board(h,w,set(cells),8)

def solve_S20_M2(grid):
    template, board = parse_template_board(grid)
    return board_union_matches(board, find_template_matches(board, template, 'dihedral'), 8)

def solve_S20_M3(grid):
    template, board = parse_template_board(grid)
    out=copyg(board)
    seen=set()
    for r,c,name,t,missing in exact_or_one_hole_matches(board, template, 'id', holes=1):
        for mr,mc,tv in missing:
            out[mr][mc]=tv
    return out

def solve_S20_M4(grid):
    t1,t2,color,board = parse_two_templates_selector_board(grid)
    template = t1 if color==2 else t2
    return board_union_matches(board, find_template_matches(board, template, 'id'), 8)

def solve_S20_M5(grid):
    template, candidates=parse_template_candidates(grid)
    idxs=[]
    for i,b in enumerate(candidates):
        if find_template_matches(b, template, 'rot4'):
            idxs.append(i)
    return strip_mark(len(candidates), idxs, 8)

def solve_S20_M6(grid):
    template, board = parse_template_board(grid)
    return border_boxes(board, find_template_matches(board, template, 'id'), 8)

def solve_S20_M7(grid):
    template, board = parse_template_board(grid)
    h,w=dims(board); th,tw=dims(template)
    cells=[]
    for r,c,_,_ in exact_with_border_clear(board, template):
        cells.append((r+th//2,c+tw//2))
    return render_board(h,w,cells,8)

def solve_S20_H1(grid):
    template,candidates=parse_template_candidates(grid)
    good=[dihedral_equiv(template,b) for b in candidates]
    # mark odd ones that are False
    idxs=[i for i,g in enumerate(good) if not g]
    return strip_mark(len(candidates), idxs, 8)

def solve_S20_H2(grid):
    template, board = parse_template_board(grid)
    h,w=dims(board); th,tw=dims(template)
    cells=[]
    for r,c,_ in color_pattern_match(board, template):
        cells.append((r+th//2,c+tw//2))
    return render_board(h,w,cells,8)

def solve_S20_H3(grid):
    template, board = parse_template_board(grid)
    out=copyg(board)
    for r,c,name,t,missing in exact_or_one_hole_matches(board, template, 'rot4', holes=2):
        for mr,mc,tv in missing:
            out[mr][mc]=tv
    return out

def solve_S20_H4(grid):
    k1,v1,k2,v2,query = parse_key_values_query(grid)
    if find_template_matches(query, k1, 'id'):
        return v1
    return v2

def solve_S20_H5(grid):
    panels=split_panels(grid)
    cands=[crop_nonzero(p) for p in panels]
    n=len(cands)
    out=blank(n,n,0)
    for i in range(n):
        for j in range(n):
            if dihedral_equiv(cands[i], cands[j]):
                out[i][j]=8
    return out

def solve_S20_H6(grid):
    src,tgt,q=parse_example_transform_query(grid)
    name=detect_transform(src,tgt)
    return apply_transform(q,name)

def solve_S20_H7(grid):
    template, candidates=parse_template_candidates(grid)
    counts=[]
    for b in candidates:
        counts.append(len(find_template_matches(b, template, 'rot4')))
    maxc=max(counts)
    idxs=[i for i,c in enumerate(counts) if c==maxc and c>0]
    return strip_mark(len(candidates), idxs, 8)
