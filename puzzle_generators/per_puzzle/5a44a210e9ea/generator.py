"""Generator for arc_additional_puzzles_21_set13_bundle:H87 — palette-depth nested frames.

Rule: row 0 lists palette colors (non-zero). Body (rows 1..h-1) holds nested
rectangular color-1 frames. Sort frames by size desc; recolor frame[i] with
palette[i] (last color repeats if more frames than colors). Output the body.

Combinatorial axes (8): grid_w, palette_kind, n_frames, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: no_palette, no_frames, single_frame.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import draw_frame, full_grid

GENERATOR_ID = "5a44a210e9ea"
VERSION = "1.1.0"
TASK_ID = "5a44a210e9ea"

SUMMARY = "Top-row palette + body of N nested color-1 frames recolored by depth."

INVARIANTS = [
    "background is 0",
    "row 0 has 2-4 distinct non-zero palette colors at distinct columns",
    "body has 2-4 nested rectangular color-1 frames (concentric, 2-cell separation)",
    "frames are perfect rectangular borders (no extras)",
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
    "position_bias":  {"type": "str", "default": "palette_row0_then_nested_frames",
                       "valid": "palette_row0_then_nested_frames"},
    "n_distinct_colors": {"type": "int", "default": "rng 3..5", "valid": "2..6"},
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
        w = ctx.draw_int("grid_w", 11, 12)
        n_frames = ctx.draw_int("n_frames", 2, 2)
    elif difficulty == "hard":
        w = ctx.draw_int("grid_w", 13, 16)
        n_frames = ctx.draw_int("n_frames", 3, 4)
    else:
        w = ctx.draw_int("grid_w", 11, 14)
        n_frames = ctx.draw_int("n_frames", 2, 4)
    rng = ctx.draw_rng("layout")

    body_h = w
    h = body_h + 1
    min_dim = 3 + 2 * (n_frames - 1)
    if min_dim > w:
        n_frames = max(1, (w - 3) // 2 + 1)

    palette_size = rng.randint(min(2, n_frames), n_frames)
    palette_colors = rng.sample([2, 3, 4, 5, 6, 7, 8, 9], palette_size)

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
            draw_frame(g, r1, c1, r2, c2, 1)
            drawn += 1
            r1 += 2; c1 += 2; r2 -= 2; c2 -= 2
        if drawn < 2:
            continue
        return g
    raise ValueError("could not realize nested frame layout in 40 attempts")


def _draw_from_degenerate(name, rng):
    w = 12
    h = 13
    g = full_grid(h, w, 0)
    if name == "no_palette":
        # Row 0 empty — rule has no colors to recolor frames with.
        draw_frame(g, 1, 0, h - 1, w - 1, 1)
        draw_frame(g, 3, 2, h - 3, w - 3, 1)
        return g
    if name == "no_frames":
        # Palette but no nested frames — rule has nothing to recolor.
        g[0][2] = 4; g[0][6] = 5
        return g
    if name == "single_frame":
        # Only one frame — rule's depth ranking is trivial.
        g[0][2] = 4; g[0][6] = 5
        draw_frame(g, 1, 0, h - 1, w - 1, 1)
        return g
    return g
