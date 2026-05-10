"""Generator for 15b:m101 — stamp prototype at all anchors.

Rule: a small non-9 prototype blob + several 9-anchor cells. Output:
empty grid + prototype stamped at each anchor (anchor = top-left of stamp).

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: no_prototype, no_anchors, anchor_oob.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid
from puzzle_generators.helpers.blobs import grow_blob

GENERATOR_ID = "70c1f7fc5056"
VERSION = "1.1.0"
TASK_ID = "70c1f7fc5056"
SUMMARY = "1 small non-9 prototype + 1-2 9-anchors with room to stamp."

INVARIANTS = [
    "background is 0",
    "exactly one non-9 prototype blob of size 2-4",
    "1-2 9-anchor single cells, each with room for prototype stamp",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_prototype", "no_anchors", "anchor_oob")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..11", "valid": "7..14"},
    "grid_w":         {"type": "int", "default": "rng 9..12", "valid": "8..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "palette_size":   {"type": "int", "default": "2", "valid": "2..2"},
    "position_bias":  {"type": "str", "default": "prototype_plus_9_anchors",
                       "valid": "prototype_plus_9_anchors"},
    "n_distinct_colors": {"type": "int", "default": "2", "valid": "2..2"},
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
        w = ctx.draw_int("grid_w", 9, 10)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 11, 13)
        w = ctx.draw_int("grid_w", 12, 14)
    else:
        h = ctx.draw_int("grid_h", 8, 11)
        w = ctx.draw_int("grid_w", 9, 12)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    used: set[tuple[int, int]] = set()
    template = grow_blob(rng, h, w, used, rng.randint(2, 4), max_attempts=80)
    if template is None:
        return g
    rs = sorted(r for r, _ in template)
    cs = sorted(c for _, c in template)
    tpl_h = rs[-1] - rs[0] + 1
    tpl_w = cs[-1] - cs[0] + 1
    color = rng.choice([2, 3, 4, 5, 6, 7, 8])
    for r, c in template:
        g[r][c] = color
    used |= template
    n_anchors = rng.randint(1, 2)
    for _ in range(n_anchors):
        for _ in range(40):
            ar = rng.randint(0, h - tpl_h)
            ac = rng.randint(0, w - tpl_w)
            stamp = {(ar + (r - rs[0]), ac + (c - cs[0])) for r, c in template}
            if any(g[rr][cc] != 0 for rr, cc in stamp):
                continue
            g[ar][ac] = 9
            break
    return g


def _draw_from_degenerate(name, rng):
    h, w = 9, 10
    g = full_grid(h, w, 0)
    if name == "no_prototype":
        # 9-anchors but no prototype blob — rule has no shape to stamp.
        g[2][3] = 9; g[6][7] = 9
        return g
    if name == "no_anchors":
        # Prototype but no 9-anchors — rule has no stamp positions.
        for r, c in [(3, 3), (3, 4), (4, 3)]: g[r][c] = 5
        return g
    if name == "anchor_oob":
        # Prototype + anchor placed near corner so the stamp would
        # extend past the grid — rule's full-stamp region is undefined.
        for r, c in [(0, 0), (0, 1), (1, 0)]: g[r][c] = 5
        g[h - 1][w - 1] = 9
        return g
    return g
