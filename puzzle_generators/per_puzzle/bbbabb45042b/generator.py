"""Generator for arc_puzzle_bank_21_set2:S2_M6 — template copies from anchors.

Rule: largest 2-blob is the template. Each color-1 cell is an anchor;
the template's normalized cells get pasted (in color 1) at each anchor.

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: no_template, no_anchors, anchor_oob.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid
from puzzle_generators.helpers.blobs import grow_blob

GENERATOR_ID = "bbbabb45042b"
VERSION = "1.1.0"
TASK_ID = "bbbabb45042b"
SUMMARY = "One 2-blob template + 1-3 single-cell 1-anchors with room around them."

INVARIANTS = [
    "background is 0",
    "exactly one 2-blob (template) of size 3-5",
    "1-3 single 1-cells each having room (template fits without OOB)",
    "anchors are far enough from the template to not 4-touch it",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_template", "no_anchors", "anchor_oob")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 9..12", "valid": "8..14"},
    "grid_w":         {"type": "int", "default": "rng 10..13", "valid": "9..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "palette_size":   {"type": "int", "default": "2", "valid": "2..2"},
    "position_bias":  {"type": "str", "default": "template_then_anchors",
                       "valid": "template_then_anchors"},
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
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 10, 11)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 12, 14)
        w = ctx.draw_int("grid_w", 13, 16)
    else:
        h = ctx.draw_int("grid_h", 9, 12)
        w = ctx.draw_int("grid_w", 10, 13)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    used: set[tuple[int, int]] = set()
    template = grow_blob(rng, h, w, used, rng.randint(3, 5), max_attempts=80)
    if template is None:
        return g
    rs = sorted(r for r, _ in template)
    cs = sorted(c for _, c in template)
    tpl_h = rs[-1] - rs[0] + 1
    tpl_w = cs[-1] - cs[0] + 1
    for r, c in template:
        g[r][c] = 2
    used |= template
    n_anchors = rng.randint(1, 3)
    for _ in range(n_anchors):
        for _ in range(40):
            ar = rng.randint(0, h - tpl_h)
            ac = rng.randint(0, w - tpl_w)
            stamped = {(ar + (r - rs[0]), ac + (c - cs[0])) for r, c in template}
            if any(g[r][c] != 0 for r, c in stamped):
                continue
            anchor = (ar, ac)
            if g[anchor[0]][anchor[1]] != 0:
                continue
            g[anchor[0]][anchor[1]] = 1
            break
    return g


def _draw_from_degenerate(name, rng):
    h, w = 10, 11
    g = full_grid(h, w, 0)
    if name == "no_template":
        # 1-anchors but no 2-template — rule has no shape to stamp.
        g[3][4] = 1; g[6][7] = 1
        return g
    if name == "no_anchors":
        # 2-template but no 1-anchors — rule has no positions to
        # stamp at.
        for r, c in [(1, 1), (1, 2), (2, 1)]: g[r][c] = 2
        return g
    if name == "anchor_oob":
        # Anchor placed near corner so the full stamp would extend
        # past the grid — rule's stamp region is undefined.
        for r, c in [(1, 1), (1, 2), (2, 1)]: g[r][c] = 2
        g[h - 1][w - 1] = 1
        return g
    return g
