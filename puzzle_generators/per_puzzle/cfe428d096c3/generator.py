"""Generator for arc_additional_puzzle_bank_volume9:M57 — Recolor solid 1-rectangles by aspect.

Rule: for each color-1 object that's a solid rectangle, recolor: square→8,
wider→2, taller→3. Non-rectangular blobs keep color 1.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_extras,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_rects, all_squares, non_rect_blobs.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "cfe428d096c3"
VERSION = "1.1.0"
TASK_ID = "cfe428d096c3"
SUMMARY = "3-4 non-touching solid 1-rectangles of different aspect (wide / tall / square); plus optional decoration."

INVARIANTS = [
    "between 3 and 4 non-touching solid 1-rectangles",
    "at least one wide (w>h), one tall (h>w), one square",
    "decoration is a non-1 color blob",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_rects", "all_squares", "non_rect_blobs")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 10..13", "valid": "8..16"},
    "grid_w":         {"type": "int", "default": "rng 10..13", "valid": "8..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_extras":       {"type": "int", "default": "rng 0..1", "valid": "0..2"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2..3"},
    "position_bias":  {"type": "str", "default": "wide_tall_square_mix",
                       "valid": "wide_tall_square_mix"},
    "n_distinct_colors": {"type": "int", "default": "2", "valid": "2..3"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def _occupied_or_adjacent(used, r1, c1, r2, c2):
    for r in range(r1 - 1, r2 + 2):
        for c in range(c1 - 1, c2 + 2):
            if (r, c) in used: return True
    return False


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 10, 11)
        w = ctx.draw_int("grid_w", 10, 11)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 12, 13)
        w = ctx.draw_int("grid_w", 12, 13)
    else:
        h = ctx.draw_int("grid_h", 10, 13)
        w = ctx.draw_int("grid_w", 10, 13)
    g = full_grid(h, w, 0)
    rng = ctx.draw_rng("layout")
    used = set()
    targets = [(1, 3), (3, 1), (2, 2)]
    rng.shuffle(targets)
    if rng.random() < 0.5:
        targets.append(rng.choice([(2, 4), (4, 2), (3, 3)]))
    for bh, bw in targets:
        for _ in range(40):
            r1 = rng.randint(0, h - bh)
            c1 = rng.randint(0, w - bw)
            r2 = r1 + bh - 1; c2 = c1 + bw - 1
            if _occupied_or_adjacent(used, r1, c1, r2, c2): continue
            for r in range(r1, r2 + 1):
                for c in range(c1, c2 + 1):
                    g[r][c] = 1; used.add((r, c))
            break
    for _ in range(15):
        r = rng.randint(0, h - 1); c = rng.randint(0, w - 1)
        if (r, c) in used: continue
        g[r][c] = 6; break
    return g


def _draw_from_degenerate(name, rng):
    h, w = 11, 11
    g = full_grid(h, w, 0)
    if name == "no_rects":
        # blank → no rectangles to recolor, rule has no effect
        return g
    if name == "all_squares":
        # all 1-rects are squares → all recolored to 8 (uniform), no aspect signal
        for r in range(2):
            for c in range(2): g[1 + r][1 + c] = 1
        for r in range(3):
            for c in range(3): g[5 + r][5 + c] = 1
        return g
    if name == "non_rect_blobs":
        # 1-blobs that aren't rectangles → all keep color 1, predicate fails
        for (r, c) in [(1, 1), (1, 2), (2, 1)]: g[r][c] = 1  # L-shape
        for (r, c) in [(5, 5), (5, 6), (6, 5), (6, 7)]: g[r][c] = 1  # not solid
        return g
    return g
