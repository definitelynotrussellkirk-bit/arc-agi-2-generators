"""Generator for ARC task 017c7c7b.

Rule: row-periodic grid. Extend height by floor(h/2). For each cell,
if its row-mod-period value is 1, replace with 2.

Combinatorial axes (8): grid_h/w, period, palette_size,
row_pattern_kind, fg_density, anchor_one_count, palette_kind,
asymmetry_force.
Degenerates: no_period, no_ones, single_row.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "d07c7972d183"
VERSION = "1.1.0"
TASK_ID = "d07c7972d183"
SUMMARY = "Row-periodic grid; rule extends height by half + recolors 1s to 2."

INVARIANTS = [
    "rows repeat with period in [1, 4]",
    "color 1 appears in >=1 cell of the period block",
    "extended height (h + h/2) <= 30",
    "no color 2 in input (rule writes 2 for output)",
]

ROW_PATTERNS = ("noise", "blocks", "diag_progression", "alternating",
                "stripe", "uniform")
PALETTE_KINDS = ("warm", "cool", "broad", "small")
DEGENERATE_TEXTURES = ("no_period", "no_ones", "single_row")
HELPFUL_TEXTURES = ROW_PATTERNS

AXES = {
    "grid_h":           {"type": "int", "default": "rng 4..14", "valid": "2..18"},
    "grid_w":           {"type": "int", "default": "rng 3..12", "valid": "1..18"},
    "period":           {"type": "int", "default": "rng 1..4", "valid": "1..6"},
    "palette_size":     {"type": "int", "default": "rng 2..5", "valid": "1..7"},
    "row_pattern_kind": {"type": "str", "default": "rng helpful",
                         "valid": "|".join(ROW_PATTERNS)},
    "fg_density":       {"type": "float", "default": "rng 0.3..0.7",
                         "valid": "0.1..1"},
    "palette_kind":     {"type": "str", "default": "rng helpful",
                         "valid": "|".join(PALETTE_KINDS)},
    "anchor_one_count": {"type": "int", "default": "rng 1..3",
                         "valid": "1..5"},
    "texture":          {"type": "str", "default": "alias for row_pattern_kind",
                         "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index, version=VERSION,
                  task_id=TASK_ID, difficulty=difficulty, overrides=overrides)
    if difficulty == "easy":
        h_lo, h_hi, w_lo, w_hi = 2, 5, 2, 5
    elif difficulty == "hard":
        h_lo, h_hi, w_lo, w_hi = 12, 18, 9, 15
    else:
        h_lo, h_hi, w_lo, w_hi = 4, 14, 3, 12
    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", w_lo, w_hi)
    rng = ctx.draw_rng("rows")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], h, w, rng)
    period = int(overrides.get("period",
                               ctx.draw_int("period", 1, min(4, h))))
    period = max(1, min(h, period))
    palette_kind = overrides.get("palette_kind",
                                 ctx.draw_choice("palette_kind",
                                                 list(PALETTE_KINDS)))
    if palette_kind == "warm":
        pool = [3, 4, 6, 9]
    elif palette_kind == "cool":
        pool = [5, 7, 8]
    elif palette_kind == "small":
        pool = [3, 4]
    else:
        pool = [3, 4, 5, 6, 7, 8, 9]
    rng.shuffle(pool)
    n_palette = int(overrides.get("palette_size",
                                  ctx.draw_int("palette_size", 2, 5)))
    palette = [1] + pool[:max(1, n_palette - 1)]
    pattern = (overrides.get("texture") or overrides.get("row_pattern_kind")
               or ctx.draw_choice("row_pattern_kind", list(ROW_PATTERNS)))
    fg_density = float(overrides.get("fg_density",
                                     ctx.draw_rng("fg_density")
                                     .uniform(0.3, 0.7)))
    anchor_count = int(overrides.get("anchor_one_count",
                                     ctx.draw_int("anchor_one_count", 1, 3)))
    base_rows = _build_base_rows(pattern, period, w, palette, fg_density, rng)
    n_ones = sum(1 for r in range(period) for v in base_rows[r] if v == 1)
    if n_ones < anchor_count:
        for _ in range(anchor_count - n_ones):
            r = rng.randint(0, period - 1)
            c = rng.randint(0, w - 1)
            base_rows[r][c] = 1
    g = full_grid(h, w, 0)
    for r in range(h):
        g[r] = list(base_rows[r % period])
    return g


def _build_base_rows(pattern, period, w, palette, density, rng):
    rows = [[] for _ in range(period)]
    if pattern == "uniform":
        for r in range(period):
            color = rng.choice(palette)
            rows[r] = [color] * w
        return rows
    if pattern == "stripe":
        for r in range(period):
            color = palette[r % len(palette)]
            rows[r] = [color] * w
        return rows
    if pattern == "blocks":
        for r in range(period):
            row = []
            block_size = max(1, w // 3)
            color_idx = 0
            for i in range(w):
                if i % block_size == 0:
                    color_idx = (color_idx + 1) % len(palette)
                row.append(palette[color_idx])
            rows[r] = row
        return rows
    if pattern == "diag_progression":
        for r in range(period):
            row = []
            for c in range(w):
                row.append(palette[(r + c) % len(palette)])
            rows[r] = row
        return rows
    if pattern == "alternating":
        for r in range(period):
            row = []
            for c in range(w):
                if c % 2 == 0:
                    row.append(palette[r % len(palette)])
                else:
                    row.append(palette[(r + 1) % len(palette)])
            rows[r] = row
        return rows
    for r in range(period):
        rows[r] = [rng.choice(palette) for _ in range(w)]
    return rows


def _draw_from_degenerate(name, h, w, rng):
    if name == "no_period":
        g = full_grid(h, w, 0)
        for r in range(h):
            for c in range(w):
                g[r][c] = rng.choice([1, 3, 4, 5, 6, 7, 8, 9])
        return g
    if name == "no_ones":
        g = full_grid(h, w, 0)
        for r in range(h):
            for c in range(w):
                g[r][c] = rng.choice([3, 4, 5, 6, 7, 8, 9])
        return g
    if name == "single_row":
        if h <= 1:
            return [[1] + [rng.choice([3, 4, 5, 6])
                           for _ in range(w - 1)]]
        g = full_grid(h, w, 0)
        row = [rng.choice([1, 3, 4, 5, 6]) for _ in range(w)]
        for r in range(h):
            g[r] = list(row)
        return g
    return [[1] * w for _ in range(h)]
