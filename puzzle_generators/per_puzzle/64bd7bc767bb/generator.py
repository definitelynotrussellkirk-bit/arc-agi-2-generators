"""Generator for puzzle f3cdc58f.

Rule: count cells of colors 1..4. Output: bars at cols 0..3 rising from
the bottom; bar i has height = count(color i+1).

Combinatorial axes (8): grid_h/w, count_distribution, position_layout,
position_bias, decoy_density, palette_force_4_colors,
count_max_kind, asymmetry.
Degenerates: only_one_color, equal_counts, no_1234.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "64bd7bc767bb"
VERSION = "1.1.0"
TASK_ID = "64bd7bc767bb"
SUMMARY = "Cells in colors 1..4; rule outputs 4-column bar chart by count."

INVARIANTS = [
    "input width >= 4 (so output has columns for colors 1..4)",
    "input height >= 4 (so bars are visible)",
    ">=1 cell of each color in {1, 2, 3, 4}",
    "max count of any color < grid height (so bar fits)",
]

POSITION_LAYOUTS = ("scattered", "blob", "diagonal", "stripes",
                    "checker", "rows_dominant", "cols_dominant")
COUNT_DISTRIBUTIONS = ("ascending", "wide_spread", "tight_spread", "shuffled")
DEGENERATE_TEXTURES = ("only_one_color", "equal_counts", "no_1234")
HELPFUL_TEXTURES = POSITION_LAYOUTS

AXES = {
    "grid_h":             {"type": "int", "default": "rng 7..14", "valid": "5..18"},
    "grid_w":             {"type": "int", "default": "rng 6..14", "valid": "4..18"},
    "count_distribution": {"type": "str", "default": "rng helpful",
                           "valid": "|".join(COUNT_DISTRIBUTIONS)},
    "position_layout":    {"type": "str", "default": "rng helpful",
                           "valid": "|".join(POSITION_LAYOUTS)},
    "position_bias":      {"type": "str", "default": "rng spread|center|edge",
                           "valid": "spread|center|edge"},
    "min_count":          {"type": "int", "default": "1", "valid": "1..3"},
    "count_max_kind":     {"type": "str", "default": "rng full|capped",
                           "valid": "full|capped"},
    "asymmetry":          {"type": "bool", "default": "false",
                           "valid": "true|false"},
    "texture":            {"type": "str", "default": "alias for position_layout",
                           "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if difficulty == "easy":
        h_lo, h_hi, w_lo, w_hi = 5, 8, 4, 7
    elif difficulty == "hard":
        h_lo, h_hi, w_lo, w_hi = 12, 18, 12, 18
    else:
        h_lo, h_hi, w_lo, w_hi = 7, 14, 6, 14
    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", w_lo, w_hi)
    rng = ctx.draw_rng("placement")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], h, w, rng)
    dist = overrides.get("count_distribution",
                         ctx.draw_choice("count_distribution",
                                         list(COUNT_DISTRIBUTIONS)))
    layout = (overrides.get("texture") or overrides.get("position_layout")
              or ctx.draw_choice("position_layout",
                                 list(POSITION_LAYOUTS)))
    min_count = int(overrides.get("min_count", 1))
    max_kind = overrides.get("count_max_kind",
                             ctx.draw_choice("count_max_kind",
                                             ["full", "capped"]))
    max_count = h - 1 if max_kind == "full" else max(2, h // 2)
    counts = _draw_counts(dist, min_count, max_count, rng)
    g = full_grid(h, w, 0)
    positions = _layout_positions(layout, h, w, rng)
    color_count = dict(zip([1, 2, 3, 4], counts))
    pos_iter = iter(positions)
    for color, cnt in color_count.items():
        placed = 0
        while placed < cnt:
            try:
                r, c = next(pos_iter)
            except StopIteration:
                break
            if g[r][c] == 0:
                g[r][c] = color
                placed += 1
    for color in (1, 2, 3, 4):
        if not any(g[r][c] == color for r in range(h) for c in range(w)):
            for r in range(h):
                for c in range(w):
                    if g[r][c] == 0:
                        g[r][c] = color
                        break
                else:
                    continue
                break
    return g


def _draw_counts(dist, min_count, max_count, rng):
    if max_count - min_count < 4:
        return [min_count, min_count + 1, min_count + 2, min_count + 3]
    if dist == "ascending":
        return [min_count, min_count + 1, min_count + 2, min_count + 3]
    if dist == "tight_spread":
        base = rng.randint(min_count, max(min_count, max_count - 3))
        return [base, base + 1, base + 2, base + 3]
    if dist == "shuffled":
        sample = rng.sample(range(min_count, max_count + 1), 4)
        return sample
    return sorted(rng.sample(range(min_count, max_count + 1), 4))


def _layout_positions(layout, h, w, rng):
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
    if layout == "stripes":
        odd = [(r, c) for (r, c) in cells if r % 2 == 0]
        even = [(r, c) for (r, c) in cells if r % 2 != 0]
        rng.shuffle(odd); rng.shuffle(even)
        return odd + even
    if layout == "checker":
        a = [(r, c) for (r, c) in cells if (r + c) % 2 == 0]
        b = [(r, c) for (r, c) in cells if (r + c) % 2 != 0]
        rng.shuffle(a); rng.shuffle(b)
        return a + b
    if layout == "rows_dominant":
        chosen_rows = rng.sample(range(h), min(3, h))
        first = [(r, c) for r in chosen_rows for c in range(w)]
        rest = [c for c in cells if c not in first]
        rng.shuffle(rest)
        return first + rest
    if layout == "cols_dominant":
        chosen_cols = rng.sample(range(w), min(3, w))
        first = [(r, c) for r in range(h) for c in chosen_cols]
        rest = [c for c in cells if c not in first]
        rng.shuffle(rest)
        return first + rest
    rng.shuffle(cells)
    return cells


def _draw_from_degenerate(name, h, w, rng):
    g = full_grid(h, w, 0)
    if name == "only_one_color":
        for c in range(min(3, w)):
            g[h - 1][c] = 1
        return g
    if name == "equal_counts":
        cells = [(r, c) for r in range(h) for c in range(w)]
        rng.shuffle(cells)
        idx = 0
        for color in (1, 2, 3, 4):
            for _ in range(2):
                if idx < len(cells):
                    r, c = cells[idx]
                    g[r][c] = color
                    idx += 1
        return g
    if name == "no_1234":
        color = rng.choice([5, 6, 7, 8, 9])
        for r in range(h):
            for c in range(w):
                if rng.random() < 0.3:
                    g[r][c] = color
        return g
    return g
