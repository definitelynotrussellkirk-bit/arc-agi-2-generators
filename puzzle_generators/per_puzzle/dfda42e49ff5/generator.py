"""Generator for arc_puzzle_bank_next21:M13 — fill horizontal gaps within each object.

Rule: for each object, each row of the object has its min-col to max-col
horizontal span filled with the object's color.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_motifs,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_motifs, all_solid_rects, single_row_motifs.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "dfda42e49ff5"
VERSION = "1.1.0"
TASK_ID = "dfda42e49ff5"

SUMMARY = "1-2 connected motifs in distinct colors with internal gaps in some rows."

INVARIANTS = [
    "background is 0",
    "1-2 connected motifs in distinct non-zero colors",
    "at least one motif has a row with internal gap (cells of color, then bg, then color again)",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_motifs", "all_solid_rects", "single_row_motifs")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 5..7", "valid": "4..10"},
    "grid_w":         {"type": "int", "default": "rng 7..9", "valid": "5..12"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_motifs":       {"type": "int", "default": "rng 1..2", "valid": "1..3"},
    "palette_size":   {"type": "int", "default": "rng 1..2", "valid": "1..9"},
    "position_bias":  {"type": "str", "default": "spaced_gappy_motifs",
                       "valid": "spaced_gappy_motifs"},
    "n_distinct_colors": {"type": "int", "default": "rng 1..2", "valid": "1..9"},
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


GAP_SHAPES = [
    [(0, 0), (0, 1), (0, 2), (1, 0), (1, 2), (2, 0), (2, 1), (2, 2)],
    [(0, 0), (0, 2), (1, 0), (1, 1), (1, 2), (2, 0), (2, 2)],
    [(0, 0), (0, 1), (1, 0), (2, 0), (2, 1)],
    [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (1, 0), (1, 4)],
    [(0, 0), (0, 1), (0, 2), (1, 0), (1, 2), (2, 0), (2, 1), (2, 2)],
]


def _build_motif(rng, k):
    return list(rng.choice(GAP_SHAPES))


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 5, 5)
        w = ctx.draw_int("grid_w", 7, 7)
        n = ctx.draw_int("n_motifs", 1, 1)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 6, 7)
        w = ctx.draw_int("grid_w", 8, 9)
        n = ctx.draw_int("n_motifs", 2, 2)
    else:
        h = ctx.draw_int("grid_h", 5, 7)
        w = ctx.draw_int("grid_w", 7, 9)
        n = ctx.draw_int("n_motifs", 1, 2)
    rng = ctx.draw_rng("layout")

    for outer in range(40):
        g = full_grid(h, w, 0)
        colors = rng.sample([1, 2, 3, 4, 5, 6, 7, 8, 9], n)
        ok = True
        for color in colors:
            cells = _build_motif(rng, rng.randint(4, 6))
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
    h, w = 6, 8
    g = full_grid(h, w, 0)
    if name == "no_motifs":
        # blank → no objects, rule has no effect
        return g
    if name == "all_solid_rects":
        # solid rectangles → no internal gaps to fill, rule is identity
        for r in range(2):
            for c in range(3): g[1 + r][1 + c] = 4
        for r in range(2):
            for c in range(3): g[3 + r][4 + c] = 6
        return g
    if name == "single_row_motifs":
        # 1xN horizontal lines → already span full row from min to max, identity
        for c in range(1, 5): g[2][c] = 4
        for c in range(2, 7): g[4][c] = 6
        return g
    return g
