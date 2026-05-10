"""Generator for arc_additional_puzzles_21_set2:H13 — Crop most-seeded 1-frame, fill 0s with 3.

Rule: among 1-frames, pick the one with most 2-seeds inside; crop;
replace remaining 0s with 3.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_frames,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_frames, no_seeds, equal_seed_counts.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, draw_rect_outline

GENERATOR_ID = "252ff772a276"
VERSION = "1.1.0"
TASK_ID = "252ff772a276"
SUMMARY = "2 1-frames, each ≥4×4 with 1-3 2-cells inside (one has more)."

INVARIANTS = [
    "2 1-color frames, each ≥4×4",
    "each frame has 1-3 2-cells inside; one frame has strictly more 2s",
    "frames don't touch (≥1 bg cell apart)",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_frames", "no_seeds", "equal_seed_counts")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 10..14", "valid": "8..16"},
    "grid_w":         {"type": "int", "default": "rng 12..15", "valid": "10..18"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_frames":       {"type": "int", "default": "2", "valid": "2..3"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2..2"},
    "position_bias":  {"type": "str", "default": "two_1frames_with_seeds",
                       "valid": "two_1frames_with_seeds"},
    "n_distinct_colors": {"type": "int", "default": "2", "valid": "2..2"},
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
        w = ctx.draw_int("grid_w", 12, 13)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 13, 14)
        w = ctx.draw_int("grid_w", 14, 15)
    else:
        h = ctx.draw_int("grid_h", 10, 14)
        w = ctx.draw_int("grid_w", 12, 15)
    g = full_grid(h, w, 0)
    rng = ctx.draw_rng("layout")
    placed = []
    seed_counts = rng.sample([2, 3], 2)  # distinct counts
    for n_seeds in seed_counts:
        for _ in range(40):
            fh = rng.randint(4, 5); fw = rng.randint(5, 6)
            r0 = rng.randint(0, h - fh); c0 = rng.randint(0, w - fw)
            if any(abs(r0 - pr) < (fh + 2) and abs(c0 - pc) < (fw + 2) for pr, pc in placed):
                continue
            draw_rect_outline(g, r0, c0, fh, fw, 1)
            interior_cells = [(r, c) for r in range(r0 + 1, r0 + fh - 1) for c in range(c0 + 1, c0 + fw - 1)]
            rng.shuffle(interior_cells)
            for cell in interior_cells[:n_seeds]:
                g[cell[0]][cell[1]] = 2
            placed.append((r0, c0))
            break
    return g


def _draw_from_degenerate(name, rng):
    h, w = 11, 13
    g = full_grid(h, w, 0)
    if name == "no_frames":
        # 2-seeds without 1-frames → no enclosure to compare
        for r, c in [(2, 2), (3, 3), (5, 5), (6, 6)]: g[r][c] = 2
        return g
    if name == "no_seeds":
        # 1-frames without 2-seeds → no count to maximize over
        draw_rect_outline(g, 1, 1, 4, 5, 1)
        draw_rect_outline(g, 6, 7, 4, 5, 1)
        return g
    if name == "equal_seed_counts":
        # 2 frames with equal seed counts → ambiguous "most" pick
        draw_rect_outline(g, 1, 1, 4, 5, 1)
        draw_rect_outline(g, 6, 7, 4, 5, 1)
        g[2][2] = 2; g[3][3] = 2  # 2 seeds in frame A
        g[7][8] = 2; g[8][9] = 2  # 2 seeds in frame B (tied)
        return g
    return g
