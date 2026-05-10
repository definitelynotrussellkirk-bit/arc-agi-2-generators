"""Generator for puzzle f5c89df1.

Rule: green(3) anchor + 8-shape near it + red(2) markers. Output
copies 8-shape (relative to green) to each red marker; clears else.

Combinatorial axes (8): grid_h/w, n_shape_cells, n_reds,
shape_position, red_position, anchor_corner, asymmetry_force,
green_position.
Degenerates: no_shape, no_reds, single_marker.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "8de1c257a9c7"
VERSION = "1.1.0"
TASK_ID = "8de1c257a9c7"
SUMMARY = "Green + 8-shape + reds; rule copies 8-shape to each red."

INVARIANTS = [
    "background is 0",
    "exactly 1 green(3) anchor",
    "1-3 cyan(8) cells near green (the shape)",
    ">=2 red(2) markers",
    "shape relative to each red stays in-bounds",
]

GREEN_POSITIONS = ("upper_left", "upper_right", "center", "spread")
RED_POSITIONS = ("lower_right", "scattered", "row_aligned", "diagonal")
DEGENERATE_TEXTURES = ("no_shape", "no_reds", "single_marker")
HELPFUL_TEXTURES = GREEN_POSITIONS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 12..18", "valid": "10..22"},
    "grid_w":         {"type": "int", "default": "rng 12..18", "valid": "10..22"},
    "n_shape_cells":  {"type": "int", "default": "rng 1..3", "valid": "1..4"},
    "n_reds":         {"type": "int", "default": "rng 2..4", "valid": "2..5"},
    "green_position": {"type": "str", "default": "rng helpful",
                       "valid": "|".join(GREEN_POSITIONS)},
    "red_position":   {"type": "str", "default": "rng",
                       "valid": "|".join(RED_POSITIONS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "texture":        {"type": "str", "default": "alias for green_position",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if difficulty == "easy":
        h_lo, h_hi = 10, 13
    elif difficulty == "hard":
        h_lo, h_hi = 18, 22
    else:
        h_lo, h_hi = 12, 18
    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", h_lo, h_hi)
    rng = ctx.draw_rng("placement")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], h, w, rng)
    n_shape = int(overrides.get("n_shape_cells",
                                ctx.draw_int("n_shape_cells", 1, 3)))
    n_shape = max(1, min(4, n_shape))
    n_reds = int(overrides.get("n_reds",
                               ctx.draw_int("n_reds", 2, 4)))
    n_reds = max(2, min(5, n_reds))
    green_pos = (overrides.get("texture") or
                 overrides.get("green_position")
                 or ctx.draw_choice("green_position",
                                    list(GREEN_POSITIONS)))
    red_pos = overrides.get("red_position",
                            ctx.draw_choice("red_position",
                                            list(RED_POSITIONS)))
    g = full_grid(h, w, 0)
    gr, gc = _pick_green(green_pos, h, w, rng)
    g[gr][gc] = 3
    placed_8 = 0
    for _ in range(8):
        if placed_8 >= n_shape:
            break
        dr = rng.randint(-1, 1); dc = rng.randint(-1, 1)
        if dr == 0 and dc == 0:
            continue
        r, c = gr + dr, gc + dc
        if 0 <= r < h and 0 <= c < w and g[r][c] == 0:
            g[r][c] = 8
            placed_8 += 1
    if placed_8 < 1:
        # Force at least 1
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            r, c = gr + dr, gc + dc
            if 0 <= r < h and 0 <= c < w and g[r][c] == 0:
                g[r][c] = 8
                break
    placed_reds = 0
    for _ in range(20):
        if placed_reds >= n_reds:
            break
        r, c = _pick_red(red_pos, h, w, gr, gc, rng)
        if not (1 <= r < h - 1 and 1 <= c < w - 1):
            continue
        if g[r][c] != 0:
            continue
        ok = all(0 <= r + dr < h and 0 <= c + dc < w
                 for dr in (-1, 0, 1) for dc in (-1, 0, 1))
        if not ok:
            continue
        g[r][c] = 2
        placed_reds += 1
    if placed_reds < 2:
        for r, c in [(h - 3, w - 3), (h - 4, 1)]:
            if 1 <= r < h - 1 and 1 <= c < w - 1 and g[r][c] == 0:
                g[r][c] = 2
                placed_reds += 1
    return g


def _pick_green(name, h, w, rng):
    if name == "upper_left":
        return rng.randint(2, h // 3), rng.randint(2, w // 3)
    if name == "upper_right":
        return rng.randint(2, h // 3), rng.randint(2 * w // 3, w - 3)
    if name == "center":
        return h // 2, w // 2
    return rng.randint(2, h - 3), rng.randint(2, w - 3)


def _pick_red(name, h, w, gr, gc, rng):
    if name == "lower_right":
        return (rng.randint(h // 2 + 1, h - 3),
                rng.randint(w // 2 + 1, w - 3))
    if name == "row_aligned":
        return rng.randint(1, h - 2), rng.randint(w // 2, w - 2)
    if name == "diagonal":
        i = rng.randint(min(h, w) // 2, min(h, w) - 2)
        return i, i
    return rng.randint(1, h - 2), rng.randint(1, w - 2)


def _draw_from_degenerate(name, h, w, rng):
    g = full_grid(h, w, 0)
    if name == "no_shape":
        g[3][3] = 3
        g[7][7] = 2
        g[h - 3][w - 3] = 2
        return g
    if name == "no_reds":
        g[3][3] = 3
        g[3][4] = 8
        return g
    if name == "single_marker":
        g[3][3] = 3
        g[3][4] = 8
        g[h - 3][w - 3] = 2
        return g
    return g
