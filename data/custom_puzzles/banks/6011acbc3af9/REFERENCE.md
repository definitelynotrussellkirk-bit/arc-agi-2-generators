# ARC-style Puzzle Bank — 21 more puzzles (set 13)

This thirteenth bank pushes into a more feature-driven style of ARC design. Instead of relying mainly on paths, panels, or contact graphs, these puzzles ask the solver to compute stable object descriptors and then reason with them: hole counts, symmetry classes, border contact, bounding-box sizes, perimeter, area ranks, and small symbolic summaries built from those measurements.

This set introduces a new helper primitive:

```text
describe_components(grid, connectivity=4)
  Return the non-zero connected components together with feature records
  such as area, bbox size, holes, symmetry flags, perimeter, and
  whether the component touches the border.
```

The reference programs assume the shared helpers in `arc_puzzle_bank_21_set13_reference.py`.


## Index

### Easy

- **S13_E1** — Recolor the Holed Objects

- **S13_E2** — Keep Only Border Touchers

- **S13_E3** — Crop the Widest Object

- **S13_E4** — Recolor the Horizontally Symmetric Objects

- **S13_E5** — Crop the Only One-Hole Shape

- **S13_E6** — Crop the Smallest Asymmetric Object

- **S13_E7** — Recolor Tall-Than-Wide Objects


### Medium

- **S13_M1** — Header Chooses the Area Rank

- **S13_M2** — Match the Seed's Feature Triple

- **S13_M3** — Header Chooses the Symmetry Class

- **S13_M4** — Write the Area Strip

- **S13_M5** — Crop the Highest-Perimeter Object

- **S13_M6** — Match the Anchor's Border/Symmetry Pair

- **S13_M7** — Odd Panel by Hole Pattern


### Hard

- **S13_H1** — Dual Legend Chooses Holes and Symmetry

- **S13_H2** — Pairwise Feature-Match Matrix

- **S13_H3** — Feature Analogy Across Two Panels

- **S13_H4** — Header Chooses Rank Within a Symmetry Class

- **S13_H5** — Recolor Repeated Feature Classes

- **S13_H6** — Combine the Blue Hole Count with the Red Symmetry

- **S13_H7** — Crop the Lexicographic Feature Champion


# Easy


## S13_E1 — Recolor the Holed Objects

**Skills:** hole counting, same-size recolor, object features


**Primitive note:** Uses describe_components directly: select components whose feature record has holes > 0.


**Scaffold:**

- Split the non-zero cells into connected components.

- For each component, look inside its bounding box and count enclosed holes.

- Recolor exactly the components with at least one hole to cyan(8).

**Train 1 input**

```text
00000000000000
02220000333000
02020000333000
02220000000000
00000000000000
00000000066600
00400000060600
00400000066600
00440000006000
00000000000000
00000000000000
```
**Train 1 output**

```text
00000000000000
08880000333000
08080000333000
08880000000000
00000000000000
00000000088800
00400000080800
00400000088800
00440000008000
00000000000000
00000000000000
```

**Train 2 input**

```text
000000000000000
099990000000000
090090000020000
090090000222000
099990000020000
000000000000000
000000000000000
033300000444000
003000000404400
003000000444000
000000000000000
000000000000000
```
**Train 2 output**

```text
000000000000000
088880000000000
080080000020000
080080000222000
088880000020000
000000000000000
000000000000000
033300000888000
003000000808800
003000000888000
000000000000000
000000000000000
```
**Test input**

```text
0000000000000000
0077700000202000
0070700000202000
0077700000222000
0000000000000000
0000000000000000
0000000000000000
0333330000066000
0303030000066000
0333330000060000
0000000000000000
0000000000000000
```
**Test output**

```text
0000000000000000
0088800000202000
0080800000202000
0088800000222000
0000000000000000
0000000000000000
0000000000000000
0888880000066000
0808080000066000
0888880000060000
0000000000000000
0000000000000000
```
**Written solution:** Treat every colored object as a component and compute its basic features. The only objects that change are the ones with one or more enclosed holes, so recolor those whole components to cyan(8) and leave everything else unchanged.

**Reference program:**

```python
def solve_S13_E1(grid):
    return recolor_same_size(grid, lambda comp: comp["holes"] > 0, 8)
```


## S13_E2 — Keep Only Border Touchers

**Skills:** border detection, object filtering, same-size erase


**Primitive note:** Uses describe_components as a border-touch predicate: keep components with touches_border = True.


**Scaffold:**

- Find each connected component.

- Check whether any cell of that component touches the outer border of the grid.

- Keep only the border-touching components and erase all interior ones.

**Train 1 input**

```text
02220000000000
02220000440000
00000000440000
00000000000006
00003000000006
00003000000006
00003300000006
00000888000000
00000808000000
00000888000000
```
**Train 1 output**

```text
02220000000000
02220000000000
00000000000000
00000000000006
00000000000006
00000000000006
00000000000006
00000888000000
00000808000000
00000888000000
```

**Train 2 input**

```text
000000020000000
000000222000000
000000020090000
000000000099000
030300000000000
030300000000000
033300000000077
000000000000077
000000444000077
000000400000000
000000444000000
```
**Train 2 output**

```text
000000020000000
000000222000000
000000020000000
000000000000000
000000000000000
000000000000000
000000000000077
000000000000077
000000444000077
000000400000000
000000444000000
```
**Test input**

```text
2222000000000000
2002000000000000
2002000000000000
2222000000000044
0000003300000044
0000000330000040
0000000030000000
0000000000000000
0000000000000000
0000000000000000
0000000077770000
```
**Test output**

```text
2222000000000000
2002000000000000
2002000000000000
2222000000000044
0000000000000044
0000000000000040
0000000000000000
0000000000000000
0000000000000000
0000000000000000
0000000077770000
```
**Written solution:** The output keeps the objects that reach the outer frame of the board. Any component that stays strictly inside the canvas is removed; any component with at least one border cell survives unchanged.

**Reference program:**

```python
def solve_S13_E2(grid):
    return filter_same_size(grid, lambda comp: comp["touches_border"])
```


## S13_E3 — Crop the Widest Object

**Skills:** bounding boxes, width comparison, cropping


**Primitive note:** Uses describe_components to compare bbox widths, then crops the winning component.


**Scaffold:**

- Describe each component by its bounding box.

- Compare the box widths.

- Crop out the widest object and recolor the cropped shape to cyan(8).

**Train 1 input**

```text
00000000000000
02222000330000
00000000330000
00000000330000
00000000000000
00444000006000
00404000006000
00444000006600
00000000000000
```
**Train 1 output**

```text
8888
```

**Train 2 input**

```text
000000000000000
022200000303000
020220000303000
022200000333000
000000000000000
000000000000000
004400000060000
004400000666000
000000000060000
000000000000000
```
**Train 2 output**

```text
8880
8088
8880
```
**Test input**

```text
0000000000777700
0222220000000000
0202020000000000
0222220000000000
0000000000000000
0000000000000000
0033300000400000
0003000000440000
0003000000000000
0000000000000000
```
**Test output**

```text
88888
80808
88888
```
**Written solution:** Measure the width of every object by the width of its bounding box. The widest one is isolated, cropped to its own box, and recolored to cyan(8) in the output.

**Reference program:**

```python
def solve_S13_E3(grid):
    desc=describe_components(grid)
    target=max(desc, key=lambda comp: (comp["width"], comp["area"], -top_left(comp)[0], -top_left(comp)[1]))
    return crop_component(target, 8)
```


## S13_E4 — Recolor the Horizontally Symmetric Objects

**Skills:** symmetry detection, same-size recolor, component masks


**Primitive note:** Uses describe_components and the sym_h flag derived from each cropped component mask.


**Scaffold:**

- Crop each object to its own bounding box.

- Test whether the cropped mask is unchanged by a top-bottom flip.

- Recolor every horizontally symmetric object to cyan(8).

**Train 1 input**

```text
000000000000000
022200003030000
020000003030000
022200003330000
000000000000000
000000000000000
044400000600000
040400000600000
044400000660000
000000000000000
000000000000000
```
**Train 1 output**

```text
000000000000000
088800003030000
080000003030000
088800003330000
000000000000000
000000000000000
088800000600000
080800000600000
088800000660000
000000000000000
000000000000000
```

**Train 2 input**

```text
0000000000000000
0222000000333000
0202200000030000
0222000000030000
0000000000000000
0000000000000000
0000000000660000
0044400000066000
0044400000006000
0000000000000000
0000000000000000
```
**Train 2 output**

```text
0000000000000000
0888000000333000
0808800000030000
0888000000030000
0000000000000000
0000000000000000
0000000000660000
0088800000066000
0088800000006000
0000000000000000
0000000000000000
```
**Test input**

```text
0000000000000000
0777770000222000
0707070000200000
0777770000222000
0000000000000000
0000000000000000
0000000000000000
0303000000044000
0303000000044000
0333000000040000
0000000000000000
0000000000000000
```
**Test output**

```text
0000000000000000
0888880000888000
0808080000800000
0888880000888000
0000000000000000
0000000000000000
0000000000000000
0303000000044000
0303000000044000
0333000000040000
0000000000000000
0000000000000000
```
**Written solution:** Each object is checked for horizontal symmetry inside its own bounding box. Any object whose top half mirrors its bottom half is recolored to cyan(8), including shapes that are symmetric in both directions.

**Reference program:**

```python
def solve_S13_E4(grid):
    return recolor_same_size(grid, lambda comp: comp["sym_h"], 8)
```


## S13_E5 — Crop the Only One-Hole Shape

**Skills:** hole detection, unique target selection, cropping


**Primitive note:** Uses describe_components to find the unique component with holes == 1.


**Scaffold:**

- Find the connected components.

- Count holes for each one.

- The unique object with exactly one hole is cropped and recolored to cyan(8).

**Train 1 input**

```text
00000000000000
02220000303000
02020000303000
02220000333000
00000000000000
00000000000000
00400000006000
00400000066600
00440000006000
00000000000000
```
**Train 1 output**

```text
888
808
888
```

**Train 2 input**

```text
000000000000000
022200000000000
022200003330000
000000003033000
000000003330000
000000000000000
000000000000000
004400000066000
000440000066000
000040000000000
000000000000000
```
**Train 2 output**

```text
8880
8088
8880
```
**Test input**

```text
0000000000000000
0022200000330000
0002000000330000
0002000000300000
0000000000000000
0000000000000000
0444400000000000
0400400000666000
0400400000600000
0444400000666000
0000000000000000
0000000000000000
```
**Test output**

```text
8888
8008
8008
8888
```
**Written solution:** There is exactly one holed object in each example. Find the component whose bounding-box mask contains one enclosed hole, crop it to its own box, and paint that cropped version cyan(8).

**Reference program:**

```python
def solve_S13_E5(grid):
    desc=describe_components(grid)
    target=next(comp for comp in sorted(desc, key=top_left) if comp["holes"]==1)
    return crop_component(target, 8)
```


## S13_E6 — Crop the Smallest Asymmetric Object

**Skills:** symmetry class, area comparison, cropping


**Primitive note:** Uses describe_components to filter to sym_count == 0, then picks the minimum area.


**Scaffold:**

- Ignore the symmetric objects.

- Among the remaining asymmetric objects, compare their areas.

- Crop the smallest asymmetric object and recolor it to cyan(8).

**Train 1 input**

```text
00000000000000
02000000330000
02200000330000
00000000300000
00000000000000
00000000000000
04440000066600
04040000066600
04440000000000
00000000000000
```
**Train 1 output**

```text
80
88
```

**Train 2 input**

```text
000000000000000
020000003300000
020000000330000
022000000030000
000000000000000
000000000000000
000000000000000
004000000606000
044400000606000
004000000666000
000000000000000
```
**Train 2 output**

```text
80
80
88
```
**Test input**

```text
0000000000000000
0444000000200000
0404400000220000
0444000000000000
0000000000000000
0000000000000000
0000000000000000
0330000000666000
0033000000060000
0003000000060000
0000000000000000
0000000000000000
```
**Test output**

```text
80
88
```
**Written solution:** Only objects with no horizontal or vertical symmetry are considered. Among those asymmetric shapes, the smallest-area one is extracted, cropped to its bounding box, and recolored to cyan(8).

**Reference program:**

```python
def solve_S13_E6(grid):
    desc=[comp for comp in describe_components(grid) if comp["sym_count"]==0]
    target=min(desc, key=lambda comp: (comp["area"], comp["perimeter"], top_left(comp)))
    return crop_component(target, 8)
```


## S13_E7 — Recolor Tall-Than-Wide Objects

**Skills:** aspect ratio, bounding boxes, same-size recolor


**Primitive note:** Uses describe_components and compares height versus width for each component.


**Scaffold:**

- Compute each object’s bounding-box height and width.

- Identify the components whose height is greater than their width.

- Recolor those tall components to cyan(8).

**Train 1 input**

```text
000000000000000
020003300044440
020003300000000
020003300000000
020000000000000
000000000000000
000000000070000
006660000070000
006060000077000
006660000000000
000000000000000
```
**Train 1 output**

```text
000000000000000
080008800044440
080008800000000
080008800000000
080000000000000
000000000000000
000000000080000
006660000080000
006060000088000
006660000000000
000000000000000
```

**Train 2 input**

```text
0000000000000000
0222000033300000
0202000030330000
0222000033300000
0020000000000000
0000000000000000
0000000000000000
0404000000000000
0404000066600000
0444000066600000
0000000000000000
0000000000000000
```
**Train 2 output**

```text
0000000000000000
0888000033300000
0808000030330000
0888000033300000
0080000000000000
0000000000000000
0000000000000000
0404000000000000
0404000066600000
0444000066600000
0000000000000000
0000000000000000
```
**Test input**

```text
0000000000000000
0200000033300000
0200000003000000
0220000003000000
0000000000000000
0000000000000000
0400000000000000
0400000066666000
0400000060606000
0400000066666000
0000000000000000
0000000000000000
```
**Test output**

```text
0000000000000000
0800000033300000
0800000003000000
0880000003000000
0000000000000000
0000000000000000
0800000000000000
0800000066666000
0800000060606000
0800000066666000
0000000000000000
0000000000000000
```
**Written solution:** The changing objects are the tall ones: their bounding boxes are higher than they are wide. Recolor every such component to cyan(8) while keeping square and wide objects unchanged.

**Reference program:**

```python
def solve_S13_E7(grid):
    return recolor_same_size(grid, lambda comp: comp["height"] > comp["width"], 8)
```


# Medium


## S13_M1 — Header Chooses the Area Rank

**Skills:** header decoding, area ranking, cropping


**Primitive note:** Uses describe_components for area, with the top header row interpreted as a rank selector.


**Scaffold:**

- Read the top header row: the number of blue(1) cells is the rank k.

- Rank the body objects by area from largest to smallest.

- Crop the k-th largest object and recolor it to cyan(8).

**Train 1 input**

```text
110000000000000
000000000000000
022200003330000
020200003030000
022200003330000
002000000000000
000000000000000
000000000000000
044400000060000
044400000066000
000000000000000
000000000000000
```
**Train 1 output**

```text
888
808
888
```

**Train 2 input**

```text
0111000000000000
0000000000000000
0222200003330000
0200200003000000
0200200003330000
0222200000000000
0000000000000000
0000000000000000
0000000000000000
0444000000066000
0444000000066000
0000000000000000
0000000000000000
```
**Train 2 output**

```text
888
888
```
**Test input**

```text
00100000000000000
00000000000000000
02222200003330000
02020200003033000
02222200003330000
00000000000000000
00000000000000000
00000000000000000
00000000000000000
04040000000600000
04040000000600000
04440000000660000
00000000000000000
```
**Test output**

```text
88888
80808
88888
```
**Written solution:** The header gives a rank. Count the blue cells in the top row, sort the body objects by area descending, and extract the object at that rank. The output is the cropped target recolored to cyan(8).

**Reference program:**

```python
def solve_S13_M1(grid):
    k = sum(1 for v in grid[0] if v == 1)
    body = [row[:] for row in grid[1:]]
    desc=describe_components(body)
    desc=sorted(desc, key=lambda comp: (-comp["area"], top_left(comp)))
    target=desc[k-1]
    return crop_component(target, 8)
```


## S13_M2 — Match the Seed's Feature Triple

**Skills:** anchor object, feature matching, same-size recolor


**Primitive note:** Uses describe_components to compute a compact feature triple for the blue seed and the candidates.


**Scaffold:**

- Use the blue(1) object as the seed.

- Describe it by (area, holes, symmetry class).

- Recolor every non-seed object with the same feature triple to cyan(8).

**Train 1 input**

```text
0000000000000000
0111000000777000
0101000000707000
0111000000777000
0010000000070000
0000000000000000
0000000000000000
0333000000404000
0303000000404000
0333000000444000
0000000000000000
0000000000000000
```
**Train 1 output**

```text
0000000000000000
0111000000888000
0101000000808000
0111000000888000
0010000000080000
0000000000000000
0000000000000000
0333000000404000
0303000000404000
0333000000444000
0000000000000000
0000000000000000
```

**Train 2 input**

```text
0000000000000000
0111000000666000
0100000000600000
0111000000666000
0000000000000000
0000000000000000
0000000000000000
0303000000444000
0303000000404000
0333000000444000
0000000000000000
```
**Train 2 output**

```text
0000000000000000
0111000000888000
0100000000800000
0111000000888000
0000000000000000
0000000000000000
0000000000000000
0303000000444000
0303000000404000
0333000000444000
0000000000000000
```
**Test input**

```text
00000000000000000
01010000007070000
01010000007070000
01110000007770000
00000000000000000
00000000000000000
00000000000000000
03330000000000000
03030000000040000
03330000000444000
00300000000040000
00000000000000000
```
**Test output**

```text
00000000000000000
01010000008080000
01010000008080000
01110000008880000
00000000000000000
00000000000000000
00000000000000000
03330000000000000
03030000000040000
03330000000444000
00300000000040000
00000000000000000
```
**Written solution:** The blue object defines a feature signature: its area, its number of holes, and its symmetry class. Any other object with the same triple is recolored to cyan(8), while the seed and all mismatches stay unchanged.

**Reference program:**

```python
def solve_S13_M2(grid):
    desc=describe_components(grid)
    seed=next(comp for comp in desc if comp["color"]==1)
    feat=feature_triple(seed)
    out=copyg(grid)
    for comp in desc:
        if comp is seed:
            continue
        if feature_triple(comp)==feat:
            for r,c in comp["cells"]:
                out[r][c]=8
    return out
```


## S13_M3 — Header Chooses the Symmetry Class

**Skills:** header decoding, symmetry classification, cropping


**Primitive note:** Uses describe_components and the sym_h / sym_v flags to classify the body shapes.


**Scaffold:**

- Count the blue cells in the header row.

- Interpret 1 as vertical-only, 2 as horizontal-only, 3 as both axes, and 4 as no symmetry.

- Crop the body object in that symmetry class and recolor it to cyan(8).

**Train 1 input**

```text
100000000000000
000000000000000
020200003330000
020200003000000
022200003330000
000000000000000
000000000000000
044400000060000
040400000060000
044400000066000
000000000000000
```
**Train 1 output**

```text
808
808
888
```

**Train 2 input**

```text
0110000000000000
0000000000000000
0222000000333000
0202200000030000
0222000000030000
0000000000000000
0000000000000000
0000000000000000
0044000000660000
0044000000066000
0000000000006000
0000000000000000
```
**Train 2 output**

```text
8880
8088
8880
```
**Test input**

```text
0011100000000000
0000000000000000
0222000000303000
0222000000303000
0000000000333000
0000000000000000
0000000000000000
0000000000000000
0444000000066000
0400000000066000
0444000000060000
0000000000000000
```
**Test output**

```text
888
888
```
**Written solution:** The top header row encodes a symmetry class by its number of blue cells: 1 means vertical-only, 2 means horizontal-only, 3 means symmetric both ways, and 4 means asymmetric. Classify the body objects, pick the one in the requested class, and crop it as a cyan(8) shape.

**Reference program:**

```python
def solve_S13_M3(grid):
    code=sum(1 for v in grid[0] if v==1)
    wanted = {1:"v", 2:"h", 3:"both", 4:"none"}[code]
    body=[row[:] for row in grid[1:]]
    desc=describe_components(body)
    target=next(comp for comp in sorted(desc, key=top_left) if sym_class(comp)==wanted)
    return crop_component(target, 8)
```


## S13_M4 — Write the Area Strip

**Skills:** symbolic output, object ordering, area encoding


**Primitive note:** Uses describe_components for area and top-left ordering to build a symbolic row output.


**Scaffold:**

- Sort the objects from top-left to bottom-right by their bounding-box positions.

- Measure the area of each object.

- Write those areas as a single output row of color numbers.

**Train 1 input**

```text
0000000000000000
0200000033300000
0220000030300000
0000000033300000
0000000000000000
0000000000000000
0004000000606000
0044400000606000
0004000000666000
0000000000000000
```
**Train 1 output**

```text
3857
```

**Train 2 input**

```text
00000000000000000
02200000333000000
02200000303300000
00000000333000000
00000000000000000
00000000000000000
00000000000000000
04440000006660000
04440000006000000
00000000006660000
00000000000000000
```
**Train 2 output**

```text
4967
```
**Test input**

```text
000000000000000000
022000000033300000
022000000030300000
020000000033300000
000000000003000000
000000000000000000
000000000000000000
000000000000000000
044000000066600000
044000000060600000
044000000066600000
000000000000000000
```
**Test output**

```text
5968
```
**Written solution:** The output is no longer a picture of the input shapes. Instead, the objects are ordered by reading order, and each object contributes one number: its area. Those numbers are written left to right as a 1×n strip.

**Reference program:**

```python
def solve_S13_M4(grid):
    desc=sorted(describe_components(grid), key=top_left)
    return [[comp["area"] for comp in desc]]
```


## S13_M5 — Crop the Highest-Perimeter Object

**Skills:** perimeter counting, shape comparison, cropping


**Primitive note:** Uses describe_components and the perimeter feature computed from each component mask.


**Scaffold:**

- For each object, count exposed sides to get its perimeter.

- Find the component with the largest perimeter.

- Crop that object and recolor it to cyan(8).

**Train 1 input**

```text
0000000000000000
0222200000030000
0200200000333000
0200200000030000
0222200000000000
0000000000000000
0000000000000000
0000000000000000
0044000000600000
0044000000660000
0000000000000000
```
**Train 1 output**

```text
8888
8008
8008
8888
```

**Train 2 input**

```text
000000000000000
022200000333000
020000000333000
022200000000000
000000000000000
000000000000000
004400000060000
004400000666000
000000000060000
000000000000000
```
**Train 2 output**

```text
888
800
888
```
**Test input**

```text
00000000000000000
02222200000333000
02020200000303000
02222200000333000
00000000000000000
00000000000000000
00444000000666000
00444000000060000
00000000000060000
00000000000000000
```
**Test output**

```text
88888
80808
88888
```
**Written solution:** Every object is scored by perimeter, counting how many sides of its cells are exposed to background. The highest-perimeter component is extracted, cropped, and recolored to cyan(8).

**Reference program:**

```python
def solve_S13_M5(grid):
    desc=describe_components(grid)
    target=max(desc, key=lambda comp: (comp["perimeter"], comp["area"], -top_left(comp)[0], -top_left(comp)[1]))
    return crop_component(target, 8)
```


## S13_M6 — Match the Anchor's Border/Symmetry Pair

**Skills:** anchor reasoning, compound feature match, same-size recolor


**Primitive note:** Uses describe_components to compare a two-feature signature (touches_border, symmetry class) against the red anchor.


**Scaffold:**

- Use the red(2) object as the anchor.

- Read two features from it: whether it touches the border and which symmetry class it has.

- Recolor all non-anchor objects with the same feature pair to cyan(8).

**Train 1 input**

```text
0222000000000000
0200000000000000
0222000000000000
0000000000000000
0000000003330000
0000000003033000
0000000003330000
0000000000004040
0000000000004040
0777000000004440
0700000000000000
0777000000000000
```
**Train 1 output**

```text
0222000000000000
0200000000000000
0222000000000000
0000000000000000
0000000003330000
0000000003033000
0000000003330000
0000000000004040
0000000000004040
0888000000004440
0800000000000000
0888000000000000
```

**Train 2 input**

```text
00000000000000000
02220000007700000
02020000007700000
02220000000000000
00000000000000000
00000000600000000
00000000600000000
03330000660000000
03330000000004444
00000000000004004
00000000000004004
00000000000004444
```
**Train 2 output**

```text
00000000000000000
02220000008800000
02020000008800000
02220000000000000
00000000000000000
00000000600000000
00000000600000000
08880000660000000
08880000000004444
00000000000004004
00000000000004004
00000000000004444
```
**Test input**

```text
20000000000000000
20000000003300000
22000000003300000
00000000003000000
00000000000000000
00000000004440000
00000000004000000
00000666004440000
00000606000000000
77000666000000000
07700000000000000
00700000000000000
```
**Test output**

```text
20000000000000000
20000000003300000
22000000003300000
00000000003000000
00000000000000000
00000000004440000
00000000004000000
00000666004440000
00000606000000000
88000666000000000
08800000000000000
00800000000000000
```
**Written solution:** The red object specifies a compound predicate: border-touching status plus symmetry class. Every other component that matches that same pair is recolored to cyan(8); mismatches stay as they are.

**Reference program:**

```python
def solve_S13_M6(grid):
    desc=describe_components(grid)
    anchor=next(comp for comp in desc if comp["color"]==2)
    feat=(anchor["touches_border"], sym_class(anchor))
    out=copyg(grid)
    for comp in desc:
        if comp is anchor:
            continue
        if (comp["touches_border"], sym_class(comp))==feat:
            for r,c in comp["cells"]:
                out[r][c]=8
    return out
```


## S13_M7 — Odd Panel by Hole Pattern

**Skills:** panel splitting, hole counting, odd-one-out


**Primitive note:** Uses panel splitting plus describe_components to summarize each panel by its multiset of hole counts.


**Scaffold:**

- Split the grid into three panels using the full-height gray(5) separators.

- Within each panel, collect the multiset of hole counts of its objects.

- Mark the one panel whose hole-count pattern differs from the other two.

**Train 1 input**

```text
02220502020502220
02020502020502000
02220502220502220
00000500000500000
00000500000500000
00000503330500300
03000503030503330
03300503330500300
00000500000500000
```
**Train 1 output**

```text
008
```

**Train 2 input**

```text
02220500200502200
02020502220502200
02220500200500000
00000500000500000
00000500000503330
03330503330503030
03030503030503330
03330503330500300
00000500000500000
```
**Train 2 output**

```text
800
```
**Test input**

```text
02020502220502000
02020502000502000
02220502220502200
00000500000500000
00000500000500000
03330503300533300
03030503300530330
03330503000533300
00000500000500000
```
**Test output**

```text
080
```
**Written solution:** The gray separator columns divide the board into three independent panels. Two panels share the same multiset of hole counts across their objects, and one panel does not. The output is a 1×3 indicator row with cyan(8) under the odd panel.

**Reference program:**

```python
def solve_S13_M7(grid):
    panels,_=split_panels(grid, sep_color=5)
    sigs=[]
    for panel in panels:
        hs=sorted(comp["holes"] for comp in describe_components(panel))
        sigs.append(tuple(hs))
    counts=Counter(sigs)
    odd_index=next(i for i,s in enumerate(sigs) if counts[s]==1)
    out=[[0,0,0]]
    out[0][odd_index]=8
    return out
```


# Hard


## S13_H1 — Dual Legend Chooses Holes and Symmetry

**Skills:** two-row legend, feature conjunction, cropping


**Primitive note:** Uses describe_components as a feature table and intersects two legend constraints.


**Scaffold:**

- Count the blue cells in the first header row and subtract 1 to get the target hole count.

- Count the red cells in the second header row and decode the symmetry class: 1 vertical-only, 2 horizontal-only, 3 both, 4 none.

- Find the unique body object satisfying both feature constraints, then crop and recolor it.

**Train 1 input**

```text
1100000000000000
0200000000000000
0000000000000000
0222000000333000
0202000000303300
0222000000333000
0020000000000000
0000000000000000
0000000000000000
0444000000060000
0404000000060000
0444000000066000
0000000000000000
0000000000000000
```
**Train 1 output**

```text
888
808
888
080
```

**Train 2 input**

```text
1000000000000000
0222200000000000
0000000000000000
0220000000303000
0022000000303000
0002000000333000
0000000000000000
0000000000000000
0000000000000000
0444000000666000
0400000000606000
0444000000666000
0000000000000000
```
**Train 2 output**

```text
880
088
008
```
**Test input**

```text
111000000000000000
022200000000000000
000000000000000000
022222000033330000
020202000030030000
022222000030030000
000000000033330000
000000000000000000
000000000000000000
000000000000000000
044400000006660000
040400000006000000
044400000006660000
004000000000000000
```
**Test output**

```text
88888
80808
88888
```
**Written solution:** This puzzle combines two legends. The first header row gives the target number of holes by using one extra blue cell, so 1→0 holes, 2→1 hole, and 3→2 holes. The second header row chooses the symmetry class with the code 1 vertical-only, 2 horizontal-only, 3 both, 4 none. The body object matching both conditions is cropped and recolored to cyan(8).

**Reference program:**

```python
def solve_S13_H1(grid):
    holes_target = max(sum(1 for v in grid[0] if v==1)-1, 0)
    sym_target = {1:"v", 2:"h", 3:"both", 4:"none"}[sum(1 for v in grid[1] if v==2)]
    body=[row[:] for row in grid[2:]]
    desc=describe_components(body)
    target=next(comp for comp in sorted(desc, key=top_left) if comp["holes"]==holes_target and sym_class(comp)==sym_target)
    return crop_component(target, 8)
```


## S13_H2 — Pairwise Feature-Match Matrix

**Skills:** symbolic matrix output, pairwise comparison, feature classes


**Primitive note:** Uses describe_components to build pairwise symbolic relations between feature descriptions.


**Scaffold:**

- Order the objects by top-left position.

- Compare every pair of objects.

- Write a square matrix: diagonal 1, 8 for same symmetry class, 4 for same hole count only, and 0 otherwise.

**Train 1 input**

```text
00000000000000000
02220000003300000
02020000003300000
02220000000000000
00000000000000000
00000000000000000
00000000000000000
04440000000606000
04000000000606000
04440000000666000
00000000000000000
```
**Train 1 output**

```text
1800
8144
0414
0441
```

**Train 2 input**

```text
0000000000000000
0222000000333000
0202000000303300
0222000000333000
0020000000000000
0000000000000000
0000004400000000
0000004400000000
0000004000000000
0000000000000000
```
**Train 2 output**

```text
140
410
001
```
**Test input**

```text
00000000000000000
02220000003333000
02220000003003000
00000000003003000
00000000003333000
00000000000000000
00000000000000000
04440000006600000
00400000000660000
00400000000060000
00000000000000000
```
**Test output**

```text
1844
8100
4014
4041
```
**Written solution:** The output is a comparison matrix over the ordered objects. Each row-column pair reports a relation: identical object index on the diagonal, same symmetry class as 8, same hole count (but different symmetry class) as 4, and 0 when neither relation holds.

**Reference program:**

```python
def solve_S13_H2(grid):
    desc=sorted(describe_components(grid), key=top_left)
    n=len(desc)
    out=blank(n,n,0)
    for i in range(n):
        out[i][i]=1
    for i,a in enumerate(desc):
        for j,b in enumerate(desc):
            if i==j:
                continue
            if sym_class(a)==sym_class(b):
                out[i][j]=8
            elif a["holes"]==b["holes"]:
                out[i][j]=4
    return out
```


## S13_H3 — Feature Analogy Across Two Panels

**Skills:** panel analogy, anchor transfer, cropping


**Primitive note:** Uses describe_components on both panels and matches the right-panel candidates to the red reference feature triple.


**Scaffold:**

- Use the red(2) object in the left panel as the reference.

- Describe it by (area, holes, symmetry class).

- In the right panel, find the object with the same feature triple and crop it.

**Train 1 input**

```text
0000000500000000
0222000533304440
0202200530304044
0222000533304440
0000000500000000
0000000500000000
0000000500000777
0033000566600707
0033000560000777
0000000566600070
0000000500000000
```
**Train 1 output**

```text
8880
8088
8880
```

**Train 2 input**

```text
0000000500000000
0202000544400666
0202000540000606
0222000544400666
0000000500000000
0000000500000000
0000000570700800
0003300570700800
0003300577700880
0000000500000000
```
**Train 2 output**

```text
808
808
888
```
**Test input**

```text
0000000500000000
0220000544000060
0220000504400666
0200000500400060
0000000500000000
0000000500000000
0033300577700888
0030300507000800
0033300507000888
0000000500000000
```
**Test output**

```text
880
088
008
```
**Written solution:** The left panel provides a reference object, highlighted in red. Its feature triple is transferred across the separator into the right panel, where the matching candidate is extracted, cropped, and recolored to cyan(8).

**Reference program:**

```python
def solve_S13_H3(grid):
    panels,_ = split_panels(grid, sep_color=5)
    ref, cand = panels[0], panels[1]
    ref_desc=describe_components(ref)
    target_feat = feature_triple(next(comp for comp in ref_desc if comp["color"]==2))
    cand_desc=describe_components(cand)
    target=next(comp for comp in sorted(cand_desc, key=top_left) if feature_triple(comp)==target_feat)
    return crop_component(target, 8)
```


## S13_H4 — Header Chooses Rank Within a Symmetry Class

**Skills:** two-stage filtering, ranking, cropping


**Primitive note:** Uses describe_components twice: once for symmetry-class filtering, then for area ranking inside that class.


**Scaffold:**

- Count the blue cells in the first header row and decode the symmetry class: 1 vertical-only, 2 horizontal-only, 3 both, 4 none.

- Count the red cells in the second header row to get the rank k.

- Among objects in the chosen class, sort by area descending and crop the k-th one.

**Train 1 input**

```text
10000000000000000
02200000000000000
00000000000000000
02220000003030000
02020000003030000
02220000003330000
00200000000000000
00000000000000000
00000000000000000
00000000000000000
04440000006660000
00400000006000000
00400000006660000
00000000000000000
```
**Train 1 output**

```text
808
808
888
```

**Train 2 input**

```text
111000000000000000
020000000000000000
000000000000000000
022220000033300000
020020000030300000
020020000033300000
022220000000000000
000000000000000000
000000000000000000
000000000000000000
044400000006000000
044400000006000000
000000000006600000
000000000000000000
```
**Train 2 output**

```text
8888
8008
8008
8888
```
**Test input**

```text
1111000000000000
0220000000000000
0000000000000000
0220000000300000
0022000000300000
0002000000330000
0000000000000000
0000000000000000
0000000000000000
0400000000666000
0440000000606000
0000000000666000
0000000000000000
```
**Test output**

```text
80
80
88
```
**Written solution:** The first header row names a symmetry class using the code 1 vertical-only, 2 horizontal-only, 3 both, 4 none. After filtering the body objects to that class, the second header row gives the area rank to take. The selected object is then cropped and recolored to cyan(8).

**Reference program:**

```python
def solve_S13_H4(grid):
    sym_target = {1:"v", 2:"h", 3:"both", 4:"none"}[sum(1 for v in grid[0] if v==1)]
    k = sum(1 for v in grid[1] if v==2)
    body=[row[:] for row in grid[2:]]
    desc=[comp for comp in describe_components(body) if sym_class(comp)==sym_target]
    desc=sorted(desc, key=lambda comp: (-comp["area"], top_left(comp)))
    target=desc[k-1]
    return crop_component(target, 8)
```


## S13_H5 — Recolor Repeated Feature Classes

**Skills:** feature grouping, equivalence classes, same-size recolor


**Primitive note:** Uses describe_components to build feature-equivalence classes and recolor the repeated ones.


**Scaffold:**

- Compute a feature triple for every object: (area, holes, symmetry class).

- Group the objects by that triple.

- Recolor every object belonging to a feature class that appears more than once.

**Train 1 input**

```text
000000000000000000
022200000033300000
020000000030000000
022200000033300000
000000000000000000
000000700000000000
000000700000000000
000000770000000000
044400000066600000
040400000060600000
044400000066600000
000000000000000000
```
**Train 1 output**

```text
000000000000000000
088800000088800000
080000000080000000
088800000088800000
000000000000000000
000000700000000000
000000700000000000
000000770000000000
088800000088800000
080800000080800000
088800000088800000
000000000000000000
```

**Train 2 input**

```text
000000000000000000
022000000033000000
022000000003300000
020000000000300000
000000000000000000
000000777000000000
000000707000000000
000000777000000000
040400000060600000
040400000060600000
044400000066600000
000000000000000000
```
**Train 2 output**

```text
000000000000000000
088000000088000000
088000000008800000
080000000000800000
000000000000000000
000000777000000000
000000707000000000
000000777000000000
080800000080800000
080800000080800000
088800000088800000
000000000000000000
```
**Test input**

```text
000000000000000000
022200000033000000
022200000033000000
000000000033000000
000000000000000000
000000700000000000
000000770000000000
000000000066660000
044000000060060000
044000000060060000
000000000066660000
000000000000000000
```
**Test output**

```text
000000000000000000
088800000088000000
088800000088000000
000000000088000000
000000000000000000
000000700000000000
000000770000000000
000000000066660000
044000000060060000
044000000060060000
000000000066660000
000000000000000000
```
**Written solution:** The objects are grouped by feature identity rather than by color or exact outline. Any feature triple that appears at least twice is considered repeated, and every component in such a repeated class is recolored to cyan(8).

**Reference program:**

```python
def solve_S13_H5(grid):
    desc=describe_components(grid)
    counts=Counter(feature_triple(comp) for comp in desc)
    out=copyg(grid)
    for comp in desc:
        if counts[feature_triple(comp)] > 1:
            for r,c in comp["cells"]:
                out[r][c]=8
    return out
```


## S13_H6 — Combine the Blue Hole Count with the Red Symmetry

**Skills:** two anchors, feature composition, cropping


**Primitive note:** Uses describe_components to combine one feature from the blue anchor with another from the red anchor.


**Scaffold:**

- Read the blue(1) anchor to get a hole count.

- Read the red(2) anchor to get a symmetry class.

- Find the non-anchor object satisfying both features, then crop and recolor it.

**Train 1 input**

```text
000000000000000000
011100000022200000
010100000020000000
011100000022200000
000000000000000000
000000400000000000
000000400000000000
000000440000000000
077700000033300000
070770000030300000
077700000033300000
000000000000000000
```
**Train 1 output**

```text
8880
8088
8880
```

**Train 2 input**

```text
000000000000000000
011000000020200000
011000000020200000
000000000022200000
000000000000000000
000000444000000000
000000404000000000
000000444000000000
077700000033300000
007000000030000000
007000000033300000
000000000000000000
```
**Train 2 output**

```text
888
080
080
```
**Test input**

```text
0000000000000000000
0111110000022200000
0101010000022200000
0111110000000000000
0000000000000000000
0000000000000000000
0000000000000000000
0000004440033330000
0777774040030030000
0707074440030030000
0777770400033330000
0000000000000000000
```
**Test output**

```text
88888
80808
88888
```
**Written solution:** Two anchors contribute different parts of the target description. The blue anchor determines the required number of holes and the red anchor determines the required symmetry class. The body object matching both is cropped and recolored to cyan(8).

**Reference program:**

```python
def solve_S13_H6(grid):
    desc=describe_components(grid)
    blue=next(comp for comp in desc if comp["color"]==1)
    red=next(comp for comp in desc if comp["color"]==2)
    holes_target = blue["holes"]
    sym_target = sym_class(red)
    candidates=[comp for comp in desc if comp["color"] not in (1,2)]
    target=next(comp for comp in sorted(candidates, key=top_left) if comp["holes"]==holes_target and sym_class(comp)==sym_target)
    return crop_component(target, 8)
```


## S13_H7 — Crop the Lexicographic Feature Champion

**Skills:** multi-feature ordering, lexicographic comparison, cropping


**Primitive note:** Uses describe_components to rank objects by the tuple (holes, sym_count, area).


**Scaffold:**

- Compare objects first by number of holes, then by symmetry-count, then by area.

- Pick the lexicographically largest feature tuple.

- Crop that champion object and recolor it to cyan(8).

**Train 1 input**

```text
000000000000000000
022222000003333000
020202000003003000
022222000003003000
000000000003333000
000000000000000000
000000000000000000
000000000000000000
044400000006060000
040400000006060000
044400000006660000
004000000000000000
```
**Train 1 output**

```text
88888
80808
88888
```

**Train 2 input**

```text
00000000000000000
02222000003330000
02002000003030000
02002000003330000
02222000000000000
00000000000000000
00000000000000000
00000000000000000
04440000006660000
04044000006000000
04440000006660000
00000000000000000
```
**Train 2 output**

```text
8888
8008
8008
8888
```
**Test input**

```text
0000000000000000
0222000000333000
0202000000303000
0222000000333000
0000000000030000
0000000000000000
0000000000000000
0444000000600000
0040000000600000
0040000000660000
0000000000000000
```
**Test output**

```text
888
808
888
```
**Written solution:** Each object is ranked by a three-level priority: more holes is better, then more axes of symmetry, then larger area. The winning component under that lexicographic order is extracted, cropped, and recolored to cyan(8).

**Reference program:**

```python
def solve_S13_H7(grid):
    desc=describe_components(grid)
    target=max(desc, key=lambda comp: (comp["holes"], comp["sym_count"], comp["area"], -top_left(comp)[0], -top_left(comp)[1]))
    return crop_component(target, 8)
```
