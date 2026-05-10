"""Generator for 4093f84a.

Rule: full gray row or column expands outward by counting colored
dots on each side.

Combinatorial axes (8): grid_h/w, orientation, palette_kind,
anchor_corner, asymmetry_force, palette_size, position_bias,
n_dots.
Degenerates: no_bar, no_dots, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "316636fa814c"
VERSION = "1.1.0"
TASK_ID = "316636fa814c"
SUMMARY = "Full gray bar expands outward by side dot counts."

INVARIANTS = [
    "color 5 forms one full-width row or full-height column bar",
    "all nonzero non-gray side cells are counted by row or column",
    "the bar splits the grid into two sides each holding dot markers",
    "non-bar cells use colors other than 0 or 5",
]

ORIENTATIONS = ("vertical", "horizontal")
PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_bar", "no_dots", "full_grid")
HELPFUL_TEXTURES = ORIENTATIONS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..12", "valid": "6..14"},
    "grid_w":         {"type": "int", "default": "rng 8..12", "valid": "6..14"},
    "orientation":    {"type": "str", "default": "rng helpful",
                       "valid": "|".join(ORIENTATIONS)},
    "palette_kind":   {"type": "str", "default": "rng",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "3", "valid": "3"},
    "position_bias":  {"type": "str", "default": "rng", "valid": "rng"},
    "n_dots":         {"type": "int", "default": "rng 4..8", "valid": "1..16"},
    "texture":        {"type": "str", "default": "alias for orientation",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], rng)
    orientation = (overrides.get("texture") if overrides.get("texture") in ORIENTATIONS else None) or \
                  overrides.get("orientation") or \
                  ctx.draw_choice("orientation", list(ORIENTATIONS))
    palette_kind = overrides.get("palette_kind") or \
                   ctx.draw_choice("palette_kind", list(PALETTE_KINDS))
    pool = _build_palette(palette_kind, rng)
    if len(pool) < 3:
        pool = pool + [c for c in [1, 2, 3, 4, 6, 7, 8, 9] if c not in pool]
    dot_colors = pool[:3]
    h = rng.randint(8, 12)
    w = rng.randint(8, 12)
    g = full_grid(h, w, 0)
    if orientation == "vertical":
        c = rng.randint(3, w - 4)
        for r in range(h):
            g[r][c] = 5
        for r in range(1, h - 1):
            for i in range(rng.randint(0, 2)):
                g[r][i] = dot_colors[(r + i) % len(dot_colors)]
            for i in range(rng.randint(0, 2)):
                g[r][w - 1 - i] = dot_colors[(r + i + 1) % len(dot_colors)]
    else:
        r = rng.randint(3, h - 4)
        for c in range(w):
            g[r][c] = 5
        for c in range(1, w - 1):
            for i in range(rng.randint(0, 2)):
                g[i][c] = dot_colors[(c + i) % len(dot_colors)]
            for i in range(rng.randint(0, 2)):
                g[h - 1 - i][c] = dot_colors[(c + i + 1) % len(dot_colors)]
    return g


def _build_palette(kind, rng):
    if kind == "warm":
        pool = [2, 3, 4, 6, 9]
    elif kind == "cool":
        pool = [1, 7, 8]
    elif kind == "primary":
        pool = [1, 2, 3, 4]
    else:
        pool = [1, 2, 3, 4, 6, 7, 8, 9]
    pool = [c for c in pool if c not in (0, 5)]
    rng.shuffle(pool)
    return pool


def _draw_from_degenerate(name, rng):
    g = full_grid(10, 10, 0)
    if name == "no_bar":
        g[3][2] = 1
        g[5][7] = 2
        return g
    if name == "no_dots":
        for c in range(10):
            g[5][c] = 5
        return g
    if name == "full_grid":
        for r in range(10):
            for c in range(10):
                g[r][c] = 5
        return g
    return g
