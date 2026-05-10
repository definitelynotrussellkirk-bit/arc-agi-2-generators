"""Generator for arc_additional_puzzles_21_set18_bundle:H120 — keyed offset merge.

Rule: a single color-9 reference defines an offset cloud (color-8 cells around it).
Anchors (colors 2/3/4/5) replay the cloud rotated by 0/90/180/270 around themselves
and paint cells with colors 4/5/6/7 (max-merged on overlap).

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: no_reference (no color-9 cell → rule has no offset
basis); no_cloud (reference present but no color-8 cloud → cloud
is empty, anchor stamps paint nothing); no_anchors (reference + cloud
present but no color {2,3,4,5} anchors → rule produces no stamps).
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "17b682bce66f"
VERSION = "1.1.0"
TASK_ID = "17b682bce66f"

SUMMARY = "1 color-9 reference + 1-3 color-8 cloud cells + 2-3 anchors (colors 2..5)."

INVARIANTS = [
    "background is 0",
    "exactly one color-9 reference cell and 1-3 color-8 cloud cells near it",
    "2-3 anchors in colors {2, 3, 4, 5} placed elsewhere",
    "anchors do not coincide with reference/cloud cells",
    "rotated cloud at each anchor must produce in-bounds cells (we keep cloud small)",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_reference", "no_cloud", "no_anchors")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":            {"type": "int", "default": "rng 9..11", "valid": "8..14"},
    "grid_w":            {"type": "int", "default": "rng 9..11", "valid": "8..14"},
    "palette_kind":      {"type": "str", "default": "rng helpful",
                          "valid": "|".join(PALETTE_KINDS)},
    "palette_size":      {"type": "int", "default": "rng 5..6", "valid": "4..6"},
    "position_bias":     {"type": "str", "default": "reference_cloud_plus_anchors",
                          "valid": "reference_cloud_plus_anchors"},
    "n_distinct_colors": {"type": "int", "default": "rng 5..6", "valid": "4..6"},
    "density":           {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":           {"type": "str", "default": "alias for palette_kind",
                          "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 9, 9)
        w = ctx.draw_int("grid_w", 9, 9)
        n_anchors = ctx.draw_int("n_anchors", 2, 2)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 11, 11)
        w = ctx.draw_int("grid_w", 11, 11)
        n_anchors = ctx.draw_int("n_anchors", 3, 3)
    else:
        h = ctx.draw_int("grid_h", 9, 11)
        w = ctx.draw_int("grid_w", 9, 11)
        n_anchors = ctx.draw_int("n_anchors", 2, 3)
    rng = ctx.draw_rng("layout")
    anchor_colors = rng.sample([2, 3, 4, 5], n_anchors)

    for outer in range(40):
        g = full_grid(h, w, 0)
        rr = rng.randint(2, h - 3)
        rc = rng.randint(2, w - 3)
        g[rr][rc] = 9
        n_cloud = rng.randint(1, 3)
        cloud_offsets = []
        for _ in range(n_cloud):
            for _try in range(40):
                dr = rng.randint(-2, 2)
                dc = rng.randint(-2, 2)
                if (dr, dc) == (0, 0): continue
                if (dr, dc) in cloud_offsets: continue
                nr, nc = rr + dr, rc + dc
                if 0 <= nr < h and 0 <= nc < w and g[nr][nc] == 0:
                    g[nr][nc] = 8
                    cloud_offsets.append((dr, dc))
                    break
        if not cloud_offsets:
            continue
        placed = []
        ok = True
        for color in anchor_colors:
            placed_a = False
            for _ in range(120):
                ar = rng.randint(0, h - 1)
                ac = rng.randint(0, w - 1)
                if g[ar][ac] != 0:
                    continue
                if any(abs(ar - pr) + abs(ac - pc) < 2 for pr, pc in placed):
                    continue
                if (ar, ac) == (rr, rc):
                    continue
                g[ar][ac] = color
                placed.append((ar, ac))
                placed_a = True
                break
            if not placed_a:
                ok = False
                break
        if ok:
            return g
    raise ValueError("could not realize keyed-offset merge layout in 40 attempts")


def _draw_from_degenerate(name, rng):
    h, w = 10, 10
    g = full_grid(h, w, 0)
    if name == "no_reference":
        # No color-9 reference — rule has no offset basis.
        g[3][4] = 8; g[3][6] = 8
        g[6][2] = 2; g[6][7] = 3
        return g
    if name == "no_cloud":
        # Reference but no color-8 cloud — anchors stamp nothing.
        g[4][4] = 9
        g[6][1] = 2; g[6][7] = 3; g[2][7] = 4
        return g
    if name == "no_anchors":
        # Reference + cloud but no anchors — no stamping happens.
        g[4][4] = 9
        g[3][5] = 8; g[5][3] = 8
        return g
    return g
