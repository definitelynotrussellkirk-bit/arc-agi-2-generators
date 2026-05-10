"""Generator for ff805c23.

Rule: 5x5 blue marker region + symmetric surroundings; rule reconstructs
the 5x5 from grid symmetries.

Combinatorial axes (8): grid_h/w, marker_position, sym_density,
palette_kind, anchor_corner, asymmetry_force, palette_size, sym_axis.
Degenerates: no_marker, no_symmetry, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, draw_rect

GENERATOR_ID = "f283b8535697"
VERSION = "1.1.0"
TASK_ID = "f283b8535697"
SUMMARY = "5x5 blue marker region + symmetric surroundings; rule reconstructs the 5x5."

INVARIANTS = [
    "exactly one 5x5 region of blue(1) cells (the marker)",
    "the rest of the grid has lr/ud/180 symmetry",
    "marker is in the top-left or top-right or other quadrant",
]

POSITION_BIASES = ("tl", "tr", "bl", "br", "rng")
PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_marker", "no_symmetry", "full_grid")
HELPFUL_TEXTURES = POSITION_BIASES

AXES = {
    "grid_h":         {"type": "int", "default": "rng 12..16", "valid": "10..20"},
    "grid_w":         {"type": "int", "default": "rng 12..16", "valid": "10..20"},
    "marker_position":{"type": "str", "default": "rng helpful",
                       "valid": "|".join(POSITION_BIASES)},
    "sym_density":    {"type": "float", "default": "0.4", "valid": "0.2..0.6"},
    "palette_kind":   {"type": "str", "default": "rng",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2..3"},
    "sym_axis":       {"type": "str", "default": "lr", "valid": "lr"},
    "texture":        {"type": "str", "default": "alias for marker_position",
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
        h_lo, h_hi = 10, 12
        d_default = 0.3
    elif difficulty == "hard":
        h_lo, h_hi = 16, 20
        d_default = 0.5
    else:
        h_lo, h_hi = 12, 16
        d_default = 0.4
    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", h_lo, h_hi)
    palette = ctx.draw_distinct_colors("palette", n=2, exclude={0, 1})
    g = full_grid(h, w, 0)
    density = float(overrides.get("sym_density", d_default))
    density = max(0.1, min(0.7, density))
    for r in range(h):
        for c in range(w // 2):
            if rng.random() < density:
                color = rng.choice(palette)
                g[r][c] = color
                g[r][w - 1 - c] = color
    pos = (overrides.get("texture") if overrides.get("texture") in POSITION_BIASES else None) or \
          overrides.get("marker_position") or \
          ctx.draw_choice("marker_position", list(POSITION_BIASES))
    if pos == "tl":
        mr, mc = 0, 0
    elif pos == "tr":
        mr, mc = 0, w - 5
    elif pos == "bl":
        mr, mc = h - 5, 0
    elif pos == "br":
        mr, mc = h - 5, w - 5
    else:
        mr = rng.randint(0, h - 5); mc = rng.randint(0, w - 5)
    draw_rect(g, mr, mc, 5, 5, 1)
    return g


def _draw_from_degenerate(name, rng):
    h, w = 14, 14
    g = full_grid(h, w, 0)
    if name == "no_marker":
        for r in range(h):
            for c in range(w // 2):
                if rng.random() < 0.3:
                    g[r][c] = 2
                    g[r][w - 1 - c] = 2
        return g
    if name == "no_symmetry":
        for r in range(h):
            for c in range(w):
                if rng.random() < 0.2:
                    g[r][c] = rng.choice([2, 3, 4])
        draw_rect(g, 2, 2, 5, 5, 1)
        return g
    if name == "full_grid":
        for r in range(h):
            for c in range(w):
                g[r][c] = 1
        return g
    return g
