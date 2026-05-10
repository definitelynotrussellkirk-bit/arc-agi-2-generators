"""Generator for arc_additional_puzzles_21_set20_bundle:H136 — nested palette fill.

Rule: column 0 lists palette colors (top-to-bottom, ignoring 0 and 8). Body
contains nested rectangular color-8 frames. Each 0-cell inside the nested
frames gets filled by palette[depth - 1] where depth = how many frames contain it.

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: no_palette, no_frames, single_frame.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import draw_frame, full_grid

GENERATOR_ID = "fe0dc9f32b7b"
VERSION = "1.1.0"
TASK_ID = "fe0dc9f32b7b"

SUMMARY = "Column-0 palette + nested rectangular color-8 frames recolored by depth."

INVARIANTS = [
    "background is 0",
    "column 0 has 2-4 distinct non-zero non-8 palette colors at distinct rows",
    "body has 2-4 nested rectangular color-8 frames (concentric, 2-cell separation)",
    "frames are placed offset from column 0 (left margin >= 2 to leave room for palette)",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_palette", "no_frames", "single_frame")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 11..14", "valid": "10..18"},
    "grid_w":         {"type": "int", "default": "rng 12..14", "valid": "11..18"},
    "n_frames":       {"type": "int", "default": "rng 2..4", "valid": "2..5"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "palette_size":   {"type": "int", "default": "rng 2..4", "valid": "2..5"},
    "position_bias":  {"type": "str", "default": "col0_palette_nested_frames",
                       "valid": "col0_palette_nested_frames"},
    "n_distinct_colors": {"type": "int", "default": "rng 2..4", "valid": "2..5"},
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
        h = ctx.draw_int("grid_h", 11, 11)
        w = ctx.draw_int("grid_w", 12, 12)
        n_frames = ctx.draw_int("n_frames", 2, 2)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 13, 16)
        w = ctx.draw_int("grid_w", 13, 16)
        n_frames = ctx.draw_int("n_frames", 3, 5)
    else:
        h = ctx.draw_int("grid_h", 11, 14)
        w = ctx.draw_int("grid_w", 12, 14)
        n_frames = ctx.draw_int("n_frames", 2, 4)
    rng = ctx.draw_rng("layout")

    frame_box = (1, 3, h - 2, w - 1)
    fr1, fc1, fr2, fc2 = frame_box
    max_frames = (min(fr2 - fr1, fc2 - fc1) - 1) // 2 + 1
    n_frames = min(n_frames, max_frames)
    palette_size = rng.randint(min(2, n_frames), n_frames)
    palette_colors = rng.sample([1, 2, 3, 4, 5, 6, 7, 9], palette_size)

    for outer in range(40):
        g = full_grid(h, w, 0)
        rows0 = rng.sample(range(h), palette_size)
        rows0.sort()
        for r0, color in zip(rows0, palette_colors):
            g[r0][0] = color

        r1, c1, r2, c2 = fr1, fc1, fr2, fc2
        drawn = 0
        for fi in range(n_frames):
            if r2 - r1 < 2 or c2 - c1 < 2:
                break
            draw_frame(g, r1, c1, r2, c2, 8)
            drawn += 1
            r1 += 2; c1 += 2; r2 -= 2; c2 -= 2
        if drawn < 2:
            continue
        return g
    raise ValueError("could not realize nested-frames layout in 40 attempts")


def _draw_from_degenerate(name, rng):
    h, w = 11, 13
    g = full_grid(h, w, 0)
    if name == "no_palette":
        # Frames but no col-0 palette — rule's "palette[depth-1]"
        # is undefined; recolor branch never fires.
        draw_frame(g, 1, 3, h - 2, w - 1, 8)
        draw_frame(g, 3, 5, h - 4, w - 3, 8)
        return g
    if name == "no_frames":
        # Palette but no nested frames — rule has no depth-counted
        # cells to recolor.
        g[2][0] = 4; g[5][0] = 6; g[8][0] = 7
        return g
    if name == "single_frame":
        # Only one frame — rule's nested-depth branch collapses to
        # depth=1 everywhere inside; only first palette color used.
        g[2][0] = 4; g[5][0] = 6
        draw_frame(g, 1, 3, h - 2, w - 1, 8)
        return g
    return g
