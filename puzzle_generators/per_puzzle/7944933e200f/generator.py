"""Generator for d9fac9be.

Rule: among 4-conn non-bg objects, find the one whose color has the
fewest occurrences in the grid; output bbox crop of that object.

Combinatorial axes (8): grid_h/w, n_common_palette, common_density,
rare_color, rare_object_size, rare_object_layout, rare_position_bias,
common_palette_kind.
Degenerates: no_common, no_rare, all_same_color.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "7944933e200f"
VERSION = "1.1.0"
TASK_ID = "7944933e200f"
SUMMARY = "Many cells of common colors and a single rarer-color object."

INVARIANTS = [
    "background is 0",
    ">=1 common-color cell with count >=3",
    "exactly 1 color appears with strictly minimum count >=1 (no tie at min)",
    "rare-color object is non-empty (>=1 cell)",
    "rare-color count is strictly less than every other non-bg color count",
]

RARE_LAYOUTS = ("single_pixel", "small_blob", "horizontal_pair",
                "vertical_pair", "diagonal_pair", "L_triplet")
COMMON_PALETTES = ("blue_red", "warm", "cool", "broad")
DEGENERATE_TEXTURES = ("no_common", "no_rare", "all_same_color")
HELPFUL_TEXTURES = RARE_LAYOUTS

AXES = {
    "grid_h":              {"type": "int", "default": "rng 9..14", "valid": "8..18"},
    "grid_w":              {"type": "int", "default": "rng 9..14", "valid": "8..18"},
    "common_density":      {"type": "float", "default": "rng 0.25..0.45",
                            "valid": "0.1..0.6"},
    "common_palette_kind": {"type": "str", "default": "rng helpful",
                            "valid": "|".join(COMMON_PALETTES)},
    "rare_color":          {"type": "color", "default": "rng (≠0,common)",
                            "valid": "1..9"},
    "rare_object_layout":  {"type": "str", "default": "rng helpful",
                            "valid": "|".join(RARE_LAYOUTS)},
    "rare_position_bias":  {"type": "str", "default": "rng spread|center|edge",
                            "valid": "spread|center|edge"},
    "rare_object_size":    {"type": "int", "default": "rng 1..3", "valid": "1..5"},
    "texture":             {"type": "str", "default": "alias for rare_object_layout",
                            "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if difficulty == "easy":
        h_lo, h_hi = 8, 10
    elif difficulty == "hard":
        h_lo, h_hi = 13, 18
    else:
        h_lo, h_hi = 9, 14
    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", h_lo, h_hi)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], h, w, rng)
    common_kind = overrides.get("common_palette_kind",
                                ctx.draw_choice("common_palette_kind",
                                                list(COMMON_PALETTES)))
    if common_kind == "blue_red":
        common_palette = [1, 2]
    elif common_kind == "warm":
        common_palette = [3, 4, 6]
    elif common_kind == "cool":
        common_palette = [1, 5, 8]
    else:
        common_palette = [1, 2, 3]
    density = float(overrides.get("common_density",
                                  ctx.draw_rng("common_density")
                                  .uniform(0.25, 0.45)))
    layout = (overrides.get("texture") or overrides.get("rare_object_layout")
              or ctx.draw_choice("rare_object_layout", list(RARE_LAYOUTS)))
    bias = overrides.get("rare_position_bias",
                         ctx.draw_choice("rare_position_bias",
                                         ["spread", "center", "edge"]))
    rare_pool = [c for c in range(1, 10) if c not in common_palette]
    rng.shuffle(rare_pool)
    rare = int(overrides.get("rare_color", rare_pool[0]))
    rare_size = int(overrides.get("rare_object_size",
                                  ctx.draw_int("rare_object_size", 1, 3)))
    g = full_grid(h, w, 0)
    for r in range(h):
        for c in range(w):
            if rng.random() < density:
                g[r][c] = rng.choice(common_palette)
    rare_cells = _rare_cells(layout, h, w, rare_size, bias, rng)
    for r, c in rare_cells:
        if 0 <= r < h and 0 <= c < w:
            g[r][c] = rare
    if not any(g[r][c] == rare for r in range(h) for c in range(w)):
        g[h // 2][w // 2] = rare
    rare_count = sum(1 for r in range(h) for c in range(w) if g[r][c] == rare)
    counts = {c: 0 for c in common_palette}
    for r in range(h):
        for c in range(w):
            if g[r][c] in counts:
                counts[g[r][c]] += 1
    for color, cnt in counts.items():
        while cnt <= rare_count:
            cells_with_other = [(r, c) for r in range(h) for c in range(w)
                                if g[r][c] == 0]
            if not cells_with_other:
                break
            r, c = rng.choice(cells_with_other)
            g[r][c] = color
            cnt += 1
            counts[color] = cnt
    return g


def _rare_cells(layout, h, w, size, bias, rng):
    if bias == "center":
        cr, cc = h // 2, w // 2
    elif bias == "edge":
        cr = rng.choice([1, h - 2])
        cc = rng.choice([1, w - 2])
    else:
        cr = rng.randint(1, h - 2)
        cc = rng.randint(1, w - 2)
    if layout == "single_pixel":
        return [(cr, cc)]
    if layout == "small_blob":
        return [(cr, cc), (cr, cc + 1), (cr + 1, cc)]
    if layout == "horizontal_pair":
        return [(cr, cc), (cr, cc + 1)]
    if layout == "vertical_pair":
        return [(cr, cc), (cr + 1, cc)]
    if layout == "diagonal_pair":
        return [(cr, cc), (cr + 1, cc + 1)]
    if layout == "L_triplet":
        return [(cr, cc), (cr + 1, cc), (cr + 1, cc + 1)]
    return [(cr, cc)] * size


def _draw_from_degenerate(name, h, w, rng):
    g = full_grid(h, w, 0)
    if name == "no_common":
        g[h // 2][w // 2] = rng.choice([3, 4, 5, 6, 7, 8, 9])
        return g
    if name == "no_rare":
        for r in range(h):
            for c in range(w):
                if rng.random() < 0.3:
                    g[r][c] = rng.choice([1, 2])
        return g
    if name == "all_same_color":
        c = rng.choice([1, 2, 3, 4, 5, 6, 7, 8, 9])
        for r in range(h):
            for cc in range(w):
                g[r][cc] = c
        return g
    return g
