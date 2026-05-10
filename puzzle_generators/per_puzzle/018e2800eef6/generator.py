"""Generator for arc_puzzle_bank_21_set11_bundle:hard_k19 — move framed motif via key.

Rule: move a framed source motif into an empty target frame using an
external transform key (1=flip-lr, 2=flip-ud, 3=180).

Combinatorial axes (8): grid_h, grid_w, palette_kind, key,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_key, both_frames_filled, no_target_frame.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import draw_frame, full_grid

GENERATOR_ID = "018e2800eef6"
VERSION = "1.1.0"
TASK_ID = "018e2800eef6"
SUMMARY = "Move a framed source motif into an empty target frame using an external transform key."

INVARIANTS = [
    "there are two same-size rectangular frames in colors 6 and 7",
    "one frame has a nonzero interior motif and the other interior is empty",
    "an external marker color 1, 2, or 3 chooses horizontal flip, vertical flip, or 180-degree rotation",
    "the output preserves frames and places the transformed motif in the empty frame",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_key", "both_frames_filled", "no_target_frame")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "11", "valid": "11..11"},
    "grid_w":         {"type": "int", "default": "15", "valid": "15..15"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "key":            {"type": "int", "default": "rng 1..3", "valid": "1..3"},
    "motif":          {"type": "int", "default": "rng 0..3", "valid": "0..3"},
    "palette_size":   {"type": "int", "default": "6", "valid": "6..6"},
    "position_bias":  {"type": "str", "default": "two_frames_with_external_key",
                       "valid": "two_frames_with_external_key"},
    "n_distinct_colors": {"type": "int", "default": "6", "valid": "6..6"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}

_MOTIFS = [
    [(0, 0, 4), (0, 2, 5), (1, 1, 8), (2, 0, 5), (2, 2, 4)],
    [(0, 1, 8), (1, 0, 4), (1, 2, 5), (2, 1, 9)],
    [(0, 0, 4), (1, 1, 5), (1, 2, 8), (2, 0, 9)],
    [(0, 2, 4), (1, 0, 8), (1, 1, 5), (2, 2, 9)],
]


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index, version=VERSION,
                  task_id=TASK_ID, difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        key = ctx.draw_int("key", 1, 1)
    elif difficulty == "hard":
        key = ctx.draw_int("key", 2, 3)
    else:
        key = ctx.draw_int("key", 1, 3)
    motif = ctx.draw_int("motif", 0, len(_MOTIFS) - 1)
    g = full_grid(11, 15, 0)
    g[0][7] = key
    draw_frame(g, 3, 2, 7, 7, 6)
    draw_frame(g, 3, 9, 7, 14, 7)
    for r, c, color in _MOTIFS[motif]:
        g[4 + r][3 + c] = color
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(11, 15, 0)
    if name == "no_key":
        # both frames + motif but no external transform key → undefined transform
        draw_frame(g, 3, 2, 7, 7, 6)
        draw_frame(g, 3, 9, 7, 14, 7)
        for r, c, color in _MOTIFS[0]:
            g[4 + r][3 + c] = color
        return g
    if name == "both_frames_filled":
        # both frames have motifs → no empty target frame
        g[0][7] = 1
        draw_frame(g, 3, 2, 7, 7, 6)
        draw_frame(g, 3, 9, 7, 14, 7)
        for r, c, color in _MOTIFS[0]:
            g[4 + r][3 + c] = color
            g[4 + r][10 + c] = color
        return g
    if name == "no_target_frame":
        # source frame + motif but no second (target) frame → nowhere to place
        g[0][7] = 2
        draw_frame(g, 3, 2, 7, 7, 6)
        for r, c, color in _MOTIFS[0]:
            g[4 + r][3 + c] = color
        return g
    return g
