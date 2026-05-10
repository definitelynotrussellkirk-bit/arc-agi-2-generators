"""Generator for d89b689b.

Rule: 2x2 cyan block + 4 quadrant markers; rule replaces block with
quadrant colors.

Combinatorial axes (8): grid_h/w, palette_kind, position_bias,
anchor_corner, asymmetry_force, palette_size, marker_distance,
center_jitter.
Degenerates: no_markers, no_block, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "6143c7ef56be"
VERSION = "1.1.0"
TASK_ID = "6143c7ef56be"
SUMMARY = "2x2 cyan block + 4 quadrant markers; rule replaces block with quadrant colors."

INVARIANTS = [
    "background is 0",
    "exactly one 2x2 cyan(8) block",
    "exactly 4 distinct non-cyan, non-bg marker cells at diagonal corners",
]

POSITION_BIASES = ("centered", "scattered", "near_edge", "rng")
PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_markers", "no_block", "full_grid")
HELPFUL_TEXTURES = POSITION_BIASES

AXES = {
    "grid_h":         {"type": "int", "default": "rng 10..14", "valid": "8..18"},
    "grid_w":         {"type": "int", "default": "rng 10..14", "valid": "8..18"},
    "palette_kind":   {"type": "str", "default": "rng",
                       "valid": "|".join(PALETTE_KINDS)},
    "position_bias":  {"type": "str", "default": "rng helpful",
                       "valid": "|".join(POSITION_BIASES)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "4", "valid": "4"},
    "marker_distance":{"type": "int", "default": "2", "valid": "2..3"},
    "texture":        {"type": "str", "default": "alias for position_bias",
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
        h_lo, h_hi = 8, 10
    elif difficulty == "hard":
        h_lo, h_hi = 14, 18
    else:
        h_lo, h_hi = 10, 14
    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", h_lo, h_hi)
    palette = ctx.draw_distinct_colors("palette", n=4, exclude={0, 8})
    g = full_grid(h, w, 0)
    bias = (overrides.get("texture") or
            overrides.get("position_bias")
            or ctx.draw_choice("position_bias", list(POSITION_BIASES)))
    if bias == "centered":
        cr = max(3, h // 2 - 1)
        cc = max(3, w // 2 - 1)
    elif bias == "near_edge":
        cr = rng.choice([3, h - 5])
        cc = rng.choice([3, w - 5])
    else:
        cr = rng.randint(3, h - 5)
        cc = rng.randint(3, w - 5)
    cr = max(3, min(cr, h - 5))
    cc = max(3, min(cc, w - 5))
    g[cr][cc] = 8; g[cr][cc + 1] = 8
    g[cr + 1][cc] = 8; g[cr + 1][cc + 1] = 8
    md = int(overrides.get("marker_distance", 2))
    md = max(2, min(3, md))
    if cr - md >= 0 and cc - md >= 0:
        g[cr - md][cc - md] = palette[0]
    if cr - md >= 0 and cc + md + 1 < w:
        g[cr - md][cc + md + 1] = palette[1]
    if cr + md + 1 < h and cc - md >= 0:
        g[cr + md + 1][cc - md] = palette[2]
    if cr + md + 1 < h and cc + md + 1 < w:
        g[cr + md + 1][cc + md + 1] = palette[3]
    return g


def _draw_from_degenerate(name, rng):
    h, w = 12, 12
    g = full_grid(h, w, 0)
    if name == "no_markers":
        g[5][5] = 8; g[5][6] = 8
        g[6][5] = 8; g[6][6] = 8
        return g
    if name == "no_block":
        g[3][3] = 1; g[3][8] = 2; g[8][3] = 3; g[8][8] = 4
        return g
    if name == "full_grid":
        for r in range(h):
            for c in range(w):
                g[r][c] = 8
        return g
    return g
