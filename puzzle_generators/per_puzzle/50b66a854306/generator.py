"""Generator for 17b:hard_113 — build dihedral equivalence matrix.

Rule: connected components sorted by column. Output NxN: 8 if shape r
and shape c match under any of the 8 dihedral transforms, else 0.

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: no_objects (no shapes → matrix is empty); single_object
(only 1 → matrix is 1x1, no contrast); all_dihedral_equivalent
(all 3 shapes are dihedral rotations of each other → matrix is
all-8, off-diagonal contrast lost).
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "50b66a854306"
VERSION = "1.1.0"
TASK_ID = "50b66a854306"

SUMMARY = "3 components in distinct colors at distinct columns; at least one pair dihedrally equivalent."

INVARIANTS = [
    "background is 0",
    "exactly 3 isolated components in distinct colors",
    "components placed at strictly distinct leftmost columns (so col-sort is unambiguous)",
    "at least one pair of components is dihedrally equivalent (so output isn't all-0 off-diagonal)",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_objects", "single_object", "all_dihedral_equivalent")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":            {"type": "int", "default": "rng 9..11", "valid": "8..14"},
    "grid_w":            {"type": "int", "default": "rng 13..15", "valid": "12..18"},
    "palette_kind":      {"type": "str", "default": "rng helpful",
                          "valid": "|".join(PALETTE_KINDS)},
    "palette_size":      {"type": "int", "default": "rng 3..3", "valid": "3..3"},
    "position_bias":     {"type": "str", "default": "three_components_distinct_columns",
                          "valid": "three_components_distinct_columns"},
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
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 13, 14)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 10, 11)
        w = ctx.draw_int("grid_w", 14, 15)
    else:
        h = ctx.draw_int("grid_h", 9, 11)
        w = ctx.draw_int("grid_w", 13, 15)
    rng = ctx.draw_rng("layout")
    base_shapes = [
        [(0, 0), (0, 1), (1, 0)],
        [(0, 0), (1, 0), (1, 1), (2, 1)],
        [(0, 0), (0, 1), (0, 2), (1, 1)],
    ]
    base = rng.choice(base_shapes)
    transformed = base
    for _ in range(rng.randint(1, 3)):
        transformed = _rotate_cw(transformed)
    if rng.random() < 0.5:
        transformed = _flip_lr(transformed)
    other = rng.choice([s for s in base_shapes if s != base])
    shapes = [base, transformed, other]
    rng.shuffle(shapes)
    palette = rng.sample([1, 2, 3, 4, 5, 6, 7, 8, 9], 3)
    for outer in range(40):
        g = full_grid(h, w, 0)
        leftmosts = []
        ok = True
        for color, shape in zip(palette, shapes):
            sh = max(r for r, _ in shape) + 1
            sw = max(c for _, c in shape) + 1
            placed = False
            for _ in range(60):
                r0 = rng.randint(0, h - sh); c0 = rng.randint(0, w - sw)
                if not _free(g, r0, c0, r0 + sh - 1, c0 + sw - 1): continue
                lc = c0 + min(c for _, c in shape)
                if lc in leftmosts: continue
                for dr, dc in shape:
                    g[r0 + dr][c0 + dc] = color
                leftmosts.append(lc); placed = True; break
            if not placed: ok = False; break
        if ok and len(set(leftmosts)) == 3:
            return g
    raise ValueError("could not place 3 shapes at distinct columns")


def _draw_from_degenerate(name, rng):
    h, w = 10, 14
    g = full_grid(h, w, 0)
    if name == "no_objects":
        return g
    if name == "single_object":
        for dr, dc in [(0, 0), (0, 1), (1, 0)]:
            g[2 + dr][3 + dc] = 4
        return g
    if name == "all_dihedral_equivalent":
        # Three rotations of L-tromino — output all-8.
        for dr, dc in [(0, 0), (0, 1), (1, 0)]:
            g[1 + dr][1 + dc] = 1
        for dr, dc in [(0, 1), (1, 0), (1, 1)]:
            g[1 + dr][6 + dc] = 2
        for dr, dc in [(0, 0), (0, 1), (1, 1)]:
            g[5 + dr][3 + dc] = 3
        return g
    return g
