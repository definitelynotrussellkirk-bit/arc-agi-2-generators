"""Generator for arc_additional_puzzle_bank_volume7:E48.

Odd-sized hollow red rectangles receive a cyan center dot.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_frames,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_frames, even_size_frames, filled_centers.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import draw_rect_outline, full_grid

GENERATOR_ID = "02b1f274e160"
VERSION = "1.1.0"
TASK_ID = "02b1f274e160"
SUMMARY = "Odd-sized hollow red rectangles receive a cyan center dot."

INVARIANTS = [
    "background is 0",
    "target red components are hollow rectangles with odd height and width",
    "center cells start empty",
    "frames are separated and not nested",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_frames", "even_size_frames", "filled_centers")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 11..15", "valid": "5..22"},
    "grid_w":         {"type": "int", "default": "rng 11..15", "valid": "5..22"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_frames":       {"type": "int", "default": "rng 1..3", "valid": "1..6"},
    "palette_size":   {"type": "int", "default": "1", "valid": "1..1"},
    "position_bias":  {"type": "str", "default": "separated_odd_frames",
                       "valid": "separated_odd_frames"},
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
        h = ctx.draw_int("grid_h", 11, 12)
        w = ctx.draw_int("grid_w", 11, 12)
        n_frames = ctx.draw_int("n_frames", 1, 1)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 14, 15)
        w = ctx.draw_int("grid_w", 14, 15)
        n_frames = ctx.draw_int("n_frames", 2, 3)
    else:
        h = ctx.draw_int("grid_h", 11, 15)
        w = ctx.draw_int("grid_w", 11, 15)
        n_frames = ctx.draw_int("n_frames", 1, 3)
    rng = ctx.draw_rng("placement")
    g = full_grid(h, w, 0)
    boxes: list[tuple[int, int, int, int]] = []
    for _ in range(220):
        if len(boxes) >= n_frames:
            break
        rh = rng.choice([3, 5])
        rw = rng.choice([3, 5])
        r = rng.randint(0, h - rh)
        c = rng.randint(0, w - rw)
        if any(not (r + rh + 1 < ar or ar + ah + 1 < r or c + rw + 1 < ac or ac + aw + 1 < c)
               for ar, ac, ah, aw in boxes):
            continue
        draw_rect_outline(g, r, c, rh, rw, 2)
        boxes.append((r, c, rh, rw))
    if not boxes:
        draw_rect_outline(g, 1, 1, 5, 5, 2)
    return g


def _draw_from_degenerate(name, rng):
    h, w = 12, 12
    g = full_grid(h, w, 0)
    if name == "no_frames":
        # blank → no frames to add center dots to
        return g
    if name == "even_size_frames":
        # frame with even height/width → no integer center cell
        draw_rect_outline(g, 1, 1, 4, 4, 2)
        draw_rect_outline(g, 6, 6, 4, 4, 2)
        return g
    if name == "filled_centers":
        # odd-sized frames but centers already non-zero → "center is empty" precondition fails
        draw_rect_outline(g, 1, 1, 5, 5, 2)
        g[3][3] = 4  # already filled
        draw_rect_outline(g, 7, 7, 3, 3, 2)
        g[8][8] = 6  # already filled
        return g
    return g
