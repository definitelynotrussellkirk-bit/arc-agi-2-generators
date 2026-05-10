"""Generator for arc_additional_puzzle_bank_volume3:H15.

Rule: control at (0,0) — 3=union, 4=XOR, 5=intersection. Output cells
in the ctrl-defined set sized to max bbox, color 8.

Combinatorial axes (8): grid_h/w, palette_kind, ctrl, palette_size,
position_bias, n_distinct_colors, overlap_kind, texture.
Degenerates: no_ctrl, invalid_ctrl, no_blobs.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, paint_at

GENERATOR_ID = "3020cc038f3f"
VERSION = "1.1.0"
TASK_ID = "3020cc038f3f"
SUMMARY = "Ctrl ∈ {3,4,5} at top-left + 1-shape and 2-shape."

INVARIANTS = [
    "(0,0) is ctrl ∈ {3,4,5}",
    "exactly one 1-blob and one 2-blob",
    "their normalized cells differ in some positions",
]

PALETTE_KINDS = ("default", "ctrl_3", "ctrl_4", "ctrl_5")
DEGENERATE_TEXTURES = ("no_ctrl", "invalid_ctrl", "no_blobs")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 7..9", "valid": "5..14"},
    "grid_w":         {"type": "int", "default": "rng 9..11", "valid": "7..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "ctrl":           {"type": "int", "default": "rng 3..5", "valid": "3..5"},
    "palette_size":   {"type": "int", "default": "3", "valid": "3"},
    "position_bias":  {"type": "str", "default": "fixed", "valid": "fixed"},
    "n_distinct_colors": {"type": "int", "default": "3", "valid": "3"},
    "overlap_kind":   {"type": "str", "default": "partial", "valid": "partial"},
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
        h = ctx.draw_int("grid_h", 7, 8)
        w = ctx.draw_int("grid_w", 9, 10)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("grid_w", 10, 11)
    else:
        h = ctx.draw_int("grid_h", 7, 9)
        w = ctx.draw_int("grid_w", 9, 11)
    ctrl = ctx.draw_int("ctrl", 3, 5)
    g = full_grid(h, w, 0)
    g[0][0] = ctrl
    paint_at(g, 1, 1, [(0, 0), (1, 0), (1, 1)], 1)
    paint_at(g, 1, w - 4, [(0, 0), (0, 1), (1, 0)], 2)
    return g


def _draw_from_degenerate(name, rng):
    h, w = 8, 10
    g = full_grid(h, w, 0)
    if name == "no_ctrl":
        # both blobs but no top-left ctrl — operation undefined
        paint_at(g, 1, 1, [(0, 0), (1, 0), (1, 1)], 1)
        paint_at(g, 1, w - 4, [(0, 0), (0, 1), (1, 0)], 2)
        return g
    if name == "invalid_ctrl":
        # ctrl outside {3,4,5} — rule cannot map it
        g[0][0] = 8
        paint_at(g, 1, 1, [(0, 0), (1, 0), (1, 1)], 1)
        paint_at(g, 1, w - 4, [(0, 0), (0, 1), (1, 0)], 2)
        return g
    if name == "no_blobs":
        # ctrl but no blobs — operands missing
        g[0][0] = 4
        return g
    return g
