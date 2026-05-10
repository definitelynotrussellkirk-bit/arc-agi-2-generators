"""Generator for arc_puzzle_bank_eleventh21:M76 — stamp prototype at every target.

Rule: 8 + 3-blob is the prototype (8 = anchor of prototype, 3 = shape
cells). 1-cells are targets. Output: empty grid + prototype's 3-cells
stamped at each target (target = where 8 lands).

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: no_prototype, no_targets, target_oob.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid
from puzzle_generators.helpers.blobs import grow_blob

GENERATOR_ID = "b87adf923da8"
VERSION = "1.1.0"
TASK_ID = "b87adf923da8"
SUMMARY = "Prototype = 8-anchor + 3-blob (small) + 1-3 single 1-targets."

INVARIANTS = [
    "background is 0",
    "exactly one 8-cell adjacent to a small 3-blob (prototype)",
    "1-3 single 1-cells with room around to stamp the prototype",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_prototype", "no_targets", "target_oob")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..11", "valid": "7..14"},
    "grid_w":         {"type": "int", "default": "rng 9..12", "valid": "8..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "palette_size":   {"type": "int", "default": "3", "valid": "3..3"},
    "position_bias":  {"type": "str", "default": "prototype_top_left_targets_scattered",
                       "valid": "prototype_top_left_targets_scattered"},
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
        w = ctx.draw_int("grid_w", 9, 10)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 11, 13)
        w = ctx.draw_int("grid_w", 12, 14)
    else:
        h = ctx.draw_int("grid_h", 8, 11)
        w = ctx.draw_int("grid_w", 9, 12)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    g[1][1] = 8
    proto_3 = [(1, 2), (2, 1), (2, 2)]
    for r, c in proto_3:
        if 0 <= r < h and 0 <= c < w:
            g[r][c] = 3
    used = {(1, 1)} | set(proto_3)
    n_targets = rng.randint(1, 3)
    proto_extent = 2
    for _ in range(n_targets):
        for _ in range(40):
            r = rng.randint(3, h - proto_extent - 1)
            c = rng.randint(0, w - proto_extent - 1)
            stamp = {(r, c)}
            for ar2, ac2 in proto_3:
                stamp.add((r + ar2 - 1, c + ac2 - 1))
            if any(g[rr][cc] != 0 for rr, cc in stamp):
                continue
            g[r][c] = 1
            used |= stamp
            break
    return g


def _draw_from_degenerate(name, rng):
    h, w = 9, 10
    g = full_grid(h, w, 0)
    if name == "no_prototype":
        # 1-targets but no 8/3 prototype — rule has no shape to stamp.
        g[5][3] = 1; g[6][7] = 1
        return g
    if name == "no_targets":
        # Prototype but no 1-targets — rule has no positions to stamp at.
        g[1][1] = 8
        for r, c in [(1, 2), (2, 1), (2, 2)]: g[r][c] = 3
        return g
    if name == "target_oob":
        # Prototype + a 1-target placed near the corner so the
        # full stamp would extend off-grid — rule's stamp region
        # is undefined.
        g[1][1] = 8
        for r, c in [(1, 2), (2, 1), (2, 2)]: g[r][c] = 3
        g[h - 1][w - 1] = 1
        return g
    return g
