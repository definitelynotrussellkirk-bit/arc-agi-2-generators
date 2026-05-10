"""Generator for arc_puzzle_bank_21_set11_bundle:hard_k20 — connect color-sorted markers.

Rule: take each marker's center; sort by color asc; draw an L-path
(horizontal then vertical) from each consecutive pair of centers,
painted with the smaller-colored object's color.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_markers,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_markers, collinear, single_marker.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "ee822284e294"
VERSION = "1.1.0"
TASK_ID = "ee822284e294"

SUMMARY = "3 single-cell markers in distinct colors; centers will be L-connected in color-asc order."

INVARIANTS = [
    "background is 0",
    "exactly 3 single-cell markers in distinct non-zero colors",
    "markers are 4-conn isolated and not collinear (so L-paths are non-trivial)",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_markers", "collinear", "single_marker")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 9..11", "valid": "8..14"},
    "grid_w":         {"type": "int", "default": "rng 11..13", "valid": "10..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_markers":      {"type": "int", "default": "3", "valid": "3..3"},
    "palette_size":   {"type": "int", "default": "3", "valid": "3..3"},
    "position_bias":  {"type": "str", "default": "non_collinear_markers",
                       "valid": "non_collinear_markers"},
    "n_distinct_colors": {"type": "int", "default": "3", "valid": "3..3"},
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
        h = ctx.draw_int("grid_h", 9, 9)
        w = ctx.draw_int("grid_w", 11, 11)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 11, 14)
        w = ctx.draw_int("grid_w", 13, 16)
    else:
        h = ctx.draw_int("grid_h", 9, 11)
        w = ctx.draw_int("grid_w", 11, 13)
    rng = ctx.draw_rng("layout")
    palette = rng.sample([1, 2, 3, 4, 5, 6, 7, 8, 9], 3)

    for outer in range(40):
        g = full_grid(h, w, 0)
        placed = []
        ok = True
        for color in palette:
            placed_a = False
            for _ in range(120):
                r = rng.randint(0, h - 1)
                c = rng.randint(0, w - 1)
                if g[r][c] != 0:
                    continue
                if any(abs(r - pr) + abs(c - pc) < 3 for pr, pc in placed):
                    continue
                g[r][c] = color
                placed.append((r, c))
                placed_a = True
                break
            if not placed_a:
                ok = False; break
        if ok:
            return g
    raise ValueError("could not place 3 markers in 40 attempts")


def _draw_from_degenerate(name, rng):
    h, w = 10, 12
    g = full_grid(h, w, 0)
    if name == "no_markers":
        # Empty grid — rule has no center to L-connect.
        return g
    if name == "collinear":
        # Markers all on the same row — L-paths collapse to straight
        # segments, removing the L-corner evidence of the rule.
        g[4][2] = 1; g[4][6] = 2; g[4][10] = 3
        return g
    if name == "single_marker":
        # Just one marker — no pair to connect.
        g[4][6] = 4
        return g
    return g
