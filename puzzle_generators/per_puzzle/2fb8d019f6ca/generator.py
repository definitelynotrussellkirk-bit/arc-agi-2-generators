"""Generator for arc_additional_puzzles_21_set12_bundle:M82 — stamp template at every 8-anchor.

Rule: BFS from (0,0) over non-0, non-8 cells gives the "template",
cropped to its bbox. Each 8-cell elsewhere is an anchor; output is a
blank grid with the template stamped (top-left aligned) at each anchor.

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: no_template (cell (0,0) is bg → rule's BFS root finds
nothing, template empty), no_anchors (template present but no 8-cells →
rule has no positions to stamp at), template_at_anchor (an 8-anchor
falls inside the template's bbox — rule's stamp lands on top of
template).
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, paint_at
from puzzle_generators.helpers.palette import random_palette

GENERATOR_ID = "2fb8d019f6ca"
VERSION = "1.1.0"
TASK_ID = "2fb8d019f6ca"
SUMMARY = "Small connected template at top-left + 1-3 8-anchors elsewhere."

INVARIANTS = [
    "(0,0) is a non-0, non-8 cell (the template root)",
    "the template is a single 4-connected region of non-0, non-8 cells",
    "1-3 8-cells elsewhere act as paste anchors",
    "anchor positions leave room for the template's bbox to land in-bounds",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_template", "no_anchors", "template_at_anchor")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":            {"type": "int", "default": "rng 9..12", "valid": "8..16"},
    "grid_w":            {"type": "int", "default": "rng 11..14", "valid": "10..16"},
    "n_anchors":         {"type": "int", "default": "rng 1..3", "valid": "1..4"},
    "palette_kind":      {"type": "str", "default": "rng helpful",
                          "valid": "|".join(PALETTE_KINDS)},
    "palette_size":      {"type": "int", "default": "rng 2..3", "valid": "2..4"},
    "position_bias":     {"type": "str", "default": "template_at_origin_plus_anchors",
                          "valid": "template_at_origin_plus_anchors"},
    "n_distinct_colors": {"type": "int", "default": "rng 2..3", "valid": "2..4"},
    "density":           {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":           {"type": "str", "default": "alias for palette_kind",
                          "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}

_TEMPLATES = [
    [(0, 0, 0), (0, 1, 1), (1, 0, 1), (1, 1, 0)],
    [(0, 0, 0), (1, 0, 0), (1, 1, 1)],
    [(0, 0, 0), (0, 1, 1), (1, 1, 0), (1, 2, 0)],
    [(0, 0, 0), (1, 0, 0), (1, 1, 0), (2, 1, 1)],
    [(0, 0, 0), (0, 1, 0), (0, 2, 0), (1, 1, 1)],
    [(0, 0, 0), (1, 0, 0), (2, 0, 0)],
]


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 11, 12)
        n_anchors = ctx.draw_int("n_anchors", 1, 1)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 11, 12)
        w = ctx.draw_int("grid_w", 13, 14)
        n_anchors = ctx.draw_int("n_anchors", 2, 3)
    else:
        h = ctx.draw_int("grid_h", 9, 12)
        w = ctx.draw_int("grid_w", 11, 14)
        n_anchors = ctx.draw_int("n_anchors", 1, 3)
    rng = ctx.draw_rng("layout")
    n_colors = rng.choice([1, 2])
    palette = list(random_palette(rng, n_colors, exclude={8}))
    template = rng.choice(_TEMPLATES)
    template_h = max(c[0] for c in template) + 1
    template_w = max(c[1] for c in template) + 1
    g = full_grid(h, w, 0)
    for dr, dc, ci in template:
        g[dr][dc] = palette[ci % n_colors]
    placed = 0
    for _ in range(80):
        if placed >= n_anchors: break
        ar = rng.randint(template_h + 1, h - template_h - 1)
        ac = rng.randint(template_w + 1, w - template_w - 1)
        if g[ar][ac] != 0: continue
        too_close = False
        for dr in range(template_h):
            for dc in range(template_w):
                if 0 <= ar + dr < h and 0 <= ac + dc < w and g[ar + dr][ac + dc] != 0:
                    too_close = True; break
            if too_close: break
        if too_close: continue
        g[ar][ac] = 8
        placed += 1
    return g


def _draw_from_degenerate(name, rng):
    h, w = 10, 12
    g = full_grid(h, w, 0)
    if name == "no_template":
        # (0,0) is bg — rule's BFS root finds nothing.
        g[5][5] = 8
        g[7][9] = 8
        return g
    if name == "no_anchors":
        # Template present but no 8-cells — rule has no positions.
        g[0][0] = 4; g[0][1] = 6; g[1][0] = 6
        return g
    if name == "template_at_anchor":
        # 8-anchor inside template bbox — stamp lands on top.
        g[0][0] = 4; g[0][1] = 6; g[1][0] = 6
        g[1][1] = 8   # anchor inside template bbox
        return g
    return g
