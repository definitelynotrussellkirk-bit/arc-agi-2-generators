"""Generator for 9b:hard_61 — local bbox overlap gallery.

Rule: each 9-frame contains a key cell directly above + a color-1
shape and color-2 shape inside (with overlapping bboxes). Output is
hstack of empty rectangles sized by each frame's interior color-1 ∩
color-2 bbox intersection, painted with the frame's key color.

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: no_frames (no 9-frames → no chambers);
no_keys (frames + shapes but no keys above → no output color);
no_overlap (frames + keys + shapes but bboxes don't overlap → empty
intersections, output is degenerate).
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "b6452f922704"
VERSION = "1.1.0"
TASK_ID = "b6452f922704"

SUMMARY = "2-3 9-frames; each has key above + color-1 + color-2 shapes inside with overlapping bboxes."

INVARIANTS = [
    "background is 0",
    "2-3 hollow 9-frames at distinct columns",
    "each frame has one key cell directly above (in the col range, value not in {0, 9})",
    "each frame's interior holds one color-1 shape and one color-2 shape with overlapping bboxes",
    "all key colors are distinct",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_frames", "no_keys", "no_overlap")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "ch_h":              {"type": "int", "default": "rng 6..7", "valid": "5..9"},
    "ch_w":              {"type": "int", "default": "rng 6..7", "valid": "5..9"},
    "palette_kind":      {"type": "str", "default": "rng helpful",
                          "valid": "|".join(PALETTE_KINDS)},
    "palette_size":      {"type": "int", "default": "rng 4..5", "valid": "4..6"},
    "position_bias":     {"type": "str", "default": "frames_with_keys_above",
                          "valid": "frames_with_keys_above"},
    "n_distinct_colors": {"type": "int", "default": "rng 4..5", "valid": "4..6"},
    "density":           {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":           {"type": "str", "default": "alias for palette_kind",
                          "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


_SHAPES = [
    [(0, 0), (0, 1), (1, 0)],
    [(0, 0), (1, 0), (1, 1)],
    [(0, 0), (0, 1)],
]


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
        fh = ctx.draw_int("ch_h", 6, 6)
        fw = ctx.draw_int("ch_w", 6, 6)
    elif difficulty == "hard":
        fh = ctx.draw_int("ch_h", 7, 7)
        fw = ctx.draw_int("ch_w", 7, 7)
    else:
        fh = ctx.draw_int("ch_h", 6, 7)
        fw = ctx.draw_int("ch_w", 6, 7)
    rng = ctx.draw_rng("layout")
    n_frames = rng.randint(2, 3)
    h = fh + 4
    w = n_frames * fw + (n_frames - 1) + 2
    g = full_grid(h, w, 0)
    key_palette = rng.sample([3, 4, 5, 6, 7, 8], n_frames)
    r0 = 2
    col_starts = [1 + i * (fw + 1) for i in range(n_frames)]
    if col_starts[-1] + fw > w:
        raise ValueError("grid too narrow")
    for c0, key_color in zip(col_starts, key_palette):
        for c in range(c0, c0 + fw): g[r0][c] = 9; g[r0 + fh - 1][c] = 9
        for r in range(r0, r0 + fh): g[r][c0] = 9; g[r][c0 + fw - 1] = 9
        kc = rng.randint(c0, c0 + fw - 1)
        g[r0 - 1][kc] = key_color
        for _ in range(60):
            sa = rng.choice(_SHAPES)
            sb = rng.choice(_SHAPES)
            sah = max(r for r, _ in sa) + 1
            saw = max(c for _, c in sa) + 1
            sbh = max(r for r, _ in sb) + 1
            sbw = max(c for _, c in sb) + 1
            ar = rng.randint(r0 + 1, r0 + fh - 1 - sah)
            ac = rng.randint(c0 + 1, c0 + fw - 1 - saw)
            br = rng.randint(r0 + 1, r0 + fh - 1 - sbh)
            bc = rng.randint(c0 + 1, c0 + fw - 1 - sbw)
            a_cells = {(ar + dr, ac + dc) for dr, dc in sa}
            b_cells = {(br + dr, bc + dc) for dr, dc in sb}
            if a_cells & b_cells: continue
            ar2, ac2 = ar + sah - 1, ac + saw - 1
            br2, bc2 = br + sbh - 1, bc + sbw - 1
            if (max(ar, br) > min(ar2, br2)) or (max(ac, bc) > min(ac2, bc2)):
                continue
            for r, c in a_cells: g[r][c] = 1
            for r, c in b_cells: g[r][c] = 2
            break
        else:
            raise ValueError("could not place A/B shapes with overlapping bbox")
    return g


def _draw_from_degenerate(name, rng):
    h, w = 11, 16
    g = full_grid(h, w, 0)
    if name == "no_frames":
        # No 9-frames — no chambers.
        g[1][3] = 5
        g[5][4] = 1; g[5][5] = 2
        return g
    if name == "no_keys":
        # Frames + shapes but no keys above — no output color.
        for c in range(1, 7): g[2][c] = 9; g[8][c] = 9
        for r in range(2, 9): g[r][1] = 9; g[r][6] = 9
        g[4][3] = 1; g[4][4] = 1
        g[5][4] = 2; g[5][5] = 2
        return g
    if name == "no_overlap":
        # Frame + key + shapes but bboxes don't overlap.
        g[1][4] = 5
        for c in range(1, 8): g[2][c] = 9; g[8][c] = 9
        for r in range(2, 9): g[r][1] = 9; g[r][7] = 9
        g[3][2] = 1; g[3][3] = 1
        g[6][5] = 2; g[6][6] = 2
        return g
    return g
