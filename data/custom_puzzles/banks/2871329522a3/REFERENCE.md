# ARC-style Puzzle Bank — 21 more puzzles (set 21)

This twenty-first bank leans into **rooms, doors, compartment logic, room-graph reasoning, and room-level library lookup**. The central move is to stop treating the grid as one flat bitmap and instead reason over enclosed rooms as discrete units: fill a chosen room, count tokens per room, navigate between rooms through doors, build symbolic outputs from the room graph, or treat entire rooms as keys and values in a little library.

The core primitive introduced here is:

```text
room_graph(grid, wall_color=1, door_color=7)
Treat 1 as walls and 7 as marked doors sitting inside those walls. Return the
enclosed floor regions as rooms together with the adjacency graph induced by
the door cells.
```

The reference programs assume the shared helpers in `arc_puzzle_bank_21_set21_reference.py`.

## Index

### Easy

- **S21_E1** — Fill the Red Seed Room

- **S21_E2** — Each Seed Colors Its Own Room

- **S21_E3** — Mark the Centers of Seeded Rooms

- **S21_E4** — Keep Only the Room with the Most Green Tokens

- **S21_E5** — Highlight the Walls Around Seeded Rooms

- **S21_E6** — Which Rooms Contain Yellow? (Strip Output)

- **S21_E7** — Fill the Room Across the Single Door

### Medium

- **S21_M1** — Fill All One-Door Neighbors of the Red Room

- **S21_M2** — Color Rooms by Door Distance

- **S21_M3** — Keep the Highest-Density Token Room

- **S21_M4** — Copy the Source Motif Into the Query Room

- **S21_M5** — Which Candidate Room Matches the Query Motif?

- **S21_M6** — Fill Rooms Whose Token Count Equals Door Degree

- **S21_M7** — Shortest Door-Path Between the Red and Green Rooms

### Hard

- **S21_H1** — Adjacency Matrix of the Room Graph

- **S21_H2** — Articulation Rooms of the Door Graph

- **S21_H3** — Room Library Lookup: Query Key → Value Room

- **S21_H4** — Odd Candidate Under Dihedral Room-Motif Equivalence

- **S21_H5** — Nearest Seed Colors on the Room Graph

- **S21_H6** — Which Candidate Matches the Query Room Signature?

- **S21_H7** — Learn Motif-to-Fill Mapping from Example Rooms

## S21_E1 — Fill the Red Seed Room
**Skills:** room extraction, compartment fill, same-size output

**Primitive note:** This is the simplest use of room_graph: ignore the door graph and just identify which enclosed floor component contains the marked seed.

**Scaffold:**

- Treat the wall-colored cells as room boundaries.
- Find the one room that contains the red seed 2.
- Fill only that room with color 8 and leave the walls in place.

**Train 1 input**

```text
1111111111
1000100001
1000100001
1000100001
1111111111
1000100001
1020100001
1000100001
1111111111
```
**Train 1 output**

```text
1111111111
1000100001
1000100001
1000100001
1111111111
1888100001
1888100001
1888100001
1111111111
```

**Train 2 input**

```text
1111111111111111
1000100000100001
1000100000100001
1000100200100001
1000100000100001
1000100000100001
1111111111111111
```
**Train 2 output**

```text
1111111111111111
1000188888100001
1000188888100001
1000188888100001
1000188888100001
1000188888100001
1111111111111111
```
**Test input**

```text
11111111111111
10000100010001
10000100010201
10000100010001
11111111111111
10000100010001
10000100010001
10000100010001
10000100010001
10000100010001
11111111111111
```
**Test output**

```text
11111111111111
10000100018881
10000100018881
10000100018881
11111111111111
10000100010001
10000100010001
10000100010001
10000100010001
10000100010001
11111111111111
```
**Written solution:** Segment the grid into rooms separated by walls. Locate the room containing the red seed, then recolor every floor cell in that room to 8 while preserving the wall structure.

**Reference program:**

```python
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
```

## S21_E2 — Each Seed Colors Its Own Room
**Skills:** multi-room mapping, local room fill, color transfer

**Primitive note:** room_graph gives you the room partition; the rule is then just a per-room color transfer from the room’s seed to the room’s whole floor.

**Scaffold:**

- Extract the rooms first; do not treat the whole board as one canvas.
- Any room with a seed should inherit that seed’s color.
- Unseeded rooms stay empty.

**Train 1 input**

```text
1111111111111
1000100010001
1020100010401
1000100010001
1111111111111
1000100010001
1000103010001
1000100010001
1111111111111
```
**Train 1 output**

```text
1111111111111
1222100014441
1222100014441
1222100014441
1111111111111
1000133310001
1000133310001
1000133310001
1111111111111
```

**Train 2 input**

```text
11111111111111111111
10001000001000100001
10001000001000102001
10001005001000100001
10001000001000100001
10001000001000100001
11111111111111111111
```
**Train 2 output**

```text
11111111111111111111
10001555551000122221
10001555551000122221
10001555551000122221
10001555551000122221
10001555551000122221
11111111111111111111
```
**Test input**

```text
1111111111
1000010001
1000010601
1000010001
1111111111
1000010001
1000010001
1003010401
1000010001
1000010001
1111111111
```
**Test output**

```text
1111111111
1000016661
1000016661
1000016661
1111111111
1333314441
1333314441
1333314441
1333314441
1333314441
1111111111
```
**Written solution:** For each room, check whether it contains a nonzero seed cell. If it does, fill the entire room with that seed color. Leave rooms with no seed blank and preserve the walls.

**Reference program:**

```python
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
```

## S21_E3 — Mark the Centers of Seeded Rooms
**Skills:** room centers, compartment geometry, sparse output

**Primitive note:** Once the rooms are extracted, their bounding boxes make the center computation straightforward.

**Scaffold:**

- Only rooms that contain a seed matter.
- Each qualifying room contributes a single marker.
- Place that marker at the geometric center of the room.

**Train 1 input**

```text
11111111111
10001000001
10201000001
10001000001
11111111111
10001000001
10001000001
10001004001
10001000001
10001000001
11111111111
```
**Train 1 output**

```text
11111111111
10001000001
10801000001
10001000001
11111111111
10001000001
10001000001
10001008001
10001000001
10001000001
11111111111
```

**Train 2 input**

```text
111111111111111
100010001000001
100010001002001
100010301000001
100010001000001
100010001000001
111111111111111
```
**Train 2 output**

```text
111111111111111
100010001000001
100010001000001
100010801008001
100010001000001
100010001000001
111111111111111
```
**Test input**

```text
1111111
1000001
1002001
1000001
1111111
1000001
1000001
1000001
1111111
1000001
1003001
1000001
1111111
```
**Test output**

```text
1111111
1000001
1008001
1000001
1111111
1000001
1000001
1000001
1111111
1000001
1008001
1000001
1111111
```
**Written solution:** Identify all rooms containing at least one seed. For each such room, compute the center cell of its rectangular interior and place an 8 there on an otherwise empty floor, keeping the wall pattern.

**Reference program:**

```python
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
```

## S21_E4 — Keep Only the Room with the Most Green Tokens
**Skills:** roomwise counting, argmax selection, same-size highlight

**Primitive note:** The primitive supplies a room partition so the token counts can be compared room by room instead of globally.

**Scaffold:**

- Count the green 3 cells separately inside each room.
- Choose the room with the largest count.
- Fill only that winning room with 8.

**Train 1 input**

```text
11111111111111
13001000010001
10001030010001
10031000010001
11111111111111
10001000010301
10001000010301
10001000010301
11111111111111
```
**Train 1 output**

```text
11111111111111
10001000010001
10001000010001
10001000010001
11111111111111
10001000018881
10001000018881
10001000018881
11111111111111
```

**Train 2 input**

```text
111111111111111
130010000310301
100010300010001
100010030010001
100010003010001
100010000010301
111111111111111
```
**Train 2 output**

```text
111111111111111
100018888810001
100018888810001
100018888810001
100018888810001
100018888810001
111111111111111
```
**Test input**

```text
11111111111
13000010301
10000010301
10000310001
11111111111
13000010001
13000010001
13000010001
10000010001
10000010001
11111111111
```
**Test output**

```text
11111111111
10000010001
10000010001
10000010001
11111111111
18888810001
18888810001
18888810001
18888810001
18888810001
11111111111
```
**Written solution:** Count how many green tokens appear in each room. Select the room with the highest count and fill that entire room with 8, leaving the rest of the floor blank and preserving the walls.

**Reference program:**

```python
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
```

## S21_E5 — Highlight the Walls Around Seeded Rooms
**Skills:** room boundaries, wall extraction, boundary rendering

**Primitive note:** Here room_graph is used to recover a room, and then the output is drawn on the adjacent wall cells rather than in the room interior.

**Scaffold:**

- Find which rooms contain the red seeds.
- Do not fill the rooms themselves.
- Instead, mark the wall cells that border those rooms.

**Train 1 input**

```text
1111111111111
1000100010001
1000102010001
1000100010001
1111111111111
1000100010001
1000100010201
1000100010001
1111111111111
```
**Train 1 output**

```text
0000088800000
0000800080000
0000800080000
0000800080000
0000088808880
0000000080008
0000000080008
0000000080008
0000000008880
```

**Train 2 input**

```text
11111111111111111
10000010001000001
10000010001000001
10020010001000001
10000010001000001
10000010001000001
11111111111111111
```
**Train 2 output**

```text
08888800000000000
80000080000000000
80000080000000000
80000080000000000
80000080000000000
80000080000000000
08888800000000000
```
**Test input**

```text
1111111111
1000010001
1000010201
1000010001
1111111111
1000010001
1000010001
1020010001
1000010001
1000010001
1111111111
```
**Test output**

```text
0000008880
0000080008
0000080008
0000080008
0888808880
8000080000
8000080000
8000080000
8000080000
8000080000
0888800000
```
**Written solution:** Detect all rooms that contain a red seed. For each one, collect the wall cells touching that room’s interior and mark those boundary wall cells with 8 on an otherwise blank grid.

**Reference program:**

```python
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
```

## S21_E6 — Which Rooms Contain Yellow? (Strip Output)
**Skills:** room order, symbolic strip output, presence detection

**Primitive note:** The room partition and its scan order become a symbolic output instead of another same-size grid.

**Scaffold:**

- Order the rooms in reading order: top-to-bottom, left-to-right.
- Check each room for the presence of a yellow 4.
- Emit a one-row strip marking the positive rooms with 8.

**Train 1 input**

```text
1111111111111
1000100010001
1040100010001
1000100010001
1111111111111
1000140010001
1000100010001
1000100010001
1111111111111
```
**Train 1 output**

```text
800080
```

**Train 2 input**

```text
11111111111111111111
10001000001000100001
10001000001000104001
10001004001000100001
10001000001000100001
10001000001000100001
11111111111111111111
```
**Train 2 output**

```text
0808
```
**Test input**

```text
1111111111
1000010001
1000010401
1000010001
1111111111
1000010001
1000010001
1000010001
1000010001
1000010001
1111111111
```
**Test output**

```text
0800
```
**Written solution:** List the rooms in reading order. For each room, test whether it contains at least one yellow token. Output a one-row strip with 8 in the positions of the rooms that do and 0 elsewhere.

**Reference program:**

```python
def solve_S21_E6(grid):
    rooms, adj, cell_to_rid = room_graph(grid)
    order=room_order(rooms)
    idxs=[i for i,rid in enumerate(order) if any(grid[r][c]==4 for r,c in rooms[rid]['cells'])]
    return render_strip(len(order), idxs, 8)
```

## S21_E7 — Fill the Room Across the Single Door
**Skills:** door interpretation, room adjacency, one-step transfer

**Primitive note:** This is the first direct use of the adjacency graph induced by door cells.

**Scaffold:**

- Treat 7 as a door marker sitting in a wall.
- Find the room containing the red seed.
- Move exactly one step across its door and fill the neighboring room.

**Train 1 input**

```text
111111111
100010001
102070001
100010001
111111111
100010001
100010001
100010001
111111111
```
**Train 1 output**

```text
111111111
100018881
100078881
100018881
111111111
100010001
100010001
100010001
111111111
```

**Train 2 input**

```text
111111111111111
100010000010001
100010000010001
100010020070001
100010000010001
100010000010001
111111111111111
```
**Train 2 output**

```text
111111111111111
100010000018881
100010000018881
100010000078881
100010000018881
100010000018881
111111111111111
```
**Test input**

```text
1111111111
1000010001
1000010001
1000010001
1111111111
1000010001
1020010001
1000070001
1000010001
1000010001
1111111111
```
**Test output**

```text
1111111111
1000010001
1000010001
1000010001
1111111111
1000018881
1000018881
1000078881
1000018881
1000018881
1111111111
```
**Written solution:** Build the room graph using the door markers. Locate the room containing the red seed, follow its single door connection to the adjacent room, and fill that destination room with 8.

**Reference program:**

```python
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
```

## S21_M1 — Fill All One-Door Neighbors of the Red Room
**Skills:** room graph, neighbor expansion, multi-target highlight

**Primitive note:** room_graph is used in its plain graph form: rooms are nodes and doors are edges.

**Scaffold:**

- Extract the door graph of the rooms.
- Start from the red-seed room.
- Fill every room at graph distance exactly 1.

**Train 1 input**

```text
1111111111111
1000100010001
1000100010001
1000100010001
1111117111111
1000100010001
1000702070001
1000100010001
1111111111111
```
**Train 1 output**

```text
1111111111111
1000188810001
1000188810001
1000188810001
1111117111111
1888100018881
1888700078881
1888100018881
1111111111111
```

**Train 2 input**

```text
11111111111
10001000001
10001000001
10207000001
10001000001
10001000001
11711111111
10001000001
10001000001
10001000001
11111111111
```
**Train 2 output**

```text
11111111111
10001888881
10001888881
10007888881
10001888881
10001888881
11711111111
18881000001
18881000001
18881000001
11111111111
```
**Test input**

```text
1111111111
1000010001
1000010001
1000010001
1117111111
1000010001
1020070001
1000010001
1117111111
1000010001
1000010001
1000010001
1111111111
```
**Test output**

```text
1111111111
1888810001
1888810001
1888810001
1117111111
1000018881
1000078881
1000018881
1117111111
1888810001
1888810001
1888810001
1111111111
```
**Written solution:** Construct the room adjacency graph from the door markers. Find the room containing the red seed and recolor every directly adjacent room to 8, leaving the seed room itself unfilled.

**Reference program:**

```python
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
```

## S21_M2 — Color Rooms by Door Distance
**Skills:** graph BFS, layered coloring, room distances

**Primitive note:** The room graph is not just used for adjacency here; it becomes a shortest-path structure.

**Scaffold:**

- Use the red-seed room as the source.
- Compute shortest-path distance through doors.
- Map distances 0, 1, 2, and 3+ to different colors.

**Train 1 input**

```text
1111111111111
1000100010001
1020700070001
1000100010001
1111117111111
1000100010001
1000100070001
1000100010001
1111111111111
```
**Train 1 output**

```text
1111111111111
1222133314441
1222733374441
1222133314441
1111117111111
1555144415551
1555144475551
1555144415551
1111111111111
```

**Train 2 input**

```text
111111111111111
100010000010001
100010000010001
102070000070001
100010000010001
100010000010001
111111171111111
100010000010001
100070000070001
100010000010001
111111111111111
```
**Train 2 output**

```text
111111111111111
122213333314441
122213333314441
122273333374441
122213333314441
122213333314441
111111171111111
155514444415551
155574444475551
155514444415551
111111111111111
```
**Test input**

```text
1111111111
1000010001
1020070001
1000010001
1117111711
1000010001
1000010001
1000010001
1117111111
1000010001
1000070001
1000010001
1111111111
```
**Test output**

```text
1111111111
1222213331
1222273331
1222213331
1117111711
1333314441
1333314441
1333314441
1117111111
1444415551
1444475551
1444415551
1111111111
```
**Written solution:** Compute the shortest room-graph distance from the red-seed room to every other room. Fill the source room with 2, distance-1 rooms with 3, distance-2 rooms with 4, and all farther reachable rooms with 5.

**Reference program:**

```python
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
```

## S21_M3 — Keep the Highest-Density Token Room
**Skills:** ratio comparison, room area, weighted selection

**Primitive note:** The room partition matters because density is measured per compartment, not over the whole board.

**Scaffold:**

- A raw token count is not enough here.
- Compare green-token count relative to room area.
- Select the room with the largest density.

**Train 1 input**

```text
11111111111
13001300001
10001000001
10031003001
11111111111
13001300031
10301000001
10001000001
10001000001
10001000031
11111111111
```
**Train 1 output**

```text
11111111111
18881000001
18881000001
18881000001
11111111111
10001000001
10001000001
10001000001
10001000001
10001000001
11111111111
```

**Train 2 input**

```text
1111111111111111111
1300100000130000001
1000103000100300001
1000100000100000001
1000100030100003001
1000100000100000031
1111111111111111111
```
**Train 2 output**

```text
1111111111111111111
1000100000188888881
1000100000188888881
1000100000188888881
1000100000188888881
1000100000188888881
1111111111111111111
```
**Test input**

```text
1111111
1030001
1000001
1000301
1111111
1000001
1003001
1000001
1111111
1300001
1000001
1000001
1000001
1000031
1111111
```
**Test output**

```text
1111111
1888881
1888881
1888881
1111111
1000001
1000001
1000001
1111111
1000001
1000001
1000001
1000001
1000001
1111111
```
**Written solution:** For each room, compute the ratio of green-token count to room area. Choose the room with the highest density and fill that room with 8 while preserving the surrounding walls.

**Reference program:**

```python
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
```

## S21_M4 — Copy the Source Motif Into the Query Room
**Skills:** room-relative coordinates, motif transfer, source/query detection

**Primitive note:** This uses room-relative coordinates: motifs are copied from one room frame to another room frame.

**Scaffold:**

- One room contains the source motif in color 3.
- Another room is marked as the query room by a 2.
- Copy the source motif’s interior coordinates into the query room using color 8.

**Train 1 input**

```text
1111111111111111111
1030001000001000001
1333001000001000001
1000001000001002001
1000001000001000001
1000001000001000001
1111111111111111111
```
**Train 1 output**

```text
1111111111111111111
1000001000001080001
1000001000001888001
1000001000001000001
1000001000001000001
1000001000001000001
1111111111111111111
```

**Train 2 input**

```text
1111111111111
1000001300001
1000001330001
1000001030001
1111111111111
1000001000001
1002001000001
1000001000001
1111111111111
```
**Train 2 output**

```text
1111111111111
1000001000001
1000001000001
1000001000001
1111111111111
1800001000001
1880001000001
1080001000001
1111111111111
```
**Test input**

```text
11111111111111111
13300000100000001
10300000100000001
10330000100000001
10000000100000201
10000000100000001
11111111111111111
```
**Test output**

```text
11111111111111111
10000000188000001
10000000108000001
10000000108800001
10000000100000001
10000000100000001
11111111111111111
```
**Written solution:** Identify the source room containing the 3-colored motif and record the motif’s occupied coordinates relative to that room’s top-left interior cell. Then find the query room containing the 2 marker and draw the same relative pattern there in color 8.

**Reference program:**

```python
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
```

## S21_M5 — Which Candidate Room Matches the Query Motif?
**Skills:** roomwise pattern comparison, symbolic selection, query/candidate split

**Primitive note:** The room partition supplies a natural set of candidates whose interiors can be compared as separate small patterns.

**Scaffold:**

- Treat the first room as the query room.
- Compare the occupied-cell pattern of each candidate room against the query.
- Output a strip marking the matching candidate.

**Train 1 input**

```text
1111111111111111111111111
1030001400001040001440001
1333001400001444001040001
1000001440001000001040001
1000001000001000001000001
1000001000001000001000001
1111111111111111111111111
```
**Train 1 output**

```text
080
```

**Train 2 input**

```text
1111111111111
1330001440001
1030001400001
1030001400001
1111111111111
1440001040001
1040001440001
1040001400001
1111111111111
```
**Train 2 output**

```text
080
```
**Test input**

```text
1111111111111111111111111
1300000010040000140000001
1300000010040000140000001
1333000014440000144400001
1000000010000000100000001
1000000010000000100000001
1111111111111111111111111
```
**Test output**

```text
08
```
**Written solution:** Use the first room as the query. Compare the relative occupied positions inside each remaining room against the query room’s relative occupied positions, ignoring color differences. Mark the matching candidate’s index with 8 in a one-row strip.

**Reference program:**

```python
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
```

## S21_M6 — Fill Rooms Whose Token Count Equals Door Degree
**Skills:** mixed local/global reasoning, graph degree, roomwise selection

**Primitive note:** This puzzle combines a room-local statistic with a graph-global statistic for the same node.

**Scaffold:**

- Count green tokens inside each room.
- Compute each room’s degree in the door graph.
- Fill the rooms where those two numbers are equal.

**Train 1 input**

```text
1111111111111
1000130013301
1030703070001
1000100310001
1111117111111
1000130010001
1000700010001
1000100310001
1111111111111
```
**Train 1 output**

```text
1111111111111
1888188810001
1888788870001
1888188810001
1111117111111
1000188818881
1000788818881
1000188818881
1111111111111
```

**Train 2 input**

```text
11111111111111111111
13001000001000100001
10001030001030100001
10007000007000700301
10001000001030100001
10001000001000100001
11111111111111111111
```
**Train 2 output**

```text
11111111111111111111
18881000001888188881
18881000001888188881
18887000007888788881
18881000001888188881
18881000001888188881
11111111111111111111
```
**Test input**

```text
1111111111
1000010001
1030070301
1000010001
1117111111
1300010001
1000010001
1000070001
1000010001
1000310001
1111111111
```
**Test output**

```text
1111111111
1000018881
1000078881
1000018881
1117111111
1888810001
1888810001
1888870001
1888810001
1888810001
1111111111
```
**Written solution:** For every room, count its green tokens and also count how many neighboring rooms it touches through doors. Recolor the rooms whose token count equals their graph degree with 8.

**Reference program:**

```python
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
```

## S21_M7 — Shortest Door-Path Between the Red and Green Rooms
**Skills:** graph pathfinding, endpoint detection, path highlighting

**Primitive note:** The room graph is used here as a navigation structure rather than just a neighborhood test.

**Scaffold:**

- Find the room with the red seed and the room with the green seed.
- Use doors as graph edges.
- Fill every room along a shortest path between the two endpoints.

**Train 1 input**

```text
1111111111111
1000100010001
1020700070001
1000100010001
1111117111111
1000100010001
1000100070301
1000100010001
1111111111111
```
**Train 1 output**

```text
1111111111111
1888188810001
1888788870001
1888188810001
1111117111111
1000188818881
1000188878881
1000188818881
1111111111111
```

**Train 2 input**

```text
11111111111111111111
10001000001000100001
10001000001000100001
10207000007000703001
10001000001000100001
10001000001000100001
11111111111111111111
```
**Train 2 output**

```text
11111111111111111111
18881888881888188881
18881888881888188881
18887888887888788881
18881888881888188881
18881888881888188881
11111111111111111111
```
**Test input**

```text
1111111111
1000010001
1020010001
1000010001
1117111111
1000010001
1000010001
1000010001
1117111111
1000010001
1000070301
1000010001
1111111111
```
**Test output**

```text
1111111111
1888810001
1888810001
1888810001
1117111111
1888810001
1888810001
1888810001
1117111111
1888818881
1888878881
1888818881
1111111111
```
**Written solution:** Build the room graph, identify the red and green endpoint rooms, and compute a shortest path between them. Fill every room on that path, including the endpoints, with 8.

**Reference program:**

```python
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
```

## S21_H1 — Adjacency Matrix of the Room Graph
**Skills:** symbolic graph output, room ordering, graph encoding

**Primitive note:** This is the most direct symbolic encoding of room_graph itself.

**Scaffold:**

- Order the rooms in reading order.
- Add an edge whenever two rooms share a door.
- Render that graph as an adjacency matrix with 8 for edges.

**Train 1 input**

```text
111111111
100010001
100070001
100010001
117111711
100010001
100010001
100010001
111111111
```
**Train 1 output**

```text
0880
8008
8000
0800
```

**Train 2 input**

```text
111111111111111111111111
100010000010001000010001
100010000010001000010001
100070000070007000070001
100010000010001000010001
100010000010001000010001
111111111111111111111111
```
**Train 2 output**

```text
08000
80800
08080
00808
00080
```
**Test input**

```text
1111111111111
1000100010001
1000700070001
1000100010001
1171117111111
1000100010001
1000100070001
1000100010001
1111111111111
```
**Test output**

```text
080800
808080
080000
800000
080008
000080
```
**Written solution:** Enumerate the rooms in reading order and compute the door adjacency relation among them. Output an N×N matrix, where N is the number of rooms, placing 8 at position (i, j) exactly when room i is adjacent to room j through a door.

**Reference program:**

```python
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
```

## S21_H2 — Articulation Rooms of the Door Graph
**Skills:** graph connectivity, cut vertices, same-size highlight

**Primitive note:** The primitive room graph is now being interrogated for a higher-order graph property: articulation points.

**Scaffold:**

- Think about which rooms are structurally critical in the door graph.
- Remove one room at a time conceptually.
- Fill the rooms whose removal disconnects the graph.

**Train 1 input**

```text
11111111111111111111
10001000001000100001
10001000001000100001
10007000007000700001
10001000001000100001
10001000001000100001
11111111111111111111
```
**Train 1 output**

```text
11111111111111111111
10001888881888100001
10001888881888100001
10007888887888700001
10001888881888100001
10001888881888100001
11111111111111111111
```

**Train 2 input**

```text
1111111111111
1000100010001
1000700070001
1000100010001
1111117111111
1000100010001
1000100010001
1000100010001
1111111111111
```
**Train 2 output**

```text
1111111111111
1888188818881
1888788878881
1888188818881
1111117111111
1888188818881
1888188818881
1888188818881
1111111111111
```
**Test input**

```text
1111111111
1000010001
1000010001
1000010001
1117111111
1000010001
1000070001
1000010001
1117111111
1000010001
1000070001
1000010001
1111111111
```
**Test output**

```text
1111111111
1888810001
1888810001
1888810001
1117111111
1888818881
1888878881
1888818881
1117111111
1888818881
1888878881
1888818881
1111111111
```
**Written solution:** Treat rooms as graph nodes and doors as edges. Find the articulation points of that graph—the rooms whose removal would disconnect part of the remaining graph—and fill exactly those rooms with 8.

**Reference program:**

```python
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
```

## S21_H3 — Room Library Lookup: Query Key → Value Room
**Skills:** library lookup, key/value pairing, room-interior matching

**Primitive note:** The room partition acts like a structured memory bank: whole rooms become keys and values.

**Scaffold:**

- Read the rooms in sequence as key, value, key, value, query.
- Match the query room’s interior pattern against the key rooms.
- Return the interior of the corresponding value room.

**Train 1 input**

```text
1111111111111111111111111111111
1030001440001300001005001300001
1333001400001300001050001300001
1000001400001330001555001330001
1000001000001000001000001000001
1000001000001000001000001000001
1111111111111111111111111111111
```
**Train 1 output**

```text
00500
05000
55500
00000
00000
```

**Train 2 input**

```text
111111111111111111111
130010041030166613001
133010401030106013301
100014001030100010001
111111111111111111111
```
**Train 2 output**

```text
004
040
400
```
**Test input**

```text
11111111111111111111111111111111111111111
13000000180000001000300010200000100030001
13000000108000001003000012220000100300001
13000000100800001030000010200000103000001
13000000100080001300000010000000130000001
10000000100000001000000010000000100000001
11111111111111111111111111111111111111111
```
**Test output**

```text
0200000
2220000
0200000
0000000
0000000
```
**Written solution:** Interpret the first and third rooms as keys, the second and fourth as their associated values, and the fifth as a query key. Compare the query room’s interior pattern to the keys, then output the interior of the matching value room.

**Reference program:**

```python
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
```

## S21_H4 — Odd Candidate Under Dihedral Room-Motif Equivalence
**Skills:** shape normalization, dihedral equivalence, odd-one-out detection

**Primitive note:** Rooms provide clean compartments in which to normalize motifs before applying dihedral equivalence.

**Scaffold:**

- Ignore the walls and compare only the motif inside each room.
- Allow rotations and reflections when comparing motifs.
- Mark the one room whose motif is not equivalent to the others.

**Train 1 input**

```text
1111111111111111111111111
1300001330001300001330001
1300001030001330001300001
1330001030001030001300001
1000001000001000001000001
1000001000001000001000001
1111111111111111111111111
```
**Train 1 output**

```text
0080
```

**Train 2 input**

```text
111111111111111111111
130010301330130013301
133013301030103013001
100010001000100310001
111111111111111111111
```
**Train 2 output**

```text
00080
```
**Test input**

```text
111111111111111111111111111111111
100400001040000014000000144400001
100400001040000014000000140000001
144400001444000014440000140000001
100000001000000010000000100000001
100000001000000010000000100000001
111111111111111111111111111111111
```
**Test output**

```text
0800
```
**Written solution:** Normalize the motif in each room up to rotation and reflection. Three of the candidate rooms belong to the same equivalence class, while one does not. Output a strip marking the odd room with 8.

**Reference program:**

```python
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
```

## S21_H5 — Nearest Seed Colors on the Room Graph
**Skills:** multi-source BFS, graph Voronoi reasoning, tie handling

**Primitive note:** This is a room-level Voronoi diagram built on the door graph rather than on the raw grid.

**Scaffold:**

- Several rooms are seeded with different colors.
- Measure distance between rooms in the door graph, not in pixel space.
- Fill each room with the nearest seed color, using 8 for exact ties.

**Train 1 input**

```text
111111111111111111111111
100010000010001000010001
100010000010001000010001
102070000070007000070301
100010000010001000010001
100010000010001000010001
111111111111111111111111
```
**Train 1 output**

```text
111111111111111111111111
122212222218881333313331
122212222218881333313331
122272222278887333373331
122212222218881333313331
122212222218881333313331
111111111111111111111111
```

**Train 2 input**

```text
1111111111111
1000100010001
1020700070301
1000100010001
1111117111111
1000100010001
1000104010001
1000100010001
1111111111111
```
**Train 2 output**

```text
1111111111111
1222188813331
1222788873331
1222188813331
1111117111111
1888144418881
1888144418881
1888144418881
1111111111111
```
**Test input**

```text
1111111111
1000010001
1020010001
1000010001
1117111711
1000010001
1000070001
1000010001
1117111111
1000010001
1000070301
1000010001
1111111111
```
**Test output**

```text
1111111111
1222212221
1222212221
1222212221
1117111711
1222212221
1222272221
1222212221
1117111111
1333313331
1333373331
1333313331
1111111111
```
**Written solution:** Start a multi-source shortest-path search from all seeded rooms at once. For each room, determine which seed color is closest in the room graph; if two different seed colors are tied for best distance, use 8 instead. Fill each room with its assigned color.

**Reference program:**

```python
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
```

## S21_H6 — Which Candidate Matches the Query Room Signature?
**Skills:** compound room signatures, degree + area + counts, symbolic selection

**Primitive note:** This pushes room_graph beyond raw geometry by blending geometric and graph-theoretic attributes into one descriptor.

**Scaffold:**

- Treat the first room as the query.
- Its signature mixes area, graph degree, and token counts.
- Mark the candidate room whose full signature matches.

**Train 1 input**

```text
111111111
120012001
103070301
100310001
117111711
130213021
102070001
100310301
111111111
```
**Train 1 output**

```text
008
```

**Train 2 input**

```text
1111111111111111111111111
1200001200001200001300001
1030001030001030001000001
1000007000007003007002001
1000001000001000001000001
1000001000001000001000001
1111111111111111111111111
```
**Train 2 output**

```text
008
```
**Test input**

```text
1111111111111111
1200012000120001
1030070300703001
1000310000100021
1111111171111111
1200012000130001
1030070300700301
1000010003100021
1111111111111111
```
**Test output**

```text
00008
```
**Written solution:** Compute a signature for each room consisting of room area, room-graph degree, count of red 2 tokens, and count of green 3 tokens. Use the first room as the query and mark the candidate room whose signature matches it exactly.

**Reference program:**

```python
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
```

## S21_H7 — Learn Motif-to-Fill Mapping from Example Rooms
**Skills:** room-level analogical transfer, motif recognition, learned mapping

**Primitive note:** The rooms serve as discrete training examples inside a single grid, and the solver must transfer a learned mapping across them.

**Scaffold:**

- Some rooms are examples: they already show both a motif and its background fill color.
- Other rooms are queries: they show the motif on blank floor only.
- Learn the motif→color mapping from the example rooms and apply it to the query rooms.

**Train 1 input**

```text
1111111111111111111111111
1262221644441600001060001
1666221644441600001666001
1222221664441660001000001
1222221444441000001000001
1222221444441000001000001
1111111111111111111111111
```
**Train 1 output**

```text
1111111111111111111111111
1262221644441444441222221
1666221644441444441222221
1222221664441444441222221
1222221444441444441222221
1222221444441444441222221
1111111111111111111111111
```

**Train 2 input**

```text
1111111111111
1655551336331
1655551363331
1655551633331
1111111111111
1006001600001
1060001600001
1600001600001
1111111111111
```
**Train 2 output**

```text
1111111111111
1655551336331
1655551363331
1655551633331
1111111111111
1333331555551
1333331555551
1333331555551
1111111111111
```
**Test input**

```text
111111111111111111111111111111111
166888881336333316600000100600001
168888881336333316000000100600001
168888881366333316000000106600001
188888881333333310000000100000001
188888881333333310000000100000001
111111111111111111111111111111111
```
**Test output**

```text
111111111111111111111111111111111
166888881336333318888888133333331
168888881336333318888888133333331
168888881366333318888888133333331
188888881333333318888888133333331
188888881333333318888888133333331
111111111111111111111111111111111
```
**Written solution:** Use the example rooms to infer which motif corresponds to which room-fill color. Then inspect the blank query rooms, identify their motifs, and fill each query room with the color associated with that motif.

**Reference program:**

```python
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
```
