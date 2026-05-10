"""Generator for arc_puzzle_bank_21_set5_s:S5_M6 — template stamp at anchors.

Rule: largest 3-blob = template. Each 4-cell is an anchor. Output:
empty grid + template (in 8) stamped at each anchor.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_anchors,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_template, no_anchors, anchor_overlaps_template.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid
from puzzle_generators.helpers.blobs import grow_blob

GENERATOR_ID = "9792326ad0cb"
VERSION = "1.1.0"
TASK_ID = "9792326ad0cb"
SUMMARY = "One 3-blob template + 1-3 4-anchors with room to stamp."

INVARIANTS = [
    "background is 0",
    "exactly one 3-blob (template) of size 2-4",
    "1-3 single 4-cells that have room for the stamp without OOB",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_template", "no_anchors", "anchor_overlaps_template")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 9..11", "valid": "8..14"},
    "grid_w":         {"type": "int", "default": "rng 10..13", "valid": "9..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_anchors":      {"type": "int", "default": "rng 1..3", "valid": "1..4"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2..2"},
    "position_bias":  {"type": "str", "default": "3blob_template_with_4anchors",
                       "valid": "3blob_template_with_4anchors"},
    "n_distinct_colors": {"type": "int", "default": "2", "valid": "2..2"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 9, 9)
        w = ctx.draw_int("grid_w", 10, 11)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 10, 11)
        w = ctx.draw_int("grid_w", 12, 13)
    else:
        h = ctx.draw_int("grid_h", 9, 11)
        w = ctx.draw_int("grid_w", 10, 13)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    used: set[tuple[int, int]] = set()
    template = grow_blob(rng, h, w, used, rng.randint(2, 4), max_attempts=80)
    if template is None:
        return g
    rs = sorted(r for r, _ in template)
    cs = sorted(c for _, c in template)
    tpl_h = rs[-1] - rs[0] + 1
    tpl_w = cs[-1] - cs[0] + 1
    for r, c in template:
        g[r][c] = 3
    used |= template
    for _ in range(rng.randint(1, 3)):
        for _ in range(40):
            ar = rng.randint(0, h - tpl_h)
            ac = rng.randint(0, w - tpl_w)
            stamped = {(ar + (r - rs[0]), ac + (c - cs[0])) for r, c in template}
            if any(g[r][c] != 0 for r, c in stamped):
                continue
            g[ar][ac] = 4
            break
    return g


def _draw_from_degenerate(name, rng):
    h, w = 10, 11
    g = full_grid(h, w, 0)
    if name == "no_template":
        # 4-anchors but no 3-blob → no shape to stamp
        g[3][3] = 4; g[6][7] = 4
        return g
    if name == "no_anchors":
        # 3-template but no 4-anchors → nothing to stamp at
        for r, c in [(2, 2), (2, 3), (3, 3)]: g[r][c] = 3
        return g
    if name == "anchor_overlaps_template":
        # 4-anchor inside template footprint → ambiguous stamp position
        for r, c in [(2, 2), (2, 3), (3, 3)]: g[r][c] = 3
        g[3][2] = 4  # inside the template's bbox
        return g
    return g
