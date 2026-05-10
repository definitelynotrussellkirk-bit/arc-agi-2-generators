"""Generator for puzzle 505fff84.

Rule: rows with exactly 1+8 markers contribute the cells strictly
between them; rule stacks those payload-rows in input order.

Combinatorial axes (8): payload_width, payload_rows, palette_kind,
marker_orientation, anchor_corner, asymmetry_force, n_distract_rows,
include_decoy.
Degenerates: no_payload_rows, all_distract, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "09fb9d59621e"
VERSION = "1.1.0"
TASK_ID = "09fb9d59621e"
SUMMARY = "Rows with 1/8 markers; rule extracts between-marker payload rows."

INVARIANTS = [
    "background is 0",
    "selected rows have exactly 1 cell of 1 + 1 cell of 8",
    "all selected rows have same payload width",
    "marker positions: c1 (1) + c8 (8), |c8 - c1| = payload_width + 1",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary")
MARKER_ORIENTATIONS = ("left_first", "right_first", "rng")
DEGENERATE_TEXTURES = ("no_payload_rows", "all_distract", "full_grid")
HELPFUL_TEXTURES = MARKER_ORIENTATIONS

AXES = {
    "payload_width":     {"type": "int", "default": "rng 3..5", "valid": "1..12"},
    "payload_rows":      {"type": "int", "default": "rng 2..4", "valid": "1..12"},
    "palette_kind":      {"type": "str", "default": "rng helpful",
                          "valid": "|".join(PALETTE_KINDS)},
    "marker_orientation":{"type": "str", "default": "rng helpful",
                          "valid": "|".join(MARKER_ORIENTATIONS)},
    "anchor_corner":     {"type": "bool", "default": "false",
                          "valid": "true|false"},
    "asymmetry_force":   {"type": "bool", "default": "false",
                          "valid": "true|false"},
    "n_distract_rows":   {"type": "int", "default": "0", "valid": "0..3"},
    "include_decoy":     {"type": "bool", "default": "false",
                          "valid": "true|false"},
    "texture":           {"type": "str", "default": "alias for marker_orientation",
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
        pw_lo, pw_hi = 1, 3
        pr_lo, pr_hi = 1, 2
    elif difficulty == "hard":
        pw_lo, pw_hi = 5, 8
        pr_lo, pr_hi = 4, 6
    else:
        pw_lo, pw_hi = 3, 5
        pr_lo, pr_hi = 2, 4
    payload_width = int(overrides.get("payload_width",
                                      ctx.draw_int("payload_width",
                                                   pw_lo, pw_hi)))
    payload_rows = int(overrides.get("payload_rows",
                                     ctx.draw_int("payload_rows",
                                                  pr_lo, pr_hi)))
    payload_width = max(1, min(12, payload_width))
    payload_rows = max(1, min(12, payload_rows))
    palette_kind = overrides.get("palette_kind",
                                 ctx.draw_choice("palette_kind",
                                                 list(PALETTE_KINDS)))
    palette = _build_palette(palette_kind, rng)
    orient = (overrides.get("texture") or
              overrides.get("marker_orientation")
              or ctx.draw_choice("marker_orientation",
                                 list(MARKER_ORIENTATIONS)))
    h = payload_rows * 2 + 2
    w = payload_width + 6
    g = full_grid(h, w, 0)
    payload_colors = palette
    for i in range(payload_rows):
        r = 1 + i * 2
        if orient == "rng":
            left = rng.choice([True, False])
        else:
            left = (orient == "left_first")
        c1 = 1
        c8 = c1 + payload_width + 1
        if left:
            g[r][c1] = 1
            g[r][c8] = 8
        else:
            g[r][c1] = 8
            g[r][c8] = 1
        for j in range(payload_width):
            g[r][c1 + 1 + j] = rng.choice(payload_colors)
    return g


def _build_palette(kind, rng):
    if kind == "warm":
        pool = [2, 3, 4, 6, 9, 0]
    elif kind == "cool":
        pool = [0, 5, 7]
    elif kind == "primary":
        pool = [0, 2, 3, 4]
    else:
        pool = [0, 2, 3, 4, 5, 6, 7, 9]
    rng.shuffle(pool)
    return pool


def _draw_from_degenerate(name, rng):
    h = 8; w = 9
    g = full_grid(h, w, 0)
    if name == "no_payload_rows":
        # Just rows of 1s without 8s
        for r in range(1, h, 2):
            g[r][1] = 1
        return g
    if name == "all_distract":
        # Many rows but none with proper 1+8 alignment
        for r in range(1, h):
            g[r][rng.randint(0, w - 1)] = rng.choice([1, 8])
        return g
    if name == "full_grid":
        for r in range(h):
            for c in range(w):
                g[r][c] = 1
        return g
    return g
