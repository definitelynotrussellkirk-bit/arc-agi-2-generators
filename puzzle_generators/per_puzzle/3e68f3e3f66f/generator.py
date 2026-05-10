"""Generator for arc_additional_puzzles_21_set10_bundle:H64 — legend-recolored broadcast copies.

Rule: row 0 holds a legend of N colors. A single source cell (color 5)
sits near a motif (markers in some non-{0,5,6,legend} color). For each
of the N anchors (color 6), the motif is copied with the source aligned
to the anchor and recolored to legend[i] (anchors sorted row-major).
Out-of-bounds offsets are clipped.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "3e68f3e3f66f"
VERSION = "1.1.0"
TASK_ID = "3e68f3e3f66f"

SUMMARY = "Top-row legend + source + motif + N anchors broadcasting motif recolored by legend[i]."

INVARIANTS = [
    "background is 0",
    "row 0 holds 2-3 non-zero legend colors at cols 0..N-1, rest 0",
    "exactly one source cell (color 5) below row 0",
    "anchor count (color 6) equals legend size",
    "motif: 2-3 cells of one marker color near source (not in {0,5,6,legend})",
    "anchors do not collide with motif/source/each other",
]

AXES = {
    "grid_h": {"type": "int", "default": "rng 10..12", "valid": "9..14"},
    "grid_w": {"type": "int", "default": "rng 10..12", "valid": "9..14"},
    "n_legend": {"type": "int", "default": "rng 2..3", "valid": "2..3"},
}


_MOTIF_SHAPES = [
    [(-1, 0), (0, 1), (1, -1)],
    [(-1, 0), (1, 0), (0, 1)],
    [(0, 1), (1, 0)],
    [(-1, 0), (0, 1)],
    [(-1, 0), (-1, 1), (1, 0)],
    [(-1, 1), (0, 1), (1, 0)],
    [(0, -1), (0, 1), (1, 0)],
]


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    h = ctx.draw_int("grid_h", 10, 12)
    w = ctx.draw_int("grid_w", 10, 12)
    n_legend = ctx.draw_int("n_legend", 2, 3)
    rng = ctx.draw_rng("layout")

    palette = [1, 2, 3, 4, 7, 8, 9]
    rng.shuffle(palette)
    legend_colors = palette[:n_legend]
    motif_color = palette[n_legend]

    for outer in range(80):
        g = full_grid(h, w, 0)
        for i, lc in enumerate(legend_colors):
            g[0][i] = lc

        offsets = rng.choice(_MOTIF_SHAPES)
        min_dr = min(0, *(dr for dr, _ in offsets))
        max_dr = max(0, *(dr for dr, _ in offsets))
        min_dc = min(0, *(dc for _, dc in offsets))
        max_dc = max(0, *(dc for _, dc in offsets))
        # source row must be ≥1 and ≥ -min_dr+1 so motif doesn't enter row 0
        src_r_lo = max(2, 1 - min_dr)
        src_r_hi = h - 1 - max_dr
        src_c_lo = -min_dc
        src_c_hi = w - 1 - max_dc
        if src_r_lo > src_r_hi or src_c_lo > src_c_hi:
            continue
        src_r = rng.randint(src_r_lo, src_r_hi)
        src_c = rng.randint(src_c_lo, src_c_hi)

        g[src_r][src_c] = 5
        motif_ok = True
        for dr, dc in offsets:
            r2, c2 = src_r + dr, src_c + dc
            if r2 == 0 or g[r2][c2] != 0:
                motif_ok = False
                break
            g[r2][c2] = motif_color
        if not motif_ok:
            continue

        placed_anchors = []
        ok = True
        for ai in range(n_legend):
            placed = False
            for _ in range(120):
                ar = rng.randint(1, h - 1)
                ac = rng.randint(0, w - 1)
                if g[ar][ac] != 0:
                    continue
                if abs(ar - src_r) + abs(ac - src_c) < 3:
                    continue
                if any(abs(ar - pr) + abs(ac - pc) < 3 for pr, pc in placed_anchors):
                    continue
                g[ar][ac] = 6
                placed_anchors.append((ar, ac))
                placed = True
                break
            if not placed:
                ok = False
                break
        if ok:
            return g
    raise ValueError("could not realize legend broadcast layout in 80 attempts")
