# ARC-style Puzzle Bank — 21 more puzzles (set 12)

This twelfth bank is organized into 7 easy, 7 medium, and 7 hard puzzles. It leans much harder into object relations than the recent contour and beam sets: which objects touch, how those contacts form a graph, which node is a leaf or a bridge, how far an object is from a seed, and how a whole cluster can be summarized into a compact symbolic output.

This set introduces a new helper primitive:

```text
component_graph(grid, connectivity=4, touch=4)
  Return the non-zero connected components together with an adjacency map
  telling which components touch by edge.
```

The reference programs assume the shared helpers in `arc_puzzle_bank_21_set12_reference.py`.


## Index

### Easy

- **S12_E1** — Recolor the Anchor's Neighbors

- **S12_E2** — Keep Only Isolated Objects

- **S12_E3** — Mark the Leaf Components

- **S12_E4** — Crop the Shape Touching the Marker

- **S12_E5** — Show Only Contact Cells

- **S12_E6** — Recolor by Contact Degree

- **S12_E7** — Keep the Largest Neighbor of Red


### Medium

- **S12_M1** — Crop the Highest-Degree Component

- **S12_M2** — Extract the Seed's Contact Cluster

- **S12_M3** — Header Chooses the Degree

- **S12_M4** — Highlight the Marker-to-Marker Path

- **S12_M5** — Select Components Touching Two Colors

- **S12_M6** — Crop the Most Colorful Cluster

- **S12_M7** — Highlight Distance-Two Components


### Hard

- **S12_H1** — Find the Articulation Component

- **S12_H2** — Odd Panel by Degree Pattern

- **S12_H3** — Dual Legend: Cluster Size and Degree

- **S12_H4** — Color by Graph Distance from the Seed

- **S12_H5** — Header Chooses the Articulation Count

- **S12_H6** — Degree Sequence of the Largest Cluster

- **S12_H7** — Adjacency Matrix of the Seed Cluster



# Easy

## S12_E1 — Recolor the Anchor's Neighbors

**Skills:** component adjacency, same-size recolor, anchor objects


**Primitive note:** Uses component_graph directly: find the blue(1) anchor component and recolor every adjacent component.


**Scaffold:**

- Find the non-zero connected components.

- Build the contact graph of components that touch by an edge.

- Starting from the blue(1) anchor, recolor all neighboring components to yellow(4).

**Train 1 input**

```text
00000000000
00000008880
00133300000
00600000000
00600000000
00600000000
00000007700
00000007700
00000000000
```
**Train 1 output**

```text
00000000000
00000008880
00144400000
00400000000
00400000000
00400000000
00000007700
00000007700
00000000000
```
**Train 2 input**

```text
000000000000
077700000000
077700000000
000000000000
000001330000
000066630000
000000000000
000000000800
000000000800
000000000800
```
**Train 2 output**

```text
000000000000
077700000000
077700000000
000000000000
000001440000
000044440000
000000000000
000000000800
000000000800
000000000800
```
**Test input**

```text
0000000000000
0770000000000
0770040000000
0000040000000
0000040000000
0000013000000
0000003000000
0000003308880
0000000008880
0000000000000
```
**Test output**

```text
0000000000000
0770000000000
0770040000000
0000040000000
0000040000000
0000014000000
0000004000000
0000004408880
0000000008880
0000000000000
```
**Written solution:** Treat each colored object as one component. Find the blue(1) anchor object, then look at the component graph to see which other objects touch it by edge. Those neighbors are recolored to yellow(4), while the anchor and all non-neighbors stay as they were.

**Reference program:**

```python
def solve_S12_E1(grid):
    comps, adj = component_graph(grid)
    out = copyg(grid)
    for i, comp in enumerate(comps):
        if comp["color"] == 1:
            for j in adj[i]:
                for r, c in comps[j]["cells"]:
                    out[r][c] = 4
    return out
```

## S12_E2 — Keep Only Isolated Objects

**Skills:** component graph, filtering, same-size erase


**Primitive note:** Uses component_graph as a degree filter: keep exactly the components of degree 0.


**Scaffold:**

- Split the input into connected non-zero components.

- For each component, count how many other components it touches.

- Keep only the components with no contacts at all.

**Train 1 input**

```text
00000000000
02230000400
02230000440
00030000000
00000000000
07800000000
00000066600
00000000000
00000000000
```
**Train 1 output**

```text
00000000000
00000000400
00000000440
00000000000
00000000000
00000000000
00000066600
00000000000
00000000000
```
**Train 2 input**

```text
000000000000
022230000000
022230000000
000030000000
000000007880
000000000880
044006000000
044006000000
000006600000
000000000000
```
**Train 2 output**

```text
000000000000
000000000000
000000000000
000000000000
000000000000
000000000000
044006000000
044006000000
000006600000
000000000000
```
**Test input**

```text
0000000000000
0022220000000
0000030000000
0000030000900
0000030000900
0000000000900
0440000066000
0440078006600
0000000000000
0000000000000
```
**Test output**

```text
0000000000000
0000000000000
0000000000000
0000000000900
0000000000900
0000000000900
0440000066000
0440000006600
0000000000000
0000000000000
```
**Written solution:** Build the contact graph of the objects. Any object with at least one neighbor is removed. Only degree-0 components, the isolated ones, remain in their original colors on a black background.

**Reference program:**

```python
def solve_S12_E2(grid):
    h, w = dims(grid)
    comps, adj = component_graph(grid)
    out = blank(h, w, 0)
    for i, comp in enumerate(comps):
        if len(adj[i]) == 0:
            for r,c in comp["cells"]:
                out[r][c] = comp["color"]
    return out
```

## S12_E3 — Mark the Leaf Components

**Skills:** graph degree, endpoint detection, same-size recolor


**Primitive note:** Uses component_graph degrees: components of degree 1 are the leaves.


**Scaffold:**

- Turn the objects into graph nodes using edge-touching as adjacency.

- Compute each object's degree.

- Recolor the degree-1 objects to cyan(8).

**Train 1 input**

```text
00000000000
00000000000
00003000000
00042200000
00002260000
00000000000
07770000000
00000000000
00000000000
```
**Train 1 output**

```text
00000000000
00000000000
00008000000
00082200000
00002280000
00000000000
07770000000
00000000000
00000000000
```
**Train 2 input**

```text
000000000000
000000000000
022334460000
022334466000
000000000000
000000000070
000000000070
000000000070
```
**Train 2 output**

```text
000000000000
000000000000
088334480000
088334488000
000000000000
000000000070
000000000070
000000000070
```
**Test input**

```text
000000000000
000000000880
000000000880
000030000000
000422600000
000027000000
000000000000
000000000000
000000000000
000000000000
```
**Test output**

```text
000000000000
000000000880
000000000880
000080000000
000822800000
000028000000
000000000000
000000000000
000000000000
000000000000
```
**Written solution:** The objects form a contact graph. The leaf components are exactly the ones touching one other component. Recolor every degree-1 component to cyan(8) and leave the rest unchanged.

**Reference program:**

```python
def solve_S12_E3(grid):
    comps, adj = component_graph(grid)
    out = copyg(grid)
    for i, comp in enumerate(comps):
        if len(adj[i]) == 1:
            for r,c in comp["cells"]:
                out[r][c] = 8
    return out
```

## S12_E4 — Crop the Shape Touching the Marker

**Skills:** marker selection, adjacency, cropping


**Primitive note:** Uses component_graph for one-step lookup from a marker to its touched shape.


**Scaffold:**

- Find the special blue(1) marker component.

- Find the unique non-zero component that touches it.

- Crop that component to its bounding box and recolor it to cyan(8).

**Train 1 input**

```text
00000000000
00000000660
00000000660
00140000000
00040000000
00044000777
00000000000
00000000000
```
**Train 1 output**

```text
80
80
88
```
**Train 2 input**

```text
000000000000
066600000000
066600000000
000000000000
000000003000
000000133300
070000000000
070000000000
070000000000
```
**Train 2 output**

```text
080
888
```
**Test input**

```text
0000000000000
0000000000000
0000000014400
0000000000440
0000770000000
0600770000000
0660000000000
0000000000000
```
**Test output**

```text
880
088
```
**Written solution:** Use the marker only to identify the target. The blue(1) marker touches exactly one real shape. Select that touched component, crop tightly around it, and recolor all of its cells to cyan(8).

**Reference program:**

```python
def solve_S12_E4(grid):
    comps, adj = component_graph(grid)
    marker = next(i for i, comp in enumerate(comps) if comp["color"] == 1)
    target = sorted(adj[marker], key=lambda j: (len(comps[j]["cells"]), top_left(comps[j])))[0]
    return extract_union_grid(grid, comps, [target], recolor=8)
```

## S12_E5 — Show Only Contact Cells

**Skills:** local contact detection, boundary reasoning, same-size output


**Primitive note:** This one uses the lower-level contact relation: mark any non-zero cell that is edge-adjacent to a different non-zero color.


**Scaffold:**

- Scan every non-zero cell.

- Ask whether one of its four neighbors has a different non-zero color.

- If so, mark that cell in the output; otherwise leave it black.

**Train 1 input**

```text
000000000000
022233000000
022233000000
000033000000
000000007000
000000006600
000000006600
000000000000
```
**Train 1 output**

```text
000000000000
000880000000
000880000000
000000000000
000000008000
000000008000
000000000000
000000000000
```
**Train 2 input**

```text
000000000000
000000000000
002222000000
000003300000
000003300000
000000000000
046000000000
046600000000
040000000000
```
**Train 2 output**

```text
000000000000
000000000000
000008000000
000008000000
000000000000
000000000000
088000000000
088000000000
000000000000
```
**Test input**

```text
0000000000000
0022230000000
0022230000000
0022230000000
0000000006000
0000000004440
0000000004440
0000000000000
0000000000000
```
**Test output**

```text
0000000000000
0000880000000
0000880000000
0000880000000
0000000008000
0000000008000
0000000000000
0000000000000
0000000000000
```
**Written solution:** A cell is kept only if it lies on an interface between two differently colored objects. So the output is a blank grid with cyan(8) only on the cells that touch a different non-zero color across an edge.

**Reference program:**

```python
def solve_S12_E5(grid):
    h, w = dims(grid)
    out = blank(h, w, 0)
    for r,c in touch_cells(grid):
        out[r][c] = 8
    return out
```

## S12_E6 — Recolor by Contact Degree

**Skills:** graph degree, global recolor, component abstraction


**Primitive note:** Uses component_graph directly, then maps each degree to a fixed output color.


**Scaffold:**

- Build the component graph.

- Compute each component's degree.

- Replace each whole component by the color assigned to its degree.

**Train 1 input**

```text
000000000000
000000000000
022334000000
022334400000
000000000000
000000000770
000000000770
000000000000
```
**Train 1 output**

```text
000000000000
000000000000
044664000000
044664400000
000000000000
000000000330
000000000330
000000000000
```
**Train 2 input**

```text
0000000000000
0000000000800
0000000000800
0000030000800
0000422600000
0000022000000
0000000000000
0000000000000
0000000000000
```
**Train 2 output**

```text
0000000000000
0000000000300
0000000000300
0000040000300
0000488400000
0000088000000
0000000000000
0000000000000
0000000000000
```
**Test input**

```text
0000000000000
0000600000000
0022334400000
0022334400000
0000000000000
0000000000000
0000000000000
0000000000700
0000000000770
0000000000000
```
**Test output**

```text
0000000000000
0000400000000
0044884400000
0044884400000
0000000000000
0000000000000
0000000000000
0000000000300
0000000000330
0000000000000
```
**Written solution:** Ignore the original colors once the objects have been identified. Compute each component's contact degree and recolor the whole component by the fixed map: degree 0 -> green(3), degree 1 -> yellow(4), degree 2 -> magenta(6), degree 3 or more -> cyan(8).

**Reference program:**

```python
def solve_S12_E6(grid):
    h, w = dims(grid)
    comps, adj = component_graph(grid)
    out = blank(h, w, 0)
    mapping = {0:3, 1:4, 2:6}
    for i, comp in enumerate(comps):
        color = mapping.get(len(adj[i]), 8)
        for r,c in comp["cells"]:
            out[r][c] = color
    return out
```

## S12_E7 — Keep the Largest Neighbor of Red

**Skills:** adjacency from anchor, area comparison, same-size masking


**Primitive note:** Uses component_graph to get the red(2) anchor's neighbors, then compares their areas.


**Scaffold:**

- Find the red(2) anchor component.

- Look only at the components that touch it.

- Choose the one with the largest area and keep only that one.

**Train 1 input**

```text
0000000000000
0770000000000
0770300000000
0000300000000
0000324440000
0000064440000
0000000000000
0000000000000
0000000000000
```
**Train 1 output**

```text
0000000000000
0000000000000
0000000000000
0000000000000
0000008880000
0000008880000
0000000000000
0000000000000
0000000000000
```
**Train 2 input**

```text
0000000000000
0000000000600
0000000000600
0000000000600
0003022444000
0003322444000
0000000444000
0000000000000
0000000000000
0000000000000
```
**Train 2 output**

```text
0000000000000
0000000000000
0000000000000
0000000000000
0000000888000
0000000888000
0000000888000
0000000000000
0000000000000
0000000000000
```
**Test input**

```text
00000000000000
07770000000000
07770000000000
00000300000000
00000300000000
00000624400000
00000604400000
00000660000000
00000000000000
00000000000000
```
**Test output**

```text
00000000000000
00000000000000
00000000000000
00000000000000
00000000000000
00000800000000
00000800000000
00000880000000
00000000000000
00000000000000
```
**Written solution:** Start from the red(2) anchor and inspect its neighboring components in the contact graph. Compare their sizes by cell count, choose the largest, and draw only that component on a black canvas, recolored to cyan(8).

**Reference program:**

```python
def solve_S12_E7(grid):
    h, w = dims(grid)
    comps, adj = component_graph(grid)
    red = next(i for i, comp in enumerate(comps) if comp["color"] == 2)
    best = max(adj[red], key=lambda j: (len(comps[j]["cells"]), -top_left(comps[j])[0], -top_left(comps[j])[1]))
    out = blank(h, w, 0)
    for r,c in comps[best]["cells"]:
        out[r][c] = 8
    return out
```


# Medium

## S12_M1 — Crop the Highest-Degree Component

**Skills:** graph degree ranking, selection, cropped output


**Primitive note:** Uses component_graph and selects the node with maximum degree.


**Scaffold:**

- Construct the component graph.

- Find the component with the highest contact degree.

- Crop that component to its bounding box and recolor it to cyan(8).

**Train 1 input**

```text
00000000000
00000000000
00003000000
00042200000
00002260000
00000000000
00000000770
00000000770
00000000000
```
**Train 1 output**

```text
88
88
```
**Train 2 input**

```text
000000000000
088800000000
000000000000
000003000000
000042000000
000002066000
000002266000
000000000000
000000000000
000000000000
```
**Train 2 output**

```text
80
80
88
```
**Test input**

```text
0000000000000
0000000000000
0000000000000
0000003330000
0000422260000
0000422260000
0000407060000
0000000000000
0000000000000
0000000000000
```
**Test output**

```text
888
888
```
**Written solution:** Treat each object as a graph node and count how many neighbors it touches. The target is the unique highest-degree node. Extract just that component, crop tightly around it, and recolor it to cyan(8).

**Reference program:**

```python
def solve_S12_M1(grid):
    comps, adj = component_graph(grid)
    best = max(range(len(comps)), key=lambda i: (len(adj[i]), len(comps[i]["cells"]), tuple(-x for x in top_left(comps[i]))))
    return extract_union_grid(grid, comps, [best], recolor=8)
```

## S12_M2 — Extract the Seed's Contact Cluster

**Skills:** graph connected components, seeded selection, cropped union


**Primitive note:** Uses component_graph plus graph connected components.


**Scaffold:**

- Locate the seed component colored blue(1).

- In the component graph, find the whole connected cluster containing that seed.

- Output the union of that cluster, cropped and recolored to cyan(8).

**Train 1 input**

```text
000000000000
000000006670
000000006600
001330000000
000334000000
000004400000
000000000000
000000000000
000000000000
```
**Train 1 output**

```text
88800
08880
00088
```
**Train 2 input**

```text
0000000000000
0000000007000
0000000007000
0004000007000
0113300008800
0113360008800
0000000000000
0000000000000
0000000000000
0000000000000
```
**Train 2 output**

```text
00800
88880
88888
```
**Test input**

```text
0000000000000
0000000000000
0013300000000
0003344600000
0000044660000
0000000000000
0000000000000
0778000000000
0770000000000
0000000000000
```
**Test output**

```text
8880000
0888880
0008888
```
**Written solution:** The blue(1) component identifies which graph cluster to keep. After building the contact graph, take every component in the same connected component as the seed. Preserve their relative positions, crop the union tightly, and recolor the whole cluster to cyan(8).

**Reference program:**

```python
def solve_S12_M2(grid):
    comps, adj = component_graph(grid)
    seed = next(i for i, comp in enumerate(comps) if comp["color"] == 1)
    cluster = next(cl for cl in graph_clusters(adj) if seed in cl)
    return extract_union_grid(grid, comps, cluster, recolor=8)
```

## S12_M3 — Header Chooses the Degree

**Skills:** header decoding, graph degree filtering, same-size masking


**Primitive note:** Uses the number of blue(1) cells in the header row as the target degree.


**Scaffold:**

- Read the top row and count the blue(1) header cells.

- Ignore the header when building the body component graph.

- Keep exactly the components whose degree equals the header count.

**Train 1 input**

```text
11000000000
00000000000
00000000000
02233400000
02233440000
00000000000
00000000770
00000000770
```
**Train 1 output**

```text
00000000000
00000000000
00000000000
00088000000
00088000000
00000000000
00000000000
00000000000
```
**Train 2 input**

```text
101000000000
000000000000
000000000000
022334400000
022334400000
000000000000
000000000600
000000000600
000000000600
```
**Train 2 output**

```text
000000000000
000000000000
000000000000
000880000000
000880000000
000000000000
000000000000
000000000000
000000000000
```
**Test input**

```text
111000000000
000000000000
000000000000
000030000000
000422000000
000022600000
000000000000
000000000770
000000000770
```
**Test output**

```text
000000000000
000000000000
000000000000
000000000000
000088000000
000088000000
000000000000
000000000000
000000000000
```
**Written solution:** The top row is a legend: the count of blue(1) cells gives the required graph degree. In the body below, build the contact graph and mark every component whose degree matches that number. The output is same-size, with those matching components in cyan(8) and everything else black.

**Reference program:**

```python
def solve_S12_M3(grid):
    h, w = dims(grid)
    k = sum(1 for v in grid[0] if v == 1)
    body = [row[:] for row in grid[1:]]
    comps, adj = component_graph(body)
    out = blank(h, w, 0)
    for i, comp in enumerate(comps):
        if len(adj[i]) == k:
            for r,c in comp["cells"]:
                out[r+1][c] = 8
    return out
```

## S12_M4 — Highlight the Marker-to-Marker Path

**Skills:** graph shortest path, marker components, same-size extraction


**Primitive note:** Uses component_graph plus a shortest-path search between the blue(1) and red(2) components.


**Scaffold:**

- Find the blue(1) and red(2) marker components.

- Build the contact graph and compute the shortest path between them.

- Render only the components that lie on that path.

**Train 1 input**

```text
0000000000
0000000000
0000700000
0133442000
0033440000
0000000000
0000000000
0000000000
```
**Train 1 output**

```text
0000000000
0000000000
0000000000
0888888000
0088880000
0000000000
0000000000
0000000000
```
**Train 2 input**

```text
00000000000
00001000000
00003300000
00003300000
00004470000
00004400000
00006600000
00006600000
00002000000
00000000000
```
**Train 2 output**

```text
00000000000
00008000000
00008800000
00008800000
00008800000
00008800000
00008800000
00008800000
00008000000
00000000000
```
**Test input**

```text
0000000000000
0000000000000
0133448000000
0033440000000
0000660000000
0000660000000
0000770000000
0000770000000
0000200000000
0000000000000
```
**Test output**

```text
0000000000000
0000000000000
0888880000000
0088880000000
0000880000000
0000880000000
0000880000000
0000880000000
0000800000000
0000000000000
```
**Written solution:** The two special colors identify the endpoints in the contact graph. Find the unique shortest component path from blue(1) to red(2), then keep exactly those path components. Draw them on a blank same-size grid in cyan(8).

**Reference program:**

```python
def solve_S12_M4(grid):
    h, w = dims(grid)
    comps, adj = component_graph(grid)
    s = next(i for i, comp in enumerate(comps) if comp["color"] == 1)
    t = next(i for i, comp in enumerate(comps) if comp["color"] == 2)
    path = shortest_path(adj, s, t)
    out = blank(h, w, 0)
    for i in path:
        for r,c in comps[i]["cells"]:
            out[r][c] = 8
    return out
```

## S12_M5 — Select Components Touching Two Colors

**Skills:** neighbor-color sets, component relations, same-size masking


**Primitive note:** Uses component_graph, but the key feature is the set of neighboring colors rather than raw degree.


**Scaffold:**

- For each component, collect the colors of the components it touches.

- Keep the components whose neighbor-color set has size at least 2.

- Erase everything else.

**Train 1 input**

```text
000000000000
000000000000
000020000000
000344000000
000044007000
000000006600
000000006600
000000000000
```
**Train 1 output**

```text
000000000000
000000000000
000000000000
000088000000
000088000000
000000000000
000000000000
000000000000
```
**Train 2 input**

```text
000000000000
002000000000
034400000000
004400700000
000000600000
000000680000
000000000000
000000000990
000000000990
```
**Train 2 output**

```text
000000000000
000000000000
008800000000
008800000000
000000800000
000000800000
000000000000
000000000000
000000000000
```
**Test input**

```text
0000000000000
0000000000830
0000000000330
0000020006000
0000346400000
0000044400000
0077000000000
0077000000000
0000000000000
0000000000000
```
**Test output**

```text
0000000000000
0000000000000
0000000000000
0000000000000
0000080800000
0000088800000
0000000000000
0000000000000
0000000000000
0000000000000
```
**Written solution:** This puzzle is about variety of contacts, not just quantity. For every component, look at the set of distinct colors among its neighboring components. Any object that touches at least two different colors is selected and drawn in cyan(8) on a black background.

**Reference program:**

```python
def solve_S12_M5(grid):
    h, w = dims(grid)
    comps, adj = component_graph(grid)
    out = blank(h, w, 0)
    for i, comp in enumerate(comps):
        if len(neighbor_color_set(comps, adj, i)) >= 2:
            for r,c in comp["cells"]:
                out[r][c] = 8
    return out
```

## S12_M6 — Crop the Most Colorful Cluster

**Skills:** graph clusters, distinct-color counting, cropped union


**Primitive note:** Uses connected clusters of the component graph and ranks them by number of distinct colors.


**Scaffold:**

- Split the contact graph into connected clusters.

- Count how many distinct colors appear in each cluster.

- Choose the cluster with the largest color variety and crop its union.

**Train 1 input**

```text
0000000000000
0000000000000
0223300006670
0223340006600
0000000000060
0000000000000
0000000000000
0000000000000
0000000000000
```
**Train 1 output**

```text
88880
88888
```
**Train 2 input**

```text
00000000000000
00000000000000
00233000000000
00033440000000
00000448000000
00000000000000
06677000000000
06677000000000
00060000000000
00000000000000
```
**Train 2 output**

```text
888000
088880
000888
```
**Test input**

```text
000000000000000
023300000000000
003344000000000
000044660000000
000000667000000
000000000000000
000000000006670
000000000008600
000000000000000
000000000000000
```
**Test output**

```text
88800000
08888000
00088880
00000888
```
**Written solution:** Group the touching objects into graph-connected clusters. For each cluster, count the distinct colors present. The winning cluster is the one with the most color variety; output that whole cluster, preserving its geometry, cropped and recolored to cyan(8).

**Reference program:**

```python
def solve_S12_M6(grid):
    comps, adj = component_graph(grid)
    clusters = graph_clusters(adj)
    def key(cl):
        colors = {comps[i]["color"] for i in cl}
        return (len(colors), len(cl), len(union_cells(comps, cl)))
    best = max(clusters, key=key)
    return extract_union_grid(grid, comps, best, recolor=8)
```

## S12_M7 — Highlight Distance-Two Components

**Skills:** BFS on contact graph, seeded selection, distance filtering


**Primitive note:** Uses graph distances from a blue(1) seed component.


**Scaffold:**

- Find the blue(1) seed component.

- Run BFS on the contact graph to get graph distances.

- Keep exactly the components at distance 2 from the seed.

**Train 1 input**

```text
00000000000
00000000000
00007000000
01334466000
00334466000
00000000000
00000000000
00000000000
```
**Train 1 output**

```text
00000000000
00000000000
00000000000
00008800000
00008800000
00000000000
00000000000
00000000000
```
**Train 2 input**

```text
000000000000
000000000000
000006000000
000000000000
011334470000
011334400000
000000000000
000000000000
000000000000
000000000000
```
**Train 2 output**

```text
000000000000
000000000000
000000000000
000000000000
000008800000
000008800000
000000000000
000000000000
000000000000
000000000000
```
**Test input**

```text
0000000000000
0000000000000
0013344700000
0003344000000
0000066000000
0000066000000
0000080000000
0000000000000
0000000000000
0000000000000
```
**Test output**

```text
0000000000000
0000000000000
0000088000000
0000088000000
0000000000000
0000000000000
0000000000000
0000000000000
0000000000000
0000000000000
```
**Written solution:** Use the blue(1) component as the graph source. Compute component distances through the contact graph. The output keeps only the objects that are exactly two graph steps away from the seed, recolored to cyan(8).

**Reference program:**

```python
def solve_S12_M7(grid):
    h, w = dims(grid)
    comps, adj = component_graph(grid)
    seed = next(i for i, comp in enumerate(comps) if comp["color"] == 1)
    dist = bfs_distances(adj, seed)
    out = blank(h, w, 0)
    for i, d in dist.items():
        if d == 2:
            for r,c in comps[i]["cells"]:
                out[r][c] = 8
    return out
```


# Hard

## S12_H1 — Find the Articulation Component

**Skills:** cut vertices, graph structure, same-size extraction


**Primitive note:** Uses articulation-point detection on the component graph.


**Scaffold:**

- Build the contact graph of components.

- Ask which component is a cut vertex: removing it would disconnect the cluster.

- Keep that articulation component and erase the rest.

**Train 1 input**

```text
00000000000
00000000000
00003000000
00042200000
00002260000
00000000000
00000000770
00000000770
00000000000
```
**Train 1 output**

```text
00000000000
00000000000
00000000000
00008800000
00008800000
00000000000
00000000000
00000000000
00000000000
```
**Train 2 input**

```text
000000000000
077000000000
077000000000
000004000000
000022330000
000022630000
000000000000
000000000000
000000000000
000000000000
```
**Train 2 output**

```text
000000000000
000000000000
000000000000
000000000000
000088000000
000088000000
000000000000
000000000000
000000000000
000000000000
```
**Test input**

```text
0000000000000
0000000000800
0000000000800
0000030000800
0000420000000
0000020600000
0000022000000
0000000000000
0000000000000
0000000000000
```
**Test output**

```text
0000000000000
0000000000000
0000000000000
0000000000000
0000080000000
0000080000000
0000088000000
0000000000000
0000000000000
0000000000000
```
**Written solution:** The target is the graph articulation point, the component whose removal would break the touching structure into more connected pieces. After finding that cut vertex in the component graph, draw only that component in cyan(8) on a black same-size grid.

**Reference program:**

```python
def solve_S12_H1(grid):
    h, w = dims(grid)
    comps, adj = component_graph(grid)
    arts = articulation_points(adj)
    out = blank(h, w, 0)
    for i in arts:
        for r,c in comps[i]["cells"]:
            out[r][c] = 8
    return out
```

## S12_H2 — Odd Panel by Degree Pattern

**Skills:** multi-panel comparison, degree multisets, cropped selection


**Primitive note:** Uses component_graph separately inside each panel, then compares the sorted degree multisets.


**Scaffold:**

- Split the image into panels using the full-height gray(5) bars.

- Within each panel, compute the degree multiset of its component graph.

- Two panels match; keep the odd one out.

**Train 1 input**

```text
00000000500000000500000000
00000000500220000500000000
00000000500220000500300000
22334460500330000504220000
22334466500330000500226000
00000000500446000500000000
00000000500446600500000000
00000000500000000500000000
```
**Train 1 output**

```text
0800
8880
0888
```
**Train 2 input**

```text
00000000500000000500000000
00300000500000000500000000
04220000522334470500300000
00226000522334400504220000
00000000500000000500226000
00000000500000000500000000
00000000500000000500000000
00000000500000000500000000
```
**Train 2 output**

```text
8888888
8888880
```
**Test input**

```text
00000000005000000000050000000000
00000000005002200000050000000000
00000000005002200000050003000000
22334466705003300000050042200000
22334466005003300000050002260000
00000000005004466700050000700000
00000000005004466000050000000000
00000000005000000000050000000000
00000000005000000000050000000000
```
**Test output**

```text
0800
8880
0888
0080
```
**Written solution:** Each panel encodes a small contact graph. Ignore geometry at first and compare only the sorted list of graph degrees in each panel. Two panels have the same degree pattern and one differs; crop the differing panel's cluster and recolor it to cyan(8).

**Reference program:**

```python
def solve_S12_H2(grid):
    groups, bars = split_by_vertical_bars(grid, color=5)
    sigs = []
    panels = []
    for start, end in groups:
        panel = crop_panel(grid, start, end)
        comps, adj = component_graph(panel)
        clusters = graph_clusters(adj)
        cl = max(clusters, key=lambda x: len(x))
        degs = tuple(sorted(len(adj[i]) for i in cl))
        sigs.append(degs)
        panels.append((panel, comps, cl))
    common = Counter(sigs).most_common(1)[0][0]
    odd_idx = next(i for i,s in enumerate(sigs) if s != common)
    panel, comps, cl = panels[odd_idx]
    return extract_union_grid(panel, comps, cl, recolor=8)
```

## S12_H3 — Dual Legend: Cluster Size and Degree

**Skills:** two-parameter legend decoding, graph clusters, targeted selection


**Primitive note:** The header row carries two constraints at once: count of blue(1) cells gives cluster size, count of red(2) cells gives local degree.


**Scaffold:**

- Read the header: blue(1) count means cluster size, red(2) count means degree.

- In the body, compute each component's cluster size and degree.

- Select the unique component matching both conditions.

**Train 1 input**

```text
111220000000
000000000000
000000000000
022334400000
022334400000
000000007000
000000086600
000000006600
000000000000
```
**Train 1 output**

```text
88
88
```
**Train 2 input**

```text
111122200000
000000000000
000000000000
000030000000
000422000000
000022600000
000000000000
000000000778
000000000770
```
**Train 2 output**

```text
88
88
```
**Test input**

```text
1111122200000
0000000000000
0000000000880
0000000000880
0000030000900
0000422660000
0000022667000
0000000000000
0000000000000
0000000000000
```
**Test output**

```text
88
88
```
**Written solution:** The top row is a two-part legend. The number of blue(1) cells specifies how many components must be in the target's graph cluster, and the number of red(2) cells specifies the target component's degree within that cluster. Find the unique component satisfying both and crop it, recolored to cyan(8).

**Reference program:**

```python
def solve_S12_H3(grid):
    want_cluster = sum(1 for v in grid[0] if v == 1)
    want_degree = sum(1 for v in grid[0] if v == 2)
    body = [row[:] for row in grid[1:]]
    comps, adj = component_graph(body)
    clusters = graph_clusters(adj)
    cluster_size = {}
    for cl in clusters:
        for i in cl:
            cluster_size[i] = len(cl)
    target = next(i for i in range(len(comps)) if cluster_size[i] == want_cluster and len(adj[i]) == want_degree)
    return extract_union_grid(body, comps, [target], recolor=8)
```

## S12_H4 — Color by Graph Distance from the Seed

**Skills:** BFS layers, multi-color output, seeded graph reasoning


**Primitive note:** Uses graph-distance layers from the blue(1) seed component.


**Scaffold:**

- Find the blue(1) source component.

- Compute graph distances through the contact graph.

- Recolor each reached component by the distance map.

**Train 1 input**

```text
000000000000
000000000770
000000000770
013344660000
003344660000
000000000000
000000000000
000000000000
000000000000
```
**Train 1 output**

```text
000000000000
000000000000
000000000000
023344660000
003344660000
000000000000
000000000000
000000000000
000000000000
```
**Train 2 input**

```text
0000000000000
0000000000800
0000000000800
0004000000800
0001133660000
0001133660000
0000000700000
0000000000000
0000000000000
0000000000000
```
**Train 2 output**

```text
0000000000000
0000000000000
0000000000000
0003000000000
0002233440000
0002233440000
0000000600000
0000000000000
0000000000000
0000000000000
```
**Test input**

```text
00000000000000
00000000000990
01334400000990
00334400000000
00006680000000
00006600000000
00007700000000
00007700000000
00000000000000
00000000000000
```
**Test output**

```text
00000000000000
00000000000000
02334400000000
00334400000000
00006660000000
00006600000000
00006600000000
00006600000000
00000000000000
00000000000000
```
**Written solution:** Start from the blue(1) seed and compute graph distances over the component contact graph. Then recolor by layer: distance 0 -> red(2), distance 1 -> green(3), distance 2 -> yellow(4), distance 3 or more -> magenta(6). Components outside the seed's cluster disappear.

**Reference program:**

```python
def solve_S12_H4(grid):
    h, w = dims(grid)
    comps, adj = component_graph(grid)
    seed = next(i for i, comp in enumerate(comps) if comp["color"] == 1)
    dist = bfs_distances(adj, seed)
    mapping = {0:2, 1:3, 2:4}
    out = blank(h, w, 0)
    for i, d in dist.items():
        color = mapping.get(d, 6)
        for r,c in comps[i]["cells"]:
            out[r][c] = color
    return out
```

## S12_H5 — Header Chooses the Articulation Count

**Skills:** header decoding, cluster-level graph analysis, cropped union


**Primitive note:** Uses the count of blue(1) header cells as the required number of articulation points in a cluster.


**Scaffold:**

- Read the header row and count the blue(1) cells.

- For each body cluster, compute how many articulation points its graph has.

- Choose the cluster whose articulation count matches the header.

**Train 1 input**

```text
1000000000000000
0000000000000000
0000000000000000
0300000077889960
4220000077889900
0226000000000000
0000000000000000
0000000044500000
0000000044000000
```
**Train 1 output**

```text
0800
8880
0888
```
**Train 2 input**

```text
1100000000000000
0000000000000000
0300000000044500
4220000000044000
0226000000000000
0000000077889960
0000000077889900
0000000000000000
0000000000000000
```
**Train 2 output**

```text
8888888
8888880
```
**Test input**

```text
000000000000000000
000000000000000000
000000050000000000
000000644000000000
022300044700000000
022000000000000000
000000000008899663
000000000008899660
000000000000000000
```
**Test output**

```text
888
880
```
**Written solution:** The header tells you how many cut vertices the target cluster should have. Build the body contact graph, split it into connected clusters, and count articulation points inside each cluster. Keep the cluster whose articulation count matches the header, crop it, and recolor it to cyan(8).

**Reference program:**

```python
def solve_S12_H5(grid):
    want_arts = sum(1 for v in grid[0] if v == 1)
    body = [row[:] for row in grid[1:]]
    comps, adj = component_graph(body)
    clusters = graph_clusters(adj)
    def art_count(cl):
        sub_adj = {i: sorted(j for j in adj[i] if j in cl) for i in cl}
        return len(articulation_points(sub_adj))
    target = next(cl for cl in clusters if art_count(cl) == want_arts)
    return extract_union_grid(body, comps, target, recolor=8)
```

## S12_H6 — Degree Sequence of the Largest Cluster

**Skills:** cluster selection, degree sequence, constructive output


**Primitive note:** Uses the largest connected cluster in the component graph, then converts graph structure into a symbolic row output.


**Scaffold:**

- Find the graph cluster with the most components.

- Compute the sorted degree sequence of that cluster.

- Write a one-row output whose colors are degree+1.

**Train 1 input**

```text
0000000000000
0000000000000
0223344600000
0223344660000
0000000000000
0000000008077
0000000000077
0000000000000
```
**Train 1 output**

```text
2233
```
**Train 2 input**

```text
00000000000000
00000000000889
00000000000880
00000300000000
00004226000000
00000270000000
00000000000000
00000000000000
00000000000000
00000000000000
```
**Train 2 output**

```text
22225
```
**Test input**

```text
000000000000000
000000000000889
000000000000880
000003000000000
000042266000000
000002266700000
000000000000000
000000000000000
000000000000000
000000000000000
```
**Test output**

```text
22234
```
**Written solution:** Choose the largest touching cluster by number of components. Compute the degrees of its components, sort those degrees, and convert them into a one-row symbolic output. Each output cell is colored degree+1, so a degree sequence like [1,1,2,2] becomes [2,2,3,3].

**Reference program:**

```python
def solve_S12_H6(grid):
    comps, adj = component_graph(grid)
    clusters = graph_clusters(adj)
    best = max(clusters, key=lambda cl: (len(cl), len(union_cells(comps, cl))))
    degs = sorted(len(adj[i]) for i in best)
    return [[d+1 for d in degs]]
```

## S12_H7 — Adjacency Matrix of the Seed Cluster

**Skills:** cluster extraction, component ordering, constructive graph output


**Primitive note:** Uses the cluster containing the blue(1) seed, ordered by component top-left position, and renders its adjacency matrix.


**Scaffold:**

- Find the contact-graph cluster containing the blue(1) seed.

- Order its components by top-left position.

- Build an adjacency matrix with 1 on the diagonal and 8 for graph edges.

**Train 1 input**

```text
0000000000000
0000000000000
0113344600000
0113344660000
0000000000000
0000000000077
0000000000077
0000000000000
```
**Train 1 output**

```text
1800
8180
0818
0081
```
**Train 2 input**

```text
0000000000000
0000000000770
0000300000770
0004110000000
0000116000000
0000000000000
0000000000000
0000000000000
0000000000000
```
**Train 2 output**

```text
1080
0180
8818
0081
```
**Test input**

```text
000000000000000
000000000000880
000000000000880
000003000000000
000041166000000
000001166700000
000000000000000
000000000000000
000000000000000
000000000000000
```
**Test output**

```text
10800
01800
88180
00818
00081
```
**Written solution:** The blue(1) component chooses which graph cluster to encode. Order that cluster's components from top-left to bottom-right. Then build a square matrix: put blue(1) on the diagonal to mark self-membership, cyan(8) wherever two ordered components touch in the graph, and black(0) elsewhere.

**Reference program:**

```python
def solve_S12_H7(grid):
    comps, adj = component_graph(grid)
    seed = next(i for i, comp in enumerate(comps) if comp["color"] == 1)
    cluster = next(cl for cl in graph_clusters(adj) if seed in cl)
    ids = sorted_ids_top_left(comps, cluster)
    idx = {cid:i for i,cid in enumerate(ids)}
    n = len(ids)
    out = blank(n, n, 0)
    for i in range(n):
        out[i][i] = 1
    for cid in ids:
        i = idx[cid]
        for nid in adj[cid]:
            if nid in idx:
                j = idx[nid]
                out[i][j] = 8
    return out
```

