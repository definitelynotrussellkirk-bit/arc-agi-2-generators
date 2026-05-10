"""Generator for v2_meta_puzzles:H7 — row-0 count + recolor matching size.

Rule: row 0 has 1-3 color-1 markers; the count = target-size. Each color-3
component of that exact size is recolored to 8.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_markers,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_markers, no_matching_motif, all_same_size.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "072d24e77cc0"
VERSION = "1.1.0"
TASK_ID = "072d24e77cc0"

SUMMARY = "Row 0 has 1-3 color-1 markers; body has 2-3 color-3 motifs (some size matches marker count)."

INVARIANTS = [
    "background is 0",
    "1-3 color-1 markers on row 0 at distinct columns",
    "2-3 color-3 motifs in body (rows >= 2) with strictly different sizes; one matches marker count",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_markers", "no_matching_motif", "all_same_size")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 7..9", "valid": "5..14"},
    "grid_w":         {"type": "int", "default": "rng 9..11", "valid": "7..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_markers":      {"type": "int", "default": "rng 2..4", "valid": "1..6"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2..2"},
    "position_bias":  {"type": "str", "default": "row0_count_with_motifs",
                       "valid": "row0_count_with_motifs"},
    "n_distinct_colors": {"type": "int", "default": "2", "valid": "2..2"},
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
        h = ctx.draw_int("grid_h", 7, 7)
        w = ctx.draw_int("grid_w", 9, 10)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("grid_w", 10, 11)
    else:
        h = ctx.draw_int("grid_h", 7, 9)
        w = ctx.draw_int("grid_w", 9, 11)
    rng = ctx.draw_rng("layout")

    for outer in range(40):
        g = full_grid(h, w, 0)
        n_markers = rng.randint(2, 4)
        cols = rng.sample(range(w), n_markers)
        for c in cols:
            g[0][c] = 1
        sizes = [n_markers, n_markers + 1, n_markers + 2]
        rng.shuffle(sizes)
        ok = True
        for size in sizes:
            cells = _build_motif(rng, size)
            rs = [r for r, _ in cells]; cs = [c for _, c in cells]
            sh = max(rs) - min(rs) + 1; sw = max(cs) - min(cs) + 1
            placed = False
            for _ in range(120):
                r0 = rng.randint(2, h - sh); c0 = rng.randint(0, w - sw)
                if not _free(g, r0, c0, r0 + sh - 1, c0 + sw - 1): continue
                for r, c in cells:
                    g[r0 + r - min(rs)][c0 + c - min(cs)] = 3
                placed = True; break
            if not placed:
                ok = False; break
        if ok:
            return g
    raise ValueError("could not realize layout")


def _draw_from_degenerate(name, rng):
    h, w = 8, 10
    g = full_grid(h, w, 0)
    if name == "no_markers":
        # row 0 blank → count = 0, no motifs match, output blank or identity
        for (r, c) in [(3, 3), (3, 4)]: g[r][c] = 3
        for (r, c) in [(5, 6), (5, 7), (6, 7)]: g[r][c] = 3
        return g
    if name == "no_matching_motif":
        # markers count = 4 but no motif of size 4 → rule fires zero times
        for c in [1, 3, 5, 7]: g[0][c] = 1
        for (r, c) in [(3, 3), (3, 4)]: g[r][c] = 3  # size 2
        for (r, c) in [(5, 6), (5, 7), (6, 7)]: g[r][c] = 3  # size 3
        return g
    if name == "all_same_size":
        # all motifs equal size matching count → all recolored, output uniform
        g[0][1] = 1; g[0][3] = 1  # count = 2
        for (r, c) in [(3, 3), (3, 4)]: g[r][c] = 3
        for (r, c) in [(5, 6), (5, 7)]: g[r][c] = 3
        for (r, c) in [(7, 1), (7, 2)]: g[r][c] = 3
        return g
    return g
