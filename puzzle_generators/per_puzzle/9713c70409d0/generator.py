"""Generator for arc_puzzle_bank_21_set18_s:S18_H2 — multi-pair motifs.

Rule: 3 pairs of motifs in distinct colors (each pair = 2 same-color
motif occurrences). Rule action: per-color pair-difference.

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: no_motifs, single_per_color, identical_pair.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "9713c70409d0"
VERSION = "1.1.0"
TASK_ID = "9713c70409d0"

SUMMARY = "3 pairs of motifs in distinct colors at distinct positions."

INVARIANTS = [
    "background is 0",
    "3 pairs of multi-cell motifs in distinct colors",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_motifs", "single_per_color", "identical_pair")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 6..8", "valid": "5..14"},
    "grid_w":         {"type": "int", "default": "rng 11..13", "valid": "9..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "palette_size":   {"type": "int", "default": "3", "valid": "3..3"},
    "position_bias":  {"type": "str", "default": "three_motif_pairs",
                       "valid": "three_motif_pairs"},
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


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 6, 6)
        w = ctx.draw_int("grid_w", 11, 12)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 8, 12)
        w = ctx.draw_int("grid_w", 13, 16)
    else:
        h = ctx.draw_int("grid_h", 6, 8)
        w = ctx.draw_int("grid_w", 11, 13)
    rng = ctx.draw_rng("layout")

    SHAPES = [
        [(0, 0), (0, 2)],
        [(0, 0), (2, 0)],
        [(0, 0), (0, 1), (1, 1)],
        [(0, 0), (1, 0), (1, 1)],
    ]

    for outer in range(40):
        g = full_grid(h, w, 0)
        colors = rng.sample([2, 3, 4, 5, 6, 7], 3)
        ok = True
        for color in colors:
            for _ in range(2):
                shape = rng.choice(SHAPES)
                rs = [r for r, _ in shape]; cs = [c for _, c in shape]
                sh = max(rs) - min(rs) + 1; sw = max(cs) - min(cs) + 1
                placed = False
                for _ in range(80):
                    r0 = rng.randint(0, h - sh); c0 = rng.randint(0, w - sw)
                    if not _free(g, r0, c0, r0 + sh - 1, c0 + sw - 1): continue
                    for r, c in shape:
                        g[r0 + r][c0 + c] = color
                    placed = True; break
                if not placed:
                    ok = False; break
            if not ok: break
        if ok:
            return g
    raise ValueError("could not realize layout")


def _draw_from_degenerate(name, rng):
    h, w = 7, 12
    g = full_grid(h, w, 0)
    if name == "no_motifs":
        # Empty grid — rule has no motif pairs to compare.
        return g
    if name == "single_per_color":
        # Each color appears once (no pair) — rule's "pair
        # difference" precondition fails.
        for r, c in [(1, 1), (2, 1)]: g[r][c] = 4
        for r, c in [(4, 7), (5, 7)]: g[r][c] = 6
        for r, c in [(1, 9), (2, 9)]: g[r][c] = 7
        return g
    if name == "identical_pair":
        # Both motifs of one color identical (no shape difference)
        # — rule's pair-diff yields no signal for that color.
        for r, c in [(1, 1), (2, 1), (2, 2)]: g[r][c] = 4
        for r, c in [(1, 5), (2, 5), (2, 6)]: g[r][c] = 4
        for r, c in [(4, 1), (4, 2)]: g[r][c] = 6
        for r, c in [(4, 9), (4, 10)]: g[r][c] = 6
        return g
    return g
