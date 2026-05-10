"""Generator for next_b:hard_09 — scale second-smallest component 2x.

Rule: among color-3 components, sort by (size, row, col) ascending.
Pick the SECOND. Scale its cells by 2x at its bbox top-left, paint
result with color 8.

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: tied_sizes (≥2 components share a size → "second by size"
falls to row/col tie-break, output ambiguous), only_two_components
(only 2 components → second is the largest, not second-smallest;
rule's distinction collapses), single_motif (only 1 component → no
"second" to scale).
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "bd05f2963d17"
VERSION = "1.1.0"
TASK_ID = "bd05f2963d17"

SUMMARY = "3 color-3 components with strictly distinct cell counts."

INVARIANTS = [
    "background is 0",
    "exactly 3 color-3 components, isolated",
    "components have strictly distinct cell counts (so the sort is unambiguous)",
    "the 2nd-smallest component's 2x-scaled bbox fits in-bounds",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("tied_sizes", "only_two_components", "single_motif")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 11..13", "valid": "10..16"},
    "grid_w":         {"type": "int", "default": "rng 13..15", "valid": "12..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "palette_size":   {"type": "int", "default": "1", "valid": "1..1"},
    "position_bias":  {"type": "str", "default": "three_distinct_size_motifs",
                       "valid": "three_distinct_size_motifs"},
    "n_distinct_colors": {"type": "int", "default": "1", "valid": "1..1"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


_BY_SIZE = {
    3: [[(0, 0), (0, 1), (1, 0)], [(0, 0), (1, 0), (1, 1)]],
    4: [[(0, 0), (0, 1), (1, 0), (1, 1)], [(0, 0), (1, 0), (1, 1), (2, 1)]],
    5: [[(0, 0), (0, 1), (0, 2), (1, 0), (1, 2)]],
    6: [[(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2)]],
}


def _free(g, r1, c1, r2, c2):
    h, w = len(g), len(g[0])
    if r1 < 0 or c1 < 0 or r2 >= h or c2 >= w: return False
    for r in range(max(0, r1 - 1), min(h, r2 + 2)):
        for c in range(max(0, c1 - 1), min(w, c2 + 2)):
            if g[r][c] != 0: return False
    return True


def _place_or_raise(g, rng, shape, color, label, *, scale_check=False):
    h, w = len(g), len(g[0])
    sh = max(r for r, _ in shape) + 1
    sw = max(c for _, c in shape) + 1
    bound_h = sh * 2 if scale_check else sh
    bound_w = sw * 2 if scale_check else sw
    for _ in range(60):
        r0 = rng.randint(0, h - bound_h); c0 = rng.randint(0, w - bound_w)
        if not _free(g, r0, c0, r0 + sh - 1, c0 + sw - 1): continue
        for dr, dc in shape:
            g[r0 + dr][c0 + dc] = color
        return
    raise ValueError(f"could not place {label}")


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 11, 11)
        w = ctx.draw_int("grid_w", 13, 13)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 13, 16)
        w = ctx.draw_int("grid_w", 15, 17)
    else:
        h = ctx.draw_int("grid_h", 11, 13)
        w = ctx.draw_int("grid_w", 13, 15)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    sizes = sorted(rng.sample([3, 4, 5, 6], 3))
    for size in sizes:
        shape = rng.choice(_BY_SIZE[size])
        _place_or_raise(g, rng, shape, 3, f"size-{size}",
                        scale_check=(size == sizes[1]))
    return g


def _draw_from_degenerate(name, rng):
    h, w = 12, 14
    g = full_grid(h, w, 0)
    if name == "tied_sizes":
        # Two components share size 4 — "second by size" tie-break
        # falls to row/col; output ambiguous.
        for dr, dc in _BY_SIZE[4][0]: g[1 + dr][1 + dc] = 3
        for dr, dc in _BY_SIZE[4][1]: g[1 + dr][7 + dc] = 3
        for dr, dc in _BY_SIZE[6][0]: g[6 + dr][3 + dc] = 3
        return g
    if name == "only_two_components":
        # Only 2 components — second IS the largest, not "second-
        # smallest"; rule's distinction collapses.
        for dr, dc in _BY_SIZE[3][0]: g[2 + dr][2 + dc] = 3
        for dr, dc in _BY_SIZE[5][0]: g[6 + dr][7 + dc] = 3
        return g
    if name == "single_motif":
        # Only 1 component — no "second" to scale; rule fails.
        for dr, dc in _BY_SIZE[4][0]: g[3 + dr][5 + dc] = 3
        return g
    return g
