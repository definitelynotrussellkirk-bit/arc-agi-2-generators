"""Generator for arc_additional_puzzles_21_set11_bundle:H74 — symmetry equivalence matrix.

Rule: every connected component is cropped (color-blind binary). Output is
N×N: 8 if two cropped shapes are equivalent under any of the 8 dihedral
transforms (rotations + reflections), 0 otherwise. Diagonal is 8 (self).

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: no_objects (no shapes → matrix is empty); single_object
(only 1 → matrix is 1x1, no off-diagonal contrast);
all_dihedral_equivalent (all 3 shapes belong to same dihedral class
→ matrix all-8, off-diagonal contrast lost).
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "60c56114260f"
VERSION = "1.1.0"
TASK_ID = "60c56114260f"

SUMMARY = "3 isolated components in distinct colors; output 3×3 dihedral-equivalence matrix."

INVARIANTS = [
    "background is 0",
    "exactly 3 isolated 4-connected components in distinct colors",
    "at least one pair is dihedrally equivalent OR at least one pair is unrelated (so output isn't trivially uniform)",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_objects", "single_object", "all_dihedral_equivalent")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":            {"type": "int", "default": "rng 9..11", "valid": "8..14"},
    "grid_w":            {"type": "int", "default": "rng 12..14", "valid": "11..16"},
    "palette_kind":      {"type": "str", "default": "rng helpful",
                          "valid": "|".join(PALETTE_KINDS)},
    "palette_size":      {"type": "int", "default": "rng 3..3", "valid": "3..3"},
    "position_bias":     {"type": "str", "default": "three_components_dihedral_pair",
                          "valid": "three_components_dihedral_pair"},
    "n_distinct_colors": {"type": "int", "default": "rng 3..3", "valid": "3..3"},
    "density":           {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":           {"type": "str", "default": "alias for palette_kind",
                          "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


_SHAPES = [
    [(0, 0), (0, 1), (0, 2), (1, 0)],          # L tetromino
    [(0, 0), (1, 0), (1, 1), (2, 1)],          # S tetromino
    [(0, 0), (0, 1), (0, 2), (1, 1)],          # T tetromino
    [(0, 0), (1, 0), (1, 1)],                  # L tromino
    [(0, 0), (0, 1), (1, 0), (1, 1)],          # 2x2 square
    [(0, 0), (0, 1), (0, 2), (0, 3)],          # I tetromino
]


def _rotate_cw(shape):
    rs = [r for r, _ in shape]
    h = max(rs) + 1
    return sorted([(c, h - 1 - r) for r, c in shape])


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
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 12, 13)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 10, 11)
        w = ctx.draw_int("grid_w", 13, 14)
    else:
        h = ctx.draw_int("grid_h", 9, 11)
        w = ctx.draw_int("grid_w", 12, 14)
    rng = ctx.draw_rng("layout")

    base = rng.choice(_SHAPES)
    rot = base
    for _ in range(rng.randint(1, 3)):
        rot = _rotate_cw(rot)
    other = rng.choice([s for s in _SHAPES if s != base])
    palette = rng.sample([1, 2, 3, 4, 6, 7, 8, 9], 3)
    shapes_colors = list(zip([base, rot, other], palette))
    rng.shuffle(shapes_colors)

    for outer in range(40):
        g = full_grid(h, w, 0)
        ok = True
        for shape, color in shapes_colors:
            sh = max(r for r, _ in shape) + 1
            sw = max(c for _, c in shape) + 1
            placed = False
            for _ in range(60):
                r0 = rng.randint(0, h - sh); c0 = rng.randint(0, w - sw)
                if not _free(g, r0, c0, r0 + sh - 1, c0 + sw - 1): continue
                for dr, dc in shape:
                    g[r0 + dr][c0 + dc] = color
                placed = True; break
            if not placed: ok = False; break
        if ok:
            return g
    raise ValueError("could not place 3 isolated shapes in 40 attempts")


def _draw_from_degenerate(name, rng):
    h, w = 10, 13
    g = full_grid(h, w, 0)
    if name == "no_objects":
        return g
    if name == "single_object":
        for dr, dc in [(0, 0), (0, 1), (1, 0)]:
            g[3 + dr][4 + dc] = 4
        return g
    if name == "all_dihedral_equivalent":
        # Three rotations of L-tromino — output is all-8.
        for dr, dc in [(0, 0), (0, 1), (1, 0)]:
            g[1 + dr][1 + dc] = 1
        for dr, dc in [(0, 1), (1, 0), (1, 1)]:
            g[1 + dr][6 + dc] = 2
        for dr, dc in [(0, 0), (0, 1), (1, 1)]:
            g[5 + dr][3 + dc] = 3
        return g
    return g
