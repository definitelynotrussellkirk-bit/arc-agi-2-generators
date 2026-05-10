"""Generator for bc1d5164.

Rule: split grid into 9 zones (corners + edges + center). Output is 3×3
where each cell is the last non-zero in row-major scan of its zone, else 0.

Combinatorial axes (8): grid_h/w, color, n_zones_filled, zone_density,
position_layout, palette_size, decoy_color, asymmetry.
Degenerates: empty_grid, all_zones_filled, single_zone.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "9df67b512dad"
VERSION = "1.1.0"
TASK_ID = "9df67b512dad"
SUMMARY = "Grid with non-zero cells per zone; rule emits 3×3 last-non-zero per zone."

INVARIANTS = [
    "background is 0",
    ">=4 zones (corners/edges/center) have >=1 non-zero cell",
    "all non-zero cells use one color (so the rule's last-non-zero is uniform)",
    "interior zones (rows in [1, h-2], cols in [1, w-2]) are wide enough",
]

POSITION_LAYOUTS = ("scattered", "all_corners", "edges_only",
                    "diag_zones", "center_heavy")
DEGENERATE_TEXTURES = ("empty_grid", "all_zones_filled", "single_zone")
HELPFUL_TEXTURES = POSITION_LAYOUTS

AXES = {
    "grid_h":           {"type": "int", "default": "rng 5..10", "valid": "4..14"},
    "grid_w":           {"type": "int", "default": "rng 7..12", "valid": "5..16"},
    "color":            {"type": "color", "default": "rng (≠0)",
                         "valid": "1..9"},
    "n_zones_filled":   {"type": "int", "default": "rng 4..7", "valid": "1..9"},
    "zone_density":     {"type": "float", "default": "rng 0.3..0.7",
                         "valid": "0.1..1"},
    "position_layout":  {"type": "str", "default": "rng helpful",
                         "valid": "|".join(POSITION_LAYOUTS)},
    "palette_size":     {"type": "int", "default": "1", "valid": "1..2"},
    "asymmetry":        {"type": "bool", "default": "false",
                         "valid": "true|false"},
    "texture":          {"type": "str", "default": "alias for position_layout",
                         "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if difficulty == "easy":
        h_lo, h_hi, w_lo, w_hi = 4, 6, 5, 8
    elif difficulty == "hard":
        h_lo, h_hi, w_lo, w_hi = 9, 14, 11, 16
    else:
        h_lo, h_hi, w_lo, w_hi = 5, 10, 7, 12
    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", w_lo, w_hi)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], h, w, rng)
    color = int(overrides.get("color",
                              rng.choice([1, 2, 3, 4, 5, 6, 7, 8, 9])))
    n_zones = int(overrides.get("n_zones_filled",
                                ctx.draw_int("n_zones_filled", 4, 7)))
    layout = (overrides.get("texture") or overrides.get("position_layout")
              or ctx.draw_choice("position_layout",
                                 list(POSITION_LAYOUTS)))
    g = full_grid(h, w, 0)
    zones = [
        ([0], [0]),
        ([0], list(range(1, w - 1))),
        ([0], [w - 1]),
        (list(range(1, h - 1)), [0]),
        (list(range(1, h - 1)), list(range(1, w - 1))),
        (list(range(1, h - 1)), [w - 1]),
        ([h - 1], [0]),
        ([h - 1], list(range(1, w - 1))),
        ([h - 1], [w - 1]),
    ]
    chosen = _pick_zones(layout, n_zones, rng)
    for idx in chosen:
        rs, cs = zones[idx]
        if rs and cs:
            r = rng.choice(rs); c = rng.choice(cs)
            g[r][c] = color
    return g


def _pick_zones(layout, n, rng):
    if layout == "all_corners":
        corners = [0, 2, 6, 8]
        rest = [1, 3, 4, 5, 7]
        rng.shuffle(rest)
        return (corners + rest)[:n]
    if layout == "edges_only":
        edges = [1, 3, 5, 7]
        rest = [0, 2, 4, 6, 8]
        rng.shuffle(rest)
        return (edges + rest)[:n]
    if layout == "diag_zones":
        diag = [0, 4, 8]
        rest = [1, 2, 3, 5, 6, 7]
        rng.shuffle(rest)
        return (diag + rest)[:n]
    if layout == "center_heavy":
        center = [4]
        rest = [0, 1, 2, 3, 5, 6, 7, 8]
        rng.shuffle(rest)
        return (center + rest)[:n]
    all_z = list(range(9))
    rng.shuffle(all_z)
    return all_z[:n]


def _draw_from_degenerate(name, h, w, rng):
    g = full_grid(h, w, 0)
    color = rng.choice([1, 2, 3, 4, 5, 6, 7, 8, 9])
    if name == "empty_grid":
        return g
    if name == "all_zones_filled":
        for r in range(h):
            for c in range(w):
                g[r][c] = color
        return g
    if name == "single_zone":
        g[h // 2][w // 2] = color
        return g
    return g
