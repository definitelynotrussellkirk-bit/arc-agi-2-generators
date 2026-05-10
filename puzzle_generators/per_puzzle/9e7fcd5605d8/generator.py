"""Generator for arc_puzzle_bank_ninth21:M60 — hollow vs solid recolor.

Rule: blobs with a hole (any bbox-interior 0-cell) → recolor 8.
Solid blobs (bbox fully filled) → recolor 5.

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: no_blobs, only_hollow, only_solid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "9e7fcd5605d8"
VERSION = "1.1.0"
TASK_ID = "9e7fcd5605d8"
SUMMARY = "1 hollow rect-frame + 1 solid 2x2 blob, distinct colors."

INVARIANTS = [
    "background is 0",
    "≥1 hollow blob (rect-frame with bbox interior 0-cells)",
    "≥1 solid blob (bbox fully filled)",
    "blobs don't 4-touch",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_blobs", "only_hollow", "only_solid")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 9..11", "valid": "8..14"},
    "grid_w":         {"type": "int", "default": "rng 10..13", "valid": "9..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "palette_size":   {"type": "int", "default": "2", "valid": "2..2"},
    "position_bias":  {"type": "str", "default": "hollow_and_solid_blobs",
                       "valid": "hollow_and_solid_blobs"},
    "n_distinct_colors": {"type": "int", "default": "2", "valid": "2..2"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def _free(g, r1, c1, r2, c2):
    h, w = len(g), len(g[0])
    if r1 < 0 or c1 < 0 or r2 >= h or c2 >= w:
        return False
    for r in range(max(0, r1 - 1), min(h, r2 + 2)):
        for c in range(max(0, c1 - 1), min(w, c2 + 2)):
            if g[r][c] != 0:
                return False
    return True


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 9, 9)
        w = ctx.draw_int("grid_w", 10, 11)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 11, 13)
        w = ctx.draw_int("grid_w", 12, 14)
    else:
        h = ctx.draw_int("grid_h", 9, 11)
        w = ctx.draw_int("grid_w", 10, 13)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    palette = rng.sample([1, 2, 3, 4, 6, 7, 9], 2)
    for _ in range(40):
        fh = rng.randint(3, 4); fw = rng.randint(3, 4)
        r1 = rng.randint(0, h - fh)
        c1 = rng.randint(0, w - fw)
        r2 = r1 + fh - 1; c2 = c1 + fw - 1
        if _free(g, r1, c1, r2, c2):
            for c in range(c1, c2 + 1):
                g[r1][c] = palette[0]; g[r2][c] = palette[0]
            for r in range(r1, r2 + 1):
                g[r][c1] = palette[0]; g[r][c2] = palette[0]
            break
    for _ in range(40):
        r1 = rng.randint(0, h - 2)
        c1 = rng.randint(0, w - 2)
        if _free(g, r1, c1, r1 + 1, c1 + 1):
            for r in range(r1, r1 + 2):
                for c in range(c1, c1 + 2):
                    g[r][c] = palette[1]
            break
    return g


def _draw_from_degenerate(name, rng):
    h, w = 10, 12
    g = full_grid(h, w, 0)
    if name == "no_blobs":
        # Empty grid — rule has no candidates to classify or
        # recolor.
        return g
    if name == "only_hollow":
        # Two hollow frames, no solid blob — rule's "solid → 5"
        # branch never fires; only the "hollow → 8" branch.
        for c in range(2, 6): g[2][c] = 4; g[5][c] = 4
        for r in range(2, 6): g[r][2] = 4; g[r][5] = 4
        for c in range(7, 11): g[6][c] = 6; g[9][c] = 6
        for r in range(6, 10): g[r][7] = 6; g[r][10] = 6
        return g
    if name == "only_solid":
        # Two solid blobs, no hollow — rule's "hollow → 8"
        # branch never fires.
        for r in range(2, 4):
            for c in range(2, 4): g[r][c] = 4
        for r in range(6, 8):
            for c in range(8, 10): g[r][c] = 6
        return g
    return g
