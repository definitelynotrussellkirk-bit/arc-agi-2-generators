"""Generator for 13b:m86 — recolor body via top legend.

Rule: row 0 holds source colors, row 1 holds target colors (paired
column-by-column where both are non-bg). Body cells (rows 2+) get
recolored: source -> target where mapping exists, else 0.

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: empty_legend (rows 0-1 empty → no source→target map,
all body cells become 0), no_body (rows 2+ empty → rule's recolor
loop has nothing to apply), unmapped_body (body uses colors not
in legend → all body cells become 0, output collapses).
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "3df81d496895"
VERSION = "1.1.0"
TASK_ID = "3df81d496895"

SUMMARY = "2-row paired-color legend at top + body using mapped source colors."

INVARIANTS = [
    "background is 0",
    "rows 0 and 1 hold a paired-color legend at 2-3 distinct columns",
    "body (rows 2+) holds 2-4 small shapes using legend source colors",
    "source and target colors are pairwise distinct, all non-bg",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("empty_legend", "no_body", "unmapped_body")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 9..11", "valid": "8..14"},
    "grid_w":         {"type": "int", "default": "rng 10..12", "valid": "9..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "palette_size":   {"type": "int", "default": "rng 4..6", "valid": "3..6"},
    "position_bias":  {"type": "str", "default": "legend_above_body",
                       "valid": "legend_above_body"},
    "n_distinct_colors": {"type": "int", "default": "rng 4..6", "valid": "3..6"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
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
        h = ctx.draw_int("grid_h", 9, 9)
        w = ctx.draw_int("grid_w", 10, 10)
        n_pairs_lo, n_pairs_hi = 2, 2
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 11, 13)
        w = ctx.draw_int("grid_w", 12, 14)
        n_pairs_lo, n_pairs_hi = 3, 4
    else:
        h = ctx.draw_int("grid_h", 9, 11)
        w = ctx.draw_int("grid_w", 10, 12)
        n_pairs_lo, n_pairs_hi = 2, 3
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
    n_shapes = rng.randint(2, 4)
    for _ in range(n_shapes):
        src_color = rng.choice(sources)
        shape = rng.choice(_SHAPES)
        sh = max(r for r, _ in shape) + 1
        sw = max(c for _, c in shape) + 1
        for _ in range(40):
            r0 = rng.randint(3, h - sh); c0 = rng.randint(0, w - sw)
            if not _free(g, r0, c0, r0 + sh - 1, c0 + sw - 1): continue
            for dr, dc in shape:
                g[r0 + dr][c0 + dc] = src_color
            break
    return g


def _draw_from_degenerate(name, rng):
    h, w = 10, 11
    g = full_grid(h, w, 0)
    if name == "empty_legend":
        # Rows 0-1 empty — rule's source→target map is empty;
        # every body cell becomes 0.
        for dr, dc in _SHAPES[0]:
            g[3 + dr][2 + dc] = 4
        for dr, dc in _SHAPES[2]:
            g[6 + dr][7 + dc] = 5
        return g
    if name == "no_body":
        # Rows 2+ empty — rule's recolor loop has nothing to apply.
        g[0][2] = 1; g[1][2] = 6
        g[0][6] = 3; g[1][6] = 7
        return g
    if name == "unmapped_body":
        # Body uses colors not in legend (sources are 1, 3 but body
        # uses 4, 5) — all body cells become 0; output collapses.
        g[0][2] = 1; g[1][2] = 6
        g[0][6] = 3; g[1][6] = 7
        for dr, dc in _SHAPES[0]:
            g[3 + dr][2 + dc] = 4
        for dr, dc in _SHAPES[2]:
            g[6 + dr][6 + dc] = 5
        return g
    return g
