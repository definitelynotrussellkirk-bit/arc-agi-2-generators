"""Generator for puzzle a85d4709.

Rule: for each row r: find first col with v == 5; output every cell in
that row to nth([2, 4, 3], that index). Effect: each row's 5-position
band determines the row's solid output color.

Combinatorial axes: grid_h, w_third (width = 3 * w_third), bg_color,
band_distribution (uniform / biased_left / biased_right), n_decoys
(non-5 fg cells). Degenerates: same_band_all_rows, no_fives_some_rows
(rule no-op for those rows), single_row.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "fda8d5c26728"
VERSION = "1.1.0"
TASK_ID = "fda8d5c26728"
SUMMARY = "Each row has 1 gray dot in a band; rule paints rows by band color (2/4/3)."

INVARIANTS = [
    "bg ≠ 2, 3, 4, 5",
    "w divisible by 3",
    "each row has ≥1 gray(5) cell",
]

BAND_DISTRIBUTIONS = ("uniform", "biased_left", "biased_right", "all_distinct")
DEGENERATE_TEXTURES = ("same_band_all_rows", "single_row", "extra_fives")
HELPFUL_TEXTURES = BAND_DISTRIBUTIONS

AXES = {
    "grid_h":             {"type": "int", "default": "rng 2..15", "valid": "2..30"},
    "grid_w_third":       {"type": "int", "default": "rng 1..3", "valid": "1..10"},
    "bg_color":           {"type": "color", "default": "rng (≠2,3,4,5)",
                           "valid": "0..9 (≠2,3,4,5)"},
    "band_distribution":  {"type": "str", "default": "rng helpful",
                           "valid": "|".join(BAND_DISTRIBUTIONS)},
    "decoy_palette_size": {"type": "int", "default": "rng 0..3", "valid": "0..6"},
    "texture":            {"type": "str", "default": "alias for band_distribution",
                           "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if difficulty == "easy":
        h_lo, h_hi, w_lo, w_hi = 2, 5, 1, 1
    elif difficulty == "hard":
        h_lo, h_hi, w_lo, w_hi = 11, 15, 2, 3
    else:
        h_lo, h_hi, w_lo, w_hi = 2, 15, 1, 3
    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w3 = ctx.draw_int("grid_w_third", w_lo, w_hi)
    w = w3 * 3
    rng = ctx.draw_rng("placement")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], h, w3, rng)
    bg = int(overrides.get("bg_color", ctx.draw_color("bg_color", exclude={2, 3, 4, 5})))
    distribution = (overrides.get("texture") or overrides.get("band_distribution")
                    or ctx.draw_choice("band_distribution", list(BAND_DISTRIBUTIONS)))
    g = full_grid(h, w, bg)
    for r in range(h):
        band = _pick_band(distribution, r, rng)
        col_in_band = rng.randint(0, w3 - 1)
        col = band * w3 + col_in_band
        g[r][col] = 5
    return g


def _pick_band(distribution, r, rng):
    if distribution == "uniform":
        return rng.choice([0, 1, 2])
    if distribution == "biased_left":
        return rng.choices([0, 1, 2], weights=[5, 2, 1])[0]
    if distribution == "biased_right":
        return rng.choices([0, 1, 2], weights=[1, 2, 5])[0]
    if distribution == "all_distinct":
        return r % 3
    return rng.choice([0, 1, 2])


def _draw_from_degenerate(name, h, w3, rng):
    w = w3 * 3
    bg = rng.choice([c for c in range(10) if c not in {2, 3, 4, 5}])
    g = full_grid(h, w, bg)
    if name == "same_band_all_rows":
        band = rng.choice([0, 1, 2])
        for r in range(h):
            col = band * w3 + rng.randint(0, w3 - 1)
            g[r][col] = 5
        return g
    if name == "single_row":
        # Only 1 row but extended grid_h beyond 1 doesn't apply (h=1 not allowed in axes).
        # Use the smallest h=2 — first row has 5, second is bg.
        col = rng.randint(0, w - 1)
        g[0][col] = 5
        # Force second row to also have a 5 somewhere.
        if h > 1:
            g[1][rng.randint(0, w - 1)] = 5
        return g
    if name == "extra_fives":
        # Multiple 5s per row — find-first uses leftmost.
        for r in range(h):
            for _ in range(rng.randint(1, 3)):
                col = rng.randint(0, w - 1)
                g[r][col] = 5
        return g
    return g
