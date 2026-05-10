"""Generator for puzzle 6cf79266.

Rule: scan grid; whenever an empty 3x3 block is found (not yet
painted), fill it with color 1.

Combinatorial axes (8): grid_h/w, n_empty_blocks, fg_density, fg_color,
position_bias, anchor_corner, asymmetry_force, palette_size.
Degenerates: no_empty_blocks, all_empty, monochrome.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "8d83f9744f6a"
VERSION = "1.1.0"
TASK_ID = "8d83f9744f6a"
SUMMARY = "Sparse 0/3 grid with explicit 3x3 empty blocks; rule paints them 1."

INVARIANTS = [
    "non-bg color is exclusively 3 (the fg_color)",
    ">=1 explicit 3x3 all-0 region (rule paints it)",
    "fg density 40-70% (so blocks are detectable)",
]

POSITION_BIASES = ("scattered", "corners", "row_aligned", "diagonal",
                   "centered")
DEGENERATE_TEXTURES = ("no_empty_blocks", "all_empty", "monochrome")
HELPFUL_TEXTURES = POSITION_BIASES

AXES = {
    "grid_h":         {"type": "int", "default": "rng 14..22", "valid": "10..28"},
    "grid_w":         {"type": "int", "default": "rng 14..22", "valid": "10..28"},
    "n_empty_blocks": {"type": "int", "default": "rng 1..3", "valid": "1..5"},
    "fg_density":     {"type": "float", "default": "rng 0.4..0.7",
                       "valid": "0.3..0.85"},
    "fg_color":       {"type": "color", "default": "3",
                       "valid": "1..9 (≠1)"},
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
        h_lo, h_hi = 10, 13
    elif difficulty == "hard":
        h_lo, h_hi = 22, 28
    else:
        h_lo, h_hi = 14, 22
    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", h_lo, h_hi)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], h, w, rng)
    n_blocks = int(overrides.get("n_empty_blocks",
                                 ctx.draw_int("n_empty_blocks", 1, 3)))
    n_blocks = max(1, min(5, n_blocks))
    fg_density = float(overrides.get("fg_density",
                                     ctx.draw_rng("fg_density")
                                     .uniform(0.4, 0.7)))
    fg_color = int(overrides.get("fg_color", 3))
    if fg_color == 1:
        fg_color = 3
    bias = (overrides.get("texture") or
            overrides.get("position_bias")
            or ctx.draw_choice("position_bias",
                               list(POSITION_BIASES)))
    g = [[fg_color if rng.random() < fg_density else 0
          for _ in range(w)] for _ in range(h)]
    positions = _pick_block_positions(bias, h, w, n_blocks, rng)
    for r0, c0 in positions[:n_blocks]:
        for dr in range(3):
            for dc in range(3):
                if 0 <= r0 + dr < h and 0 <= c0 + dc < w:
                    g[r0 + dr][c0 + dc] = 0
    return g


def _pick_block_positions(bias, h, w, n, rng):
    if bias == "corners":
        corners = [(0, 0), (0, w - 3), (h - 3, 0), (h - 3, w - 3)]
        rng.shuffle(corners)
        return corners
    if bias == "row_aligned":
        r = rng.randint(0, h - 3)
        return [(r, c) for c in range(0, w - 2, 4)]
    if bias == "diagonal":
        return [(i * 4, i * 4) for i in range(min(h // 4, w // 4))]
    if bias == "centered":
        cr, cc = (h - 3) // 2, (w - 3) // 2
        return [(cr, cc), (max(0, cr - 4), cc), (cr, max(0, cc - 4))]
    return [(rng.randint(0, h - 3), rng.randint(0, w - 3))
            for _ in range(n * 2)]


def _draw_from_degenerate(name, h, w, rng):
    g = full_grid(h, w, 0)
    if name == "no_empty_blocks":
        # Densely fill with 3s so no 3x3 empty block exists
        for r in range(h):
            for c in range(w):
                g[r][c] = 3 if rng.random() < 0.95 else 0
        return g
    if name == "all_empty":
        return g
    if name == "monochrome":
        for r in range(h):
            for c in range(w):
                g[r][c] = 3
        return g
    return g
