"""Generator for 17b:hard_119 — build pairwise union gallery.

Rule: connected components sorted by column. Each is binary-cropped
and padded to common dims. Output is NxN gallery where each cell is
the cellwise OR of two padded shapes, painted color 8, with 1-cell
gaps between gallery cells.

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: tied_columns (≥2 shapes share leftmost col → sort
ambiguous, gallery row/col order ambiguous), all_same_shape (all 3
shapes identical → off-diagonal OR equals diagonal, gallery has no
contrast), single_shape (only 1 component → 1x1 gallery, no pairwise
union shown).
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "27b865c5f43a"
VERSION = "1.1.0"
TASK_ID = "27b865c5f43a"

SUMMARY = "3 components in distinct colors at distinct columns."

INVARIANTS = [
    "background is 0",
    "exactly 3 isolated components in distinct colors",
    "components placed at strictly distinct leftmost columns",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("tied_columns", "all_same_shape", "single_shape")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 9..11", "valid": "8..14"},
    "grid_w":         {"type": "int", "default": "rng 12..14", "valid": "11..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "palette_size":   {"type": "int", "default": "3", "valid": "3..3"},
    "position_bias":  {"type": "str", "default": "three_distinct_columns",
                       "valid": "three_distinct_columns"},
    "n_distinct_colors": {"type": "int", "default": "3", "valid": "3..3"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


_SHAPES = [
    [(0, 0), (0, 1), (1, 0)],
    [(0, 0), (1, 0), (1, 1), (2, 1)],
    [(0, 0), (0, 1), (0, 2), (1, 1)],
    [(0, 0), (0, 1), (1, 0), (1, 1)],
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
        h = ctx.draw_int("grid_h", 9, 9)
        w = ctx.draw_int("grid_w", 12, 12)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 11, 13)
        w = ctx.draw_int("grid_w", 14, 16)
    else:
        h = ctx.draw_int("grid_h", 9, 11)
        w = ctx.draw_int("grid_w", 12, 14)
    rng = ctx.draw_rng("layout")
    palette = rng.sample([1, 2, 3, 4, 5, 6, 7, 8, 9], 3)
    for outer in range(40):
        g = full_grid(h, w, 0)
        leftmosts = []
        ok = True
        for color in palette:
            placed = False
            for _ in range(60):
                shape = rng.choice(_SHAPES)
                sh = max(r for r, _ in shape) + 1
                sw = max(c for _, c in shape) + 1
                r0 = rng.randint(0, h - sh); c0 = rng.randint(0, w - sw)
                if not _free(g, r0, c0, r0 + sh - 1, c0 + sw - 1): continue
                lc = c0 + min(c for _, c in shape)
                if lc in leftmosts: continue
                for dr, dc in shape:
                    g[r0 + dr][c0 + dc] = color
                leftmosts.append(lc); placed = True; break
            if not placed: ok = False; break
        if ok and len(set(leftmosts)) == 3:
            return g
    raise ValueError("could not place 3 shapes at distinct cols")


def _draw_from_degenerate(name, rng):
    h, w = 10, 13
    g = full_grid(h, w, 0)
    if name == "tied_columns":
        # Two shapes share leftmost col — rule's column-sort
        # falls to row tie-break; gallery row/col order ambiguous.
        for dr, dc in _SHAPES[0]:
            g[1 + dr][2 + dc] = 1
        for dr, dc in _SHAPES[2]:
            g[5 + dr][2 + dc] = 3
        for dr, dc in _SHAPES[3]:
            g[1 + dr][8 + dc] = 4
        return g
    if name == "all_same_shape":
        # All 3 shapes identical — off-diagonal OR equals diagonal,
        # gallery has no contrast across rows/cols.
        for dr, dc in _SHAPES[3]:
            g[1 + dr][1 + dc] = 1
        for dr, dc in _SHAPES[3]:
            g[1 + dr][6 + dc] = 3
        for dr, dc in _SHAPES[3]:
            g[1 + dr][10 + dc] = 4
        return g
    if name == "single_shape":
        # Only 1 component — 1x1 gallery; no pairwise union shown.
        for dr, dc in _SHAPES[1]:
            g[3 + dr][5 + dc] = 6
        return g
    return g
