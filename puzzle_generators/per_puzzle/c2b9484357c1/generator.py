"""Generator for arc_puzzle_bank_next21:M14 — fill largest hollow obj's holes.

Rule: among components with holes (cells in their bbox interior that aren't
in the cell set), the largest one has its holes filled with its own color.

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: no_rect, no_blob, both_hollow.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import draw_frame, full_grid

GENERATOR_ID = "c2b9484357c1"
VERSION = "1.1.0"
TASK_ID = "c2b9484357c1"

SUMMARY = "1 hollow rectangle in some color + 1 small solid blob in another color."

INVARIANTS = [
    "background is 0",
    "exactly one hollow rectangle (≥4×4) in some color",
    "exactly one small solid blob (2-4 cells) in another color",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_rect", "no_blob", "both_hollow")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 7..9", "valid": "5..14"},
    "grid_w":         {"type": "int", "default": "rng 8..10", "valid": "6..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "palette_size":   {"type": "int", "default": "2", "valid": "2..3"},
    "position_bias":  {"type": "str", "default": "rect_plus_blob",
                       "valid": "rect_plus_blob"},
    "n_distinct_colors": {"type": "int", "default": "2", "valid": "2..3"},
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


def _build_motif(rng, k):
    cells = [(0, 0)]; seen = {(0, 0)}
    while len(cells) < k:
        r, c = rng.choice(cells)
        dr, dc = rng.choice([(-1, 0), (1, 0), (0, -1), (0, 1)])
        nr, nc = r + dr, c + dc
        if (nr, nc) not in seen:
            cells.append((nr, nc)); seen.add((nr, nc))
    return cells


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 7, 8)
        w = ctx.draw_int("grid_w", 8, 9)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 9, 11)
        w = ctx.draw_int("grid_w", 10, 12)
    else:
        h = ctx.draw_int("grid_h", 7, 9)
        w = ctx.draw_int("grid_w", 8, 10)
    rng = ctx.draw_rng("layout")

    for outer in range(40):
        g = full_grid(h, w, 0)
        rect_color, blob_color = rng.sample([1, 2, 3, 4, 5, 6, 7, 8, 9], 2)
        fh, fw = rng.choice([(4, 5), (5, 4), (4, 4), (5, 5)])
        placed = False
        for _ in range(80):
            r0 = rng.randint(0, h - fh); c0 = rng.randint(0, w - fw)
            if not _free(g, r0, c0, r0 + fh - 1, c0 + fw - 1): continue
            draw_frame(g, r0, c0, r0 + fh - 1, c0 + fw - 1, rect_color)
            placed = True; break
        if not placed:
            continue
        cells = _build_motif(rng, rng.randint(2, 4))
        rs = [r for r, _ in cells]; cs = [c for _, c in cells]
        sh = max(rs) - min(rs) + 1; sw = max(cs) - min(cs) + 1
        for _ in range(80):
            r0 = rng.randint(0, h - sh); c0 = rng.randint(0, w - sw)
            if not _free(g, r0, c0, r0 + sh - 1, c0 + sw - 1): continue
            for r, c in cells:
                g[r0 + r - min(rs)][c0 + c - min(cs)] = blob_color
            return g
    raise ValueError("could not realize M14 layout")


def _draw_from_degenerate(name, rng):
    h, w = 8, 9
    g = full_grid(h, w, 0)
    if name == "no_rect":
        # Only solid blob, no hollow rectangle — rule has nothing to fill.
        g[3][3] = 4; g[3][4] = 4; g[4][3] = 4
        return g
    if name == "no_blob":
        # Hollow rect but no other component — rule's "largest" is trivial (only one).
        draw_frame(g, 1, 1, 5, 5, 4)
        return g
    if name == "both_hollow":
        # Two hollow rects with same hole-count — "largest" tied.
        draw_frame(g, 0, 0, 3, 3, 4)
        draw_frame(g, 4, 4, 7, 7, 5)
        return g
    return g
