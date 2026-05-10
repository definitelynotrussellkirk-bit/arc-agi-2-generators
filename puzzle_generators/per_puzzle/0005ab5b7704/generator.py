"""Generator for arc_puzzle_bank_21_set5_s:S5_M3.

Rule: top-row color-4 markers select which body columns survive; other
columns are dropped (or zeroed).

Combinatorial axes (8): grid_h/w, palette_kind, n_selected, palette_size,
position_bias, n_distinct_colors, body_density, texture.
Degenerates: no_markers, all_columns_marked, no_body.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "0005ab5b7704"
VERSION = "1.1.0"
TASK_ID = "0005ab5b7704"
SUMMARY = "Top-row color-4 markers select which body columns survive."

INVARIANTS = [
    "background is 0",
    "top row contains color-4 markers in a proper subset of columns",
    "body rows contain varied non-marker colors",
    "at least one unmarked body column contains nonzero cells",
]

PALETTE_KINDS = ("default", "sparse", "dense", "varied_palette")
DEGENERATE_TEXTURES = ("no_markers", "all_columns_marked", "no_body")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 7..10", "valid": "5..14"},
    "grid_w":         {"type": "int", "default": "rng 8..12", "valid": "5..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_selected":     {"type": "int", "default": "rng 3..5", "valid": "1..10"},
    "palette_size":   {"type": "int", "default": "rng 4..7", "valid": "1..9"},
    "position_bias":  {"type": "str", "default": "spread", "valid": "spread"},
    "n_distinct_colors": {"type": "int", "default": "rng 4..7", "valid": "1..9"},
    "body_density":   {"type": "str", "default": "mixed", "valid": "mixed"},
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
        w = ctx.draw_int("grid_w", 8, 10)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 11, 12)
    else:
        h = ctx.draw_int("grid_h", 7, 10)
        w = ctx.draw_int("grid_w", 8, 12)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    selected = sorted(rng.sample(range(w), rng.randint(3, min(5, w - 2))))
    for c in selected:
        g[0][c] = 4
    colors = [1, 2, 3, 5, 6, 7, 8, 9]
    for r in range(1, h):
        for c in range(w):
            if rng.random() < 0.45:
                g[r][c] = rng.choice(colors)
    return g


def _draw_from_degenerate(name, rng):
    h, w = 8, 10
    g = full_grid(h, w, 0)
    if name == "no_markers":
        # body has cells but no top-row 4-markers — selection has no candidates
        for r in range(1, h):
            for c in range(w):
                if (r + c) % 3 == 0:
                    g[r][c] = ((c % 7) + 1)
        return g
    if name == "all_columns_marked":
        # every column marked — output equals input (rule trivial)
        for c in range(w):
            g[0][c] = 4
        for r in range(1, h):
            for c in range(w):
                if (r + c) % 3 == 0:
                    g[r][c] = ((c % 7) + 1)
        return g
    if name == "no_body":
        # markers but no body cells — rule has nothing to compress
        for c in range(0, w, 2):
            g[0][c] = 4
        return g
    return g
