"""Generator for puzzle 423a55dc.

Rule: shift each cell's column LEFT by (max_r - row), where max_r is
the bottommost non-bg row. Bottom row stays; rows above shear left.

Combinatorial axes (8): grid_h/w, shape_h, shape_w, palette_kind,
density, position_bias, anchor_corner, asymmetry_force.
Degenerates: no_cells, full_grid, single_row.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "4326f5c2ded0"
VERSION = "1.1.0"
TASK_ID = "4326f5c2ded0"
SUMMARY = "Cells; rule shears left by distance from bottom non-bg row."

INVARIANTS = [
    "background is 0",
    "non-bg cells stay in-bounds after shear",
    "shape concentrated near right side (room for left-shift)",
]

POSITION_BIASES = ("right_aligned", "diagonal", "tight", "spread")
PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_cells", "full_grid", "single_row")
HELPFUL_TEXTURES = POSITION_BIASES

AXES = {
    "grid_h":         {"type": "int", "default": "rng 12..18", "valid": "10..22"},
    "grid_w":         {"type": "int", "default": "rng 12..18", "valid": "10..22"},
    "shape_h":        {"type": "int", "default": "rng 4..7", "valid": "3..10"},
    "shape_w":        {"type": "int", "default": "rng 3..6", "valid": "3..8"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "density":        {"type": "float", "default": "rng 0.4..0.7",
                       "valid": "0.2..1"},
    "position_bias":  {"type": "str", "default": "rng helpful",
                       "valid": "|".join(POSITION_BIASES)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "texture":        {"type": "str", "default": "alias for position_bias",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if difficulty == "easy":
        h_lo, h_hi = 10, 12
    elif difficulty == "hard":
        h_lo, h_hi = 18, 22
    else:
        h_lo, h_hi = 12, 18
    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", h_lo, h_hi)
    rng = ctx.draw_rng("placement")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], h, w, rng)
    rh = int(overrides.get("shape_h",
                           ctx.draw_int("shape_h", 4, 7)))
    rw = int(overrides.get("shape_w",
                           ctx.draw_int("shape_w", 3, 6)))
    rh = max(3, min(min(h - 2, 10), rh))
    rw = max(3, min(min(w - 2, 8), rw))
    palette_kind = overrides.get("palette_kind",
                                 ctx.draw_choice("palette_kind",
                                                 list(PALETTE_KINDS)))
    palette = _build_palette(palette_kind, 2, rng)
    density = float(overrides.get("density",
                                  ctx.draw_rng("density")
                                  .uniform(0.4, 0.7)))
    g = full_grid(h, w, 0)
    max_r = h - 2
    rr = max_r - rh + 1
    min_rc = max_r - rr
    if w - rw - 1 < min_rc:
        rc = min_rc
    else:
        rc = rng.randint(min_rc, w - rw - 1)
    if rc + rw > w:
        # Shrink shape if too wide
        rw = w - rc
        if rw < 1:
            return _draw_from_degenerate("single_row", h, w, rng)
    for dr in range(rh):
        for dc in range(rw):
            if rng.random() < density:
                g[rr + dr][rc + dc] = rng.choice(palette)
    for c in range(rc, min(rc + rw, w)):
        if rng.random() < 0.5:
            g[max_r][c] = rng.choice(palette)
    if not any(g[r][c] != 0 for r in range(h) for c in range(w)):
        g[max_r][rc] = palette[0]
    return g


def _build_palette(kind, n, rng):
    if kind == "warm":
        pool = [2, 3, 4, 6, 9]
    elif kind == "cool":
        pool = [1, 5, 7, 8]
    elif kind == "primary":
        pool = [1, 2, 3, 4]
    else:
        pool = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    rng.shuffle(pool)
    return pool[:n]


def _draw_from_degenerate(name, h, w, rng):
    g = full_grid(h, w, 0)
    if name == "no_cells":
        return g
    if name == "full_grid":
        for r in range(h):
            for c in range(w):
                g[r][c] = 3
        return g
    if name == "single_row":
        for c in range(w // 2, w):
            g[h // 2][c] = 3
        return g
    return g
