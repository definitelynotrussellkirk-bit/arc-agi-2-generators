"""Generator for arc_additional_puzzles_21_set6:M41 — stamp 2/4-blob template at each 6-9 anchor.

Rule: find largest connected blob of {2,4}-colored cells. Normalize
its cell-shape. Each cell with color in {6,7,8,9} is an anchor;
output stamps the shape at the anchor (using anchor's color).

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: no_anchors (no {6,7,8,9} cells → rule's per-anchor stamp
loop is empty, output = input), no_template (no {2,4} cells → rule's
template extractor finds nothing, stamp has no shape), single_cell_template
(template is a single cell → rule's stamp is trivial, no shape contrast).
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "05b5a82ace36"
VERSION = "1.1.0"
TASK_ID = "05b5a82ace36"
SUMMARY = "Mixed 2/4 template + 1-3 anchor cells in {6, 7, 8, 9}."

INVARIANTS = [
    "background is 0",
    "exactly one connected blob using colors 2 and/or 4 (the template)",
    "1-3 anchor cells in {6, 7, 8, 9} elsewhere",
    "anchors leave room for the stamped template to land in-bounds",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_anchors", "no_template", "single_cell_template")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 9..12", "valid": "8..14"},
    "grid_w":         {"type": "int", "default": "rng 11..14", "valid": "10..16"},
    "n_anchors":      {"type": "int", "default": "rng 1..3", "valid": "1..4"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "palette_size":   {"type": "int", "default": "rng 3..5", "valid": "3..6"},
    "position_bias":  {"type": "str", "default": "template_plus_anchors",
                       "valid": "template_plus_anchors"},
    "n_distinct_colors": {"type": "int", "default": "rng 3..5", "valid": "3..6"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}

_TEMPLATES = [
    [(0, 0, 2), (1, 0, 2), (1, 1, 4)],
    [(0, 0, 2), (0, 1, 2), (1, 1, 4)],
    [(0, 0, 2), (0, 1, 4), (0, 2, 4), (1, 0, 2)],
    [(0, 0, 4), (1, 0, 2), (1, 1, 4), (1, 2, 2)],
    [(0, 0, 2), (0, 1, 4), (1, 0, 4), (1, 1, 2)],
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
        h = ctx.draw_int("grid_h", 11, 13)
        w = ctx.draw_int("grid_w", 13, 16)
        n_anchors = ctx.draw_int("n_anchors", 3, 4)
    else:
        h = ctx.draw_int("grid_h", 9, 12)
        w = ctx.draw_int("grid_w", 11, 14)
        n_anchors = ctx.draw_int("n_anchors", 1, 3)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    template = rng.choice(_TEMPLATES)
    th = max(c[0] for c in template) + 1
    tw = max(c[1] for c in template) + 1
    tr = rng.randint(0, 2)
    tc = rng.randint(0, 2)
    for dr, dc, color in template:
        g[tr + dr][tc + dc] = color
    placed_anchors: list[tuple[int, int]] = [(tr, tc), (tr + th, tc + tw)]
    chosen_colors = rng.sample([6, 7, 8, 9], n_anchors)
    margin = max(th, tw) + 1
    for color in chosen_colors:
        for _ in range(80):
            ar = rng.randint(margin, h - margin - 1)
            ac = rng.randint(margin, w - margin - 1)
            if g[ar][ac] != 0: continue
            if any(abs(ar - pr) < margin and abs(ac - pc) < margin for pr, pc in placed_anchors): continue
            g[ar][ac] = color
            placed_anchors.append((ar, ac))
            break
    return g


def _draw_from_degenerate(name, rng):
    h, w = 11, 13
    g = full_grid(h, w, 0)
    if name == "no_anchors":
        # No anchors — rule's per-anchor stamp loop is empty;
        # output equals input (template only).
        for dr, dc, color in _TEMPLATES[0]:
            g[1 + dr][1 + dc] = color
        return g
    if name == "no_template":
        # No {2,4} cells — rule's template extractor finds nothing;
        # the stamp has no shape to apply at anchors.
        g[5][5] = 6
        g[7][8] = 7
        return g
    if name == "single_cell_template":
        # Template is a single cell — stamp is trivial; no shape
        # contrast across anchors.
        g[1][1] = 2
        g[5][5] = 6
        g[8][9] = 7
        return g
    return g
