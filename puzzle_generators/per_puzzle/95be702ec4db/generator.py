"""Generator for 11b:hard_75 — rotational equivalence matrix.

Rule: 3 hollow 9-frames (sorted by column) each contain a single-color
shape. Output is a 3x3 matrix where cell (r,c) is 8 iff inner[r] is
rotation-equivalent to inner[c], else 0.

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: all_same_family (all 3 shapes rotation-equivalent → matrix
is all-8, no contrast across cells), all_distinct_families (no pair
matches → matrix is identity-only, off-diagonal stays 0), empty_interiors
(all 3 frames have no interior shape → matrix collapses to "everything
matches everything").
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "95be702ec4db"
VERSION = "1.1.0"
TASK_ID = "95be702ec4db"
SUMMARY = "3 hollow 9-frames at distinct cols, each with a single-color inner shape."

INVARIANTS = [
    "background is 0",
    "exactly 3 hollow 9-frames with the same interior dimensions",
    "each frame's interior contains a single non-bg, non-9 color shape",
    "frames are placed at distinct (and well-separated) column positions",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("all_same_family", "all_distinct_families", "empty_interiors")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..10", "valid": "7..14"},
    "grid_w":         {"type": "int", "default": "rng 17..18", "valid": "15..22"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "palette_size":   {"type": "int", "default": "3", "valid": "3..3"},
    "position_bias":  {"type": "str", "default": "three_9_frames",
                       "valid": "three_9_frames"},
    "n_distinct_colors": {"type": "int", "default": "3", "valid": "3..3"},
    "density":        {"type": "str", "default": "fixed_layout", "valid": "fixed_layout"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


_SHAPE_FAMILIES = [
    [
        [(0, 0), (0, 1), (1, 0)],
        [(0, 0), (0, 1), (1, 1)],
        [(0, 1), (1, 0), (1, 1)],
        [(0, 0), (1, 0), (1, 1)],
    ],
    [
        [(0, 0), (1, 0), (1, 1), (2, 1)],
        [(0, 1), (0, 2), (1, 0), (1, 1)],
    ],
    [
        [(0, 1), (1, 0), (1, 1), (1, 2), (2, 1)],
    ],
    [
        [(0, 0), (0, 1), (0, 2), (1, 0)],
        [(0, 0), (0, 1), (1, 1), (2, 1)],
        [(0, 1), (1, 0), (1, 1), (1, 2)],
        [(0, 0), (1, 0), (1, 1), (2, 0)],
    ],
]


def _draw_frame(g, r0, c0, fh, fw):
    for c in range(c0, c0 + fw): g[r0][c] = 9; g[r0 + fh - 1][c] = 9
    for r in range(r0, r0 + fh): g[r][c0] = 9; g[r][c0 + fw - 1] = 9


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 8, 8)
        w = ctx.draw_int("grid_w", 17, 17)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 10, 13)
        w = ctx.draw_int("grid_w", 18, 21)
    else:
        h = ctx.draw_int("grid_h", 8, 10)
        w = ctx.draw_int("grid_w", 17, 18)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    fh = 5; fw = 5
    starts = [0, 6, 12]
    r0 = rng.randint(1, max(1, h - fh - 1))
    palette = rng.sample([1, 2, 3, 4, 5, 6, 7, 8], 3)
    for c0, color in zip(starts, palette):
        _draw_frame(g, r0, c0, fh, fw)
        family = rng.choice(_SHAPE_FAMILIES)
        shape = rng.choice(family)
        sh = max(r for r, _ in shape) + 1
        sw = max(c for _, c in shape) + 1
        ir = r0 + 1 + rng.randint(0, fh - 2 - sh)
        ic = c0 + 1 + rng.randint(0, fw - 2 - sw)
        for dr, dc in shape:
            g[ir + dr][ic + dc] = color
    return g


def _draw_from_degenerate(name, rng):
    h, w = 9, 17
    g = full_grid(h, w, 0)
    fh, fw = 5, 5
    r0 = 1
    starts = [0, 6, 12]
    for c0 in starts:
        _draw_frame(g, r0, c0, fh, fw)
    if name == "all_same_family":
        # All 3 inner shapes are rotation-equivalent (same family
        # of L-tromino) → matrix is all-8, no contrast.
        family = _SHAPE_FAMILIES[0]
        for c0, color, shape in zip(starts, [1, 2, 3], family[:3]):
            for dr, dc in shape:
                g[r0 + 1 + dr][c0 + 1 + dc] = color
        return g
    if name == "all_distinct_families":
        # No pair matches under rotation → matrix is identity-only.
        for c0, color, family in zip(starts, [1, 2, 3], _SHAPE_FAMILIES[:3]):
            shape = family[0]
            for dr, dc in shape:
                g[r0 + 1 + dr][c0 + 1 + dc] = color
        return g
    if name == "empty_interiors":
        # No inner shapes — all "shapes" are empty; rule's matcher
        # treats them all equal → matrix all-8.
        return g
    return g
