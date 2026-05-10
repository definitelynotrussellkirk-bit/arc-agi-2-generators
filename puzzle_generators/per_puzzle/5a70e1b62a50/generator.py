"""Generator for arc_additional_puzzles_21_set11_bundle:E76.

Rule: closed same-color frames have their zero interiors filled with the frame color.

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: no_frames, open_frame, frame_at_border.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import draw_frame, full_grid

GENERATOR_ID = "5a70e1b62a50"
VERSION = "1.1.0"
TASK_ID = "5a70e1b62a50"
SUMMARY = "One or two closed rectangular frames with zero interiors."

INVARIANTS = [
    "background is 0",
    "each nonzero object is a closed rectangular frame",
    "frame interiors are zero and do not touch the grid border",
    "each enclosed zero region has exactly one neighboring color",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_frames", "open_frame", "frame_at_border")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 7..11", "valid": "6..14"},
    "grid_w":         {"type": "int", "default": "rng 8..13", "valid": "6..16"},
    "frame_count":    {"type": "int", "default": "rng 1..2", "valid": "1..2"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "palette_size":   {"type": "int", "default": "rng 1..2", "valid": "1..2"},
    "position_bias":  {"type": "str", "default": "scattered_closed_frames",
                       "valid": "scattered_closed_frames"},
    "n_distinct_colors": {"type": "int", "default": "rng 1..2", "valid": "1..2"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def _overlaps_with_margin(a, b, margin=1):
    ar1, ac1, ar2, ac2 = a
    br1, bc1, br2, bc2 = b
    return not (
        ar2 + margin < br1
        or br2 + margin < ar1
        or ac2 + margin < bc1
        or bc2 + margin < ac1
    )


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 7, 8)
        w = ctx.draw_int("grid_w", 8, 9)
        frame_count = ctx.draw_int("frame_count", 1, 1)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 11, 13)
        w = ctx.draw_int("grid_w", 13, 15)
        frame_count = ctx.draw_int("frame_count", 2, 2)
    else:
        h = ctx.draw_int("grid_h", 7, 11)
        w = ctx.draw_int("grid_w", 8, 13)
        frame_count = ctx.draw_int("frame_count", 1, 2)
    colors = ctx.draw_distinct_colors("colors", n=frame_count, exclude={0})
    rng = ctx.draw_rng("layout")

    g = full_grid(h, w, 0)
    frames = []
    for color in colors:
        placed = False
        for _ in range(200):
            rh = rng.randint(4, min(7, h - 2))
            rw = rng.randint(4, min(8, w - 2))
            r1 = rng.randint(1, h - rh - 1)
            c1 = rng.randint(1, w - rw - 1)
            bbox = (r1, c1, r1 + rh - 1, c1 + rw - 1)
            if all(not _overlaps_with_margin(bbox, other) for other in frames):
                draw_frame(g, *bbox, color)
                frames.append(bbox)
                placed = True
                break
        if not placed:
            break
    return g


def _draw_from_degenerate(name, rng):
    h, w = 9, 11
    g = full_grid(h, w, 0)
    if name == "no_frames":
        # Empty grid — rule has no frames to fill.
        return g
    if name == "open_frame":
        # 3-walls of a rectangle (one missing) — rule's "closed
        # frame" filter excludes; output equals input.
        for c in range(2, 7): g[2][c] = 4
        for r in range(2, 6): g[r][2] = 4
        for r in range(2, 6): g[r][6] = 4
        return g
    if name == "frame_at_border":
        # Frame placed flush against the grid border — rule's
        # "interior touches border" precondition violated; the
        # frame's interior region is part of the unbounded "outside".
        draw_frame(g, 0, 0, 5, 6, 4)
        return g
    return g
