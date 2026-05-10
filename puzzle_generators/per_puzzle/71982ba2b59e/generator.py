"""Generator for 6b:hard_40 — shape-color relation matrix.

Rule: connected components sorted by (row, col). Output NxN: cell
(r, c) = colors[r] on diagonal; 8 if shape-rotation-equivalent;
6 if same color; 0 otherwise.

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: no_objects (empty grid → no rows/cols);
single_object (1 component → 1x1 trivial output);
all_distinct (3 distinct colors + 3 distinct shapes → output is
all-0 except diagonal — no off-diagonal signal).
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "71982ba2b59e"
VERSION = "1.1.0"
TASK_ID = "71982ba2b59e"

SUMMARY = "3 isolated components; mix of colors and rotation-equivalences."

INVARIANTS = [
    "background is 0",
    "exactly 3 isolated components",
    "at least one pair shares color OR is rotation-equivalent (so output isn't all-0)",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_objects", "single_object", "all_distinct")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":            {"type": "int", "default": "rng 9..11", "valid": "8..14"},
    "grid_w":            {"type": "int", "default": "rng 12..14", "valid": "11..16"},
    "palette_kind":      {"type": "str", "default": "rng helpful",
                          "valid": "|".join(PALETTE_KINDS)},
    "palette_size":      {"type": "int", "default": "rng 3..3", "valid": "3..3"},
    "position_bias":     {"type": "str", "default": "three_isolated_motifs",
                          "valid": "three_isolated_motifs"},
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
    base_shapes = [
        [(0, 0), (0, 1), (1, 0)],
        [(0, 0), (1, 0), (1, 1), (2, 1)],
        [(0, 0), (0, 1), (0, 2), (1, 1)],
    ]
    base = rng.choice(base_shapes)
    rotated = base
    for _ in range(rng.randint(1, 3)):
        rotated = _rotate_cw(rotated)
    other = rng.choice([s for s in base_shapes if s != base])
    palette = rng.sample([1, 2, 3, 4, 5, 6, 7, 8, 9], 3)
    shapes_colors = list(zip([base, rotated, other], palette))
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
    raise ValueError("could not place 3 shapes")


def _draw_from_degenerate(name, rng):
    h, w = 10, 12
    g = full_grid(h, w, 0)
    if name == "no_objects":
        # Empty — no components, output is 0x0.
        return g
    if name == "single_object":
        # One component only — output is 1x1 diagonal.
        for dr, dc in [(0, 0), (0, 1), (1, 0)]:
            g[3 + dr][4 + dc] = 5
        return g
    if name == "all_distinct":
        # 3 distinct colors + 3 distinct shapes — no 8/6 off-diagonals.
        for dr, dc in [(0, 0), (0, 1), (1, 0)]:
            g[1 + dr][1 + dc] = 1
        for dr, dc in [(0, 0), (1, 0), (1, 1), (2, 1)]:
            g[1 + dr][6 + dc] = 2
        for dr, dc in [(0, 0), (0, 1), (0, 2), (1, 1)]:
            g[6 + dr][3 + dc] = 4
        return g
    return g
