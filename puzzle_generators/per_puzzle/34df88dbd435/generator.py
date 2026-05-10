"""Generator for puzzle b4dc03b8.

Rule: for each non-bg object: bbox h > w → 2 (tall); w > h → 8 (wide);
h == w → 4 (square).

Combinatorial axes (8): grid_h/w, n_tall, n_wide, n_square,
shape_kind (rect/L/cross/blob/line), aspect_ratio_strength,
input_palette_mode, placement.
Degenerates: all_tall, all_wide, all_square.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid
from puzzle_generators.helpers.blobs import grow_blob, bbox_of, bbox_overlaps

GENERATOR_ID = "34df88dbd435"
VERSION = "1.1.0"
TASK_ID = "34df88dbd435"
SUMMARY = "Objects with various aspect ratios; rule recolors by tall(2)/wide(8)/square(4)."

INVARIANTS = [
    "≥1 tall object (bbox h > w)",
    "≥1 wide object (bbox w > h)",
    "≥1 square object (bbox h == w)",
    "objects 4-disconnected with margin ≥ 1",
]

SHAPE_KINDS = ("rect", "L_shape", "cross", "blob", "line")
PALETTE_MODES = ("same_color", "all_distinct", "per_aspect")
PLACEMENTS = ("random", "corners", "row", "column", "grid")
DEGENERATE_TEXTURES = ("all_tall", "all_wide", "all_square")
HELPFUL_TEXTURES = SHAPE_KINDS

AXES = {
    "grid_h":             {"type": "int", "default": "rng 8..14", "valid": "6..18"},
    "grid_w":             {"type": "int", "default": "rng 8..14", "valid": "6..18"},
    "n_tall":             {"type": "int", "default": "rng 1..2", "valid": "0..4"},
    "n_wide":             {"type": "int", "default": "rng 1..2", "valid": "0..4"},
    "n_square":           {"type": "int", "default": "rng 1..2", "valid": "0..4"},
    "shape_kind":         {"type": "str", "default": "rng helpful",
                           "valid": "|".join(SHAPE_KINDS)},
    "input_palette_mode": {"type": "str", "default": "rng helpful",
                           "valid": "|".join(PALETTE_MODES)},
    "placement":          {"type": "str", "default": "rng helpful",
                           "valid": "|".join(PLACEMENTS)},
    "texture":            {"type": "str", "default": "alias for shape_kind",
                           "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if difficulty == "easy":
        h_lo, h_hi, n_lo, n_hi = 8, 11, 1, 1
    elif difficulty == "hard":
        h_lo, h_hi, n_lo, n_hi = 13, 18, 2, 2
    else:
        h_lo, h_hi, n_lo, n_hi = 8, 18, 1, 2
    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", h_lo, h_hi)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], h, w, rng)
    n_t = int(overrides.get("n_tall", ctx.draw_int("n_tall", n_lo, n_hi)))
    n_w = int(overrides.get("n_wide", ctx.draw_int("n_wide", n_lo, n_hi)))
    n_s = int(overrides.get("n_square", ctx.draw_int("n_square", n_lo, n_hi)))
    palette_mode = overrides.get("input_palette_mode",
                                 ctx.draw_choice("input_palette_mode", list(PALETTE_MODES)))
    palette = list(ctx.draw_distinct_colors("palette", n=6, exclude={0, 2, 4, 8}))
    g = full_grid(h, w, 0)
    used: set = set(); bboxes: list = []
    plan = ([("tall", n_t)] + [("wide", n_w)] + [("square", n_s)])
    color_idx = 0
    for orient, count in plan:
        for _ in range(count):
            for _try in range(15):
                size = rng.randint(3, 7)
                blob = _make_oriented(rng, h, w, used, size, orient)
                if blob is None: continue
                bb = bbox_of(blob)
                if any(bbox_overlaps(bb, ob) for ob in bboxes): continue
                if palette_mode == "same_color":
                    color = palette[0]
                elif palette_mode == "per_aspect":
                    color = palette[{"tall": 0, "wide": 1, "square": 2}.get(orient, 0)
                                    % len(palette)]
                else:
                    color = palette[color_idx % len(palette)]; color_idx += 1
                used |= blob; bboxes.append(bb)
                for r, c in blob:
                    g[r][c] = color
                break
    return g


def _make_oriented(rng, h, w, used, target_size, orient):
    for _ in range(15):
        blob = grow_blob(rng, h, w, used, target_size)
        if blob is None: return None
        bb = bbox_of(blob)
        bh = bb[2] - bb[0] + 1; bw = bb[3] - bb[1] + 1
        if orient == "tall" and bh > bw: return blob
        if orient == "wide" and bw > bh: return blob
        if orient == "square" and bh == bw: return blob
    return None


def _draw_from_degenerate(name, h, w, rng):
    g = full_grid(h, w, 0)
    color = rng.choice([1, 3, 5, 6, 7, 9])
    if name == "all_tall":
        # 3 tall objects.
        for i, c0 in enumerate([2, w // 2, w - 4]):
            for r in range(2, 6):
                if 0 <= c0 < w:
                    g[r][c0] = color
        return g
    if name == "all_wide":
        for i, r0 in enumerate([2, h // 2, h - 3]):
            for c in range(2, 7):
                if 0 <= r0 < h and c < w:
                    g[r0][c] = color
        return g
    if name == "all_square":
        for r0, c0 in [(2, 2), (2, w - 5), (h - 5, 2)]:
            for r in range(r0, r0 + 3):
                for c in range(c0, c0 + 3):
                    if 0 <= r < h and 0 <= c < w:
                        g[r][c] = color
        return g
    return g
