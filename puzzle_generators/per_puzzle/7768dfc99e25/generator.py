"""Generator for arc_puzzle_bank_21_set5_s:S5_E5 — crop red border-toucher.

Among red objects, crop the one that touches the grid border.

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: no_border_touch (no red touches the border → rule's
selector finds nothing, output undefined), all_border_touch (every
red touches the border → tie-break decides which one to crop, no
contrast), single_object (only one red object, trivially the
border-toucher → no candidate contrast).
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "7768dfc99e25"
VERSION = "1.1.0"
TASK_ID = "7768dfc99e25"

SUMMARY = "Among red objects, crop the one that touches the grid border."

INVARIANTS = [
    "background is 0",
    "there are multiple red objects",
    "exactly one red object touches the outer border",
    "interior red distractors do not touch the selected border object",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_border_touch", "all_border_touch", "single_object")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":            {"type": "int", "default": "rng 8..10", "valid": "6..14"},
    "grid_w":            {"type": "int", "default": "rng 8..11", "valid": "6..14"},
    "border_side":       {"type": "choice", "default": "rng top|left|right|bottom",
                          "valid": "top|left|right|bottom"},
    "palette_kind":      {"type": "str", "default": "rng helpful",
                          "valid": "|".join(PALETTE_KINDS)},
    "palette_size":      {"type": "int", "default": "rng 1..1", "valid": "1..1"},
    "position_bias":     {"type": "str", "default": "border_red_plus_interior_reds",
                          "valid": "border_red_plus_interior_reds"},
    "n_distinct_colors": {"type": "int", "default": "rng 1..1", "valid": "1..1"},
    "density":           {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":           {"type": "str", "default": "alias for palette_kind",
                          "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}

_BORDER_SHAPES = [
    [(0, 0), (1, 0), (2, 0), (2, 1)],
    [(0, 0), (0, 1), (1, 1), (2, 1)],
    [(0, 0), (0, 1), (1, 0), (2, 0), (2, 1)],
]

_INTERIOR_SHAPES = [
    [(0, 0), (0, 1)],
    [(0, 0), (1, 0), (1, 1)],
    [(0, 0), (0, 1), (1, 0), (1, 1)],
]


def _paint(g, cells, r0, c0, color):
    for dr, dc in cells:
        g[r0 + dr][c0 + dc] = color


def _clear(g, cells, r0, c0, occupied):
    h = len(g)
    w = len(g[0])
    placed = [(r0 + r, c0 + c) for r, c in cells]
    if any(r < 0 or c < 0 or r >= h or c >= w for r, c in placed):
        return False
    if any(g[r][c] != 0 for r, c in placed):
        return False
    return not any(abs(r - rr) <= 1 and abs(c - cc) <= 1
                   for r, c in placed for rr, cc in occupied)


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index, version=VERSION,
                  task_id=TASK_ID, difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 8, 8)
        w = ctx.draw_int("grid_w", 8, 9)
        n_distractors = 1
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 10, 10)
        w = ctx.draw_int("grid_w", 11, 11)
        n_distractors = 3
    else:
        h = ctx.draw_int("grid_h", 8, 10)
        w = ctx.draw_int("grid_w", 8, 11)
        n_distractors = 2
    side = ctx.draw_choice("border_side", ["top", "left", "right", "bottom"])
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    shape = rng.choice(_BORDER_SHAPES)
    sh = max(r for r, _ in shape) + 1
    sw = max(c for _, c in shape) + 1
    if side == "top":
        r0 = 0
        c0 = rng.randint(1, w - sw - 1)
    elif side == "bottom":
        r0 = h - sh
        c0 = rng.randint(1, w - sw - 1)
    elif side == "left":
        r0 = rng.randint(1, h - sh - 1)
        c0 = 0
    else:
        r0 = rng.randint(1, h - sh - 1)
        c0 = w - sw
    _paint(g, shape, r0, c0, 2)
    occupied = {(r0 + r, c0 + c) for r, c in shape}
    for _ in range(n_distractors):
        cells = rng.choice(_INTERIOR_SHAPES)
        max_r = max(r for r, _ in cells)
        max_c = max(c for _, c in cells)
        for _attempt in range(200):
            rr = rng.randint(1, h - max_r - 2)
            cc = rng.randint(1, w - max_c - 2)
            if _clear(g, cells, rr, cc, occupied):
                _paint(g, cells, rr, cc, 2)
                occupied.update((rr + r, cc + c) for r, c in cells)
                break
        else:
            raise ValueError("could not place interior red object")
    if rng.random() < 0.5:
        g[h - 1][w - 1] = 1
    return g


def _draw_from_degenerate(name, rng):
    h, w = 9, 10
    g = full_grid(h, w, 0)
    if name == "no_border_touch":
        # No red touches the outer border — rule's selector finds
        # nothing; output is undefined.
        for dr, dc in [(0, 0), (0, 1), (1, 0)]:
            g[3 + dr][3 + dc] = 2
        for dr, dc in [(0, 0), (1, 0)]:
            g[5 + dr][6 + dc] = 2
        return g
    if name == "all_border_touch":
        # Every red touches the border — tie-break decides which one
        # is cropped; no contrast.
        g[0][2] = 2; g[0][3] = 2; g[1][3] = 2
        g[h - 1][6] = 2; g[h - 2][6] = 2
        g[4][0] = 2; g[5][0] = 2
        return g
    if name == "single_object":
        # Only one red object, trivially the border-toucher — no
        # cross-candidate contrast.
        g[0][3] = 2; g[1][3] = 2; g[1][4] = 2; g[2][3] = 2
        return g
    return g
