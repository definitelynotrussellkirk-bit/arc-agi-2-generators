"""Generator for arc_puzzle_bank_21_set10_e:hard_j20 — codes in row 0 + motif transform.

Rule: row 0 has 3 single-cell codes (colors 2, 3, 4) defining a transform
sequence. A color-4 motif is in the body and gets transformed.

Combinatorial axes (8): grid_h, grid_w, palette_kind, motif_size,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_codes, no_motif, motif_in_top_row.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "f3acfc6e19e1"
VERSION = "1.1.0"
TASK_ID = "f3acfc6e19e1"

SUMMARY = "Row 0 has 3 single-cell codes (2, 3, 4) + a color-4 motif in the body."

INVARIANTS = [
    "background is 0",
    "row 0 has 3 cells: a color-2 cell at (0, 0), color-3 at (0, 1), color-4 at (0, 2)",
    "exactly one color-4 motif (3-5 cells) in the body (rows >= 2)",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_codes", "no_motif", "motif_in_top_row")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 7..9", "valid": "5..14"},
    "grid_w":         {"type": "int", "default": "rng 9..11", "valid": "7..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "motif_size":     {"type": "int", "default": "rng 3..5", "valid": "1..6"},
    "palette_size":   {"type": "str", "default": "3 (codes) + 1 (motif)", "valid": "3..3"},
    "position_bias":  {"type": "str", "default": "codes_top_motif_body",
                       "valid": "codes_top_motif_body"},
    "n_distinct_colors": {"type": "int", "default": "3", "valid": "3..3"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def _build_motif(rng, k):
    cells = [(0, 0)]; seen = {(0, 0)}
    while len(cells) < k:
        r, c = rng.choice(cells)
        dr, dc = rng.choice([(-1, 0), (1, 0), (0, -1), (0, 1)])
        nr, nc = r + dr, c + dc
        if (nr, nc) not in seen:
            cells.append((nr, nc)); seen.add((nr, nc))
    return cells


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 7, 7)
        w = ctx.draw_int("grid_w", 9, 9)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 9, 12)
        w = ctx.draw_int("grid_w", 11, 13)
    else:
        h = ctx.draw_int("grid_h", 7, 9)
        w = ctx.draw_int("grid_w", 9, 11)
    rng = ctx.draw_rng("layout")

    g = full_grid(h, w, 0)
    g[0][0] = 2
    g[0][1] = 3
    g[0][2] = 4
    cells = _build_motif(rng, rng.randint(3, 5))
    rs = [r for r, _ in cells]; cs = [c for _, c in cells]
    sh = max(rs) - min(rs) + 1; sw = max(cs) - min(cs) + 1
    for _ in range(80):
        r0 = rng.randint(2, h - sh); c0 = rng.randint(0, w - sw)
        cells_p = [(r0 + r - min(rs), c0 + c - min(cs)) for r, c in cells]
        if any(g[r][c] != 0 for r, c in cells_p): continue
        for r, c in cells_p:
            g[r][c] = 4
        return g
    return g


def _draw_from_degenerate(name, rng):
    h, w = 8, 10
    g = full_grid(h, w, 0)
    if name == "no_codes":
        # Body motif present but row 0 lacks the 2-3-4 code triple — rule
        # has no transform sequence to apply.
        for dr, dc in [(0, 0), (1, 0), (1, 1)]:
            g[3 + dr][4 + dc] = 4
        return g
    if name == "no_motif":
        # Codes present but body is empty — rule has no motif to transform.
        g[0][0] = 2; g[0][1] = 3; g[0][2] = 4
        return g
    if name == "motif_in_top_row":
        # Motif drawn in row 0, mixing it with the code zone — codes
        # cannot be cleanly distinguished from the body motif.
        g[0][0] = 2; g[0][1] = 3; g[0][2] = 4
        for dc in range(3):
            g[0][5 + dc] = 4
        g[1][6] = 4
        return g
    return g
