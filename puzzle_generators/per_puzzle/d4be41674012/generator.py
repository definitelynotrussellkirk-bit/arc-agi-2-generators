"""Generator for arc_puzzle_bank_21_set16_bundle:medium_p04 — hole-count packing.

Rule: each connected component is cropped to its bbox; hole-count is the
number of enclosed-zero regions inside the crop. Sort components by
(hole_count asc, area asc, color asc); pack crops left-to-right with one
blank column between them.

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: no_components, all_same_holes, single_component.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "d4be41674012"
VERSION = "1.1.0"
TASK_ID = "d4be41674012"

SUMMARY = "3 isolated components with 0, 1, and 2 enclosed holes; output packed left-to-right by ascending hole count."

INVARIANTS = [
    "background is 0",
    "exactly 3 isolated 4-connected components",
    "each component has a distinct enclosed-hole count drawn from {0, 1, 2}",
    "component colors are sampled distinctly from {1..9}",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_components", "all_same_holes", "single_component")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 11..14", "valid": "10..16"},
    "grid_w":         {"type": "int", "default": "rng 14..18", "valid": "12..20"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "palette_size":   {"type": "int", "default": "3", "valid": "2..4"},
    "position_bias":  {"type": "str", "default": "three_components_distinct_holes",
                       "valid": "three_components_distinct_holes"},
    "n_distinct_colors": {"type": "int", "default": "3", "valid": "2..4"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def _free(g, r1, c1, r2, c2):
    h, w = len(g), len(g[0])
    if r1 < 0 or c1 < 0 or r2 >= h or c2 >= w: return False
    for r in range(max(0, r1 - 1), min(h, r2 + 2)):
        for c in range(max(0, c1 - 1), min(w, c2 + 2)):
            if g[r][c] != 0: return False
    return True


def _solid(rng, color):
    sh, sw = rng.choice([(2, 2), (2, 3), (3, 2)])
    return [(r, c, color) for r in range(sh) for c in range(sw)], sh, sw


def _ring(rng, color):
    sh, sw = rng.choice([(3, 3), (3, 4), (4, 3)])
    cells = []
    for r in range(sh):
        for c in range(sw):
            if r in (0, sh - 1) or c in (0, sw - 1):
                cells.append((r, c, color))
    return cells, sh, sw


def _double_ring(rng, color):
    sh, sw = rng.choice([(3, 5), (3, 6)])
    cells = []
    if sw == 5:
        holes = {(1, 1), (1, 3)}
    else:
        holes = {(1, 1), (1, 4)}
    for r in range(sh):
        for c in range(sw):
            is_perim = (r in (0, sh - 1) or c in (0, sw - 1))
            middle = (r == 1 and 0 < c < sw - 1)
            if is_perim or (middle and (r, c) not in holes):
                cells.append((r, c, color))
    return cells, sh, sw


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 11, 12)
        w = ctx.draw_int("grid_w", 14, 15)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 13, 15)
        w = ctx.draw_int("grid_w", 16, 19)
    else:
        h = ctx.draw_int("grid_h", 11, 14)
        w = ctx.draw_int("grid_w", 14, 18)
    rng = ctx.draw_rng("layout")

    builders = [_solid, _ring, _double_ring]
    rng.shuffle(builders)
    colors = rng.sample([1, 2, 3, 4, 6, 7, 8, 9], 3)

    for outer in range(40):
        g = full_grid(h, w, 0)
        ok = True
        for builder, color in zip(builders, colors):
            cells, sh, sw = builder(rng, color)
            placed = False
            for _ in range(80):
                r0 = rng.randint(0, h - sh); c0 = rng.randint(0, w - sw)
                if not _free(g, r0, c0, r0 + sh - 1, c0 + sw - 1): continue
                for dr, dc, cc in cells:
                    g[r0 + dr][c0 + dc] = cc
                placed = True
                break
            if not placed:
                ok = False
                break
        if ok:
            return g
    raise ValueError("could not place 3 isolated components in 40 attempts")


def _draw_from_degenerate(name, rng):
    h, w = 12, 15
    g = full_grid(h, w, 0)
    if name == "no_components":
        return g
    if name == "all_same_holes":
        # All 3 components are solid (hole count = 0) — sort tie-break ambiguous.
        for r in range(2):
            for c in range(2): g[1 + r][1 + c] = 4
        for r in range(2):
            for c in range(2): g[1 + r][6 + c] = 5
        for r in range(2):
            for c in range(2): g[1 + r][11 + c] = 6
        return g
    if name == "single_component":
        # Only one component — rule's pack is trivial.
        for r in range(2, 5):
            for c in range(5, 8): g[r][c] = 4
        return g
    return g
