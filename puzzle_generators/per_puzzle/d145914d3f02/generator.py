"""Generator for arc_additional_puzzles_21_set18_bundle:M120 — rotated 7-template stamps at anchors.

Rule: a 9-cell defines the origin; nearby 7-cells form the template
(by offset). Each anchor cell with value in {2,3,4,5} stamps 7s at the
template's offsets rotated by the anchor's transform (2=0°, 3=90°,
4=180°, 5=270°).

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: no_anchors (no stamps to apply → output equals input),
symmetric_template (template invariant under 90° rotations → all 4
anchor codes produce identical stamps), single_anchor (only one
anchor → no rotation contrast across stamps).
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "d145914d3f02"
VERSION = "1.1.0"
TASK_ID = "d145914d3f02"
SUMMARY = "9 origin + 2-3 7-cells defining template, plus 1-3 rotation-anchors (2/3/4/5)."

INVARIANTS = [
    "background is 0",
    "exactly one 9-cell (the origin)",
    "2-3 7-cells form a small template adjacent to the 9",
    "1-3 anchor cells with distinct values from {2, 3, 4, 5}",
    "anchors leave room for the rotated template to land in-bounds",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_anchors", "symmetric_template", "single_anchor")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 11..14", "valid": "10..16"},
    "grid_w":         {"type": "int", "default": "rng 12..15", "valid": "10..18"},
    "n_anchors":      {"type": "int", "default": "rng 1..3", "valid": "1..4"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "palette_size":   {"type": "int", "default": "rng 4..6", "valid": "3..6"},
    "position_bias":  {"type": "str", "default": "origin_template_anchors",
                       "valid": "origin_template_anchors"},
    "n_distinct_colors": {"type": "int", "default": "rng 4..6", "valid": "3..6"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}

_TEMPLATES = [
    [(-1, 0), (0, -1)],
    [(-1, 0), (0, -1), (1, 0)],
    [(-1, 0), (0, 1), (1, 0)],
    [(0, 1), (1, 0)],
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
        n_anchors = ctx.draw_int("n_anchors", 1, 1)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 13, 15)
        w = ctx.draw_int("grid_w", 14, 17)
        n_anchors = ctx.draw_int("n_anchors", 3, 4)
    else:
        h = ctx.draw_int("grid_h", 11, 14)
        w = ctx.draw_int("grid_w", 12, 15)
        n_anchors = ctx.draw_int("n_anchors", 1, 3)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    template = rng.choice(_TEMPLATES)
    nine_r = rng.randint(2, 4)
    nine_c = rng.randint(2, 4)
    g[nine_r][nine_c] = 9
    for dr, dc in template:
        rr = nine_r + dr; cc = nine_c + dc
        if 0 <= rr < h and 0 <= cc < w:
            g[rr][cc] = 7
    anchors = rng.sample([2, 3, 4, 5], n_anchors)
    placed_anchors: list[tuple[int, int]] = []
    margin = 4
    for v in anchors:
        for _ in range(80):
            ar = rng.randint(margin, h - margin - 1)
            ac = rng.randint(margin, w - margin - 1)
            if g[ar][ac] != 0: continue
            if any(abs(ar - pr) < 4 and abs(ac - pc) < 4 for pr, pc in placed_anchors): continue
            if abs(ar - nine_r) < 4 and abs(ac - nine_c) < 4: continue
            g[ar][ac] = v
            placed_anchors.append((ar, ac))
            break
    return g


def _draw_from_degenerate(name, rng):
    h, w = 12, 14
    g = full_grid(h, w, 0)
    g[3][3] = 9
    for dr, dc in _TEMPLATES[1]:
        g[3 + dr][3 + dc] = 7
    if name == "no_anchors":
        # No anchors — rule's stamp loop is empty; output equals
        # input (just the origin + template).
        return g
    if name == "symmetric_template":
        # Use a 4-fold symmetric template (the 4 cardinal neighbors)
        # so all rotations produce identical output; rule's
        # rotation-by-anchor branch yields no contrast.
        g = full_grid(h, w, 0)
        g[3][3] = 9
        for dr, dc in [(-1, 0), (0, -1), (0, 1), (1, 0)]:
            g[3 + dr][3 + dc] = 7
        g[7][7] = 2
        g[10][3] = 4
        return g
    if name == "single_anchor":
        # Only one anchor — rule applies just one rotation; no
        # cross-anchor contrast in output.
        g[8][8] = 3
        return g
    return g
