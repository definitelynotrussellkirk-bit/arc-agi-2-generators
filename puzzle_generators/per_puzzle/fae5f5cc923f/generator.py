"""Generator for 95990924.

Rule: each solid 2x2 block of 5s gets corner markers: 1=BR, 2=BL, 3=TR,
4=TL diagonal.

Combinatorial axes (8): grid_h/w, n_blocks, block_separation,
position_bias, palette_kind, anchor_corner, asymmetry_force, palette_size.
Degenerates: no_block, touching_blocks, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, draw_rect

GENERATOR_ID = "fae5f5cc923f"
VERSION = "1.1.0"
TASK_ID = "fae5f5cc923f"
SUMMARY = "1-3 solid 2x2 5-blocks, well-separated, with >=2 cells of buffer."

INVARIANTS = [
    "1-3 solid 2x2 blocks of color 5",
    "each block has >=2 cells of buffer to all grid edges",
    "blocks are non-overlapping and don't touch",
]

POSITION_BIASES = ("scattered", "diagonal", "row_aligned", "centered")
PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_block", "touching_blocks", "full_grid")
HELPFUL_TEXTURES = POSITION_BIASES

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..11", "valid": "6..14"},
    "grid_w":         {"type": "int", "default": "rng 8..11", "valid": "6..14"},
    "n_blocks":       {"type": "int", "default": "rng 1..3", "valid": "1..4"},
    "block_separation":{"type": "int", "default": "5", "valid": "3..8"},
    "position_bias":  {"type": "str", "default": "rng helpful",
                       "valid": "|".join(POSITION_BIASES)},
    "palette_kind":   {"type": "str", "default": "rng",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "1", "valid": "1"},
    "texture":        {"type": "str", "default": "alias for position_bias",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], rng)
    if difficulty == "easy":
        h_lo, h_hi = 6, 8
        nb_lo, nb_hi = 1, 1
    elif difficulty == "hard":
        h_lo, h_hi = 12, 14
        nb_lo, nb_hi = 3, 4
    else:
        h_lo, h_hi = 8, 11
        nb_lo, nb_hi = 1, 3
    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", h_lo, h_hi)
    g = full_grid(h, w, 0)
    n_blocks = int(overrides.get("n_blocks",
                                 ctx.draw_int("n_blocks", nb_lo, nb_hi)))
    n_blocks = max(1, min(4, n_blocks))
    bias = (overrides.get("texture") or
            overrides.get("position_bias")
            or ctx.draw_choice("position_bias", list(POSITION_BIASES)))
    sep = int(overrides.get("block_separation", 5))
    placed = []
    for _try in range(120):
        if len(placed) >= n_blocks:
            break
        r0, c0 = _pick_block_pos(bias, h, w, len(placed), placed, rng)
        r0 = max(2, min(r0, h - 4))
        c0 = max(2, min(c0, w - 4))
        if any(abs(r0 - pr) < sep and abs(c0 - pc) < sep for pr, pc in placed):
            continue
        draw_rect(g, r0, c0, 2, 2, 5)
        placed.append((r0, c0))
    return g


def _pick_block_pos(bias, h, w, idx, placed, rng):
    if bias == "diagonal":
        steps = idx + 1
        r0 = 2 + (h - 6) * steps // max(1, idx + 2)
        c0 = 2 + (w - 6) * steps // max(1, idx + 2)
    elif bias == "row_aligned":
        r0 = h // 2 + rng.randint(-1, 1)
        c0 = 2 + idx * (w // 4)
    elif bias == "centered":
        r0 = max(2, h // 2 - 1 + rng.randint(-1, 1))
        c0 = max(2, w // 2 - 1 + rng.randint(-1, 1))
    else:
        r0 = rng.randint(2, h - 4)
        c0 = rng.randint(2, w - 4)
    return r0, c0


def _draw_from_degenerate(name, rng):
    h, w = 10, 10
    g = full_grid(h, w, 0)
    if name == "no_block":
        g[5][5] = 3
        return g
    if name == "touching_blocks":
        draw_rect(g, 3, 3, 2, 2, 5)
        draw_rect(g, 3, 5, 2, 2, 5)
        return g
    if name == "full_grid":
        for r in range(h):
            for c in range(w):
                g[r][c] = 5
        return g
    return g
