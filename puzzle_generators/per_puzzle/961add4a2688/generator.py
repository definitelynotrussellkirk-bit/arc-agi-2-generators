"""Generator for arc_additional_puzzles_21_set8:M51 — gravity-up scattered markers within an 8-frame.

Rule: a single 8-color rectangle frame contains scattered non-zero
markers in its strict interior. Output: frame preserved; for each
interior column, the markers in that column are packed at the top of
the column (gravity up).

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_markers,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_frame, no_markers, full_interior.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, draw_frame

GENERATOR_ID = "961add4a2688"
VERSION = "1.1.0"
TASK_ID = "961add4a2688"
SUMMARY = "8-color rectangle frame with 4-7 scattered non-0/non-8 markers in its interior."

INVARIANTS = [
    "background is 0",
    "exactly one full-perimeter 8-color rectangle frame ≥6×6",
    "4-7 markers in the strict interior, each with a color != 8",
    "markers are placed in random interior positions (no overlap)",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_frame", "no_markers", "full_interior")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 9..11", "valid": "8..14"},
    "grid_w":         {"type": "int", "default": "rng 10..12", "valid": "9..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_markers":      {"type": "int", "default": "rng 4..7", "valid": "2..12"},
    "palette_size":   {"type": "int", "default": "rng 4..7", "valid": "2..8"},
    "position_bias":  {"type": "str", "default": "frame_with_markers",
                       "valid": "frame_with_markers"},
    "n_distinct_colors": {"type": "int", "default": "rng 4..7", "valid": "2..8"},
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
        h = ctx.draw_int("grid_h", 9, 9)
        w = ctx.draw_int("grid_w", 10, 10)
        n_markers = ctx.draw_int("n_markers", 3, 4)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 10, 11)
        w = ctx.draw_int("grid_w", 11, 12)
        n_markers = ctx.draw_int("n_markers", 6, 7)
    else:
        h = ctx.draw_int("grid_h", 9, 11)
        w = ctx.draw_int("grid_w", 10, 12)
        n_markers = ctx.draw_int("n_markers", 4, 7)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    rh = rng.randint(7, h - 1)
    rw = rng.randint(7, w - 1)
    r1 = rng.randint(0, h - rh)
    c1 = rng.randint(0, w - rw)
    r2 = r1 + rh - 1
    c2 = c1 + rw - 1
    draw_frame(g, r1, c1, r2, c2, 8)
    interior = [(r, c) for r in range(r1 + 1, r2) for c in range(c1 + 1, c2)]
    rng.shuffle(interior)
    for r, c in interior[:n_markers]:
        g[r][c] = rng.choice([1, 2, 3, 4, 5, 6, 7, 9])
    return g


def _draw_from_degenerate(name, rng):
    h, w = 9, 10
    g = full_grid(h, w, 0)
    if name == "no_frame":
        # markers but no enclosing 8-frame → no container, gravity has no top
        g[2][3] = 4; g[5][6] = 6; g[3][7] = 7
        return g
    if name == "no_markers":
        # frame with empty interior → gravity-up is identity
        draw_frame(g, 1, 1, 7, 8, 8)
        return g
    if name == "full_interior":
        # interior totally filled → gravity-up has no slots to drop into
        draw_frame(g, 1, 1, 7, 8, 8)
        for r in range(2, 7):
            for c in range(2, 8):
                g[r][c] = 4
        return g
    return g
