"""Generator for v2_meta_puzzles:H4 — mirror non-5 cells across vertical 5-axis.

Rule: a vertical axis defined by a single color-5 cell. All non-{0, 5} cells
are mirrored to the opposite column (col-distance preserved).

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_motifs,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_axis, motif_on_axis, motif_on_both_sides.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "158efba9f453"
VERSION = "1.1.0"
TASK_ID = "158efba9f453"
SUMMARY = "Single color-5 axis marker + 2-3 motifs in distinct non-{0, 5} colors on one side."

INVARIANTS = [
    "background is 0",
    "exactly one color-5 single-cell axis marker",
    "2-3 small motifs in distinct non-{0, 5} colors entirely on one side of the axis column",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_axis", "motif_on_axis", "motif_on_both_sides")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 7..9", "valid": "5..14"},
    "grid_w":         {"type": "int", "default": "rng 9..11", "valid": "8..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_motifs":       {"type": "int", "default": "rng 2..3", "valid": "1..4"},
    "palette_size":   {"type": "int", "default": "rng 2..3", "valid": "1..4"},
    "position_bias":  {"type": "str", "default": "one_side_of_axis",
                       "valid": "one_side_of_axis"},
    "n_distinct_colors": {"type": "int", "default": "rng 2..3", "valid": "1..4"},
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
        n = ctx.draw_int("n_motifs", 2, 2)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("grid_w", 10, 11)
        n = ctx.draw_int("n_motifs", 3, 3)
    else:
        h = ctx.draw_int("grid_h", 7, 9)
        w = ctx.draw_int("grid_w", 9, 11)
        n = ctx.draw_int("n_motifs", 2, 3)
    rng = ctx.draw_rng("layout")

    for outer in range(40):
        g = full_grid(h, w, 0)
        axis_c = rng.randint(w // 2, w - 3)
        axis_r = rng.randint(0, h - 1)
        g[axis_r][axis_c] = 5
        colors = rng.sample([1, 2, 3, 4, 6, 7, 8, 9], n)
        ok = True
        for color in colors:
            cells = _build_motif(rng, rng.randint(2, 4))
            rs = [r for r, _ in cells]; cs = [c for _, c in cells]
            sh = max(rs) - min(rs) + 1; sw = max(cs) - min(cs) + 1
            placed = False
            for _ in range(120):
                r0 = rng.randint(0, h - sh)
                c0 = rng.randint(0, axis_c - sw)
                cells_p = [(r0 + r - min(rs), c0 + c - min(cs)) for r, c in cells]
                if any(g[r][c] != 0 for r, c in cells_p): continue
                ok2 = True
                for r, c in cells_p:
                    mc = 2 * axis_c - c
                    if not (0 <= mc < w): ok2 = False; break
                if not ok2: continue
                for r, c in cells_p:
                    g[r][c] = color
                placed = True; break
            if not placed:
                ok = False; break
        if ok:
            return g
    raise ValueError("could not realize H4 layout")


def _draw_from_degenerate(name, rng):
    h, w = 8, 11
    g = full_grid(h, w, 0)
    if name == "no_axis":
        # no color-5 cell → no mirror axis defined, rule has no anchor
        for r, c in [(2, 2), (3, 3), (4, 1)]:
            g[r][c] = 4
        return g
    if name == "motif_on_axis":
        # motif cell at the axis column → ambiguous which side the cell belongs to
        g[3][5] = 5  # axis
        for r, c in [(2, 5), (3, 4), (4, 5)]:
            g[r][c] = 4
        return g
    if name == "motif_on_both_sides":
        # cells on both sides of the axis → "entirely on one side" invariant violated
        g[3][5] = 5  # axis
        for r, c in [(2, 2), (3, 3)]:
            g[r][c] = 4
        for r, c in [(4, 7), (5, 8)]:
            g[r][c] = 4
        return g
    return g
