"""Generator for 1c56ad9f.

Rule: nonempty rows shifted by 0,-1,0,1 wave anchored at last nonempty
row.

Combinatorial axes (8): grid_h/w, n_rows, n_cells_per_row,
palette_size, palette_kind, position_bias, anchor_corner,
asymmetry_force.
Degenerates: no_rows, single_row, all_rows.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "8a3fe170ed27"
VERSION = "1.1.0"
TASK_ID = "8a3fe170ed27"
SUMMARY = "Nonempty rows shifted by 0,-1,0,1 wave anchored at last row."

INVARIANTS = [
    "several rows contain colored cells on bg=0",
    "last nonempty row is the phase anchor",
    "rows above follow 0,-1,0,1 shift cycle",
    "at least one shifted row has room to move (cols >=2 from edge)",
]

POSITION_BIAS = ("center", "spread", "edge")
PALETTE_KINDS = ("warm", "cool", "broad", "small")
DEGENERATE_TEXTURES = ("no_rows", "single_row", "all_rows")
HELPFUL_TEXTURES = POSITION_BIAS

AXES = {
    "grid_h":           {"type": "int", "default": "rng 8..14", "valid": "5..20"},
    "grid_w":           {"type": "int", "default": "rng 8..14", "valid": "5..20"},
    "n_rows":           {"type": "int", "default": "rng 4..6", "valid": "2..8"},
    "n_cells_per_row":  {"type": "int", "default": "rng 2..4", "valid": "1..6"},
    "palette_size":     {"type": "int", "default": "rng 3..5", "valid": "1..7"},
    "palette_kind":     {"type": "str", "default": "rng helpful",
                         "valid": "|".join(PALETTE_KINDS)},
    "position_bias":    {"type": "str", "default": "rng helpful",
                         "valid": "|".join(POSITION_BIAS)},
    "anchor_corner":    {"type": "bool", "default": "false",
                         "valid": "true|false"},
    "texture":          {"type": "str", "default": "alias for position_bias",
                         "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if difficulty == "easy":
        h_lo, h_hi = 5, 8
    elif difficulty == "hard":
        h_lo, h_hi = 13, 20
    else:
        h_lo, h_hi = 8, 14
    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", h_lo, h_hi)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], h, w, rng)
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
    n_palette = int(overrides.get("palette_size",
                                  ctx.draw_int("palette_size", 3, 5)))
    palette = pool[:max(1, n_palette)]
    n_rows = int(overrides.get("n_rows",
                               ctx.draw_int("n_rows", 4, min(6, h - 2))))
    n_rows = max(2, min(min(8, h - 2), n_rows))
    n_cells = int(overrides.get("n_cells_per_row",
                                ctx.draw_int("n_cells_per_row", 2,
                                             min(4, w - 4))))
    n_cells = max(1, min(min(6, w - 4), n_cells))
    bias = (overrides.get("texture") or
            overrides.get("position_bias")
            or ctx.draw_choice("position_bias", list(POSITION_BIAS)))
    g = full_grid(h, w, 0)
    rows = _pick_rows(bias, h, n_rows, rng)
    for i, r in enumerate(rows):
        cols = _pick_cols(bias, w, n_cells, rng)
        for c in cols:
            g[r][c] = palette[i % len(palette)]
    return g


def _pick_rows(bias, h, n, rng):
    avail = list(range(1, h - 1))
    if bias == "center":
        center = h // 2
        avail.sort(key=lambda r: abs(r - center))
        return sorted(avail[:n])
    if bias == "edge":
        avail.sort(key=lambda r: -min(r, h - 1 - r))
        return sorted(avail[:n])
    return sorted(rng.sample(avail, min(n, len(avail))))


def _pick_cols(bias, w, n, rng):
    avail = list(range(2, w - 2))
    if not avail:
        return [w // 2]
    if bias == "center":
        center = w // 2
        avail.sort(key=lambda c: abs(c - center))
        return avail[:n]
    if bias == "edge":
        avail.sort(key=lambda c: -min(c - 2, w - 3 - c))
        return avail[:n]
    return rng.sample(avail, min(n, len(avail)))


def _draw_from_degenerate(name, h, w, rng):
    g = full_grid(h, w, 0)
    color = rng.choice([1, 2, 3, 4, 5, 6, 7, 8, 9])
    if name == "no_rows":
        return g
    if name == "single_row":
        for c in range(2, w - 2):
            g[h // 2][c] = color
        return g
    if name == "all_rows":
        for r in range(h):
            g[r][w // 2] = color
        return g
    return g
