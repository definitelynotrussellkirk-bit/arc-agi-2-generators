"""Generator for 1187a52b.

Rule: separator rows + cols define tile size; collect cells across
all tiles and output the tile with 1 where tiles disagree.

Combinatorial axes (8): grid_size, palette_kind, anchor_corner,
asymmetry_force, palette_size, position_bias, n_copies, n_mut.
Degenerates: no_mutations, full_mutations, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "9bfbec04496c"
VERSION = "1.1.0"
TASK_ID = "9bfbec04496c"
SUMMARY = "2x2 tile repeated 3x3 separated by sep-color rows/cols; some cells mutated."

INVARIANTS = [
    "tile size 2x2",
    "three horizontal copies separated by sep-color cols",
    "three vertical copies separated by sep-color rows",
    "one or two mutated cells in the copies so the output has 1s",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_mutations", "full_mutations", "full_grid")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_size":      {"type": "int", "default": "8", "valid": "8"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "rng 4..8", "valid": "2..9"},
    "position_bias":  {"type": "str", "default": "fixed", "valid": "fixed"},
    "n_copies":       {"type": "int", "default": "3", "valid": "3"},
    "n_mut":          {"type": "int", "default": "rng 1..2", "valid": "1..3"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], rng)
    tile_h = 2; tile_w = 2
    n_copies = 3
    h = n_copies * (tile_h + 1) - 1
    w = n_copies * (tile_w + 1) - 1
    palette_kind = (overrides.get("texture") or
                    overrides.get("palette_kind") or
                    ctx.draw_choice("palette_kind", list(PALETTE_KINDS)))
    pool = _build_palette(palette_kind, rng)
    if len(pool) < 2:
        pool = pool + [c for c in [1, 2, 3, 4, 6, 7, 8, 9] if c not in pool]
    sep_color = pool[0]
    palette = [v for v in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9] if v != sep_color]
    base_tile = [[rng.choice(palette) for _ in range(tile_w)] for _ in range(tile_h)]
    g = full_grid(h, w, 0)
    for br in range(n_copies):
        for bc in range(n_copies):
            r_off = br * (tile_h + 1)
            c_off = bc * (tile_w + 1)
            for r in range(tile_h):
                for c in range(tile_w):
                    g[r_off + r][c_off + c] = base_tile[r][c]
            if bc < n_copies - 1:
                for r in range(tile_h):
                    g[r_off + r][c_off + tile_w] = sep_color
        if br < n_copies - 1:
            for c in range(w):
                g[br * (tile_h + 1) + tile_h][c] = sep_color
    n_mut = rng.randint(1, 2)
    for _ in range(n_mut):
        for _ in range(40):
            br = rng.randint(0, n_copies - 1)
            bc = rng.randint(0, n_copies - 1)
            r = rng.randint(0, tile_h - 1)
            c = rng.randint(0, tile_w - 1)
            r_off = br * (tile_h + 1)
            c_off = bc * (tile_w + 1)
            old = g[r_off + r][c_off + c]
            new_val = rng.choice([v for v in palette if v != old])
            g[r_off + r][c_off + c] = new_val
            break
    return g


def _build_palette(kind, rng):
    if kind == "warm":
        pool = [2, 3, 4, 6, 9]
    elif kind == "cool":
        pool = [1, 5, 7, 8]
    elif kind == "primary":
        pool = [1, 2, 3, 4]
    else:
        pool = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    pool = [c for c in pool if c != 0]
    rng.shuffle(pool)
    return pool


def _draw_from_degenerate(name, rng):
    h = w = 8
    g = full_grid(h, w, 0)
    sep = 5
    for br in range(3):
        for bc in range(3):
            r_off = br * 3; c_off = bc * 3
            for r in range(2):
                for c in range(2):
                    g[r_off + r][c_off + c] = 2
            if bc < 2:
                for r in range(2):
                    g[r_off + r][c_off + 2] = sep
        if br < 2:
            for c in range(w):
                g[br * 3 + 2][c] = sep
    if name == "no_mutations":
        return g
    if name == "full_mutations":
        for br in range(3):
            for bc in range(3):
                r_off = br * 3; c_off = bc * 3
                g[r_off][c_off] = 1
        return g
    if name == "full_grid":
        for r in range(h):
            for c in range(w):
                g[r][c] = sep
        return g
    return g
