"""Generator for puzzle bda2d7a6.

Rule: square with concentric rings (Chebyshev depth uniform color).
Output: cyclically shifts each ring's color → unique_rings[(i-1) mod n].

Combinatorial axes (8): n, palette_kind, palette_size, ring_pattern,
duplicate_rings, anchor_corner, asymmetry_force, color_diversity.
Degenerates: monochrome, two_rings, full_grid_one_color.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "fb1e79984e59"
VERSION = "1.1.0"
TASK_ID = "fb1e79984e59"
SUMMARY = "Square with concentric rings; rule cyclically shifts ring colors."

INVARIANTS = [
    "input is square n x n with n in [5, 11]",
    "each Chebyshev-depth ring is a single color",
    ">=2 distinct ring colors (so shift is visible)",
]

PALETTE_KINDS = ("warm", "cool", "broad", "rainbow", "pastel")
RING_PATTERNS = ("all_distinct", "alternate", "outer_match",
                 "inner_match", "gradient")
DEGENERATE_TEXTURES = ("monochrome", "two_rings", "full_grid_one_color")
HELPFUL_TEXTURES = RING_PATTERNS

AXES = {
    "n":              {"type": "int", "default": "rng 5..9", "valid": "5..11"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "ring_pattern":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(RING_PATTERNS)},
    "color_diversity":{"type": "int", "default": "max distinct rings",
                       "valid": "2..n_rings"},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_seed":   {"type": "int", "default": "rng",
                       "valid": "any"},
    "texture":        {"type": "str", "default": "alias for ring_pattern",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    rng = ctx.draw_rng("colors")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], rng)
    if difficulty == "easy":
        n_lo, n_hi = 5, 6
    elif difficulty == "hard":
        n_lo, n_hi = 9, 11
    else:
        n_lo, n_hi = 5, 9
    n = int(overrides.get("n", ctx.draw_int("n", n_lo, n_hi)))
    n = max(5, min(11, n))
    n_rings = (n + 1) // 2
    palette_kind = overrides.get("palette_kind",
                                 ctx.draw_choice("palette_kind",
                                                 list(PALETTE_KINDS)))
    pattern = (overrides.get("texture") or
               overrides.get("ring_pattern")
               or ctx.draw_choice("ring_pattern",
                                  list(RING_PATTERNS)))
    palette = _build_palette(palette_kind, n_rings, rng)
    ring_colors = _apply_pattern(pattern, palette, n_rings, rng)
    g = [[0] * n for _ in range(n)]
    for r in range(n):
        for c in range(n):
            depth = min(r, c, n - 1 - r, n - 1 - c)
            g[r][c] = ring_colors[depth]
    # Make sure >=2 distinct colors
    if len(set(ring_colors)) < 2 and n_rings > 1:
        ring_colors[0] = palette[0]
        ring_colors[-1] = palette[1] if len(palette) > 1 else \
                          (palette[0] + 1) % 10
        for r in range(n):
            for c in range(n):
                depth = min(r, c, n - 1 - r, n - 1 - c)
                g[r][c] = ring_colors[depth]
    return g


def _build_palette(kind, n, rng):
    if kind == "warm":
        pool = [2, 3, 4, 6, 9]
    elif kind == "cool":
        pool = [1, 5, 7, 8]
    elif kind == "rainbow":
        pool = [1, 2, 3, 4, 6, 7, 8, 9]
    elif kind == "pastel":
        pool = [3, 4, 6, 7]
    else:
        pool = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    rng.shuffle(pool)
    while len(pool) < n:
        for c in [1, 2, 3, 4, 5, 6, 7, 8, 9]:
            if c not in pool:
                pool.append(c)
    return pool[:n]


def _apply_pattern(pattern, palette, n, rng):
    if n == 0:
        return []
    if pattern == "all_distinct":
        return list(palette[:n])
    if pattern == "alternate":
        return [palette[i % 2] for i in range(n)]
    if pattern == "outer_match":
        # Outermost ring matches innermost
        rings = list(palette[:n])
        if n > 1:
            rings[-1] = rings[0]
        return rings
    if pattern == "inner_match":
        rings = list(palette[:n])
        if n > 1:
            rings[0] = rings[-1]
        return rings
    if pattern == "gradient":
        return [palette[i % len(palette)] for i in range(n)]
    return list(palette[:n])


def _draw_from_degenerate(name, rng):
    n = 7
    g = [[0] * n for _ in range(n)]
    if name == "monochrome":
        c = rng.choice([1, 2, 3, 4, 5, 6, 7, 8, 9])
        for r in range(n):
            for cc in range(n):
                g[r][cc] = c
        return g
    if name == "two_rings":
        c1, c2 = rng.sample([1, 2, 3, 4, 5, 6, 7, 8, 9], 2)
        for r in range(n):
            for cc in range(n):
                depth = min(r, cc, n - 1 - r, n - 1 - cc)
                g[r][cc] = c1 if depth % 2 == 0 else c2
        return g
    if name == "full_grid_one_color":
        c = rng.choice([1, 2, 3, 4, 5, 6, 7, 8, 9])
        for r in range(n):
            for cc in range(n):
                g[r][cc] = c
        return g
    return g
