"""Generator for 2faf500b.

Rule: color-9 markers inside each component move one cell outward from
the component half they occupy.

Combinatorial axes (8): grid_h/w, orientation, base_color, comp_h, comp_w,
n_markers, palette_kind, anchor_corner.
Degenerates: no_markers, only_markers, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import draw_rect, full_grid

GENERATOR_ID = "6b5d8752c5c4"
VERSION = "1.1.0"
TASK_ID = "6b5d8752c5c4"
SUMMARY = "Color-9 markers inside component move 1 cell outward by half occupied."

INVARIANTS = [
    "nonzero cells form one or more 8-connected components",
    "each component contains color-9 marker cells",
    "wide components split left/right and tall components split top/bottom",
    "the output contains only shifted color-9 marker cells",
]

ORIENTATIONS = ("wide", "tall")
PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_markers", "only_markers", "full_grid")
HELPFUL_TEXTURES = ORIENTATIONS

AXES = {
    "grid_h":         {"type": "int", "default": "11", "valid": "8..16"},
    "grid_w":         {"type": "int", "default": "13", "valid": "8..18"},
    "orientation":    {"type": "str", "default": "rng wide/tall",
                       "valid": "|".join(ORIENTATIONS)},
    "base_color":     {"type": "color", "default": "rng !0,9", "valid": "1..8"},
    "comp_h":         {"type": "int", "default": "rng 3..6", "valid": "3..7"},
    "comp_w":         {"type": "int", "default": "rng 3..6", "valid": "3..7"},
    "n_markers":      {"type": "int", "default": "rng 2..3", "valid": "2..4"},
    "palette_kind":   {"type": "str", "default": "rng",
                       "valid": "|".join(PALETTE_KINDS)},
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
    if difficulty == "easy":
        h, w = 9, 11
    elif difficulty == "hard":
        h, w = 14, 18
    else:
        h, w = 11, 13
    h = int(overrides.get("grid_h", h))
    w = int(overrides.get("grid_w", w))
    orientation = (overrides.get("texture") if overrides.get("texture") in ORIENTATIONS else None) or \
                  overrides.get("orientation") or \
                  ctx.draw_choice("orientation", list(ORIENTATIONS))
    palette_kind = overrides.get("palette_kind",
                                 ctx.draw_choice("palette_kind",
                                                 list(PALETTE_KINDS)))
    pal = _build_palette(palette_kind, rng)
    base_color = int(overrides.get("base_color", rng.choice(pal)))
    g = full_grid(h, w, 0)
    r0 = rng.randint(2, max(2, h // 3))
    c0 = rng.randint(2, max(2, w // 3))
    if orientation == "wide":
        ch = int(overrides.get("comp_h", 3))
        cw = int(overrides.get("comp_w", 6))
        ch = min(ch, h - r0 - 1)
        cw = min(cw, w - c0 - 1)
        draw_rect(g, r0, c0, ch, cw, base_color)
        markers = [(r0 + 1, c0 + 1), (r0 + 1, c0 + cw - 2)]
        if rng.random() < 0.5:
            markers.append((r0 + 1, c0 + 2))
    else:
        ch = int(overrides.get("comp_h", 6))
        cw = int(overrides.get("comp_w", 3))
        ch = min(ch, h - r0 - 1)
        cw = min(cw, w - c0 - 1)
        draw_rect(g, r0, c0, ch, cw, base_color)
        markers = [(r0 + 1, c0 + 1), (r0 + ch - 2, c0 + 1)]
        if rng.random() < 0.5:
            markers.append((r0 + 2, c0 + 1))
    for r, c in markers:
        if 0 <= r < h and 0 <= c < w:
            g[r][c] = 9
    return g


def _build_palette(kind, rng):
    if kind == "warm":
        pool = [2, 3, 4, 6]
    elif kind == "cool":
        pool = [1, 5, 7, 8]
    elif kind == "primary":
        pool = [1, 2, 3, 4]
    else:
        pool = [1, 2, 3, 4, 5, 6, 7, 8]
    pool = [c for c in pool if c not in (0, 9)]
    rng.shuffle(pool)
    return pool


def _draw_from_degenerate(name, rng):
    h, w = 11, 13
    g = full_grid(h, w, 0)
    if name == "no_markers":
        draw_rect(g, 3, 3, 3, 6, 2)
        return g
    if name == "only_markers":
        g[3][3] = 9
        g[5][7] = 9
        return g
    if name == "full_grid":
        for r in range(h):
            for c in range(w):
                g[r][c] = 9
        return g
    return g
