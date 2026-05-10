"""Generator for f0afb749.

Rule: 2× scale + diagonal trail. Each cell becomes a 2×2 block. For
each non-zero cell at (sr, sc), a diagonal trail of 1s is drawn in the
output where r-c == 2*(sr-sc).

Combinatorial axes (8): grid_h/w, n_marks, palette_kind, mark_layout,
position_bias, palette_size, mark_density, anchor_corner.
Degenerates: empty_grid, all_filled, single_diag.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "827c34fc8e04"
VERSION = "1.1.0"
TASK_ID = "827c34fc8e04"
SUMMARY = "Small grid + non-bg cells; rule scales 2× + draws diagonal 1-trails."

INVARIANTS = [
    "h, w in [2, 5]",
    "1-N non-bg cells",
    "no non-bg cell uses color 1 (rule writes 1 for trail)",
]

MARK_LAYOUTS = ("scattered", "diagonal", "anti_diag", "row", "col",
                "corners", "blob")
PALETTE_KINDS = ("warm", "cool", "broad", "small")
DEGENERATE_TEXTURES = ("empty_grid", "all_filled", "single_diag")
HELPFUL_TEXTURES = MARK_LAYOUTS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 2..5", "valid": "2..5"},
    "grid_w":         {"type": "int", "default": "rng 2..5", "valid": "2..5"},
    "n_marks":        {"type": "int", "default": "rng 1..h*w/2",
                       "valid": "1..h*w-1"},
    "mark_layout":    {"type": "str", "default": "rng helpful",
                       "valid": "|".join(MARK_LAYOUTS)},
    "position_bias":  {"type": "str", "default": "rng spread|center|edge",
                       "valid": "spread|center|edge"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "palette_size":   {"type": "int", "default": "rng 1..3", "valid": "1..7"},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "texture":        {"type": "str", "default": "alias for mark_layout",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if difficulty == "easy":
        h_lo, h_hi = 2, 3
    elif difficulty == "hard":
        h_lo, h_hi = 4, 5
    else:
        h_lo, h_hi = 2, 5
    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", h_lo, h_hi)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], h, w, rng)
    n_marks = int(overrides.get("n_marks",
                                ctx.draw_int("n_marks", 1, max(1, h * w // 2))))
    n_marks = max(1, min(h * w - 1, n_marks))
    palette_kind = overrides.get("palette_kind",
                                 ctx.draw_choice("palette_kind",
                                                 list(PALETTE_KINDS)))
    if palette_kind == "warm":
        pool = [3, 4, 6, 9]
    elif palette_kind == "cool":
        pool = [5, 7, 8]
    elif palette_kind == "small":
        pool = [2, 3]
    else:
        pool = [2, 3, 4, 5, 6, 7, 8, 9]
    rng.shuffle(pool)
    n_palette = int(overrides.get("palette_size",
                                  ctx.draw_int("palette_size", 1, 3)))
    palette = pool[:max(1, n_palette)]
    layout = (overrides.get("texture") or overrides.get("mark_layout")
              or ctx.draw_choice("mark_layout", list(MARK_LAYOUTS)))
    bias = overrides.get("position_bias",
                         ctx.draw_choice("position_bias",
                                         ["spread", "center", "edge"]))
    g = full_grid(h, w, 0)
    cells = _layout_cells(layout, h, w, bias, rng)
    for r, c in cells[:n_marks]:
        g[r][c] = rng.choice(palette)
    if bool(overrides.get("anchor_corner", False)):
        g[0][0] = palette[0]
    return g


def _layout_cells(layout, h, w, bias, rng):
    cells = [(r, c) for r in range(h) for c in range(w)]
    if layout == "diagonal":
        diag = [(k, k) for k in range(min(h, w))]
        rest = [c for c in cells if c not in diag]
        rng.shuffle(rest)
        return diag + rest
    if layout == "anti_diag":
        anti = [(k, w - 1 - k) for k in range(min(h, w))]
        rest = [c for c in cells if c not in anti]
        rng.shuffle(rest)
        return anti + rest
    if layout == "row":
        r = rng.randint(0, h - 1)
        chosen = [(r, c) for c in range(w)]
        rest = [cc for cc in cells if cc not in chosen]
        rng.shuffle(rest)
        return chosen + rest
    if layout == "col":
        c = rng.randint(0, w - 1)
        chosen = [(r, c) for r in range(h)]
        rest = [cc for cc in cells if cc not in chosen]
        rng.shuffle(rest)
        return chosen + rest
    if layout == "corners":
        corners = [(0, 0), (0, w - 1), (h - 1, 0), (h - 1, w - 1)]
        rest = [c for c in cells if c not in corners]
        rng.shuffle(rest)
        return corners + rest
    if layout == "blob":
        cr, cc = rng.randint(0, h - 1), rng.randint(0, w - 1)
        cells.sort(key=lambda rc: abs(rc[0] - cr) + abs(rc[1] - cc))
        return cells
    rng.shuffle(cells)
    return cells


def _draw_from_degenerate(name, h, w, rng):
    g = full_grid(h, w, 0)
    color = rng.choice([2, 3, 4, 5, 6, 7, 8, 9])
    if name == "empty_grid":
        return g
    if name == "all_filled":
        for r in range(h):
            for c in range(w):
                g[r][c] = color
        return g
    if name == "single_diag":
        for k in range(min(h, w)):
            g[k][k] = color
        return g
    return g
