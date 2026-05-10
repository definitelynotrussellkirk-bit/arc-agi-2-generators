"""Generator for arc_puzzle_bank_fourth21:M27 — keep only holed objects.

Rule: keep blobs that have at least one bbox-interior 0-cell (hollow);
drop solid blobs.

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: all_solid (no holed objects → rule erases everything,
output is empty), all_holed (every object is holed → rule keeps
everything, no contrast), no_objects (grid is all bg → rule's
selector finds nothing).
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "0049208d162d"
VERSION = "1.1.0"
TASK_ID = "0049208d162d"
SUMMARY = "1 hollow rect-frame (kept) + 1-2 solid small blobs (dropped)."

INVARIANTS = [
    "background is 0",
    "≥1 hollow blob (with at least one bbox-interior 0-cell)",
    "≥1 solid blob (whose bbox is fully filled)",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("all_solid", "all_holed", "no_objects")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":            {"type": "int", "default": "rng 9..11", "valid": "8..14"},
    "grid_w":            {"type": "int", "default": "rng 11..13", "valid": "9..14"},
    "palette_kind":      {"type": "str", "default": "rng helpful",
                          "valid": "|".join(PALETTE_KINDS)},
    "palette_size":      {"type": "int", "default": "rng 3..3", "valid": "3..3"},
    "position_bias":     {"type": "str", "default": "frame_plus_solid_blobs",
                          "valid": "frame_plus_solid_blobs"},
    "n_distinct_colors": {"type": "int", "default": "rng 3..3", "valid": "3..3"},
    "density":           {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":           {"type": "str", "default": "alias for palette_kind",
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
        w = ctx.draw_int("grid_w", 11, 11)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 11, 11)
        w = ctx.draw_int("grid_w", 13, 13)
    else:
        h = ctx.draw_int("grid_h", 9, 11)
        w = ctx.draw_int("grid_w", 11, 13)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    palette = rng.sample([1, 2, 3, 4, 5, 6, 7, 8, 9], 3)
    for _ in range(40):
        fh = rng.randint(3, 4); fw = rng.randint(3, 4)
        r1 = rng.randint(0, h - fh)
        c1 = rng.randint(0, w - fw)
        r2 = r1 + fh - 1
        c2 = c1 + fw - 1
        if _free(g, r1, c1, r2, c2):
            for c in range(c1, c2 + 1):
                g[r1][c] = palette[0]; g[r2][c] = palette[0]
            for r in range(r1, r2 + 1):
                g[r][c1] = palette[0]; g[r][c2] = palette[0]
            break
    used = {(r, c) for r in range(h) for c in range(w) if g[r][c] != 0}
    for color in palette[1:]:
        for _ in range(40):
            r1 = rng.randint(0, h - 2)
            c1 = rng.randint(0, w - 2)
            cells = {(r1, c1), (r1, c1 + 1), (r1 + 1, c1), (r1 + 1, c1 + 1)}
            if cells & used:
                continue
            ok = True
            for r, c in cells:
                for dr, dc in ((-1, 0), (1, 0), (0, -1), (0, 1)):
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < h and 0 <= nc < w and (nr, nc) not in cells and g[nr][nc] != 0:
                        ok = False; break
                if not ok: break
            if not ok: continue
            for r, c in cells:
                g[r][c] = color
            used |= cells
            break
    return g


def _draw_from_degenerate(name, rng):
    h, w = 10, 12
    g = full_grid(h, w, 0)
    if name == "all_solid":
        # No holed objects — rule erases everything; output empty.
        for r, c in [(1, 1), (1, 2), (2, 1), (2, 2)]: g[r][c] = 4
        for r, c in [(5, 6), (5, 7), (6, 6), (6, 7)]: g[r][c] = 6
        for r, c in [(8, 2), (8, 3)]: g[r][c] = 8
        return g
    if name == "all_holed":
        # Every object is hollow — rule keeps everything; no contrast.
        # 3x3 frame
        for c in range(1, 4): g[1][c] = 4; g[3][c] = 4
        g[2][1] = 4; g[2][3] = 4
        # another 3x3 frame
        for c in range(6, 9): g[6][c] = 6; g[8][c] = 6
        g[7][6] = 6; g[7][8] = 6
        return g
    if name == "no_objects":
        # Grid is all bg — rule's selector finds nothing.
        return g
    return g
