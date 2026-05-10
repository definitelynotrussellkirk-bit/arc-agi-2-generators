"""Generator for arc_puzzle_bank_21_set5_s:S5_M1 — quadrant palette summary.

Rule: divide grid into 4 quadrants. For each quadrant, find the
non-zero color present (if any). Output is a 2x2 grid where each cell
holds the color of the corresponding quadrant (0 if empty).

Combinatorial axes (8): half_h, half_w, palette_kind, blob_size,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: empty_quadrants, multi_color_quadrant, all_same_color.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid
from puzzle_generators.helpers.blobs import grow_blob

GENERATOR_ID = "31e0316dace3"
VERSION = "1.1.0"
TASK_ID = "31e0316dace3"
SUMMARY = "One small blob per quadrant, each in a distinct color."

INVARIANTS = [
    "background is 0",
    "grid h, w are even (so quadrants are well-defined)",
    "exactly one non-zero color per quadrant; quadrants have distinct colors",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("empty_quadrants", "multi_color_quadrant", "all_same_color")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "half_h":         {"type": "int", "default": "rng 4..5", "valid": "3..6"},
    "half_w":         {"type": "int", "default": "rng 4..5", "valid": "3..6"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "blob_size":      {"type": "int", "default": "rng 2..4", "valid": "1..6"},
    "palette_size":   {"type": "int", "default": "4", "valid": "4..4"},
    "position_bias":  {"type": "str", "default": "one_blob_per_quadrant",
                       "valid": "one_blob_per_quadrant"},
    "n_distinct_colors": {"type": "int", "default": "4", "valid": "4..4"},
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
        hh = ctx.draw_int("half_h", 4, 4)
        hw = ctx.draw_int("half_w", 4, 4)
    elif difficulty == "hard":
        hh = ctx.draw_int("half_h", 5, 5)
        hw = ctx.draw_int("half_w", 5, 5)
    else:
        hh = ctx.draw_int("half_h", 4, 5)
        hw = ctx.draw_int("half_w", 4, 5)
    h = hh * 2
    w = hw * 2
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    palette = rng.sample([1, 2, 3, 4, 5, 6, 7, 8, 9], 4)
    quads = [(0, 0, hh, hw), (0, hw, hh, w), (hh, 0, h, hw), (hh, hw, h, w)]
    used: set[tuple[int, int]] = set()
    for (r1, c1, r2, c2), color in zip(quads, palette):
        for _ in range(40):
            sz = rng.randint(2, 4)
            qh, qw = r2 - r1, c2 - c1
            cells = grow_blob(rng, qh, qw, set(), sz, max_attempts=20)
            if cells is None:
                continue
            shifted = {(r + r1, c + c1) for r, c in cells}
            if any(p in used for p in shifted):
                continue
            for r, c in shifted:
                g[r][c] = color
            used |= shifted
            break
    return g


def _draw_from_degenerate(name, rng):
    h, w = 8, 8
    g = full_grid(h, w, 0)
    if name == "empty_quadrants":
        # only 1-2 quadrants have blobs → others undefined (0)
        g[1][1] = 4; g[1][2] = 4
        return g
    if name == "multi_color_quadrant":
        # one quadrant has 2 distinct colors → ambiguous summary
        g[1][1] = 4; g[2][1] = 6
        g[1][5] = 7; g[2][5] = 7
        g[5][1] = 8; g[5][2] = 8
        g[5][5] = 9; g[5][6] = 9
        return g
    if name == "all_same_color":
        # all quadrants share one color → 2x2 summary is monochrome
        for (r, c) in [(1, 1), (1, 5), (5, 1), (5, 5)]:
            g[r][c] = 4; g[r][c + 1] = 4
        return g
    return g
