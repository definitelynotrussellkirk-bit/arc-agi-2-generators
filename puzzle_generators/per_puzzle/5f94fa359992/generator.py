"""Generator for 9b:m61 — order framed crops by key.

Rule: each 9-frame has a single key cell directly above (in column
range, row r1-1). Sort frames by key value ascending; output hstacks
their cropped non-9 interiors.

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: no_frames (no 9-frames → rule has no chambers);
no_keys (frames but no keys above → no sort key);
tied_keys (frames with duplicate key colors → sort ambiguous).
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "5f94fa359992"
VERSION = "1.1.0"
TASK_ID = "5f94fa359992"

SUMMARY = "2-3 hollow 9-frames at distinct cols + key cell above each + a shape inside each."

INVARIANTS = [
    "background is 0",
    "2-3 hollow 9-frames at distinct columns",
    "each frame has exactly one key cell in row r1-1, within the frame's column range",
    "each frame's interior holds a small shape in a non-9, non-key color",
    "all key colors are distinct (so the sort is unambiguous)",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_frames", "no_keys", "tied_keys")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":            {"type": "int", "default": "rng 9..11", "valid": "8..14"},
    "grid_w":            {"type": "int", "default": "rng 15..18", "valid": "14..20"},
    "palette_kind":      {"type": "str", "default": "rng helpful",
                          "valid": "|".join(PALETTE_KINDS)},
    "palette_size":      {"type": "int", "default": "rng 4..6", "valid": "4..8"},
    "position_bias":     {"type": "str", "default": "frames_with_keys_above",
                          "valid": "frames_with_keys_above"},
    "n_distinct_colors": {"type": "int", "default": "rng 4..6", "valid": "4..8"},
    "density":           {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":           {"type": "str", "default": "alias for palette_kind",
                          "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


_INNER_SHAPES = [
    [(0, 0), (0, 1), (1, 0)],
    [(0, 0), (1, 0), (1, 1)],
    [(0, 0), (0, 1)],
    [(0, 0), (0, 1), (1, 1)],
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
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 15, 16)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 10, 11)
        w = ctx.draw_int("grid_w", 17, 18)
    else:
        h = ctx.draw_int("grid_h", 9, 11)
        w = ctx.draw_int("grid_w", 15, 18)
    rng = ctx.draw_rng("layout")
    n_frames = rng.randint(2, 3)
    fh = 4; fw = 4
    palette = rng.sample([1, 2, 3, 4, 5, 6, 7, 8], n_frames * 2)
    key_colors = palette[:n_frames]
    inner_colors = palette[n_frames:]
    for _ in range(40):
        g = full_grid(h, w, 0)
        r0 = 2
        col_starts = sorted(rng.sample(range(0, w - fw), n_frames))
        ok_layout = all(col_starts[i + 1] - col_starts[i] > fw
                        for i in range(len(col_starts) - 1))
        if not ok_layout:
            continue
        ok = True
        for c0, key_color, inner_color in zip(col_starts, key_colors, inner_colors):
            for c in range(c0, c0 + fw): g[r0][c] = 9; g[r0 + fh - 1][c] = 9
            for r in range(r0, r0 + fh): g[r][c0] = 9; g[r][c0 + fw - 1] = 9
            key_c = rng.randint(c0, c0 + fw - 1)
            g[r0 - 1][key_c] = key_color
            shape = rng.choice(_INNER_SHAPES)
            sh = max(r for r, _ in shape) + 1
            sw = max(c for _, c in shape) + 1
            ir = r0 + 1 + rng.randint(0, fh - 2 - sh)
            ic = c0 + 1 + rng.randint(0, fw - 2 - sw)
            for dr, dc in shape:
                g[ir + dr][ic + dc] = inner_color
        if ok:
            return g
    raise ValueError("could not lay out frames + keys")


def _draw_from_degenerate(name, rng):
    h, w = 9, 16
    g = full_grid(h, w, 0)
    if name == "no_frames":
        # No frames — no chambers to crop.
        g[1][3] = 5
        g[1][8] = 6
        g[3][4] = 1; g[3][9] = 2
        return g
    if name == "no_keys":
        # Frames + inner shapes but no keys above — no sort key.
        for c in range(1, 5): g[2][c] = 9; g[5][c] = 9
        for r in range(2, 6): g[r][1] = 9; g[r][4] = 9
        for c in range(7, 11): g[2][c] = 9; g[5][c] = 9
        for r in range(2, 6): g[r][7] = 9; g[r][10] = 9
        g[3][2] = 1; g[3][8] = 2
        return g
    if name == "tied_keys":
        # Two frames with the same key color — sort ambiguous.
        for c in range(1, 5): g[2][c] = 9; g[5][c] = 9
        for r in range(2, 6): g[r][1] = 9; g[r][4] = 9
        g[1][2] = 5
        g[3][2] = 1
        for c in range(7, 11): g[2][c] = 9; g[5][c] = 9
        for r in range(2, 6): g[r][7] = 9; g[r][10] = 9
        g[1][8] = 5
        g[3][8] = 2
        return g
    return g
