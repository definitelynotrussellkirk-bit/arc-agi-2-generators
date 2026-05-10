"""Generator for v2_meta_puzzles:E3 — keep border-touching objects.

Rule: only objects that touch the grid border are kept; interior-only
objects are erased.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_motifs,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: all_border, all_interior, no_motifs.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "9de4ae27d0d0"
VERSION = "1.1.0"
TASK_ID = "9de4ae27d0d0"
SUMMARY = "2-4 connected motifs in distinct colors; some touch the grid border, some do not."

INVARIANTS = [
    "background is 0",
    "2-4 motifs in distinct non-zero colors",
    "at least one motif touches the grid border and at least one does not",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("all_border", "all_interior", "no_motifs")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 7..9", "valid": "5..12"},
    "grid_w":         {"type": "int", "default": "rng 7..9", "valid": "5..12"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_motifs":       {"type": "int", "default": "rng 2..4", "valid": "2..5"},
    "palette_size":   {"type": "int", "default": "rng 2..4", "valid": "2..9"},
    "position_bias":  {"type": "str", "default": "border_plus_interior_motifs",
                       "valid": "border_plus_interior_motifs"},
    "n_distinct_colors": {"type": "int", "default": "rng 2..4", "valid": "2..9"},
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
        w = ctx.draw_int("grid_w", 7, 8)
        n = ctx.draw_int("n_motifs", 2, 2)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("grid_w", 8, 9)
        n = ctx.draw_int("n_motifs", 3, 4)
    else:
        h = ctx.draw_int("grid_h", 7, 9)
        w = ctx.draw_int("grid_w", 7, 9)
        n = ctx.draw_int("n_motifs", 2, 4)
    rng = ctx.draw_rng("layout")

    for outer in range(40):
        g = full_grid(h, w, 0)
        colors = rng.sample([1, 2, 3, 4, 5, 6, 7, 8, 9], n)
        touching = (n + 1) // 2
        ok = True
        for i, color in enumerate(colors):
            cells = _build_motif(rng, rng.randint(2, 4))
            rs = [r for r, _ in cells]; cs = [c for _, c in cells]
            sh = max(rs) - min(rs) + 1; sw = max(cs) - min(cs) + 1
            placed = False
            wants_border = i < touching
            for _ in range(120):
                if wants_border:
                    if rng.choice([True, False]):
                        r0 = rng.choice([0, h - sh]); c0 = rng.randint(0, w - sw)
                    else:
                        r0 = rng.randint(0, h - sh); c0 = rng.choice([0, w - sw])
                else:
                    r0 = rng.randint(1, h - sh - 1) if h - sh > 1 else 0
                    c0 = rng.randint(1, w - sw - 1) if w - sw > 1 else 0
                if not _free(g, r0, c0, r0 + sh - 1, c0 + sw - 1): continue
                for r, c in cells:
                    g[r0 + r - min(rs)][c0 + c - min(cs)] = color
                placed = True; break
            if not placed:
                ok = False; break
        if ok:
            return g
    raise ValueError("could not realize E3 layout")


def _draw_from_degenerate(name, rng):
    h, w = 8, 8
    g = full_grid(h, w, 0)
    if name == "all_border":
        # all motifs touch the border → rule keeps everything, no contrast
        for (r, c) in [(0, 1), (0, 2), (1, 1)]: g[r][c] = 4
        for (r, c) in [(h - 1, 5), (h - 1, 6)]: g[r][c] = 6
        for (r, c) in [(3, 0), (4, 0)]: g[r][c] = 3
        return g
    if name == "all_interior":
        # no motif touches border → rule erases everything, output is empty
        for (r, c) in [(2, 2), (2, 3), (3, 2)]: g[r][c] = 4
        for (r, c) in [(5, 5), (5, 6), (6, 5)]: g[r][c] = 6
        return g
    if name == "no_motifs":
        # blank grid → rule has nothing to keep or drop
        return g
    return g
