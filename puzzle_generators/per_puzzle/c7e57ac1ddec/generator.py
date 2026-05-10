"""Generator for arc_puzzle_bank_next_21_bundle:easy_11_bridge_single_horizontal_gaps.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_gaps,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_gaps, gap_already_filled, wider_gaps.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "c7e57ac1ddec"
VERSION = "1.1.0"
TASK_ID = "c7e57ac1ddec"
SUMMARY = "Rows containing 2-0-2 motifs whose single gap is bridged with 7."

INVARIANTS = [
    "background is 0",
    "at least one horizontal 2-0-2 motif appears",
    "motifs are spaced so their gaps are unambiguous",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_gaps", "gap_already_filled", "wider_gaps")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 6..10", "valid": "5..14"},
    "grid_w":         {"type": "int", "default": "rng 9..13", "valid": "7..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_gaps":         {"type": "int", "default": "rng 3..6", "valid": "1..10"},
    "palette_size":   {"type": "int", "default": "1", "valid": "1..2"},
    "position_bias":  {"type": "str", "default": "horizontal_pair",
                       "valid": "horizontal_pair"},
    "n_distinct_colors": {"type": "int", "default": "1", "valid": "1..2"},
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
        h = ctx.draw_int("grid_h", 6, 7)
        w = ctx.draw_int("grid_w", 9, 10)
        n_gaps = ctx.draw_int("n_gaps", 3, 4)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 12, 13)
        n_gaps = ctx.draw_int("n_gaps", 5, 6)
    else:
        h = ctx.draw_int("grid_h", 6, 10)
        w = ctx.draw_int("grid_w", 9, 13)
        n_gaps = ctx.draw_int("n_gaps", 3, 6)
    rng = ctx.draw_rng("placement")
    g = full_grid(h, w, 0)

    placed: set[tuple[int, int]] = set()
    for _ in range(160):
        if len(placed) >= n_gaps:
            break
        r = rng.randint(0, h - 1)
        c = rng.randint(0, w - 3)
        cells = {(r, c), (r, c + 1), (r, c + 2)}
        if any((r, cc) in placed for cc in range(max(0, c - 2), min(w, c + 5))):
            continue
        g[r][c] = 2
        g[r][c + 2] = 2
        placed |= cells
    if not placed:
        g[0][0] = g[0][2] = 2
    return g


def _draw_from_degenerate(name, rng):
    h, w = 8, 11
    g = full_grid(h, w, 0)
    if name == "no_gaps":
        # 2-cells present but never paired with single gap → rule has no targets
        for r, c in [(1, 1), (3, 5), (5, 8)]:
            g[r][c] = 2
        return g
    if name == "gap_already_filled":
        # 2-0-2 motif structure exists but gap is already non-bg → rule no-op for those gaps
        g[2][1] = 2
        g[2][3] = 2
        g[2][2] = 5  # gap pre-filled with non-7
        g[5][6] = 2
        g[5][8] = 2
        g[5][7] = 4
        return g
    if name == "wider_gaps":
        # 2-..-2 with 2+ cells of gap → rule's "single gap" condition never matches
        g[3][1] = 2
        g[3][4] = 2  # gap of 2 cells
        g[6][2] = 2
        g[6][7] = 2  # gap of 4 cells
        return g
    return g
