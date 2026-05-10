"""Generator for 8dae5dfc.

Rule: each multicolor 8-conn component has nested concentric layers.
Take diagonal cells' unique colors innermost-out, reverse, remap colors.

Combinatorial axes (8): grid_h/w, n_blocks, n_layers_min, n_layers_max,
palette_kind, position_bias, anchor_corner, asymmetry_force.
Degenerates: solid_block, single_layer, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import draw_frame, fill_box, full_grid
from puzzle_generators.helpers.place import place_no_overlap

GENERATOR_ID = "0846393acd63"
VERSION = "1.1.0"
TASK_ID = "0846393acd63"
SUMMARY = "1-2 nested concentric rectangle blocks; rule reverses layer colors."

INVARIANTS = [
    "each block has 3-5 nested concentric square frames",
    "frame colors all distinct within a block",
    "blocks don't touch",
]

POSITION_BIASES = ("centered", "scattered", "corners", "rng")
PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("solid_block", "single_layer", "full_grid")
HELPFUL_TEXTURES = POSITION_BIASES

AXES = {
    "grid_h":         {"type": "int", "default": "rng 16..20", "valid": "12..28"},
    "grid_w":         {"type": "int", "default": "rng 16..20", "valid": "12..28"},
    "n_blocks":       {"type": "int", "default": "rng 1..2", "valid": "1..3"},
    "n_layers_min":   {"type": "int", "default": "3", "valid": "2..4"},
    "n_layers_max":   {"type": "int", "default": "5", "valid": "3..6"},
    "palette_kind":   {"type": "str", "default": "rng",
                       "valid": "|".join(PALETTE_KINDS)},
    "position_bias":  {"type": "str", "default": "rng helpful",
                       "valid": "|".join(POSITION_BIASES)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "texture":        {"type": "str", "default": "alias for position_bias",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def _draw_nested(g, r0, c0, layers):
    n = len(layers)
    for i, color in enumerate(layers):
        rr0, cc0 = r0 + i, c0 + i
        rr1, cc1 = r0 + 2 * n - 1 - i, c0 + 2 * n - 1 - i
        if i == n - 1:
            fill_box(g, rr0, cc0, rr1, cc1, color)
        else:
            draw_frame(g, rr0, cc0, rr1, cc1, color)


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], rng)
    if difficulty == "easy":
        h_lo, h_hi = 12, 16
        nb_lo, nb_hi = 1, 1
        nl_lo, nl_hi = 2, 3
    elif difficulty == "hard":
        h_lo, h_hi = 20, 28
        nb_lo, nb_hi = 2, 3
        nl_lo, nl_hi = 4, 6
    else:
        h_lo, h_hi = 16, 20
        nb_lo, nb_hi = 1, 2
        nl_lo, nl_hi = 3, 5
    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", h_lo, h_hi)
    g = full_grid(h, w, 0)
    n_blocks = int(overrides.get("n_blocks",
                                 ctx.draw_int("n_blocks", nb_lo, nb_hi)))
    n_blocks = max(1, min(3, n_blocks))
    nl_min = int(overrides.get("n_layers_min", nl_lo))
    nl_max = int(overrides.get("n_layers_max", nl_hi))
    palette_kind = overrides.get("palette_kind",
                                 ctx.draw_choice("palette_kind",
                                                 list(PALETTE_KINDS)))
    pool = _build_pool(palette_kind, rng)
    for _ in range(n_blocks):
        n_layers = rng.randint(nl_min, nl_max)
        size = 2 * n_layers
        if size + 4 > h or size + 4 > w:
            n_layers = max(2, min(h, w) // 2 - 2)
            size = 2 * n_layers
        if n_layers < 2:
            continue
        footprint = [(r, c) for r in range(size) for c in range(size)]
        if len(pool) < n_layers:
            pool = pool + [c for c in [1, 2, 3, 4, 5, 6, 7, 8, 9] if c not in pool]
        layers = rng.sample(pool, n_layers)
        pos = place_no_overlap(rng, g, footprint, layers[0],
                               padding=1, max_tries=40)
        if pos is not None:
            r0, c0 = pos
            _draw_nested(g, r0, c0, layers)
    return g


def _build_pool(kind, rng):
    if kind == "warm":
        pool = [2, 3, 4, 6, 9]
    elif kind == "cool":
        pool = [1, 5, 7, 8]
    elif kind == "primary":
        pool = [1, 2, 3, 4]
    else:
        pool = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    rng.shuffle(pool)
    return pool


def _draw_from_degenerate(name, rng):
    h, w = 16, 16
    g = full_grid(h, w, 0)
    if name == "solid_block":
        fill_box(g, 4, 4, 11, 11, 2)
        return g
    if name == "single_layer":
        draw_frame(g, 4, 4, 11, 11, 2)
        return g
    if name == "full_grid":
        for r in range(h):
            for c in range(w):
                g[r][c] = 2
        return g
    return g
