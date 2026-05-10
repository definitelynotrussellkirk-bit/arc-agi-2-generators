"""Generator for 75b8110e.

Rule: even-dim grid split into 4 quadrants. Output is hh×hw where
each cell starts as TL value; if BR non-0 override; if BL non-0
override; if TR non-0 override. (TR > BL > BR > TL priority.)

Combinatorial axes (8): grid_n, palette_size, quadrant_density,
distinct_quadrants, layout_kind, decoy_density, asymmetry_force,
quadrant_disjoint.
Degenerates: empty_quadrants, full_quadrants, single_quadrant.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "18a3c532c9dc"
VERSION = "1.1.0"
TASK_ID = "18a3c532c9dc"
SUMMARY = "Even-dim grid; 4 quadrants of distinct colors; rule overlays them."

INVARIANTS = [
    "h and w both even and >=4",
    "each quadrant has >=1 non-bg cell (so overlays have content)",
    "the 4 quadrant colors are distinct (so output traces back uniquely)",
    "background is 0",
]

LAYOUT_KINDS = ("scattered", "blob", "diagonal", "stripes",
                "row_dominant", "checker")
DEGENERATE_TEXTURES = ("empty_quadrants", "full_quadrants", "single_quadrant")
HELPFUL_TEXTURES = LAYOUT_KINDS

AXES = {
    "grid_n":             {"type": "int", "default": "rng 6..16 even",
                           "valid": "4..20 even"},
    "palette_size":       {"type": "int", "default": "4", "valid": "4..8"},
    "quadrant_density":   {"type": "float", "default": "rng 0.3..0.6",
                           "valid": "0.1..0.85"},
    "layout_kind":        {"type": "str", "default": "rng helpful",
                           "valid": "|".join(LAYOUT_KINDS)},
    "asymmetry_force":    {"type": "bool", "default": "true", "valid": "true|false"},
    "quadrant_disjoint":  {"type": "bool", "default": "false", "valid": "true|false"},
    "anchor_corners":     {"type": "bool", "default": "false", "valid": "true|false"},
    "noise_overlay":      {"type": "float", "default": "0", "valid": "0..0.05"},
    "texture":            {"type": "str", "default": "alias for layout_kind",
                           "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if difficulty == "easy":
        n_choices = [4, 6]
    elif difficulty == "hard":
        n_choices = [12, 14, 16]
    else:
        n_choices = [6, 8, 10, 12]
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        n = rng.choice(n_choices)
        return _draw_from_degenerate(overrides["texture"], n, rng)
    n = int(overrides.get("grid_n", rng.choice(n_choices)))
    if n % 2 == 1:
        n += 1
    n = max(4, min(20, n))
    pal = rng.sample([1, 2, 3, 4, 5, 6, 7, 8, 9], 4)
    layout = (overrides.get("texture") or overrides.get("layout_kind")
              or ctx.draw_choice("layout_kind", list(LAYOUT_KINDS)))
    density = float(overrides.get("quadrant_density",
                                  ctx.draw_rng("quadrant_density")
                                  .uniform(0.3, 0.6)))
    g = full_grid(n, n, 0)
    hh = n // 2
    quads = [(0, 0, pal[0]), (0, hh, pal[1]), (hh, 0, pal[2]), (hh, hh, pal[3])]
    for r0, c0, color in quads:
        _fill_quadrant(g, r0, c0, hh, color, layout, density, rng)
    if bool(overrides.get("anchor_corners", False)):
        g[0][0] = pal[0]
        g[0][n - 1] = pal[1]
        g[n - 1][0] = pal[2]
        g[n - 1][n - 1] = pal[3]
    for q_idx, (r0, c0, color) in enumerate(quads):
        has_color = any(g[r0 + r][c0 + c] == color
                        for r in range(hh) for c in range(hh))
        if not has_color:
            g[r0][c0] = color
    return g


def _fill_quadrant(g, r0, c0, hh, color, layout, density, rng):
    if layout == "blob":
        cr = rng.randint(0, hh - 1)
        cc = rng.randint(0, hh - 1)
        for r in range(hh):
            for c in range(hh):
                d = abs(r - cr) + abs(c - cc)
                if d <= hh // 2 and rng.random() < density:
                    g[r0 + r][c0 + c] = color
    elif layout == "diagonal":
        for k in range(hh):
            g[r0 + k][c0 + k] = color
    elif layout == "stripes":
        horiz = rng.random() < 0.5
        for r in range(hh):
            for c in range(hh):
                if horiz and r % 2 == 0:
                    g[r0 + r][c0 + c] = color
                elif not horiz and c % 2 == 0:
                    g[r0 + r][c0 + c] = color
    elif layout == "row_dominant":
        target_r = rng.randint(0, hh - 1)
        for c in range(hh):
            g[r0 + target_r][c0 + c] = color
        for r in range(hh):
            for c in range(hh):
                if rng.random() < density / 2:
                    g[r0 + r][c0 + c] = color
    elif layout == "checker":
        for r in range(hh):
            for c in range(hh):
                if (r + c) % 2 == 0 and rng.random() < density + 0.2:
                    g[r0 + r][c0 + c] = color
    else:  # scattered
        for r in range(hh):
            for c in range(hh):
                if rng.random() < density:
                    g[r0 + r][c0 + c] = color


def _draw_from_degenerate(name, n, rng):
    g = full_grid(n, n, 0)
    pal = rng.sample([1, 2, 3, 4, 5, 6, 7, 8, 9], 4)
    hh = n // 2
    if name == "empty_quadrants":
        for i, (r0, c0, _) in enumerate([(0, 0, 0), (0, hh, 0),
                                          (hh, 0, 0), (hh, hh, 0)]):
            g[r0][c0] = pal[i]
        return g
    if name == "full_quadrants":
        for i, (r0, c0) in enumerate([(0, 0), (0, hh), (hh, 0), (hh, hh)]):
            for r in range(hh):
                for c in range(hh):
                    g[r0 + r][c0 + c] = pal[i]
        return g
    if name == "single_quadrant":
        for r in range(hh):
            for c in range(hh):
                g[r][c] = pal[0]
        return g
    return g
