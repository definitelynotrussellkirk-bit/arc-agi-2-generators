"""Generator for arc_additional_puzzles_21_set17_bundle:H113 — palette-lift matrix with commands.

Rule: row 0 holds 3 palette colors. Rows 1-2 cols 0-1 are selectors (4 of them
referencing bank keys). Rows 3-4 cols 0-1 are transform commands. Row 6 has
bank keys; rows 7-9 hold 3x3 templates anchored at each key's column. For each
of 4 selector cells, look up the template, apply its transform, recolor with
the palette, and assemble into a 6x6 2x2 mosaic.

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: no_palette (row 0 empty → rule's color-lift map is
empty); no_bank (row 6 / template area empty → rule's selectors
have no targets); selector_unmatched (selector references key not
present in bank → rule's lookup returns nothing).
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "48e1e7f40749"
VERSION = "1.1.0"
TASK_ID = "48e1e7f40749"

SUMMARY = "Row-0 palette + 2x2 selector + 2x2 commands + bank of 3 keyed 3x3 templates."

INVARIANTS = [
    "background is 0",
    "row 0 has 3 distinct non-zero palette colors at cols 0, 1, 2 (rest 0)",
    "rows 1-2 cols 0-1 hold 4 selector keys (each in {1, 2, 3} matching a bank key)",
    "rows 3-4 cols 0-1 hold 4 transform commands (codes 0..5)",
    "row 6 has 3 distinct bank keys (1, 2, 3) at distinct columns spaced 4 apart",
    "rows 7-9 hold three 3x3 templates anchored at each bank key column",
    "rest of the grid is 0",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_palette", "no_bank", "selector_unmatched")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":            {"type": "int", "default": "fixed 10", "valid": "10"},
    "grid_w":            {"type": "int", "default": "fixed 11", "valid": "11"},
    "palette_kind":      {"type": "str", "default": "rng helpful",
                          "valid": "|".join(PALETTE_KINDS)},
    "palette_size":      {"type": "int", "default": "rng 3..3", "valid": "3..3"},
    "position_bias":     {"type": "str", "default": "fixed_meta_layout",
                          "valid": "fixed_meta_layout"},
    "n_distinct_colors": {"type": "int", "default": "rng 3..3", "valid": "3..3"},
    "density":           {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":           {"type": "str", "default": "alias for palette_kind",
                          "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    rng = ctx.draw_rng("layout")
    h = 10
    w = 11
    g = full_grid(h, w, 0)

    palette = rng.sample([1, 2, 3, 4, 5, 6, 7, 8, 9], 3)
    for i, color in enumerate(palette):
        g[0][i] = color

    for r in (1, 2, 3, 4):
        g[r][0] = rng.randint(1, 5) if r >= 3 else rng.randint(1, 3)
        g[r][1] = rng.randint(1, 5) if r >= 3 else rng.randint(1, 3)

    bank_cols = [0, 4, 8]
    keys = [1, 2, 3]
    rng.shuffle(keys)
    for kcol, key in zip(bank_cols, keys):
        g[6][kcol] = key
        for r in range(7, 10):
            for c in range(kcol, kcol + 3):
                if rng.random() < 0.5:
                    g[r][c] = rng.randint(1, 3)
        if all(g[r][c] == 0 for r in range(7, 10) for c in range(kcol, kcol + 3)):
            r = rng.randint(7, 9)
            c = rng.randint(kcol, kcol + 2)
            g[r][c] = rng.randint(1, 3)
    return g


def _draw_from_degenerate(name, rng):
    h, w = 10, 11
    g = full_grid(h, w, 0)
    if name == "no_palette":
        # Row 0 empty — rule's color-lift map is empty.
        for r in (1, 2):
            g[r][0] = 1; g[r][1] = 2
        for r in (3, 4):
            g[r][0] = 0; g[r][1] = 1
        bank_cols = [0, 4, 8]
        for kcol, key in zip(bank_cols, [1, 2, 3]):
            g[6][kcol] = key
            g[7][kcol] = 1
            g[8][kcol + 1] = 2
        return g
    if name == "no_bank":
        # No bank rows — rule's selectors find no templates.
        g[0][0] = 4; g[0][1] = 5; g[0][2] = 6
        for r in (1, 2):
            g[r][0] = 1; g[r][1] = 2
        for r in (3, 4):
            g[r][0] = 0; g[r][1] = 1
        return g
    if name == "selector_unmatched":
        # Selectors reference keys not in bank.
        g[0][0] = 4; g[0][1] = 5; g[0][2] = 6
        for r in (1, 2):
            g[r][0] = 3; g[r][1] = 3   # all 3s
        for r in (3, 4):
            g[r][0] = 0; g[r][1] = 1
        # Bank only has key 1 (no 2 or 3)
        g[6][0] = 1
        g[7][0] = 1; g[8][1] = 2
        return g
    return g
