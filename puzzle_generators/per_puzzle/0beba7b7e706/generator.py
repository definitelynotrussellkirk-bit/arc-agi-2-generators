"""Generator for 18b:hard_126 — centered transformed stamp count map.

Rule: prototype occupies subgrid (0,0)-(2,2) (3x3). Cells with values
in {1,2,3,4} elsewhere are markers; output stamps the prototype
transformed by code at each marker position (centered), with overlap
counts.

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: no_prototype, no_markers, prototype_blank.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "0beba7b7e706"
VERSION = "1.1.0"
TASK_ID = "0beba7b7e706"
SUMMARY = "3x3 prototype at top-left + 1-3 markers in {1,2,3,4} elsewhere."

INVARIANTS = [
    "background is 0",
    "subgrid (0,0)-(2,2) holds the prototype: a binary pattern in some non-bg color",
    "1-3 marker cells with values in {1, 2, 3, 4} placed in rows 4+ (away from prototype)",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_prototype", "no_markers", "prototype_blank")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 9..11", "valid": "8..14"},
    "grid_w":         {"type": "int", "default": "rng 9..11", "valid": "8..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "palette_size":   {"type": "int", "default": "rng 2..4", "valid": "2..5"},
    "position_bias":  {"type": "str", "default": "prototype_top_left_markers_below",
                       "valid": "prototype_top_left_markers_below"},
    "n_distinct_colors": {"type": "int", "default": "rng 2..4", "valid": "2..5"},
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
        w = ctx.draw_int("grid_w", 9, 9)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 11, 14)
        w = ctx.draw_int("grid_w", 11, 14)
    else:
        h = ctx.draw_int("grid_h", 9, 11)
        w = ctx.draw_int("grid_w", 9, 11)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    proto_color = rng.choice([5, 6, 7, 8, 9])
    cells_proto = [(r, c) for r in range(3) for c in range(3)]
    n_proto = rng.randint(3, 5)
    for r, c in rng.sample(cells_proto, n_proto):
        g[r][c] = proto_color
    n_markers = rng.randint(1, 3)
    placed = 0; attempts = 0
    while placed < n_markers and attempts < 60:
        attempts += 1
        r = rng.randint(4, h - 2); c = rng.randint(2, w - 2)
        if g[r][c] != 0: continue
        bad = False
        for dr, dc in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            rr, cc = r + dr, c + dc
            if 0 <= rr < h and 0 <= cc < w and g[rr][cc] != 0:
                bad = True; break
        if bad: continue
        g[r][c] = rng.randint(1, 4)
        placed += 1
    return g


def _draw_from_degenerate(name, rng):
    h, w = 10, 10
    g = full_grid(h, w, 0)
    if name == "no_prototype":
        # Prototype subgrid (0,0)-(2,2) is empty — rule has no shape
        # to stamp at marker positions.
        g[5][5] = 2
        g[7][3] = 4
        return g
    if name == "no_markers":
        # Prototype present but no {1,2,3,4} markers — rule has no
        # stamp positions.
        for r, c in [(0, 0), (1, 1), (2, 0), (2, 2)]: g[r][c] = 6
        return g
    if name == "prototype_blank":
        # Prototype subgrid is fully empty (no cells set) but markers
        # exist — rule's stamp pattern has zero on-cells, output
        # equals input.
        g[5][5] = 2
        g[7][3] = 4
        return g
    return g
