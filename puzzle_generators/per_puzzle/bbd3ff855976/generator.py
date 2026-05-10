"""Generator for 15b:hard_103 — overlay anchor stamps into count map.

Rule: anchors are 9-cells; the prototype is the largest non-9, non-bg
shape. Output stamps the prototype's binary mask at each anchor with
overlap counts.

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: no_anchors (no 9-cells → rule's per-anchor stamp loop
is empty, output equals input), no_prototype (no non-9 shape → rule's
extractor finds nothing), single_cell_prototype (prototype is one
cell → stamp is trivial, no shape contrast).
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "bbd3ff855976"
VERSION = "1.1.0"
TASK_ID = "bbd3ff855976"
SUMMARY = "Prototype shape (non-9 color) + 2-3 anchors (color 9)."

INVARIANTS = [
    "background is 0",
    "exactly one prototype shape (non-9, non-bg color)",
    "2-3 isolated 9-anchor cells",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_anchors", "no_prototype", "single_cell_prototype")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 11..13", "valid": "10..16"},
    "grid_w":         {"type": "int", "default": "rng 12..14", "valid": "10..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "palette_size":   {"type": "int", "default": "2", "valid": "2..2"},
    "position_bias":  {"type": "str", "default": "prototype_plus_anchors",
                       "valid": "prototype_plus_anchors"},
    "n_distinct_colors": {"type": "int", "default": "2", "valid": "2..2"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


_SHAPES = [
    [(0, 0), (0, 1), (1, 0), (1, 1)],
    [(0, 0), (0, 1), (0, 2), (1, 1)],
    [(0, 0), (1, 0), (1, 1), (2, 1)],
    [(0, 0), (0, 1), (1, 0)],
]


def _free(g, r1, c1, r2, c2):
    h, w = len(g), len(g[0])
    if r1 < 0 or c1 < 0 or r2 >= h or c2 >= w: return False
    for r in range(max(0, r1 - 1), min(h, r2 + 2)):
        for c in range(max(0, c1 - 1), min(w, c2 + 2)):
            if g[r][c] != 0: return False
    return True


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 11, 11)
        w = ctx.draw_int("grid_w", 12, 12)
        n_anchors_lo, n_anchors_hi = 2, 2
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 13, 15)
        w = ctx.draw_int("grid_w", 14, 16)
        n_anchors_lo, n_anchors_hi = 3, 4
    else:
        h = ctx.draw_int("grid_h", 11, 13)
        w = ctx.draw_int("grid_w", 12, 14)
        n_anchors_lo, n_anchors_hi = 2, 3
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    proto_color = rng.choice([1, 2, 3, 4, 5, 6, 7, 8])
    shape = rng.choice(_SHAPES)
    sh = max(r for r, _ in shape) + 1
    sw = max(c for _, c in shape) + 1
    placed = False
    for _ in range(40):
        r0 = rng.randint(0, h - sh); c0 = rng.randint(0, w - sw)
        if not _free(g, r0, c0, r0 + sh - 1, c0 + sw - 1): continue
        for dr, dc in shape:
            g[r0 + dr][c0 + dc] = proto_color
        placed = True; break
    if not placed: return g
    n_anchors = rng.randint(n_anchors_lo, n_anchors_hi)
    placed_anchors = 0
    for _ in range(60):
        if placed_anchors >= n_anchors: break
        r = rng.randint(2, h - 3); c = rng.randint(2, w - 3)
        if g[r][c] != 0: continue
        bad = False
        for dr in (-1, 0, 1):
            for dc in (-1, 0, 1):
                rr, cc = r + dr, c + dc
                if 0 <= rr < h and 0 <= cc < w and g[rr][cc] != 0:
                    bad = True; break
            if bad: break
        if bad: continue
        g[r][c] = 9
        placed_anchors += 1
    return g


def _draw_from_degenerate(name, rng):
    h, w = 12, 13
    g = full_grid(h, w, 0)
    if name == "no_anchors":
        # No 9-cells — rule's per-anchor stamp loop is empty;
        # output equals input.
        for dr, dc in _SHAPES[0]:
            g[2 + dr][2 + dc] = 4
        return g
    if name == "no_prototype":
        # No non-9 shape — rule's extractor finds nothing; per-anchor
        # stamp has no shape to apply.
        g[5][5] = 9
        g[8][9] = 9
        return g
    if name == "single_cell_prototype":
        # Prototype is one cell — stamp is trivial; no shape contrast.
        g[2][2] = 4
        g[6][6] = 9
        g[9][10] = 9
        return g
    return g
