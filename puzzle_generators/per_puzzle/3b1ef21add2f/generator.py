"""Generator for additional_bank:E1 — recolor full 2x2 red blocks to green.

Rule: full 2x2 blocks of color 2 are recolored to color 3.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_blocks,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_full_blocks, all_distractors, blocks_touching.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import draw_rect, full_grid

GENERATOR_ID = "3b1ef21add2f"
VERSION = "1.1.0"
TASK_ID = "3b1ef21add2f"
SUMMARY = "Full 2x2 red blocks are recolored to green."

INVARIANTS = [
    "background is 0",
    "at least one full 2x2 block of color 2 is present",
    "some optional red distractors are not full 2x2 blocks",
    "red blocks are separated so their 2x2 neighborhoods are clear",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_full_blocks", "all_distractors", "blocks_touching")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 7..11", "valid": "5..16"},
    "grid_w":         {"type": "int", "default": "rng 7..11", "valid": "5..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_blocks":       {"type": "int", "default": "rng 2..4", "valid": "1..8"},
    "palette_size":   {"type": "int", "default": "1", "valid": "1..1"},
    "position_bias":  {"type": "str", "default": "spaced_2x2_red_blocks",
                       "valid": "spaced_2x2_red_blocks"},
    "n_distinct_colors": {"type": "int", "default": "1", "valid": "1..1"},
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
        h = ctx.draw_int("grid_h", 7, 8)
        w = ctx.draw_int("grid_w", 7, 8)
        n_blocks = ctx.draw_int("n_blocks", 2, 2)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 10, 11)
        w = ctx.draw_int("grid_w", 10, 11)
        n_blocks = ctx.draw_int("n_blocks", 3, 4)
    else:
        h = ctx.draw_int("grid_h", 7, 11)
        w = ctx.draw_int("grid_w", 7, 11)
        n_blocks = ctx.draw_int("n_blocks", 2, 4)
    rng = ctx.draw_rng("placement")
    g = full_grid(h, w, 0)
    boxes: list[tuple[int, int]] = []
    for _ in range(120):
        if len(boxes) >= n_blocks:
            break
        r = rng.randint(0, h - 2)
        c = rng.randint(0, w - 2)
        if any(abs(r - rr) < 3 and abs(c - cc) < 3 for rr, cc in boxes):
            continue
        draw_rect(g, r, c, 2, 2, 2)
        boxes.append((r, c))
    if not boxes:
        draw_rect(g, 0, 0, 2, 2, 2)
    return g


def _draw_from_degenerate(name, rng):
    h, w = 9, 9
    g = full_grid(h, w, 0)
    if name == "no_full_blocks":
        # only L-shapes / lines / singletons of red → no full 2x2 to recolor
        for (r, c) in [(1, 1), (1, 2), (2, 1)]: g[r][c] = 2  # L
        for (r, c) in [(5, 4), (5, 5), (5, 6)]: g[r][c] = 2  # line
        g[7][7] = 2                                            # singleton
        return g
    if name == "all_distractors":
        # similar to above but more distractor variety
        for (r, c) in [(1, 1), (1, 2), (1, 3)]: g[r][c] = 2  # 1x3
        for (r, c) in [(4, 4), (5, 4), (6, 4)]: g[r][c] = 2  # 3x1
        return g
    if name == "blocks_touching":
        # two 2x2 blocks 4-touching → look like one 2x4 to component analysis
        draw_rect(g, 1, 1, 2, 2, 2)
        draw_rect(g, 1, 3, 2, 2, 2)   # adjacent
        return g
    return g
