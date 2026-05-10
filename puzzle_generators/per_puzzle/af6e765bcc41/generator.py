"""Generator for arc_additional_puzzle_bank_volume17:E117.

Hollow orange rectangular frames have their interiors filled cyan.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_frames,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_frames, solid_rects, frame_too_thin.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import draw_rect_outline, full_grid

GENERATOR_ID = "af6e765bcc41"
VERSION = "1.1.0"
TASK_ID = "af6e765bcc41"
SUMMARY = "Hollow orange rectangular frames have their interiors filled cyan."

INVARIANTS = [
    "background is 0",
    "each orange component is a hollow rectangular frame",
    "frame interiors start empty",
    "frames are separated and not nested",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_frames", "solid_rects", "frame_too_thin")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 10..14", "valid": "5..22"},
    "grid_w":         {"type": "int", "default": "rng 10..14", "valid": "5..22"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_frames":       {"type": "int", "default": "rng 1..3", "valid": "1..6"},
    "palette_size":   {"type": "int", "default": "1", "valid": "1..1"},
    "position_bias":  {"type": "str", "default": "separated_hollow_frames",
                       "valid": "separated_hollow_frames"},
    "n_distinct_colors": {"type": "int", "default": "1", "valid": "1..1"},
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
        h = ctx.draw_int("grid_h", 10, 11)
        w = ctx.draw_int("grid_w", 10, 11)
        n_frames = ctx.draw_int("n_frames", 1, 1)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 13, 14)
        w = ctx.draw_int("grid_w", 13, 14)
        n_frames = ctx.draw_int("n_frames", 2, 3)
    else:
        h = ctx.draw_int("grid_h", 10, 14)
        w = ctx.draw_int("grid_w", 10, 14)
        n_frames = ctx.draw_int("n_frames", 1, 3)
    rng = ctx.draw_rng("placement")
    g = full_grid(h, w, 0)
    boxes: list[tuple[int, int, int, int]] = []
    for _ in range(220):
        if len(boxes) >= n_frames:
            break
        rh = rng.randint(4, min(6, h))
        rw = rng.randint(4, min(6, w))
        r = rng.randint(0, h - rh)
        c = rng.randint(0, w - rw)
        if any(not (r + rh + 1 < ar or ar + ah + 1 < r or c + rw + 1 < ac or ac + aw + 1 < c)
               for ar, ac, ah, aw in boxes):
            continue
        draw_rect_outline(g, r, c, rh, rw, 7)
        boxes.append((r, c, rh, rw))
    if not boxes:
        draw_rect_outline(g, 1, 1, 4, 4, 7)
    return g


def _draw_from_degenerate(name, rng):
    h, w = 11, 11
    g = full_grid(h, w, 0)
    if name == "no_frames":
        # blank → no frames to fill
        return g
    if name == "solid_rects":
        # solid rects (not hollow) → "hollow frame" precondition fails
        for r in range(2, 6):
            for c in range(2, 6):
                g[r][c] = 7
        return g
    if name == "frame_too_thin":
        # 2-cell-thick frame → no proper interior to fill
        g[1][1] = 7; g[1][2] = 7
        g[2][1] = 7; g[2][2] = 7
        return g
    return g
