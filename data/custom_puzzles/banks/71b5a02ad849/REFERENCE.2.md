# New Primitive Spec — `trace_polyline_markers`

```python
trace_polyline_markers(base_grid, marker_groups, mode='hv', intersection_color=None)
```

Purpose: draw one or more Manhattan polylines from ordered marker groups. Each group is a color plus an ordered point list. The primitive traces each consecutive pair of points using horizontal-then-vertical (`hv`) or vertical-then-horizontal (`vh`) routing.

Arguments:

- `base_grid`: output canvas to paint on
- `marker_groups`: iterable like `[(color, [(r,c), ...]), ...]`
- `mode`: `'hv'` or `'vh'` for segment routing order
- `intersection_color`: if not `None`, cells used by 2+ groups are recolored to this value

Why it matters: many ARC-like tasks contain sparse markers that implicitly define a path, wire, or route. This primitive turns that latent geometric instruction into a first-class DSL operation, rather than forcing the solver to rebuild Manhattan routing from raw loops each time.

Used in this set: **E49**, **M48**, and **H49**.