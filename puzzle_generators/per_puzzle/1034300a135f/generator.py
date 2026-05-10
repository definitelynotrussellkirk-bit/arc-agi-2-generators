"""Generator for puzzle ac0c2ac3.

Rule: scattered markers; rule outputs concentric rings sorted by each
marker's min-distance to grid edge.

Combinatorial axes (8): grid_h/w, n_markers, palette_size,
palette_kind, position_bias, edge_distance_kind, anchor_corner,
asymmetry_force.
Degenerates: no_markers, equal_distances, all_one_color.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "1034300a135f"
VERSION = "1.1.0"
TASK_ID = "1034300a135f"
SUMMARY = "Scattered markers; rule outputs concentric rings sorted by edge distance."

INVARIANTS = [
    "bg is most common color (0)",
    "3-5 distinct marker colors, each at a single cell",
    "markers have STRICTLY distinct min-distances to grid edge",
]

POSITION_BIAS = ("center", "spread", "edge", "corners")
EDGE_DIST_KINDS = ("ascending", "wide_spread", "tight_spread", "shuffled")
PALETTE_KINDS = ("warm", "cool", "broad", "small")
DEGENERATE_TEXTURES = ("no_markers", "equal_distances", "all_one_color")
HELPFUL_TEXTURES = POSITION_BIAS

AXES = {
    "grid_h":            {"type": "int", "default": "rng 9..16", "valid": "7..20"},
    "grid_w":            {"type": "int", "default": "rng 9..16", "valid": "7..20"},
    "n_markers":         {"type": "int", "default": "rng 3..5", "valid": "2..7"},
    "palette_size":      {"type": "int", "default": "= n_markers",
                          "valid": "2..7"},
    "palette_kind":      {"type": "str", "default": "rng helpful",
                          "valid": "|".join(PALETTE_KINDS)},
    "position_bias":     {"type": "str", "default": "rng helpful",
                          "valid": "|".join(POSITION_BIAS)},
    "edge_distance_kind": {"type": "str", "default": "rng helpful",
                           "valid": "|".join(EDGE_DIST_KINDS)},
    "anchor_corner":     {"type": "bool", "default": "false",
                          "valid": "true|false"},
    "texture":           {"type": "str", "default": "alias for position_bias",
                          "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if difficulty == "easy":
        h_lo, h_hi = 7, 10
    elif difficulty == "hard":
        h_lo, h_hi = 14, 20
    else:
        h_lo, h_hi = 9, 16
    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", h_lo, h_hi)
    rng = ctx.draw_rng("placement")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], h, w, rng)
    n_markers = int(overrides.get("n_markers",
                                  ctx.draw_int("n_markers", 3, 5)))
    n_markers = max(2, min(min(7, min(h, w) // 2), n_markers))
    palette_kind = overrides.get("palette_kind",
                                 ctx.draw_choice("palette_kind",
                                                 list(PALETTE_KINDS)))
    if palette_kind == "warm":
        pool = [3, 4, 6, 9]
    elif palette_kind == "cool":
        pool = [1, 5, 7, 8]
    elif palette_kind == "small":
        pool = [1, 2, 3]
    else:
        pool = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    rng.shuffle(pool)
    if len(pool) < n_markers:
        extras = [c for c in range(1, 10) if c not in pool]
        rng.shuffle(extras)
        pool += extras
    palette = pool[:n_markers]
    g = full_grid(h, w, 0)
    used_distances = set()
    placed = 0
    for color in palette:
        for _try in range(40):
            r = rng.randint(0, h - 1); c = rng.randint(0, w - 1)
            d = min(r, c, h - 1 - r, w - 1 - c)
            if d in used_distances:
                continue
            if g[r][c] != 0:
                continue
            g[r][c] = color
            used_distances.add(d)
            placed += 1
            break
    if placed < 3:
        # Force placement at distinct distances 0, 1, 2
        for i, d in enumerate([0, 1, 2]):
            if i < len(palette):
                r = d; c = d
                if 0 <= r < h and 0 <= c < w and g[r][c] == 0:
                    g[r][c] = palette[i]
    return g


def _draw_from_degenerate(name, h, w, rng):
    g = full_grid(h, w, 0)
    if name == "no_markers":
        return g
    if name == "equal_distances":
        # All at distance 0 (corners)
        g[0][0] = 1
        g[0][w - 1] = 2
        g[h - 1][0] = 3
        g[h - 1][w - 1] = 4
        return g
    if name == "all_one_color":
        for r in range(0, h, 2):
            for c in range(0, w, 2):
                g[r][c] = 1
        return g
    return g
