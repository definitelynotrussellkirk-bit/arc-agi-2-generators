"""Generator for arc_additional_puzzles_21_set10_bundle:H66 — rotational equivalence matrix.

Rule: every non-zero connected component (color-separated) is cropped
to a binary bounding box; components are ordered by top-left position.
Output is N×N: 1 on diagonal, 2 if two shapes are equal up to rotation,
3 otherwise.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "da7aac74dddc"
VERSION = "1.1.0"
TASK_ID = "da7aac74dddc"

SUMMARY = "3 isolated components (mixed colors); output 3×3 rotation-equivalence matrix."

INVARIANTS = [
    "background is 0",
    "exactly 3 isolated connected components in colors {1..9}",
    "components are 4-connected and color-separated",
    "at least one pair is rotation-equivalent OR at least one pair is unrelated (so output isn't trivially all-1)",
]

AXES = {
    "grid_h": {"type": "int", "default": "rng 9..11", "valid": "8..14"},
    "grid_w": {"type": "int", "default": "rng 11..13", "valid": "10..16"},
}


_SHAPES = [
    [(0, 0), (1, 0), (1, 1)],                  # L tromino
    [(0, 0), (0, 1), (1, 0)],                  # mirror L tromino
    [(0, 0), (0, 1), (0, 2), (1, 1)],          # T tetromino
    [(0, 0), (1, 0), (1, 1), (2, 1)],          # S tetromino
    [(0, 0), (0, 1), (1, 0), (1, 1)],          # 2x2 square
    [(0, 0), (0, 1), (0, 2)],                  # I tromino
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
    h = ctx.draw_int("grid_h", 9, 11)
    w = ctx.draw_int("grid_w", 11, 13)
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
