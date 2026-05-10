"""Generator for 8a371977.

Rule: bg=1; objects in grid layout; rule recolors boundary objects red,
interior green.

Combinatorial axes (8): grid_h/w, n_rows, n_cols, obj_h_max, obj_w_max,
palette_kind, anchor_corner, asymmetry_force.
Degenerates: single_object, no_objects, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "dfef186a194a"
VERSION = "1.1.0"
TASK_ID = "dfef186a194a"
SUMMARY = "Objects in grid layout on bg=1; rule recolors boundary red, interior green."

INVARIANTS = [
    "background is 1",
    "all non-bg objects share a single color",
    "objects arranged in NxM grid where N, M >= 3",
    "objects separated by at least 1 cell of bg",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("single_object", "no_objects", "full_grid")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 14..18", "valid": "12..22"},
    "grid_w":         {"type": "int", "default": "rng 14..18", "valid": "12..22"},
    "n_rows":         {"type": "int", "default": "rng 3..4", "valid": "3..5"},
    "n_cols":         {"type": "int", "default": "rng 3..4", "valid": "3..5"},
    "obj_h_max":      {"type": "int", "default": "2", "valid": "1..3"},
    "obj_w_max":      {"type": "int", "default": "2", "valid": "1..3"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
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
        h_lo, h_hi = 12, 14
        nr_choices = (3,)
    elif difficulty == "hard":
        h_lo, h_hi = 18, 22
        nr_choices = (3, 4, 5)
    else:
        h_lo, h_hi = 14, 18
        nr_choices = (3, 4)
    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", h_lo, h_hi)
    palette_kind = (overrides.get("texture") or
                    overrides.get("palette_kind")
                    or ctx.draw_choice("palette_kind",
                                       list(PALETTE_KINDS)))
    pal = _build_palette(palette_kind, rng)
    obj_color = pal[0] if pal else 5
    n_rows = int(overrides.get("n_rows",
                               rng.choice(nr_choices)))
    n_cols = int(overrides.get("n_cols",
                               rng.choice(nr_choices)))
    n_rows = max(3, min(5, n_rows))
    n_cols = max(3, min(5, n_cols))
    cell_h = h // (n_rows + 1)
    cell_w = w // (n_cols + 1)
    if cell_h < 2 or cell_w < 2:
        return _draw_from_degenerate("no_objects", rng)
    g = full_grid(h, w, 1)
    for ri in range(n_rows):
        for ci in range(n_cols):
            tr = (ri + 1) * cell_h - rng.randint(0, 1)
            tc = (ci + 1) * cell_w - rng.randint(0, 1)
            if tr >= h - 1 or tc >= w - 1:
                continue
            obj_h = rng.choice([1, 2])
            obj_w = rng.choice([1, 2])
            if tr + obj_h > h or tc + obj_w > w:
                continue
            for dr in range(obj_h):
                for dc in range(obj_w):
                    g[tr + dr][tc + dc] = obj_color
    return g


def _build_palette(kind, rng):
    if kind == "warm":
        pool = [4, 6, 9]
    elif kind == "cool":
        pool = [5, 7, 8]
    elif kind == "primary":
        pool = [4]
    else:
        pool = [4, 5, 6, 7, 8, 9]
    pool = [c for c in pool if c not in (1, 2, 3)]
    rng.shuffle(pool)
    return pool


def _draw_from_degenerate(name, rng):
    h, w = 16, 16
    g = full_grid(h, w, 1)
    if name == "single_object":
        g[7][7] = 5; g[7][8] = 5
        return g
    if name == "no_objects":
        return g
    if name == "full_grid":
        for r in range(h):
            for c in range(w):
                g[r][c] = 5
        return g
    return g
