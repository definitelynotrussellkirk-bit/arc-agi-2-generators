"""Generator for 12b:m81 — select area-matched component scale2.

Rule: count K = number of 1-cells in row 0. Find the component (in
rows 1+) with exactly K cells. Output is that shape cropped, scaled 2x.

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: no_match (no body component has K cells → rule's selector
finds nothing), tied_match (≥2 body components have K cells → "the
matched one" tie-break decides), no_header (row 0 empty → K=0; rule
treats as no body component matches).
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "a0444de97675"
VERSION = "1.1.0"
TASK_ID = "a0444de97675"
SUMMARY = "Top row has K isolated 1-cells; 3 body shapes with distinct sizes, one == K."

INVARIANTS = [
    "background is 0",
    "row 0 has K isolated 1-cells (no other non-bg cells in row 0)",
    "rows 1+ hold 3 multi-cell components with strictly distinct cell counts",
    "exactly one component has K cells",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_match", "tied_match", "no_header")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 9..11", "valid": "8..14"},
    "grid_w":         {"type": "int", "default": "rng 10..12", "valid": "9..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "palette_size":   {"type": "int", "default": "rng 4..5", "valid": "3..6"},
    "position_bias":  {"type": "str", "default": "header_count_plus_components",
                       "valid": "header_count_plus_components"},
    "n_distinct_colors": {"type": "int", "default": "rng 4..5", "valid": "3..6"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}

_BY_SIZE = {
    3: [[(0, 0), (0, 1), (1, 0)], [(0, 0), (1, 0), (1, 1)]],
    4: [[(0, 0), (0, 1), (1, 0), (1, 1)], [(0, 0), (1, 0), (1, 1), (2, 1)]],
    5: [[(0, 0), (0, 1), (1, 0), (1, 1), (1, 2)],
        [(0, 0), (0, 1), (0, 2), (1, 0), (1, 2)]],
    6: [[(0, 0), (0, 1), (1, 0), (1, 1), (2, 0), (2, 1)]],
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
        r0 = rng.randint(1, h - sh); c0 = rng.randint(0, w - sw)
        if not _free(g, r0, c0, r0 + sh - 1, c0 + sw - 1): continue
        for dr, dc in shape:
            g[r0 + dr][c0 + dc] = color
        return True
    return False


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 9, 9)
        w = ctx.draw_int("grid_w", 10, 10)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 11, 13)
        w = ctx.draw_int("grid_w", 12, 14)
    else:
        h = ctx.draw_int("grid_h", 9, 11)
        w = ctx.draw_int("grid_w", 10, 12)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    sizes = rng.sample([3, 4, 5, 6], 3)
    k = rng.choice(sizes)
    cols_for_ones = rng.sample(range(0, w), k)
    for c in cols_for_ones: g[0][c] = 1
    palette = rng.sample([2, 3, 4, 5, 6, 7, 8, 9], 3)
    for size, color in zip(sizes, palette):
        _place(g, rng, rng.choice(_BY_SIZE[size]), color)
    return g


def _draw_from_degenerate(name, rng):
    h, w = 10, 11
    g = full_grid(h, w, 0)
    if name == "no_match":
        # Header K=2 but no body comp has 2 cells; rule finds none.
        g[0][2] = 1; g[0][6] = 1
        for dr, dc in _BY_SIZE[3][0]: g[2 + dr][1 + dc] = 4
        for dr, dc in _BY_SIZE[5][0]: g[6 + dr][6 + dc] = 6
        return g
    if name == "tied_match":
        # K=4 and two body comps have 4 cells; "the one" is ambiguous.
        for c in range(4): g[0][c + 2] = 1
        for dr, dc in _BY_SIZE[4][0]: g[2 + dr][1 + dc] = 4
        for dr, dc in _BY_SIZE[4][1]: g[2 + dr][7 + dc] = 6
        for dr, dc in _BY_SIZE[6][0]: g[6 + dr][3 + dc] = 7
        return g
    if name == "no_header":
        # Row 0 empty — K=0; no body comp has 0 cells.
        for dr, dc in _BY_SIZE[3][0]: g[2 + dr][1 + dc] = 4
        for dr, dc in _BY_SIZE[4][0]: g[5 + dr][6 + dc] = 6
        return g
    return g
