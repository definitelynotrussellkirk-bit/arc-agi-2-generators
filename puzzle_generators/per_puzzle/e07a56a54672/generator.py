"""Generator for v3_rich_schema:hard_02_scale_smallest_object_2x — scale smallest 2x.

Rule: 2 color-3 motifs of strictly different sizes; the smallest is scaled
2× (each cell → 2×2 block) and painted in color 8.

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: equal_sizes (both motifs same size → "smallest" is
ambiguous; tie-break by position is the only signal); single_motif
(only 1 motif → rule's "smallest of two" precondition fails);
no_motifs (empty grid → rule's selector finds nothing, output is empty).
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "e07a56a54672"
VERSION = "1.1.0"
TASK_ID = "e07a56a54672"

SUMMARY = "2 separated color-3 motifs of strictly different sizes."

INVARIANTS = [
    "background is 0",
    "all non-zero cells are color 3",
    "exactly 2 separated color-3 motifs with strictly different sizes",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("equal_sizes", "single_motif", "no_motifs")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 9..11", "valid": "7..14"},
    "grid_w":         {"type": "int", "default": "rng 11..13", "valid": "8..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "palette_size":   {"type": "int", "default": "1", "valid": "1..1"},
    "position_bias":  {"type": "str", "default": "two_unequal_motifs",
                       "valid": "two_unequal_motifs"},
    "n_distinct_colors": {"type": "int", "default": "1", "valid": "1..1"},
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
        h = ctx.draw_int("grid_h", 9, 9)
        w = ctx.draw_int("grid_w", 11, 11)
        size_pair = (2, 4)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 11, 14)
        w = ctx.draw_int("grid_w", 13, 16)
        size_pair = (3, 6)
    else:
        h = ctx.draw_int("grid_h", 9, 11)
        w = ctx.draw_int("grid_w", 11, 13)
        size_pair = (2, 4)
    rng = ctx.draw_rng("layout")

    for outer in range(40):
        g = full_grid(h, w, 0)
        sizes = list(size_pair)
        rng.shuffle(sizes)
        ok = True
        for size in sizes:
            cells = _build_motif(rng, size)
            rs = [r for r, _ in cells]; cs = [c for _, c in cells]
            sh = max(rs) - min(rs) + 1; sw = max(cs) - min(cs) + 1
            placed = False
            for _ in range(120):
                r0 = rng.randint(0, h - sh); c0 = rng.randint(0, w - sw)
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
    h, w = 10, 12
    g = full_grid(h, w, 0)
    if name == "equal_sizes":
        # Both motifs same cell count → rule's "smallest" is
        # ambiguous; only positional tie-break decides which scales.
        for r, c in [(2, 2), (2, 3), (3, 3)]: g[r][c] = 3
        for r, c in [(6, 7), (6, 8), (7, 8)]: g[r][c] = 3
        return g
    if name == "single_motif":
        # Only one motif — rule's "smallest of two" precondition
        # fails; output's contrast (smallest scaled, largest kept)
        # collapses.
        for r, c in [(3, 3), (3, 4), (4, 4)]: g[r][c] = 3
        return g
    if name == "no_motifs":
        # Empty grid — rule's selector finds nothing.
        return g
    return g
