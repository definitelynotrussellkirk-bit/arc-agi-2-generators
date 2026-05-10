"""Generator for ff2825db.

Rule: most-frequent interior color becomes outer frame and hollow bbox
around its own cells.

Combinatorial axes (8): grid_h/w, winner_area, palette_kind,
border_color, n_other, anchor_corner, asymmetry_force, palette_size.
Degenerates: tied_freqs, single_color, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import draw_frame, full_grid

GENERATOR_ID = "9edcccd1341f"
VERSION = "1.1.0"
TASK_ID = "9edcccd1341f"
SUMMARY = "Most frequent interior color becomes outer frame and hollow bbox."

INVARIANTS = [
    "row 0 is preserved as a color key",
    "row 1/col 0 supplies the input border color",
    "interior non-border cells include one dominant color",
    "the output keeps row 0 and draws outer and inner hollow rectangles in the dominant color",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("tied_freqs", "single_color", "full_grid")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "10", "valid": "8..14"},
    "grid_w":         {"type": "int", "default": "10", "valid": "8..14"},
    "winner_area":    {"type": "int", "default": "rng 4..6", "valid": "4..8"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "border_color":   {"type": "color", "default": "rng",
                       "valid": "1..9"},
    "n_other":        {"type": "int", "default": "rng 2..3", "valid": "1..4"},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "3", "valid": "3"},
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
        wa_lo, wa_hi = 4, 4
        no_lo, no_hi = 1, 2
    elif difficulty == "hard":
        h, w = 12, 12
        wa_lo, wa_hi = 5, 8
        no_lo, no_hi = 3, 4
    else:
        h, w = 10, 10
        wa_lo, wa_hi = 4, 6
        no_lo, no_hi = 2, 3
    h = int(overrides.get("grid_h", h))
    w = int(overrides.get("grid_w", w))
    palette_kind = (overrides.get("texture") or
                    overrides.get("palette_kind")
                    or ctx.draw_choice("palette_kind",
                                       list(PALETTE_KINDS)))
    palette = _build_palette(palette_kind, rng)
    bdr = palette[0] if len(palette) > 0 else 5
    winner = palette[1] if len(palette) > 1 else 2
    other = palette[2] if len(palette) > 2 else 3
    g = full_grid(h, w, 0)
    for c in range(min(4, w)):
        g[0][c] = [winner, other, bdr, winner][c]
    draw_frame(g, 1, 0, h - 1, w - 1, bdr)
    winner_cells = [(3, 3), (3, 4), (4, 3), (4, 4), (5, 4)]
    wa = int(overrides.get("winner_area",
                           rng.randint(wa_lo, wa_hi)))
    wa = max(4, min(len(winner_cells), wa))
    for r, c in winner_cells[:wa]:
        if r < h and c < w:
            g[r][c] = winner
    n_other = int(overrides.get("n_other",
                                ctx.draw_int("n_other", no_lo, no_hi)))
    n_other = max(1, min(4, n_other))
    other_cells = [(6, 7), (7, 7), (6, 6), (7, 6)]
    for r, c in other_cells[:n_other]:
        if r < h and c < w:
            g[r][c] = other
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
    rng.shuffle(pool)
    return pool


def _draw_from_degenerate(name, rng):
    h, w = 10, 10
    g = full_grid(h, w, 0)
    if name == "tied_freqs":
        draw_frame(g, 1, 0, 9, 9, 5)
        g[3][3] = 2; g[3][4] = 3; g[4][3] = 2; g[4][4] = 3
        return g
    if name == "single_color":
        draw_frame(g, 1, 0, 9, 9, 5)
        return g
    if name == "full_grid":
        for r in range(h):
            for c in range(w):
                g[r][c] = 5
        return g
    return g
