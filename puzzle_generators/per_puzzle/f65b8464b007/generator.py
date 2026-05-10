"""Generator for e78887d1.

Rule: N sections each with colored shape; rule rotates shapes through
sections.

Combinatorial axes (8): n_sections, palette_kind, n_cells_min, n_cells_max,
section_w, anchor_corner, asymmetry_force, palette_size.
Degenerates: same_color, no_sections, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "f65b8464b007"
VERSION = "1.1.0"
TASK_ID = "f65b8464b007"
SUMMARY = "5-row grid: 3-4 sections with colored shapes; rule rotates shapes."

INVARIANTS = [
    "h = 5",
    "rows 0 and h-1 are all 0",
    "n sections (3 or 4), each 3-wide, separated by 1-col 0-gaps",
    "each section has >=1 colored cell in rows 1..3, all sections distinct colors",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("same_color", "no_sections", "full_grid")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "n_sections":     {"type": "int", "default": "rng 3..4", "valid": "2..5"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_cells_min":    {"type": "int", "default": "3", "valid": "1..6"},
    "n_cells_max":    {"type": "int", "default": "5", "valid": "3..9"},
    "section_w":      {"type": "int", "default": "3", "valid": "3"},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "rng 3..4", "valid": "2..5"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], rng)
    if difficulty == "easy":
        ns_lo, ns_hi = 2, 3
        nc_lo, nc_hi = 2, 4
    elif difficulty == "hard":
        ns_lo, ns_hi = 4, 5
        nc_lo, nc_hi = 4, 7
    else:
        ns_lo, ns_hi = 3, 4
        nc_lo, nc_hi = 3, 5
    h = 5
    n = ctx.draw_int("n_sections", ns_lo, ns_hi)
    n = max(2, min(5, n))
    sw = 3
    stride = sw + 1
    w = n * stride - 1
    g = full_grid(h, w, 0)
    palette_kind = (overrides.get("texture") or
                    overrides.get("palette_kind")
                    or ctx.draw_choice("palette_kind",
                                       list(PALETTE_KINDS)))
    pool = _build_palette(palette_kind, n, rng)
    if len(pool) < n:
        pool = pool + [c for c in [1, 2, 3, 4, 5, 6, 7, 8, 9] if c not in pool]
    palette = pool[:n]
    nc_min = int(overrides.get("n_cells_min", nc_lo))
    nc_max = int(overrides.get("n_cells_max", nc_hi))
    nc_min = max(1, nc_min)
    nc_max = max(nc_min, min(9, nc_max))
    for i in range(n):
        sc = i * stride
        color = palette[i]
        cells_pool = [(r, c) for r in range(1, 4) for c in range(sc, sc + sw)]
        n_cells = rng.randint(nc_min, min(nc_max, len(cells_pool)))
        chosen = rng.sample(cells_pool, n_cells)
        for r, c in chosen:
            g[r][c] = color
    return g


def _build_palette(kind, n, rng):
    if kind == "warm":
        pool = [2, 3, 4, 6, 9]
    elif kind == "cool":
        pool = [1, 5, 7, 8]
    elif kind == "primary":
        pool = [1, 2, 3, 4]
    else:
        pool = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    rng.shuffle(pool)
    return pool


def _draw_from_degenerate(name, rng):
    h, w = 5, 11
    g = full_grid(h, w, 0)
    if name == "same_color":
        for sc in [0, 4, 8]:
            for r in range(1, 4):
                g[r][sc] = 2
        return g
    if name == "no_sections":
        return g
    if name == "full_grid":
        for r in range(h):
            for c in range(w):
                g[r][c] = 2
        return g
    return g
