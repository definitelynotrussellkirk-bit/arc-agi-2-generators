"""Generator for 9b:hard_57 — frame select-rank, transform, pack.

Rule: each 9-frame has a sel-key above (value 2 = first/smallest, 3 =
last/largest) and a tr-key to the left (3=identity, 4=CW, 5=flip-lr,
6=180). Inside, ≥2 components in any color; pick by sel-key, transform
by tr-key. Output hstacks the parts.

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: no_sel_key (no sel-keys above frames → no rank selection);
no_tr_key (no tr-keys left of frames → no transform);
tied_sizes (2 interior shapes with same size → first/last sel ambiguous).
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "4729a9750abc"
VERSION = "1.1.0"
TASK_ID = "4729a9750abc"

SUMMARY = "2 hollow 9-frames, each with sel-key above + tr-key left + 2 interior shapes (distinct sizes)."

INVARIANTS = [
    "background is 0",
    "exactly 2 hollow 9-frames at distinct positions",
    "each frame has one sel-key in row r1-1 (value 2 or 3)",
    "each frame has one tr-key at col c1-1 (value 3, 4, 5, or 6)",
    "each frame's interior holds 2 components in distinct colors with distinct sizes",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_sel_key", "no_tr_key", "tied_sizes")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "ch_h":              {"type": "int", "default": "rng 7..8", "valid": "6..10"},
    "ch_w":              {"type": "int", "default": "rng 7..8", "valid": "6..10"},
    "palette_kind":      {"type": "str", "default": "rng helpful",
                          "valid": "|".join(PALETTE_KINDS)},
    "palette_size":      {"type": "int", "default": "rng 4..5", "valid": "4..6"},
    "position_bias":     {"type": "str", "default": "two_frames_with_keys",
                          "valid": "two_frames_with_keys"},
    "n_distinct_colors": {"type": "int", "default": "rng 4..5", "valid": "4..6"},
    "density":           {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":           {"type": "str", "default": "alias for palette_kind",
                          "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


_BY_SIZE = {
    3: [[(0, 0), (0, 1), (1, 0)], [(0, 0), (1, 0), (1, 1)]],
    4: [[(0, 0), (0, 1), (1, 0), (1, 1)], [(0, 0), (1, 0), (1, 1), (2, 1)]],
    5: [[(0, 0), (0, 1), (0, 2), (1, 0), (1, 2)]],
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
        fh = ctx.draw_int("ch_h", 8, 8)
        fw = ctx.draw_int("ch_w", 8, 8)
    elif difficulty == "hard":
        fh = ctx.draw_int("ch_h", 9, 9)
        fw = ctx.draw_int("ch_w", 9, 9)
    else:
        fh = ctx.draw_int("ch_h", 8, 9)
        fw = ctx.draw_int("ch_w", 8, 9)
    rng = ctx.draw_rng("layout")
    h = fh + 4
    w = 2 * fw + 4
    g = full_grid(h, w, 0)
    r0 = 2
    col_starts = [2, 2 + fw + 1]
    if col_starts[-1] + fw > w:
        raise ValueError("grid too narrow")
    for c0 in col_starts:
        for c in range(c0, c0 + fw): g[r0][c] = 9; g[r0 + fh - 1][c] = 9
        for r in range(r0, r0 + fh): g[r][c0] = 9; g[r][c0 + fw - 1] = 9
        sel_c = rng.randint(c0, c0 + fw - 1)
        g[r0 - 1][sel_c] = rng.choice([2, 3])
        tr_r = rng.randint(r0, r0 + fh - 1)
        g[tr_r][c0 - 1] = rng.choice([3, 4, 5, 6])
        sizes = rng.sample([3, 4], 2)
        palette = rng.sample([1, 2, 3, 4, 6, 7, 8], 2)
        for size, color in zip(sizes, palette):
            shape = rng.choice(_BY_SIZE[size])
            sh = max(r for r, _ in shape) + 1
            sw = max(c for _, c in shape) + 1
            placed = False
            for _ in range(60):
                ir = rng.randint(r0 + 1, r0 + fh - 1 - sh)
                ic = rng.randint(c0 + 1, c0 + fw - 1 - sw)
                cells = [(ir + dr, ic + dc) for dr, dc in shape]
                if any(g[r][c] != 0 for r, c in cells): continue
                for r, c in cells: g[r][c] = color
                placed = True; break
            if not placed:
                raise ValueError(f"could not place size-{size} shape")
    return g


def _draw_from_degenerate(name, rng):
    h, w = 14, 22
    g = full_grid(h, w, 0)
    fh, fw = 8, 8
    r0 = 2
    cs = [2, 12]
    if name == "no_sel_key":
        # Frames + tr-keys + interior shapes but no sel-keys above.
        for c0 in cs:
            for c in range(c0, c0 + fw): g[r0][c] = 9; g[r0 + fh - 1][c] = 9
            for r in range(r0, r0 + fh): g[r][c0] = 9; g[r][c0 + fw - 1] = 9
            g[r0 + 2][c0 - 1] = 4
            g[r0 + 2][c0 + 2] = 1; g[r0 + 2][c0 + 3] = 1; g[r0 + 3][c0 + 2] = 1
            g[r0 + 5][c0 + 4] = 2; g[r0 + 5][c0 + 5] = 2
        return g
    if name == "no_tr_key":
        # Frames + sel-keys + interior shapes but no tr-keys left.
        for c0 in cs:
            for c in range(c0, c0 + fw): g[r0][c] = 9; g[r0 + fh - 1][c] = 9
            for r in range(r0, r0 + fh): g[r][c0] = 9; g[r][c0 + fw - 1] = 9
            g[r0 - 1][c0 + 2] = 2
            g[r0 + 2][c0 + 2] = 1; g[r0 + 2][c0 + 3] = 1; g[r0 + 3][c0 + 2] = 1
            g[r0 + 5][c0 + 4] = 3; g[r0 + 5][c0 + 5] = 3
        return g
    if name == "tied_sizes":
        # Frames + keys but interior shapes have equal sizes — first/last ambiguous.
        for c0 in cs:
            for c in range(c0, c0 + fw): g[r0][c] = 9; g[r0 + fh - 1][c] = 9
            for r in range(r0, r0 + fh): g[r][c0] = 9; g[r][c0 + fw - 1] = 9
            g[r0 - 1][c0 + 2] = 2
            g[r0 + 2][c0 - 1] = 4
            g[r0 + 2][c0 + 2] = 1; g[r0 + 2][c0 + 3] = 1; g[r0 + 3][c0 + 2] = 1
            g[r0 + 5][c0 + 4] = 3; g[r0 + 5][c0 + 5] = 3; g[r0 + 6][c0 + 5] = 3
        return g
    return g
