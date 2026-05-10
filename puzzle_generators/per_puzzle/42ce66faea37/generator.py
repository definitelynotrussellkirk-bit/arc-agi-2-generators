"""Generator for arc_puzzle_bank_eighteenth_21_bundle:easy_126_fill_diagonal_segments_between_matching_endpoints.

Fill 45-degree diagonal segments between matching endpoints.

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: adjacent_endpoints (endpoints of a color are 1 cell apart
→ no segment to fill, only the endpoints exist), axial_endpoints
(endpoints share row/col not diagonal → rule's diagonal filter
excludes them), single_endpoint (only one cell of a color → no pair
to connect).
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "42ce66faea37"
VERSION = "1.1.0"
TASK_ID = "42ce66faea37"

SUMMARY = "Fill 45-degree diagonal segments between matching endpoints."

INVARIANTS = [
    "background is 0",
    "each active color appears exactly twice",
    "the endpoints share a 45-degree diagonal",
    "diagonal segments are separated to avoid overlap",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("adjacent_endpoints", "axial_endpoints", "single_endpoint")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..11", "valid": "5..18"},
    "grid_w":         {"type": "int", "default": "rng 8..11", "valid": "5..18"},
    "segments":       {"type": "int", "default": "rng 2..3", "valid": "1..6"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "palette_size":   {"type": "int", "default": "rng 2..3", "valid": "1..6"},
    "position_bias":  {"type": "str", "default": "diagonal_endpoint_pairs",
                       "valid": "diagonal_endpoint_pairs"},
    "n_distinct_colors": {"type": "int", "default": "rng 2..3", "valid": "1..6"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def _path(r1, c1, r2, c2):
    dr = 1 if r2 > r1 else -1
    dc = 1 if c2 > c1 else -1
    length = abs(r2 - r1)
    return [(r1 + i * dr, c1 + i * dc) for i in range(length + 1)]


def _free(g, cells):
    h, w = len(g), len(g[0])
    for r, c in cells:
        for rr in range(max(0, r - 1), min(h, r + 2)):
            for cc in range(max(0, c - 1), min(w, c + 2)):
                if g[rr][cc] != 0:
                    return False
    return True


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index, version=VERSION,
                  task_id=TASK_ID, difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 8, 8)
        w = ctx.draw_int("grid_w", 8, 8)
        target = ctx.draw_int("segments", 1, 2)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 11, 14)
        w = ctx.draw_int("grid_w", 11, 14)
        target = ctx.draw_int("segments", 3, 5)
    else:
        h = ctx.draw_int("grid_h", 8, 11)
        w = ctx.draw_int("grid_w", 8, 11)
        target = ctx.draw_int("segments", 2, 3)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    colors = rng.sample([1, 2, 3, 4, 5, 6, 7, 8, 9], target)
    placed = 0
    for color in colors:
        for _ in range(160):
            length = rng.randint(2, min(5, h - 1, w - 1))
            dr = rng.choice([-1, 1])
            dc = rng.choice([-1, 1])
            r1_min = 0 if dr > 0 else length
            r1_max = h - 1 - length if dr > 0 else h - 1
            c1_min = 0 if dc > 0 else length
            c1_max = w - 1 - length if dc > 0 else w - 1
            r1 = rng.randint(r1_min, r1_max)
            c1 = rng.randint(c1_min, c1_max)
            r2 = r1 + dr * length
            c2 = c1 + dc * length
            cells = _path(r1, c1, r2, c2)
            if _free(g, cells):
                g[r1][c1] = color
                g[r2][c2] = color
                placed += 1
                break
    if placed == 0:
        raise ValueError("could not place any diagonal endpoint pair")
    return g


def _draw_from_degenerate(name, rng):
    h, w = 9, 9
    g = full_grid(h, w, 0)
    if name == "adjacent_endpoints":
        # Endpoints 1 apart → no segment between them; rule's
        # diagonal-fill leaves the output as just the endpoints.
        g[2][2] = 1; g[3][3] = 1
        g[5][5] = 3; g[6][6] = 3
        return g
    if name == "axial_endpoints":
        # Endpoints share a row/col, not diagonal → rule's
        # diagonal filter excludes them; output equals input.
        g[2][2] = 1; g[2][6] = 1
        g[5][3] = 3; g[8][3] = 3
        return g
    if name == "single_endpoint":
        # Only one cell of a color — rule has no pair to connect.
        g[3][3] = 4
        g[6][7] = 6
        return g
    return g
