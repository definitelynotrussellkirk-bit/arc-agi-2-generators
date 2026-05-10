# ARC-style Puzzle Bank — 21 more puzzles (set 22)

This twenty-second bank leans into **marker-defined local frames, coordinate transport, candidate matching, and frame-relative symbolic reasoning**. The common move is to stop reading motifs in raw image coordinates and instead interpret them inside small, colored local frames. Once a frame is parsed, offsets, rotations, reflections, candidate matching, and even symbolic outputs can all be defined in frame-relative coordinates rather than global rows and columns.

The core primitive introduced here is:

```text
marker_frame(grid, colors=(2,3,4))
Interpret three adjacent colored markers as a local coordinate frame: the first color is the origin, the second is +x, and the third is +y. Reuse the same logic with colors (5,6,7) for target or candidate frames.
```

The reference programs assume the shared helpers in `arc_puzzle_bank_21_set22_reference.py`.

## Index

### Easy

- **S22_E1** — Mark the Local Diagonal

- **S22_E2** — Complete the 2×2 Local Block

- **S22_E3** — Draw the Local X-Bar

- **S22_E4** — Copy One Offset to the Target Frame

- **S22_E5** — Copy a Small Same-Orientation Motif

- **S22_E6** — Copy Only the Maximum-X Point

- **S22_E7** — Canonical Occupancy Strip

### Medium

- **S22_M1** — Orientation-Aware Motif Copy

- **S22_M2** — Multicolor Orientation-Aware Copy

- **S22_M3** — Fill the Source Bounding Box at the Target

- **S22_M4** — Copy Only the Bounding-Box Boundary

- **S22_M5** — Quadrant Count Strip

- **S22_M6** — Copy Only to the Matching Orientation

- **S22_M7** — Copy the Farthest Local Points

### Hard

- **S22_H1** — Odd Candidate Under Local-Coordinate Equivalence

- **S22_H2** — Diagonal Reflection Then Copy

- **S22_H3** — Local 90° Rotation Then Copy

- **S22_H4** — 3×3 Local Occupancy Matrix

- **S22_H5** — Copy Only Symmetric Local Pairs

- **S22_H6** — Frame-Library Lookup

- **S22_H7** — Which Candidate Is the Local 90° Rotation?

## S22_E1 — Mark the Local Diagonal
**Skills:** frame parsing, local coordinates, same-size output

**Primitive note:** A single target frame is enough here: once the local x and y directions are known, the missing corner at local coordinate (1,1) is determined.

**Scaffold:**

- Find the target frame markers 5, 6, and 7.
- Treat 6 as one step in +x and 7 as one step in +y from the origin 5.
- Color the cell one x-step and one y-step from the origin with 8.

**Train 1 input**

```text
0000000
0000000
0056000
0070000
0000000
0000000
0000000
```
**Train 1 output**

```text
0000000
0000000
0056000
0078000
0000000
0000000
0000000
```
**Train 2 input**

```text
00000000
00000000
00000000
00000000
00600000
00570000
00000000
00000000
```
**Train 2 output**

```text
00000000
00000000
00000000
00000000
00680000
00570000
00000000
00000000
```
**Test input**

```text
000000000
000000000
000000000
000000700
000000560
000000000
000000000
```
**Test output**

```text
000000000
000000000
000000000
000000780
000000560
000000000
000000000
```
**Written solution**

Parse the target frame so you know the local axes. Then move one local step in x and one local step in y from the origin and color that single global cell 8.

**Reference program**

```python
def solve_S22_E1(grid):
    out = copy_grid(grid)
    frame = find_frames(grid, (5,6,7))[0]
    r,c = gpos(frame["origin"], frame["vx"], frame["vy"], 1, 1)
    out[r][c] = 8
    return out
```

## S22_E2 — Complete the 2×2 Local Block
**Skills:** frame completion, local neighborhood, same-size output

**Primitive note:** The three frame markers already occupy three corners of a local 2×2 block. The task is to recolor that whole local square.

**Scaffold:**

- Use the frame to identify the local coordinates (0,0), (1,0), and (0,1).
- Add the fourth corner at (1,1).
- Recolor all four cells of that local square to 8.

**Train 1 input**

```text
0000000
0000000
0056000
0070000
0000000
0000000
0000000
```
**Train 1 output**

```text
0000000
0000000
0088000
0088000
0000000
0000000
0000000
```
**Train 2 input**

```text
00000000
00000000
00000000
00000000
00000700
00006500
00000000
00000000
```
**Train 2 output**

```text
00000000
00000000
00000000
00000000
00008800
00008800
00000000
00000000
```
**Test input**

```text
000000000
000000000
000000000
000005700
000006000
000000000
000000000
```
**Test output**

```text
000000000
000000000
000000000
000008800
000008800
000000000
000000000
```
**Written solution**

Interpret the markers as a local unit square and recolor every cell of that square, including the three marker cells and the missing diagonal corner, to 8.

**Reference program**

```python
def solve_S22_E2(grid):
    out = copy_grid(grid)
    frame = find_frames(grid,(5,6,7))[0]
    for uv in [(0,0),(1,0),(0,1),(1,1)]:
        r,c = gpos(frame["origin"], frame["vx"], frame["vy"], *uv)
        out[r][c] = 8
    return out
```

## S22_E3 — Draw the Local X-Bar
**Skills:** directed extension, local axes, same-size output

**Primitive note:** This is a one-dimensional use of the frame: follow only the positive x direction defined by the 6 marker.

**Scaffold:**

- Find the origin and the +x direction.
- Take local positions (0,0), (1,0), and (2,0).
- Color that three-cell local bar with 8.

**Train 1 input**

```text
00000000
00000000
00000000
00560000
00700000
00000000
00000000
00000000
```
**Train 1 output**

```text
00000000
00000000
00000000
00888000
00700000
00000000
00000000
00000000
```
**Train 2 input**

```text
00000000
00000000
00000000
00000000
00000600
00000570
00000000
00000000
```
**Train 2 output**

```text
00000000
00000000
00000000
00000800
00000800
00000870
00000000
00000000
```
**Test input**

```text
000000000
000000000
000000000
000000000
000006500
000000700
000000000
000000000
```
**Test output**

```text
000000000
000000000
000000000
000000000
000088800
000000700
000000000
000000000
```
**Written solution**

Read the target frame, then walk along its local x-axis starting at the origin. Color the origin, the x-marker cell, and the next x-step cell with 8.

**Reference program**

```python
def solve_S22_E3(grid):
    out = copy_grid(grid)
    frame = find_frames(grid,(5,6,7))[0]
    for uv in [(0,0),(1,0),(2,0)]:
        r,c = gpos(frame["origin"], frame["vx"], frame["vy"], *uv)
        out[r][c] = 8
    return out
```

## S22_E4 — Copy One Offset to the Target Frame
**Skills:** offset extraction, transport between frames, same-size output

**Primitive note:** The source and target frames share the same orientation, so this is pure local-offset copying.

**Scaffold:**

- Locate the one motif cell near the source frame.
- Measure its local offset from the source origin.
- Place an 8 at the same local offset from the target origin.

**Train 1 input**

```text
00000000000000000
00000000000000000
00000000000000000
00000000000000000
00023000000056000
00040800000070000
00000000000000000
00000000000000000
00000000000000000
```
**Train 1 output**

```text
00000000000000000
00000000000000000
00000000000000000
00000000000000000
00023000000056000
00040800000070800
00000000000000000
00000000000000000
00000000000000000
```
**Train 2 input**

```text
0000000000000000
0000000000000000
0000000000000000
0000000000000000
0000000000000000
0000000000000000
0003000000060000
0002400000057000
0000080000000000
0000000000000000
0000000000000000
```
**Train 2 output**

```text
0000000000000000
0000000000000000
0000000000000000
0000000000000000
0000000000000000
0000000000000000
0003000000060000
0002400000057000
0000080000000800
0000000000000000
0000000000000000
```
**Test input**

```text
000000000000000000
000000000000000000
000000000000000000
000000800000000000
000040000000007000
000023000000005600
000000000000000000
000000000000000000
000000000000000000
000000000000000000
```
**Test output**

```text
000000000000000000
000000000000000000
000000000000000000
000000800000000080
000040000000007000
000023000000005600
000000000000000000
000000000000000000
000000000000000000
000000000000000000
```
**Written solution**

Find the single source motif cell, convert it to a local coordinate relative to the source frame, and stamp that same local coordinate in the target frame.

**Reference program**

```python
def solve_S22_E4(grid):
    out = copy_grid(grid)
    sf = find_frames(grid,(2,3,4))[0]
    tf = find_frames(grid,(5,6,7))[0]
    pts = extract_local_points(grid, sf, {8}, radius=4)
    assert len(pts)==1
    (uv,col) = pts[0]
    r,c = gpos(tf["origin"], tf["vx"], tf["vy"], *uv)
    out[r][c] = col
    return out
```

## S22_E5 — Copy a Small Same-Orientation Motif
**Skills:** multi-point offset copy, frame-relative transport, same-size output

**Primitive note:** This is the multi-cell version of E4: all source offsets are copied unchanged because the frames point the same way.

**Scaffold:**

- Collect every motif cell around the source frame.
- Record each local offset from the source origin.
- Replay those offsets around the target frame with color 8.

**Train 1 input**

```text
000000000000000000
000000000000000000
000000000000000000
000000000000000000
000000000000000000
000023000000056000
000040880000070000
000008000000000000
000000000000000000
000000000000000000
000000000000000000
```
**Train 1 output**

```text
000000000000000000
000000000000000000
000000000000000000
000000000000000000
000000000000000000
000023000000056000
000040880000070880
000008000000008000
000000000000000000
000000000000000000
000000000000000000
```
**Train 2 input**

```text
000000000000000000
000000000000000000
000000000000000000
000000000000000000
000000000000000000
000000000000000000
008000000000000000
000420000000750000
080030000000060000
008000000000000000
000000000000000000
000000000000000000
```
**Train 2 output**

```text
000000000000000000
000000000000000000
000000000000000000
000000000000000000
000000000000000000
000000000000000000
008000000008000000
000420000000750000
080030000080060000
008000000008000000
000000000000000000
000000000000000000
```
**Test input**

```text
000000000000000000
000000000000000000
000000000000000000
000808000000000000
000040800000070000
000023000000056000
000000000000000000
000000000000000000
000000000000000000
000000000000000000
000000000000000000
```
**Test output**

```text
000000000000000000
000000000000000000
000000000000000000
000808000000808000
000040800000070800
000023000000056000
000000000000000000
000000000000000000
000000000000000000
000000000000000000
000000000000000000
```
**Written solution**

Extract the source motif as a set of local offsets and draw the same offset pattern around the target frame, preserving the relative arrangement.

**Reference program**

```python
def solve_S22_E5(grid):
    out = copy_grid(grid)
    sf = find_frames(grid,(2,3,4))[0]
    tf = find_frames(grid,(5,6,7))[0]
    pts = extract_local_points(grid, sf, {8}, radius=4)
    for uv,col in pts:
        r,c = gpos(tf["origin"], tf["vx"], tf["vy"], *uv)
        out[r][c] = col
    return out
```

## S22_E6 — Copy Only the Maximum-X Point
**Skills:** local ranking, selection, frame-relative copy

**Primitive note:** The frame turns a geometric selection problem into a coordinate one: just keep the point with the largest local x value.

**Scaffold:**

- Convert every source motif cell to a local coordinate.
- Find the one with the greatest x coordinate.
- Copy only that selected point to the target frame.

**Train 1 input**

```text
000000000000000000
000000000000000000
000000000000000000
000000000000000000
000000000000000000
000023800000056000
000840000000070000
000008000000000000
000000000000000000
000000000000000000
000000000000000000
```
**Train 1 output**

```text
000000000000000000
000000000000000000
000000000000000000
000000000000000000
000000000000000000
000023800000056800
000840000000070000
000008000000000000
000000000000000000
000000000000000000
000000000000000000
```
**Train 2 input**

```text
000000000000000000
000000000000000000
000000000000000000
000000000000000000
000008000000000000
000080000000000000
000040800000070000
000320000000650000
000000000000000000
000000000000000000
000000000000000000
000000000000000000
```
**Train 2 output**

```text
000000000000000000
000000000000000000
000000000000000000
000000000000000000
000008000000000000
000080000000080000
000040800000070000
000320000000650000
000000000000000000
000000000000000000
000000000000000000
000000000000000000
```
**Test input**

```text
000000000000000000
000000000000000000
000000000000000000
000000000000000000
000008000000000000
000320000000650000
000840000000070000
000000800000000000
000000000000000000
000000000000000000
000000000000000000
```
**Test output**

```text
000000000000000000
000000000000000000
000000000000000000
000000000000000000
000008000000000000
000320000000650000
000840000000870000
000000800000000000
000000000000000000
000000000000000000
000000000000000000
```
**Written solution**

Measure the source motif cells in local coordinates, choose the cell with maximal local x, and stamp only that point into the target frame.

**Reference program**

```python
def solve_S22_E6(grid):
    out = copy_grid(grid)
    sf = find_frames(grid,(2,3,4))[0]
    tf = find_frames(grid,(5,6,7))[0]
    pts = extract_local_points(grid, sf, {8}, radius=4)
    maxu = max(u for (u,v),col in pts)
    chosen = [ (uv,col) for uv,col in pts if uv[0]==maxu ]
    for uv,col in chosen:
        r,c = gpos(tf["origin"], tf["vx"], tf["vy"], *uv)
        out[r][c] = col
    return out
```

## S22_E7 — Canonical Occupancy Strip
**Skills:** symbolic output, local-coordinate lookup, feature extraction

**Primitive note:** Instead of drawing back into the large grid, this task converts four specific local coordinates into a compact strip output.

**Scaffold:**

- Check whether the source motif occupies each canonical local position in order.
- Use the order (2,0), (0,2), (1,1), (2,2).
- Write 8 in the strip where the position is occupied and 0 otherwise.

**Train 1 input**

```text
000000000
000000000
000000000
000000000
000023800
000048000
000000800
000000000
000000000
```
**Train 1 output**

```text
8088
```
**Train 2 input**

```text
000000000
000000000
000080000
000030000
000024800
000000000
000000000
000000000
000000000
```
**Train 2 output**

```text
8800
```
**Test input**

```text
000000000
000000000
000080800
000048000
000023000
000000000
000000000
000000000
000000000
```
**Test output**

```text
0888
```
**Written solution**

Inspect the source motif at four named local coordinates and emit a 1×4 strip that marks which of those coordinates are present.

**Reference program**

```python
def solve_S22_E7(grid):
    sf = find_frames(grid,(2,3,4))[0]
    pts = set(uv for uv,col in extract_local_points(grid, sf, {8}, radius=4))
    return [[8 if uv in pts else 0 for uv in CANON_E7]]
```

## S22_M1 — Orientation-Aware Motif Copy
**Skills:** rotation/reflection handling, local transport, same-size output

**Primitive note:** The source and target frames can differ by a dihedral transform, so only local coordinates—not raw global vectors—stay invariant.

**Scaffold:**

- Read the motif relative to the source frame, not in global row and column offsets.
- Keep the local coordinates unchanged.
- Render those same local coordinates in the target frame's orientation.

**Train 1 input**

```text
000000000000000000
000000000000000000
000000000000000000
000000000000000000
000000000000000000
000008000000060000
000023000000057000
000040800000000000
000800000000000000
000000000000000000
000000000000000000
000000000000000000
```
**Train 1 output**

```text
000000000000000000
000000000000000000
000000000000000000
000000000000000000
000000000000008000
000008000000860000
000023000000057000
000040800000000800
000800000000000000
000000000000000000
000000000000000000
000000000000000000
```
**Train 2 input**

```text
000000000000000000
000000000000000000
000000000000000000
000000000000000000
000008000000000000
000840800000000000
000023000000750000
000000000000060000
000000000000000000
000000000000000000
000000000000000000
000000000000000000
```
**Train 2 output**

```text
000000000000000000
000000000000000000
000000000000000000
000000000000000000
000008000000000000
000840800000800000
000023000000750000
000000000008060000
000000000000800000
000000000000000000
000000000000000000
000000000000000000
```
**Test input**

```text
000000000000000000
000000000000000000
000000000000000000
000000000000000000
000800000000000000
000040800000000000
000320000000057000
008000000000060000
000000000000000000
000000000000000000
000000000000000000
000000000000000000
```
**Test output**

```text
000000000000000000
000000000000000000
000000000000000000
000000000000000000
000800000000008000
000040800000000000
000320000000057000
008000000000060800
000000000000800000
000000000000000000
000000000000000000
000000000000000000
```
**Written solution**

Convert the source motif into local coordinates and then plot the same local coordinates in the target frame. Because the target frame may rotate or reflect the axes, the global placement changes automatically.

**Reference program**

```python
def solve_S22_M1(grid):
    out = copy_grid(grid)
    sf = find_frames(grid,(2,3,4))[0]
    tf = find_frames(grid,(5,6,7))[0]
    pts = extract_local_points(grid, sf, {8}, radius=4)
    for uv,col in pts:
        r,c = gpos(tf["origin"], tf["vx"], tf["vy"], *uv)
        out[r][c] = col
    return out
```

## S22_M2 — Multicolor Orientation-Aware Copy
**Skills:** multicolor transport, local coordinates, orientation change

**Primitive note:** This is M1 plus color preservation: both coordinates and payload colors must survive the frame change.

**Scaffold:**

- Extract each source motif cell together with its color.
- Store its local coordinate and color.
- Recreate the colored local motif in the target frame.

**Train 1 input**

```text
000000000000000000
000000000000000000
000000000000000000
000000000000000000
000000000000000000
000008000000060000
000023000000057000
000040800000000000
000900000000000000
000000000000000000
000000000000000000
000000000000000000
```
**Train 1 output**

```text
000000000000000000
000000000000000000
000000000000000000
000000000000000000
000000000000008000
000008000000860000
000023000000057000
000040800000000900
000900000000000000
000000000000000000
000000000000000000
000000000000000000
```
**Train 2 input**

```text
000000000000000000
000000000000000000
000000000000000000
000000000000000000
000000000000000000
009000000000000000
000320000000056000
000040900000070000
000800000000000000
000000000000000000
000000000000000000
000000000000000000
```
**Train 2 output**

```text
000000000000000000
000000000000000000
000000000000000000
000000000000000000
000000000000000000
009000000000000900
000320000000056000
000040900009070000
000800000000008000
000000000000000000
000000000000000000
000000000000000000
```
**Test input**

```text
000000000000000000
000000000000000000
000000000000000000
000000000000000000
000000000000000000
000008000000070000
000420000000056000
009030000000000000
000800000000000000
000000000000000000
000000000000000000
000000000000000000
```
**Test output**

```text
000000000000000000
000000000000000000
000000000000000000
000000000000000000
000000000000009000
000008000000070800
000420000000056000
009030000000800000
000800000000000000
000000000000000000
000000000000000000
000000000000000000
```
**Written solution**

Read the source motif as colored local points and place each colored point at the same local coordinate in the target frame.

**Reference program**

```python
def solve_S22_M2(grid):
    out = copy_grid(grid)
    sf = find_frames(grid,(2,3,4))[0]
    tf = find_frames(grid,(5,6,7))[0]
    pts = extract_local_points(grid, sf, {8,9}, radius=4)
    for uv,col in pts:
        r,c = gpos(tf["origin"], tf["vx"], tf["vy"], *uv)
        out[r][c] = col
    return out
```

## S22_M3 — Fill the Source Bounding Box at the Target
**Skills:** local bounding boxes, abstraction, frame-relative rendering

**Primitive note:** The target is not the original source points but the full local rectangle spanning them.

**Scaffold:**

- Convert the source motif to local coordinates.
- Find the min and max x and y values.
- Fill the entire local rectangle between those extrema in the target frame.

**Train 1 input**

```text
000000000000000000
000000000000000000
000000000000000000
000000000000000000
000000000000000000
000000000000060000
000023000000057000
000040880000000000
000000000000000000
000000080000000000
000000000000000000
000000000000000000
```
**Train 1 output**

```text
000000000000000000
000000000000000000
000000000000000000
000000000000008880
000000000000008880
000000000000060000
000023000000057000
000040880000000000
000000000000000000
000000080000000000
000000000000000000
000000000000000000
```
**Train 2 input**

```text
000000000000000000
000000000000000000
000000000000000000
000000000000000000
008800000000000000
080040000000000000
000023000000056000
000000000000070000
000000000000000000
000000000000000000
000000000000000000
000000000000000000
```
**Train 2 output**

```text
000000000000000000
000000000000000000
000000000000000000
000000000000000000
008800000000000000
080040000000000000
000023000000056000
000000000088870000
000000000088800000
000000000000000000
000000000000000000
000000000000000000
```
**Test input**

```text
000000000000000000
000000000000000000
000000000000000000
000000000000000000
000000000000000000
000040000000000000
000320000000057000
000000080000060000
000008000000000000
000000800000000000
000000000000000000
000000000000000000
```
**Test output**

```text
000000000000000000
000000000000000000
000000000000000000
000000000088800000
000000000088800000
000040000088800000
000320000000057000
000000080000060000
000008000000000000
000000800000000000
000000000000000000
000000000000000000
```
**Written solution**

Take the source motif's local bounding box and draw that whole filled local rectangle in the target frame.

**Reference program**

```python
def solve_S22_M3(grid):
    out = copy_grid(grid)
    sf = find_frames(grid,(2,3,4))[0]
    tf = find_frames(grid,(5,6,7))[0]
    pts = [uv for uv,col in extract_local_points(grid,sf,{8},radius=4)]
    for uv,col in bbox_fill_pts(pts,8):
        r,c = gpos(tf["origin"], tf["vx"], tf["vy"], *uv)
        out[r][c] = col
    return out
```

## S22_M4 — Copy Only the Bounding-Box Boundary
**Skills:** outline extraction, local abstractions, frame-relative rendering

**Primitive note:** This is the boundary-only companion to M3: infer the local box, then keep just its perimeter.

**Scaffold:**

- Find the source motif's local bounding box.
- Keep only the coordinates on that box's border.
- Draw that local border in the target frame.

**Train 1 input**

```text
0000000000000000000
0000000000000000000
0000000000000000000
0000000000000000000
0000000000000000000
0000000000000060000
0000023000000057000
0008040000000000000
0000008000000000000
0000800000000000000
0000000000000000000
0000000000000000000
0000000000000000000
```
**Train 1 output**

```text
0000000000000000000
0000000000000000000
0000000000000000000
0000000000000000000
0000000000000000000
0000000000000068880
0000023000000058080
0008040000000008080
0000008000000008880
0000800000000000000
0000000000000000000
0000000000000000000
0000000000000000000
```
**Train 2 input**

```text
0000000000000000000
0000000000000000000
0000000000000000000
0000000000000000000
0000800000000000000
0080000000000000000
0000320000000056000
0008040000000070000
0000000000000000000
0000000000000000000
0000000000000000000
0000000000000000000
0000000000000000000
```
**Train 2 output**

```text
0000000000000000000
0000000000000000000
0000000000000000000
0000000000000000000
0000800000000008880
0080000000000008080
0000320000000058080
0008040000000078880
0000000000000000000
0000000000000000000
0000000000000000000
0000000000000000000
0000000000000000000
```
**Test input**

```text
0000000000000000000
0000000000000000000
0000000000000000000
0000008000000000000
0000800000000000000
0000000800000070000
0000420000000056000
0000030000000000000
0000000000000000000
0000000000000000000
0000000000000000000
0000000000000000000
0000000000000000000
```
**Test output**

```text
0000000000000000000
0000000000000000000
0000000000000000000
0000008000000000000
0000800000000000000
0000000800088870000
0000420000080856000
0000030000080800000
0000000000088800000
0000000000000000000
0000000000000000000
0000000000000000000
0000000000000000000
```
**Written solution**

Compute the local bounding box of the source motif and render only its perimeter, not the filled interior, around the target frame.

**Reference program**

```python
def solve_S22_M4(grid):
    out = copy_grid(grid)
    sf = find_frames(grid,(2,3,4))[0]
    tf = find_frames(grid,(5,6,7))[0]
    pts = [uv for uv,col in extract_local_points(grid,sf,{8},radius=4)]
    for uv,col in bbox_boundary_pts(pts,8):
        r,c = gpos(tf["origin"], tf["vx"], tf["vy"], *uv)
        out[r][c] = col
    return out
```

## S22_M5 — Quadrant Count Strip
**Skills:** symbolic summarization, local quadrants, counting

**Primitive note:** The frame gives a signed coordinate system, which makes quadrant counting well-defined even when the frame rotates globally.

**Scaffold:**

- Measure every source motif point in local coordinates.
- Count how many lie in each signed quadrant.
- Output the four counts in fixed quadrant order.

**Train 1 input**

```text
00000000000
00000000000
00000000000
00000080000
00080000000
00000230000
00000488000
00008000000
00000000000
00000000000
00000000000
```
**Train 1 output**

```text
2111
```
**Train 2 input**

```text
00000000000
00000000000
00000000000
00008000000
00008308000
00000240000
00000080000
00000008000
00000000000
00000000000
00000000000
```
**Train 2 output**

```text
1202
```
**Test input**

```text
00000000000
00000000000
00000000000
00000008000
00008480000
00000230000
00000088000
00008000000
00000000000
00000000000
00000000000
```
**Test output**

```text
2112
```
**Written solution**

Use the source frame to assign each motif cell to a local quadrant and output the quadrant counts as a 1×4 numeric strip.

**Reference program**

```python
def solve_S22_M5(grid):
    sf = find_frames(grid,(2,3,4))[0]
    pts = [uv for uv,col in extract_local_points(grid,sf,{8},radius=4)]
    return [qcounts(pts)]
```

## S22_M6 — Copy Only to the Matching Orientation
**Skills:** orientation matching, candidate selection, frame-relative copy

**Primitive note:** Multiple target frames are present, but only one has the same local axis orientation as the source.

**Scaffold:**

- Compare the source frame's x and y directions to each target frame.
- Choose the target whose ordered axis directions match.
- Copy the source motif only into that matching target.

**Train 1 input**

```text
0000000000000000000000000
0000000000000000000000000
0000000000006000000000000
0000000000005700000000000
0000000000000000000000000
0000000000000000000000000
0002300000000000005600000
0084080000000000007000000
0000800000007000000000000
0000000000005600000000000
0000000000000000000000000
0000000000000000000000000
0000000000000000000000000
```
**Train 1 output**

```text
0000000000000000000000000
0000000000000000000000000
0000000000006000000000000
0000000000005700000000000
0000000000000000000000000
0000000000000000000000000
0002300000000000005600000
0084080000000000087080000
0000800000007000000800000
0000000000005600000000000
0000000000000000000000000
0000000000000000000000000
0000000000000000000000000
```
**Train 2 input**

```text
0000000000000000000000000
0000000000000000000000000
0000000000000000000000000
0000000000065000000000000
0080000000007000000000000
0000000000000000000000000
0042000000000000075000000
0803000000000000006000000
0000800000000000000000000
0000000000005600000000000
0000000000007000000000000
0000000000000000000000000
0000000000000000000000000
```
**Train 2 output**

```text
0000000000000000000000000
0000000000000000000000000
0000000000000000000000000
0000000000065000000000000
0080000000007000080000000
0000000000000000000000000
0042000000000000075000000
0803000000000000806000000
0000800000000000000800000
0000000000005600000000000
0000000000007000000000000
0000000000000000000000000
0000000000000000000000000
```
**Test input**

```text
0000000000000000000000000
0000000000000000000000000
0000000000006000000000000
0000000000005700000000000
0000000000000000000000000
0000800000000000000000000
0032000000000000065000000
0004080000000000007000000
0080000000000000000000000
0000000000005600000000000
0000000000007000000000000
0000000000000000000000000
0000000000000000000000000
```
**Test output**

```text
0000000000000000000000000
0000000000000000000000000
0000000000006000000000000
0000000000005700000000000
0000000000000000000000000
0000800000000000000800000
0032000000000000065000000
0004080000000000007080000
0080000000000000080000000
0000000000005600000000000
0000000000007000000000000
0000000000000000000000000
0000000000000000000000000
```
**Written solution**

Identify which candidate target frame has the same oriented local basis as the source, then copy the source motif there and nowhere else.

**Reference program**

```python
def solve_S22_M6(grid):
    out = copy_grid(grid)
    sf = find_frames(grid,(2,3,4))[0]
    tfs = find_frames(grid,(5,6,7))
    pts = extract_local_points(grid, sf, {8}, radius=4)
    sig = frame_signature(sf)
    for tf in tfs:
        if frame_signature(tf) == sig:
            for uv,col in pts:
                r,c = gpos(tf["origin"], tf["vx"], tf["vy"], *uv)
                out[r][c] = col
    return out
```

## S22_M7 — Copy the Farthest Local Points
**Skills:** distance ranking, local metrics, frame-relative copy

**Primitive note:** The ranking criterion is local Manhattan radius from the frame origin, not raw image distance.

**Scaffold:**

- Convert the source motif cells to local coordinates.
- Compute each point's |x|+|y| distance from the origin.
- Copy only the point or points with maximal local radius to the target.

**Train 1 input**

```text
000000000000000000
000000000000000000
000000000000000000
000000000000000000
000008000000000000
000000000000060000
000023080000057000
008048000000000000
000000000000000000
000000000000000000
000000000000000000
000000000000000000
```
**Train 1 output**

```text
000000000000000000
000000000000000000
000000000000000000
000000000000080000
000008000000000000
000000000008060000
000023080000057000
008048000000000000
000000000000008000
000000000000000000
000000000000000000
000000000000000000
```
**Train 2 input**

```text
000000000000000000
000000000000000000
000000000000000000
000000000000000000
000800000000000000
000040800000000000
080023000000056000
000000000000070000
000800000000000000
000000000000000000
000000000000000000
000000000000000000
```
**Train 2 output**

```text
000000000000000000
000000000000000000
000000000000000000
000000000000000000
000800000000800000
000040800000000000
080023000080056000
000000000000070800
000800000000800000
000000000000000000
000000000000000000
000000000000000000
```
**Test input**

```text
000000000000000000
000000000000000000
000000000000000000
000080000000000000
000000000000000000
000840000000000000
008320000000057000
000000800000060000
000000000000000000
000000000000000000
000000000000000000
000000000000000000
```
**Test output**

```text
000000000000000000
000000000000000000
000000000000000000
000080000000000000
000000000000800000
000840000000000000
008320000000057080
000000800000060000
000000000000000000
000000000000000000
000000000000000000
000000000000000000
```
**Written solution**

Find the source motif cells with largest local Manhattan distance from the origin and reproduce only those farthest cells in the target frame.

**Reference program**

```python
def solve_S22_M7(grid):
    out = copy_grid(grid)
    sf = find_frames(grid,(2,3,4))[0]
    tf = find_frames(grid,(5,6,7))[0]
    pts = extract_local_points(grid,sf,{8},radius=4)
    maxrad = max(manhattan_radius(uv) for uv,col in pts)
    chosen = [ (uv,col) for uv,col in pts if manhattan_radius(uv)==maxrad ]
    for uv,col in chosen:
        r,c = gpos(tf["origin"], tf["vx"], tf["vy"], *uv)
        out[r][c] = col
    return out
```

## S22_H1 — Odd Candidate Under Local-Coordinate Equivalence
**Skills:** candidate comparison, canonical local signatures, symbolic output

**Primitive note:** The candidate motifs must be compared after normalizing them to their own frames; global placement and orientation are distractions.

**Scaffold:**

- Reduce the source motif to its canonical set of local coordinates.
- Do the same for each candidate frame.
- Mark the one candidate whose local signature does not match the others.

**Train 1 input**

```text
0000000000000000000000000
0000000000000800000000000
0000000000086000000000000
0000000000005700000000000
0000000000000080080000000
0000800000000000007080000
0002300000000000005600000
0004080000000000000800000
0080000000000080000000000
0000000000005600000000000
0000000000007080000000000
0000000000080000000000000
0000000000000000000000000
```
**Train 1 output**

```text
008
```
**Train 2 input**

```text
0000000000000000000000000
0000000000000000000000000
0000000000800000000000000
0000000000065000000000000
0080000000007080000000000
0000000000080000000800000
0042000000000000005600000
0803000000080000807000000
0000800000006080000800000
0000000000005700000000000
0000000000000000000000000
0000000000000800000000000
0000000000000000000000000
```
**Train 2 output**

```text
080
```
**Test input**

```text
0000000000000000000000000
0000000000000000000000000
0000000000080000000000000
0000000000005600000000000
0000800000807000080000000
0804000000000800007080000
0002300000000000065000000
0080000000000800000800000
0000000000000000000000000
0000000000005700000000000
0000000000086080000000000
0000000000000000000000000
0000000000000000000000000
```
**Test output**

```text
008
```
**Written solution**

Normalize every motif to its frame-relative local coordinates and identify the single candidate whose local pattern differs from the rest. Output a strip marking that odd candidate.

**Reference program**

```python
def solve_S22_H1(grid):
    sf = find_frames(grid,(2,3,4))[0]
    candidates = find_frames(grid,(5,6,7))
    src_sig = canonical_offsets([uv for uv,col in extract_local_points(grid,sf,{8},radius=4)])
    odd=[]
    for i,tf in enumerate(candidates):
        sig = canonical_offsets([uv for uv,col in extract_local_points(grid,tf,{8},radius=4)])
        odd.append(sig)
    # choose candidate whose signature differs from majority
    # assume exactly one odd
    counts = defaultdict(int)
    for sig in odd:
        counts[sig]+=1
    idx = [i for i,sig in enumerate(odd) if counts[sig]==1][0]
    out=[[0]*len(candidates)]
    out[0][idx]=8
    return out
```

## S22_H2 — Diagonal Reflection Then Copy
**Skills:** coordinate transforms, local reflection, orientation-aware rendering

**Primitive note:** The learned transform is internal to the frame: swap x and y before drawing in the target frame.

**Scaffold:**

- Extract the source motif in local coordinates.
- Apply the transform (x,y) → (y,x).
- Render the reflected local motif in the target frame.

**Train 1 input**

```text
000000000000000000
000000000000000000
000000000000000000
000000000000000000
000000000000000000
000008000000060000
000023000000057000
000040800000000000
000800000000000000
000000000000000000
000000000000000000
000000000000000000
```
**Train 1 output**

```text
000000000000000000
000000000000000000
000000000000000000
000000000000000000
000000000000800000
000008000000060800
000023000000057000
000040800000008000
000800000000000000
000000000000000000
000000000000000000
000000000000000000
```
**Train 2 input**

```text
000000000000000000
000000000000000000
000000000000000000
000000000000000000
000000000000000000
008000000000000000
000320000000056000
000040800000070000
000800000000000000
000000000000000000
000000000000000000
000000000000000000
```
**Train 2 output**

```text
000000000000000000
000000000000000000
000000000000000000
000000000000000000
000000000000008000
008000000000000000
000320000000056000
000040800000070800
000800000000800000
000000000000000000
000000000000000000
000000000000000000
```
**Test input**

```text
000000000000000000
000000000000000000
000000000000000000
000000000000000000
000000000000000000
000800000000070000
000420000000056000
008030000000000000
000008000000000000
000000000000000000
000000000000000000
000000000000000000
```
**Test output**

```text
000000000000000000
000000000000000000
000000000000000000
000000000000000000
000000000000800000
000800000000070800
000420000000056000
008030000000008000
000008000000000000
000000000000000000
000000000000000000
000000000000000000
```
**Written solution**

Read the motif relative to the source frame, swap each point's local x and y coordinates, and then place the transformed points in the target frame.

**Reference program**

```python
def solve_S22_H2(grid):
    out = copy_grid(grid)
    sf = find_frames(grid,(2,3,4))[0]
    tf = find_frames(grid,(5,6,7))[0]
    pts = extract_local_points(grid,sf,{8},radius=4)
    newpts = [ (transform_uv(uv,'refl_diag'), col) for uv,col in pts ]
    for uv,col in newpts:
        r,c = gpos(tf["origin"], tf["vx"], tf["vy"], *uv)
        out[r][c]=col
    return out
```

## S22_H3 — Local 90° Rotation Then Copy
**Skills:** coordinate transforms, multicolor motifs, rotated transport

**Primitive note:** This is a composed operation: preserve colors, rotate the local motif 90° counterclockwise, then map it into the target frame.

**Scaffold:**

- Extract the colored source motif in local coordinates.
- Apply the local rotation (x,y) → (-y,x).
- Draw the rotated colored motif in the target frame.

**Train 1 input**

```text
000000000000000000
000000000000000000
000000000000000000
000000000000000000
000000000000000000
000008000000060000
000023000000057000
000040800000000000
000900000000000000
000000000000000000
000000000000000000
000000000000000000
```
**Train 1 output**

```text
000000000000000000
000000000000000000
000000000000000000
000000000000000000
000000000000000000
000008000000068000
000023000000057000
000040800000000800
000900000000900000
000000000000000000
000000000000000000
000000000000000000
```
**Train 2 input**

```text
000000000000000000
000000000000000000
000000000000000000
000000000000000000
000008000000000000
009040000000000000
000023000000056000
000000900000070000
000000000000000000
000000000000000000
000000000000000000
000000000000000000
```
**Train 2 output**

```text
000000000000000000
000000000000000000
000000000000000000
000000000000000000
000008000000900000
009040000000000000
000023000000056000
000000900008070000
000000000000009000
000000000000000000
000000000000000000
000000000000000000
```
**Test input**

```text
000000000000000000
000000000000000000
000000000000000000
000000000000000000
000900000000000000
008040000000000000
000320000000057000
000008000000060000
000000000000000000
000000000000000000
000000000000000000
000000000000000000
```
**Test output**

```text
000000000000000000
000000000000000000
000000000000000000
000000000000000000
000900000000009000
008040000000000800
000320000000057000
000008000000860000
000000000000000000
000000000000000000
000000000000000000
000000000000000000
```
**Written solution**

Interpret each colored source point in local coordinates, rotate those coordinates by 90° in the local frame, and render the result with the same colors in the target frame.

**Reference program**

```python
def solve_S22_H3(grid):
    out = copy_grid(grid)
    sf = find_frames(grid,(2,3,4))[0]
    tf = find_frames(grid,(5,6,7))[0]
    pts = extract_local_points(grid,sf,{8,9},radius=4)
    newpts = [ (transform_uv(uv,'rot90'), col) for uv,col in pts ]
    for uv,col in newpts:
        r,c = gpos(tf["origin"], tf["vx"], tf["vy"], *uv)
        out[r][c]=col
    return out
```

## S22_H4 — 3×3 Local Occupancy Matrix
**Skills:** canonicalization, symbolic output, local neighborhood encoding

**Primitive note:** The output forgets the original frame orientation and writes a normalized local occupancy image instead.

**Scaffold:**

- Inspect which local offsets in the set {-1,0,1}×{-1,0,1} are occupied.
- Use local coordinates, not global directions.
- Emit a normalized 3×3 matrix with 8s at occupied local offsets.

**Train 1 input**

```text
000000000
000000000
000000000
000808000
000023000
000840000
000000000
000000000
000000000
```
**Train 1 output**

```text
808
000
800
```
**Train 2 input**

```text
000000000
000000000
000000000
000838000
000024000
000800000
000000000
000000000
000000000
```
**Train 2 output**

```text
808
000
008
```
**Test input**

```text
000000000
000000000
000000000
000848000
000023000
000800000
000000000
000000000
000000000
```
**Test output**

```text
800
000
808
```
**Written solution**

Project the source motif into a canonical local 3×3 coordinate window centered on the origin and output that normalized occupancy matrix.

**Reference program**

```python
def solve_S22_H4(grid):
    sf = find_frames(grid,(2,3,4))[0]
    pts = set(uv for uv,col in extract_local_points(grid,sf,{8},radius=2))
    out = blank(3,3,0)
    for u in [-1,0,1]:
        for v in [-1,0,1]:
            if (u,v) in pts:
                out[v+1][u+1] = 8  # row by v, col by u
    return out
```

## S22_H5 — Copy Only Symmetric Local Pairs
**Skills:** symmetry filtering, local reflections, frame-relative copy

**Primitive note:** A source point survives only if its reflection across the local y-axis is also present.

**Scaffold:**

- Convert the source motif to local coordinates.
- Keep only points whose mirrored partner (-x,y) also exists.
- Copy that symmetry-filtered subset to the target frame.

**Train 1 input**

```text
000000000000000000
000000000000000000
000000000000000000
000000000000000000
000000800000000000
000808000000060000
000023000000057000
008040800000000000
000000000000000000
000000000000000000
000000000000000000
000000000000000000
```
**Train 1 output**

```text
000000000000000000
000000000000000000
000000000000000000
000000000000000000
000000800000008000
000808000000860000
000023000000057000
008040800000800000
000000000000008000
000000000000000000
000000000000000000
000000000000000000
```
**Train 2 input**

```text
000000000000000000
000000000000000000
000000000000000000
000000000000000000
000800000000000000
008000800000000000
000320000000056000
000040000000070000
000808000000000000
000000000000000000
000000000000000000
000000000000000000
```
**Train 2 output**

```text
000000000000000000
000000000000000000
000000000000000000
000000000000000000
000800000000000000
008000800008000800
000320000000056000
000040000000070000
000808000000808000
000000000000000000
000000000000000000
000000000000000000
```
**Test input**

```text
000000000000000000
000000000000000000
000000000000000000
000000000000000000
000800800000000000
008000000000070000
000420000000056000
008030000000000000
000800000000000000
000000000000000000
000000000000000000
000000000000000000
```
**Test output**

```text
000000000000000000
000000000000000000
000000000000000000
000000000000000000
000800800000808000
008000000008070800
000420000000056000
008030000000000000
000800000000000000
000000000000000000
000000000000000000
000000000000000000
```
**Written solution**

Filter the source motif by local mirror symmetry across the y-axis and then draw only those mirrored-pair points in the target frame.

**Reference program**

```python
def solve_S22_H5(grid):
    out = copy_grid(grid)
    sf = find_frames(grid,(2,3,4))[0]
    tf = find_frames(grid,(5,6,7))[0]
    pts = extract_local_points(grid,sf,{8},radius=4)
    pset = set(uv for uv,col in pts)
    keep = [ (uv,col) for uv,col in pts if (-uv[0], uv[1]) in pset ]
    for uv,col in keep:
        r,c = gpos(tf["origin"], tf["vx"], tf["vy"], *uv)
        out[r][c]=col
    return out
```

## S22_H6 — Frame-Library Lookup
**Skills:** analogy, local motif keys, keyed value retrieval, multi-frame parsing

**Primitive note:** Each row supplies a key motif in a source frame and a value motif in a target frame. The query row asks which stored value belongs to its key.

**Scaffold:**

- Read the first two source rows as key motifs and the first two target rows as their values.
- Normalize the query key motif in the third source row.
- Find the matching stored key and copy its value motif into the third target frame.

**Train 1 input**

```text
000000000000000000000000
000000000000000089000000
000000000000000600000000
000230000000000570000000
000408000000000000000000
000080000000000000000000
000000000000000000000000
000000000000000000000000
000000000000000000000000
008008000000000000000000
000400000000000000000000
000230000000000568000000
000000000000008700000000
000000000000000090000000
000000000000000000000000
000000000000000000000000
000000000000000000000000
008000000000000000000000
080400000000000000000000
003200000000006500000000
000000000000000700000000
000000000000000000000000
000000000000000000000000
000000000000000000000000
000000000000000000000000
```
**Train 1 output**

```text
000000000000000000000000
000000000000000089000000
000000000000000600000000
000230000000000570000000
000408000000000000000000
000080000000000000000000
000000000000000000000000
000000000000000000000000
000000000000000000000000
008008000000000000000000
000400000000000000000000
000230000000000568000000
000000000000008700000000
000000000000000090000000
000000000000000000000000
000000000000000000000000
000000000000000000000000
008000000000000000000000
080400000000000000000000
003200000000006500000000
000000000000080700000000
000000000000090000000000
000000000000000000000000
000000000000000000000000
000000000000000000000000
```
**Train 2 input**

```text
000000000000000000000000
000000000000000000000000
000000000000000000000000
000230000000000570000000
000408000000000600000000
000080000000000089000000
000000000000000000000000
000000000000000000000000
000000000000000000000000
000000000000000000000000
000000000000008000000000
003200000000007500000000
000400000000090600000000
080080000000000800000000
000000000000000000000000
000000000000000000000000
000000000000000000000000
000008000000000000000000
000300000000000700000000
000240000000000560000000
000008000000000000000000
000000000000000000000000
000000000000000000000000
000000000000000000000000
000000000000000000000000
```
**Train 2 output**

```text
000000000000000000000000
000000000000000000000000
000000000000000000000000
000230000000000570000000
000408000000000600000000
000080000000000089000000
000000000000000000000000
000000000000000000000000
000000000000000000000000
000000000000000000000000
000000000000008000000000
003200000000007500000000
000400000000090600000000
080080000000000800000000
000000000000000000000000
000000000000000000000000
000000000000000000000000
000008000000000090000000
000300000000008700000000
000240000000000568000000
000008000000000000000000
000000000000000000000000
000000000000000000000000
000000000000000000000000
000000000000000000000000
```
**Test input**

```text
000000000000000000000000
008000000000000000000000
080400000000000000000000
003200000000000560000000
000000000000000708000000
000000000000000009000000
000000000000000000000000
000000000000000000000000
000000000000000000000000
008008000000000800000000
000400000000000609000000
000230000000000570000000
000000000000000080000000
000000000000000000000000
000000000000000000000000
000000000000000000000000
000000000000000000000000
000000000000000000000000
000008000000000000000000
000240000000006500000000
000300000000000700000000
000008000000000000000000
000000000000000000000000
000000000000000000000000
000000000000000000000000
```
**Test output**

```text
000000000000000000000000
008000000000000000000000
080400000000000000000000
003200000000000560000000
000000000000000708000000
000000000000000009000000
000000000000000000000000
000000000000000000000000
000000000000000000000000
008008000000000800000000
000400000000000609000000
000230000000000570000000
000000000000000080000000
000000000000000000000000
000000000000000000000000
000000000000000000000000
000000000000000000000000
000000000000000000000000
000008000000000000000000
000240000000086500000000
000300000000000780000000
000008000000009000000000
000000000000000000000000
000000000000000000000000
000000000000000000000000
```
**Written solution**

Build a small lookup table from the example rows: local source-key motif to local target-value motif. Then match the query key motif and replay the corresponding value motif in the blank query target.

**Reference program**

```python
def solve_S22_H6(grid):
    sfs = find_frames(grid,(2,3,4))
    tfs = find_frames(grid,(5,6,7))
    # pair source/target by reading order, query is last source, answer goes in last target
    assert len(sfs)==len(tfs)==3
    src_motifs = [canonical_offsets([uv for uv,col in extract_local_points(grid,sf,{8},radius=4)]) for sf in sfs]
    tgt_pts = [extract_local_points(grid,tf,{8,9},radius=4) for tf in tfs]
    # examples 0,1 map source->target
    mapping = {src_motifs[i]: tgt_pts[i] for i in range(2)}
    query_sig = src_motifs[2]
    value = mapping[query_sig]
    out = copy_grid(grid)
    qtf = tfs[2]
    for uv,col in value:
        r,c = gpos(qtf["origin"], qtf["vx"], qtf["vy"], *uv)
        out[r][c]=col
    return out
```

## S22_H7 — Which Candidate Is the Local 90° Rotation?
**Skills:** transformed matching, candidate selection, symbolic output

**Primitive note:** The correct candidate is not the raw source motif but the source motif after a specific local rotation.

**Scaffold:**

- Extract the source motif as local coordinates.
- Rotate that local pattern by 90°.
- Find which candidate frame already contains that rotated local pattern and mark it in the strip.

**Train 1 input**

```text
0000000000000000000000000
0000000000000000000000000
0000000000006800000000000
0000000000005700000000000
0000000000000080080000000
0000800000080000007080000
0002300000000000005600000
0004080000000000000800000
0080000000000880000000000
0000000000005600000000000
0000000000007000000000000
0000000000080000000000000
0000000000000000000000000
```
**Train 1 output**

```text
800
```
**Train 2 input**

```text
0000000000000000000000000
0000000000000800000000000
0000000000807000000000000
0000000000005600000000000
0000000000000080080000000
0800000000000000000000000
0032000000000000005600000
0004080000000800807000000
0080000000000000000800000
0000000000075000000000000
0000000000806000000000000
0000000000000800000000000
0000000000000000000000000
```
**Train 2 output**

```text
080
```
**Test input**

```text
0000000000000000000000000
0000000000000000000000000
0000000000080000000000000
0000000000005600000000000
0080000000807000000000000
0000800000000800007080000
0042000000000000065000000
0803000000000800080000000
0000000000080000000800000
0000000000005700000000000
0000000000806000000000000
0000000000000000000000000
0000000000000000000000000
```
**Test output**

```text
080
```
**Written solution**

Rotate the source motif in local coordinates and compare the result to each candidate motif after normalizing them to their own frames. Mark the candidate that matches the rotated local pattern.

**Reference program**

```python
def solve_S22_H7(grid):
    sf = find_frames(grid,(2,3,4))[0]
    candidates = find_frames(grid,(5,6,7))
    src_sig = canonical_offsets(transform_points([uv for uv,col in extract_local_points(grid,sf,{8},radius=4)], 'rot90'))
    idx=None
    for i,tf in enumerate(candidates):
        sig = canonical_offsets([uv for uv,col in extract_local_points(grid,tf,{8},radius=4)])
        if sig == src_sig:
            idx = i
            break
    out=[[0]*len(candidates)]
    out[0][idx]=8
    return out
```
