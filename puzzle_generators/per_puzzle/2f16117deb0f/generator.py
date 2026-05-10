"""Generator for arc_additional_puzzles_21_set17_bundle:M113 — palette-lift bank entries via selector.

Rule:
  Row 0 = legend (K non-zero colors).
  Row 1 = selector (K keys in {1..K}).
  Row 3 = bank keys (numbers 1..K placed at separated cols).
  Rows 4-5 = 2x2 bank entries directly under each key.
For each selector key, look up its bank entry, palette-lift symbols
1..K → legend[0..K-1], and stack entries horizontally.

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, K, texture.
Degenerates: no_legend, no_selector, no_bank.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid
from puzzle_generators.helpers.palette import random_palette

GENERATOR_ID = "2f16117deb0f"
VERSION = "1.1.0"
TASK_ID = "2f16117deb0f"
SUMMARY = "Legend + selector + 2x2 bank entries (3 entries) for palette-lifted horizontal concat."

INVARIANTS = [
    "row 0 holds K non-zero legend colors at columns 0..K-1",
    "row 1 holds K selector keys in {1..K} at columns 0..K-1",
    "row 2 is all zeros",
    "row 3 holds keys 1..K at non-overlapping column positions (col triples 2 wide)",
    "rows 4-5 hold 2x2 bank entries at the same column triples, with symbols in {0..K}",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_legend", "no_selector", "no_bank")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "K":              {"type": "int", "default": "rng 2..3", "valid": "2..3"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "palette_size":   {"type": "int", "default": "= K", "valid": "2..3"},
    "position_bias":  {"type": "str", "default": "legend_selector_bank_layout",
                       "valid": "legend_selector_bank_layout"},
    "n_distinct_colors": {"type": "int", "default": "= K", "valid": "2..3"},
    "density":        {"type": "str", "default": "balanced", "valid": "balanced"},
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
        K = ctx.draw_int("K", 2, 2)
    elif difficulty == "hard":
        K = ctx.draw_int("K", 3, 3)
    else:
        K = ctx.draw_int("K", 2, 3)
    rng = ctx.draw_rng("layout")
    h = 6
    w = 3 * K + (K - 1) + 2
    g = full_grid(h, w, 0)
    legend = list(random_palette(rng, K))
    for i, color in enumerate(legend):
        g[0][i] = color
    selector = [rng.randint(1, K) for _ in range(K)]
    for i, k in enumerate(selector):
        g[1][i] = k
    keys = list(range(1, K + 1))
    rng.shuffle(keys)
    cols = []
    next_c = 0
    for k in keys:
        c0 = next_c
        g[3][c0] = k
        for ir in range(2):
            for ic in range(2):
                if rng.random() < 0.6:
                    g[4 + ir][c0 + ic] = rng.randint(1, K)
        cols.append(c0)
        next_c = c0 + 3
    return g


def _draw_from_degenerate(name, rng):
    K = 2
    h = 6
    w = 3 * K + (K - 1) + 2
    g = full_grid(h, w, 0)
    if name == "no_legend":
        # Selector + bank but no row-0 legend — rule has no
        # palette-lift mapping; symbol→color step is undefined.
        g[1][0] = 1; g[1][1] = 2
        g[3][0] = 1; g[4][0] = 1; g[4][1] = 2
        g[3][3] = 2; g[4][3] = 1; g[5][3] = 2
        return g
    if name == "no_selector":
        # Legend + bank but row 1 is empty — rule has no keys to look up.
        g[0][0] = 4; g[0][1] = 6
        g[3][0] = 1; g[4][0] = 1; g[4][1] = 2
        g[3][3] = 2; g[4][3] = 1; g[5][3] = 2
        return g
    if name == "no_bank":
        # Legend + selector but no bank entries below — rule has no
        # entries to look up.
        g[0][0] = 4; g[0][1] = 6
        g[1][0] = 1; g[1][1] = 2
        return g
    return g
