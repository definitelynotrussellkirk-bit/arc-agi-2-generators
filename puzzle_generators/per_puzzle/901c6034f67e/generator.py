"""Generator for arc_puzzle_bank_21_set8:medium_h10 — rank objs by size, recolor by rank.

Rule: connected components are ranked by size (descending) then by position;
each is recolored to a fixed palette by rank.

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: tied_sizes (≥2 components share a size → "rank by size"
falls back to position tie-break, output ambiguous), single_motif
(only one component → only rank-1 color used; lower-rank colors gone),
no_motifs (no components → ranking has nothing to assign).
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "901c6034f67e"
VERSION = "1.1.0"
TASK_ID = "901c6034f67e"

SUMMARY = "3 connected motifs of strictly different sizes in distinct colors."

INVARIANTS = [
    "background is 0",
    "exactly 3 motifs in distinct non-zero colors with strictly different sizes",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("tied_sizes", "single_motif", "no_motifs")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 7..9", "valid": "5..14"},
    "grid_w":         {"type": "int", "default": "rng 9..11", "valid": "7..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "palette_size":   {"type": "int", "default": "3", "valid": "3..3"},
    "position_bias":  {"type": "str", "default": "three_distinct_size_motifs",
                       "valid": "three_distinct_size_motifs"},
    "n_distinct_colors": {"type": "int", "default": "3", "valid": "3..3"},
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
        w = ctx.draw_int("grid_w", 9, 9)
        sizes_pool = [3, 5, 7]
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 9, 12)
        w = ctx.draw_int("grid_w", 11, 14)
        sizes_pool = [3, 6, 9]
    else:
        h = ctx.draw_int("grid_h", 7, 9)
        w = ctx.draw_int("grid_w", 9, 11)
        sizes_pool = [3, 5, 7]
    rng = ctx.draw_rng("layout")

    for outer in range(40):
        g = full_grid(h, w, 0)
        sizes = list(sizes_pool)
        rng.shuffle(sizes)
        colors = rng.sample([1, 2, 3, 4, 5, 6, 7, 8, 9], 3)
        ok = True
        for size, color in zip(sizes, colors):
            cells = _build_motif(rng, size)
            rs = [r for r, _ in cells]; cs = [c for _, c in cells]
            sh = max(rs) - min(rs) + 1; sw = max(cs) - min(cs) + 1
            placed = False
            for _ in range(120):
                r0 = rng.randint(0, h - sh); c0 = rng.randint(0, w - sw)
                if not _free(g, r0, c0, r0 + sh - 1, c0 + sw - 1): continue
                for r, c in cells:
                    g[r0 + r - min(rs)][c0 + c - min(cs)] = color
                placed = True; break
            if not placed:
                ok = False; break
        if ok:
            return g
    raise ValueError("could not realize layout")


def _draw_from_degenerate(name, rng):
    h, w = 8, 11
    g = full_grid(h, w, 0)
    if name == "tied_sizes":
        # All 3 components have size 3 — rank-by-size is ambiguous;
        # output decided only by positional tie-break.
        for r, c in [(1, 1), (1, 2), (2, 2)]: g[r][c] = 1
        for r, c in [(1, 7), (1, 8), (2, 8)]: g[r][c] = 3
        for r, c in [(5, 4), (5, 5), (6, 5)]: g[r][c] = 4
        return g
    if name == "single_motif":
        # Only one component — only rank-1 color is used; lower
        # ranks unassigned.
        for r, c in [(2, 4), (2, 5), (3, 5), (3, 6), (4, 6)]: g[r][c] = 6
        return g
    if name == "no_motifs":
        # Empty grid — rank assignment has nothing.
        return g
    return g
