"""Generator for 5b:m31 — scale key-adjacent component.

Rule: a single key cell (color 8) sits 4-adjacent to one of the
multi-cell shapes. That shape gets cropped and upscaled 2x. Output
keeps the shape's original color.

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: no_key (no color-8 cell → rule's selector returns
nothing), key_isolated (key not 4-adjacent to any shape → rule's
"adjacent component" selector finds nothing), key_adj_multiple (key
is 4-adjacent to multiple shapes → "the adjacent shape" is ambiguous).
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "725513c9d0c9"
VERSION = "1.1.0"
TASK_ID = "725513c9d0c9"
SUMMARY = "1 key cell (8) 4-adjacent to one shape + 2 unrelated shapes."

INVARIANTS = [
    "background is 0",
    "exactly one isolated key cell of color 8",
    "the key is 4-adjacent to exactly one multi-cell shape",
    "the other 1-2 shapes are not 4-adjacent to anything",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_key", "key_isolated", "key_adj_multiple")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":            {"type": "int", "default": "rng 9..11", "valid": "8..14"},
    "grid_w":            {"type": "int", "default": "rng 11..13", "valid": "10..16"},
    "palette_kind":      {"type": "str", "default": "rng helpful",
                          "valid": "|".join(PALETTE_KINDS)},
    "palette_size":      {"type": "int", "default": "rng 3..4", "valid": "3..5"},
    "position_bias":     {"type": "str", "default": "key_adj_one_shape",
                          "valid": "key_adj_one_shape"},
    "n_distinct_colors": {"type": "int", "default": "rng 3..4", "valid": "3..5"},
    "density":           {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":           {"type": "str", "default": "alias for palette_kind",
                          "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}

_SHAPES = [
    [(0, 0), (1, 0), (2, 0), (2, 1)],
    [(0, 0), (0, 1), (1, 0)],
    [(0, 0), (1, 0), (1, 1), (2, 1)],
    [(0, 0), (0, 1), (0, 2), (1, 1)],
    [(0, 0), (0, 1), (1, 0), (1, 1)],
    [(0, 0), (0, 1), (0, 2), (1, 0)],
]


def _free(g, r1, c1, r2, c2):
    h, w = len(g), len(g[0])
    if r1 < 0 or c1 < 0 or r2 >= h or c2 >= w: return False
    for r in range(max(0, r1 - 1), min(h, r2 + 2)):
        for c in range(max(0, c1 - 1), min(w, c2 + 2)):
            if g[r][c] != 0: return False
    return True


def _place(g, rng, shape, color):
    h, w = len(g), len(g[0])
    sh = max(r for r, _ in shape) + 1
    sw = max(c for _, c in shape) + 1
    for _ in range(40):
        r0 = rng.randint(1, h - sh - 1); c0 = rng.randint(1, w - sw - 1)
        if not _free(g, r0, c0, r0 + sh - 1, c0 + sw - 1): continue
        for dr, dc in shape:
            g[r0 + dr][c0 + dc] = color
        return (r0, c0, sh, sw)
    return None


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 9, 9)
        w = ctx.draw_int("grid_w", 11, 12)
        n_lo, n_hi = 2, 2
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 11, 11)
        w = ctx.draw_int("grid_w", 13, 13)
        n_lo, n_hi = 3, 3
    else:
        h = ctx.draw_int("grid_h", 9, 11)
        w = ctx.draw_int("grid_w", 11, 13)
        n_lo, n_hi = 2, 3
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    n_shapes = rng.randint(n_lo, n_hi)
    palette = rng.sample([2, 3, 4, 5, 6, 7, 9], n_shapes)
    placed_keyed = None
    for i, color in enumerate(palette):
        info = _place(g, rng, rng.choice(_SHAPES), color)
        if i == 0 and info is not None:
            placed_keyed = info
    if placed_keyed is None:
        return g
    r0, c0, sh, sw = placed_keyed
    candidates = []
    shape_cells = [(r, c) for r in range(r0, r0 + sh) for c in range(c0, c0 + sw)
                   if g[r][c] == palette[0]]
    for r, c in shape_cells:
        for dr, dc in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            nr, nc = r + dr, c + dc
            if 0 <= nr < h and 0 <= nc < w and g[nr][nc] == 0:
                candidates.append((nr, nc))
    valid = []
    for nr, nc in candidates:
        bad = False
        for dr, dc in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            rr, cc = nr + dr, nc + dc
            if 0 <= rr < h and 0 <= cc < w and g[rr][cc] not in (0, palette[0]):
                bad = True; break
        if not bad: valid.append((nr, nc))
    if valid:
        nr, nc = rng.choice(valid)
        g[nr][nc] = 8
    return g


def _draw_from_degenerate(name, rng):
    h, w = 10, 12
    g = full_grid(h, w, 0)
    if name == "no_key":
        # No color-8 — rule's selector returns nothing.
        for dr, dc in [(0, 0), (1, 0), (1, 1)]:
            g[2 + dr][2 + dc] = 4
        for dr, dc in [(0, 0), (0, 1), (1, 0)]:
            g[6 + dr][7 + dc] = 6
        return g
    if name == "key_isolated":
        # Key not 4-adjacent to any shape — selector finds nothing.
        for dr, dc in [(0, 0), (1, 0), (1, 1)]:
            g[2 + dr][2 + dc] = 4
        for dr, dc in [(0, 0), (0, 1), (1, 0)]:
            g[6 + dr][7 + dc] = 6
        g[5][5] = 8   # isolated, no shape adjacent
        return g
    if name == "key_adj_multiple":
        # Key 4-adjacent to multiple shapes — "the adjacent shape" is
        # ambiguous.
        g[3][3] = 4
        g[3][5] = 6
        g[3][4] = 8   # adjacent to both color-4 and color-6
        return g
    return g
