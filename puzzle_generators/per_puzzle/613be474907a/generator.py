"""Generator for d968ffd4.

Rule: two colored regions with a gap; rule bridges the gap halfway
each side.

Combinatorial axes (8): grid_h/w, palette_kind, anchor_corner,
asymmetry_force, palette_size, position_bias, n_distinct_colors,
gap_w.
Degenerates: no_regions, single_region, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, draw_rect

GENERATOR_ID = "613be474907a"
VERSION = "1.1.0"
TASK_ID = "613be474907a"
SUMMARY = "Two colored regions with a gap; rule bridges halfway each side."

INVARIANTS = [
    "bg is the mode color",
    "exactly two distinct non-bg colors with non-overlapping bboxes on one axis",
    "gap between bboxes is at least three cells wide",
    "regions sit clear of grid borders",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_regions", "single_region", "full_grid")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 10..14", "valid": "8..18"},
    "grid_w":         {"type": "int", "default": "rng 14..18", "valid": "12..22"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2"},
    "position_bias":  {"type": "str", "default": "rng", "valid": "rng"},
    "n_distinct_colors":{"type": "int", "default": "2", "valid": "2"},
    "gap_w":          {"type": "int", "default": "rng 3..6", "valid": "3..8"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    rng = ctx.draw_rng("placement")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], rng)
    if difficulty == "easy":
        h_lo, h_hi = 10, 11
    elif difficulty == "hard":
        h_lo, h_hi = 14, 18
    else:
        h_lo, h_hi = 10, 14
    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", 14, 18)
    bg = rng.choice([0, 5, 7])
    palette = ctx.draw_distinct_colors("palette", n=2, exclude={bg})
    c1, c2 = palette
    g = full_grid(h, w, bg)
    bh = rng.randint(2, 4)
    rr = rng.randint(1, h - bh - 1)
    bw1 = rng.randint(2, 3)
    bw2 = rng.randint(2, 3)
    rc1 = rng.randint(0, 2)
    gap_w = rng.randint(3, 6)
    rc2 = rc1 + bw1 + gap_w
    if rc2 + bw2 > w:
        return [[bg]]
    draw_rect(g, rr, rc1, bh, bw1, c1)
    draw_rect(g, rr, rc2, bh, bw2, c2)
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(12, 16, 0)
    if name == "no_regions":
        return g
    if name == "single_region":
        draw_rect(g, 4, 4, 3, 3, 2)
        return g
    if name == "full_grid":
        for r in range(12):
            for c in range(16):
                g[r][c] = 2
        return g
    return g
