"""Generator for arc_additional_puzzles_21_set13_bundle:H91 — legend-driven transform stamping.

Rule: rows 0/1 form a legend mapping anchor color → transform token (9=id, 2=cw,
3=180, 4=transpose). Body has a 5-motif (cells of color 5) and anchors (other
non-{0,5} colors). Output drops rows 0/1; for each anchor cell in the body,
stamp the motif (transformed per the anchor color's legend code) with the
transformed cells offset from the anchor's body-row position.

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: no_legend (rows 0/1 empty → rule has no transform map);
no_motif (legend present but no color-5 motif → rule has no template);
no_anchors (legend + motif but no body anchors → no stamps placed).
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "12ec29eae990"
VERSION = "1.1.0"
TASK_ID = "12ec29eae990"

SUMMARY = "Top 2-row legend maps anchor color → transform; body has a 5-motif and 2-3 anchors."

INVARIANTS = [
    "background is 0",
    "row 0 holds 2-3 transform tokens (one of {2, 3, 4, 9}) at distinct columns",
    "row 1 holds the matching anchor colors aligned column-wise with the tokens",
    "body has at least one color-5 cell forming the motif",
    "body has 2-3 anchor cells in colors from the legend; anchors are separated from the motif",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_legend", "no_motif", "no_anchors")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":            {"type": "int", "default": "rng 11..13", "valid": "10..16"},
    "grid_w":            {"type": "int", "default": "rng 12..14", "valid": "10..18"},
    "n_pairs":           {"type": "int", "default": "rng 2..3", "valid": "2..3"},
    "palette_kind":      {"type": "str", "default": "rng helpful",
                          "valid": "|".join(PALETTE_KINDS)},
    "palette_size":      {"type": "int", "default": "rng 4..5", "valid": "3..6"},
    "position_bias":     {"type": "str", "default": "top_legend_with_motif_and_anchors",
                          "valid": "top_legend_with_motif_and_anchors"},
    "n_distinct_colors": {"type": "int", "default": "rng 4..5", "valid": "3..6"},
    "density":           {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":           {"type": "str", "default": "alias for palette_kind",
                          "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


_MOTIFS = [
    [(0, 0), (0, 1)],
    [(0, 0), (1, 0)],
    [(0, 0), (1, 0), (1, 1)],
    [(0, 0), (0, 1), (1, 0)],
    [(0, 0), (1, 0), (2, 0), (2, 1)],
]


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 11, 12)
        w = ctx.draw_int("grid_w", 12, 13)
        n_pairs = ctx.draw_int("n_pairs", 2, 2)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 12, 13)
        w = ctx.draw_int("grid_w", 13, 14)
        n_pairs = ctx.draw_int("n_pairs", 3, 3)
    else:
        h = ctx.draw_int("grid_h", 11, 13)
        w = ctx.draw_int("grid_w", 12, 14)
        n_pairs = ctx.draw_int("n_pairs", 2, 3)
    rng = ctx.draw_rng("layout")

    anchor_colors = rng.sample([1, 2, 3, 4, 6, 7, 8, 9], n_pairs)
    tokens = [rng.choice([2, 3, 4, 9]) for _ in range(n_pairs)]

    for outer in range(60):
        g = full_grid(h, w, 0)
        cols0 = rng.sample(range(w), n_pairs)
        cols0.sort()
        for col, tok, color in zip(cols0, tokens, anchor_colors):
            g[0][col] = tok
            g[1][col] = color
        motif = rng.choice(_MOTIFS)
        mh = max(r for r, _ in motif) + 1
        mw = max(c for _, c in motif) + 1
        placed_motif = False
        for _ in range(80):
            mr = rng.randint(2, h - mh)
            mc = rng.randint(0, w - mw)
            cells_to_paint = [(mr + dr, mc + dc) for dr, dc in motif]
            if any(g[r][c] != 0 for r, c in cells_to_paint):
                continue
            for r, c in cells_to_paint:
                g[r][c] = 5
            placed_motif = True
            motif_cells = cells_to_paint
            break
        if not placed_motif:
            continue
        ok = True
        for color in anchor_colors:
            placed = False
            for _ in range(120):
                ar = rng.randint(2, h - 1)
                ac = rng.randint(0, w - 1)
                if g[ar][ac] != 0:
                    continue
                if any(abs(ar - mrr) + abs(ac - mcc) < 3 for mrr, mcc in motif_cells):
                    continue
                g[ar][ac] = color
                placed = True
                break
            if not placed:
                ok = False
                break
        if ok:
            return g
    raise ValueError("could not realize legend-stamping layout in 60 attempts")


def _draw_from_degenerate(name, rng):
    h, w = 12, 13
    g = full_grid(h, w, 0)
    if name == "no_legend":
        # Rows 0/1 empty — rule has no transform map.
        for dr, dc in [(0, 0), (0, 1), (1, 0)]:
            g[5 + dr][3 + dc] = 5
        g[8][2] = 4; g[10][9] = 6
        return g
    if name == "no_motif":
        # Legend present but no color-5 motif.
        g[0][2] = 9; g[1][2] = 4
        g[0][8] = 2; g[1][8] = 6
        g[7][3] = 4; g[9][9] = 6
        return g
    if name == "no_anchors":
        # Legend + motif but no body anchors.
        g[0][2] = 9; g[1][2] = 4
        g[0][8] = 2; g[1][8] = 6
        for dr, dc in [(0, 0), (0, 1), (1, 0)]:
            g[5 + dr][3 + dc] = 5
        return g
    return g
