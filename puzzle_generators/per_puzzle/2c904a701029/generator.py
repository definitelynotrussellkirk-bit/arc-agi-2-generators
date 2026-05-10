"""Generator for arc_additional_puzzles_21_set16_bundle:H108 — nested depth recoloring.

Rule: row 0 lists palette colors (non-zero, non-5). Body has nested rectangular
color-5 frames. Sort by size desc; recolor each frame to palette[i]
(last color repeats if more frames than palette entries). Output keeps row 0
and the recolored body.

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, n_frames, texture.
Degenerates: no_palette, no_frames, single_frame.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import draw_frame, full_grid

GENERATOR_ID = "2c904a701029"
VERSION = "1.1.0"
TASK_ID = "2c904a701029"

SUMMARY = "Top-row palette + body of nested color-5 frames recolored by depth."

INVARIANTS = [
    "background is 0",
    "row 0 has 2-4 distinct palette colors at distinct columns (no 0 or 5)",
    "body has 2-4 nested rectangular color-5 frames (concentric, 2-cell separation)",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_palette", "no_frames", "single_frame")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_w":         {"type": "int", "default": "rng 11..14", "valid": "10..18"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_frames":       {"type": "int", "default": "rng 2..4", "valid": "2..5"},
    "palette_size":   {"type": "int", "default": "rng 2..4", "valid": "2..5"},
    "position_bias":  {"type": "str", "default": "concentric_5_frames",
                       "valid": "concentric_5_frames"},
    "n_distinct_colors": {"type": "int", "default": "= palette_size+1", "valid": "3..6"},
    "density":        {"type": "str", "default": "balanced", "valid": "balanced"},
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
        w = ctx.draw_int("grid_w", 11, 11)
        n_frames = ctx.draw_int("n_frames", 2, 2)
    elif difficulty == "hard":
        w = ctx.draw_int("grid_w", 14, 17)
        n_frames = ctx.draw_int("n_frames", 4, 5)
    else:
        w = ctx.draw_int("grid_w", 11, 14)
        n_frames = ctx.draw_int("n_frames", 2, 4)
    rng = ctx.draw_rng("layout")

    body_h = w
    h = body_h + 1
    max_frames = (min(h - 1, w) - 3) // 2 + 1
    n_frames = min(n_frames, max_frames)
    palette_size = rng.randint(min(2, n_frames), n_frames)
    palette_colors = rng.sample([1, 2, 3, 4, 6, 7, 8, 9], palette_size)

    for outer in range(40):
        g = full_grid(h, w, 0)
        cols0 = rng.sample(range(w), palette_size)
        cols0.sort()
        for col, color in zip(cols0, palette_colors):
            g[0][col] = color

        r1, c1, r2, c2 = 1, 0, h - 1, w - 1
        drawn = 0
        for fi in range(n_frames):
            if r2 - r1 < 2 or c2 - c1 < 2:
                break
            draw_frame(g, r1, c1, r2, c2, 5)
            drawn += 1
            r1 += 2; c1 += 2; r2 -= 2; c2 -= 2
        if drawn < 2:
            continue
        return g
    raise ValueError("could not realize nested-5-frames layout in 40 attempts")


def _draw_from_degenerate(name, rng):
    w = 11
    body_h = w
    h = body_h + 1
    g = full_grid(h, w, 0)
    if name == "no_palette":
        # Frames in body but row 0 has no palette colors — rule has no
        # depth-to-color mapping to apply.
        r1, c1, r2, c2 = 1, 0, h - 1, w - 1
        for _ in range(3):
            if r2 - r1 < 2 or c2 - c1 < 2: break
            draw_frame(g, r1, c1, r2, c2, 5)
            r1 += 2; c1 += 2; r2 -= 2; c2 -= 2
        return g
    if name == "no_frames":
        # Palette in row 0 but body is empty — rule has no frames
        # to recolor.
        g[0][1] = 3; g[0][5] = 7; g[0][9] = 4
        return g
    if name == "single_frame":
        # Palette + only one frame — rule's depth-ordering has only
        # one entry; nesting hierarchy is degenerate.
        g[0][1] = 3; g[0][5] = 7
        draw_frame(g, 1, 0, h - 1, w - 1, 5)
        return g
    return g
