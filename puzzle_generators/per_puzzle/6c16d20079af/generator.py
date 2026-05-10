"""Generator for 5b:hard_35 — fill holed component with key color.

Rule: a single key cell (value 8 or 9) names the fill color. Output is
the first (in scan order) component with at least one bbox-interior bg
cell, cropped, with its holes filled by the key color.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_solid,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_key, no_holed, no_solid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "6c16d20079af"
VERSION = "1.1.0"
TASK_ID = "6c16d20079af"
SUMMARY = "1 isolated key cell (8 or 9) + 1 holed component + 1-2 non-holed components."

INVARIANTS = [
    "background is 0",
    "exactly one isolated key cell with value in {8, 9}",
    "the first scan-order component has at least one hole (bbox-interior bg)",
    "1-2 other components are solid (no holes)",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_key", "no_holed", "no_solid")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 9..11", "valid": "8..14"},
    "grid_w":         {"type": "int", "default": "rng 11..13", "valid": "10..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_solid":        {"type": "int", "default": "rng 1..2", "valid": "1..3"},
    "palette_size":   {"type": "int", "default": "rng 3..4", "valid": "2..5"},
    "position_bias":  {"type": "str", "default": "holed_top_solid_bottom",
                       "valid": "holed_top_solid_bottom"},
    "n_distinct_colors": {"type": "int", "default": "rng 3..4", "valid": "2..5"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}

_HOLED = [
    [(0, 0), (0, 1), (0, 2), (1, 0), (1, 2), (2, 0), (2, 1), (2, 2)],
    [(0, 0), (0, 1), (0, 2), (0, 3), (1, 0), (1, 3),
     (2, 0), (2, 1), (2, 2), (2, 3)],
]
_SOLID = [
    [(0, 0), (1, 0), (1, 1)],
    [(0, 0), (0, 1), (1, 0)],
    [(0, 0), (0, 1), (1, 0), (1, 1)],
]


def _free(g, r1, c1, r2, c2):
    h, w = len(g), len(g[0])
    if r1 < 0 or c1 < 0 or r2 >= h or c2 >= w: return False
    for r in range(max(0, r1 - 1), min(h, r2 + 2)):
        for c in range(max(0, c1 - 1), min(w, c2 + 2)):
            if g[r][c] != 0: return False
    return True


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 11, 12)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 11, 13)
        w = ctx.draw_int("grid_w", 13, 15)
    else:
        h = ctx.draw_int("grid_h", 9, 11)
        w = ctx.draw_int("grid_w", 11, 13)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    n_solid = rng.randint(1, 2)
    palette = rng.sample([1, 2, 3, 4, 6, 7], 1 + n_solid)
    holed = rng.choice(_HOLED)
    sh = max(r for r, _ in holed) + 1
    sw = max(c for _, c in holed) + 1
    for _ in range(40):
        r0 = rng.randint(0, h // 2 - sh); c0 = rng.randint(0, w - sw)
        if not _free(g, r0, c0, r0 + sh - 1, c0 + sw - 1): continue
        for dr, dc in holed: g[r0 + dr][c0 + dc] = palette[0]
        break
    for color in palette[1:]:
        s = rng.choice(_SOLID)
        ssh = max(r for r, _ in s) + 1
        ssw = max(c for _, c in s) + 1
        for _ in range(40):
            r0 = rng.randint(h // 2, h - ssh); c0 = rng.randint(0, w - ssw)
            if not _free(g, r0, c0, r0 + ssh - 1, c0 + ssw - 1): continue
            for dr, dc in s: g[r0 + dr][c0 + dc] = color
            break
    key = rng.choice([8, 9])
    for _ in range(60):
        r = rng.randint(0, h - 1); c = rng.randint(0, w - 1)
        if g[r][c] != 0: continue
        bad = False
        for dr in (-1, 0, 1):
            for dc in (-1, 0, 1):
                rr, cc = r + dr, c + dc
                if 0 <= rr < h and 0 <= cc < w and g[rr][cc] != 0:
                    bad = True; break
            if bad: break
        if bad: continue
        g[r][c] = key; break
    return g


def _draw_from_degenerate(name, rng):
    h, w = 10, 12
    g = full_grid(h, w, 0)
    if name == "no_key":
        # Components but no key — rule has no fill color for holes.
        for dr, dc in _HOLED[0]: g[1 + dr][1 + dc] = 4
        for dr, dc in _SOLID[0]: g[6 + dr][6 + dc] = 5
        return g
    if name == "no_holed":
        # All components are solid — rule has no holed component to fill.
        g[0][8] = 8
        for dr, dc in _SOLID[0]: g[1 + dr][1 + dc] = 4
        for dr, dc in _SOLID[1]: g[6 + dr][6 + dc] = 5
        return g
    if name == "no_solid":
        # Only a holed component, no solids — rule selects holed (no contrast).
        g[0][8] = 8
        for dr, dc in _HOLED[0]: g[1 + dr][1 + dc] = 4
        return g
    return g
