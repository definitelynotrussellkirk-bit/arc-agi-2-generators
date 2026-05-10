"""Generator for arc_additional_puzzles_21_set16_bundle:M111 — N×N dihedral-equivalence matrix.

Rule: each object (sorted top-left) becomes a binary mask. Output is
N×N matrix where cell (r, c) = 8 if mask r is some dihedral transform
of mask c, else 0.

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: no_objects (grid is all bg → rule's matrix has size 0),
single_object (only one object → 1x1 trivial matrix, no contrast),
all_dihedral_equivalent (every object is dihedrally equivalent → output
matrix is all 8s, no contrast).
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, paint_at
from puzzle_generators.helpers.palette import random_palette
from puzzle_generators.helpers.blobs import bbox_overlaps

GENERATOR_ID = "1120fd69b838"
VERSION = "1.1.0"
TASK_ID = "1120fd69b838"
SUMMARY = "3 connected objects: 2 share a base shape (any rotation), 1 has a different cell-count base shape."

INVARIANTS = [
    "background is 0",
    "exactly 3 4-connected non-bg objects, each a distinct color",
    "2 objects share the same base shape (or some dihedral transform of it)",
    "the 3rd object has a different cell-count → never dihedral-equivalent to the others",
    "objects don't touch each other",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_objects", "single_object", "all_dihedral_equivalent")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":            {"type": "int", "default": "rng 8..12", "valid": "7..14"},
    "grid_w":            {"type": "int", "default": "rng 12..16", "valid": "10..18"},
    "palette_kind":      {"type": "str", "default": "rng helpful",
                          "valid": "|".join(PALETTE_KINDS)},
    "palette_size":      {"type": "int", "default": "rng 3..3", "valid": "3..3"},
    "position_bias":     {"type": "str", "default": "two_dihedral_plus_outlier",
                          "valid": "two_dihedral_plus_outlier"},
    "n_distinct_colors": {"type": "int", "default": "rng 3..3", "valid": "3..3"},
    "density":           {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":           {"type": "str", "default": "alias for palette_kind",
                          "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}

_3CELL_VARIANTS = [
    [(0, 0), (0, 1), (1, 0)],
    [(0, 0), (0, 1), (1, 1)],
    [(0, 0), (1, 0), (1, 1)],
    [(0, 1), (1, 0), (1, 1)],
]
_4CELL_VARIANTS = [
    [(0, 0), (0, 1), (1, 0), (1, 1)],
    [(0, 0), (0, 1), (0, 2), (1, 1)],
    [(0, 0), (1, 0), (1, 1), (2, 1)],
    [(0, 0), (0, 1), (0, 2), (0, 3)],
]


def _bbox(cells):
    rs = [r for r, _ in cells]; cs = [c for _, c in cells]
    return max(rs) - min(rs) + 1, max(cs) - min(cs) + 1


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("grid_w", 12, 13)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 11, 12)
        w = ctx.draw_int("grid_w", 15, 16)
    else:
        h = ctx.draw_int("grid_h", 8, 12)
        w = ctx.draw_int("grid_w", 12, 16)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    palette = list(random_palette(rng, 3))
    a_shape = rng.choice(_3CELL_VARIANTS)
    b_shape = rng.choice(_4CELL_VARIANTS)
    shapes = [a_shape, rng.choice(_3CELL_VARIANTS), b_shape]
    rng.shuffle(shapes)
    placed: list[tuple[int, int, int, int]] = []
    for shape, color in zip(shapes, palette):
        sh, sw = _bbox(shape)
        for _ in range(80):
            r0 = rng.randint(0, h - sh)
            c0 = rng.randint(0, w - sw)
            bb_pad = (r0 - 1, c0 - 1, r0 + sh, c0 + sw)
            if any(bbox_overlaps(bb_pad, p) for p in placed): continue
            paint_at(g, r0, c0, shape, color)
            placed.append((r0, c0, r0 + sh - 1, c0 + sw - 1))
            break
    return g


def _draw_from_degenerate(name, rng):
    h, w = 9, 14
    g = full_grid(h, w, 0)
    if name == "no_objects":
        # No objects — rule's matrix has size 0.
        return g
    if name == "single_object":
        # Only one object — trivial 1x1 matrix.
        for dr, dc in [(0, 0), (0, 1), (1, 0)]:
            g[3 + dr][5 + dc] = 4
        return g
    if name == "all_dihedral_equivalent":
        # Three L-trominoes — all dihedral equivalents; output matrix
        # is all 8s.
        for dr, dc in [(0, 0), (0, 1), (1, 0)]:
            g[1 + dr][1 + dc] = 4
        for dr, dc in [(0, 0), (1, 0), (1, 1)]:
            g[1 + dr][6 + dc] = 6
        for dr, dc in [(0, 1), (1, 0), (1, 1)]:
            g[1 + dr][11 + dc] = 8   # all are L variants
        return g
    return g
