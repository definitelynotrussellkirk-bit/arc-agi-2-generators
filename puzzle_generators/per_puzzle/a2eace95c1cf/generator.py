"""Generator for arc_additional_puzzles_21_set14_bundle:M98 — Fill rect frames with seed color.

Rule: each rectangle frame with one non-frame seed cell inside gets
its interior filled with the seed's color.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_frames,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_frames, no_seeds, multiple_seeds_per_frame.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, draw_rect_outline

GENERATOR_ID = "a2eace95c1cf"
VERSION = "1.1.0"
TASK_ID = "a2eace95c1cf"
SUMMARY = "2 rectangle frames, each ≥4×4 with one seed cell inside (different from frame color)."

INVARIANTS = [
    "2 distinct rectangle frames, each ≥4×4",
    "each frame has exactly one non-zero non-border cell inside (seed)",
    "frames don't touch (≥1 bg cell apart)",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_frames", "no_seeds", "multiple_seeds_per_frame")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..10", "valid": "6..14"},
    "grid_w":         {"type": "int", "default": "rng 11..14", "valid": "9..18"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_frames":       {"type": "int", "default": "2", "valid": "1..3"},
    "palette_size":   {"type": "int", "default": "4", "valid": "4..4"},
    "position_bias":  {"type": "str", "default": "framed_seeds",
                       "valid": "framed_seeds"},
    "n_distinct_colors": {"type": "int", "default": "4", "valid": "4..4"},
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
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("grid_w", 11, 12)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 13, 14)
    else:
        h = ctx.draw_int("grid_h", 8, 10)
        w = ctx.draw_int("grid_w", 11, 14)
    g = full_grid(h, w, 0)
    rng = ctx.draw_rng("layout")
    placed = []
    for _ in range(2):
        for _ in range(40):
            fh = rng.randint(4, 5); fw = rng.randint(4, 5)
            r0 = rng.randint(1, h - fh - 1); c0 = rng.randint(1, w - fw - 1)
            if any(abs(r0 - pr) < (fh + 2) and abs(c0 - pc) < (fw + 2) for pr, pc in placed):
                continue
            border, seed = rng.sample([1, 2, 3, 4, 5, 6, 7, 8, 9], 2)
            draw_rect_outline(g, r0, c0, fh, fw, border)
            sr = rng.randint(r0 + 1, r0 + fh - 2)
            sc = rng.randint(c0 + 1, c0 + fw - 2)
            g[sr][sc] = seed
            placed.append((r0, c0))
            break
    return g


def _draw_from_degenerate(name, rng):
    h, w = 9, 12
    g = full_grid(h, w, 0)
    if name == "no_frames":
        # seeds without frames → no enclosure to fill
        g[3][3] = 4
        g[5][7] = 6
        return g
    if name == "no_seeds":
        # frames without seeds → no fill color defined
        draw_rect_outline(g, 1, 1, 4, 4, 4)
        draw_rect_outline(g, 1, 7, 4, 4, 6)
        return g
    if name == "multiple_seeds_per_frame":
        # 2 seeds in one frame → ambiguous fill color
        draw_rect_outline(g, 1, 1, 4, 4, 4)
        g[2][2] = 6; g[3][3] = 7  # 2 seeds in same frame
        draw_rect_outline(g, 1, 7, 4, 4, 8)
        g[2][8] = 9
        return g
    return g
