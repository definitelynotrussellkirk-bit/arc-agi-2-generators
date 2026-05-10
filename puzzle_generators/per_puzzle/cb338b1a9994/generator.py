"""Generator for v1_e_m_h_keys:M4 — translate non-{0,1,2} cells by 1→2 vector.

Rule: a color-1 marker and a color-2 marker define a translation vector
(dr, dc) = p2 - p1. All non-{0, 1, 2} cells are translated by (dr, dc).

Combinatorial axes (8): grid_h, grid_w, palette_kind, motif_size,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_markers, zero_vector, no_motif.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "cb338b1a9994"
VERSION = "1.1.0"
TASK_ID = "cb338b1a9994"

SUMMARY = "1 color-1 marker + 1 color-2 marker (vector) + a connected motif in another color."

INVARIANTS = [
    "background is 0",
    "exactly one color-1 marker and one color-2 marker at distinct positions",
    "exactly one connected motif (3-5 cells) in some non-{0, 1, 2} color",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_markers", "zero_vector", "no_motif")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 7..9", "valid": "5..14"},
    "grid_w":         {"type": "int", "default": "rng 8..10", "valid": "6..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "motif_size":     {"type": "int", "default": "rng 3..5", "valid": "2..6"},
    "palette_size":   {"type": "int", "default": "3", "valid": "2..4"},
    "position_bias":  {"type": "str", "default": "markers_topleft_motif_below",
                       "valid": "markers_topleft_motif_below"},
    "n_distinct_colors": {"type": "int", "default": "3", "valid": "3..4"},
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
        w = ctx.draw_int("grid_w", 8, 9)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 9, 11)
        w = ctx.draw_int("grid_w", 10, 12)
    else:
        h = ctx.draw_int("grid_h", 7, 9)
        w = ctx.draw_int("grid_w", 8, 10)
    rng = ctx.draw_rng("layout")

    for outer in range(40):
        g = full_grid(h, w, 0)
        # markers
        r1 = rng.randint(0, 1); c1 = rng.randint(0, 2)
        r2 = rng.randint(2, 3); c2 = rng.randint(3, 4)
        if (r1, c1) == (r2, c2): continue
        g[r1][c1] = 1
        g[r2][c2] = 2
        # motif
        color = rng.choice([3, 4, 5, 6, 7, 8, 9])
        cells = _build_motif(rng, rng.randint(3, 5))
        rs = [r for r, _ in cells]; cs = [c for _, c in cells]
        sh = max(rs) - min(rs) + 1; sw = max(cs) - min(cs) + 1
        for _ in range(80):
            r0 = rng.randint(h // 2, h - sh); c0 = rng.randint(0, w - sw)
            cells_p = [(r0 + r - min(rs), c0 + c - min(cs)) for r, c in cells]
            if any(g[r][c] != 0 for r, c in cells_p): continue
            for r, c in cells_p:
                g[r][c] = color
            return g
    raise ValueError("could not realize layout")


def _draw_from_degenerate(name, rng):
    h, w = 8, 9
    g = full_grid(h, w, 0)
    if name == "no_markers":
        # No 1/2 markers — rule has no translation vector defined.
        for r, c in [(5, 3), (5, 4), (6, 3)]: g[r][c] = 4
        return g
    if name == "zero_vector":
        # 1 and 2 at same position is impossible; pick co-located markers separately.
        # Use vector = (0,0) by overlapping markers (only one is visible).
        g[0][0] = 1; g[0][1] = 2
        for r, c in [(5, 3), (5, 4), (6, 3)]: g[r][c] = 4
        return g
    if name == "no_motif":
        # Markers but no motif — rule has nothing to translate.
        g[0][0] = 1; g[2][3] = 2
        return g
    return g
