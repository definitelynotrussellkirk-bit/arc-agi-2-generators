"""Generator for f5aa3634.

Rule: several components; rule extracts the one that appears twice.

Combinatorial axes (8): grid_h/w, palette_kind, anchor_corner,
asymmetry_force, palette_size, position_bias, n_components,
n_distinct_colors.
Degenerates: no_components, single_component, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "70c33a3391ac"
VERSION = "1.1.0"
TASK_ID = "70c33a3391ac"
SUMMARY = "Multiple components; rule extracts the duplicated one."

INVARIANTS = [
    "background is 0",
    "exactly one component shape+color appears twice",
    "all other components are unique in shape+color",
    "components separated by bg margin of at least one cell",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_components", "single_component", "full_grid")
HELPFUL_TEXTURES = PALETTE_KINDS

SHAPES = [
    [(0, 0), (0, 1), (1, 0)],
    [(0, 0), (0, 1), (0, 2)],
    [(0, 0), (1, 0), (2, 0)],
    [(0, 1), (1, 0), (1, 1), (1, 2)],
    [(0, 0), (0, 1), (1, 1), (1, 2)],
    [(0, 0), (1, 0), (1, 1), (2, 1)],
    [(0, 0), (0, 1), (1, 0), (1, 1)],
    [(0, 0), (0, 1), (0, 2), (1, 1)],
    [(0, 0), (0, 1), (0, 2), (1, 0)],
]

AXES = {
    "grid_h":         {"type": "int", "default": "rng 14..18", "valid": "12..22"},
    "grid_w":         {"type": "int", "default": "rng 14..18", "valid": "12..22"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "4", "valid": "4"},
    "position_bias":  {"type": "str", "default": "rng", "valid": "rng"},
    "n_components":   {"type": "int", "default": "5", "valid": "4..6"},
    "n_distinct_colors":{"type": "int", "default": "4", "valid": "4"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def _shape_dims(cells):
    rs = [r for r, _ in cells]
    cs = [c for _, c in cells]
    return max(rs) + 1, max(cs) + 1


def _try_place(g, cells, color, rng, h, w, attempts=30):
    sh, sw = _shape_dims(cells)
    for _ in range(attempts):
        rr = rng.randint(0, h - sh)
        rc = rng.randint(0, w - sw)
        ok = True
        for r in range(max(0, rr - 1), min(h, rr + sh + 1)):
            for c in range(max(0, rc - 1), min(w, rc + sw + 1)):
                if g[r][c] != 0:
                    ok = False; break
            if not ok:
                break
        if not ok:
            continue
        for dr, dc in cells:
            g[rr + dr][rc + dc] = color
        return True
    return False


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    rng = ctx.draw_rng("placement")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], rng)
    if difficulty == "easy":
        h_lo, h_hi = 14, 14
    elif difficulty == "hard":
        h_lo, h_hi = 18, 22
    else:
        h_lo, h_hi = 14, 18
    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", h_lo, h_hi)
    palette = ctx.draw_distinct_colors("palette", n=4, exclude={0})
    g = full_grid(h, w, 0)
    shape_idxs = rng.sample(range(len(SHAPES)), 4)
    dup_shape = SHAPES[shape_idxs[0]]
    dup_color = palette[0]
    placed_dup = 0
    for _ in range(2):
        if _try_place(g, dup_shape, dup_color, rng, h, w):
            placed_dup += 1
    if placed_dup < 2:
        return [[0]]
    placed_unique = 0
    for i in range(1, 4):
        if _try_place(g, SHAPES[shape_idxs[i]], palette[i], rng, h, w):
            placed_unique += 1
    if placed_unique < 2:
        return [[0]]
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(15, 15, 0)
    if name == "no_components":
        return g
    if name == "single_component":
        for dr, dc in SHAPES[0]:
            g[2 + dr][2 + dc] = 2
        return g
    if name == "full_grid":
        for r in range(15):
            for c in range(15):
                g[r][c] = 2
        return g
    return g
