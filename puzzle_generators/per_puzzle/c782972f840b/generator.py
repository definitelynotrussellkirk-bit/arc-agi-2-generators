"""Generator for 10b:hard_66 — build rotation-invariant shape-color relation matrix.

Rule: components sorted; output NxN: diagonal=9, same-shape+color=6,
same-shape+diff-color=4, diff-shape+same-color=2, else=0.

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: no_objects (no shapes → matrix is empty); single_object
(only 1 → matrix is 1x1 with diag=9, no off-diagonal contrast);
all_distinct (no two pairs share shape OR color → all off-diagonal
cells are 0, only diag has signal).
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "c782972f840b"
VERSION = "1.1.0"
TASK_ID = "c782972f840b"

SUMMARY = "3 isolated components mixing colors and shapes."

INVARIANTS = [
    "background is 0",
    "exactly 3 isolated components",
    "at least one pair shares color or rotation; output not all-0 off-diagonal",
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
    "position_bias":     {"type": "str", "default": "three_components_shape_color_mix",
                          "valid": "three_components_shape_color_mix"},
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
    if rng.random() < 0.5:
        palette[1] = palette[0]
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
    h, w = 10, 13
    g = full_grid(h, w, 0)
    if name == "no_objects":
        return g
    if name == "single_object":
        for dr, dc in [(0, 0), (0, 1), (1, 0)]:
            g[3 + dr][4 + dc] = 4
        return g
    if name == "all_distinct":
        # Three distinct shapes in three distinct colors — no shared shape OR color.
        for dr, dc in [(0, 0), (0, 1), (1, 0)]:
            g[1 + dr][1 + dc] = 1
        for dr, dc in [(0, 0), (0, 1), (1, 0), (1, 1)]:
            g[1 + dr][6 + dc] = 2
        for dr, dc in [(0, 0), (0, 1), (0, 2), (0, 3)]:
            g[5 + dr][3 + dc] = 3
        return g
    return g
