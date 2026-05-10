"""Generator for puzzle 84f2aca1.

Rule: for each non-bg blob, compute strictly-inside bbox region; fill
0-cells there with 7 (or 5 if interior is exactly 1 cell).

Combinatorial axes (8): grid_h/w, n_frames, frame_h_min, frame_h_max,
frame_w_min, frame_w_max, color_kind, position_bias.
Degenerates: tiny_frame, full_grid_frame, single_dot.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, draw_rect_outline

GENERATOR_ID = "82e4aea30adc"
VERSION = "1.1.0"
TASK_ID = "82e4aea30adc"
SUMMARY = "Hollow rect frames; rule fills strict interior with 7 (or 5 for 1-cell)."

INVARIANTS = [
    "background is 0",
    ">=1 hollow rectangle frame >=3x3",
    "frames don't touch each other (4-conn)",
    "frame interior is 0 (rule fills it)",
]

POSITION_BIASES = ("spread", "corners", "row_aligned", "col_aligned",
                   "diagonal")
DEGENERATE_TEXTURES = ("tiny_frame", "full_grid_frame", "single_dot")
HELPFUL_TEXTURES = POSITION_BIASES

AXES = {
    "grid_h":         {"type": "int", "default": "rng 6..10", "valid": "5..14"},
    "grid_w":         {"type": "int", "default": "rng 7..11", "valid": "6..16"},
    "n_frames":       {"type": "int", "default": "rng 1..2", "valid": "1..3"},
    "frame_h_min":    {"type": "int", "default": "3", "valid": "3..6"},
    "frame_h_max":    {"type": "int", "default": "rng 4..5", "valid": "3..7"},
    "frame_w_min":    {"type": "int", "default": "3", "valid": "3..6"},
    "frame_w_max":    {"type": "int", "default": "rng 4..5", "valid": "3..7"},
    "position_bias":  {"type": "str", "default": "rng helpful",
                       "valid": "|".join(POSITION_BIASES)},
    "texture":        {"type": "str", "default": "alias for position_bias",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if difficulty == "easy":
        h_lo, h_hi = 5, 7
    elif difficulty == "hard":
        h_lo, h_hi = 10, 14
    else:
        h_lo, h_hi = 6, 10
    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", h_lo + 1, h_hi + 2)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], h, w, rng)
    n_frames = int(overrides.get("n_frames",
                                 ctx.draw_int("n_frames", 1, 2)))
    n_frames = max(1, min(3, n_frames))
    fh_min = int(overrides.get("frame_h_min", 3))
    fh_max = int(overrides.get("frame_h_max",
                               ctx.draw_int("frame_h_max", 4, 5)))
    fw_min = int(overrides.get("frame_w_min", 3))
    fw_max = int(overrides.get("frame_w_max",
                               ctx.draw_int("frame_w_max", 4, 5)))
    fh_min = max(3, min(fh_min, h))
    fh_max = max(fh_min, min(fh_max, h))
    fw_min = max(3, min(fw_min, w))
    fw_max = max(fw_min, min(fw_max, w))
    bias = (overrides.get("texture") or
            overrides.get("position_bias")
            or ctx.draw_choice("position_bias", list(POSITION_BIASES)))
    g = full_grid(h, w, 0)
    palette = list(ctx.draw_distinct_colors("colors",
                                            n=max(2, n_frames + 1),
                                            exclude={0, 5, 7}))
    placed_boxes = []
    placed = 0
    for attempt in range(n_frames * 8):
        if placed >= n_frames:
            break
        fh = rng.randint(fh_min, fh_max)
        fw = rng.randint(fw_min, fw_max)
        if fh > h or fw > w:
            continue
        rr, rc = _pick_position(bias, h, w, fh, fw, placed, rng)
        if rr is None:
            continue
        ok = all(not (rr - 1 <= or2 and rr + fh >= or1
                       and rc - 1 <= oc2 and rc + fw >= oc1)
                  for (or1, oc1, or2, oc2) in placed_boxes)
        if not ok:
            continue
        color = palette[placed % len(palette)]
        draw_rect_outline(g, rr, rc, fh, fw, color)
        placed_boxes.append((rr, rc, rr + fh - 1, rc + fw - 1))
        placed += 1
    if placed == 0:
        rr = max(0, (h - 4) // 2)
        rc = max(0, (w - 4) // 2)
        draw_rect_outline(g, rr, rc, 4, 4, palette[0])
    return g


def _pick_position(bias, h, w, fh, fw, idx, rng):
    if h - fh < 0 or w - fw < 0:
        return None, None
    if bias == "corners":
        corners = [(0, 0), (0, w - fw), (h - fh, 0), (h - fh, w - fw)]
        return corners[idx % 4]
    if bias == "row_aligned":
        rr = max(0, (h - fh) // 2)
        rc = idx * (fw + 1)
        if rc + fw > w:
            rc = rng.randint(0, w - fw)
        return rr, rc
    if bias == "col_aligned":
        rr = idx * (fh + 1)
        if rr + fh > h:
            rr = rng.randint(0, h - fh)
        return rr, max(0, (w - fw) // 2)
    if bias == "diagonal":
        rr = idx * (fh + 1)
        rc = idx * (fw + 1)
        if rr + fh > h: rr = rng.randint(0, h - fh)
        if rc + fw > w: rc = rng.randint(0, w - fw)
        return rr, rc
    return rng.randint(0, h - fh), rng.randint(0, w - fw)


def _draw_from_degenerate(name, h, w, rng):
    g = full_grid(h, w, 0)
    color = rng.choice([2, 3, 4, 6, 8, 9])
    if name == "tiny_frame":
        rr = max(0, (h - 3) // 2)
        rc = max(0, (w - 3) // 2)
        draw_rect_outline(g, rr, rc, 3, 3, color)
        return g
    if name == "full_grid_frame":
        draw_rect_outline(g, 0, 0, h, w, color)
        return g
    if name == "single_dot":
        g[h // 2][w // 2] = color
        return g
    return g
