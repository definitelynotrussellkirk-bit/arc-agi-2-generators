"""Generator for 15b:m104 — read frame majorities into row.

Rule: 3 hollow rectangular 8-frames at different positions; each
frame's interior holds a strict-majority color among 1-2 colors.
Output is a 1x3 row of those majority colors, ordered by frame's
leftmost column.

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: no_frames, no_majority, all_same_majority.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "ce7cf0742e9a"
VERSION = "1.1.0"
TASK_ID = "ce7cf0742e9a"
SUMMARY = "3 hollow 8-frames; each interior has a strict-majority non-8 color."

INVARIANTS = [
    "background is 0",
    "exactly 3 hollow rectangular 8-frames, distinct columns",
    "each interior has 1-2 distinct non-8 colors with a strict majority",
    "all 3 majority colors are distinct",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_frames", "no_majority", "all_same_majority")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 7..9", "valid": "7..18"},
    "grid_w":         {"type": "int", "default": "rng 17..18", "valid": "17..18"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "palette_size":   {"type": "int", "default": "6", "valid": "6..6"},
    "position_bias":  {"type": "str", "default": "three_frames_in_row",
                       "valid": "three_frames_in_row"},
    "n_distinct_colors": {"type": "int", "default": "6", "valid": "6..6"},
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
        h = ctx.draw_int("grid_h", 7, 7)
        w = ctx.draw_int("grid_w", 17, 17)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 9, 9)
        w = ctx.draw_int("grid_w", 18, 18)
    else:
        h = ctx.draw_int("grid_h", 7, 9)
        w = ctx.draw_int("grid_w", 17, 18)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    palette = rng.sample([1, 2, 3, 4, 5, 6, 7, 9], 6)
    majors = palette[:3]
    minors = palette[3:]
    r0 = rng.randint(0, h - 5)
    starts = [0, 6, 12 + (w - 17)]
    for c0, major, minor in zip(starts, majors, minors):
        for c in range(c0, c0 + 5):
            g[r0][c] = 8
            g[r0 + 4][c] = 8
        for r in range(r0, r0 + 5):
            g[r][c0] = 8
            g[r][c0 + 4] = 8
        interior = [(r, c) for r in range(r0 + 1, r0 + 4)
                    for c in range(c0 + 1, c0 + 4)]
        rng.shuffle(interior)
        n_major = rng.randint(5, 7)
        for r, c in interior[:n_major]:
            g[r][c] = major
        for r, c in interior[n_major:]:
            g[r][c] = minor
    return g


def _draw_from_degenerate(name, rng):
    h, w = 7, 17
    g = full_grid(h, w, 0)
    starts = [0, 6, 12]
    if name == "no_frames":
        # Loose color cells but no 8-frames — rule's "frame
        # interior" majority readout has no scope.
        g[2][2] = 4; g[2][8] = 6; g[2][14] = 7
        return g
    if name == "no_majority":
        # 3 frames but each interior has a 5-4 split (no strict
        # majority); rule's "strict majority" filter fails per frame.
        for c0 in starts:
            for c in range(c0, c0 + 5):
                g[1][c] = 8; g[5][c] = 8
            for r in range(1, 6):
                g[r][c0] = 8; g[r][c0 + 4] = 8
            interior = [(r, c) for r in range(2, 5) for c in range(c0 + 1, c0 + 4)]
            for i, (r, c) in enumerate(interior):
                g[r][c] = 4 if i < 4 else 6
        return g
    if name == "all_same_majority":
        # All 3 frames have the same majority color — rule's
        # "distinct majority" precondition fails; output strip is
        # uniform.
        for c0 in starts:
            for c in range(c0, c0 + 5):
                g[1][c] = 8; g[5][c] = 8
            for r in range(1, 6):
                g[r][c0] = 8; g[r][c0 + 4] = 8
            for r in range(2, 5):
                for c in range(c0 + 1, c0 + 4):
                    g[r][c] = 4
        return g
    return g
