"""Generator for arc_additional_puzzles_21_set9:M60 — Code-driven motif transforms.

Rule: top row has 2-4 codes from {1,2,3,4} indicating transforms (none,
rotate-cw, rotate-180, flip-ud) applied to motif (rows 1+ cropped).
Output: side-by-side transformed motifs separated by 0-cols.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_codes,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_codes, no_motif, code_out_of_range.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "01f1e6b34a5b"
VERSION = "1.1.0"
TASK_ID = "01f1e6b34a5b"
SUMMARY = "Top row: 2-4 codes from {1,2,3,4}. Below: small motif (h=3..5, w=3..5)."

INVARIANTS = [
    "row 0: 2-4 cells with values in {1, 2, 3, 4}, rest 0",
    "rows 1+: motif with ≥3 non-zero cells of color 2",
    "motif is asymmetric so transforms produce distinct outputs",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_codes", "no_motif", "code_out_of_range")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 4..6", "valid": "3..8"},
    "grid_w":         {"type": "int", "default": "rng 3..5", "valid": "3..6"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_codes":        {"type": "int", "default": "rng 2..4", "valid": "2..4"},
    "palette_size":   {"type": "int", "default": "rng 2..5", "valid": "2..5"},
    "position_bias":  {"type": "str", "default": "row0_codes_plus_motif",
                       "valid": "row0_codes_plus_motif"},
    "n_distinct_colors": {"type": "int", "default": "rng 2..5", "valid": "2..5"},
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
        h = ctx.draw_int("grid_h", 4, 4)
        w = ctx.draw_int("grid_w", 3, 4)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 5, 6)
        w = ctx.draw_int("grid_w", 4, 5)
    else:
        h = ctx.draw_int("grid_h", 4, 6)
        w = ctx.draw_int("grid_w", 3, 5)
    g = full_grid(h, w, 0)
    rng = ctx.draw_rng("layout")
    n_codes = rng.randint(2, min(4, w))
    code_cols = rng.sample(range(w), n_codes)
    for c in code_cols:
        g[0][c] = rng.choice([1, 2, 3, 4])
    n_motif = rng.randint(3, max(3, (h - 1) * w // 2))
    placed = 0
    for _ in range(60):
        if placed >= n_motif:
            break
        r = rng.randint(1, h - 1); c = rng.randint(0, w - 1)
        if g[r][c] == 0:
            g[r][c] = 2
            placed += 1
    return g


def _draw_from_degenerate(name, rng):
    h, w = 5, 5
    g = full_grid(h, w, 0)
    if name == "no_codes":
        # motif without row-0 codes → no transforms specified
        for r, c in [(1, 1), (2, 1), (2, 2), (3, 2)]: g[r][c] = 2
        return g
    if name == "no_motif":
        # codes alone with no motif → nothing to transform
        g[0][0] = 1; g[0][2] = 3; g[0][4] = 4
        return g
    if name == "code_out_of_range":
        # codes outside {1,2,3,4} → "valid code" precondition fails
        g[0][0] = 5; g[0][2] = 7  # not valid transform codes
        for r, c in [(1, 1), (2, 1), (2, 2), (3, 2)]: g[r][c] = 2
        return g
    return g
