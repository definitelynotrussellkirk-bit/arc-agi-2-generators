"""Generator for 17829a00.

Rule: top-border colored objects slide upward, bottom-border colored
objects slide downward.

Combinatorial axes (8): grid_h/w, palette_kind, n_top_objs, n_bot_objs,
obj_h, obj_w, anchor_corner, asymmetry_force.
Degenerates: no_objects, no_borders, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import draw_rect, full_grid

GENERATOR_ID = "b320eba4cfd5"
VERSION = "1.1.0"
TASK_ID = "b320eba4cfd5"
SUMMARY = "Top-bordered objects slide up, bottom-bordered objects slide down."

INVARIANTS = [
    "top and bottom border colors are distinct from the background",
    "interior objects use one of the two border colors",
    "top-colored objects normalize to the top interior row",
    "bottom-colored objects normalize to the bottom interior row",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_objects", "no_borders", "full_grid")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 10..14", "valid": "6..20"},
    "grid_w":         {"type": "int", "default": "rng 10..14", "valid": "6..20"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_top_objs":     {"type": "int", "default": "1", "valid": "1..3"},
    "n_bot_objs":     {"type": "int", "default": "1", "valid": "1..3"},
    "obj_h":          {"type": "int", "default": "2", "valid": "2..3"},
    "obj_w":          {"type": "int", "default": "2", "valid": "2..3"},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
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
        h_lo, h_hi = 6, 10
        nt_lo, nt_hi = 1, 1
    elif difficulty == "hard":
        h_lo, h_hi = 14, 20
        nt_lo, nt_hi = 2, 3
    else:
        h_lo, h_hi = 10, 14
        nt_lo, nt_hi = 1, 2
    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", h_lo, h_hi)
    palette_kind = (overrides.get("texture") or
                    overrides.get("palette_kind")
                    or ctx.draw_choice("palette_kind",
                                       list(PALETTE_KINDS)))
    pal = _build_palette(palette_kind, 2, rng)
    top = pal[0]
    bottom = pal[1] if len(pal) > 1 else 6
    g = full_grid(h, w, 0)
    g[0][0] = top
    g[h - 1][0] = bottom
    n_top = int(overrides.get("n_top_objs",
                              ctx.draw_int("n_top_objs", nt_lo, nt_hi)))
    n_bot = int(overrides.get("n_bot_objs",
                              ctx.draw_int("n_bot_objs", nt_lo, nt_hi)))
    obj_h = int(overrides.get("obj_h", 2))
    obj_w = int(overrides.get("obj_w", 2))
    for _ in range(n_top):
        rr = rng.randint(3, max(3, h // 2))
        cc = rng.randint(2, max(2, w - obj_w - 2))
        if rr + obj_h <= h and cc + obj_w <= w:
            draw_rect(g, rr, cc, obj_h, obj_w, top)
    for _ in range(n_bot):
        rr = rng.randint(min(h - obj_h - 1, h // 2), h - obj_h - 1)
        cc = rng.randint(2, max(2, w - obj_w - 2))
        if rr + obj_h <= h and cc + obj_w <= w:
            draw_rect(g, rr, cc, obj_h, obj_w, bottom)
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
    if len(pool) < n:
        for c in [1, 2, 3, 4, 5, 6, 7, 8, 9]:
            if c not in pool:
                pool.append(c)
            if len(pool) >= n:
                break
    return pool[:n]


def _draw_from_degenerate(name, rng):
    h, w = 12, 12
    g = full_grid(h, w, 0)
    if name == "no_objects":
        g[0][0] = 1; g[h - 1][0] = 2
        return g
    if name == "no_borders":
        draw_rect(g, 3, 3, 2, 2, 1)
        return g
    if name == "full_grid":
        for r in range(h):
            for c in range(w):
                g[r][c] = 1
        return g
    return g
