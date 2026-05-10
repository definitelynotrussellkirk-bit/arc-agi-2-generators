"""Generator for arc_puzzle_bank_fifteenth_21_bundle:easy_105_crop_the_unique_object.

Rule: crop to the bounding box of the single connected nonzero object.

Combinatorial axes (8): grid_h, grid_w, palette_kind, object_cells,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_object, multiple_objects, full_grid_object.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "65dc463a7236"
VERSION = "1.1.0"
TASK_ID = "65dc463a7236"

SUMMARY = "Embed one connected object inside a larger zero grid for nonzero cropping."

INVARIANTS = [
    "background is 0",
    "there is one connected nonzero object",
    "object is inset from the canvas border",
    "output is the object's nonzero bounding box",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_object", "multiple_objects", "full_grid_object")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..10", "valid": "5..16"},
    "grid_w":         {"type": "int", "default": "rng 9..12", "valid": "5..18"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "object_cells":   {"type": "int", "default": "rng 4..7", "valid": "1..20"},
    "palette_size":   {"type": "int", "default": "1", "valid": "1..2"},
    "position_bias":  {"type": "str", "default": "centered_object",
                       "valid": "centered_object"},
    "n_distinct_colors": {"type": "int", "default": "1", "valid": "1..2"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index, version=VERSION,
                  task_id=TASK_ID, difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 8, 8)
        w = ctx.draw_int("grid_w", 9, 10)
        target = ctx.draw_int("object_cells", 4, 5)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 11, 12)
        target = ctx.draw_int("object_cells", 6, 7)
    else:
        h = ctx.draw_int("grid_h", 8, 10)
        w = ctx.draw_int("grid_w", 9, 12)
        target = ctx.draw_int("object_cells", 4, 7)
    rng = ctx.draw_rng("layout")
    color = rng.choice([1, 2, 3, 4, 5, 6, 7, 8, 9])
    cells = {(0, 0)}
    frontier = [(0, 0)]
    attempts = 0
    while len(cells) < target and frontier and attempts < 300:
        attempts += 1
        r, c = rng.choice(frontier)
        dr, dc = rng.choice([(-1, 0), (1, 0), (0, -1), (0, 1)])
        nr, nc = r + dr, c + dc
        if -2 <= nr <= 2 and -2 <= nc <= 2 and (nr, nc) not in cells:
            cells.add((nr, nc))
            frontier.append((nr, nc))
    min_r = min(r for r, _ in cells)
    min_c = min(c for _, c in cells)
    norm = [(r - min_r, c - min_c) for r, c in cells]
    obj_h = max(r for r, _ in norm) + 1
    obj_w = max(c for _, c in norm) + 1
    top = rng.randint(1, h - obj_h - 1)
    left = rng.randint(1, w - obj_w - 1)
    g = full_grid(h, w, 0)
    for r, c in norm:
        g[top + r][left + c] = color
    return g


def _draw_from_degenerate(name, rng):
    h, w = 9, 10
    g = full_grid(h, w, 0)
    if name == "no_object":
        # blank → no object to crop
        return g
    if name == "multiple_objects":
        # two separated objects → "the unique object" is ambiguous
        for (r, c) in [(1, 1), (1, 2), (2, 1)]: g[r][c] = 4
        for (r, c) in [(6, 7), (6, 8), (7, 8)]: g[r][c] = 6
        return g
    if name == "full_grid_object":
        # object spans whole grid → crop is identity
        for r in range(h):
            for c in range(w):
                g[r][c] = 4
        return g
    return g
