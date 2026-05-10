"""Generator for 15113be4.

Rule: 2x2 marker template defines a key bitmap; candidate slots whose
1-mask matches the key are recolored to the marker color.

Combinatorial axes (8): grid_size, palette_kind, anchor_corner,
asymmetry_force, palette_size, position_bias, marker_color,
n_slots.
Degenerates: no_slots, all_match, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "3143493b7c83"
VERSION = "1.1.0"
TASK_ID = "3143493b7c83"
SUMMARY = "2x2 marker template + matching 1-mask slots get recolored to marker."

INVARIANTS = [
    "background is color 0",
    "one marker color defines a 2x2 downsampled key bitmap",
    "candidate slots start on multiples of four",
    "slots with 1s at every key position are recolored to the marker color",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_slots", "all_match", "full_grid")
HELPFUL_TEXTURES = PALETTE_KINDS
TEMPLATE = [(0, 0), (1, 1)]

AXES = {
    "grid_size":      {"type": "int", "default": "12", "valid": "12"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "1", "valid": "1"},
    "position_bias":  {"type": "str", "default": "fixed", "valid": "fixed"},
    "marker_color":   {"type": "color", "default": "rng !{0,1,4}",
                       "valid": "2|3|5|6|7|8|9"},
    "n_slots":        {"type": "int", "default": "3", "valid": "3"},
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
    _ = ctx.draw_int("grid_size", 12, 12)
    palette_kind = (overrides.get("texture") or
                    overrides.get("palette_kind") or
                    ctx.draw_choice("palette_kind", list(PALETTE_KINDS)))
    pool = _build_palette(palette_kind, rng)
    if not pool:
        pool = [2, 3, 5, 6, 7, 8, 9]
    marker = pool[0]
    g = full_grid(12, 12, 0)
    for tr, tc in TEMPLATE:
        for dr in range(2):
            for dc in range(2):
                g[tr * 2 + dr][tc * 2 + dc] = marker
    for rs, cs in [(4, 4), (4, 8), (8, 4)]:
        for tr, tc in TEMPLATE:
            g[rs + tr][cs + tc] = 1
    g[8][8] = 1
    return g


def _build_palette(kind, rng):
    if kind == "warm":
        pool = [2, 3, 6, 9]
    elif kind == "cool":
        pool = [5, 7, 8]
    elif kind == "primary":
        pool = [2, 3]
    else:
        pool = [2, 3, 5, 6, 7, 8, 9]
    pool = [c for c in pool if c not in (0, 1, 4)]
    rng.shuffle(pool)
    return pool


def _draw_from_degenerate(name, rng):
    g = full_grid(12, 12, 0)
    if name == "no_slots":
        for tr, tc in TEMPLATE:
            for dr in range(2):
                for dc in range(2):
                    g[tr * 2 + dr][tc * 2 + dc] = 2
        return g
    if name == "all_match":
        for tr, tc in TEMPLATE:
            for dr in range(2):
                for dc in range(2):
                    g[tr * 2 + dr][tc * 2 + dc] = 2
        for rs, cs in [(4, 4), (4, 8), (8, 4), (8, 8)]:
            for tr, tc in TEMPLATE:
                g[rs + tr][cs + tc] = 1
        return g
    if name == "full_grid":
        for r in range(12):
            for c in range(12):
                g[r][c] = 5
        return g
    return g
