"""Generator for 16b:m110 — select by most frequent legend color and scale2.

Rule: row 0 holds a multi-color legend; the most frequent non-bg color
is the key. The body component of that color is cropped and scaled 2x.

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: tied_majority (≥2 legend colors share max frequency →
"most frequent" is ambiguous, tie-break decides), no_legend (row 0
is empty → rule's frequency selector returns nothing), no_majority_body
(majority color has no body component → rule's selector finds no
body shape to scale).
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "0fcb77c31d06"
VERSION = "1.1.0"
TASK_ID = "0fcb77c31d06"
SUMMARY = "Top row legend with strict-majority color + body shapes (one in that color)."

INVARIANTS = [
    "background is 0",
    "row 0 has 4-6 cells in 2-3 distinct colors with one strict majority",
    "body (rows 1+) has 2-3 multi-cell components, one in the majority color",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("tied_majority", "no_legend", "no_majority_body")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":            {"type": "int", "default": "rng 8..10", "valid": "7..14"},
    "grid_w":            {"type": "int", "default": "rng 10..13", "valid": "9..14"},
    "palette_kind":      {"type": "str", "default": "rng helpful",
                          "valid": "|".join(PALETTE_KINDS)},
    "palette_size":      {"type": "int", "default": "rng 3..3", "valid": "3..3"},
    "position_bias":     {"type": "str", "default": "row0_legend_plus_body_shapes",
                          "valid": "row0_legend_plus_body_shapes"},
    "n_distinct_colors": {"type": "int", "default": "rng 3..3", "valid": "3..3"},
    "density":           {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":           {"type": "str", "default": "alias for palette_kind",
                          "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}

_SHAPES = [
    [(0, 0), (1, 0), (1, 1)],
    [(0, 0), (0, 1), (1, 0)],
    [(0, 0), (0, 1), (0, 2), (1, 1)],
    [(0, 0), (1, 0), (1, 1), (2, 1)],
    [(0, 0), (0, 1), (1, 0), (1, 1)],
    [(0, 0), (1, 0), (2, 0), (2, 1)],
]


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
        r0 = rng.randint(2, h - sh); c0 = rng.randint(0, w - sw)
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
        h = ctx.draw_int("grid_h", 8, 8)
        w = ctx.draw_int("grid_w", 10, 11)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 10, 10)
        w = ctx.draw_int("grid_w", 12, 13)
    else:
        h = ctx.draw_int("grid_h", 8, 10)
        w = ctx.draw_int("grid_w", 10, 13)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    legend_palette = rng.sample([2, 3, 4, 5, 6, 7, 8, 9], 3)
    majority = legend_palette[0]
    others = legend_palette[1:]
    n_majority = rng.randint(3, 4)
    n_other = rng.randint(1, 2)
    n_other2 = rng.randint(1, 2)
    legend_seq = [majority] * n_majority + [others[0]] * n_other + [others[1]] * n_other2
    cols_for_legend = rng.sample(range(0, w), len(legend_seq))
    for col, color in zip(cols_for_legend, legend_seq):
        g[0][col] = color
    for color in legend_palette:
        _place(g, rng, rng.choice(_SHAPES), color)
    return g


def _draw_from_degenerate(name, rng):
    h, w = 9, 11
    g = full_grid(h, w, 0)
    if name == "tied_majority":
        # Two legend colors share max frequency — "most frequent" is
        # ambiguous; tie-break decides.
        g[0][0] = 4; g[0][1] = 4; g[0][2] = 4
        g[0][4] = 6; g[0][5] = 6; g[0][6] = 6
        for dr, dc in [(0, 0), (0, 1), (1, 0)]:
            g[3 + dr][2 + dc] = 4
        for dr, dc in [(0, 0), (1, 0), (1, 1)]:
            g[3 + dr][7 + dc] = 6
        return g
    if name == "no_legend":
        # Row 0 empty — rule's frequency selector returns nothing.
        for dr, dc in [(0, 0), (0, 1), (1, 0)]:
            g[3 + dr][2 + dc] = 4
        for dr, dc in [(0, 0), (1, 0), (1, 1)]:
            g[6 + dr][7 + dc] = 6
        return g
    if name == "no_majority_body":
        # Majority color has no body component — rule's selector finds
        # no shape to scale.
        g[0][0] = 4; g[0][1] = 4; g[0][2] = 4
        g[0][4] = 6
        for dr, dc in [(0, 0), (0, 1), (1, 0)]:
            g[3 + dr][2 + dc] = 6
        return g
    return g
