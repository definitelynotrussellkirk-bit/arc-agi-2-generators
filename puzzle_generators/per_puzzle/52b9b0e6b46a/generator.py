"""Generator for arc_puzzle_bank_21_set14_bundle:hard_n03 — corner-code + rank + frame stamp.

Rule: a color-9 marker at one of 4 corners encodes a transform code (TL=0,
TR=1, BR=2, BL=3). 1-3 color-7 markers on row 0 encode rank. One color-8
hollow frame. Several components in non-{7, 8, 9} colors. The rank-th
component (by size) is transformed by code and stamped centered in the frame.

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: no_corner (no color-9 marker → no transform code);
no_rank (no color-7 markers → no rank index);
no_frame (corner+rank+motifs but no 8-frame → no destination).
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import draw_frame, full_grid

GENERATOR_ID = "52b9b0e6b46a"
VERSION = "1.1.0"
TASK_ID = "52b9b0e6b46a"

SUMMARY = "Color-9 marker at a corner + 1-3 color-7 cells on row 0 + 8-frame + 2-3 colored motifs."

INVARIANTS = [
    "background is 0",
    "exactly one color-9 marker at a corner",
    "1-3 color-7 markers on row 0 at distinct columns (not at the corner-9 col if applicable)",
    "exactly one hollow color-8 frame",
    "2-3 connected motifs in distinct colors from {1, 2, 3, 4, 5, 6}",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_corner", "no_rank", "no_frame")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":            {"type": "int", "default": "rng 11..13", "valid": "10..16"},
    "grid_w":            {"type": "int", "default": "rng 13..15", "valid": "12..20"},
    "n_motifs":          {"type": "int", "default": "rng 2..3", "valid": "2..4"},
    "palette_kind":      {"type": "str", "default": "rng helpful",
                          "valid": "|".join(PALETTE_KINDS)},
    "palette_size":      {"type": "int", "default": "rng 5..6", "valid": "5..7"},
    "position_bias":     {"type": "str", "default": "corner_rank_frame_motifs",
                          "valid": "corner_rank_frame_motifs"},
    "n_distinct_colors": {"type": "int", "default": "rng 5..6", "valid": "5..7"},
    "density":           {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":           {"type": "str", "default": "alias for palette_kind",
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
        h = ctx.draw_int("grid_h", 11, 12)
        w = ctx.draw_int("grid_w", 13, 14)
        n_motifs = ctx.draw_int("n_motifs", 2, 2)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 12, 13)
        w = ctx.draw_int("grid_w", 14, 15)
        n_motifs = ctx.draw_int("n_motifs", 3, 3)
    else:
        h = ctx.draw_int("grid_h", 11, 13)
        w = ctx.draw_int("grid_w", 13, 15)
        n_motifs = ctx.draw_int("n_motifs", 2, 3)
    rng = ctx.draw_rng("layout")

    for outer in range(40):
        g = full_grid(h, w, 0)
        corner = rng.choice([(0, 0), (0, w - 1), (h - 1, w - 1), (h - 1, 0)])
        g[corner[0]][corner[1]] = 9
        n_rank = rng.randint(1, min(3, n_motifs))
        avoid = {corner[1]} if corner[0] == 0 else set()
        cols_avail = [c for c in range(w) if c not in avoid]
        chosen_cols = rng.sample(cols_avail, n_rank)
        for c in chosen_cols:
            g[0][c] = 7
        fh, fw = rng.choice([(5, 6), (5, 7), (6, 6), (6, 7)])
        placed_f = False
        for _ in range(120):
            r0 = rng.randint(2, h - fh - 1); c0 = rng.randint(1, w - fw - 1)
            if not _free(g, r0, c0, r0 + fh - 1, c0 + fw - 1): continue
            draw_frame(g, r0, c0, r0 + fh - 1, c0 + fw - 1, 8)
            placed_f = True; break
        if not placed_f:
            continue
        sizes = rng.sample([3, 4, 5], n_motifs)
        colors = rng.sample([1, 2, 3, 4, 5, 6], n_motifs)
        ok = True
        for size, color in zip(sizes, colors):
            cells = _build_motif(rng, size)
            rs = [r for r, _ in cells]; cs = [c for _, c in cells]
            sh = max(rs) - min(rs) + 1; sw = max(cs) - min(cs) + 1
            placed = False
            for _ in range(120):
                r0 = rng.randint(2, h - sh); c0 = rng.randint(0, w - sw)
                if not _free(g, r0, c0, r0 + sh - 1, c0 + sw - 1): continue
                for r, c in cells:
                    g[r0 + r - min(rs)][c0 + c - min(cs)] = color
                placed = True; break
            if not placed:
                ok = False; break
        if ok:
            return g
    raise ValueError("could not realize set14 n03 layout")


def _draw_from_degenerate(name, rng):
    h, w = 12, 14
    g = full_grid(h, w, 0)
    if name == "no_corner":
        # No corner-9 marker — no transform code.
        g[0][5] = 7
        draw_frame(g, 3, 1, 7, 7, 8)
        for dr, dc in [(0, 0), (0, 1), (1, 0)]:
            g[8 + dr][9 + dc] = 4
        return g
    if name == "no_rank":
        # Corner + frame + motifs but no row-0 7-markers — no rank index.
        g[0][0] = 9
        draw_frame(g, 3, 2, 7, 8, 8)
        for dr, dc in [(0, 0), (0, 1), (1, 0)]:
            g[8 + dr][9 + dc] = 4
        return g
    if name == "no_frame":
        # Corner + rank + motifs but no 8-frame — no destination.
        g[0][0] = 9
        g[0][5] = 7
        for dr, dc in [(0, 0), (0, 1), (1, 0)]:
            g[5 + dr][5 + dc] = 4
        return g
    return g
