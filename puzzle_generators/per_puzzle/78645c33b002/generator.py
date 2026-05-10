"""Generator for eb5a1d5d.

Rule: nested concentric rectangles; rule outputs square pattern colored
by layer index.

Combinatorial axes (8): grid_h/w, n_layers, palette_kind, position_bias,
margin_factor, anchor_corner, asymmetry_force, palette_size.
Degenerates: solid_block, single_layer, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, draw_rect

GENERATOR_ID = "78645c33b002"
VERSION = "1.1.0"
TASK_ID = "78645c33b002"
SUMMARY = "Nested concentric rectangles; rule outputs square pattern colored by layer index."

INVARIANTS = [
    "input has K (>=2) nested concentric solid rectangles",
    "each layer is one uniform color",
    "outermost color is at (0, 0)",
    "innermost rectangle has no inner cells",
]

POSITION_BIASES = ("centered", "off_center", "tight", "rng")
PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("solid_block", "single_layer", "full_grid")
HELPFUL_TEXTURES = POSITION_BIASES

AXES = {
    "grid_h":         {"type": "int", "default": "rng 11..15", "valid": "9..18"},
    "grid_w":         {"type": "int", "default": "rng 11..15", "valid": "9..18"},
    "n_layers":       {"type": "int", "default": "rng 2..4", "valid": "2..6"},
    "palette_kind":   {"type": "str", "default": "rng",
                       "valid": "|".join(PALETTE_KINDS)},
    "position_bias":  {"type": "str", "default": "rng helpful",
                       "valid": "|".join(POSITION_BIASES)},
    "margin_factor":  {"type": "int", "default": "4", "valid": "2..6"},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "rng 2..4", "valid": "2..6"},
    "texture":        {"type": "str", "default": "alias for position_bias",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    rng = ctx.draw_rng("placement")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], rng)
    if difficulty == "easy":
        h_lo, h_hi = 9, 11
        nl_lo, nl_hi = 2, 2
    elif difficulty == "hard":
        h_lo, h_hi = 15, 18
        nl_lo, nl_hi = 4, 6
    else:
        h_lo, h_hi = 11, 15
        nl_lo, nl_hi = 2, 4
    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", h_lo, h_hi)
    n_layers = int(overrides.get("n_layers",
                                 ctx.draw_int("n_layers", nl_lo, nl_hi)))
    n_layers = max(2, min(6, n_layers))
    palette_kind = overrides.get("palette_kind",
                                 ctx.draw_choice("palette_kind",
                                                 list(PALETTE_KINDS)))
    palette = _build_palette(palette_kind, n_layers, rng)
    margin_factor = int(overrides.get("margin_factor", 4))
    margin_factor = max(2, min(6, margin_factor))
    g = full_grid(h, w, palette[0])
    r1, c1, r2, c2 = 0, 0, h - 1, w - 1
    for layer in range(1, n_layers):
        if (r2 - r1) < 4 or (c2 - c1) < 4:
            break
        dr = rng.randint(1, max(1, (r2 - r1) // margin_factor))
        dc = rng.randint(1, max(1, (c2 - c1) // margin_factor))
        r1 += dr
        c1 += dc
        r2 -= rng.randint(1, max(1, (r2 - r1) // margin_factor))
        c2 -= rng.randint(1, max(1, (c2 - c1) // margin_factor))
        if r2 <= r1 or c2 <= c1:
            break
        draw_rect(g, r1, c1, r2 - r1 + 1, c2 - c1 + 1, palette[layer])
    return g


def _build_palette(kind, n, rng):
    if kind == "warm":
        pool = [2, 3, 4, 6, 9]
    elif kind == "cool":
        pool = [1, 5, 7, 8]
    elif kind == "primary":
        pool = [1, 2, 3, 4]
    else:
        pool = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    rng.shuffle(pool)
    if len(pool) < n:
        for c in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]:
            if c not in pool:
                pool.append(c)
            if len(pool) >= n:
                break
    return pool[:n]


def _draw_from_degenerate(name, rng):
    h, w = 12, 12
    g = full_grid(h, w, 2)
    if name == "solid_block":
        return g
    if name == "single_layer":
        draw_rect(g, 3, 3, 6, 6, 4)
        return g
    if name == "full_grid":
        for r in range(h):
            for c in range(w):
                g[r][c] = 4
        return g
    return g
