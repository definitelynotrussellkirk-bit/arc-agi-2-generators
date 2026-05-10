"""Generator for ARC task f45f5ca7.

Rule: for each row r, take v = g[r][0]. Lookup table: 2→2, 3→4, 4→3,
8→1, else 0 (call this `c*`). Output cell (r, c) = v if c == c*, else 0.

Combinatorial axes: grid_h/w, code_distribution (which codes appear in
col 0), decoy_density (cells in cols 1+ that get ignored).
Degenerates: all_zero_col0 (rule no-op), only_uncoded (no signals),
no_decoys.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "1e74f9aa9324"
VERSION = "1.1.0"
TASK_ID = "1e74f9aa9324"
SUMMARY = "Each row's col-0 encodes a target column for that color via a fixed lookup."

INVARIANTS = [
    "grid width is ≥5 (so the lookup column index can fit)",
    "col 0 contains values from {0, 2, 3, 4, 8}",
    "non-col-0 cells are decoys (rule discards them)",
]

CODE_DISTRIBUTIONS = ("uniform", "biased_2", "biased_8", "all_distinct", "mostly_zero")
DEGENERATE_TEXTURES = ("all_zero_col0", "only_uncoded", "no_decoys")
HELPFUL_TEXTURES = CODE_DISTRIBUTIONS

AXES = {
    "grid_h":              {"type": "int", "default": "rng 4..14", "valid": "1..30"},
    "grid_w":              {"type": "int", "default": "rng 5..14", "valid": "5..30"},
    "code_distribution":   {"type": "str", "default": "rng helpful",
                            "valid": "|".join(CODE_DISTRIBUTIONS)},
    "decoy_density":       {"type": "float", "default": "rng 0.0..0.25", "valid": "0..0.5"},
    "texture":             {"type": "str", "default": "alias for code_distribution",
                            "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if difficulty == "easy":
        h_lo, h_hi, w_lo, w_hi = 4, 6, 5, 8
    elif difficulty == "hard":
        h_lo, h_hi, w_lo, w_hi = 11, 14, 11, 14
    else:
        h_lo, h_hi, w_lo, w_hi = 4, 14, 5, 14
    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", w_lo, w_hi)
    rng = ctx.draw_rng("rows")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], h, w, rng)
    distribution = (overrides.get("texture")
                    or overrides.get("code_distribution")
                    or ctx.draw_choice("code_distribution", list(CODE_DISTRIBUTIONS)))
    decoy_d = float(overrides.get("decoy_density",
                                  ctx.draw_rng("decoy_density").uniform(0.0, 0.25)))

    g = full_grid(h, w, 0)
    for r in range(h):
        g[r][0] = _pick_code(distribution, r, rng)
    decoy_palette = [c for c in [1, 2, 3, 4, 5, 6, 7, 8, 9]]
    for r in range(h):
        for c in range(1, w):
            if rng.random() < decoy_d:
                g[r][c] = rng.choice(decoy_palette)
    return g


def _pick_code(distribution, r, rng):
    if distribution == "uniform":
        return rng.choice([0, 2, 3, 4, 8])
    if distribution == "biased_2":
        return rng.choices([2, 0, 3, 4, 8], weights=[5, 1, 1, 1, 1])[0]
    if distribution == "biased_8":
        return rng.choices([8, 0, 2, 3, 4], weights=[5, 1, 1, 1, 1])[0]
    if distribution == "all_distinct":
        codes = [0, 2, 3, 4, 8]
        return codes[r % len(codes)]
    if distribution == "mostly_zero":
        return rng.choices([0, 2, 3, 4, 8], weights=[7, 1, 1, 1, 1])[0]
    return rng.choice([0, 2, 3, 4, 8])


def _draw_from_degenerate(name, h, w, rng):
    g = full_grid(h, w, 0)
    decoy = [c for c in range(1, 10)]
    if name == "all_zero_col0":
        # Col 0 all zero → rule outputs all zero.
        for r in range(h):
            for c in range(1, w):
                if rng.random() < 0.3:
                    g[r][c] = rng.choice(decoy)
        return g
    if name == "only_uncoded":
        # Col 0 uses colors NOT in {0, 2, 3, 4, 8} → all looked up to 0.
        uncoded = [1, 5, 6, 7, 9]
        for r in range(h):
            g[r][0] = rng.choice(uncoded)
        return g
    if name == "no_decoys":
        # Col 0 has codes; cols 1+ entirely 0.
        for r in range(h):
            g[r][0] = rng.choice([2, 3, 4, 8])
        return g
    return g
