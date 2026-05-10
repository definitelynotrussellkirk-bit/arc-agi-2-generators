"""Generator for arc_additional_puzzle_bank_volume8:H56 — orange shapes match legend glyphs.

Rule: a gray divider separates legend glyphs (colors 2/3/4) above and
orange-7 scene shapes below. Each scene shape is recolored to the
legend glyph it matches up to rotation.

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: no_legend, no_scene, no_divider.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, paint_at

GENERATOR_ID = "fd745e4aa1ad"
VERSION = "1.1.0"
TASK_ID = "fd745e4aa1ad"
SUMMARY = "Orange scene objects below a gray divider are recolored by matching their shape to rotated legend glyphs."

INVARIANTS = [
    "a full gray divider separates legend and scene",
    "legend glyphs use colors 2, 3, and 4",
    "scene objects are color 7",
    "each scene object matches one legend shape up to rotation",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_legend", "no_scene", "no_divider")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 13..16", "valid": "13..20"},
    "grid_w":         {"type": "int", "default": "rng 14..18", "valid": "14..22"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "palette_size":   {"type": "int", "default": "5", "valid": "5..5"},
    "position_bias":  {"type": "str", "default": "legend_top_scene_below",
                       "valid": "legend_top_scene_below"},
    "n_distinct_colors": {"type": "int", "default": "5", "valid": "5..5"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def _norm(cells: list[tuple[int, int]]) -> list[tuple[int, int]]:
    min_r = min(r for r, _ in cells)
    min_c = min(c for _, c in cells)
    return sorted((r - min_r, c - min_c) for r, c in cells)


def _rot(cells: list[tuple[int, int]], turns: int) -> list[tuple[int, int]]:
    cur = _norm(cells)
    for _ in range(turns % 4):
        height = max(r for r, _ in cur) + 1
        cur = _norm([(c, height - 1 - r) for r, c in cur])
    return cur


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 13, 13)
        w = ctx.draw_int("grid_w", 14, 15)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 16, 19)
        w = ctx.draw_int("grid_w", 18, 21)
    else:
        h = ctx.draw_int("grid_h", 13, 16)
        w = ctx.draw_int("grid_w", 14, 18)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    glyph2 = [(0, 0), (1, 0), (2, 0), (2, 1)]
    glyph3 = [(1, 0), (1, 1), (1, 2), (0, 1)]
    glyph4 = [(0, 0), (1, 0), (2, 0), (2, 1), (2, 2)]
    paint_at(g, 1, 1, glyph2, 2)
    paint_at(g, 1, 5, glyph3, 3)
    paint_at(g, 1, 9, glyph4, 4)
    for c in range(w):
        g[4][c] = 5
    paint_at(g, 6, 1 + rng.randint(0, 1), _rot(glyph3, rng.randint(0, 3)), 7)
    paint_at(g, 7, max(6, w // 2), _rot(glyph2, rng.randint(0, 3)), 7)
    paint_at(g, h - 4, w - 4, _rot(glyph4, rng.randint(0, 3)), 7)
    return g


def _draw_from_degenerate(name, rng):
    h, w = 14, 16
    g = full_grid(h, w, 0)
    glyph2 = [(0, 0), (1, 0), (2, 0), (2, 1)]
    glyph3 = [(1, 0), (1, 1), (1, 2), (0, 1)]
    glyph4 = [(0, 0), (1, 0), (2, 0), (2, 1), (2, 2)]
    if name == "no_legend":
        # Scene shapes present but no legend glyphs — rule has no
        # color mapping to apply.
        for c in range(w):
            g[4][c] = 5
        paint_at(g, 6, 2, glyph2, 7)
        paint_at(g, 9, 8, glyph4, 7)
        return g
    if name == "no_scene":
        # Legend present but no orange scene shapes — rule has nothing
        # to recolor.
        paint_at(g, 1, 1, glyph2, 2)
        paint_at(g, 1, 5, glyph3, 3)
        paint_at(g, 1, 9, glyph4, 4)
        for c in range(w):
            g[4][c] = 5
        return g
    if name == "no_divider":
        # Legend + scene but no gray divider — legend/scene boundary
        # undefined, rule has no separator to ground its match logic.
        paint_at(g, 1, 1, glyph2, 2)
        paint_at(g, 1, 5, glyph3, 3)
        paint_at(g, 1, 9, glyph4, 4)
        paint_at(g, 6, 2, glyph2, 7)
        return g
    return g
