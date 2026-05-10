"""Reference helper library and 21 reference solve functions for the twenty-third custom ARC puzzle bank.

New primitive introduced in this set:

  tile_lattice(grid, divider_color=9)

Parse a regular lattice of equal-sized tiles separated by full divider rows
and columns. Unlike arbitrary panel extraction, this primitive treats the
board as a macro-grid of same-sized local boards, which lets the solver
compare, reorder, rotate, summarize, vote over, and look up whole tiles.

All solve_* functions are deterministic reference programs for the
synthetic ARC-style tasks in set 23.
"""
from typing import List
from collections import Counter
import itertools

Grid = List[List[int]]

def blank(h,w,v=0): return [[v]*w for _ in range(h)]


def copy_grid(g): return [row[:] for row in g]


def dims(g): return len(g), len(g[0])


def rot90(t):
    h,w = len(t), len(t[0])
    return [[t[h-1-r][c] for r in range(h)] for c in range(w)]


def rot180(t): return rot90(rot90(t))


def rot270(t): return rot90(rot180(t))


def rotk(tile,k):
    x=tile
    for _ in range(k%4):
        x=rot90(x)
    return x


def flip_h(t): return [row[::-1] for row in t]


def flatten(t): return tuple(v for row in t for v in row)


def nonzero_count(t, colors=None):
    if colors is None:
        return sum(v!=0 for row in t for v in row)
    return sum(v in colors for row in t for v in row)


def majority_nonzero_color(tile):
    cnt=Counter(v for row in tile for v in row if v!=0)
    if not cnt:
        return 0
    best=max(cnt.items(), key=lambda kv:(kv[1], -kv[0]))[0]
    return best


def vertical_symmetry(tile):
    return tile == flip_h(tile)


def bbox_of_nonzero(tile):
    pts=[(r,c) for r,row in enumerate(tile) for c,v in enumerate(row) if v!=0]
    if not pts: return None
    rs=[r for r,c in pts]; cs=[c for r,c in pts]
    return min(rs), min(cs), max(rs), max(cs)


def bbox_fill(tile, color=8):
    out=blank(*dims(tile),0)
    bb=bbox_of_nonzero(tile)
    if bb is None: return out
    r0,c0,r1,c1=bb
    for r in range(r0,r1+1):
        for c in range(c0,c1+1):
            out[r][c]=color
    return out


def tile_lattice(grid, divider_color=9):
    h,w=dims(grid)
    divider_rows=[r for r in range(h) if all(v==divider_color for v in grid[r])]
    divider_cols=[c for c in range(w) if all(grid[r][c]==divider_color for r in range(h))]
    row_bounds=[]
    prev=-1
    for r in divider_rows+[h]:
        if r-prev-1>0:
            row_bounds.append((prev+1,r))
        prev=r
    col_bounds=[]
    prev=-1
    for c in divider_cols+[w]:
        if c-prev-1>0:
            col_bounds.append((prev+1,c))
        prev=c
    tiles=[]
    for r0,r1 in row_bounds:
        row=[]
        for c0,c1 in col_bounds:
            row.append([grid[r][c0:c1] for r in range(r0,r1)])
        tiles.append(row)
    return tiles, row_bounds, col_bounds


def assemble_tiles(tile_matrix, divider_color=9):
    tr=len(tile_matrix); tc=len(tile_matrix[0])
    th,tw=dims(tile_matrix[0][0])
    h=tr*th + (tr-1)
    w=tc*tw + (tc-1)
    out=blank(h,w,divider_color)
    for rr in range(tr):
        for cc in range(tc):
            tile=tile_matrix[rr][cc]
            for r in range(th):
                for c in range(tw):
                    out[rr*(th+1)+r][cc*(tw+1)+c]=tile[r][c]
    return out


def flat_tiles(grid):
    tiles, _, _ = tile_lattice(grid)
    return [t for row in tiles for t in row], len(tiles), len(tiles[0])


def assemble_from_flat(tiles, rows, cols):
    mat=[]
    idx=0
    for r in range(rows):
        row=[]
        for c in range(cols):
            row.append(tiles[idx]); idx+=1
        mat.append(row)
    return assemble_tiles(mat)


def one_hot(n, idx, color=8):
    return [[color if i==idx else 0 for i in range(n)]]


def canonical_rotation(t, ignore_colors=False):
    xs=[]
    x=t
    for _ in range(4):
        key=flatten([[1 if v else 0 for v in row] for row in x] if ignore_colors else x)
        xs.append((key, x))
        x=rot90(x)
    xs.sort(key=lambda z:z[0])
    return [row[:] for row in xs[0][1]]


def colorize_occ(occ_tile, color):
    return [[color if v else 0 for v in row] for row in occ_tile]


def solve_S23_E1(grid):
    tiles, _, _ = tile_lattice(grid)
    out=[]
    for row in tiles:
        out.append([nonzero_count(t) for t in row])
    return out


def solve_S23_E2(grid):
    tiles, _, _ = tile_lattice(grid)
    out_tiles=[]
    for row in tiles:
        out_row=[]
        for t in row:
            x=copy_grid(t)
            if t[0][0]!=0 and t[2][2]!=0:
                x[1][1]=8
            out_row.append(x)
        out_tiles.append(out_row)
    return assemble_tiles(out_tiles)


def solve_S23_E3(grid):
    tiles, _, _ = tile_lattice(grid)
    counts=[nonzero_count(t) for row in tiles for t in row]
    idx=max(range(len(counts)), key=lambda i: counts[i])
    flat=[copy_grid(t) for row in tiles for t in row]
    best=flat[idx]
    flat2=[]
    for i,t in enumerate(flat):
        if i==idx:
            flat2.append([[8 if v!=0 else 0 for v in row] for row in t])
        else:
            flat2.append(copy_grid(t))
    rows=len(tiles); cols=len(tiles[0])
    return assemble_from_flat(flat2, rows, cols)


def solve_S23_E4(grid):
    flat, rows, cols = flat_tiles(grid)
    # source tile: most color-2 cells
    src_idx=max(range(len(flat)), key=lambda i: sum(v==2 for row in flat[i] for v in row))
    tgt_idx=[i for i,t in enumerate(flat) if any(v==3 for row in t for v in row)][0]
    src=flat[src_idx]
    out=[copy_grid(t) for t in flat]
    newt=blank(*dims(src),0)
    for r,row in enumerate(src):
        for c,v in enumerate(row):
            if v==2:
                newt[r][c]=8
    out[tgt_idx]=newt
    return assemble_from_flat(out, rows, cols)


def solve_S23_E5(grid):
    tiles, _, _ = tile_lattice(grid)
    return [[majority_nonzero_color(t) for t in row] for row in tiles]


def solve_S23_E6(grid):
    tiles, _, _ = tile_lattice(grid)
    out=[[flip_h(t) for t in row] for row in tiles]
    return assemble_tiles(out)


def solve_S23_E7(grid):
    flat, rows, cols = flat_tiles(grid)
    out=blank(rows, cols, 0)
    idx=0
    for r in range(rows):
        for c in range(cols):
            if vertical_symmetry(flat[idx]):
                out[r][c]=8
            idx+=1
    return out


def solve_S23_M1(grid):
    flat, rows, cols = flat_tiles(grid)
    out=[]
    for t in flat:
        motif=[[1 if v==2 else 0 for v in row] for row in t]
        tile=colorize_occ(motif,8)
        if any(v==3 for row in t for v in row):
            tile=rot90(tile)
        out.append(tile)
    return assemble_from_flat(out, rows, cols)


def solve_S23_M2(grid):
    flat, rows, cols = flat_tiles(grid)
    h,w=dims(flat[0])
    out=blank(h,w,0)
    for t in flat:
        for r in range(h):
            for c in range(w):
                if t[r][c]!=0:
                    out[r][c]=8
    return out


def solve_S23_M3(grid):
    tiles, _, _ = tile_lattice(grid)
    top=tiles[0]
    bottom=tiles[1]
    lib={}
    for t in top:
        key=t[0][0]
        lib[key]=[[1 if (v==2 or (v!=0 and (r,c)!=(0,0) and v!=key)) else 0 for c,v in enumerate(row)] for r,row in enumerate(t)]
        # but keep only motif nonzero excluding key
        lib[key]=[[1 if (v==2) else 0 for v in row] for row in t]
    out=[ [copy_grid(t) for t in top], [] ]
    for q in bottom:
        key=max(v for row in q for v in row)
        motif=lib[key]
        out[1].append(colorize_occ(motif,8))
    return assemble_tiles(out)


def solve_S23_M4(grid):
    flat, rows, cols = flat_tiles(grid)
    # find class by canonical rotation
    reps=[flatten(canonical_rotation([[1 if v!=0 else 0 for v in row] for row in t])) for t in flat]
    freq=Counter(reps)
    odd_idx=[i for i,r in enumerate(reps) if freq[r]==1][0]
    return one_hot(len(flat), odd_idx)


def solve_S23_M5(grid):
    tiles, _, _ = tile_lattice(grid)
    out=[[bbox_fill(t,8) for t in row] for row in tiles]
    return assemble_tiles(out)


def solve_S23_M6(grid):
    flat, rows, cols = flat_tiles(grid)
    assert rows==1
    ordered=sorted(flat, key=lambda t:(nonzero_count(t), flatten(t)))
    return assemble_from_flat(ordered, 1, cols)


def solve_S23_M7(grid):
    flat, rows, cols = flat_tiles(grid)
    out=[canonical_rotation(t) for t in flat]
    return assemble_from_flat(out, rows, cols)


def solve_S23_H1(grid):
    tiles, _, _ = tile_lattice(grid)
    A,B,C = tiles[0]
    cands = tiles[1]
    target=rot90([[1 if v!=0 else 0 for v in row] for row in C])
    idx=[i for i,t in enumerate(cands) if [[1 if v!=0 else 0 for v in row] for row in t]==target][0]
    return one_hot(len(cands), idx)


def solve_S23_H2(grid):
    flat, rows, cols = flat_tiles(grid)
    n=len(flat)
    reps=[canonical_rotation([[1 if v!=0 else 0 for v in row] for row in t]) for t in flat]
    out=blank(n,n,0)
    for i in range(n):
        for j in range(n):
            if reps[i]==reps[j]:
                out[i][j]=8
    return out


def solve_S23_H3(grid):
    flat, rows, cols = flat_tiles(grid)
    h,w=dims(flat[0])
    out=blank(h,w,0)
    for r in range(h):
        for c in range(w):
            cnt=sum(1 for t in flat if t[r][c]!=0)
            if cnt>=3:
                out[r][c]=8
    return out


def solve_S23_H4(grid):
    tiles, _, _ = tile_lattice(grid)
    top=tiles[0]
    bottom=tiles[1]
    proto=[]
    for t in top:
        label=t[0][0]
        motif=[[1 if (v!=0 and not (r==0 and c==0)) else 0 for c,v in enumerate(row)] for r,row in enumerate(t)]
        proto.append((label, canonical_rotation(motif)))
    out=[]
    for q in bottom:
        qcan=canonical_rotation([[1 if v!=0 else 0 for v in row] for row in q])
        label=[lab for lab,can in proto if can==qcan][0]
        out.append(label)
    return [out]


def solve_S23_H5(grid):
    tiles, _, _ = tile_lattice(grid)
    A=tiles[0][0]; B=tiles[0][1]; C=tiles[1][0]
    h,w=dims(A)
    out=blank(h,w,0)
    for r in range(h):
        for c in range(w):
            bit=((A[r][c]!=0) ^ (B[r][c]!=0) ^ (C[r][c]!=0))
            if bit:
                out[r][c]=8
    return out


def solve_S23_H6(grid):
    flat, rows, cols = flat_tiles(grid)
    # first three are sequence, last is blank
    return colorize_occ([[1 if v!=0 else 0 for v in row] for row in rot90(flat[2])],8)


def solve_S23_H7(grid):
    flat, rows, cols = flat_tiles(grid)
    # search arrangement 2x2 with rotations
    indices=range(len(flat))
    rots=[lambda x:x, rot90, rot180, rot270]
    best=None
    for perm in itertools.permutations(indices,4):
        for ks in itertools.product(range(4), repeat=4):
            arr=[rotk(flat[perm[i]], ks[i]) for i in range(4)]
            t0,t1,t2,t3=arr
            # match right/left and bottom/top edge-center colors
            if t0[1][2]!=t1[1][0]: 
                continue
            if t2[1][2]!=t3[1][0]:
                continue
            if t0[2][1]!=t2[0][1]:
                continue
            if t1[2][1]!=t3[0][1]:
                continue
            cand=assemble_tiles([[t0,t1],[t2,t3]])
            key=flatten(cand)
            if best is None or key<best[0]:
                best=(key,cand)
    if best is None:
        raise ValueError("no arrangement")
    return best[1]

