"""Generator for ea9794b1.

Rule: even-dim grid, 4 quadrants. Output (hh × hw): for each (r, c)
take TL; if BR non-0 override; if BL non-0 override; if TR non-0
override (priority: TR > BL > BR > TL).

Combinatorial axes (8): grid_n, palette_size, quadrant_density,
quadrant_layout, decoy_density, asymmetry_force, anchor_corners,
quad_disjoint.
Degenerates: empty_quadrants, full_quadrants, single_quadrant.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "f112ec4615da"
VERSION = "1.1.0"
TASK_ID = "f112ec4615da"
SUMMARY = "Even-dim grid; 4 quadrants of distinct colors; rule overlays them."

INVARIANTS = [
    "h and w both even and >=4",
    "each quadrant has >=1 non-bg cell",
    "the 4 quadrant colors are distinct",
    "background is 0",
]

LAYOUT_KINDS = ("scattered", "blob", "diagonal", "stripes",
                "row_dominant", "checker", "frame")
DEGENERATE_TEXTURES = ("empty_quadrants", "full_quadrants", "single_quadrant")
HELPFUL_TEXTURES = LAYOUT_KINDS

AXES = {
    "grid_n":             {"type": "int", "default": "rng 6..14 even",
                           "valid": "4..18 even"},
    "palette_size":       {"type": "int", "default": "4", "valid": "4..8"},
    "quadrant_density":   {"type": "float", "default": "rng 0.3..0.55",
                           "valid": "0.1..0.85"},
    "quadrant_layout":    {"type": "str", "default": "rng helpful",
                           "valid": "|".join(LAYOUT_KINDS)},
    "asymmetry_force":    {"type": "bool", "default": "true",
                           "valid": "true|false"},
    "anchor_corners":     {"type": "bool", "default": "false",
                           "valid": "true|false"},
    "decoy_density":      {"type": "float", "default": "0", "valid": "0..0.05"},
    "noise_overlay":      {"type": "float", "default": "0", "valid": "0..0.05"},
    "texture":            {"type": "str", "default": "alias for quadrant_layout",
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
        n_choices = [6, 8, 10, 12, 14]
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        n = rng.choice(n_choices)
        return _draw_from_degenerate(overrides["texture"], n, rng)
    n = int(overrides.get("grid_n", rng.choice(n_choices)))
    if n % 2 == 1:
        n += 1
    n = max(4, min(18, n))
    pal = rng.sample([1, 2, 3, 4, 5, 6, 7, 8, 9], 4)
    layout = (overrides.get("texture") or overrides.get("quadrant_layout")
              or ctx.draw_choice("quadrant_layout", list(LAYOUT_KINDS)))
    density = float(overrides.get("quadrant_density",
                                  ctx.draw_rng("quadrant_density")
                                  .uniform(0.3, 0.55)))
    g = full_grid(n, n, 0)
    hh = n // 2
    quads = [(0, 0, pal[0]), (0, hh, pal[1]),
             (hh, 0, pal[2]), (hh, hh, pal[3])]
    for r0, c0, color in quads:
        _fill_quadrant(g, r0, c0, hh, color, layout, density, rng)
    if bool(overrides.get("anchor_corners", False)):
        g[0][0] = pal[0]
        g[0][n - 1] = pal[1]
        g[n - 1][0] = pal[2]
        g[n - 1][n - 1] = pal[3]
    for r0, c0, color in quads:
        if not any(g[r0 + r][c0 + c] == color
                   for r in range(hh) for c in range(hh)):
            g[r0][c0] = color
    return g


def _fill_quadrant(g, r0, c0, hh, color, layout, density, rng):
    if layout == "blob":
        cr = rng.randint(0, hh - 1); cc = rng.randint(0, hh - 1)
        for r in range(hh):
            for c in range(hh):
                if abs(r - cr) + abs(c - cc) <= max(2, hh // 2) \
                        and rng.random() < density:
                    g[r0 + r][c0 + c] = color
        return
    if layout == "diagonal":
        for k in range(hh):
            g[r0 + k][c0 + k] = color
        return
    if layout == "stripes":
        horiz = rng.random() < 0.5
        for r in range(hh):
            for c in range(hh):
                if horiz and r % 2 == 0 and rng.random() < density + 0.2:
                    g[r0 + r][c0 + c] = color
                elif not horiz and c % 2 == 0 and rng.random() < density + 0.2:
                    g[r0 + r][c0 + c] = color
        return
    if layout == "row_dominant":
        target_r = rng.randint(0, hh - 1)
        for c in range(hh):
            g[r0 + target_r][c0 + c] = color
        return
    if layout == "checker":
        for r in range(hh):
            for c in range(hh):
                if (r + c) % 2 == 0 and rng.random() < density + 0.2:
                    g[r0 + r][c0 + c] = color
        return
    if layout == "frame":
        for r in range(hh):
            for c in range(hh):
                if r in (0, hh - 1) or c in (0, hh - 1):
                    g[r0 + r][c0 + c] = color
        return
    for r in range(hh):
        for c in range(hh):
            if rng.random() < density:
                g[r0 + r][c0 + c] = color


def _draw_from_degenerate(name, n, rng):
    g = full_grid(n, n, 0)
    pal = rng.sample([1, 2, 3, 4, 5, 6, 7, 8, 9], 4)
    hh = n // 2
    if name == "empty_quadrants":
        for i, (r0, c0) in enumerate([(0, 0), (0, hh), (hh, 0), (hh, hh)]):
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
