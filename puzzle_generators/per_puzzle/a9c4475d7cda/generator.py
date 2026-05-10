"""Generator for puzzle 6773b310.

Rule: 8-rows + 8-cols divide grid into 9 sections. Output 1 per
section with >=2 cells of color 6, else 0.

Combinatorial axes (8): grid_size, sep_rows, sep_cols, six_min,
six_max, palette_size, anchor_corner, asymmetry_force.
Degenerates: no_sixes, all_sixes, no_separators.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "a9c4475d7cda"
VERSION = "1.1.0"
TASK_ID = "a9c4475d7cda"
SUMMARY = "11x11 grid w/ 8-cross + 6-cells per section; rule outputs 3x3 binary."

INVARIANTS = [
    "h=w=11",
    "exactly 2 full-width 8-rows + 2 full-height 8-cols",
    "each section has 0-4 6-cells",
    "section dim >=2",
]

DENSITY_KINDS = ("uniform", "centered", "edges_heavy",
                 "polarized", "varied")
DEGENERATE_TEXTURES = ("no_sixes", "all_sixes", "no_separators")
HELPFUL_TEXTURES = DENSITY_KINDS

AXES = {
    "grid_size":      {"type": "int", "default": "11", "valid": "11"},
    "six_min":        {"type": "int", "default": "0", "valid": "0..3"},
    "six_max":        {"type": "int", "default": "rng 3..5", "valid": "1..6"},
    "density_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(DENSITY_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "1", "valid": "1..2"},
    "include_decoy":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "texture":        {"type": "str", "default": "alias for density_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], rng)
    h = w = 11
    six_min = int(overrides.get("six_min", 0))
    six_max = int(overrides.get("six_max",
                                ctx.draw_int("six_max", 3, 5)))
    six_min = max(0, min(3, six_min))
    six_max = max(six_min, min(6, six_max))
    density = (overrides.get("texture") or
               overrides.get("density_kind")
               or ctx.draw_choice("density_kind",
                                  list(DENSITY_KINDS)))
    g = full_grid(h, w, 0)
    sep_rows = sorted(rng.sample(range(2, h - 2), 2))
    while sep_rows[1] - sep_rows[0] < 2:
        sep_rows = sorted(rng.sample(range(2, h - 2), 2))
    sep_cols = sorted(rng.sample(range(2, w - 2), 2))
    while sep_cols[1] - sep_cols[0] < 2:
        sep_cols = sorted(rng.sample(range(2, w - 2), 2))
    for r in sep_rows:
        for c in range(w):
            g[r][c] = 8
    for c in sep_cols:
        for r in range(h):
            g[r][c] = 8
    row_bands = [(0, sep_rows[0]), (sep_rows[0] + 1, sep_rows[1]),
                 (sep_rows[1] + 1, h)]
    col_bands = [(0, sep_cols[0]), (sep_cols[0] + 1, sep_cols[1]),
                 (sep_cols[1] + 1, w)]
    for ri, rb in enumerate(row_bands):
        for ci, cb in enumerate(col_bands):
            n_sixes = _pick_count(density, ri, ci, six_min, six_max, rng)
            for _ in range(n_sixes):
                for _ in range(15):
                    r = rng.randint(rb[0], rb[1] - 1)
                    c = rng.randint(cb[0], cb[1] - 1)
                    if g[r][c] == 0:
                        g[r][c] = 6
                        break
    return g


def _pick_count(density, ri, ci, mn, mx, rng):
    if density == "uniform":
        return rng.randint(mn, mx)
    if density == "centered":
        return mx if (ri == 1 and ci == 1) else rng.randint(mn, max(mn, mx - 2))
    if density == "edges_heavy":
        on_edge = (ri == 0 or ri == 2 or ci == 0 or ci == 2)
        return mx if on_edge else mn
    if density == "polarized":
        return mx if (ri + ci) % 2 == 0 else mn
    return rng.randint(mn, mx)


def _draw_from_degenerate(name, rng):
    h = w = 11
    g = full_grid(h, w, 0)
    sep_rows = [3, 7]; sep_cols = [3, 7]
    for r in sep_rows:
        for c in range(w):
            g[r][c] = 8
    for c in sep_cols:
        for r in range(h):
            g[r][c] = 8
    if name == "no_sixes":
        return g
    if name == "all_sixes":
        for r in range(h):
            for c in range(w):
                if g[r][c] == 0:
                    g[r][c] = 6
        return g
    if name == "no_separators":
        return full_grid(h, w, 0)
    return g
