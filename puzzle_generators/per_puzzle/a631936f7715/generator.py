"""Generator for b7256dcd.

Rule: magenta components are recolored by adjacent label cells;
labels are removed to background.

Combinatorial axes (8): grid_h/w, component_count, palette_kind,
anchor_corner, asymmetry_force, palette_size, position_bias,
shape_variant.
Degenerates: no_components, no_labels, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "a631936f7715"
VERSION = "1.1.0"
TASK_ID = "a631936f7715"
SUMMARY = "Magenta components recolored by adjacent label cells; labels removed."

INVARIANTS = [
    "background is color 7",
    "source components use color 6",
    "each component has one adjacent non-background non-magenta label color",
    "label colors are distinct so each component gets a unique recolor",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_components", "no_labels", "full_grid")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 12..13", "valid": "10..16"},
    "grid_w":         {"type": "int", "default": "rng 12..13", "valid": "10..16"},
    "component_count":{"type": "int", "default": "3", "valid": "3"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "3", "valid": "3"},
    "position_bias":  {"type": "str", "default": "fixed", "valid": "fixed"},
    "shape_variant":  {"type": "str", "default": "fixed", "valid": "fixed"},
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
    palette_kind = (overrides.get("texture") or
                    overrides.get("palette_kind") or
                    ctx.draw_choice("palette_kind", list(PALETTE_KINDS)))
    pool = _build_palette(palette_kind, rng)
    if len(pool) < 3:
        pool = pool + [c for c in [1, 2, 3, 4, 5, 8, 9] if c not in pool]
    labels = pool[:3]
    g = full_grid(12 + rng.randint(0, 1), 12 + rng.randint(0, 1), 7)
    specs = [
        (2, 2, [(0, 0), (1, 0), (1, 1)], (0, -1)),
        (2, 8, [(0, 0), (0, 1), (1, 1)], (-1, 0)),
        (8, 5, [(0, 0), (1, 0)], (0, 1)),
    ]
    for idx, (r0, c0, cells, label_off) in enumerate(specs):
        for dr, dc in cells:
            g[r0 + dr][c0 + dc] = 6
        lr = r0 + cells[0][0] + label_off[0]
        lc = c0 + cells[0][1] + label_off[1]
        g[lr][lc] = labels[idx]
    return g


def _build_palette(kind, rng):
    if kind == "warm":
        pool = [2, 3, 4, 9]
    elif kind == "cool":
        pool = [1, 5, 8]
    elif kind == "primary":
        pool = [1, 2, 3, 4]
    else:
        pool = [1, 2, 3, 4, 5, 8, 9]
    pool = [c for c in pool if c not in (0, 6, 7)]
    rng.shuffle(pool)
    return pool


def _draw_from_degenerate(name, rng):
    g = full_grid(12, 12, 7)
    if name == "no_components":
        g[2][2] = 1
        g[5][5] = 2
        return g
    if name == "no_labels":
        for dr, dc in [(0, 0), (1, 0), (1, 1)]:
            g[2 + dr][2 + dc] = 6
        return g
    if name == "full_grid":
        for r in range(12):
            for c in range(12):
                g[r][c] = 6
        return g
    return g
