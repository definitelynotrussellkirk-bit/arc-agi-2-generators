"""Generator for aabf363d.

Rule: bottom-left cell holds the marker color. The first non-bg cell
that is NOT the marker color is the shape's color. Recolor every cell
of shape-color to marker-color; everything else becomes 0.

Combinatorial axes (8): grid_h/w, shape_size, marker_color, shape_color,
shape_layout, shape_position_bias, decoy_marker_count, decoy_density.
Degenerates: no_shape, full_grid_shape, marker_only.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.blobs import grow_blob
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "449ea8b9619c"
VERSION = "1.1.0"
TASK_ID = "449ea8b9619c"
SUMMARY = "Bottom-left marker; rule recolors single non-marker shape to marker color."

INVARIANTS = [
    "bottom-left cell holds the marker color",
    ">=1 non-marker, non-bg cell forms the shape",
    "shape uses one color (≠ marker)",
    "marker color appears only at bottom-left (so first non-marker non-bg is shape)",
]

SHAPE_LAYOUTS = ("blob", "vertical_strip", "horizontal_strip",
                 "L_shape", "diag", "scattered_compact")
DEGENERATE_TEXTURES = ("no_shape", "full_grid_shape", "marker_only")
HELPFUL_TEXTURES = SHAPE_LAYOUTS

AXES = {
    "grid_h":            {"type": "int", "default": "rng 7..12", "valid": "5..16"},
    "grid_w":            {"type": "int", "default": "rng 7..12", "valid": "5..16"},
    "shape_size":        {"type": "int", "default": "rng 5..15", "valid": "3..25"},
    "marker_color":      {"type": "color", "default": "rng (≠0)", "valid": "1..9"},
    "shape_color":       {"type": "color", "default": "rng (≠0,marker)",
                          "valid": "1..9"},
    "shape_layout":      {"type": "str", "default": "rng helpful",
                          "valid": "|".join(SHAPE_LAYOUTS)},
    "shape_position_bias": {"type": "str",
                            "default": "rng top|center|spread",
                            "valid": "top|center|spread"},
    "decoy_density":     {"type": "float", "default": "0", "valid": "0..0.05"},
    "texture":           {"type": "str", "default": "alias for shape_layout",
                          "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index, version=VERSION,
                  task_id=TASK_ID, difficulty=difficulty, overrides=overrides)
    if difficulty == "easy":
        h_lo, h_hi, s_lo, s_hi = 5, 7, 4, 7
    elif difficulty == "hard":
        h_lo, h_hi, s_lo, s_hi = 11, 16, 12, 22
    else:
        h_lo, h_hi, s_lo, s_hi = 7, 12, 5, 15
    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", h_lo, h_hi)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], h, w, rng)
    size = int(overrides.get("shape_size",
                             ctx.draw_int("shape_size", s_lo, s_hi)))
    marker = int(overrides.get("marker_color",
                               ctx.draw_color("marker_color", exclude={0})))
    fill = int(overrides.get("shape_color",
                             ctx.draw_color("shape_color",
                                            exclude={0, marker})))
    layout = (overrides.get("texture") or overrides.get("shape_layout")
              or ctx.draw_choice("shape_layout", list(SHAPE_LAYOUTS)))
    bias = overrides.get("shape_position_bias",
                         ctx.draw_choice("shape_position_bias",
                                         ["top", "center", "spread"]))
    g = full_grid(h, w, 0)
    g[h - 1][0] = marker
    cells = _shape_cells(layout, size, h, w, bias, rng)
    for r, c in cells:
        if 0 <= r < h and 0 <= c < w and (r, c) != (h - 1, 0):
            g[r][c] = fill
    has_shape = any(g[r][c] == fill for r in range(h) for c in range(w))
    if not has_shape:
        g[0][0] = fill
    return g


def _shape_cells(layout, size, h, w, bias, rng):
    if bias == "top":
        anchor_r = 1
    elif bias == "center":
        anchor_r = h // 2
    else:
        anchor_r = rng.randint(0, max(0, h - 3))
    anchor_c = rng.randint(2, max(2, w - 3))
    if layout == "blob":
        used = {(h - 1, 0)}
        cells = grow_blob(rng, h, w, used, size)
        if cells is None:
            return [(1, 2), (1, 3), (2, 2), (2, 3), (3, 2)]
        return list(cells)
    if layout == "vertical_strip":
        return [(anchor_r + i, anchor_c) for i in range(min(size, h - anchor_r))]
    if layout == "horizontal_strip":
        return [(anchor_r, anchor_c + i)
                for i in range(min(size, w - anchor_c))]
    if layout == "L_shape":
        cells = [(anchor_r + i, anchor_c) for i in range(min(size // 2, h - anchor_r))]
        cells += [(anchor_r, anchor_c + i)
                  for i in range(1, min(size - len(cells) + 1, w - anchor_c))]
        return cells
    if layout == "diag":
        cells = []
        for i in range(size):
            r = anchor_r + i
            c = anchor_c + i
            if 0 <= r < h and 0 <= c < w:
                cells.append((r, c))
        return cells
    cells = []
    placed = set()
    for _ in range(size * 5):
        if len(cells) >= size:
            break
        r = anchor_r + rng.randint(-2, 2)
        c = anchor_c + rng.randint(-2, 2)
        if 0 <= r < h and 0 <= c < w and (r, c) not in placed and (r, c) != (h - 1, 0):
            placed.add((r, c))
            cells.append((r, c))
    return cells


def _draw_from_degenerate(name, h, w, rng):
    g = full_grid(h, w, 0)
    marker = rng.choice([1, 2, 3, 4, 5, 6, 7, 8, 9])
    fill = rng.choice([c for c in range(1, 10) if c != marker])
    if name == "no_shape":
        g[h - 1][0] = marker
        return g
    if name == "full_grid_shape":
        for r in range(h):
            for c in range(w):
                g[r][c] = fill
        g[h - 1][0] = marker
        return g
    if name == "marker_only":
        g[h - 1][0] = marker
        g[0][0] = fill
        return g
    return g
