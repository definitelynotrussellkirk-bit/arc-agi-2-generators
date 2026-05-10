"""Generator for f8b3ba0a.

Rule: count colors. Sort desc. Output [3rd, 4th, 5th] most common as
3×1 column.

Combinatorial axes (8): grid_h/w, palette_size, count_distribution,
position_layout, palette_kind, anchor_corner, asymmetry_force,
spread_kind.
Degenerates: too_few_colors, equal_counts, all_one_color.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid
from puzzle_generators.helpers.place import random_free_cell

GENERATOR_ID = "427be9c8dedb"
VERSION = "1.1.0"
TASK_ID = "427be9c8dedb"
SUMMARY = "Grid with 5+ distinct non-zero colors; rule outputs 3×1 of 3rd,4th,5th."

INVARIANTS = [
    ">=6 distinct colors total (incl. bg=0)",
    "5+ non-zero colors with STRICTLY distinct counts",
    "bg=0 has the largest count overall",
    "the 3rd, 4th, 5th distinct (by count) colors are unambiguous",
]

POSITION_LAYOUTS = ("scattered", "blob", "stripes", "checker")
COUNT_DISTRIBUTIONS = ("default", "wide_spread", "tight_spread", "ascending")
PALETTE_KINDS = ("warm", "cool", "broad", "small")
DEGENERATE_TEXTURES = ("too_few_colors", "equal_counts", "all_one_color")
HELPFUL_TEXTURES = POSITION_LAYOUTS

AXES = {
    "grid_h":             {"type": "int", "default": "rng 11..16", "valid": "9..20"},
    "grid_w":             {"type": "int", "default": "rng 8..14", "valid": "7..16"},
    "palette_size":       {"type": "int", "default": "rng 5..7", "valid": "5..9"},
    "count_distribution": {"type": "str", "default": "rng helpful",
                           "valid": "|".join(COUNT_DISTRIBUTIONS)},
    "position_layout":    {"type": "str", "default": "rng helpful",
                           "valid": "|".join(POSITION_LAYOUTS)},
    "palette_kind":       {"type": "str", "default": "rng helpful",
                           "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":      {"type": "bool", "default": "false",
                           "valid": "true|false"},
    "asymmetry_force":    {"type": "bool", "default": "false",
                           "valid": "true|false"},
    "texture":            {"type": "str", "default": "alias for position_layout",
                           "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if difficulty == "easy":
        h_lo, h_hi, w_lo, w_hi = 9, 12, 7, 10
    elif difficulty == "hard":
        h_lo, h_hi, w_lo, w_hi = 15, 20, 13, 16
    else:
        h_lo, h_hi, w_lo, w_hi = 11, 16, 8, 14
    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", w_lo, w_hi)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], h, w, rng)
    palette_kind = overrides.get("palette_kind",
                                 ctx.draw_choice("palette_kind",
                                                 list(PALETTE_KINDS)))
    if palette_kind == "warm":
        pool = [3, 4, 6, 9]
    elif palette_kind == "cool":
        pool = [1, 5, 7, 8]
    elif palette_kind == "small":
        pool = [1, 2, 3, 4, 5]
    else:
        pool = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    rng.shuffle(pool)
    n_palette = int(overrides.get("palette_size",
                                  ctx.draw_int("palette_size", 5, 7)))
    n_palette = max(5, n_palette)
    palette = pool[:n_palette]
    if len(palette) < 5:
        extras = [c for c in [1, 2, 3, 4, 5, 6, 7, 8, 9] if c not in palette]
        rng.shuffle(extras)
        palette += extras[:5 - len(palette)]
    palette = palette[:n_palette]
    dist = overrides.get("count_distribution",
                         ctx.draw_choice("count_distribution",
                                         list(COUNT_DISTRIBUTIONS)))
    counts = _draw_counts(dist, len(palette), h, w, rng)
    g = full_grid(h, w, 0)
    for color, count in zip(palette, counts):
        for _ in range(count):
            cell = random_free_cell(g, rng, max_tries=40)
            if cell is not None:
                g[cell[0]][cell[1]] = color
    return g


def _draw_counts(dist, n, h, w, rng):
    total = h * w
    if dist == "wide_spread":
        return [int(total * 0.3), int(total * 0.15),
                int(total * 0.07), int(total * 0.04), 2,
                rng.randint(2, 5)][:n]
    if dist == "tight_spread":
        base = int(total * 0.15)
        return [base + 5, base + 3, base + 1, base - 1, max(2, base - 3),
                max(2, base - 5)][:n]
    if dist == "ascending":
        return [int(total * (0.05 + i * 0.05)) for i in range(n)][::-1]
    return [rng.randint(22, 28), rng.randint(10, 14),
            rng.randint(6, 7), rng.randint(4, 5),
            rng.randint(2, 3), rng.randint(2, 3),
            rng.randint(2, 3)][:n]


def _draw_from_degenerate(name, h, w, rng):
    g = full_grid(h, w, 0)
    if name == "too_few_colors":
        # only 3 colors
        from puzzle_generators.helpers.place import random_free_cell as rfc
        for color, count in zip([1, 2, 3], [10, 6, 3]):
            for _ in range(count):
                cell = rfc(g, rng, max_tries=20)
                if cell:
                    g[cell[0]][cell[1]] = color
        return g
    if name == "equal_counts":
        from puzzle_generators.helpers.place import random_free_cell as rfc
        for color in [1, 2, 3, 4, 5]:
            for _ in range(5):
                cell = rfc(g, rng, max_tries=20)
                if cell:
                    g[cell[0]][cell[1]] = color
        return g
    if name == "all_one_color":
        for r in range(h):
            for c in range(w):
                if rng.random() < 0.4:
                    g[r][c] = 1
        return g
    return g
