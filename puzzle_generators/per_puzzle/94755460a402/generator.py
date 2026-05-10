"""Generator for arc_additional_puzzles_21_set20_bundle:H140 — Selector + cmd; pick frame, crop interior, transform.

Rule: selector at (0,0); cmd at (0,1). Find rect-frame matching selector
color; crop interior; apply cmd: 1=cw, 2=180, 3=flip-lr, 4=transpose, else=id.

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: no_frames, selector_unmatched, no_cmd.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import draw_frame, full_grid

GENERATOR_ID = "94755460a402"
VERSION = "1.1.0"
TASK_ID = "94755460a402"
SUMMARY = "Selector + cmd at top + multiple frames of different colors with internal motifs."

INVARIANTS = [
    "(0,0) is selector ∈ {2..9}",
    "(0,1) is cmd ∈ 1..5",
    "2-3 closed frames of distinct colors with multicolor interior",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_frames", "selector_unmatched", "no_cmd")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 12..14", "valid": "10..18"},
    "grid_w":         {"type": "int", "default": "rng 16..18", "valid": "14..20"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "selector":       {"type": "int", "default": "rng 2..9", "valid": "2..9"},
    "cmd":            {"type": "int", "default": "rng 1..5", "valid": "1..5"},
    "palette_size":   {"type": "int", "default": "5..6", "valid": "5..7"},
    "position_bias":  {"type": "str", "default": "two_frames_top_then_right",
                       "valid": "two_frames_top_then_right"},
    "n_distinct_colors": {"type": "int", "default": "5..6", "valid": "5..7"},
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
        h = ctx.draw_int("grid_h", 12, 12)
        w = ctx.draw_int("grid_w", 16, 16)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 14, 17)
        w = ctx.draw_int("grid_w", 18, 19)
    else:
        h = ctx.draw_int("grid_h", 12, 14)
        w = ctx.draw_int("grid_w", 16, 18)
    selector = ctx.draw_int("selector", 2, 9)
    cmd = ctx.draw_int("cmd", 1, 5)
    g = full_grid(h, w, 0)
    rng = ctx.draw_rng("layout")
    g[0][0] = selector
    g[0][1] = cmd
    draw_frame(g, 2, 3, 6, 7, selector)
    interior_palette = [c for c in range(2, 10) if c != selector]
    rng.shuffle(interior_palette)
    g[3][4] = interior_palette[0]; g[3][6] = interior_palette[1]
    g[4][4] = interior_palette[0]; g[4][5] = interior_palette[2]
    g[5][5] = interior_palette[2]; g[5][6] = interior_palette[3 % len(interior_palette)]
    other = rng.choice([c for c in range(2, 10) if c != selector])
    draw_frame(g, 2, 11, 7, 15, other)
    other_pal = [c for c in range(2, 10) if c != other and c != selector]
    rng.shuffle(other_pal)
    g[3][12] = other_pal[0]; g[4][13] = other_pal[1]; g[5][14] = other_pal[2]
    return g


def _draw_from_degenerate(name, rng):
    h, w = 12, 16
    g = full_grid(h, w, 0)
    if name == "no_frames":
        # Selector + cmd at top but no frames at all — rule has nothing
        # to crop or transform.
        g[0][0] = 3
        g[0][1] = 2
        return g
    if name == "selector_unmatched":
        # Selector points to a color that isn't any frame — rule's
        # frame-pick step has no candidate to choose.
        g[0][0] = 7  # selector
        g[0][1] = 2  # cmd
        draw_frame(g, 2, 3, 6, 7, 3)  # frame is 3, not 7
        draw_frame(g, 2, 11, 7, 15, 4)  # frame is 4, not 7
        return g
    if name == "no_cmd":
        # Selector present but (0,1) is 0 — rule's transform-code lookup
        # has no entry.
        g[0][0] = 3
        # leave (0,1) at 0
        draw_frame(g, 2, 3, 6, 7, 3)
        return g
    return g
