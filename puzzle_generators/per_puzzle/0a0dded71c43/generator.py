"""Generator for arc_additional_puzzle_bank_volume13:E87.

One-cell gaps between aligned magenta endpoints are filled orange.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_gaps,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_gaps, no_endpoints, gap_already_filled.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "0a0dded71c43"
VERSION = "1.1.0"
TASK_ID = "0a0dded71c43"
SUMMARY = "One-cell gaps between aligned magenta endpoints are filled orange."

INVARIANTS = [
    "background is 0",
    "each target gap has magenta endpoints exactly two cells apart",
    "horizontal and vertical orientations can appear",
    "gap patterns are separated to avoid accidental longer interactions",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_gaps", "no_endpoints", "gap_already_filled")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 7..12", "valid": "3..18"},
    "grid_w":         {"type": "int", "default": "rng 7..12", "valid": "3..18"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_gaps":         {"type": "int", "default": "rng 3..6", "valid": "1..12"},
    "palette_size":   {"type": "int", "default": "1", "valid": "1..1"},
    "position_bias":  {"type": "str", "default": "magenta_endpoint_pairs_2apart",
                       "valid": "magenta_endpoint_pairs_2apart"},
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
        n_gaps = ctx.draw_int("n_gaps", 2, 3)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 10, 12)
        w = ctx.draw_int("grid_w", 10, 12)
        n_gaps = ctx.draw_int("n_gaps", 5, 6)
    else:
        h = ctx.draw_int("grid_h", 7, 12)
        w = ctx.draw_int("grid_w", 7, 12)
        n_gaps = ctx.draw_int("n_gaps", 3, 6)
    rng = ctx.draw_rng("placement")
    g = full_grid(h, w, 0)
    centers: list[tuple[int, int]] = []
    for _ in range(220):
        if len(centers) >= n_gaps:
            break
        vertical = rng.choice([False, True])
        if vertical:
            r = rng.randint(1, h - 2)
            c = rng.randint(0, w - 1)
            cells = [(r - 1, c), (r + 1, c)]
        else:
            r = rng.randint(0, h - 1)
            c = rng.randint(1, w - 2)
            cells = [(r, c - 1), (r, c + 1)]
        if any(abs(r - rr) < 3 and abs(c - cc) < 3 for rr, cc in centers):
            continue
        if any(g[rr][cc] != 0 for rr, cc in cells):
            continue
        for rr, cc in cells:
            g[rr][cc] = 6
        centers.append((r, c))
    if not centers:
        g[2][1] = 6
        g[2][3] = 6
    return g


def _draw_from_degenerate(name, rng):
    h, w = 8, 9
    g = full_grid(h, w, 0)
    if name == "no_gaps":
        # blank → no endpoint pairs to bridge
        return g
    if name == "no_endpoints":
        # only single magenta cells → no pair → no gap to fill
        g[2][2] = 6
        g[5][7] = 6
        return g
    if name == "gap_already_filled":
        # endpoints with the midpoint already non-zero → rule has no work
        g[3][1] = 6; g[3][2] = 4; g[3][3] = 6
        return g
    return g
