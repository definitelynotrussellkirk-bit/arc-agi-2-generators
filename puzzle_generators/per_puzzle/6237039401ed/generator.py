"""Generator for additional_scaffolded:E5.

Solid 2x2 color-5 squares are recolored to color 1.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_blocks,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_blocks, distractor_only, single_cell.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import draw_rect, full_grid

GENERATOR_ID = "6237039401ed"
VERSION = "1.1.0"
TASK_ID = "6237039401ed"
SUMMARY = "Solid 2x2 color-5 squares are recolored to color 1."

INVARIANTS = [
    "background is 0",
    "at least one full 2x2 block of color 5 is present",
    "optional color-5 distractors do not themselves contain a full 2x2 block",
    "2x2 blocks are separated so their neighborhoods remain distinct",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_blocks", "distractor_only", "single_cell")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 7..12", "valid": "3..18"},
    "grid_w":         {"type": "int", "default": "rng 7..12", "valid": "3..18"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_blocks":       {"type": "int", "default": "rng 2..5", "valid": "1..10"},
    "palette_size":   {"type": "int", "default": "1", "valid": "1..1"},
    "position_bias":  {"type": "str", "default": "isolated_5_squares",
                       "valid": "isolated_5_squares"},
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
        n_blocks = ctx.draw_int("n_blocks", 2, 3)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 10, 12)
        w = ctx.draw_int("grid_w", 10, 12)
        n_blocks = ctx.draw_int("n_blocks", 4, 5)
    else:
        h = ctx.draw_int("grid_h", 7, 12)
        w = ctx.draw_int("grid_w", 7, 12)
        n_blocks = ctx.draw_int("n_blocks", 2, 5)
    rng = ctx.draw_rng("placement")
    g = full_grid(h, w, 0)
    anchors: list[tuple[int, int]] = []
    for _ in range(180):
        if len(anchors) >= n_blocks:
            break
        r = rng.randint(0, h - 2)
        c = rng.randint(0, w - 2)
        if any(abs(r - rr) < 3 and abs(c - cc) < 3 for rr, cc in anchors):
            continue
        draw_rect(g, r, c, 2, 2, 5)
        anchors.append((r, c))
    if not anchors:
        draw_rect(g, 1, 1, 2, 2, 5)
    # Add a small non-square distractor when there is room.
    for r in range(h - 1):
        for c in range(w - 1):
            if g[r][c] == g[r + 1][c] == g[r][c + 1] == 0:
                g[r][c] = 5
                g[r + 1][c] = 5
                g[r][c + 1] = 5
                return g
    return g


def _draw_from_degenerate(name, rng):
    h, w = 9, 9
    g = full_grid(h, w, 0)
    if name == "no_blocks":
        # blank → no 5-squares to recolor
        return g
    if name == "distractor_only":
        # only L-shaped distractors (no full 2x2) → rule has no fire site
        for r, c in [(1, 1), (1, 2), (2, 1)]: g[r][c] = 5
        for r, c in [(5, 5), (5, 6), (6, 6)]: g[r][c] = 5
        return g
    if name == "single_cell":
        # single 5-cells → not 2x2 squares, rule won't fire
        g[2][2] = 5
        g[5][5] = 5
        return g
    return g
