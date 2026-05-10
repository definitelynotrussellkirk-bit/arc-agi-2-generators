"""Generator for dce56571.

Rule: bg=8. Single non-8 color C with count cells. Output is 8-bg
grid with horizontal C-bar centered at middle row, length=count.

Combinatorial axes (8): grid_h/w, color, count, cell_layout,
position_bias, palette_size, decoy_density, asymmetry.
Degenerates: no_color, full_color, count_too_large.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "4a46459a3faf"
VERSION = "1.1.0"
TASK_ID = "4a46459a3faf"
SUMMARY = "8-bg grid with single non-8 color; rule centers count-length bar."

INVARIANTS = [
    "background is 8 (rule's bg)",
    ">=2 cells of single non-8 color (count = bar length)",
    "count <= w (bar fits horizontally)",
    "exactly one non-8 color in input (rule's find-first picks unambiguously)",
]

CELL_LAYOUTS = ("scattered", "blob", "diagonal", "row", "col",
                "checker", "frame", "corners")
DEGENERATE_TEXTURES = ("no_color", "full_color", "count_too_large")
HELPFUL_TEXTURES = CELL_LAYOUTS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 6..12", "valid": "5..16"},
    "grid_w":         {"type": "int", "default": "rng 11..18", "valid": "9..22"},
    "color":          {"type": "color", "default": "rng (≠8)", "valid": "1..9 (≠8)"},
    "count":          {"type": "int", "default": "rng 2..w-2", "valid": "1..w"},
    "cell_layout":    {"type": "str", "default": "rng helpful",
                       "valid": "|".join(CELL_LAYOUTS)},
    "position_bias":  {"type": "str", "default": "rng spread|center|edge",
                       "valid": "spread|center|edge"},
    "palette_size":   {"type": "int", "default": "1", "valid": "1..1"},
    "asymmetry":      {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "texture":        {"type": "str", "default": "alias for cell_layout",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if difficulty == "easy":
        h_lo, h_hi, w_lo, w_hi = 5, 7, 9, 12
    elif difficulty == "hard":
        h_lo, h_hi, w_lo, w_hi = 11, 16, 16, 22
    else:
        h_lo, h_hi, w_lo, w_hi = 6, 12, 11, 18
    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", w_lo, w_hi)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], h, w, rng)
    color = int(overrides.get("color",
                              rng.choice([1, 2, 3, 4, 5, 6, 7, 9])))
    max_count = w - 1
    count = int(overrides.get("count",
                              ctx.draw_int("count", 2, max(2, max_count))))
    count = max(2, min(max_count, count))
    layout = (overrides.get("texture") or overrides.get("cell_layout")
              or ctx.draw_choice("cell_layout", list(CELL_LAYOUTS)))
    bias = overrides.get("position_bias",
                         ctx.draw_choice("position_bias",
                                         ["spread", "center", "edge"]))
    g = full_grid(h, w, 8)
    cells = _layout_cells(layout, h, w, bias, rng)
    for r, c in cells[:count]:
        g[r][c] = color
    return g


def _layout_cells(layout, h, w, bias, rng):
    cells = [(r, c) for r in range(h) for c in range(w)]
    if layout == "blob":
        cr, cc = rng.randint(0, h - 1), rng.randint(0, w - 1)
        cells.sort(key=lambda rc: abs(rc[0] - cr) + abs(rc[1] - cc))
        return cells
    if layout == "diagonal":
        diag = [(k, k) for k in range(min(h, w))]
        rest = [c for c in cells if c not in diag]
        rng.shuffle(rest)
        return diag + rest
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
    if layout == "checker":
        even = [(r, c) for (r, c) in cells if (r + c) % 2 == 0]
        odd = [(r, c) for (r, c) in cells if (r + c) % 2 != 0]
        rng.shuffle(even); rng.shuffle(odd)
        return even + odd
    if layout == "frame":
        border = [(r, c) for (r, c) in cells
                  if r in (0, h - 1) or c in (0, w - 1)]
        interior = [(r, c) for (r, c) in cells if (r, c) not in border]
        rng.shuffle(border); rng.shuffle(interior)
        return border + interior
    rng.shuffle(cells)
    return cells


def _draw_from_degenerate(name, h, w, rng):
    g = full_grid(h, w, 8)
    color = rng.choice([1, 2, 3, 4, 5, 6, 7, 9])
    if name == "no_color":
        return g
    if name == "full_color":
        for r in range(h):
            for c in range(w):
                g[r][c] = color
        return g
    if name == "count_too_large":
        # count > w-2 (bar would overflow)
        for c in range(w):
            g[0][c] = color
        return g
    return g
