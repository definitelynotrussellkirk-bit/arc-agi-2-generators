"""Generator for fcc82909.

Rule: multicolor 8-connected objects on bg=0; rule paints n rows of
green(3) below each object's bbox, where n = object's distinct color
count.

Combinatorial axes (8): grid_h/w, n_objs, obj_h_max, obj_w_max,
palette_kind, palette_size, anchor_corner, asymmetry_force.
Degenerates: green_in_object, single_color_objs, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "e9e7805b09dd"
VERSION = "1.1.0"
TASK_ID = "e9e7805b09dd"
SUMMARY = "Multicolor objects; rule paints n green rows below each, n = distinct color count."

INVARIANTS = [
    "background is 0",
    "objects use colors != 3",
    ">=n rows of bg below each object (where n = distinct colors)",
    "objects' bbox columns don't overlap with another object's below-extension",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("green_in_object", "single_color_objs", "full_grid")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 14..18", "valid": "12..22"},
    "grid_w":         {"type": "int", "default": "rng 14..18", "valid": "12..22"},
    "n_objs":         {"type": "int", "default": "rng 2..3", "valid": "1..4"},
    "obj_h_max":      {"type": "int", "default": "3", "valid": "2..4"},
    "obj_w_max":      {"type": "int", "default": "4", "valid": "3..5"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "palette_size":   {"type": "int", "default": "4", "valid": "3..5"},
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
        no_lo, no_hi = 1, 2
    elif difficulty == "hard":
        h_lo, h_hi = 18, 22
        no_lo, no_hi = 2, 4
    else:
        h_lo, h_hi = 14, 18
        no_lo, no_hi = 2, 3
    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", h_lo, h_hi)
    palette_kind = (overrides.get("texture") or
                    overrides.get("palette_kind")
                    or ctx.draw_choice("palette_kind",
                                       list(PALETTE_KINDS)))
    palette_size = int(overrides.get("palette_size", 4))
    palette = _build_palette(palette_kind, palette_size, rng)
    n_objs = int(overrides.get("n_objs",
                               ctx.draw_int("n_objs", no_lo, no_hi)))
    n_objs = max(1, min(4, n_objs))
    obj_h_max = int(overrides.get("obj_h_max", 3))
    obj_w_max = int(overrides.get("obj_w_max", 4))
    g = full_grid(h, w, 0)
    used_cols = []
    placed = 0
    for _try in range(60):
        if placed >= n_objs:
            break
        oh = rng.randint(2, obj_h_max)
        ow = rng.randint(2, obj_w_max)
        n_colors = rng.randint(1, min(3, len(palette)))
        rr = rng.randint(0, h - oh - n_colors - 1)
        rc = rng.randint(0, w - ow)
        overlap = False
        for (uc1, uc2, ur1, ur2) in used_cols:
            if not (rc + ow <= uc1 or rc >= uc2 + 1):
                overlap = True
                break
        if overlap:
            continue
        obj_palette = rng.sample(palette, n_colors)
        cells_painted = set()
        for dr in range(oh):
            for dc in range(ow):
                if rng.random() < 0.7:
                    g[rr + dr][rc + dc] = rng.choice(obj_palette)
                    cells_painted.add((rr + dr, rc + dc))
        for i, col in enumerate(obj_palette):
            tr = rr + (i % oh)
            tc = rc + (i % ow)
            g[tr][tc] = col
            cells_painted.add((tr, tc))
        for dr in range(oh):
            for dc in range(ow):
                if (rr + dr, rc + dc) not in cells_painted:
                    g[rr + dr][rc + dc] = rng.choice(obj_palette)
        used_cols.append((rc, rc + ow - 1, rr, rr + oh - 1))
        placed += 1
    if placed < 1:
        return _draw_from_degenerate("single_color_objs", rng)
    return g


def _build_palette(kind, n, rng):
    if kind == "warm":
        pool = [2, 4, 6, 9]
    elif kind == "cool":
        pool = [1, 5, 7, 8]
    elif kind == "primary":
        pool = [1, 2, 4]
    else:
        pool = [1, 2, 4, 5, 6, 7, 8, 9]
    pool = [c for c in pool if c != 3]
    rng.shuffle(pool)
    if len(pool) < n:
        for c in [1, 2, 4, 5, 6, 7, 8, 9]:
            if c not in pool:
                pool.append(c)
            if len(pool) >= n:
                break
    return pool[:n]


def _draw_from_degenerate(name, rng):
    h, w = 16, 16
    g = full_grid(h, w, 0)
    if name == "green_in_object":
        for dr in range(2):
            for dc in range(3):
                g[2 + dr][2 + dc] = rng.choice([2, 3, 4])
        return g
    if name == "single_color_objs":
        for dr in range(2):
            for dc in range(2):
                g[3 + dr][3 + dc] = 2
        return g
    if name == "full_grid":
        for r in range(h):
            for c in range(w):
                g[r][c] = 2
        return g
    return g
