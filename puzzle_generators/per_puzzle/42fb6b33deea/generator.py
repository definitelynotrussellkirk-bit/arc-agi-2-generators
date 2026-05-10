"""Generator for arc_additional_puzzles_21_set6:M36 — Fill bbox of any color group with exactly 4 cells.

Rule: for each non-bg color, if it has exactly 4 cells, fill its bbox
with that color in an empty output grid.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_colors,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_quad_color, all_quad_colors, overlapping_bboxes.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "42fb6b33deea"
VERSION = "1.1.0"
TASK_ID = "42fb6b33deea"
SUMMARY = "Mix of color groups with various counts; only ones with exactly 4 cells get bbox-filled."

INVARIANTS = [
    "between 2 and 3 distinct non-bg colors",
    "≥1 color has exactly 4 cells (so output != input)",
    "color groups don't have overlapping bboxes",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_quad_color", "all_quad_colors", "overlapping_bboxes")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 6..10", "valid": "5..14"},
    "grid_w":         {"type": "int", "default": "rng 8..12", "valid": "7..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_colors":       {"type": "int", "default": "3", "valid": "2..4"},
    "palette_size":   {"type": "int", "default": "3", "valid": "2..4"},
    "position_bias":  {"type": "str", "default": "non_overlapping_bboxes",
                       "valid": "non_overlapping_bboxes"},
    "n_distinct_colors": {"type": "int", "default": "3", "valid": "2..4"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def _bb_overlap(b1, b2):
    return not (b1[2] < b2[0] or b2[2] < b1[0] or b1[3] < b2[1] or b2[3] < b1[1])


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 6, 7)
        w = ctx.draw_int("grid_w", 8, 9)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 11, 12)
    else:
        h = ctx.draw_int("grid_h", 6, 10)
        w = ctx.draw_int("grid_w", 8, 12)
    g = full_grid(h, w, 0)
    rng = ctx.draw_rng("layout")
    colors = list(range(1, 10)); rng.shuffle(colors)
    bboxes = []
    placed_4 = False
    for color in colors[:3]:
        for _ in range(20):
            rh = rng.randint(2, 4); rw = rng.randint(2, 4)
            r1 = rng.randint(0, h - rh); c1 = rng.randint(0, w - rw)
            bb = (r1, c1, r1 + rh - 1, c1 + rw - 1)
            if any(_bb_overlap(bb, ob) for ob in bboxes): continue
            if not placed_4:
                n_cells = 4; placed_4 = True
            else:
                n_cells = rng.choice([1, 2, 3, 5, 6])
            n_cells = min(n_cells, rh * rw)
            positions = [(r1+dr, c1+dc) for dr in range(rh) for dc in range(rw)]
            rng.shuffle(positions)
            if n_cells == 4 and rh*rw >= 4:
                corners = [(r1, c1), (r1, c1+rw-1), (r1+rh-1, c1), (r1+rh-1, c1+rw-1)]
                for cr in corners[:4]:
                    g[cr[0]][cr[1]] = color
            else:
                for r, c in positions[:n_cells]:
                    g[r][c] = color
            bboxes.append(bb)
            break
    return g


def _draw_from_degenerate(name, rng):
    h, w = 8, 10
    g = full_grid(h, w, 0)
    if name == "no_quad_color":
        # no color has exactly 4 cells → rule fires zero times, output blank
        g[1][1] = 4; g[1][3] = 4; g[2][2] = 4  # 3 cells
        g[5][5] = 6; g[5][6] = 6  # 2 cells
        g[7][8] = 3  # 1 cell
        return g
    if name == "all_quad_colors":
        # every color has exactly 4 cells → every group gets bbox-filled, dense output
        g[1][1] = 4; g[1][3] = 4; g[2][1] = 4; g[2][3] = 4
        g[5][5] = 6; g[5][7] = 6; g[6][5] = 6; g[6][7] = 6
        return g
    if name == "overlapping_bboxes":
        # two quad colors with overlapping bboxes → output collision
        g[1][1] = 4; g[1][4] = 4; g[3][1] = 4; g[3][4] = 4
        g[2][3] = 6; g[2][6] = 6; g[4][3] = 6; g[4][6] = 6  # overlaps in (2-3)x(3-4)
        return g
    return g
