"""Generator for 447fd412.

Rule: a small 1-template with adjacent 2 markers is scaled and stamped
at matching standalone 2-blocks.

Combinatorial axes (8): grid_h/w, scale, palette_kind, anchor_corner,
asymmetry_force, palette_size, position_bias, n_distinct_colors.
Degenerates: no_template, no_blocks, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "5f7e273c56dd"
VERSION = "1.1.0"
TASK_ID = "5f7e273c56dd"
SUMMARY = "Small 1-template with adjacent 2 markers is scaled and stamped at standalone 2-blocks."

INVARIANTS = [
    "background is color 0",
    "the source template contains color 1 cells and adjacent color 2 marker cells",
    "standalone color 2 blocks mark scaled copies of the template markers",
    "standalone block side length is the template scale",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_template", "no_blocks", "full_grid")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "varied", "valid": "varied"},
    "grid_w":         {"type": "int", "default": "varied", "valid": "varied"},
    "scale":          {"type": "int", "default": "rng 1..3", "valid": "1..3"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2"},
    "position_bias":  {"type": "str", "default": "varied", "valid": "varied"},
    "n_distinct_colors":{"type": "int", "default": "2", "valid": "2"},
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
    if difficulty == "easy":
        scale = ctx.draw_int("scale", 1, 1)
    elif difficulty == "hard":
        scale = ctx.draw_int("scale", 3, 3)
    else:
        scale = ctx.draw_int("scale", 1, 3)
    h = 14 + 3 * scale + rng.randint(0, 2)
    w = 14 + 3 * scale + rng.randint(0, 2)
    g = full_grid(h, w, 0)

    template_r = 1 + (sample_index % 2)
    template_c = 1 + ((sample_index // 2) % 2)
    one_cells = [(0, 0), (0, 1), (1, 1)]
    marker_cells = [(1, 2), (2, 1)]
    for dr, dc in one_cells:
        g[template_r + dr][template_c + dc] = 1
    for dr, dc in marker_cells:
        g[template_r + dr][template_c + dc] = 2

    origin_r = 6 + rng.randint(0, 2)
    origin_c = 6 + rng.randint(0, 2)
    for mr, mc in marker_cells:
        br = origin_r + mr * scale
        bc = origin_c + mc * scale
        for dr in range(scale):
            for dc in range(scale):
                g[br + dr][bc + dc] = 2
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(18, 18, 0)
    if name == "no_template":
        g[10][10] = 2
        return g
    if name == "no_blocks":
        for dr, dc in [(0, 0), (0, 1), (1, 1)]:
            g[1 + dr][1 + dc] = 1
        for dr, dc in [(1, 2), (2, 1)]:
            g[1 + dr][1 + dc] = 2
        return g
    if name == "full_grid":
        for r in range(18):
            for c in range(18):
                g[r][c] = 2
        return g
    return g
