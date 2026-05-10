"""Generator for arc_puzzle_bank_ninth21:M59 — reflect across painted vertical 5-axis.

Rule: a full vertical 5-line at some col c. Mirror every non-5 cell
across that axis: (r, x) → (r, 2c - x). Original cells stay.

Combinatorial axes (8): grid_h, grid_w, palette_kind, blob_size,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_axis, no_blob, blob_on_axis.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid
from puzzle_generators.helpers.blobs import grow_blob

GENERATOR_ID = "250671db7aa1"
VERSION = "1.1.0"
TASK_ID = "250671db7aa1"
SUMMARY = "Full vertical 5-line + content on one side that reflects in-bounds."

INVARIANTS = [
    "background is 0",
    "exactly one full vertical 5-line",
    "all non-5 content on one side; reflected positions stay in-bounds",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_axis", "no_blob", "blob_on_axis")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..11", "valid": "7..14"},
    "grid_w":         {"type": "int", "default": "rng 9..12", "valid": "8..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "blob_size":      {"type": "int", "default": "rng 3..5", "valid": "1..7"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2..2"},
    "position_bias":  {"type": "str", "default": "5axis_with_left_blob",
                       "valid": "5axis_with_left_blob"},
    "n_distinct_colors": {"type": "int", "default": "2", "valid": "2..2"},
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
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 10, 11)
        w = ctx.draw_int("grid_w", 11, 12)
    else:
        h = ctx.draw_int("grid_h", 8, 11)
        w = ctx.draw_int("grid_w", 9, 12)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    axis_c = w // 2  # center axis (or close to it)
    for r in range(h):
        g[r][axis_c] = 5
    used = {(r, axis_c) for r in range(h)}
    # reserve right side so blob lives on left
    for r in range(h):
        for c in range(axis_c, w):
            used.add((r, c))
    color = rng.choice([1, 2, 3, 4, 6, 7, 8, 9])
    for _ in range(40):
        cells = grow_blob(rng, h, w, used, rng.randint(3, 5), max_attempts=20)
        if cells is None:
            continue
        # check reflections in-bounds
        ok = True
        for r, c in cells:
            mc = 2 * axis_c - c
            if not (0 <= mc < w):
                ok = False; break
        if not ok:
            continue
        for r, c in cells:
            g[r][c] = color
        break
    return g


def _draw_from_degenerate(name, rng):
    h, w = 9, 11
    g = full_grid(h, w, 0)
    if name == "no_axis":
        # blob but no 5-axis → no reflection axis defined
        g[3][2] = 4; g[3][3] = 4; g[4][3] = 4
        return g
    if name == "no_blob":
        # 5-axis but no blob → nothing to reflect
        for r in range(h): g[r][w // 2] = 5
        return g
    if name == "blob_on_axis":
        # blob lies on the axis itself → reflection is identity
        for r in range(h): g[r][w // 2] = 5
        # blob cells overlap axis (note this also breaks the "non-5 on one side" invariant)
        g[2][w // 2] = 4
        g[3][w // 2] = 4
        return g
    return g
