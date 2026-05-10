"""Generator for arc_puzzle_bank_nineteenth_21_bundle:medium_127_select_legend_object_and_rotate_cw.

Rule: cell (0,0) holds a marker color. Find the object that shares
that color, crop to bbox, rotate clockwise, output.

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: no_marker (cell (0,0) is bg → rule's marker selector
returns nothing, no target chosen), no_match (marker present but no
object shares its color → rule's selector finds nothing), rot_symmetric_target
(target object is rotationally symmetric → rotate-cw is identity,
output equals cropped input).
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, paint_at
from puzzle_generators.helpers.palette import random_palette
from puzzle_generators.helpers.blobs import bbox_overlaps

GENERATOR_ID = "c425a7cc61c7"
VERSION = "1.1.0"
TASK_ID = "c425a7cc61c7"
SUMMARY = "Marker at (0,0) + a target-color shape + 1-2 distractor shapes."

INVARIANTS = [
    "background is 0",
    "(0, 0) holds the target marker color",
    "exactly one object of that color elsewhere with ≥3 cells",
    "1-2 distractor objects in other colors",
    "objects don't touch each other or (0, 0)",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_marker", "no_match", "rot_symmetric_target")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":            {"type": "int", "default": "rng 9..12", "valid": "8..14"},
    "grid_w":            {"type": "int", "default": "rng 10..14", "valid": "9..18"},
    "palette_kind":      {"type": "str", "default": "rng helpful",
                          "valid": "|".join(PALETTE_KINDS)},
    "palette_size":      {"type": "int", "default": "rng 3..3", "valid": "2..4"},
    "position_bias":     {"type": "str", "default": "marker_plus_target_plus_distractors",
                          "valid": "marker_plus_target_plus_distractors"},
    "n_distinct_colors": {"type": "int", "default": "rng 3..3", "valid": "2..4"},
    "density":           {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":           {"type": "str", "default": "alias for palette_kind",
                          "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}

_TARGET_SHAPES = [
    [(0, 0), (0, 1), (0, 2), (1, 0)],
    [(0, 0), (0, 1), (1, 1), (1, 2)],
    [(0, 0), (1, 0), (1, 1), (2, 1)],
    [(0, 0), (0, 1), (0, 2), (1, 0), (2, 0)],
]
_DISTRACT = [
    [(0, 0), (0, 1)],
    [(0, 0), (1, 0)],
    [(0, 0), (0, 1), (1, 0)],
    [(0, 0), (1, 0), (1, 1)],
]


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 10, 11)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 12, 12)
        w = ctx.draw_int("grid_w", 13, 14)
    else:
        h = ctx.draw_int("grid_h", 9, 12)
        w = ctx.draw_int("grid_w", 10, 14)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    palette = list(random_palette(rng, 3))
    target = palette[0]
    g[0][0] = target
    placed: list[tuple[int, int, int, int]] = [(0, 0, 0, 0)]
    target_shape = rng.choice(_TARGET_SHAPES)
    sh = max(c[0] for c in target_shape) + 1
    sw = max(c[1] for c in target_shape) + 1
    for _ in range(80):
        r0 = rng.randint(2, h - sh - 1)
        c0 = rng.randint(2, w - sw - 1)
        bb = (r0 - 1, c0 - 1, r0 + sh, c0 + sw)
        if any(bbox_overlaps(bb, p) for p in placed): continue
        paint_at(g, r0, c0, target_shape, target)
        placed.append((r0, c0, r0 + sh - 1, c0 + sw - 1))
        break
    for color in palette[1:]:
        ds = rng.choice(_DISTRACT)
        dh = max(c[0] for c in ds) + 1
        dw = max(c[1] for c in ds) + 1
        for _ in range(80):
            r0 = rng.randint(2, h - dh - 1)
            c0 = rng.randint(2, w - dw - 1)
            bb = (r0 - 1, c0 - 1, r0 + dh, c0 + dw)
            if any(bbox_overlaps(bb, p) for p in placed): continue
            paint_at(g, r0, c0, ds, color)
            placed.append((r0, c0, r0 + dh - 1, c0 + dw - 1))
            break
    return g


def _draw_from_degenerate(name, rng):
    h, w = 10, 11
    g = full_grid(h, w, 0)
    if name == "no_marker":
        # (0,0) is bg — rule's marker-selector returns nothing.
        for dr, dc in [(0, 0), (0, 1), (0, 2), (1, 0)]:
            g[3 + dr][3 + dc] = 4
        for dr, dc in [(0, 0), (1, 0)]:
            g[6 + dr][7 + dc] = 6
        return g
    if name == "no_match":
        # Marker present at (0,0) but no object shares its color.
        g[0][0] = 4
        for dr, dc in [(0, 0), (0, 1), (1, 0)]:
            g[3 + dr][3 + dc] = 6
        for dr, dc in [(0, 0), (1, 0)]:
            g[6 + dr][7 + dc] = 8
        return g
    if name == "rot_symmetric_target":
        # Target object is rotationally symmetric (2x2 block) — rotate-cw
        # is identity; output equals cropped input.
        g[0][0] = 4
        g[3][3] = 4; g[3][4] = 4; g[4][3] = 4; g[4][4] = 4
        for dr, dc in [(0, 0), (1, 0)]:
            g[6 + dr][7 + dc] = 8
        return g
    return g
