"""Generator for 12b:m78 — recolor canvas via two-row legend.

Rule: rows 0 and 1 hold a paired-color legend (source -> target where
both are non-bg in the same column). Row 2 is a gap. Body cells in
rows 3+ get recolored: source -> target where mapping exists, else
keep value (the rule's `t10-alist-ref` returns v if no match).

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: empty_legend (rows 0/1 are all bg → mapping is empty,
rule's recolor is identity), identity_legend (src == tgt for every
column → rule applies identity, no visible change), no_body_shapes
(rows 3+ are all bg → rule has nothing to recolor, output equals
input).
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "69cab6228fdc"
VERSION = "1.1.0"
TASK_ID = "69cab6228fdc"

SUMMARY = "2-row paired-color legend at top + gap row + body using mapped source colors."

INVARIANTS = [
    "background is 0",
    "rows 0 and 1 hold a paired-color legend at 2-3 distinct columns",
    "row 2 is a gap (all bg)",
    "body (rows 3+) holds 2-4 small shapes using legend source colors",
    "source and target colors are pairwise distinct, all non-bg",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("empty_legend", "identity_legend", "no_body_shapes")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":            {"type": "int", "default": "rng 10..12", "valid": "9..14"},
    "grid_w":            {"type": "int", "default": "rng 10..12", "valid": "9..14"},
    "n_pairs":           {"type": "int", "default": "rng 2..3", "valid": "2..4"},
    "n_shapes":          {"type": "int", "default": "rng 2..4", "valid": "1..5"},
    "palette_kind":      {"type": "str", "default": "rng helpful",
                          "valid": "|".join(PALETTE_KINDS)},
    "palette_size":      {"type": "int", "default": "rng 4..6", "valid": "4..8"},
    "position_bias":     {"type": "str", "default": "legend_at_top",
                          "valid": "legend_at_top"},
    "n_distinct_colors": {"type": "int", "default": "rng 4..6", "valid": "4..8"},
    "density":           {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":           {"type": "str", "default": "alias for palette_kind",
                          "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


_SHAPES = [
    [(0, 0), (0, 1), (1, 0)],
    [(0, 0), (1, 0), (1, 1)],
    [(0, 0), (0, 1), (1, 1)],
    [(0, 0), (1, 0), (1, 1), (2, 1)],
]


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
        h = ctx.draw_int("grid_h", 10, 10)
        w = ctx.draw_int("grid_w", 10, 10)
        n_pairs_lo, n_pairs_hi = 2, 2
        n_shapes_lo, n_shapes_hi = 2, 3
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 12, 12)
        w = ctx.draw_int("grid_w", 12, 12)
        n_pairs_lo, n_pairs_hi = 3, 3
        n_shapes_lo, n_shapes_hi = 3, 4
    else:
        h = ctx.draw_int("grid_h", 10, 12)
        w = ctx.draw_int("grid_w", 10, 12)
        n_pairs_lo, n_pairs_hi = 2, 3
        n_shapes_lo, n_shapes_hi = 2, 4
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    n_pairs = rng.randint(n_pairs_lo, n_pairs_hi)
    palette = rng.sample([1, 2, 3, 4, 5, 6, 7, 8, 9], 2 * n_pairs)
    sources = palette[:n_pairs]
    targets = palette[n_pairs:]
    legend_cols = rng.sample(range(0, w), n_pairs)
    for col, src, tgt in zip(legend_cols, sources, targets):
        g[0][col] = src
        g[1][col] = tgt
    n_shapes = rng.randint(n_shapes_lo, n_shapes_hi)
    for _ in range(n_shapes):
        src_color = rng.choice(sources)
        shape = rng.choice(_SHAPES)
        sh = max(r for r, _ in shape) + 1
        sw = max(c for _, c in shape) + 1
        for _ in range(40):
            r0 = rng.randint(4, h - sh); c0 = rng.randint(0, w - sw)
            if not _free(g, r0, c0, r0 + sh - 1, c0 + sw - 1): continue
            for dr, dc in shape:
                g[r0 + dr][c0 + dc] = src_color
            break
    return g


def _draw_from_degenerate(name, rng):
    h, w = 11, 11
    g = full_grid(h, w, 0)
    if name == "empty_legend":
        # Rows 0/1 are all bg → mapping empty; rule's recolor is identity.
        for dr, dc in [(0, 0), (0, 1), (1, 0)]:
            g[5 + dr][3 + dc] = 4
        for dr, dc in [(0, 0), (1, 0), (1, 1)]:
            g[7 + dr][7 + dc] = 6
        return g
    if name == "identity_legend":
        # src == tgt at every legend column → rule applies identity.
        g[0][1] = 4; g[1][1] = 4
        g[0][5] = 6; g[1][5] = 6
        for dr, dc in [(0, 0), (0, 1), (1, 0)]:
            g[5 + dr][3 + dc] = 4
        for dr, dc in [(0, 0), (1, 0), (1, 1)]:
            g[7 + dr][7 + dc] = 6
        return g
    if name == "no_body_shapes":
        # Body rows 3+ are bg → rule has nothing to recolor; output = input.
        g[0][1] = 4; g[1][1] = 7
        g[0][5] = 6; g[1][5] = 8
        return g
    return g
