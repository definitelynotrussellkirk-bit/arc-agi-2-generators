"""Generator for additional_bank:H7 — Recolor 7-objects by control cell.

Rule: control cell at (0, 0) is 1 or 2. 7-objects elsewhere: if
control=1, recolor hollow ones to 8; if control=2, recolor solid ones.

Combinatorial axes (8): grid_h, grid_w, palette_kind, control,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_control, no_hollow, no_solid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, draw_rect, draw_rect_outline

GENERATOR_ID = "c7f337af82e5"
VERSION = "1.1.0"
TASK_ID = "c7f337af82e5"
SUMMARY = "Control cell at (0,0) ∈ {1,2}, plus 2-3 7-objects (mix of hollow and solid)."

INVARIANTS = [
    "cell (0,0) is 1 or 2 (the control)",
    "2-3 objects of color 7 elsewhere",
    "≥1 hollow 7-frame and ≥1 solid 7-rectangle",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_control", "no_hollow", "no_solid")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..10", "valid": "6..12"},
    "grid_w":         {"type": "int", "default": "rng 9..12", "valid": "8..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "control":        {"type": "int", "default": "rng 1|2", "valid": "1..2"},
    "palette_size":   {"type": "int", "default": "3", "valid": "3..3"},
    "position_bias":  {"type": "str", "default": "control_plus_7objects",
                       "valid": "control_plus_7objects"},
    "n_distinct_colors": {"type": "int", "default": "3", "valid": "3..3"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 8, 8)
        w = ctx.draw_int("grid_w", 9, 10)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 11, 12)
    else:
        h = ctx.draw_int("grid_h", 8, 10)
        w = ctx.draw_int("grid_w", 9, 12)
    g = full_grid(h, w, 0)
    rng = ctx.draw_rng("layout")
    g[0][0] = rng.choice([1, 2])
    placed = []
    # Place 1 hollow frame
    for _ in range(40):
        fh = rng.randint(3, 4); fw = rng.randint(3, 4)
        r0 = rng.randint(1, h - fh - 1); c0 = rng.randint(1, w - fw - 1)
        if any(abs(r0 - pr) < (fh + 2) and abs(c0 - pc) < (fw + 2) for pr, pc in placed):
            continue
        draw_rect_outline(g, r0, c0, fh, fw, 7)
        placed.append((r0, c0))
        break
    # Place 1 solid rect
    for _ in range(40):
        rh = rng.randint(2, 3); rw = rng.randint(2, 3)
        r0 = rng.randint(1, h - rh - 1); c0 = rng.randint(1, w - rw - 1)
        if any(abs(r0 - pr) < (rh + 2) and abs(c0 - pc) < (rw + 2) for pr, pc in placed):
            continue
        draw_rect(g, r0, c0, rh, rw, 7)
        placed.append((r0, c0))
        break
    return g


def _draw_from_degenerate(name, rng):
    h, w = 9, 11
    g = full_grid(h, w, 0)
    if name == "no_control":
        # 7-objects but no control cell at (0,0) → no rule selector
        draw_rect_outline(g, 2, 2, 3, 3, 7)
        draw_rect(g, 5, 6, 2, 3, 7)
        return g
    if name == "no_hollow":
        # control + only solid 7-rects → control=1 has no hollow targets
        g[0][0] = 1
        draw_rect(g, 2, 2, 2, 3, 7)
        draw_rect(g, 5, 6, 2, 3, 7)
        return g
    if name == "no_solid":
        # control + only hollow 7-frames → control=2 has no solid targets
        g[0][0] = 2
        draw_rect_outline(g, 2, 2, 3, 3, 7)
        draw_rect_outline(g, 5, 6, 3, 3, 7)
        return g
    return g
