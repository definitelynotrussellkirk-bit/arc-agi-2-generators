"""Generator for ARC task 575b1a71.

Rule: for each cell with v == 0: replace with rank = 1 + (count of
distinct zero-cols < this col's col).

Combinatorial axes (8): grid_h/w, base_color, n_zero_cols,
zero_col_layout, zero_density, decoy_density, decoy_palette_size,
zero_position_bias.
Degenerates: no_zeros, all_zeros, single_zero_col.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "af840d59f24c"
VERSION = "1.1.0"
TASK_ID = "af840d59f24c"
SUMMARY = "Canvas with zeros in select columns; rule replaces each zero with its column rank."

INVARIANTS = [
    "≥1 zero cell exists",
    "rank colors stay in ARC range (zero cols ≤ 9)",
    "non-zero cells are preserved",
]

ZERO_COL_LAYOUTS = ("evenly_spaced", "clustered", "edge_biased", "random")
DEGENERATE_TEXTURES = ("no_zeros", "all_zeros", "single_zero_col")
HELPFUL_TEXTURES = ZERO_COL_LAYOUTS

AXES = {
    "grid_h":             {"type": "int", "default": "rng 4..14", "valid": "3..18"},
    "grid_w":             {"type": "int", "default": "rng 4..9", "valid": "2..9"},
    "base_color":         {"type": "color", "default": "rng (≠0,1..max_rank)", "valid": "1..9"},
    "n_zero_cols":        {"type": "int", "default": "rng 2..min(4,w-1)", "valid": "1..9"},
    "zero_col_layout":    {"type": "str", "default": "rng helpful",
                           "valid": "|".join(ZERO_COL_LAYOUTS)},
    "zero_density":       {"type": "float", "default": "rng 0.3..0.8", "valid": "0..1"},
    "decoy_palette_size": {"type": "int", "default": "rng 0..3", "valid": "0..6"},
    "decoy_density":      {"type": "float", "default": "rng 0..0.2", "valid": "0..0.5"},
    "texture":            {"type": "str", "default": "alias for zero_col_layout",
                           "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if difficulty == "easy":
        h_lo, h_hi, w_lo, w_hi = 4, 7, 4, 6
    elif difficulty == "hard":
        h_lo, h_hi, w_lo, w_hi = 11, 14, 7, 9
    else:
        h_lo, h_hi, w_lo, w_hi = 4, 14, 4, 9
    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", w_lo, w_hi)
    rng = ctx.draw_rng("zeros")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], h, w, rng)
    base = int(overrides.get("base_color",
                             ctx.draw_color("base_color", exclude={0, 1, 2, 3, 4, 5})))
    n_zero_cols = int(overrides.get("n_zero_cols",
                                    ctx.draw_int("n_zero_cols", 2,
                                                 max(2, min(4, w - 1)))))
    n_zero_cols = max(1, min(w, n_zero_cols))
    layout = (overrides.get("texture") or overrides.get("zero_col_layout")
              or ctx.draw_choice("zero_col_layout", list(ZERO_COL_LAYOUTS)))
    density = float(overrides.get("zero_density",
                                  ctx.draw_rng("zero_density").uniform(0.3, 0.8)))
    n_decoy = int(overrides.get("decoy_palette_size",
                                ctx.draw_int("decoy_palette_size", 0, 3)))
    decoy_d = float(overrides.get("decoy_density",
                                  ctx.draw_rng("decoy_density").uniform(0.0, 0.2)))
    g = full_grid(h, w, base)
    zero_cols = _zero_col_positions(layout, w, n_zero_cols, rng)
    for c in zero_cols:
        for r in range(h):
            if rng.random() < density:
                g[r][c] = 0
    decoy_palette = [c for c in range(1, 10) if c != base and c not in (1, 2, 3, 4, 5)]
    rng.shuffle(decoy_palette)
    decoy_palette = decoy_palette[:max(0, n_decoy)]
    if decoy_palette and decoy_d > 0:
        for r in range(h):
            for c in range(w):
                if c not in zero_cols and rng.random() < decoy_d:
                    g[r][c] = rng.choice(decoy_palette)
    if not any(g[r][c] == 0 for r in range(h) for c in range(w)):
        g[0][zero_cols[0]] = 0
    return g


def _zero_col_positions(layout, w, n, rng):
    if layout == "evenly_spaced":
        step = max(1, w // (n + 1))
        return [step * (i + 1) for i in range(n) if step * (i + 1) < w]
    if layout == "clustered":
        center = rng.randint(0, w - 1)
        cols = sorted(range(w), key=lambda c: abs(c - center))
        return sorted(cols[:n])
    if layout == "edge_biased":
        edges = [0, w - 1]
        return sorted(edges[:n] + rng.sample([c for c in range(1, w - 1)], min(max(0, n - 2), w - 2)))
    cols = list(range(w))
    rng.shuffle(cols)
    return sorted(cols[:n])


def _draw_from_degenerate(name, h, w, rng):
    base = rng.choice([6, 7, 8, 9])
    g = full_grid(h, w, base)
    if name == "no_zeros":
        # Need ≥1 zero per invariant.
        g[0][0] = 0
        return g
    if name == "all_zeros":
        for r in range(h):
            for c in range(w):
                g[r][c] = 0
        return g
    if name == "single_zero_col":
        c = rng.randint(0, w - 1)
        for r in range(h):
            if rng.random() < 0.5:
                g[r][c] = 0
        # Force ≥1 zero.
        g[0][c] = 0
        return g
    return g
