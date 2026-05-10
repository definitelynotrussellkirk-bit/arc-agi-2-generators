"""Generator for 5b:m35 — mirror component across pivot.

Rule: a single pivot cell P + a small component C. Output keeps P and
adds 3 reflections of C: across vertical axis through P, across
horizontal axis through P, and across both (180° rotation).

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: no_pivot (no color-8 pivot → rule has no axis);
no_component (pivot present but no shape to mirror → output =
input); point_symmetric_component (component is point-symmetric
about the pivot → all 4 reflections coincide, no new cells added).
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "bd24325c2939"
VERSION = "1.1.0"
TASK_ID = "bd24325c2939"
SUMMARY = "Single pivot cell + a small component whose 4-fold reflection lands in-bounds."

INVARIANTS = [
    "background is 0",
    "exactly one isolated pivot cell at (pr, pc)",
    "exactly one small connected component (color != pivot color)",
    "all 4 reflections (lr, ud, both, identity) are in-bounds and disjoint",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_pivot", "no_component", "point_symmetric_component")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":            {"type": "int", "default": "rng 9..12", "valid": "8..14"},
    "grid_w":            {"type": "int", "default": "rng 9..12", "valid": "8..14"},
    "palette_kind":      {"type": "str", "default": "rng helpful",
                          "valid": "|".join(PALETTE_KINDS)},
    "palette_size":      {"type": "int", "default": "rng 2..3", "valid": "2..3"},
    "position_bias":     {"type": "str", "default": "pivot_with_component_in_quadrant",
                          "valid": "pivot_with_component_in_quadrant"},
    "n_distinct_colors": {"type": "int", "default": "rng 2..3", "valid": "2..3"},
    "density":           {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":           {"type": "str", "default": "alias for palette_kind",
                          "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}

_SHAPES = [
    [(0, 0), (1, 0)],
    [(0, 0), (1, 0), (1, 1)],
    [(0, 0), (0, 1), (1, 0)],
    [(0, 0), (1, 0), (2, 0)],
    [(0, 0), (1, 0), (2, 0), (2, 1)],
    [(0, 0), (0, 1), (1, 1)],
]


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 9, 10)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 11, 12)
        w = ctx.draw_int("grid_w", 11, 12)
    else:
        h = ctx.draw_int("grid_h", 9, 12)
        w = ctx.draw_int("grid_w", 9, 12)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    pivot_color = 8
    colors = rng.sample([1, 2, 3, 4, 6, 7, 9], 1)
    pr = rng.randint(h // 2 - 1, h // 2 + 1)
    pc = rng.randint(w // 2 - 1, w // 2 + 1)
    g[pr][pc] = pivot_color
    for _ in range(80):
        shape = list(rng.choice(_SHAPES))
        sh = max(r for r, _ in shape) + 1
        sw = max(c for _, c in shape) + 1
        r0 = rng.randint(0, max(0, pr - sh - 1))
        c0 = rng.randint(0, max(0, pc - sw - 1))
        cells = [(r0 + dr, c0 + dc) for dr, dc in shape]
        all_cells = set()
        for r, c in cells:
            for mr, mc in (
                (r, c),
                (r, 2 * pc - c),
                (2 * pr - r, c),
                (2 * pr - r, 2 * pc - c),
            ):
                if not (0 <= mr < h and 0 <= mc < w):
                    all_cells = None; break
                if (mr, mc) == (pr, pc):
                    all_cells = None; break
                all_cells.add((mr, mc))
            if all_cells is None: break
        if all_cells is None: continue
        if len(all_cells) != 4 * len(shape): continue
        color = colors[0]
        for r, c in cells:
            g[r][c] = color
        return g
    return g


def _draw_from_degenerate(name, rng):
    h, w = 10, 10
    g = full_grid(h, w, 0)
    if name == "no_pivot":
        # No color-8 pivot — rule has no mirror axis.
        for dr, dc in [(0, 0), (1, 0), (1, 1)]:
            g[1 + dr][1 + dc] = 4
        return g
    if name == "no_component":
        # Pivot present but no other shape — output equals input.
        g[5][5] = 8
        return g
    if name == "point_symmetric_component":
        # Component is already point-symmetric about pivot → mirrors coincide.
        g[5][5] = 8
        # Place a single cell on each side of pivot at equal distance — all 4
        # mirrors collapse to those 2 cells.
        g[3][3] = 4; g[7][7] = 4
        return g
    return g
