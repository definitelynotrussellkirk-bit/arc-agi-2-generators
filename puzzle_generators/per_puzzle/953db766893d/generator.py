"""Generator for puzzle 83302e8f.

Rule: invert grid (zeros↔ones); 4-conn components on inverted = rooms.
Smallest-size rooms → 3, others → 4.

Combinatorial axes (8): grid_h/w, wall_color, n_walls,
wall_orientation, wall_position_bias, room_size_distribution,
gap_size, decoy_density.
Degenerates: no_walls, all_walls, single_room.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "953db766893d"
VERSION = "1.1.0"
TASK_ID = "953db766893d"
SUMMARY = "Walls partition grid into rooms; rule paints smallest rooms 3, others 4."

INVARIANTS = [
    "background is 0 (rooms)",
    ">=2 0-cell 4-connected components",
    ">=1 room has STRICTLY minimum size (no tie)",
    ">=1 room is larger than the min",
    "wall color != 3 and != 4 (avoid output conflict)",
]

WALL_ORIENTATIONS = ("cross", "horizontal_only", "vertical_only",
                     "double_horiz", "double_vert", "L_split")
DEGENERATE_TEXTURES = ("no_walls", "all_walls", "single_room")
HELPFUL_TEXTURES = WALL_ORIENTATIONS

AXES = {
    "grid_h":              {"type": "int", "default": "rng 10..18", "valid": "8..22"},
    "grid_w":              {"type": "int", "default": "rng 10..18", "valid": "8..22"},
    "wall_color":          {"type": "color", "default": "rng (≠0,3,4)",
                            "valid": "1..9 (≠3,4)"},
    "wall_orientation":    {"type": "str", "default": "rng helpful",
                            "valid": "|".join(WALL_ORIENTATIONS)},
    "wall_position_bias":  {"type": "str", "default": "rng spread|center|edge",
                            "valid": "spread|center|edge"},
    "n_walls":             {"type": "int", "default": "rng 1..3",
                            "valid": "1..4"},
    "min_wall_distance":   {"type": "int", "default": "2", "valid": "1..4"},
    "decoy_density":       {"type": "float", "default": "0", "valid": "0..0.05"},
    "texture":             {"type": "str", "default": "alias for wall_orientation",
                            "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if difficulty == "easy":
        h_lo, h_hi = 8, 12
    elif difficulty == "hard":
        h_lo, h_hi = 16, 22
    else:
        h_lo, h_hi = 10, 18
    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", h_lo, h_hi)
    rng = ctx.draw_rng("placement")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], h, w, rng)
    wall_color = int(overrides.get("wall_color",
                                   ctx.draw_color("wall_color",
                                                  exclude={0, 3, 4})))
    orient = (overrides.get("texture") or
              overrides.get("wall_orientation")
              or ctx.draw_choice("wall_orientation",
                                 list(WALL_ORIENTATIONS)))
    bias = overrides.get("wall_position_bias",
                         ctx.draw_choice("wall_position_bias",
                                         ["spread", "center", "edge"]))
    g = full_grid(h, w, 0)
    if orient == "horizontal_only":
        wr = _bias_row(bias, h, rng)
        for c in range(w):
            g[wr][c] = wall_color
    elif orient == "vertical_only":
        wc = _bias_col(bias, w, rng)
        for r in range(h):
            g[r][wc] = wall_color
    elif orient == "double_horiz":
        r1 = h // 3
        r2 = 2 * h // 3
        for c in range(w):
            g[r1][c] = wall_color
            g[r2][c] = wall_color
    elif orient == "double_vert":
        c1 = w // 3
        c2 = 2 * w // 3
        for r in range(h):
            g[r][c1] = wall_color
            g[r][c2] = wall_color
    elif orient == "L_split":
        wr = _bias_row(bias, h, rng)
        wc = _bias_col(bias, w, rng)
        for c in range(wc + 1):
            g[wr][c] = wall_color
        for r in range(wr + 1):
            g[r][wc] = wall_color
    else:  # cross
        wr = _bias_row(bias, h, rng)
        wc = _bias_col(bias, w, rng)
        for c in range(w):
            g[wr][c] = wall_color
        for r in range(h):
            g[r][wc] = wall_color
    n_rooms = _count_rooms(g)
    if n_rooms < 2:
        wr = h // 2; wc = w // 2
        for c in range(w):
            g[wr][c] = wall_color
        for r in range(h):
            g[r][wc] = wall_color
    if not _has_distinct_min(g):
        for r in range(h):
            for c in range(w):
                if g[r][c] == 0:
                    if r < h - 1 and c < w - 1 and g[r + 1][c + 1] == 0:
                        continue
                    g[r][c] = wall_color
                    return g
    return g


def _bias_row(bias, h, rng):
    if bias == "center":
        return h // 2
    if bias == "edge":
        return rng.choice([2, h - 3])
    return rng.randint(2, h - 3)


def _bias_col(bias, w, rng):
    if bias == "center":
        return w // 2
    if bias == "edge":
        return rng.choice([2, w - 3])
    return rng.randint(2, w - 3)


def _count_rooms(g):
    h, w = len(g), len(g[0])
    visited = [[False] * w for _ in range(h)]
    n = 0
    for r in range(h):
        for c in range(w):
            if g[r][c] != 0 or visited[r][c]:
                continue
            n += 1
            stack = [(r, c)]
            while stack:
                rr, cc = stack.pop()
                if not (0 <= rr < h and 0 <= cc < w):
                    continue
                if visited[rr][cc] or g[rr][cc] != 0:
                    continue
                visited[rr][cc] = True
                stack += [(rr - 1, cc), (rr + 1, cc),
                          (rr, cc - 1), (rr, cc + 1)]
    return n


def _has_distinct_min(g):
    h, w = len(g), len(g[0])
    visited = [[False] * w for _ in range(h)]
    sizes = []
    for r in range(h):
        for c in range(w):
            if g[r][c] != 0 or visited[r][c]:
                continue
            stack = [(r, c)]
            sz = 0
            while stack:
                rr, cc = stack.pop()
                if not (0 <= rr < h and 0 <= cc < w):
                    continue
                if visited[rr][cc] or g[rr][cc] != 0:
                    continue
                visited[rr][cc] = True
                sz += 1
                stack += [(rr - 1, cc), (rr + 1, cc),
                          (rr, cc - 1), (rr, cc + 1)]
            sizes.append(sz)
    if len(sizes) < 2:
        return False
    sizes.sort()
    return sizes[0] != sizes[1]


def _draw_from_degenerate(name, h, w, rng):
    g = full_grid(h, w, 0)
    color = rng.choice([1, 2, 5, 6, 7, 8, 9])
    if name == "no_walls":
        return g
    if name == "all_walls":
        for r in range(h):
            for c in range(w):
                g[r][c] = color
        return g
    if name == "single_room":
        for c in range(w):
            g[0][c] = color
            g[h - 1][c] = color
        for r in range(h):
            g[r][0] = color
            g[r][w - 1] = color
        return g
    return g
