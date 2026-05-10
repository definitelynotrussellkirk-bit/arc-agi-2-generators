"""Generator for arc_puzzle_bank_nineteenth21:M130 — stamp colored shape at every 1-anchor.

Rule: a colored shape acts as a template (with anchor at its
top-left). Each 1-cell elsewhere is an anchor; output stamps the
template at each anchor. Original shape and 1s are erased.

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: no_template, no_anchors, anchor_oob.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, paint_at
from puzzle_generators.helpers.palette import random_palette
from puzzle_generators.helpers.blobs import bbox_overlaps

GENERATOR_ID = "f5ccc2b4c650"
VERSION = "1.1.0"
TASK_ID = "f5ccc2b4c650"
SUMMARY = "Colored 3-cell template + 1-2 single-cell 1-anchors elsewhere."

INVARIANTS = [
    "background is 0",
    "exactly one 3-cell colored template (color ≠ 1)",
    "1-2 single-cell 1-anchors with room for the template to land in-bounds",
    "anchors don't touch each other or the template",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_template", "no_anchors", "anchor_oob")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 5..7", "valid": "5..10"},
    "grid_w":         {"type": "int", "default": "rng 8..11", "valid": "7..14"},
    "n_anchors":      {"type": "int", "default": "rng 1..2", "valid": "1..3"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "palette_size":   {"type": "int", "default": "2", "valid": "2..2"},
    "position_bias":  {"type": "str", "default": "template_with_anchors",
                       "valid": "template_with_anchors"},
    "n_distinct_colors": {"type": "int", "default": "2", "valid": "2..2"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}

_TEMPLATES = [
    [(0, 0), (0, 1), (1, 0)],
    [(0, 0), (0, 1), (1, 1)],
    [(0, 0), (1, 0), (1, 1)],
    [(0, 1), (1, 0), (1, 1)],
]


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 5, 5)
        w = ctx.draw_int("grid_w", 8, 9)
        n_anchors = ctx.draw_int("n_anchors", 1, 1)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 7, 9)
        w = ctx.draw_int("grid_w", 11, 13)
        n_anchors = ctx.draw_int("n_anchors", 2, 3)
    else:
        h = ctx.draw_int("grid_h", 5, 7)
        w = ctx.draw_int("grid_w", 8, 11)
        n_anchors = ctx.draw_int("n_anchors", 1, 2)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    color = rng.choice(list(random_palette(rng, 4, exclude={1})))
    template = rng.choice(_TEMPLATES)
    sh = max(c[0] for c in template) + 1
    sw = max(c[1] for c in template) + 1
    r0 = rng.randint(0, max(0, h - sh - 2))
    c0 = rng.randint(0, max(0, w // 2 - sw - 1))
    paint_at(g, r0, c0, template, color)
    placed: list[tuple[int, int, int, int]] = [
        (r0 - 1, c0 - 1, r0 + sh, c0 + sw)]
    for _ in range(80):
        if len(placed) - 1 >= n_anchors: break
        ar = rng.randint(0, h - sh - 1)
        ac = rng.randint(c0 + sw + 1, w - sw)
        bb = (ar - 1, ac - 1, ar + sh, ac + sw)
        if any(bbox_overlaps(bb, p) for p in placed): continue
        if g[ar][ac] != 0: continue
        g[ar][ac] = 1
        placed.append(bb)
    return g


def _draw_from_degenerate(name, rng):
    h, w = 6, 10
    g = full_grid(h, w, 0)
    if name == "no_template":
        # Anchors but no template — rule's stamp source is
        # undefined; output has only erased 1-cells.
        g[2][5] = 1; g[4][7] = 1
        return g
    if name == "no_anchors":
        # Template but no 1-anchors — rule has no positions to
        # stamp at; output equals input minus the erased template.
        for r, c in [(1, 1), (1, 2), (2, 1)]: g[r][c] = 4
        return g
    if name == "anchor_oob":
        # Anchor at right edge so stamp would extend OOB —
        # rule's silently-drop behavior leaves clipped/empty
        # output.
        for r, c in [(1, 1), (1, 2), (2, 1)]: g[r][c] = 4
        g[4][w - 1] = 1
        return g
    return g
