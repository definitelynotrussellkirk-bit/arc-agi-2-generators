"""Generator for 72207abc.

Rule: row 1 has seed cells (filtered as the row's non-zero cells in
order). For k=0,1,...: place seed[k mod ns] at col k*(k+1)/2 (triangular).

Combinatorial axes (8): grid_w, n_seed_cells, palette_kind, seed_layout,
seed_position_bias, distract_row0_density, distract_row2_density,
allow_decoy_palette.
Degenerates: empty_seed, single_seed, full_row1.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "8cbd834f4187"
VERSION = "1.1.0"
TASK_ID = "8cbd834f4187"
SUMMARY = "3-row grid; row 1 has seed cells; rule plants them at triangular positions."

INVARIANTS = [
    "exactly 3 rows",
    "row 1 has >=1 non-zero seed cell",
    "row 0 and row 2 are all 0 (so output is unambiguous)",
    "seed cells are placed at small col indices (so triangular layout has room)",
]

SEED_LAYOUTS = ("contiguous_left", "scattered", "ascending", "alternating")
PALETTE_KINDS = ("warm", "cool", "broad", "small")
DEGENERATE_TEXTURES = ("empty_seed", "single_seed", "full_row1")
HELPFUL_TEXTURES = SEED_LAYOUTS

AXES = {
    "grid_w":          {"type": "int", "default": "rng 12..24", "valid": "10..28"},
    "n_seed_cells":    {"type": "int", "default": "rng 2..4", "valid": "1..6"},
    "palette_kind":    {"type": "str", "default": "rng helpful",
                        "valid": "|".join(PALETTE_KINDS)},
    "seed_layout":     {"type": "str", "default": "rng helpful",
                        "valid": "|".join(SEED_LAYOUTS)},
    "seed_max_col":    {"type": "int", "default": "rng 4..7", "valid": "1..10"},
    "distract_outside_seed": {"type": "bool", "default": "false",
                              "valid": "true|false"},
    "anchor_row1_first": {"type": "bool", "default": "true",
                          "valid": "true|false"},
    "padding_zeros":   {"type": "int", "default": "0", "valid": "0..3"},
    "texture":         {"type": "str", "default": "alias for seed_layout",
                        "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if difficulty == "easy":
        w_lo, w_hi, n_lo, n_hi = 10, 14, 2, 2
    elif difficulty == "hard":
        w_lo, w_hi, n_lo, n_hi = 22, 28, 3, 5
    else:
        w_lo, w_hi, n_lo, n_hi = 12, 24, 2, 4
    w = ctx.draw_int("grid_w", w_lo, w_hi)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], w, rng)
    n_seed = int(overrides.get("n_seed_cells",
                               ctx.draw_int("n_seed_cells", n_lo, n_hi)))
    n_seed = max(1, min(6, n_seed))
    palette_kind = overrides.get("palette_kind",
                                 ctx.draw_choice("palette_kind",
                                                 list(PALETTE_KINDS)))
    if palette_kind == "warm":
        pool = [3, 4, 6, 9]
    elif palette_kind == "cool":
        pool = [1, 5, 7, 8]
    elif palette_kind == "small":
        pool = [1, 2, 3]
    else:
        pool = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    rng.shuffle(pool)
    palette = pool[:n_seed]
    if len(palette) < n_seed:
        extra_pool = [c for c in range(1, 10) if c not in palette]
        rng.shuffle(extra_pool)
        palette += extra_pool[:n_seed - len(palette)]
    layout = (overrides.get("texture") or overrides.get("seed_layout")
              or ctx.draw_choice("seed_layout", list(SEED_LAYOUTS)))
    seed_max = int(overrides.get("seed_max_col",
                                 ctx.draw_int("seed_max_col", 4, 7)))
    seed_max = max(n_seed, min(w - 1, seed_max))
    h = 3
    g = full_grid(h, w, 0)
    cols = _seed_cols(layout, n_seed, seed_max, rng)
    for i, c in enumerate(cols[:n_seed]):
        g[1][c] = palette[i]
    return g


def _seed_cols(layout, n, max_col, rng):
    if layout == "contiguous_left":
        return list(range(n))
    if layout == "ascending":
        step = max(1, max_col // n)
        return [i * step for i in range(n) if i * step < max_col]
    if layout == "alternating":
        cs = [c for c in range(max_col) if c % 2 == 0]
        return cs[:n] if cs else list(range(n))
    cs = list(range(max_col))
    rng.shuffle(cs)
    return sorted(cs[:n])


def _draw_from_degenerate(name, w, rng):
    g = full_grid(3, w, 0)
    color = rng.choice([1, 2, 3, 4, 5, 6, 7, 8, 9])
    if name == "empty_seed":
        g[1][0] = color
        return g
    if name == "single_seed":
        g[1][2] = color
        return g
    if name == "full_row1":
        for c in range(min(5, w)):
            g[1][c] = rng.choice([1, 2, 3, 4, 5, 6, 7, 8, 9])
        return g
    return g
