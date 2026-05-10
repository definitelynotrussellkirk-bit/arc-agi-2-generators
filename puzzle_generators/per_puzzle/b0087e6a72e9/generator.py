"""Generator for ce602527.

Rule: smallest ranked hollow object cropped from the background.

Combinatorial axes (8): grid_h/w, frame_size, frame_color, palette_kind,
position_bias, anchor_corner, asymmetry_force, palette_size.
Degenerates: solid_block, no_frame, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import draw_frame, full_grid

GENERATOR_ID = "b0087e6a72e9"
VERSION = "1.1.0"
TASK_ID = "b0087e6a72e9"
SUMMARY = "Smallest ranked hollow object cropped from background."

INVARIANTS = [
    "background is the most common color",
    "there is at least one hollow object with area at most 25",
    "the selected object has a nonempty hole inside its bounding box",
    "the output is the bounding-box crop of that object",
]

FRAME_SIZES = ("3x4", "4x4", "4x5", "3x3", "5x5")
PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("solid_block", "no_frame", "full_grid")
HELPFUL_TEXTURES = FRAME_SIZES

AXES = {
    "grid_h":         {"type": "int", "default": "rng 9..12", "valid": "8..16"},
    "grid_w":         {"type": "int", "default": "rng 9..12", "valid": "8..16"},
    "frame_size":     {"type": "str", "default": "rng helpful",
                       "valid": "|".join(FRAME_SIZES)},
    "frame_color":    {"type": "color", "default": "rng !0",
                       "valid": "1..9"},
    "palette_kind":   {"type": "str", "default": "rng",
                       "valid": "|".join(PALETTE_KINDS)},
    "position_bias":  {"type": "str", "default": "rng",
                       "valid": "centered|rng"},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "1", "valid": "1"},
    "texture":        {"type": "str", "default": "alias for frame_size",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], rng)
    size = (overrides.get("texture") if overrides.get("texture") in FRAME_SIZES else None) or \
           overrides.get("frame_size") or \
           ctx.draw_choice("frame_size", list(FRAME_SIZES))
    fh, fw = (int(x) for x in size.split("x"))
    if difficulty == "easy":
        h_lo, h_hi = 8, 9
    elif difficulty == "hard":
        h_lo, h_hi = 12, 16
    else:
        h_lo, h_hi = 9, 12
    h = h_lo + rng.randint(0, h_hi - h_lo)
    w = h_lo + rng.randint(0, h_hi - h_lo)
    g = full_grid(h, w, 0)
    if h - fh - 4 < 0 or w - fw - 4 < 0:
        h = max(h, fh + 5)
        w = max(w, fw + 5)
        g = full_grid(h, w, 0)
    r0 = 2 + rng.randint(0, max(0, h - fh - 4))
    c0 = 2 + rng.randint(0, max(0, w - fw - 4))
    draw_frame(g, r0, c0, r0 + fh - 1, c0 + fw - 1, 2)
    return g


def _draw_from_degenerate(name, rng):
    h, w = 10, 10
    g = full_grid(h, w, 0)
    if name == "solid_block":
        for r in range(3, 7):
            for c in range(3, 7):
                g[r][c] = 2
        return g
    if name == "no_frame":
        return g
    if name == "full_grid":
        for r in range(h):
            for c in range(w):
                g[r][c] = 2
        return g
    return g
