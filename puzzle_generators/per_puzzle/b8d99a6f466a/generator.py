"""Generator for arc_additional_puzzles_21_set21_bundle:M142 -- flood rooms from markers.

Combinatorial axes (8): grid_h, grid_w, palette_kind, rooms,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_walls, no_markers, multiple_markers_per_room.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "b8d99a6f466a"
VERSION = "1.1.0"
TASK_ID = "b8d99a6f466a"
SUMMARY = "Walls of 1 split the canvas into rooms; colored markers flood their room."

INVARIANTS = [
    "wall cells are color 1",
    "each zero region contains exactly one marker color other than 0 or 1",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_walls", "no_markers", "multiple_markers_per_room")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..12", "valid": "6..16"},
    "grid_w":         {"type": "int", "default": "rng 8..12", "valid": "6..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "rooms":          {"type": "choice", "default": "rng 2 or 4", "valid": "2 or 4"},
    "palette_size":   {"type": "int", "default": "rng 2..4", "valid": "2..5"},
    "position_bias":  {"type": "str", "default": "1walls_split_into_rooms",
                       "valid": "1walls_split_into_rooms"},
    "n_distinct_colors": {"type": "int", "default": "rng 2..4", "valid": "2..5"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(
        seed=seed,
        sample_index=sample_index,
        version=VERSION,
        task_id=TASK_ID,
        difficulty=difficulty,
        overrides=overrides,
    )
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("grid_w", 8, 9)
        rooms = ctx.draw_choice("rooms", [2])
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 11, 12)
        w = ctx.draw_int("grid_w", 11, 12)
        rooms = ctx.draw_choice("rooms", [4])
    else:
        h = ctx.draw_int("grid_h", 8, 12)
        w = ctx.draw_int("grid_w", 8, 12)
        rooms = ctx.draw_choice("rooms", [2, 4])
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    split_r = h // 2
    split_c = w // 2
    for c in range(w):
        g[split_r][c] = 1
    if rooms == 4:
        for r in range(h):
            g[r][split_c] = 1

    areas = [
        (1, 1, split_r - 1, split_c - 1 if rooms == 4 else w - 2),
        (split_r + 1, 1, h - 2, split_c - 1 if rooms == 4 else w - 2),
    ]
    if rooms == 4:
        areas.extend([
            (1, split_c + 1, split_r - 1, w - 2),
            (split_r + 1, split_c + 1, h - 2, w - 2),
        ])
    colors = list(ctx.draw_distinct_colors("markers", n=len(areas), exclude=[0, 1]))
    for color, (r1, c1, r2, c2) in zip(colors, areas):
        if r1 <= r2 and c1 <= c2:
            g[rng.randint(r1, r2)][rng.randint(c1, c2)] = color
    return g


def _draw_from_degenerate(name, rng):
    h, w = 9, 9
    g = full_grid(h, w, 0)
    if name == "no_walls":
        # markers without 1-walls → no rooms to flood within
        g[2][2] = 4; g[6][6] = 6
        return g
    if name == "no_markers":
        # walls form rooms but no markers → nothing to flood with
        for c in range(w): g[4][c] = 1
        return g
    if name == "multiple_markers_per_room":
        # one room has 2 markers → ambiguous flood color
        for c in range(w): g[4][c] = 1
        g[1][1] = 4; g[2][3] = 6  # 2 markers in top room
        g[6][3] = 7
        return g
    return g
