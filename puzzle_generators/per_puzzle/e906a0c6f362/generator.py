"""Generator for puzzle 782b5218.

Rule: input has a 'primary' color (first non-bg, non-red cell in
row-major scan) and red(2) markers in each column. Output paints each
column: above red → 0, at red → 2, below red → primary.

Combinatorial axes (8): grid_h/w, primary_color, primary_position,
red_distribution, red_min_row, red_max_row, anchor_corner,
asymmetry_force.
Degenerates: no_primary, no_reds, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "e906a0c6f362"
VERSION = "1.1.0"
TASK_ID = "e906a0c6f362"
SUMMARY = "Primary color marker + per-column reds; rule paints 0/2/primary stripes."

INVARIANTS = [
    "background is 0",
    "exactly one non-red non-bg cell at row-major scan front",
    "every column has >=1 red(2) cell",
    "primary != 2 and != 0",
]

RED_DISTRIBUTIONS = ("uniform", "increasing", "decreasing",
                     "centered", "edges", "alternating")
PRIMARY_POSITIONS = ("top_left", "top_right", "row_0_random",
                     "col_0_random")
DEGENERATE_TEXTURES = ("no_primary", "no_reds", "full_grid")
HELPFUL_TEXTURES = RED_DISTRIBUTIONS

AXES = {
    "grid_h":            {"type": "int", "default": "rng 8..14", "valid": "6..18"},
    "grid_w":            {"type": "int", "default": "rng 6..12", "valid": "4..16"},
    "primary":           {"type": "color", "default": "rng (≠0,2)",
                          "valid": "1..9 (≠2)"},
    "primary_position":  {"type": "str", "default": "top_left",
                          "valid": "|".join(PRIMARY_POSITIONS)},
    "red_distribution":  {"type": "str", "default": "rng helpful",
                          "valid": "|".join(RED_DISTRIBUTIONS)},
    "red_min_row":       {"type": "int", "default": "2", "valid": "1..h-2"},
    "red_max_row":       {"type": "int", "default": "h-2", "valid": "2..h-1"},
    "anchor_corner":     {"type": "bool", "default": "false",
                          "valid": "true|false"},
    "texture":           {"type": "str", "default": "alias for red_distribution",
                          "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if difficulty == "easy":
        h_lo, h_hi = 6, 9
    elif difficulty == "hard":
        h_lo, h_hi = 14, 18
    else:
        h_lo, h_hi = 8, 14
    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", h_lo - 2, h_hi - 2)
    rng = ctx.draw_rng("placement")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], h, w, rng)
    primary = int(overrides.get("primary",
                                ctx.draw_color("primary",
                                               exclude={0, 2})))
    pos = overrides.get("primary_position", "top_left")
    distribution = (overrides.get("texture") or
                    overrides.get("red_distribution")
                    or ctx.draw_choice("red_distribution",
                                       list(RED_DISTRIBUTIONS)))
    rmin = int(overrides.get("red_min_row", 2))
    rmax = int(overrides.get("red_max_row", h - 2))
    rmin = max(1, min(h - 2, rmin))
    rmax = max(rmin, min(h - 1, rmax))
    g = full_grid(h, w, 0)
    if pos == "top_left":
        pr, pc = 0, 0
    elif pos == "top_right":
        pr, pc = 0, w - 1
    elif pos == "row_0_random":
        pr, pc = 0, rng.randint(0, w - 1)
    elif pos == "col_0_random":
        pr, pc = rng.randint(0, h - 1), 0
    else:
        pr, pc = 0, 0
    g[pr][pc] = primary
    for c in range(w):
        r = _pick_red_row(distribution, c, w, rmin, rmax, rng)
        if r == pr and c == pc:
            r = min(rmax, r + 1) if r + 1 <= rmax else max(rmin, r - 1)
        g[r][c] = 2
    return g


def _pick_red_row(distribution, c, w, rmin, rmax, rng):
    if distribution == "uniform":
        return rng.randint(rmin, rmax)
    if distribution == "increasing":
        return rmin + (rmax - rmin) * c // max(1, w - 1)
    if distribution == "decreasing":
        return rmax - (rmax - rmin) * c // max(1, w - 1)
    if distribution == "centered":
        center = (rmin + rmax) // 2
        d = abs(c - w // 2)
        return max(rmin, min(rmax, center - d))
    if distribution == "edges":
        if c < w // 2:
            return rmin
        return rmax
    if distribution == "alternating":
        return rmin if c % 2 == 0 else rmax
    return rng.randint(rmin, rmax)


def _draw_from_degenerate(name, h, w, rng):
    g = full_grid(h, w, 0)
    if name == "no_primary":
        # Reds but no primary color → rule has no primary to use
        for c in range(w):
            g[h // 2][c] = 2
        return g
    if name == "no_reds":
        # Primary but no reds → rule's column rules don't fire
        g[0][0] = 3
        return g
    if name == "full_grid":
        primary = 4
        for r in range(h):
            for c in range(w):
                g[r][c] = primary if (r + c) % 2 == 0 else 2
        return g
    return g
