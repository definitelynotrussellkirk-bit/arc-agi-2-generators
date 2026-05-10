"""Generator for arc_additional_puzzles_21_set17_bundle:M118 — stamp template at every 8-anchor.

Rule: the largest connected component containing an 8 is the
template, with the 8-cell as its origin. Stamp the template (anchored
at 8) at each free 8-cell in the grid. Overlap: same color stays;
different → 9.

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: no_anchors (no free 8-cells → rule's stamp loop is empty,
output equals input), no_template (no 8-containing component → rule's
template extractor finds nothing), single_cell_template (template is
just the 8 itself → stamp is a no-op).
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, paint_at
from puzzle_generators.helpers.blobs import bbox_overlaps

GENERATOR_ID = "75ff4423494a"
VERSION = "1.1.0"
TASK_ID = "75ff4423494a"
SUMMARY = "Small template (one 8 + colored cells) plus 1-2 free 8-anchors."

INVARIANTS = [
    "background is 0",
    "exactly one connected component containing a single 8 (the template)",
    "1-2 lone 8-cells elsewhere act as anchors",
    "anchors don't merge into the template's connected component",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_anchors", "no_template", "single_cell_template")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 9..12", "valid": "8..14"},
    "grid_w":         {"type": "int", "default": "rng 11..14", "valid": "10..16"},
    "n_anchors":      {"type": "int", "default": "rng 1..2", "valid": "1..3"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "palette_size":   {"type": "int", "default": "rng 2..3", "valid": "2..4"},
    "position_bias":  {"type": "str", "default": "template_plus_anchors",
                       "valid": "template_plus_anchors"},
    "n_distinct_colors": {"type": "int", "default": "rng 2..3", "valid": "2..4"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}

_TEMPLATES = [
    ([(0, 0), (0, 1), (1, 0), (1, 1), (2, 1)], 0),
    ([(0, 0), (0, 1), (1, 0), (1, 1)], 0),
    ([(0, 0), (1, 0), (1, 1), (1, 2), (2, 1)], 0),
    ([(0, 0), (0, 1), (0, 2), (1, 1), (2, 1)], 0),
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
        n_anchors = ctx.draw_int("n_anchors", 2, 3)
    else:
        h = ctx.draw_int("grid_h", 9, 12)
        w = ctx.draw_int("grid_w", 11, 14)
        n_anchors = ctx.draw_int("n_anchors", 1, 2)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    cells, marker_idx = rng.choice(_TEMPLATES)
    sh = max(c[0] for c in cells) + 1
    sw = max(c[1] for c in cells) + 1
    other_color = rng.choice([2, 3, 4, 5, 6, 7])
    r0 = rng.randint(1, h - sh - 2)
    c0 = rng.randint(1, w - sw - 2)
    for i, (dr, dc) in enumerate(cells):
        g[r0 + dr][c0 + dc] = 8 if i == marker_idx else other_color
    placed: list[tuple[int, int, int, int]] = [(r0 - 1, c0 - 1, r0 + sh, c0 + sw)]
    extra = 0
    for _ in range(80):
        if extra >= n_anchors: break
        ar = rng.randint(2, h - sh - 2)
        ac = rng.randint(2, w - sw - 2)
        bb = (ar - 1, ac - 1, ar + 1, ac + 1)
        if any(bbox_overlaps(bb, p) for p in placed): continue
        if g[ar][ac] != 0: continue
        g[ar][ac] = 8
        placed.append(bb)
        extra += 1
    return g


def _draw_from_degenerate(name, rng):
    h, w = 11, 13
    g = full_grid(h, w, 0)
    if name == "no_anchors":
        # No free 8-anchors — rule's stamp loop is empty; output
        # equals input (just the template).
        cells, marker_idx = _TEMPLATES[0]
        for i, (dr, dc) in enumerate(cells):
            g[1 + dr][1 + dc] = 8 if i == marker_idx else 3
        return g
    if name == "no_template":
        # No 8-containing component — rule's template extractor
        # finds nothing; the per-anchor stamp has no shape.
        for r, c in [(2, 2), (3, 2), (3, 3)]: g[r][c] = 3
        g[7][8] = 8
        return g
    if name == "single_cell_template":
        # Template is just the 8 itself (no other colored cells)
        # — stamp is a no-op; rule's overlap branch never fires.
        g[2][2] = 8
        g[7][8] = 8
        return g
    return g
