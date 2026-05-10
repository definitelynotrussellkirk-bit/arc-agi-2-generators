"""Generator for 41ace6b5.

Rule: nxn grid with row of 2s as divider; odd cols have alternating 8s;
rule normalizes alternating bars around the divider.

Combinatorial axes (8): n, sep_position, density_top, density_bottom,
density_2, palette_kind, anchor_corner, asymmetry_force.
Degenerates: no_divider, full_8s, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "982fefa4fff9"
VERSION = "1.1.0"
TASK_ID = "982fefa4fff9"
SUMMARY = "Square grid with 2-divider + 8s in odd cols; rule normalizes alternating bars."

INVARIANTS = [
    "input is square nxn (n in [7, 11])",
    "exactly one row contains a 2 (the divider)",
    "the divider is interior (rows 2..n-3)",
    "odd columns have 8s above and below the divider",
]

SEP_POSITIONS = ("center", "upper", "lower", "rng")
DEGENERATE_TEXTURES = ("no_divider", "full_8s", "full_grid")
HELPFUL_TEXTURES = SEP_POSITIONS

AXES = {
    "n":              {"type": "int", "default": "rng 7..11", "valid": "5..14"},
    "sep_position":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(SEP_POSITIONS)},
    "density_top":    {"type": "float", "default": "rng 0.4..0.6", "valid": "0.2..0.8"},
    "density_bottom": {"type": "float", "default": "rng 0.4..0.6", "valid": "0.2..0.8"},
    "density_2":      {"type": "float", "default": "0.5", "valid": "0.3..0.7"},
    "palette_kind":   {"type": "str", "default": "fixed", "valid": "fixed"},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "texture":        {"type": "str", "default": "alias for sep_position",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    rng = ctx.draw_rng("placement")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], rng)
    if difficulty == "easy":
        n_lo, n_hi = 5, 7
    elif difficulty == "hard":
        n_lo, n_hi = 11, 14
    else:
        n_lo, n_hi = 7, 11
    n = ctx.draw_int("n", n_lo, n_hi)
    sep_pos = (overrides.get("texture") or
               overrides.get("sep_position")
               or ctx.draw_choice("sep_position", list(SEP_POSITIONS)))
    if sep_pos == "center":
        sep = n // 2
    elif sep_pos == "upper":
        sep = max(2, n // 3)
    elif sep_pos == "lower":
        sep = min(n - 3, 2 * n // 3)
    else:
        sep = rng.randint(2, n - 3)
    sep = max(2, min(sep, n - 3))
    g = full_grid(n, n, 0)
    d2 = float(overrides.get("density_2", 0.5))
    for c in range(n):
        if rng.random() < d2:
            g[sep][c] = 2
    d_top = float(overrides.get("density_top",
                                rng.uniform(0.3, 0.7)))
    d_bot = float(overrides.get("density_bottom",
                                rng.uniform(0.3, 0.7)))
    for c in range(1, n, 2):
        for r in range(n):
            if r == sep:
                continue
            density = d_top if r < sep else d_bot
            if rng.random() < density:
                g[r][c] = 8
    return g


def _draw_from_degenerate(name, rng):
    n = 9
    g = full_grid(n, n, 0)
    if name == "no_divider":
        for c in range(1, n, 2):
            for r in range(n):
                if rng.random() < 0.5:
                    g[r][c] = 8
        return g
    if name == "full_8s":
        for r in range(n):
            for c in range(n):
                g[r][c] = 8
        return g
    if name == "full_grid":
        for r in range(n):
            for c in range(n):
                g[r][c] = 2
        return g
    return g
