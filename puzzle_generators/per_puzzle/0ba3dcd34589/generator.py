"""Generator for arc_puzzle_bank_21_set11_s:S11_E2 — Fill frame interiors with 8.

Rule: each hollow-rectangle frame's interior cells get filled with 8.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_frames,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_frames, solid_rects, frame_too_thin.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, draw_rect_outline

GENERATOR_ID = "0ba3dcd34589"
VERSION = "1.1.0"
TASK_ID = "0ba3dcd34589"
SUMMARY = "2-3 hollow rectangle frames (≥3×3 each), distinct colors, well separated."

INVARIANTS = [
    "2-3 frames, each is a perfect hollow rectangle ≥3×3",
    "each frame uses a distinct non-bg color (and not 8)",
    "frames don't touch (≥1 bg cell apart)",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_frames", "solid_rects", "frame_too_thin")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 7..9", "valid": "5..12"},
    "grid_w":         {"type": "int", "default": "rng 11..14", "valid": "9..18"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_frames":       {"type": "int", "default": "rng 2..3", "valid": "2..3"},
    "palette_size":   {"type": "int", "default": "rng 2..3", "valid": "2..3"},
    "position_bias":  {"type": "str", "default": "separated_hollow_frames",
                       "valid": "separated_hollow_frames"},
    "n_distinct_colors": {"type": "int", "default": "rng 2..3", "valid": "2..3"},
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
        h = ctx.draw_int("grid_h", 7, 7)
        w = ctx.draw_int("grid_w", 11, 12)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("grid_w", 13, 14)
    else:
        h = ctx.draw_int("grid_h", 7, 9)
        w = ctx.draw_int("grid_w", 11, 14)
    g = full_grid(h, w, 0)
    rng = ctx.draw_rng("layout")
    palette = rng.sample([2, 3, 4, 6, 7, 9], 3)
    occupied_cols = []
    for color in palette[:rng.randint(2, 3)]:
        for _ in range(40):
            fh = rng.randint(3, min(5, h - 2))
            fw = rng.randint(3, min(5, w - 2))
            r0 = rng.randint(1, h - fh - 1)
            c0 = rng.randint(1, w - fw - 1)
            if any(abs(c0 - oc) < (fw + 1) and abs(r0 - or_) < (fh + 1)
                   for oc, or_ in occupied_cols):
                continue
            draw_rect_outline(g, r0, c0, fh, fw, color)
            occupied_cols.append((c0, r0))
            break
    return g


def _draw_from_degenerate(name, rng):
    h, w = 8, 12
    g = full_grid(h, w, 0)
    if name == "no_frames":
        # blank → no frames to fill
        return g
    if name == "solid_rects":
        # solid rects (not frames) → "hollow frame" precondition fails
        for r in range(2, 5):
            for c in range(2, 5):
                g[r][c] = 4
        return g
    if name == "frame_too_thin":
        # 2x2 frame → no proper interior to fill
        g[1][1] = 4; g[1][2] = 4
        g[2][1] = 4; g[2][2] = 4
        return g
    return g
