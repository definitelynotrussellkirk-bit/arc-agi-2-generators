"""Generator for arc_puzzle_bank_next21:E8.

Rule: place separated horizontal color-zero-color sandwiches; rule fills the
center.

Combinatorial axes (8): grid_h, grid_w, palette_kind, motifs,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_motifs, gap_already_filled, mismatched_endpoints.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "dfc7297269cc"
VERSION = "1.1.0"
TASK_ID = "dfc7297269cc"
SUMMARY = "Place separated horizontal color-zero-color sandwiches."

INVARIANTS = [
    "background is 0",
    "each active motif is color, zero, same color in one row",
    "motifs are separated so only intended center cells are filled",
    "at least one sandwich center changes in the output",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_motifs", "gap_already_filled", "mismatched_endpoints")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 5..8", "valid": "3..14"},
    "grid_w":         {"type": "int", "default": "rng 7..11", "valid": "5..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "motifs":         {"type": "int", "default": "rng 2..4", "valid": "1..8"},
    "palette_size":   {"type": "int", "default": "rng 2..4", "valid": "1..8"},
    "position_bias":  {"type": "str", "default": "horizontal_pair",
                       "valid": "horizontal_pair"},
    "n_distinct_colors": {"type": "int", "default": "rng 2..4", "valid": "1..8"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index, version=VERSION,
                  task_id=TASK_ID, difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 5, 6)
        w = ctx.draw_int("grid_w", 7, 9)
        target = ctx.draw_int("motifs", 2, 2)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 7, 8)
        w = ctx.draw_int("grid_w", 10, 11)
        target = ctx.draw_int("motifs", 3, 4)
    else:
        h = ctx.draw_int("grid_h", 5, 8)
        w = ctx.draw_int("grid_w", 7, 11)
        target = ctx.draw_int("motifs", 2, 4)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    reserved: set[tuple[int, int]] = set()
    placed = 0
    for _ in range(300):
        if placed >= target:
            break
        r = rng.randrange(h)
        c = rng.randint(1, w - 2)
        footprint = {(r, c - 1), (r, c), (r, c + 1)}
        guard = {
            (rr, cc)
            for rr in range(max(0, r - 1), min(h, r + 2))
            for cc in range(max(0, c - 2), min(w, c + 3))
        }
        if guard & reserved:
            continue
        color = rng.choice([1, 2, 3, 4, 5, 6, 7, 8, 9])
        g[r][c - 1] = color
        g[r][c + 1] = color
        reserved.update(guard | footprint)
        placed += 1
    return g


def _draw_from_degenerate(name, rng):
    h, w = 6, 9
    g = full_grid(h, w, 0)
    if name == "no_motifs":
        # scattered single cells, no sandwich pairs → rule has no targets
        for r, c, v in [(1, 2, 4), (3, 5, 5), (5, 7, 6)]:
            g[r][c] = v
        return g
    if name == "gap_already_filled":
        # sandwich endpoints but center already non-bg → rule no-op for those
        g[2][1] = 3; g[2][2] = 5; g[2][3] = 3
        g[4][4] = 6; g[4][5] = 7; g[4][6] = 6
        return g
    if name == "mismatched_endpoints":
        # different-color endpoints → rule's "same color" condition never matches
        g[2][1] = 3; g[2][3] = 5
        g[4][4] = 6; g[4][6] = 7
        return g
    return g
