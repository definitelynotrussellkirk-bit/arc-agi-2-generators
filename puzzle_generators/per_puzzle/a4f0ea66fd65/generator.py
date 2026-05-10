"""Generator for arc_additional_puzzle_bank_volume21:E146 — copy cyan object by red→green vector.

Rule: a cyan object plus a red marker and a green marker. The output
adds a copy of the cyan object translated by the vector from the red
marker to the green marker.

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, object_size, texture.
Degenerates: no_markers, no_object, oob_destination.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "a4f0ea66fd65"
VERSION = "1.1.0"
TASK_ID = "a4f0ea66fd65"
SUMMARY = "A cyan object is copied by the vector from a red marker to a green marker."

INVARIANTS = [
    "background is 0",
    "there is exactly one red marker and one green marker",
    "cyan source object has a translated in-bounds destination",
    "translated destination cells are initially empty",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_markers", "no_object", "oob_destination")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..13", "valid": "6..24"},
    "grid_w":         {"type": "int", "default": "rng 8..13", "valid": "6..24"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "object_size":    {"type": "int", "default": "rng 3..6", "valid": "1..15"},
    "palette_size":   {"type": "int", "default": "3", "valid": "3..3"},
    "position_bias":  {"type": "str", "default": "object_with_red_green_marker_pair",
                       "valid": "object_with_red_green_marker_pair"},
    "n_distinct_colors": {"type": "int", "default": "3", "valid": "3..3"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("grid_w", 8, 9)
        object_size = ctx.draw_int("object_size", 3, 4)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 13, 18)
        w = ctx.draw_int("grid_w", 13, 18)
        object_size = ctx.draw_int("object_size", 4, 6)
    else:
        h = ctx.draw_int("grid_h", 8, 13)
        w = ctx.draw_int("grid_w", 8, 13)
        object_size = ctx.draw_int("object_size", 3, 6)
    rng = ctx.draw_rng("placement")
    g = full_grid(h, w, 0)
    dr, dc = rng.choice([(2, 1), (2, -1), (1, 2), (-1, 2), (-2, 1), (1, -2)])
    r_min = max(1, -dr + 1)
    r_max = min(h - 3, h - dr - 2)
    c_min = max(1, -dc + 1)
    c_max = min(w - 3, w - dc - 2)
    anchor = (rng.randint(r_min, r_max), rng.randint(c_min, c_max))
    local = [(0, 0), (0, 1), (1, 0), (1, 1)]
    rng.shuffle(local)
    cells = {(anchor[0] + lr, anchor[1] + lc) for lr, lc in local[:min(object_size, 4)]}
    for r, c in cells:
        g[r][c] = 8
    shifted = {(r + dr, c + dc) for r, c in cells}
    candidates = []
    for r in range(h):
        for c in range(w):
            gr, gc = r + dr, c + dc
            if not (0 <= gr < h and 0 <= gc < w):
                continue
            if (r, c) in cells or (gr, gc) in cells or (r, c) in shifted or (gr, gc) in shifted:
                continue
            candidates.append((r, c))
    marker_r, marker_c = rng.choice(candidates)
    g[marker_r][marker_c] = 2
    g[marker_r + dr][marker_c + dc] = 3
    return g


def _draw_from_degenerate(name, rng):
    h, w = 10, 10
    g = full_grid(h, w, 0)
    if name == "no_markers":
        # Cyan object only, no red/green markers — rule has no
        # translation vector to compute.
        for r, c in [(3, 3), (3, 4), (4, 3)]: g[r][c] = 8
        return g
    if name == "no_object":
        # Red + green markers but no cyan object — rule has nothing
        # to copy.
        g[2][2] = 2; g[4][5] = 3
        return g
    if name == "oob_destination":
        # Object + markers exist but the translated copy lands
        # entirely outside the grid — rule's destination is undefined.
        for r, c in [(7, 7), (7, 8), (8, 7)]: g[r][c] = 8
        g[7][8] = 8
        g[1][1] = 2
        g[8][8] = 3
        return g
    return g
