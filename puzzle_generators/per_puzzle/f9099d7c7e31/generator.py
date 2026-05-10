"""Generator for arc_additional_puzzle_bank_volume4:M25 — Crop to widest object.

Rule: sort objects by (obj-w desc, obj-size desc); crop to bbox of the
first.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_blobs,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: tied_widths, single_blob, no_blobs.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid
from puzzle_generators.helpers.blobs import grow_blob, bbox_of, bbox_overlaps

GENERATOR_ID = "f9099d7c7e31"
VERSION = "1.1.0"
TASK_ID = "f9099d7c7e31"
SUMMARY = "Several non-touching blobs of distinct widths; output crops to widest's bbox."

INVARIANTS = [
    "between 2 and 4 non-touching blobs",
    "widths are distinct (so widest is unambiguous)",
    "blobs are bbox-isolated",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("tied_widths", "single_blob", "no_blobs")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..12", "valid": "7..16"},
    "grid_w":         {"type": "int", "default": "rng 9..14", "valid": "8..18"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_blobs":        {"type": "int", "default": "rng 2..4",  "valid": "2..5"},
    "palette_size":   {"type": "int", "default": "rng 2..4", "valid": "1..9"},
    "position_bias":  {"type": "str", "default": "distinct_widths",
                       "valid": "distinct_widths"},
    "n_distinct_colors": {"type": "int", "default": "rng 2..4", "valid": "1..9"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("grid_w", 9, 10)
        n_blobs = ctx.draw_int("n_blobs", 2, 2)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 11, 12)
        w = ctx.draw_int("grid_w", 13, 14)
        n_blobs = ctx.draw_int("n_blobs", 3, 4)
    else:
        h = ctx.draw_int("grid_h", 8, 12)
        w = ctx.draw_int("grid_w", 9, 14)
        n_blobs = ctx.draw_int("n_blobs", 2, 4)
    g = full_grid(h, w, 0)
    rng = ctx.draw_rng("layout")
    colors = list(range(1, 10)); rng.shuffle(colors)
    used = set(); bboxes = []; widths_used = set()
    for i in range(n_blobs):
        size = rng.randint(3, 6)
        for _ in range(15):
            blob = grow_blob(rng, h, w, used, size)
            if blob is None: continue
            bb = bbox_of(blob)
            bw = bb[3] - bb[1] + 1
            if bw in widths_used: continue
            if any(bbox_overlaps(bb, ob) for ob in bboxes): continue
            used |= blob; bboxes.append(bb); widths_used.add(bw)
            for r, c in blob: g[r][c] = colors[i % len(colors)]
            break
    return g


def _draw_from_degenerate(name, rng):
    h, w = 10, 12
    g = full_grid(h, w, 0)
    if name == "tied_widths":
        # all blobs share the widest width → tie-break by size, ambiguous if sizes equal
        g[1][1] = 4; g[1][2] = 4; g[1][3] = 4
        g[5][5] = 6; g[5][6] = 6; g[5][7] = 6
        g[8][9] = 3; g[8][10] = 3; g[8][11] = 3
        return g
    if name == "single_blob":
        # one blob → trivially widest, output is its bbox crop (whole input)
        for r in range(2):
            for c in range(3): g[3 + r][4 + c] = 4
        return g
    if name == "no_blobs":
        # blank → no objects, rule has no widest to crop to
        return g
    return g
