"""Generator for arc_puzzle_bank_21_set16_bundle:medium_p06 — pack transformed base.

Rule: row 0 holds 1-4 transform codes; rows 2..h-1 hold a base motif.
For each code, transform a crop of the base; pack the transformed pieces
left-to-right with one blank column between them.

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, n_codes, texture.
Degenerates: no_codes, no_motif, code_in_motif_row.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "10bc62b2de84"
VERSION = "1.1.0"
TASK_ID = "10bc62b2de84"

SUMMARY = "Row 0: 1-4 transform codes; rows 2..h-1: a small base motif."

INVARIANTS = [
    "background is 0",
    "row 0 has 1-4 non-zero transform codes (1..7) at distinct columns",
    "row 1 is all 0 (separator)",
    "rows 2..h-1 hold a connected base motif (3-5 cells)",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_codes", "no_motif", "code_in_motif_row")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..10", "valid": "7..14"},
    "grid_w":         {"type": "int", "default": "rng 11..14", "valid": "10..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_codes":        {"type": "int", "default": "rng 2..4", "valid": "1..5"},
    "palette_size":   {"type": "int", "default": "rng 2..3", "valid": "2..3"},
    "position_bias":  {"type": "str", "default": "codes_top_motif_below",
                       "valid": "codes_top_motif_below"},
    "n_distinct_colors": {"type": "int", "default": "rng 2..3", "valid": "2..3"},
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
        w = ctx.draw_int("grid_w", 11, 12)
        n_codes = ctx.draw_int("n_codes", 2, 2)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 10, 13)
        w = ctx.draw_int("grid_w", 14, 16)
        n_codes = ctx.draw_int("n_codes", 4, 5)
    else:
        h = ctx.draw_int("grid_h", 8, 10)
        w = ctx.draw_int("grid_w", 11, 14)
        n_codes = ctx.draw_int("n_codes", 2, 4)
    rng = ctx.draw_rng("layout")

    g = full_grid(h, w, 0)
    cols = rng.sample(range(w), n_codes)
    cols.sort()
    for c in cols:
        g[0][c] = rng.randint(1, 4)

    motif_color = rng.choice([8, 9])
    cells = [(0, 0)]
    seen = {(0, 0)}
    target = rng.randint(3, 5)
    while len(cells) < target:
        r, c = rng.choice(cells)
        dr, dc = rng.choice([(-1, 0), (1, 0), (0, -1), (0, 1)])
        nr, nc = r + dr, c + dc
        if (nr, nc) not in seen:
            cells.append((nr, nc)); seen.add((nr, nc))
    rs = [r for r, _ in cells]; cs = [c for _, c in cells]
    sh = max(rs) - min(rs) + 1
    sw = max(cs) - min(cs) + 1
    sr0, sc0 = -min(rs), -min(cs)
    r0 = rng.randint(2, h - sh)
    c0 = rng.randint(0, w - sw)
    for r, c in cells:
        g[r0 + sr0 + r][c0 + sc0 + c] = motif_color
    return g


def _draw_from_degenerate(name, rng):
    h, w = 9, 12
    g = full_grid(h, w, 0)
    if name == "no_codes":
        # Motif but row 0 is empty — no transforms to apply.
        for r, c in [(3, 3), (3, 4), (4, 3)]: g[r][c] = 8
        return g
    if name == "no_motif":
        # Codes but no motif — nothing to transform.
        g[0][2] = 1; g[0][6] = 3; g[0][9] = 4
        return g
    if name == "code_in_motif_row":
        # Codes leak past row 0 — "row 0 only" precondition fails.
        g[0][2] = 1; g[0][6] = 3
        g[3][3] = 1
        for r, c in [(4, 5), (4, 6), (5, 5)]: g[r][c] = 8
        return g
    return g
