"""Generator for puzzle 9110e3c5.

Rule: dominant (mode) color in {1, 2, 3} selects one of three 3×3
shapes (S, plus, L). Output is the chosen shape.

Combinatorial axes (8): grid_h/w, dom_color, dom_count_ratio,
other_palette_size, cell_layout, position_bias, anchor_corner,
asymmetry.
Degenerates: monochrome, equal_counts, no_dominant.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "ff3bd1942373"
VERSION = "1.1.0"
TASK_ID = "ff3bd1942373"
SUMMARY = "Grid where mode is in {1,2,3}; rule outputs a fixed 3×3 shape per mode."

INVARIANTS = [
    "the mode color is in {1, 2, 3}",
    "the mode color appears STRICTLY more often than any other",
    ">=1 non-mode cell exists",
]

CELL_LAYOUTS = ("scattered", "blob", "diagonal", "row_dominant",
                "col_dominant", "checker", "frame")
DEGENERATE_TEXTURES = ("monochrome", "equal_counts", "no_dominant")
HELPFUL_TEXTURES = CELL_LAYOUTS

AXES = {
    "grid_h":             {"type": "int", "default": "rng 5..12", "valid": "3..16"},
    "grid_w":             {"type": "int", "default": "rng 5..12", "valid": "3..16"},
    "dom_color":          {"type": "int", "default": "rng 1..3", "valid": "1..3"},
    "dom_count_ratio":    {"type": "float", "default": "rng 0.6..0.8",
                           "valid": "0.5..0.95"},
    "other_palette_size": {"type": "int", "default": "rng 1..4",
                           "valid": "1..7"},
    "cell_layout":        {"type": "str", "default": "rng helpful",
                           "valid": "|".join(CELL_LAYOUTS)},
    "position_bias":      {"type": "str", "default": "rng spread|center|edge",
                           "valid": "spread|center|edge"},
    "anchor_corner":      {"type": "bool", "default": "false",
                           "valid": "true|false"},
    "texture":            {"type": "str", "default": "alias for cell_layout",
                           "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if difficulty == "easy":
        h_lo, h_hi = 3, 5
    elif difficulty == "hard":
        h_lo, h_hi = 10, 16
    else:
        h_lo, h_hi = 5, 12
    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", h_lo, h_hi)
    rng = ctx.draw_rng("placement")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], h, w, rng)
    dom_color = int(overrides.get("dom_color",
                                  ctx.draw_int("dom_color", 1, 3)))
    dom_color = max(1, min(3, dom_color))
    n_other = int(overrides.get("other_palette_size",
                                ctx.draw_int("other_palette_size", 1, 4)))
    other_pool = [c for c in range(10) if c != dom_color]
    rng.shuffle(other_pool)
    other_palette = other_pool[:max(1, n_other)]
    layout = (overrides.get("texture") or overrides.get("cell_layout")
              or ctx.draw_choice("cell_layout", list(CELL_LAYOUTS)))
    bias = overrides.get("position_bias",
                         ctx.draw_choice("position_bias",
                                         ["spread", "center", "edge"]))
    dom_ratio = float(overrides.get("dom_count_ratio",
                                    ctx.draw_rng("dom_count_ratio")
                                    .uniform(0.6, 0.8)))
    g = full_grid(h, w, dom_color)
    total = h * w
    n_other_total = max(1, total - int(total * dom_ratio))
    positions = _layout_positions(layout, h, w, bias, rng)
    for r, c in positions[:n_other_total]:
        g[r][c] = rng.choice(other_palette)
    if bool(overrides.get("anchor_corner", False)):
        g[0][0] = dom_color
    counts = {}
    for r in range(h):
        for c in range(w):
            counts[g[r][c]] = counts.get(g[r][c], 0) + 1
    sorted_counts = sorted(counts.items(), key=lambda kv: -kv[1])
    if not sorted_counts or sorted_counts[0][0] != dom_color or \
            (len(sorted_counts) > 1 and
             sorted_counts[0][1] <= sorted_counts[1][1]):
        for r in range(h):
            for c in range(w):
                if g[r][c] != dom_color and rng.random() < 0.3:
                    g[r][c] = dom_color
    return g


def _layout_positions(layout, h, w, bias, rng):
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
    if layout == "row_dominant":
        chosen_rows = rng.sample(range(h), min(2, h))
        first = [(r, c) for r in chosen_rows for c in range(w)]
        rest = [c for c in cells if c not in first]
        rng.shuffle(rest)
        return first + rest
    if layout == "col_dominant":
        chosen_cols = rng.sample(range(w), min(2, w))
        first = [(r, c) for r in range(h) for c in chosen_cols]
        rest = [c for c in cells if c not in first]
        rng.shuffle(rest)
        return first + rest
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
    if bias == "center":
        cr, cc = h // 2, w // 2
        cells.sort(key=lambda rc: abs(rc[0] - cr) + abs(rc[1] - cc))
        return cells
    if bias == "edge":
        cells.sort(key=lambda rc: -min(rc[0], h - 1 - rc[0], rc[1], w - 1 - rc[1]))
        return cells
    rng.shuffle(cells)
    return cells


def _draw_from_degenerate(name, h, w, rng):
    if name == "monochrome":
        c = rng.choice([1, 2, 3])
        return [[c] * w for _ in range(h)]
    if name == "equal_counts":
        c1, c2 = rng.sample([1, 2, 3], 2)
        g = full_grid(h, w, c1)
        for r in range(h):
            for c in range(w):
                g[r][c] = c1 if (r + c) % 2 == 0 else c2
        return g
    if name == "no_dominant":
        # Spread mode in {1..3} thinly
        g = full_grid(h, w, 1)
        for r in range(h):
            for c in range(w):
                g[r][c] = 1 + ((r + c) % 9)
        return g
    return [[1] * w for _ in range(h)]
