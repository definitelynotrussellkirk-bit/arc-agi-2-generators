"""Generator for b548a754.

Rule: a framed rectangle stretches its bbox to include a cyan marker.

Combinatorial axes (8): grid_h/w, marker_side, palette_kind, frame_h,
frame_w, anchor_corner, asymmetry_force, palette_size.
Degenerates: no_marker, no_frame, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import draw_frame, full_grid

GENERATOR_ID = "a3c33cc348fb"
VERSION = "1.1.0"
TASK_ID = "a3c33cc348fb"
SUMMARY = "A framed rectangle stretches its bbox to include a cyan marker."

INVARIANTS = [
    "background is color 0",
    "there is exactly one color-8 marker outside the source rectangle",
    "the source rectangle has a frame color and a distinct interior color",
    "the output rectangle is the old bbox expanded just enough to contain the cyan marker",
]

MARKER_SIDES = ("right", "bottom", "left", "top")
PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_marker", "no_frame", "full_grid")
HELPFUL_TEXTURES = MARKER_SIDES

AXES = {
    "grid_h":         {"type": "int", "default": "13", "valid": "10..18"},
    "grid_w":         {"type": "int", "default": "13", "valid": "10..18"},
    "marker_side":    {"type": "str", "default": "rng helpful",
                       "valid": "|".join(MARKER_SIDES)},
    "palette_kind":   {"type": "str", "default": "rng",
                       "valid": "|".join(PALETTE_KINDS)},
    "frame_h":        {"type": "int", "default": "5", "valid": "4..7"},
    "frame_w":        {"type": "int", "default": "5", "valid": "4..7"},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2"},
    "texture":        {"type": "str", "default": "alias for marker_side",
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
        h, w = 10, 10
    elif difficulty == "hard":
        h, w = 18, 18
    else:
        h, w = 13, 13
    h = int(overrides.get("grid_h", h))
    w = int(overrides.get("grid_w", w))
    side = (overrides.get("texture") if overrides.get("texture") in MARKER_SIDES else None) or \
           overrides.get("marker_side") or \
           ctx.draw_choice("marker_side", list(MARKER_SIDES))
    palette_kind = overrides.get("palette_kind",
                                 ctx.draw_choice("palette_kind",
                                                 list(PALETTE_KINDS)))
    pal = _build_palette(palette_kind, 2, rng)
    frame, inner = pal[0], pal[1]
    g = full_grid(h, w, 0)
    fh = int(overrides.get("frame_h", 5))
    fw = int(overrides.get("frame_w", 5))
    fh = max(4, min(fh, h - 4))
    fw = max(4, min(fw, w - 4))
    r1 = 3
    c1 = 3
    r2 = r1 + fh - 1
    c2 = c1 + fw - 1
    draw_frame(g, r1, c1, r2, c2, frame)
    for r in range(r1 + 1, r2):
        for c in range(c1 + 1, c2):
            g[r][c] = inner
    if side == "right":
        if c2 + 3 < w:
            g[(r1 + r2) // 2][c2 + 3] = 8
    elif side == "bottom":
        if r2 + 3 < h:
            g[r2 + 3][(c1 + c2) // 2] = 8
    elif side == "left":
        if c1 - 3 >= 0:
            g[(r1 + r2) // 2][c1 - 3] = 8
    elif side == "top":
        if r1 - 3 >= 0:
            g[r1 - 3][(c1 + c2) // 2] = 8
    return g


def _build_palette(kind, n, rng):
    if kind == "warm":
        pool = [2, 3, 4, 6, 9]
    elif kind == "cool":
        pool = [1, 5, 7]
    elif kind == "primary":
        pool = [1, 2, 3, 4]
    else:
        pool = [1, 2, 3, 4, 5, 6, 7, 9]
    pool = [c for c in pool if c not in (0, 8)]
    rng.shuffle(pool)
    if len(pool) < n:
        for c in [1, 2, 3, 4, 5, 6, 7, 9]:
            if c not in pool:
                pool.append(c)
            if len(pool) >= n:
                break
    return pool[:n]


def _draw_from_degenerate(name, rng):
    h, w = 13, 13
    g = full_grid(h, w, 0)
    if name == "no_marker":
        draw_frame(g, 3, 3, 7, 7, 2)
        for r in range(4, 7):
            for c in range(4, 7):
                g[r][c] = 3
        return g
    if name == "no_frame":
        g[5][10] = 8
        return g
    if name == "full_grid":
        for r in range(h):
            for c in range(w):
                g[r][c] = 8
        return g
    return g
