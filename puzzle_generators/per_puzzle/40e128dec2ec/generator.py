"""Generator for arc_puzzle_bank_21_set12_bundle:hard_l17 — 5-divider + 2 motifs + 2 frames.

Rule: a horizontal color-5 divider; above are color codes, below are 2
frames in colors 1 and 2; rule fills frame interior with tiled pattern.

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: no_divider, no_codes, no_frames.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import draw_frame, full_grid

GENERATOR_ID = "40e128dec2ec"
VERSION = "1.1.0"
TASK_ID = "40e128dec2ec"

SUMMARY = "Color-5 horizontal divider + 2 codes above + 2 hollow frames (1, 2) below."

INVARIANTS = [
    "background is 0",
    "exactly one full color-5 row (the divider)",
    "above the divider: 2 single-cell codes (colors 2 and 3)",
    "below the divider: 2 hollow frames in colors 1 and 2",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_divider", "no_codes", "no_frames")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 9..11", "valid": "7..14"},
    "grid_w":         {"type": "int", "default": "rng 13..15", "valid": "10..18"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "palette_size":   {"type": "int", "default": "5", "valid": "5..5"},
    "position_bias":  {"type": "str", "default": "divider_with_codes_and_frames",
                       "valid": "divider_with_codes_and_frames"},
    "n_distinct_colors": {"type": "int", "default": "5", "valid": "5..5"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def _free(g, r1, c1, r2, c2):
    h, w = len(g), len(g[0])
    if r1 < 0 or c1 < 0 or r2 >= h or c2 >= w: return False
    for r in range(max(0, r1 - 1), min(h, r2 + 2)):
        for c in range(max(0, c1 - 1), min(w, c2 + 2)):
            if g[r][c] != 0: return False
    return True


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 9, 9)
        w = ctx.draw_int("grid_w", 13, 13)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 11, 14)
        w = ctx.draw_int("grid_w", 15, 18)
    else:
        h = ctx.draw_int("grid_h", 9, 11)
        w = ctx.draw_int("grid_w", 13, 15)
    rng = ctx.draw_rng("layout")

    for outer in range(40):
        g = full_grid(h, w, 0)
        div_r = 2
        for c in range(w): g[div_r][c] = 5
        g[0][1] = 2
        g[1][2] = 3
        ok = True
        for color in (1, 2):
            placed = False
            for _ in range(80):
                fh = rng.choice([4, 5]); fw = rng.choice([4, 5])
                r0 = rng.randint(div_r + 1, h - fh); c0 = rng.randint(0, w - fw)
                if not _free(g, r0, c0, r0 + fh - 1, c0 + fw - 1): continue
                draw_frame(g, r0, c0, r0 + fh - 1, c0 + fw - 1, color)
                placed = True; break
            if not placed:
                ok = False; break
        if ok:
            return g
    raise ValueError("could not realize layout")


def _draw_from_degenerate(name, rng):
    h, w = 10, 14
    g = full_grid(h, w, 0)
    if name == "no_divider":
        # Codes and frames but no 5-row divider — rule's "above
        # codes / below frames" partition fails.
        g[0][1] = 2; g[1][2] = 3
        draw_frame(g, 4, 1, 7, 5, 1)
        draw_frame(g, 4, 8, 7, 12, 2)
        return g
    div_r = 2
    for c in range(w): g[div_r][c] = 5
    if name == "no_codes":
        # Divider and frames but no codes above — rule's recolor
        # spec is undefined.
        draw_frame(g, 4, 1, 7, 5, 1)
        draw_frame(g, 4, 8, 7, 12, 2)
        return g
    if name == "no_frames":
        # Divider and codes but no frames below — rule has no
        # frames to fill.
        g[0][1] = 2; g[1][2] = 3
        return g
    return g
