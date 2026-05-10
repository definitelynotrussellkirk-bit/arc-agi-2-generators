"""Generator for puzzle bf699163.

Rule: bg=5. Find bbox of all 7-cells. Among non-7 non-bg objects,
return the crop of the first one whose center is inside that bbox.

Combinatorial axes (8): grid_h/w, frame_h, frame_w, n_outside_glyphs,
glyph_kind, palette_kind, position_bias, anchor_corner.
Degenerates: no_inside, no_frame, single_glyph.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid
from puzzle_generators.helpers.shape import RING_3X3

GENERATOR_ID = "0a7f0faace31"
VERSION = "1.1.0"
TASK_ID = "0a7f0faace31"
SUMMARY = "bg=5 with 7-bbox + glyphs; rule outputs the inside-bbox glyph."

INVARIANTS = [
    "bg = 5",
    "4 7-corners forming a bbox >=7x7",
    "exactly one 3x3 hollow-ring glyph inside the bbox",
    "1-3 other 3x3 hollow-rings outside the bbox",
    "all glyphs have distinct non-{5,7} colors",
]

GLYPH_KINDS = ("hollow_ring", "solid_3x3", "plus", "diagonal", "L_shape")
PALETTE_KINDS = ("warm", "cool", "broad", "primary")
POSITION_BIASES = ("scattered", "corners", "row_aligned", "col_aligned")
DEGENERATE_TEXTURES = ("no_inside", "no_frame", "single_glyph")
HELPFUL_TEXTURES = GLYPH_KINDS

AXES = {
    "grid_h":           {"type": "int", "default": "rng 14..20", "valid": "12..24"},
    "grid_w":           {"type": "int", "default": "rng 14..20", "valid": "12..24"},
    "frame_h":          {"type": "int", "default": "rng 7..10", "valid": "5..14"},
    "frame_w":          {"type": "int", "default": "rng 7..10", "valid": "5..14"},
    "n_outside":        {"type": "int", "default": "rng 2..3", "valid": "1..4"},
    "glyph_kind":       {"type": "str", "default": "rng helpful",
                         "valid": "|".join(GLYPH_KINDS)},
    "palette_kind":     {"type": "str", "default": "rng helpful",
                         "valid": "|".join(PALETTE_KINDS)},
    "position_bias":    {"type": "str", "default": "rng",
                         "valid": "|".join(POSITION_BIASES)},
    "texture":          {"type": "str", "default": "alias for glyph_kind",
                         "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


_GLYPH_CELLS = {
    "hollow_ring": list(RING_3X3),
    "solid_3x3":   [(r, c) for r in range(3) for c in range(3)],
    "plus":        [(0, 1), (1, 0), (1, 1), (1, 2), (2, 1)],
    "diagonal":    [(0, 0), (1, 1), (2, 2), (0, 2), (2, 0)],
    "L_shape":     [(0, 0), (1, 0), (2, 0), (2, 1), (2, 2)],
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if difficulty == "easy":
        h_lo, h_hi = 12, 14
    elif difficulty == "hard":
        h_lo, h_hi = 18, 24
    else:
        h_lo, h_hi = 14, 20
    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", h_lo, h_hi)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], h, w, rng)
    fh = int(overrides.get("frame_h",
                           ctx.draw_int("frame_h", 7, min(10, h - 4))))
    fw = int(overrides.get("frame_w",
                           ctx.draw_int("frame_w", 7, min(10, w - 4))))
    fh = max(7, min(h - 4, fh))
    fw = max(7, min(w - 4, fw))
    n_out = int(overrides.get("n_outside",
                              ctx.draw_int("n_outside", 2, 3)))
    n_out = max(1, min(4, n_out))
    glyph_kind = (overrides.get("texture") or
                  overrides.get("glyph_kind")
                  or ctx.draw_choice("glyph_kind", list(GLYPH_KINDS)))
    palette_kind = overrides.get("palette_kind",
                                 ctx.draw_choice("palette_kind",
                                                 list(PALETTE_KINDS)))
    palette = _build_palette(palette_kind, n_out + 1, rng)
    g = full_grid(h, w, 5)
    fr = rng.randint(0, h - fh - 1)
    fc = rng.randint(0, w - fw - 1)
    g[fr][fc] = 7
    g[fr][fc + fw - 1] = 7
    g[fr + fh - 1][fc] = 7
    g[fr + fh - 1][fc + fw - 1] = 7
    inside_color = palette[0]
    glyph_r = fr + (fh // 2) - 1
    glyph_c = fc + (fw // 2) - 1
    _place_glyph(g, glyph_r, glyph_c, inside_color, glyph_kind)
    placed = 0
    for i in range(n_out * 8):
        if placed >= n_out:
            break
        gr = rng.randint(0, h - 4)
        gc = rng.randint(0, w - 4)
        cr, cc = gr + 1, gc + 1
        if fr <= cr <= fr + fh - 1 and fc <= cc <= fc + fw - 1:
            continue
        ok = True
        for r in range(gr, gr + 3):
            for c in range(gc, gc + 3):
                if g[r][c] != 5:
                    ok = False; break
            if not ok:
                break
        if not ok:
            continue
        _place_glyph(g, gr, gc, palette[1 + placed], glyph_kind)
        placed += 1
    return g


def _place_glyph(g, gr, gc, color, kind):
    cells = _GLYPH_CELLS.get(kind, _GLYPH_CELLS["hollow_ring"])
    for dr, dc in cells:
        if 0 <= gr + dr < len(g) and 0 <= gc + dc < len(g[0]):
            g[gr + dr][gc + dc] = color


def _build_palette(kind, n, rng):
    if kind == "warm":
        pool = [2, 3, 4, 6, 9]
    elif kind == "cool":
        pool = [1, 8]
    elif kind == "primary":
        pool = [1, 2, 3, 4]
    else:
        pool = [1, 2, 3, 4, 6, 8, 9]
    rng.shuffle(pool)
    while len(pool) < n:
        for c in [1, 2, 3, 4, 6, 8, 9]:
            if c not in pool:
                pool.append(c)
    return pool[:n]


def _draw_from_degenerate(name, h, w, rng):
    g = full_grid(h, w, 5)
    if name == "no_inside":
        # Frame but no inside glyph
        fh, fw = 8, 8
        fr, fc = 2, 2
        g[fr][fc] = 7
        g[fr][fc + fw - 1] = 7
        g[fr + fh - 1][fc] = 7
        g[fr + fh - 1][fc + fw - 1] = 7
        return g
    if name == "no_frame":
        # Glyph but no 7-frame
        for dr, dc in RING_3X3:
            g[5 + dr][5 + dc] = 3
        return g
    if name == "single_glyph":
        for dr, dc in RING_3X3:
            g[5 + dr][5 + dc] = 3
        return g
    return g
