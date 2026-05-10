"""Generator for d2acf2cb.

Rule: cells in 4-anchored rows (col 0 == col w-1 == 4) or 4-anchored
cols (row 0 == row h-1 == 4) get swapped: 0↔8 and 6↔7.

Combinatorial axes (8): grid_h/w, n_anchored_rows, n_anchored_cols,
fg_density, palette_distribution, position_bias, swap_visibility,
asymmetry_force.
Degenerates: no_anchors, all_anchored, single_anchor.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "832404dc8a5c"
VERSION = "1.1.0"
TASK_ID = "832404dc8a5c"
SUMMARY = "Grid with 4-anchored rows/cols; rule swaps 0↔8 and 6↔7 in those."

INVARIANTS = [
    "background uses {0, 6, 7, 8} cells",
    ">=1 row with 4 at col 0 AND col w-1",
    "interior cells of anchored rows have at least one of {0, 6, 7, 8}",
    "interior cells contain >=1 cell that swaps (so rule effect is visible)",
]

PALETTE_DISTS = ("uniform", "0_heavy", "8_heavy", "6_heavy", "7_heavy")
DEGENERATE_TEXTURES = ("no_anchors", "all_anchored", "single_anchor")
HELPFUL_TEXTURES = PALETTE_DISTS

AXES = {
    "grid_h":              {"type": "int", "default": "rng 7..12", "valid": "6..16"},
    "grid_w":              {"type": "int", "default": "rng 8..14", "valid": "7..18"},
    "n_anchored_rows":     {"type": "int", "default": "rng 1..3", "valid": "0..5"},
    "n_anchored_cols":     {"type": "int", "default": "rng 0..2", "valid": "0..5"},
    "fg_density":          {"type": "float", "default": "rng 0.4..0.7",
                            "valid": "0.2..1"},
    "palette_distribution": {"type": "str", "default": "rng helpful",
                             "valid": "|".join(PALETTE_DISTS)},
    "include_decoy":       {"type": "bool", "default": "false",
                            "valid": "true|false"},
    "position_bias":       {"type": "str", "default": "rng spread|center",
                            "valid": "spread|center"},
    "texture":             {"type": "str", "default": "alias for palette_distribution",
                            "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if difficulty == "easy":
        h_lo, h_hi, w_lo, w_hi = 6, 8, 7, 9
    elif difficulty == "hard":
        h_lo, h_hi, w_lo, w_hi = 11, 16, 12, 18
    else:
        h_lo, h_hi, w_lo, w_hi = 7, 12, 8, 14
    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", w_lo, w_hi)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], h, w, rng)
    n_arows = int(overrides.get("n_anchored_rows",
                                ctx.draw_int("n_anchored_rows", 1, 3)))
    n_acols = int(overrides.get("n_anchored_cols",
                                ctx.draw_int("n_anchored_cols", 0, 2)))
    n_arows = max(1, min(h - 2, n_arows))
    n_acols = max(0, min(w - 2, n_acols))
    palette_dist = (overrides.get("texture") or
                    overrides.get("palette_distribution")
                    or ctx.draw_choice("palette_distribution",
                                       list(PALETTE_DISTS)))
    density = float(overrides.get("fg_density",
                                  ctx.draw_rng("fg_density")
                                  .uniform(0.4, 0.7)))
    palette = _palette_weighted(palette_dist)
    g = full_grid(h, w, 0)
    for r in range(h):
        for c in range(w):
            if rng.random() < density:
                g[r][c] = rng.choice(palette)
    anchor_rows = rng.sample(range(1, h - 1), n_arows)
    for r in anchor_rows:
        g[r][0] = 4
        g[r][w - 1] = 4
        for c in range(1, w - 1):
            if g[r][c] not in (0, 6, 7, 8):
                g[r][c] = rng.choice([6, 7, 8])
    if n_acols > 0:
        anchor_cols = rng.sample(range(1, w - 1), n_acols)
        for c in anchor_cols:
            g[0][c] = 4
            g[h - 1][c] = 4
            for r in range(1, h - 1):
                if g[r][c] not in (0, 6, 7, 8):
                    g[r][c] = rng.choice([6, 7, 8])
    has_swap_visible = False
    for r in anchor_rows:
        for c in range(1, w - 1):
            if g[r][c] in (0, 6, 7, 8) and g[r][c] != 0:
                has_swap_visible = True
                break
        if has_swap_visible:
            break
    if not has_swap_visible and anchor_rows:
        r = anchor_rows[0]
        g[r][1] = 8
    return g


def _palette_weighted(dist):
    if dist == "0_heavy":
        return [0, 0, 0, 6, 7, 8]
    if dist == "8_heavy":
        return [0, 8, 8, 8, 6, 7]
    if dist == "6_heavy":
        return [0, 6, 6, 6, 7, 8]
    if dist == "7_heavy":
        return [0, 7, 7, 7, 6, 8]
    return [0, 6, 7, 8]


def _draw_from_degenerate(name, h, w, rng):
    g = full_grid(h, w, 0)
    if name == "no_anchors":
        for r in range(h):
            for c in range(w):
                if rng.random() < 0.4:
                    g[r][c] = rng.choice([6, 7, 8])
        return g
    if name == "all_anchored":
        for r in range(h):
            g[r][0] = 4
            g[r][w - 1] = 4
            for c in range(1, w - 1):
                g[r][c] = rng.choice([0, 6, 7, 8])
        return g
    if name == "single_anchor":
        r = h // 2
        g[r][0] = 4
        g[r][w - 1] = 4
        for c in range(1, w - 1):
            g[r][c] = rng.choice([0, 6, 7, 8])
        return g
    return g
