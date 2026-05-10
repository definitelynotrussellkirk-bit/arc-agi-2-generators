"""Generator for arc_puzzle_bank_21_set24_s:S24_H4 — keyed depth-histogram match.

Rule: 4 panels separated by full color-9 columns. The first three panels
are keyed prototypes; the last panel is a query shape. Output the key of
the first prototype whose onion-depth histogram matches the query.

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: no_separators, no_query, no_matching_prototype.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "5585e9717c1e"
VERSION = "1.1.0"
TASK_ID = "5585e9717c1e"

SUMMARY = "3 keyed prototype panels plus 1 query panel separated by color-9 columns."

INVARIANTS = [
    "background is 0",
    "panels separated by full color-9 columns",
    "prototype keys sit at each prototype panel's top-left corner",
    "the query panel matches exactly one prototype's onion-depth histogram",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_separators", "no_query", "no_matching_prototype")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "panel_h":        {"type": "int", "default": "rng 5..6", "valid": "5..6"},
    "panel_w":        {"type": "int", "default": "rng 5..6", "valid": "5..6"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "palette_size":   {"type": "int", "default": "5", "valid": "5..5"},
    "position_bias":  {"type": "str", "default": "1x4_panel_lattice",
                       "valid": "1x4_panel_lattice"},
    "n_distinct_colors": {"type": "int", "default": "5", "valid": "5..5"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def _build_motif(rng, k):
    cells = [(0, 0)]; seen = {(0, 0)}
    while len(cells) < k:
        r, c = rng.choice(cells)
        dr, dc = rng.choice([(-1, 0), (1, 0), (0, -1), (0, 1)])
        nr, nc = r + dr, c + dc
        if (nr, nc) not in seen:
            cells.append((nr, nc)); seen.add((nr, nc))
    return cells


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        panel_h = ctx.draw_int("panel_h", 5, 5)
        panel_w = ctx.draw_int("panel_w", 5, 5)
    elif difficulty == "hard":
        panel_h = ctx.draw_int("panel_h", 6, 6)
        panel_w = ctx.draw_int("panel_w", 6, 6)
    else:
        panel_h = ctx.draw_int("panel_h", 5, 6)
        panel_w = ctx.draw_int("panel_w", 5, 6)
    rng = ctx.draw_rng("layout")

    n = 4
    h = panel_h
    w = panel_w * n + (n - 1)
    g = full_grid(h, w, 0)
    for k in range(1, n):
        c = panel_w * k + (k - 1)
        for r in range(h): g[r][c] = 9

    shapes = [
        [(2, 1), (2, 2)],
        [(2, 1), (2, 2), (3, 1), (3, 2)],
        [(1, 1), (1, 2), (1, 3),
         (2, 1), (2, 2), (2, 3),
         (3, 1), (3, 2), (3, 3)],
    ]
    prototypes = list(zip([2, 3, 4], shapes))
    rng.shuffle(prototypes)
    target_idx = rng.randrange(len(prototypes))

    for k, (key, cells) in enumerate(prototypes):
        c0 = k * (panel_w + 1)
        g[0][c0] = key
        for r, c in cells:
            g[r][c0 + c] = 1

    query_c0 = 3 * (panel_w + 1)
    for r, c in prototypes[target_idx][1]:
        g[r][query_c0 + c] = 1
    return g


def _draw_from_degenerate(name, rng):
    panel_h = 5; panel_w = 5; n = 4
    h = panel_h
    w = panel_w * n + (n - 1)
    g = full_grid(h, w, 0)
    shapes = [
        [(2, 1), (2, 2)],
        [(2, 1), (2, 2), (3, 1), (3, 2)],
        [(1, 1), (1, 2), (2, 1), (2, 2), (3, 1), (3, 2)],
    ]
    if name == "no_separators":
        # Panel content but no 9-dividers — rule's panel split
        # fails; prototypes/query indistinguishable.
        for k, (key, cells) in enumerate(zip([2, 3, 4], shapes)):
            c0 = k * (panel_w + 1)
            g[0][c0] = key
            for r, c in cells: g[r][c0 + c] = 1
        return g
    for k in range(1, n):
        c = panel_w * k + (k - 1)
        for r in range(h): g[r][c] = 9
    if name == "no_query":
        # 3 prototypes but query panel empty — rule's lookup
        # has no shape to compare.
        for k, (key, cells) in enumerate(zip([2, 3, 4], shapes)):
            c0 = k * (panel_w + 1)
            g[0][c0] = key
            for r, c in cells: g[r][c0 + c] = 1
        return g
    if name == "no_matching_prototype":
        # Query shape doesn't match any prototype histogram —
        # rule's selection fails.
        for k, (key, cells) in enumerate(zip([2, 3, 4], shapes)):
            c0 = k * (panel_w + 1)
            g[0][c0] = key
            for r, c in cells: g[r][c0 + c] = 1
        query_c0 = 3 * (panel_w + 1)
        for r, c in [(1, 1), (3, 3), (2, 2)]:
            g[r][query_c0 + c] = 1
        return g
    return g
