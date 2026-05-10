"""Generator for puzzle f8ff0b80.

Rule: 3 distinct non-bg colors; output is 3×1 column sorted by
cell-count descending.

Combinatorial axes (8): grid_h/w, palette_kind, count_distribution,
position_layout, position_bias, decoy_density, n_colors,
min_count_gap.
Degenerates: monochrome, two_colors, equal_counts.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "3233860e2d81"
VERSION = "1.1.0"
TASK_ID = "3233860e2d81"
SUMMARY = "Grid with 3 distinct non-bg colors; rule outputs 3×1 sorted by count desc."

INVARIANTS = [
    "background is 0",
    "exactly 3 distinct non-bg colors",
    "the 3 colors have STRICTLY distinct counts (so sort is unambiguous)",
    "min count >= 2 (so each color is non-trivially present)",
]

POSITION_LAYOUTS = ("scattered", "blob", "row_dominant",
                    "col_dominant", "diag", "checker")
COUNT_DISTRIBUTIONS = ("ascending", "wide_spread", "tight_spread")
DEGENERATE_TEXTURES = ("monochrome", "two_colors", "equal_counts")
HELPFUL_TEXTURES = POSITION_LAYOUTS

AXES = {
    "grid_h":            {"type": "int", "default": "rng 7..14", "valid": "5..18"},
    "grid_w":            {"type": "int", "default": "rng 7..14", "valid": "5..18"},
    "palette_kind":      {"type": "str", "default": "rng warm|cool|broad",
                          "valid": "warm|cool|broad"},
    "count_distribution": {"type": "str", "default": "rng helpful",
                           "valid": "|".join(COUNT_DISTRIBUTIONS)},
    "position_layout":   {"type": "str", "default": "rng helpful",
                          "valid": "|".join(POSITION_LAYOUTS)},
    "position_bias":     {"type": "str", "default": "rng spread|center|edge",
                          "valid": "spread|center|edge"},
    "min_count_gap":     {"type": "int", "default": "1", "valid": "1..3"},
    "min_count":         {"type": "int", "default": "2", "valid": "1..5"},
    "texture":           {"type": "str", "default": "alias for position_layout",
                          "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if difficulty == "easy":
        h_lo, h_hi = 5, 8
    elif difficulty == "hard":
        h_lo, h_hi = 12, 18
    else:
        h_lo, h_hi = 7, 14
    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", h_lo, h_hi)
    rng = ctx.draw_rng("placement")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], h, w, rng)
    palette_kind = overrides.get("palette_kind",
                                 ctx.draw_choice("palette_kind",
                                                 ["warm", "cool", "broad"]))
    if palette_kind == "warm":
        pool = [3, 4, 6, 9]
    elif palette_kind == "cool":
        pool = [1, 5, 7, 8]
    else:
        pool = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    rng.shuffle(pool)
    palette = pool[:3]
    if len(palette) < 3:
        extras = [c for c in range(1, 10) if c not in palette]
        rng.shuffle(extras)
        palette += extras[:3 - len(palette)]
    palette = palette[:3]
    dist = overrides.get("count_distribution",
                         ctx.draw_choice("count_distribution",
                                         list(COUNT_DISTRIBUTIONS)))
    layout = (overrides.get("texture") or overrides.get("position_layout")
              or ctx.draw_choice("position_layout",
                                 list(POSITION_LAYOUTS)))
    min_count = int(overrides.get("min_count", 2))
    gap = int(overrides.get("min_count_gap", 1))
    counts = _draw_counts(dist, min_count, gap, h * w, rng)
    counts = sorted(counts)
    g = full_grid(h, w, 0)
    cells = _layout_positions(layout, h, w, rng)
    idx = 0
    for color, n in zip(palette, counts):
        for _ in range(n):
            if idx >= len(cells):
                break
            r, c = cells[idx]
            idx += 1
            g[r][c] = color
    return g


def _draw_counts(dist, min_count, gap, total, rng):
    if dist == "ascending":
        return [min_count, min_count + gap, min_count + 2 * gap]
    if dist == "tight_spread":
        return [min_count, min_count + 1, min_count + 2]
    return [min_count, min_count + max(2, gap),
            min_count + max(4, 2 * gap)]


def _layout_positions(layout, h, w, rng):
    cells = [(r, c) for r in range(h) for c in range(w)]
    if layout == "blob":
        cr, cc = rng.randint(0, h - 1), rng.randint(0, w - 1)
        cells.sort(key=lambda rc: abs(rc[0] - cr) + abs(rc[1] - cc))
        return cells
    if layout == "row_dominant":
        chosen_rows = rng.sample(range(h), min(3, h))
        first = [(r, c) for r in chosen_rows for c in range(w)]
        rest = [c for c in cells if c not in first]
        rng.shuffle(rest)
        return first + rest
    if layout == "col_dominant":
        chosen_cols = rng.sample(range(w), min(3, w))
        first = [(r, c) for r in range(h) for c in chosen_cols]
        rest = [c for c in cells if c not in first]
        rng.shuffle(rest)
        return first + rest
    if layout == "diag":
        diag = [(k, k) for k in range(min(h, w))]
        rest = [c for c in cells if c not in diag]
        rng.shuffle(rest)
        return diag + rest
    if layout == "checker":
        even = [(r, c) for (r, c) in cells if (r + c) % 2 == 0]
        odd = [(r, c) for (r, c) in cells if (r + c) % 2 != 0]
        rng.shuffle(even); rng.shuffle(odd)
        return even + odd
    rng.shuffle(cells)
    return cells


def _draw_from_degenerate(name, h, w, rng):
    g = full_grid(h, w, 0)
    pool = list(range(1, 10))
    rng.shuffle(pool)
    if name == "monochrome":
        c = pool[0]
        for r in range(h):
            for cc in range(w):
                if rng.random() < 0.4:
                    g[r][cc] = c
        return g
    if name == "two_colors":
        c1, c2 = pool[0], pool[1]
        cells = [(r, c) for r in range(h) for c in range(w)]
        rng.shuffle(cells)
        for r, c in cells[:5]:
            g[r][c] = c1
        for r, c in cells[5:10]:
            g[r][c] = c2
        return g
    if name == "equal_counts":
        c1, c2, c3 = pool[0], pool[1], pool[2]
        cells = [(r, c) for r in range(h) for c in range(w)]
        rng.shuffle(cells)
        for r, c in cells[:4]:
            g[r][c] = c1
        for r, c in cells[4:8]:
            g[r][c] = c2
        for r, c in cells[8:12]:
            g[r][c] = c3
        return g
    return g
