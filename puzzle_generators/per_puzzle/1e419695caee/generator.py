"""Generator for arc_additional_puzzle_bank_volume6:M41 — Recolor magenta(6) objects by hole count.

Rule: for each magenta(6) object, recolor by hole count:
  0 holes → 2; 1 hole → 3; 2+ holes → 4.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_obj,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: all_solid, all_frames, no_magenta.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid
from puzzle_generators.helpers.blobs import has_neighbor

GENERATOR_ID = "1e419695caee"
VERSION = "1.1.0"
TASK_ID = "1e419695caee"
SUMMARY = "Several magenta-6 objects with mixed hole counts; output recolors by hole count."

INVARIANTS = [
    "between 2 and 3 magenta-6 objects",
    "objects span hole counts (0, 1, optionally 2)",
    "objects don't touch and bboxes don't overlap",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("all_solid", "all_frames", "no_magenta")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 7..10", "valid": "6..14"},
    "grid_w":         {"type": "int", "default": "rng 12..18", "valid": "10..22"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_obj":          {"type": "int", "default": "rng 2..3", "valid": "2..4"},
    "palette_size":   {"type": "int", "default": "1", "valid": "1"},
    "position_bias":  {"type": "str", "default": "horizontal_strip",
                       "valid": "horizontal_strip"},
    "n_distinct_colors": {"type": "int", "default": "1", "valid": "1"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def _solid_rect(rh, rw, r1, c1):
    return {(r1 + dr, c1 + dc) for dr in range(rh) for dc in range(rw)}


def _hollow_frame(rh, rw, r1, c1):
    cells = set()
    for c in range(c1, c1 + rw):
        cells.add((r1, c)); cells.add((r1 + rh - 1, c))
    for r in range(r1, r1 + rh):
        cells.add((r, c1)); cells.add((r, c1 + rw - 1))
    return cells


def _double_frame(rh, rw, r1, c1):
    cells = _hollow_frame(rh, rw, r1, c1)
    mid = r1 + rh // 2
    for c in range(c1, c1 + rw):
        cells.add((mid, c))
    return cells


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 7, 8)
        w = ctx.draw_int("grid_w", 12, 14)
        n_obj = 2
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 16, 18)
        n_obj = 3
    else:
        h = ctx.draw_int("grid_h", 7, 10)
        w = ctx.draw_int("grid_w", 12, 18)
        n_obj = ctx.draw_int("n_obj", 2, 3)
    g = full_grid(h, w, 0)
    rng = ctx.draw_rng("layout")

    plans = ["solid", "frame"] + (["dbl"] if n_obj >= 3 else [])
    rng.shuffle(plans)

    cur_c = 1
    used = set()
    for kind in plans:
        if kind == "solid":
            rh = rng.randint(2, 3); rw = rng.randint(2, 3)
            cells = _solid_rect(rh, rw, 0, 0)
        elif kind == "frame":
            rh = 4; rw = 4
            cells = _hollow_frame(rh, rw, 0, 0)
        else:
            rh = 5; rw = 4
            cells = _double_frame(rh, rw, 0, 0)
        rs = [r for r, _ in cells]; cs = [c for _, c in cells]
        bh = max(rs) - min(rs) + 1; bw = max(cs) - min(cs) + 1
        if cur_c + bw + 1 >= w: continue
        rr = rng.randint(0, h - bh)
        rc = cur_c
        placed = {(rr + r - min(rs), rc + c - min(cs)) for r, c in cells}
        if any(p in used or has_neighbor(p, used, ignore=placed) for p in placed):
            cur_c += bw + 2; continue
        used |= placed
        for r, c in placed: g[r][c] = 6
        cur_c += bw + 2
    return g


def _draw_from_degenerate(name, rng):
    h, w = 8, 14
    g = full_grid(h, w, 0)
    if name == "all_solid":
        # all magenta objects are solid (0 holes) → only the 0-hole → 2 branch fires
        for r in range(1, 3):
            for c in range(1, 4):
                g[r][c] = 6
        for r in range(4, 6):
            for c in range(7, 10):
                g[r][c] = 6
        return g
    if name == "all_frames":
        # all magenta objects are hollow frames (1 hole) → only the 1-hole → 3 branch fires
        for r in range(1, 5):
            g[r][1] = 6; g[r][4] = 6
        g[1][2] = 6; g[1][3] = 6; g[4][2] = 6; g[4][3] = 6
        for r in range(2, 6):
            g[r][8] = 6; g[r][11] = 6
        g[2][9] = 6; g[2][10] = 6; g[5][9] = 6; g[5][10] = 6
        return g
    if name == "no_magenta":
        # no color-6 cells → rule has no objects to recolor
        for r in range(2, 4):
            for c in range(3, 5):
                g[r][c] = 4
        for r in range(5, 7):
            for c in range(8, 11):
                g[r][c] = 8
        return g
    return g
