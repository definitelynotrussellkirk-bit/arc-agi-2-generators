"""Generator for ARC task d4469b4b.

Rule: input grid; mode (most common) value selects a 3×3 fixed pattern:
1 → plus, 2 → T-down, 3 → corner-L, else all 0.

Combinatorial axes (8): mode_color, grid_h/w, mode_count, other_color,
other_count, cell_layout, palette_size, decoy_density.
Degenerates: monochrome, all_zero, no_clear_mode.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "49754d8fa42e"
VERSION = "1.1.0"
TASK_ID = "49754d8fa42e"
SUMMARY = "Grid with foreground mode in {1,2,3}; rule emits a fixed 3×3 pattern by mode."

INVARIANTS = [
    "foreground mode is one of {1, 2, 3}",
    "mode color count is STRICTLY higher than any other non-bg color count",
    ">=2 distinct colors total (so mode is well-defined)",
    "background may be 0 or another non-mode color (rule uses (mode g 0))",
]

CELL_LAYOUTS = ("scattered", "blob", "diagonal", "row_dominant",
                "col_dominant", "checker", "frame")
DEGENERATE_TEXTURES = ("monochrome", "all_zero", "no_clear_mode")
HELPFUL_TEXTURES = CELL_LAYOUTS

AXES = {
    "mode_color":     {"type": "choice", "default": "rng 1|2|3",
                       "valid": "1|2|3"},
    "grid_h":         {"type": "int", "default": "rng 4..7", "valid": "3..10"},
    "grid_w":         {"type": "int", "default": "rng 4..7", "valid": "3..10"},
    "mode_count":     {"type": "int", "default": "rng h*w/3..h*w/2",
                       "valid": "3..h*w-1"},
    "other_color":    {"type": "color", "default": "rng (≠0,mode)",
                       "valid": "1..9"},
    "cell_layout":    {"type": "str", "default": "rng helpful",
                       "valid": "|".join(CELL_LAYOUTS)},
    "palette_size":   {"type": "int", "default": "rng 2..3", "valid": "2..6"},
    "decoy_density":  {"type": "float", "default": "0", "valid": "0..0.05"},
    "texture":        {"type": "str", "default": "alias for cell_layout",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index, version=VERSION,
                  task_id=TASK_ID, difficulty=difficulty, overrides=overrides)
    if difficulty == "easy":
        h_lo, h_hi = 3, 5
    elif difficulty == "hard":
        h_lo, h_hi = 7, 10
    else:
        h_lo, h_hi = 4, 7
    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", h_lo, h_hi)
    rng = ctx.draw_rng("cells")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], h, w, rng)
    color = int(overrides.get("mode_color",
                              ctx.draw_choice("mode_color", [1, 2, 3])))
    n_palette = int(overrides.get("palette_size",
                                  ctx.draw_int("palette_size", 2, 3)))
    other_pool = [c for c in range(1, 10) if c not in (0, color)]
    rng.shuffle(other_pool)
    others = other_pool[:max(1, n_palette - 1)]
    layout = (overrides.get("texture") or overrides.get("cell_layout")
              or ctx.draw_choice("cell_layout", list(CELL_LAYOUTS)))
    total = h * w
    mode_count = int(overrides.get("mode_count",
                                   ctx.draw_int("mode_count",
                                                max(2, total // 3),
                                                max(3, total // 2))))
    mode_count = max(2, min(total - 2, mode_count))
    g = full_grid(h, w, 0)
    cells = _layout_cells(layout, h, w, rng)
    for r, c in cells[:mode_count]:
        g[r][c] = color
    other_total = max(1, mode_count - 2)
    other_per = max(1, other_total // max(1, len(others)))
    idx = mode_count
    for other in others:
        for _ in range(min(other_per, other_total)):
            if idx >= len(cells):
                break
            r, c = cells[idx]
            g[r][c] = other
            idx += 1
            other_total -= 1
    counts = {}
    for r in range(h):
        for c in range(w):
            counts[g[r][c]] = counts.get(g[r][c], 0) + 1
    sorted_counts = sorted(counts.items(), key=lambda kv: -kv[1])
    if not sorted_counts or sorted_counts[0][0] != color or \
            (len(sorted_counts) > 1 and sorted_counts[0][1] <= sorted_counts[1][1]):
        for r in range(h):
            for c in range(w):
                if g[r][c] != 0 and g[r][c] != color and rng.random() < 0.3:
                    g[r][c] = color
    return g


def _layout_cells(layout, h, w, rng):
    cells = [(r, c) for r in range(h) for c in range(w)]
    if layout == "blob":
        cr, cc = rng.randint(0, h - 1), rng.randint(0, w - 1)
        cells.sort(key=lambda rc: abs(rc[0] - cr) + abs(rc[1] - cc))
        return cells
    if layout == "diagonal":
        diag_cells = [(k, k) for k in range(min(h, w))]
        rest = [c for c in cells if c not in diag_cells]
        rng.shuffle(rest)
        return diag_cells + rest
    if layout == "row_dominant":
        r = rng.randint(0, h - 1)
        chosen = [(r, c) for c in range(w)]
        rest = [c for c in cells if c not in chosen]
        rng.shuffle(rest)
        return chosen + rest
    if layout == "col_dominant":
        c = rng.randint(0, w - 1)
        chosen = [(r, c) for r in range(h)]
        rest = [cc for cc in cells if cc not in chosen]
        rng.shuffle(rest)
        return chosen + rest
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
    g = full_grid(h, w, 0)
    if name == "monochrome":
        c = rng.choice([1, 2, 3])
        return [[c] * w for _ in range(h)]
    if name == "all_zero":
        return g
    if name == "no_clear_mode":
        c1 = rng.choice([1, 2, 3])
        c2 = rng.choice([cc for cc in (1, 2, 3) if cc != c1])
        for r in range(h):
            for c in range(w):
                g[r][c] = c1 if (r + c) % 2 == 0 else c2
        return g
    return g
