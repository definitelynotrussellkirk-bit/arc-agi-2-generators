"""Generator for 21b:hard_142 — build dihedral equivalence matrix.

Rule: connected components sorted by (row, col). Output is NxN where
[i][j] = 8 iff shape i equals shape j under any of the 8 dihedral
symmetries (4 rotations + 4 reflections).

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: no_objects (no shapes → matrix is empty); single_object
(one shape → matrix is 1x1 self-equivalent, no contrast);
all_dihedral_equivalent (all 3 shapes belong to the same dihedral
class → output is all-8, off-diagonal contrast lost).
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "185447d509d8"
VERSION = "1.1.0"
TASK_ID = "185447d509d8"
SUMMARY = "3 components in distinct colors; one pair dihedrally equivalent."

INVARIANTS = [
    "background is 0",
    "exactly 3 isolated components in distinct colors",
    "at least one pair is dihedrally equivalent",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_objects", "single_object", "all_dihedral_equivalent")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":            {"type": "int", "default": "rng 8..10", "valid": "7..14"},
    "grid_w":            {"type": "int", "default": "rng 13..15", "valid": "12..18"},
    "palette_kind":      {"type": "str", "default": "rng helpful",
                          "valid": "|".join(PALETTE_KINDS)},
    "palette_size":      {"type": "int", "default": "rng 3..3", "valid": "3..3"},
    "position_bias":     {"type": "str", "default": "three_components_one_dihedral_pair",
                          "valid": "three_components_one_dihedral_pair"},
    "n_distinct_colors": {"type": "int", "default": "rng 3..3", "valid": "3..3"},
    "density":           {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":           {"type": "str", "default": "alias for palette_kind",
                          "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


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
        r0 = rng.randint(0, h - sh); c0 = rng.randint(0, w - sw)
        if not _free(g, r0, c0, r0 + sh - 1, c0 + sw - 1): continue
        for dr, dc in shape:
            g[r0 + dr][c0 + dc] = color
        return True
    return False


def _rotate_cw(shape):
    rs = [r for r, _ in shape]
    h = max(rs) + 1
    return sorted([(c, h - 1 - r) for r, c in shape])


def _flip_lr(shape):
    cs = [c for _, c in shape]
    w = max(cs) + 1
    return sorted([(r, w - 1 - c) for r, c in shape])


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("grid_w", 13, 14)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 14, 15)
    else:
        h = ctx.draw_int("grid_h", 8, 10)
        w = ctx.draw_int("grid_w", 13, 15)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    palette = rng.sample([1, 2, 3, 4, 6, 7, 8, 9], 3)
    base_shapes = [
        [(0, 0), (0, 1), (1, 0)],
        [(0, 0), (1, 0), (1, 1), (2, 1)],
        [(0, 0), (0, 1), (0, 2), (1, 1)],
    ]
    base = rng.choice(base_shapes)
    transformed = base
    n = rng.randint(1, 3)
    for _ in range(n):
        transformed = _rotate_cw(transformed)
    if rng.random() < 0.5:
        transformed = _flip_lr(transformed)
    other = rng.choice([s for s in base_shapes if s != base])
    shapes = [base, transformed, other]
    rng.shuffle(shapes)
    for color, shape in zip(palette, shapes):
        _place(g, rng, shape, color)
    return g


def _draw_from_degenerate(name, rng):
    h, w = 9, 14
    g = full_grid(h, w, 0)
    if name == "no_objects":
        # Empty grid — equivalence matrix is empty.
        return g
    if name == "single_object":
        # Only one component — matrix is 1x1, no off-diagonal contrast.
        for dr, dc in [(0, 0), (0, 1), (1, 0)]:
            g[2 + dr][3 + dc] = 4
        return g
    if name == "all_dihedral_equivalent":
        # Three rotations of the same L-tromino — output is all-8 (no contrast).
        for dr, dc in [(0, 0), (0, 1), (1, 0)]:
            g[1 + dr][1 + dc] = 1
        for dr, dc in [(0, 1), (1, 0), (1, 1)]:
            g[1 + dr][6 + dc] = 2
        for dr, dc in [(0, 0), (0, 1), (1, 1)]:
            g[5 + dr][3 + dc] = 3
        return g
    return g
