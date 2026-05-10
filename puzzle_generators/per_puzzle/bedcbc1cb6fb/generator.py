"""Generator for 99306f82.

Rule: diagonal marker colors fill a blue frame interior with concentric
rectangles from outside-in.

Combinatorial axes (8): grid_h/w, ring_count, palette_kind, frame_h,
frame_w, anchor_corner, asymmetry_force, palette_size.
Degenerates: no_markers, no_frame, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import draw_frame, full_grid

GENERATOR_ID = "bedcbc1cb6fb"
VERSION = "1.1.0"
TASK_ID = "bedcbc1cb6fb"
SUMMARY = "Diagonal marker colors fill blue frame interior with concentric rectangles."

INVARIANTS = [
    "background is color 0",
    "the target frame uses color 1",
    "diagonal markers are nonzero and not color 1",
    "marker order along the main diagonal defines the outside-in fill order",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_markers", "no_frame", "full_grid")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "10", "valid": "8..14"},
    "grid_w":         {"type": "int", "default": "10", "valid": "8..14"},
    "ring_count":     {"type": "int", "default": "3", "valid": "1..4"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "frame_h":        {"type": "int", "default": "6", "valid": "5..8"},
    "frame_w":        {"type": "int", "default": "6", "valid": "5..8"},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "3", "valid": "2..4"},
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
        h, w = 8, 8
        rc_lo, rc_hi = 2, 2
    elif difficulty == "hard":
        h, w = 12, 12
        rc_lo, rc_hi = 3, 4
    else:
        h, w = 10, 10
        rc_lo, rc_hi = 3, 3
    h = int(overrides.get("grid_h", h))
    w = int(overrides.get("grid_w", w))
    rc = int(overrides.get("ring_count",
                           ctx.draw_int("ring_count", rc_lo, rc_hi)))
    rc = max(1, min(4, rc))
    palette_kind = (overrides.get("texture") or
                    overrides.get("palette_kind")
                    or ctx.draw_choice("palette_kind",
                                       list(PALETTE_KINDS)))
    pal = _build_palette(palette_kind, rc, rng)
    g = full_grid(h, w, 0)
    for i, color in enumerate(pal):
        if i < min(h, w):
            g[i][i] = color
    fh = int(overrides.get("frame_h", 6))
    fw = int(overrides.get("frame_w", 6))
    fh = max(5, min(fh, h - 4))
    fw = max(5, min(fw, w - 4))
    fr = max(3, (h - fh) // 2)
    fc = max(3, (w - fw) // 2)
    draw_frame(g, fr, fc, fr + fh - 1, fc + fw - 1, 1)
    return g


def _build_palette(kind, n, rng):
    if kind == "warm":
        pool = [2, 3, 4, 6, 9]
    elif kind == "cool":
        pool = [5, 7, 8]
    elif kind == "primary":
        pool = [2, 3, 4]
    else:
        pool = [2, 3, 4, 5, 6, 7, 8, 9]
    pool = [c for c in pool if c not in (0, 1)]
    rng.shuffle(pool)
    if len(pool) < n:
        for c in [2, 3, 4, 5, 6, 7, 8, 9]:
            if c not in pool:
                pool.append(c)
            if len(pool) >= n:
                break
    return pool[:n]


def _draw_from_degenerate(name, rng):
    h, w = 10, 10
    g = full_grid(h, w, 0)
    if name == "no_markers":
        draw_frame(g, 3, 3, 8, 8, 1)
        return g
    if name == "no_frame":
        for i in range(3):
            g[i][i] = 2 + i
        return g
    if name == "full_grid":
        for r in range(h):
            for c in range(w):
                g[r][c] = 1
        return g
    return g
