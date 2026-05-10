"""Generator for arc_puzzle_bank_21_set20_bundle:easy_p05 — same-color border seeds beam inward.

Rule: each border seed fires a beam of its color inward, stopping at
optional 8-walls.

Combinatorial axes (8): grid_h, grid_w, palette_kind, seed_count, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: no_seeds, all_walls, single_seed.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "079232b060cd"
VERSION = "1.1.0"
TASK_ID = "079232b060cd"
SUMMARY = "Same-color border seeds fire inward through zeros, stopping at optional 8 walls."

INVARIANTS = [
    "background is 0",
    "all non-wall seeds sit on the border and share one color",
    "wall cells use color 8 and may truncate one or more beams",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_seeds", "all_walls", "single_seed")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 7..10", "valid": "5..14"},
    "grid_w":         {"type": "int", "default": "rng 8..12", "valid": "5..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "seed_count":     {"type": "int", "default": "rng 2..4", "valid": "1..8"},
    "palette_size":   {"type": "str", "default": "1 (seed) +1 (wall)", "valid": "2..2"},
    "position_bias":  {"type": "str", "default": "border_seeds_inward_beam",
                       "valid": "border_seeds_inward_beam"},
    "n_distinct_colors": {"type": "int", "default": "2", "valid": "2..2"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def _beam_cells(h, w, r, c):
    if r == 0:
        dr, dc = 1, 0
    elif r == h - 1:
        dr, dc = -1, 0
    elif c == 0:
        dr, dc = 0, 1
    else:
        dr, dc = 0, -1
    cells = []
    rr, cc = r + dr, c + dc
    while 0 <= rr < h and 0 <= cc < w:
        cells.append((rr, cc))
        rr += dr
        cc += dc
    return cells


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index, version=VERSION,
                  task_id=TASK_ID, difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 7, 8)
        w = ctx.draw_int("grid_w", 8, 10)
        seed_count = ctx.draw_int("seed_count", 2, 3)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 10, 13)
        w = ctx.draw_int("grid_w", 12, 15)
        seed_count = ctx.draw_int("seed_count", 4, 6)
    else:
        h = ctx.draw_int("grid_h", 7, 10)
        w = ctx.draw_int("grid_w", 8, 12)
        seed_count = ctx.draw_int("seed_count", 2, 4)
    rng = ctx.draw_rng("layout")
    grid = full_grid(h, w, 0)
    color = rng.choice([1, 2, 3, 4, 5, 6, 7, 9])

    border = (
        [(0, c) for c in range(1, w - 1)]
        + [(h - 1, c) for c in range(1, w - 1)]
        + [(r, 0) for r in range(1, h - 1)]
        + [(r, w - 1) for r in range(1, h - 1)]
    )
    rng.shuffle(border)
    for r, c in border[: min(seed_count, len(border))]:
        grid[r][c] = color
        cells = _beam_cells(h, w, r, c)
        if len(cells) >= 3 and rng.random() < 0.6:
            wr, wc = rng.choice(cells[1:])
            grid[wr][wc] = 8
    return grid


def _draw_from_degenerate(name, rng):
    h, w = 8, 10
    g = full_grid(h, w, 0)
    if name == "no_seeds":
        # Empty grid — no border seed to fire a beam.
        return g
    if name == "all_walls":
        # The entire interior is filled with 8-walls, so even if seeds existed
        # the beams would be immediately blocked. Rule degenerates to identity.
        for r in range(1, h - 1):
            for c in range(1, w - 1):
                g[r][c] = 8
        g[0][3] = 4; g[h - 1][6] = 4
        return g
    if name == "single_seed":
        # Just one seed — minimal evidence of the rule.
        g[0][3] = 4
        return g
    return g
