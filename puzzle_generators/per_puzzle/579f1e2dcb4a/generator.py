"""Generator for 5b:m30 — crop components and pack left-to-right.

Rule: components sorted by (col, row). Output is hconcat of their crops
(top-aligned), with 1-col gaps.

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: tied_leftmost (≥2 components share a leftmost col → sort
falls back to row, output ambiguous), single_motif (only one component
→ pack is trivial, just one crop), no_motifs (no components → output
is empty/undefined).
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "579f1e2dcb4a"
VERSION = "1.1.0"
TASK_ID = "579f1e2dcb4a"
SUMMARY = "3 small shapes in distinct colors at distinct leftmost columns."

INVARIANTS = [
    "background is 0",
    "exactly 3 connected components, distinct colors",
    "each component has a strictly distinct leftmost column",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("tied_leftmost", "single_motif", "no_motifs")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 9..11", "valid": "8..14"},
    "grid_w":         {"type": "int", "default": "rng 12..14", "valid": "11..18"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "palette_size":   {"type": "int", "default": "3", "valid": "3..3"},
    "position_bias":  {"type": "str", "default": "distinct_leftmost_columns",
                       "valid": "distinct_leftmost_columns"},
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
    [(0, 0), (1, 0), (1, 1)],
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
        h = ctx.draw_int("grid_h", 11, 14)
        w = ctx.draw_int("grid_w", 14, 18)
    else:
        h = ctx.draw_int("grid_h", 9, 11)
        w = ctx.draw_int("grid_w", 12, 14)
    rng = ctx.draw_rng("layout")
    for _ in range(40):
        g = full_grid(h, w, 0)
        palette = rng.sample([1, 2, 3, 4, 6, 7, 8, 9], 3)
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
                shape_left = min(c for _, c in shape)
                lc = c0 + shape_left
                if lc in leftmosts: continue
                for dr, dc in shape:
                    g[r0 + dr][c0 + dc] = color
                leftmosts.append(lc); placed = True; break
            if not placed: ok = False; break
        if ok and len(set(leftmosts)) == 3:
            return g
    return g


def _draw_from_degenerate(name, rng):
    h, w = 10, 13
    g = full_grid(h, w, 0)
    if name == "tied_leftmost":
        # Two components share leftmost column — rule's sort by col
        # falls back to row tie-break; output ambiguous.
        for dr, dc in _SHAPES[0]:
            g[1 + dr][3 + dc] = 1
        for dr, dc in _SHAPES[2]:
            g[5 + dr][3 + dc] = 3
        for dr, dc in _SHAPES[4]:
            g[1 + dr][8 + dc] = 4
        return g
    if name == "single_motif":
        # Only one component — pack is trivial, just one crop.
        for dr, dc in _SHAPES[1]:
            g[3 + dr][5 + dc] = 6
        return g
    if name == "no_motifs":
        # No components — pack output is empty/undefined.
        return g
    return g
