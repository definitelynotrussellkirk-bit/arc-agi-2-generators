"""Generator for arc_puzzle_bank_seventh21:M47.

The first two rows define source-to-target color mappings. Body cells use the
source colors and are recolored by the rule while the legend stays unchanged.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_maps,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_legend, no_body, body_unknown_source.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "f6f10283c81b"
VERSION = "1.1.0"
TASK_ID = "f6f10283c81b"
SUMMARY = "Two legend rows remap body colors from source palette to target palette."

INVARIANTS = [
    "row 0 contains source colors at legend columns",
    "row 1 contains the target color for each same-column source",
    "rows below the legend contain only source colors and background",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_legend", "no_body", "body_unknown_source")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..10", "valid": "5..16"},
    "grid_w":         {"type": "int", "default": "rng 8..12", "valid": "5..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_maps":         {"type": "int", "default": "rng 3..4", "valid": "1..4"},
    "palette_size":   {"type": "int", "default": "rng 6..8", "valid": "2..9"},
    "position_bias":  {"type": "str", "default": "two_legend_rows_plus_body",
                       "valid": "two_legend_rows_plus_body"},
    "n_distinct_colors": {"type": "int", "default": "rng 6..8", "valid": "2..9"},
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
        h = ctx.draw_int("grid_h", 8, 8)
        w = ctx.draw_int("grid_w", 8, 9)
        n_maps = min(ctx.draw_int("n_maps", 2, 3), w)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 10, 12)
        n_maps = min(ctx.draw_int("n_maps", 3, 4), w)
    else:
        h = ctx.draw_int("grid_h", 8, 10)
        w = ctx.draw_int("grid_w", 8, 12)
        n_maps = min(ctx.draw_int("n_maps", 3, 4), w)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    cols = sorted(rng.sample(range(w), n_maps))
    sources = rng.sample([1, 2, 3, 4, 5], n_maps)
    targets = rng.sample([6, 7, 8, 9], n_maps)
    for col, src, dst in zip(cols, sources, targets):
        g[0][col] = src
        g[1][col] = dst
    for src in sources:
        placed = False
        while not placed:
            r = rng.randint(3, h - 1)
            c = rng.randint(0, w - 1)
            if g[r][c] == 0:
                g[r][c] = src
                placed = True
    for r in range(3, h):
        for c in range(w):
            if g[r][c] == 0 and rng.random() < 0.32:
                g[r][c] = rng.choice(sources)
    return g


def _draw_from_degenerate(name, rng):
    h, w = 9, 10
    g = full_grid(h, w, 0)
    if name == "no_legend":
        # body has source colors but no legend → no remap mapping defined
        g[3][2] = 1; g[5][6] = 2; g[7][3] = 3
        return g
    if name == "no_body":
        # legend present but body is empty → nothing to recolor
        for col, src, dst in [(1, 1, 6), (3, 2, 7), (5, 3, 8)]:
            g[0][col] = src; g[1][col] = dst
        return g
    if name == "body_unknown_source":
        # body contains colors not in legend's source set → no mapping for them
        g[0][1] = 1; g[1][1] = 6
        g[3][2] = 4  # 4 is not in legend sources
        g[5][6] = 5
        return g
    return g
