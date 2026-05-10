"""Generator for next_b:m10 — recolor objects by above key.

Rule: a single key cell sits directly above a multi-cell shape;
the shape gets recolored to match the key's color.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_groups,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_keys, key_below_shape, multiple_keys_per_shape.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "b71c45e9a3c0"
VERSION = "1.1.0"
TASK_ID = "b71c45e9a3c0"
SUMMARY = "2-3 (key cell above, multi-cell color-3 shape below) groups."

INVARIANTS = [
    "background is 0",
    "shapes use a single shared color (3)",
    "each group has a single key cell directly above a multi-cell color-3 shape",
    "groups don't overlap and aren't 4-adjacent",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_keys", "key_below_shape", "multiple_keys_per_shape")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 9..12", "valid": "8..14"},
    "grid_w":         {"type": "int", "default": "rng 9..12", "valid": "8..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_groups":       {"type": "int", "default": "rng 2..3", "valid": "1..4"},
    "palette_size":   {"type": "int", "default": "rng 2..3", "valid": "1..5"},
    "position_bias":  {"type": "str", "default": "key_above_shape",
                       "valid": "key_above_shape"},
    "n_distinct_colors": {"type": "int", "default": "rng 2..3", "valid": "1..5"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}

_SHAPES = [
    [(0, 0), (1, 0), (1, 1)],
    [(0, 0), (0, 1), (1, 1)],
    [(0, 0), (1, 0), (2, 0), (2, 1)],
    [(0, 0), (0, 1), (1, 0)],
    [(0, 0), (0, 1), (1, 0), (1, 1)],
    [(0, 0), (1, 0), (1, 1), (2, 1)],
]


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 9, 10)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 11, 12)
        w = ctx.draw_int("grid_w", 11, 12)
    else:
        h = ctx.draw_int("grid_h", 9, 12)
        w = ctx.draw_int("grid_w", 9, 12)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    n = rng.randint(2, 3)
    palette = rng.sample([1, 2, 4, 5, 6, 7, 8, 9], n)
    used: set[tuple[int, int]] = set()
    for color in palette:
        for _ in range(60):
            shape = rng.choice(_SHAPES)
            sh = max(r for r, _ in shape) + 1
            sw = max(c for _, c in shape) + 1
            r_shape = rng.randint(2, h - sh)
            c0 = rng.randint(0, w - sw)
            shape_top_cols = [c for r, c in shape if r == 0]
            key_c = c0 + shape_top_cols[0]
            r_key = r_shape - 2
            cells = [(r_shape + dr, c0 + dc) for dr, dc in shape]
            cells.append((r_key, key_c))
            bad = False
            for r, c in cells:
                for rr in range(max(0, r - 1), min(h, r + 2)):
                    for cc in range(max(0, c - 1), min(w, c + 2)):
                        if (rr, cc) in used: bad = True; break
                    if bad: break
                if bad: break
            if bad: continue
            for r, c in cells[:-1]: g[r][c] = 3
            g[r_key][key_c] = color
            for r, c in cells:
                for rr in range(max(0, r - 1), min(h, r + 2)):
                    for cc in range(max(0, c - 1), min(w, c + 2)):
                        used.add((rr, cc))
            break
    return g


def _draw_from_degenerate(name, rng):
    h, w = 10, 10
    g = full_grid(h, w, 0)
    if name == "no_keys":
        # no key cells, only color-3 shapes → rule has no recolor target
        for r, c in [(3, 2), (4, 2), (4, 3)]:
            g[r][c] = 3
        for r, c in [(7, 6), (7, 7), (8, 6)]:
            g[r][c] = 3
        return g
    if name == "key_below_shape":
        # key sits BELOW the shape → "key above shape" invariant violated, ambiguous association
        for r, c in [(2, 3), (3, 3), (3, 4)]:
            g[r][c] = 3
        g[6][3] = 5  # key below shape, not above
        return g
    if name == "multiple_keys_per_shape":
        # multiple keys sit above one shape → ambiguous which key's color to apply
        for r, c in [(5, 3), (5, 4), (6, 3)]:
            g[r][c] = 3
        g[2][3] = 4  # key 1
        g[3][4] = 6  # key 2
        return g
    return g
