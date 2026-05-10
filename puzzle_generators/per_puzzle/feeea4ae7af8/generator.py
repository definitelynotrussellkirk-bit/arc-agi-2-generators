"""Generator for arc_additional_puzzles_21_set17_bundle:M117 — pick object by cmd at (0,0).

Rule: cell (0,0) holds a command; the rest of the grid has objects.
Pick one object per command:
  1: smallest size; 2: largest size; 3: widest bbox; 4: tallest bbox
Output is the bbox crop of the chosen object.

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: no_command (cell (0,0) is bg → rule has no command);
no_objects (command set but no objects → selector has no
candidates); tied_dimensions (two objects share size, height, and
width → selector ambiguous for some commands).
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, paint_at
from puzzle_generators.helpers.palette import random_palette
from puzzle_generators.helpers.blobs import bbox_overlaps

GENERATOR_ID = "feeea4ae7af8"
VERSION = "1.1.0"
TASK_ID = "feeea4ae7af8"
SUMMARY = "Cmd at (0,0) plus 2-3 distinct shapes with distinct size/height/width."

INVARIANTS = [
    "background is 0",
    "(0,0) holds a command in {1, 2, 3, 4}",
    "2-3 4-connected non-bg objects with distinct (size, bbox_h, bbox_w) tuples",
    "objects don't touch each other or (0,0)",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_command", "no_objects", "tied_dimensions")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":            {"type": "int", "default": "rng 9..12", "valid": "8..14"},
    "grid_w":            {"type": "int", "default": "rng 12..14", "valid": "10..18"},
    "palette_kind":      {"type": "str", "default": "rng helpful",
                          "valid": "|".join(PALETTE_KINDS)},
    "palette_size":      {"type": "int", "default": "rng 4..4", "valid": "4..4"},
    "position_bias":     {"type": "str", "default": "cmd_at_origin_with_objects",
                          "valid": "cmd_at_origin_with_objects"},
    "n_distinct_colors": {"type": "int", "default": "rng 4..4", "valid": "4..4"},
    "density":           {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":           {"type": "str", "default": "alias for palette_kind",
                          "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}

_SHAPES = [
    ([(0, 0), (0, 1), (1, 0), (1, 1)], 4, 2, 2),
    ([(0, 0), (0, 1), (0, 2), (0, 3), (0, 4)], 5, 1, 5),
    ([(0, 0), (1, 0), (2, 0), (3, 0)], 4, 4, 1),
    ([(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2), (2, 0), (2, 1), (2, 2)], 9, 3, 3),
    ([(0, 0), (0, 1), (0, 2), (1, 1)], 4, 2, 3),
    ([(0, 0), (1, 0), (1, 1), (2, 0), (2, 1), (3, 1)], 6, 4, 2),
]


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 12, 13)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 11, 12)
        w = ctx.draw_int("grid_w", 13, 14)
    else:
        h = ctx.draw_int("grid_h", 9, 12)
        w = ctx.draw_int("grid_w", 12, 14)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    cmd = rng.choice([1, 2, 3, 4])
    g[0][0] = cmd
    chosen_shapes: list = []
    seen_keys: set = set()
    while len(chosen_shapes) < 3:
        s = rng.choice(_SHAPES)
        key = (s[1], s[2], s[3])
        if key in seen_keys: continue
        seen_keys.add(key)
        chosen_shapes.append(s)
    palette = list(random_palette(rng, 3))
    placed: list[tuple[int, int, int, int]] = [(0, 0, 0, 0)]
    for (cells, _sz, sh, sw), color in zip(chosen_shapes, palette):
        for _ in range(80):
            r0 = rng.randint(1, h - sh)
            c0 = rng.randint(1, w - sw)
            bb_pad = (r0 - 1, c0 - 1, r0 + sh, c0 + sw)
            if any(bbox_overlaps(bb_pad, p) for p in placed): continue
            paint_at(g, r0, c0, cells, color)
            placed.append((r0, c0, r0 + sh - 1, c0 + sw - 1))
            break
    return g


def _draw_from_degenerate(name, rng):
    h, w = 10, 13
    g = full_grid(h, w, 0)
    if name == "no_command":
        # Cell (0,0) is bg — rule has no command.
        for r in range(2):
            for c in range(2):
                g[3 + r][3 + c] = 4
        for r in range(2):
            for c in range(3):
                g[6 + r][8 + c] = 5
        return g
    if name == "no_objects":
        # Command set but no objects.
        g[0][0] = 1
        return g
    if name == "tied_dimensions":
        # Two objects with same size, h, w — selector ambiguous.
        g[0][0] = 1
        for r in range(2):
            for c in range(2):
                g[3 + r][3 + c] = 4
        for r in range(2):
            for c in range(2):
                g[6 + r][8 + c] = 5
        return g
    return g
