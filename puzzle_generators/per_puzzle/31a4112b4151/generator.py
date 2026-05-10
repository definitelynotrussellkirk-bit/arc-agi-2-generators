"""Generator for arc_puzzle_bank_eighteenth21:M124 — stamp 3-shape at every 9-anchor.

Rule: a 9-cell anchors a 3-cell colored template (offsets stay
fixed). Each additional 9-cell elsewhere becomes another anchor;
output stamps the template at each anchor (the original 9 stays;
the original template is preserved; new 9-anchors get the template).
Output erases the lone 9-anchors (the template's 9 stays).

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: no_template (9-anchor present but no adjacent
template → rule has no offsets); no_anchors (template + initial 9
present but no extra 9s → rule has no destinations to stamp);
single_cell_template (template is just 1 cell → all stamps trivial,
no shape contrast).
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, paint_at
from puzzle_generators.helpers.palette import random_palette
from puzzle_generators.helpers.blobs import bbox_overlaps

GENERATOR_ID = "31a4112b4151"
VERSION = "1.1.0"
TASK_ID = "31a4112b4151"
SUMMARY = "9-anchor + 3-cell template (one color) + 1-2 additional lone 9-anchors."

INVARIANTS = [
    "background is 0",
    "exactly one anchor 9-cell adjacent to a 3-cell template (single non-9 color)",
    "1-2 additional 9-cells elsewhere with room to stamp the template in-bounds",
    "lone 9-cells don't touch each other or the template region",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_template", "no_anchors", "single_cell_template")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":            {"type": "int", "default": "rng 8..11", "valid": "7..14"},
    "grid_w":            {"type": "int", "default": "rng 8..11", "valid": "7..14"},
    "n_anchors":         {"type": "int", "default": "rng 1..2", "valid": "1..3"},
    "palette_kind":      {"type": "str", "default": "rng helpful",
                          "valid": "|".join(PALETTE_KINDS)},
    "palette_size":      {"type": "int", "default": "rng 2..2", "valid": "2..2"},
    "position_bias":     {"type": "str", "default": "anchor_template_with_extras",
                          "valid": "anchor_template_with_extras"},
    "n_distinct_colors": {"type": "int", "default": "rng 2..2", "valid": "2..2"},
    "density":           {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":           {"type": "str", "default": "alias for palette_kind",
                          "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}

_TEMPLATES = [
    [(0, 1), (1, 0), (1, 1)],
    [(1, -1), (1, 0), (1, 1)],
    [(0, 1), (1, 1), (2, 1)],
    [(-1, 1), (0, 1), (1, 1)],
]


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("grid_w", 8, 9)
        n_anchors = ctx.draw_int("n_anchors", 1, 1)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 10, 11)
        w = ctx.draw_int("grid_w", 10, 11)
        n_anchors = ctx.draw_int("n_anchors", 2, 2)
    else:
        h = ctx.draw_int("grid_h", 8, 11)
        w = ctx.draw_int("grid_w", 8, 11)
        n_anchors = ctx.draw_int("n_anchors", 1, 2)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    template = rng.choice(_TEMPLATES)
    color = rng.choice(list(random_palette(rng, 4, exclude={9})))
    rs = [r for r, _ in template]; cs = [c for _, c in template]
    rmin, rmax, cmin, cmax = min(rs), max(rs), min(cs), max(cs)
    margin_top = max(0, -rmin) + 1
    margin_bot = max(0, rmax) + 1
    margin_lt = max(0, -cmin) + 1
    margin_rt = max(0, cmax) + 1
    anchor_r = rng.randint(margin_top, h - margin_bot - 1)
    anchor_c = rng.randint(margin_lt, w - margin_rt - 1)
    g[anchor_r][anchor_c] = 9
    for dr, dc in template:
        g[anchor_r + dr][anchor_c + dc] = color
    placed: list[tuple[int, int, int, int]] = [
        (anchor_r + rmin - 1, anchor_c + cmin - 1,
         anchor_r + rmax + 1, anchor_c + cmax + 1)]
    placed_count = 0
    for _ in range(80):
        if placed_count >= n_anchors: break
        ar = rng.randint(margin_top, h - margin_bot - 1)
        ac = rng.randint(margin_lt, w - margin_rt - 1)
        if g[ar][ac] != 0: continue
        bb = (ar + rmin - 1, ac + cmin - 1, ar + rmax + 1, ac + cmax + 1)
        if any(bbox_overlaps(bb, p) for p in placed): continue
        g[ar][ac] = 9
        placed.append(bb)
        placed_count += 1
    return g


def _draw_from_degenerate(name, rng):
    h, w = 10, 10
    g = full_grid(h, w, 0)
    if name == "no_template":
        # Anchor 9 present but no adjacent template — rule has no offsets.
        g[3][3] = 9
        g[6][7] = 9
        return g
    if name == "no_anchors":
        # Template + initial 9 but no extra 9s — no destinations.
        g[3][3] = 9
        g[3][4] = 4; g[4][3] = 4; g[4][4] = 4
        return g
    if name == "single_cell_template":
        # Template is 1 cell — all stamps trivial.
        g[3][3] = 9
        g[3][4] = 4
        g[6][7] = 9
        return g
    return g
