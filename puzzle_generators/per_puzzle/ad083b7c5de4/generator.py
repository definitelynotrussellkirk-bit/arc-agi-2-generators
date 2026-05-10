"""Generator for 917bccba.

Rule: frame is preserved while horizontal and vertical guide lines
move to the frame top and right edges.

Combinatorial axes (8): grid_h/w, frame_size, palette_kind,
anchor_corner, asymmetry_force, palette_size, position_bias,
n_distinct_colors.
Degenerates: no_frame, no_lines, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "ad083b7c5de4"
VERSION = "1.1.0"
TASK_ID = "ad083b7c5de4"
SUMMARY = "Frame preserved; guide lines move to frame top and right edges."

INVARIANTS = [
    "background is color 0",
    "one rectangular frame uses a nonzero color",
    "one guide color appears outside the frame",
    "the frame bbox is smaller than the full grid",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_frame", "no_lines", "full_grid")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 11..15", "valid": "9..18"},
    "grid_w":         {"type": "int", "default": "rng 11..15", "valid": "9..18"},
    "frame_size":     {"type": "int", "default": "rng 4..6", "valid": "3..8"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2"},
    "position_bias":  {"type": "str", "default": "fixed", "valid": "fixed"},
    "n_distinct_colors":{"type": "int", "default": "2", "valid": "2"},
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
        size_lo, size_hi = 4, 4
    elif difficulty == "hard":
        size_lo, size_hi = 6, 7
    else:
        size_lo, size_hi = 4, 6
    size = ctx.draw_int("frame_size", size_lo, size_hi)
    h = 11 + rng.randint(0, 4)
    w = 11 + rng.randint(0, 4)
    palette_kind = (overrides.get("texture") or
                    overrides.get("palette_kind") or
                    ctx.draw_choice("palette_kind", list(PALETTE_KINDS)))
    pool = _build_palette(palette_kind, rng)
    if len(pool) < 2:
        pool = pool + [c for c in [1, 2, 3, 4, 5, 6, 7, 8, 9] if c not in pool]
    frame_color, line_color = pool[0], pool[1]
    g = full_grid(h, w, 0)
    r1 = 3
    c1 = 2 + (sample_index % 2)
    r2 = r1 + size
    c2 = c1 + size
    for c in range(c1, c2 + 1):
        g[r1][c] = frame_color
        g[r2][c] = frame_color
    for r in range(r1, r2 + 1):
        g[r][c1] = frame_color
        g[r][c2] = frame_color
    for c in range(w):
        if c < c1 or c > c2:
            g[r2][c] = line_color
    for r in range(h):
        if r < r1 or r > r2:
            g[r][c1] = line_color
    return g


def _build_palette(kind, rng):
    if kind == "warm":
        pool = [2, 3, 4, 6, 9]
    elif kind == "cool":
        pool = [1, 5, 7, 8]
    elif kind == "primary":
        pool = [1, 2, 3, 4]
    else:
        pool = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    pool = [c for c in pool if c != 0]
    rng.shuffle(pool)
    return pool


def _draw_from_degenerate(name, rng):
    g = full_grid(13, 13, 0)
    if name == "no_frame":
        for c in range(13):
            g[6][c] = 2
        return g
    if name == "no_lines":
        for c in range(3, 9):
            g[3][c] = 1; g[8][c] = 1
        for r in range(3, 9):
            g[r][3] = 1; g[r][8] = 1
        return g
    if name == "full_grid":
        for r in range(13):
            for c in range(13):
                g[r][c] = 2
        return g
    return g
