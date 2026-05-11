"""Reference helper library and 21 reference solve functions for the twenty-first custom ARC puzzle bank.

New primitive introduced in this set:

  room_graph(grid, wall_color=1, door_color=7)

Treat 1 as walls and 7 as marked doors sitting inside those walls. The helper
returns the enclosed floor regions as rooms together with the adjacency graph
induced by the door cells. Many tasks in this bank work at the room level
rather than the raw pixel level.

All solve_* functions are deterministic reference programs for the synthetic
ARC-style tasks in set 21.
"""
from typing import List, Tuple
from collections import deque, defaultdict

Grid = List[List[int]]

def blank(h, w, v=0):
    return [[v] * w for _ in range(h)]

def dims(g):
    return len(g), len(g[0])

def extract_rooms(grid, wall_colors=(1, 7, 9)):
    h, w = dims(grid)
    seen = [[False] * w for _ in range(h)]
    rooms = []
    cell_to_rid = {}
    for r in range(h):
        for c in range(w):
            if seen[r][c] or grid[r][c] in wall_colors:
                continue
            q = deque([(r, c)])
            seen[r][c] = True
            cells = []
            while q:
                cr, cc = q.popleft()
                cells.append((cr, cc))
                cell_to_rid[(cr, cc)] = len(rooms)
                for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                    nr, nc = cr + dr, cc + dc
                    if 0 <= nr < h and 0 <= nc < w and (not seen[nr][nc]) and grid[nr][nc] not in wall_colors:
                        seen[nr][nc] = True
                        q.append((nr, nc))
            minr = min(r for r, c in cells)
            minc = min(c for r, c in cells)
            maxr = max(r for r, c in cells)
            maxc = max(c for r, c in cells)
            rooms.append({
                "id": len(rooms),
                "cells": cells,
                "bbox": (minr, minc, maxr - minr + 1, maxc - minc + 1),
            })
    return rooms, cell_to_rid

def room_graph(grid):
    rooms, cell_to_rid = extract_rooms(grid)
    adj = {i: set() for i in range(len(rooms))}
    h, w = dims(grid)
    for r in range(h):
        for c in range(w):
            if grid[r][c] == 7:
                nbr = set()
                for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                    nr, nc = r + dr, c + dc
                    if (nr, nc) in cell_to_rid:
                        nbr.add(cell_to_rid[(nr, nc)])
                if len(nbr) >= 2:
                    nbr = list(nbr)
                    for i in range(len(nbr)):
                        for j in range(i + 1, len(nbr)):
                            a, b = nbr[i], nbr[j]
                            adj[a].add(b)
                            adj[b].add(a)
    return rooms, adj, cell_to_rid

def room_order(rooms):
    return sorted(range(len(rooms)), key=lambda i: (rooms[i]["bbox"][0], rooms[i]["bbox"][1]))

def room_center(room):
    r, c, h, w = room["bbox"]
    return (r + h // 2, c + w // 2)

def wall_boundary_cells(room, grid):
    out = set()
    h, w = dims(grid)
    for r, c in room["cells"]:
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < h and 0 <= nc < w and grid[nr][nc] in (1, 7):
                out.add((nr, nc))
    return out

def render_strip(n, idxs, color=8):
    out = [[0] * n]
    for i in idxs:
        out[0][i] = color
    return out

def bfs_path(adj, start, goal):
    q = deque([start])
    prev = {start: None}
    while q:
        u = q.popleft()
        if u == goal:
            break
        for v in sorted(adj[u]):
            if v not in prev:
                prev[v] = u
                q.append(v)
    if goal not in prev:
        return None
    path = []
    u = goal
    while u is not None:
        path.append(u)
        u = prev[u]
    return path[::-1]

def all_pairs_shortest(adj):
    d = {}
    for s in adj:
        q = deque([s])
        dist = {s: 0}
        while q:
            u = q.popleft()
            for v in adj[u]:
                if v not in dist:
                    dist[v] = dist[u] + 1
                    q.append(v)
        d[s] = dist
    return d

def articulation_points(adj):
    nodes = list(adj)
    arts = []
    for rem in nodes:
        others = [n for n in nodes if n != rem]
        if len(others) <= 1:
            continue
        start = others[0]
        seen = {start}
        q = deque([start])
        while q:
            u = q.popleft()
            for v in adj[u]:
                if v == rem:
                    continue
                if v not in seen and v != rem:
                    seen.add(v)
                    q.append(v)
        if len(seen) != len(others):
            arts.append(rem)
    return arts

def crop_room_interior(grid, room):
    r, c, h, w = room["bbox"]
    return [row[c:c + w] for row in grid[r:r + h]]

def dihedral_variants(cells):
    pts = list(cells)
    if not pts:
        return {tuple()}
    out = set()
    for trans in range(8):
        arr = []
        for r, c in pts:
            if trans == 0:
                u, v = r, c
            elif trans == 1:
                u, v = c, -r
            elif trans == 2:
                u, v = -r, -c
            elif trans == 3:
                u, v = -c, r
            elif trans == 4:
                u, v = r, -c
            elif trans == 5:
                u, v = -c, -r
            elif trans == 6:
                u, v = -r, c
            else:
                u, v = c, r
            arr.append((u, v))
        minu = min(u for u, v in arr)
        minv = min(v for u, v in arr)
        out.add(tuple(sorted((u - minu, v - minv) for u, v in arr)))
    return out

def solve_S21_E1(grid):
    rooms, adj, cell_to_rid = room_graph(grid)
    target=None
    for rid,room in enumerate(rooms):
        if any(grid[r][c]==2 for r,c in room['cells']):
            target=rid; break
    out=blank(*dims(grid),0)
    for r in range(len(grid)):
        for c in range(len(grid[0])):
            if grid[r][c] in (1,7): out[r][c]=grid[r][c]
    for r,c in rooms[target]['cells']:
        out[r][c]=8
    return out


def solve_S21_E2(grid):
    rooms, adj, cell_to_rid = room_graph(grid)
    out=blank(*dims(grid),0)
    for r in range(len(grid)):
        for c in range(len(grid[0])):
            if grid[r][c] in (1,7): out[r][c]=grid[r][c]
    for rid,room in enumerate(rooms):
        colors=[grid[r][c] for r,c in room['cells'] if grid[r][c] not in (0,)]
        if colors:
            # assume one seed color
            col=colors[0]
            for r,c in room['cells']:
                out[r][c]=col
    return out


def solve_S21_E3(grid):
    rooms, adj, cell_to_rid = room_graph(grid)
    out=blank(*dims(grid),0)
    for r in range(len(grid)):
        for c in range(len(grid[0])):
            if grid[r][c] in (1,7): out[r][c]=grid[r][c]
    for rid,room in enumerate(rooms):
        if any(grid[r][c] in (2,3,4,5,6,8,9) for r,c in room['cells']): # any nonzero token
            rr,cc=room_center(room)
            out[rr][cc]=8
    return out


def solve_S21_E4(grid):
    rooms, adj, cell_to_rid = room_graph(grid)
    counts=[sum(1 for r,c in room['cells'] if grid[r][c]==3) for room in rooms]
    target=max(range(len(rooms)), key=lambda rid: counts[rid])
    out=blank(*dims(grid),0)
    for r in range(len(grid)):
        for c in range(len(grid[0])):
            if grid[r][c] in (1,7): out[r][c]=grid[r][c]
    for r,c in rooms[target]['cells']:
        out[r][c]=8
    return out


def solve_S21_E5(grid):
    rooms, adj, cell_to_rid = room_graph(grid)
    out=blank(*dims(grid),0)
    target_cells=set()
    for rid,room in enumerate(rooms):
        if any(grid[r][c]==2 for r,c in room['cells']):
            target_cells |= wall_boundary_cells(room, grid)
    for r,c in target_cells:
        out[r][c]=8
    return out


def solve_S21_E6(grid):
    rooms, adj, cell_to_rid = room_graph(grid)
    order=room_order(rooms)
    idxs=[i for i,rid in enumerate(order) if any(grid[r][c]==4 for r,c in rooms[rid]['cells'])]
    return render_strip(len(order), idxs, 8)


def solve_S21_E7(grid):
    rooms, adj, cell_to_rid = room_graph(grid)
    seed_room=None
    for rid,room in enumerate(rooms):
        if any(grid[r][c]==2 for r,c in room['cells']):
            seed_room=rid; break
    nbrs=sorted(adj[seed_room])
    target=nbrs[0]
    out=blank(*dims(grid),0)
    for r in range(len(grid)):
        for c in range(len(grid[0])):
            if grid[r][c] in (1,7): out[r][c]=grid[r][c]
    for r,c in rooms[target]['cells']:
        out[r][c]=8
    return out


def solve_S21_H1(grid):
    rooms, adj, cell_to_rid = room_graph(grid)
    order=room_order(rooms)
    idx={rid:i for i,rid in enumerate(order)}
    n=len(order)
    out=blank(n,n,0)
    for a in order:
        for b in adj[a]:
            out[idx[a]][idx[b]]=8
    return out


def solve_S21_H2(grid):
    rooms, adj, cell_to_rid = room_graph(grid)
    arts=articulation_points(adj)
    out=blank(*dims(grid),0)
    for r in range(len(grid)):
        for c in range(len(grid[0])):
            if grid[r][c] in (1,7): out[r][c]=grid[r][c]
    for rid in arts:
        for r,c in rooms[rid]['cells']:
            out[r][c]=8
    return out


def solve_S21_H3(grid):
    rooms, adj, cell_to_rid = room_graph(grid)
    order=room_order(rooms)
    # assume sequence keyA, valueA, keyB, valueB, query
    def sig(room):
        r0,c0,h,w=room['bbox']
        return tuple(sorted((r-r0,c-c0,v) for r,c in room['cells'] if (v:=grid[r][c])!=0))
    key1,val1,key2,val2,query=[rooms[rid] for rid in order[:5]]
    q=sig(query)
    if sig(key1)==q:
        return crop_room_interior(grid, val1)
    else:
        return crop_room_interior(grid, val2)


def solve_S21_H4(grid):
    rooms, adj, cell_to_rid = room_graph(grid)
    order=room_order(rooms)
    sigs=[]
    for rid in order:
        r0,c0,h,w=rooms[rid]['bbox']
        cells=[(r-r0,c-c0) for r,c in rooms[rid]['cells'] if grid[r][c]!=0]
        sigs.append(dihedral_variants(cells))
    idxs=[]
    # find odd one whose equivalence class unique
    for i in range(len(sigs)):
        count=sum(1 for j in range(len(sigs)) if sigs[i] & sigs[j])
        if count==1:
            idxs.append(i)
    return render_strip(len(order), idxs, 8)


def solve_S21_H5(grid):
    rooms, adj, cell_to_rid = room_graph(grid)
    seed_rooms=[]
    for rid,room in enumerate(rooms):
        colors={grid[r][c] for r,c in room['cells']} - {0}
        colors={c for c in colors if c not in (1,7,9)}
        if colors:
            # assume at most one seed color
            color=sorted(colors)[0]
            seed_rooms.append((rid,color))
    dists=all_pairs_shortest(adj)
    out=blank(*dims(grid),0)
    for r in range(len(grid)):
        for c in range(len(grid[0])):
            if grid[r][c] in (1,7): out[r][c]=grid[r][c]
    for rid,room in enumerate(rooms):
        best=None; best_colors=set()
        for sr,col in seed_rooms:
            d=dists[sr].get(rid,999)
            if best is None or d<best:
                best=d; best_colors={col}
            elif d==best:
                best_colors.add(col)
        fill = list(best_colors)[0] if len(best_colors)==1 else 8
        for r,c in room['cells']:
            out[r][c]=fill
    return out


def solve_S21_H6(grid):
    rooms, adj, cell_to_rid = room_graph(grid)
    order=room_order(rooms)
    query=order[0]
    def sig(rid):
        room=rooms[rid]
        area=len(room['cells'])
        deg=len(adj[rid])
        cnt2=sum(1 for r,c in room['cells'] if grid[r][c]==2)
        cnt3=sum(1 for r,c in room['cells'] if grid[r][c]==3)
        return (area,deg,cnt2,cnt3)
    qsig=sig(query)
    idxs=[]
    for i,rid in enumerate(order[1:]):
        if sig(rid)==qsig:
            idxs.append(i)
    return render_strip(len(order)-1, idxs, 8)


def solve_S21_H7(grid):
    rooms, adj, cell_to_rid = room_graph(grid)
    # example rooms have nonzero fill background plus motif color 6 or 3? Let's decide later.
    order=room_order(rooms)
    # learn mapping from motif signature (non-background special cells) to background fill color
    mapping={}
    query_rooms=[]
    for rid in order:
        room=rooms[rid]
        vals=[grid[r][c] for r,c in room['cells']]
        nonzero=set(vals)-{0}
        # example room: exactly one dominant fill color among nonzero excluding motif color 6? use max count color other than 6
        cnt=defaultdict(int)
        for v in vals:
            if v!=0: cnt[v]+=1
        # motif cells will be color 6. example if any nonzero color besides 6 repeated on > half area
        bg_candidates=[(n,v) for v,n in cnt.items() if v!=6]
        if bg_candidates and max(n for n,v in bg_candidates) > len(room['cells'])//2:
            fill_color=max(bg_candidates)[1]
            r0,c0,h,w=room['bbox']
            motif=tuple(sorted((r-r0,c-c0) for r,c in room['cells'] if grid[r][c]==6))
            mapping[motif]=fill_color
        else:
            query_rooms.append(rid)
    out=blank(*dims(grid),0)
    for r in range(len(grid)):
        for c in range(len(grid[0])):
            if grid[r][c] in (1,7): out[r][c]=grid[r][c]
    # keep example rooms as-is? We'll copy them maybe preserve colored fill and motif
    for rid in order:
        room=rooms[rid]
        vals=[grid[r][c] for r,c in room['cells']]
        cnt=defaultdict(int)
        for v in vals:
            if v!=0: cnt[v]+=1
        bg_candidates=[(n,v) for v,n in cnt.items() if v!=6]
        is_example = bg_candidates and max(n for n,v in bg_candidates) > len(room['cells'])//2
        if is_example:
            for r,c in room['cells']:
                out[r][c]=grid[r][c]
        else:
            r0,c0,h,w=room['bbox']
            motif=tuple(sorted((r-r0,c-c0) for r,c in room['cells'] if grid[r][c]==6))
            fill=mapping[motif]
            for r,c in room['cells']:
                out[r][c]=fill
    return out


def solve_S21_M1(grid):
    rooms, adj, cell_to_rid = room_graph(grid)
    seed_room=None
    for rid,room in enumerate(rooms):
        if any(grid[r][c]==2 for r,c in room['cells']):
            seed_room=rid; break
    out=blank(*dims(grid),0)
    for r in range(len(grid)):
        for c in range(len(grid[0])):
            if grid[r][c] in (1,7): out[r][c]=grid[r][c]
    for target in adj[seed_room]:
        for r,c in rooms[target]['cells']:
            out[r][c]=8
    return out


def solve_S21_M2(grid):
    rooms, adj, cell_to_rid = room_graph(grid)
    seed_room=None
    for rid,room in enumerate(rooms):
        if any(grid[r][c]==2 for r,c in room['cells']):
            seed_room=rid; break
    dist=all_pairs_shortest(adj)[seed_room]
    cmap={0:2,1:3,2:4}
    out=blank(*dims(grid),0)
    for r in range(len(grid)):
        for c in range(len(grid[0])):
            if grid[r][c] in (1,7): out[r][c]=grid[r][c]
    for rid,room in enumerate(rooms):
        d=dist.get(rid,99)
        col=cmap.get(d,5)
        for r,c in room['cells']:
            out[r][c]=col
    return out


def solve_S21_M3(grid):
    rooms, adj, cell_to_rid = room_graph(grid)
    # highest density of color 3 tokens / area
    scores=[]
    for room in rooms:
        cnt=sum(1 for r,c in room['cells'] if grid[r][c]==3)
        scores.append((cnt, len(room['cells'])))
    target=max(range(len(rooms)), key=lambda rid: scores[rid][0]/scores[rid][1] if scores[rid][1] else -1)
    # avoid float? fine scratch
    out=blank(*dims(grid),0)
    for r in range(len(grid)):
        for c in range(len(grid[0])):
            if grid[r][c] in (1,7): out[r][c]=grid[r][c]
    for r,c in rooms[target]['cells']:
        out[r][c]=8
    return out


def solve_S21_M4(grid):
    rooms, adj, cell_to_rid = room_graph(grid)
    source=None; target=None
    for rid,room in enumerate(rooms):
        vals=set(grid[r][c] for r,c in room['cells'])
        if 3 in vals and 2 not in vals:
            source=rid
        if 2 in vals:
            target=rid
    # positions of 3 in source relative to room bbox
    sr,sc,sh,sw=rooms[source]['bbox']
    pts=[(r-sr,c-sc) for r,c in rooms[source]['cells'] if grid[r][c]==3]
    tr,tc,th,tw=rooms[target]['bbox']
    out=blank(*dims(grid),0)
    for r in range(len(grid)):
        for c in range(len(grid[0])):
            if grid[r][c] in (1,7): out[r][c]=grid[r][c]
    for dr,dc in pts:
        out[tr+dr][tc+dc]=8
    return out


def solve_S21_M5(grid):
    rooms, adj, cell_to_rid = room_graph(grid)
    order=room_order(rooms)
    query_rid=order[0]
    qsig=tuple(sorted((r-rooms[query_rid]['bbox'][0], c-rooms[query_rid]['bbox'][1]) for r,c in rooms[query_rid]['cells'] if grid[r][c]!=0))
    idxs=[]
    for i,rid in enumerate(order[1:]):
        sig=tuple(sorted((r-rooms[rid]['bbox'][0], c-rooms[rid]['bbox'][1]) for r,c in rooms[rid]['cells'] if grid[r][c]!=0))
        # ignore colors
        if sig==qsig:
            idxs.append(i)
    return render_strip(len(order)-1, idxs, 8)


def solve_S21_M6(grid):
    rooms, adj, cell_to_rid = room_graph(grid)
    out=blank(*dims(grid),0)
    for r in range(len(grid)):
        for c in range(len(grid[0])):
            if grid[r][c] in (1,7): out[r][c]=grid[r][c]
    for rid,room in enumerate(rooms):
        cnt=sum(1 for r,c in room['cells'] if grid[r][c]==3)
        deg=len(adj[rid])
        if cnt==deg:
            for r,c in room['cells']:
                out[r][c]=8
    return out


def solve_S21_M7(grid):
    rooms, adj, cell_to_rid = room_graph(grid)
    red=None; green=None
    for rid,room in enumerate(rooms):
        vals=set(grid[r][c] for r,c in room['cells'])
        if 2 in vals: red=rid
        if 3 in vals: green=rid
    path=bfs_path(adj, red, green)
    out=blank(*dims(grid),0)
    for r in range(len(grid)):
        for c in range(len(grid[0])):
            if grid[r][c] in (1,7): out[r][c]=grid[r][c]
    for rid in path:
        for r,c in rooms[rid]['cells']:
            out[r][c]=8
    return out
