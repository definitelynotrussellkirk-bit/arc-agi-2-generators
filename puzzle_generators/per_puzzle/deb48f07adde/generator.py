"""Generator for arc_additional_puzzles_21_set20_bundle:H135 — panel transform analogy.

Rule: full-col color-5 dividers split into 3 NxN panels. Each panel is cropped
to content. Transform t in {1..6} maps A→B (1=id, 2=cw, 3=180, 4=transpose,
5=flip-lr, 6=flip-ud). Output = t(C).

Combinatorial axes (8): panel_n, transform, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: no_dividers, identity_transform, no_C.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "deb48f07adde"
VERSION = "1.1.0"
TASK_ID = "deb48f07adde"

SUMMARY = "3 NxN panels separated by full-col color-5 dividers; B = transform(A); output = transform(C)."

INVARIANTS = [
    "background is 0",
    "two full-height color-5 divider columns split the grid into three equal NxN panels",
    "panels are square so all 6 transforms apply uniformly",
    "A and B are related by some transform t in {1..6}",
    "C contains a non-empty independent shape",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_dividers", "identity_transform", "no_C")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "panel_n":        {"type": "int", "default": "rng 4..5", "valid": "3..6"},
    "transform":      {"type": "int", "default": "rng 2..6", "valid": "1..6"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "palette_size":   {"type": "int", "default": "3", "valid": "2..4"},
    "position_bias":  {"type": "str", "default": "three_panels_5dividers",
                       "valid": "three_panels_5dividers"},
    "n_distinct_colors": {"type": "int", "default": "3", "valid": "2..4"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def _xform(cells, t, n):
    if t == 1: return list(cells)
    if t == 2: return [(c, n - 1 - r) for r, c in cells]
    if t == 3: return [(n - 1 - r, n - 1 - c) for r, c in cells]
    if t == 4: return [(c, r) for r, c in cells]
    if t == 5: return [(r, n - 1 - c) for r, c in cells]
    return [(n - 1 - r, c) for r, c in cells]


def _rand_cells(rng, n, k):
    cells = [(rng.randint(0, n - 1), rng.randint(0, n - 1))]
    seen = set(cells)
    while len(cells) < k:
        r, c = rng.choice(cells)
        dr, dc = rng.choice([(-1, 0), (1, 0), (0, -1), (0, 1)])
        nr, nc = r + dr, c + dc
        if 0 <= nr < n and 0 <= nc < n and (nr, nc) not in seen:
            cells.append((nr, nc)); seen.add((nr, nc))
    return cells


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        n = ctx.draw_int("panel_n", 4, 4)
        t = ctx.draw_int("transform", 2, 3)
    elif difficulty == "hard":
        n = ctx.draw_int("panel_n", 5, 6)
        t = ctx.draw_int("transform", 4, 6)
    else:
        n = ctx.draw_int("panel_n", 4, 5)
        t = ctx.draw_int("transform", 2, 6)
    rng = ctx.draw_rng("layout")
    h = n
    w = n * 3 + 2
    d1, d2 = n, 2 * n + 1
    color_a, color_c = rng.sample([1, 2, 3, 4, 5, 6, 7, 9], 2)

    for outer in range(40):
        g = full_grid(h, w, 0)
        for r in range(h):
            g[r][d1] = 8
            g[r][d2] = 8
        ka = rng.randint(3, max(3, n))
        cells_a = _rand_cells(rng, n, ka)
        cells_b = _xform(cells_a, t, n)
        if set(cells_a) == set(cells_b):
            continue
        kc = rng.randint(3, max(3, n))
        cells_c = _rand_cells(rng, n, kc)
        for r, c in cells_a:
            g[r][c] = color_a
        for r, c in cells_b:
            g[r][d1 + 1 + c] = color_a
        for r, c in cells_c:
            g[r][d2 + 1 + c] = color_c
        return g
    raise ValueError("could not realize 3-panel analogy in 40 attempts")


def _draw_from_degenerate(name, rng):
    n = 4
    h = n
    w = n * 3 + 2
    g = full_grid(h, w, 0)
    if name == "no_dividers":
        # Panels not separated — rule cannot identify panel boundaries.
        g[0][0] = 4; g[1][1] = 4
        g[0][5] = 4; g[1][6] = 4
        g[0][10] = 5; g[1][11] = 5
        return g
    if name == "identity_transform":
        # A = B exactly — rule infers identity, output = C unchanged.
        d1, d2 = n, 2 * n + 1
        for r in range(h):
            g[r][d1] = 8; g[r][d2] = 8
        g[0][0] = 4; g[1][1] = 4
        g[0][d1 + 1] = 4; g[1][d1 + 2] = 4
        g[0][d2 + 1] = 5; g[1][d2 + 2] = 5
        return g
    if name == "no_C":
        # Panel C empty — rule has no input to transform.
        d1, d2 = n, 2 * n + 1
        for r in range(h):
            g[r][d1] = 8; g[r][d2] = 8
        g[0][0] = 4; g[1][1] = 4
        g[0][d1 + 1] = 4; g[2][d1 + 2] = 4
        return g
    return g
