"""Generator for v1_e_m_h_keys:E3 — fill 3x3 hollow color-4 center with color 6.

Rule: each 3x3 block where all 8 perimeter cells are color-4 and the center
is 0 has its center filled with color 6.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_blocks,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_blocks, solid_squares, center_already_filled.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "7494855fa379"
VERSION = "1.1.0"
TASK_ID = "7494855fa379"

SUMMARY = "1-2 3x3 hollow color-4 blocks (border filled, center 0)."

INVARIANTS = [
    "background is 0",
    "1-2 hollow 3x3 blocks of color-4 (8 perimeter cells, 0 center)",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_blocks", "solid_squares", "center_already_filled")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 5..7", "valid": "4..10"},
    "grid_w":         {"type": "int", "default": "rng 7..9", "valid": "5..12"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_blocks":       {"type": "int", "default": "rng 1..2", "valid": "1..3"},
    "palette_size":   {"type": "int", "default": "1", "valid": "1..2"},
    "position_bias":  {"type": "str", "default": "spaced_3x3_hollow_blocks",
                       "valid": "spaced_3x3_hollow_blocks"},
    "n_distinct_colors": {"type": "int", "default": "1", "valid": "1..2"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def _free(g, r1, c1, r2, c2):
    h, w = len(g), len(g[0])
    if r1 < 0 or c1 < 0 or r2 >= h or c2 >= w: return False
    for r in range(max(0, r1 - 1), min(h, r2 + 2)):
        for c in range(max(0, c1 - 1), min(w, c2 + 2)):
            if g[r][c] != 0: return False
    return True


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 5, 5)
        w = ctx.draw_int("grid_w", 7, 7)
        n = ctx.draw_int("n_blocks", 1, 1)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 6, 7)
        w = ctx.draw_int("grid_w", 8, 9)
        n = ctx.draw_int("n_blocks", 2, 2)
    else:
        h = ctx.draw_int("grid_h", 5, 7)
        w = ctx.draw_int("grid_w", 7, 9)
        n = ctx.draw_int("n_blocks", 1, 2)
    rng = ctx.draw_rng("layout")

    for outer in range(40):
        g = full_grid(h, w, 0)
        ok = True
        for _ in range(n):
            placed = False
            for _ in range(80):
                r0 = rng.randint(0, h - 3); c0 = rng.randint(0, w - 3)
                if not _free(g, r0, c0, r0 + 2, c0 + 2): continue
                for dr in range(3):
                    for dc in range(3):
                        if (dr, dc) != (1, 1):
                            g[r0 + dr][c0 + dc] = 4
                placed = True; break
            if not placed:
                ok = False; break
        if ok:
            return g
    raise ValueError("could not realize E3 layout")


def _draw_from_degenerate(name, rng):
    h, w = 6, 8
    g = full_grid(h, w, 0)
    if name == "no_blocks":
        # blank → no 3x3 blocks, rule fires zero times
        return g
    if name == "solid_squares":
        # solid 3x3 (center already 4) → predicate "center is 0" fails
        for dr in range(3):
            for dc in range(3): g[1 + dr][1 + dc] = 4
        return g
    if name == "center_already_filled":
        # hollow ring with center already non-zero (and not 6) → predicate fails
        for dr in range(3):
            for dc in range(3):
                if (dr, dc) != (1, 1): g[1 + dr][1 + dc] = 4
        g[2][2] = 8  # wrong color in center
        return g
    return g
