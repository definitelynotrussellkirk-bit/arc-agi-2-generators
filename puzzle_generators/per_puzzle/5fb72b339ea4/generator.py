"""Generator for ARC task 88a62173.

Rule: input is 5 × 5 with 4 corner 2 × 2 patches; exactly one is unique.
Output is the unique 2 × 2 patch.

Combinatorial axes (8):
  * unique_corner       — which corner has the unique patch (0..3)
  * common_pattern      — pattern of the 3 identical patches:
                          mostly_zero / two_color / L_shape / diagonal /
                          single_color / corners
  * unique_difference   — how the unique differs: extra_cell /
                          different_color / inverted / single_swap /
                          all_different
  * a_color / b_color / c_color — colors used in patches
  * center_decoy        — what fills the center 1 × 1 cells (rule ignores):
                          random / zero / matching / decoy_palette
  * inter_corner_decoy  — patterns in the gap rows/cols (also ignored)
  * caller-opt-in degenerates: all_corners_same (no unique),
                              two_pairs (ambiguous unique),
                              all_corners_different.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "5fb72b339ea4"
VERSION = "1.1.0"
TASK_ID = "5fb72b339ea4"
SUMMARY = "5 × 5 with 4 corner 2 × 2 patches; rule outputs the unique one."

INVARIANTS = [
    "input is 5 × 5",
    "corner patches at (0..1, 0..1), (0..1, 3..4), (3..4, 0..1), (3..4, 3..4)",
    "exactly one corner patch is unique among the four",
]

COMMON_PATTERNS = ("mostly_zero", "two_color", "L_shape", "diagonal",
                   "single_color", "corners_solid")
UNIQUE_DIFFERENCES = ("extra_cell", "different_color", "inverted",
                     "single_swap", "all_different")
CENTER_DECOYS = ("zero", "random", "matching", "decoy_palette")
DEGENERATE_TEXTURES = ("all_corners_same", "two_pairs", "all_different")
HELPFUL_TEXTURES = COMMON_PATTERNS

AXES = {
    "unique_corner":     {"type": "int", "default": "rng 0..3", "valid": "0..3"},
    "common_pattern":    {"type": "str", "default": "rng helpful",
                          "valid": "|".join(COMMON_PATTERNS)},
    "unique_difference": {"type": "str", "default": "rng helpful",
                          "valid": "|".join(UNIQUE_DIFFERENCES)},
    "a_color":           {"type": "color", "default": "rng (≠0)", "valid": "1..9"},
    "b_color":           {"type": "color", "default": "rng (≠0,a)", "valid": "1..9"},
    "c_color":           {"type": "color", "default": "rng (≠0,a,b)", "valid": "1..9"},
    "center_decoy":      {"type": "str", "default": "rng helpful",
                          "valid": "|".join(CENTER_DECOYS)},
    "decoy_palette_size": {"type": "int", "default": "rng 0..3", "valid": "0..6"},
    "texture":           {"type": "str", "default": "alias for common_pattern",
                          "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    rng = ctx.draw_rng("cells")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], rng, ctx)
    unique = int(overrides.get("unique_corner",
                               ctx.draw_int("unique_corner", 0, 3)))
    common_pattern = (overrides.get("texture") or overrides.get("common_pattern")
                      or ctx.draw_choice("common_pattern", list(COMMON_PATTERNS)))
    diff_kind = overrides.get("unique_difference",
                              ctx.draw_choice("unique_difference", list(UNIQUE_DIFFERENCES)))
    a = int(overrides.get("a_color", ctx.draw_color("a_color", exclude={0})))
    b = int(overrides.get("b_color", ctx.draw_color("b_color", exclude={0, a})))
    c = int(overrides.get("c_color", ctx.draw_color("c_color", exclude={0, a, b})))
    center_decoy = overrides.get("center_decoy",
                                 ctx.draw_choice("center_decoy", list(CENTER_DECOYS)))
    n_decoy = int(overrides.get("decoy_palette_size",
                                ctx.draw_int("decoy_palette_size", 0, 3)))
    decoy_palette = [c2 for c2 in range(1, 10) if c2 not in {a, b, c}]
    rng.shuffle(decoy_palette)
    decoy_palette = decoy_palette[:max(0, n_decoy)]
    g = full_grid(5, 5, 0)
    common_patch = _make_common(common_pattern, a, b)
    unique_patch = _make_unique(diff_kind, common_patch, a, b, c)
    starts = [(0, 0), (0, 3), (3, 0), (3, 3)]
    for i, (r0, c0) in enumerate(starts):
        patch = unique_patch if i == unique else common_patch
        for dr in range(2):
            for dc in range(2):
                g[r0 + dr][c0 + dc] = patch[dr][dc]
    # Center decoy
    if center_decoy == "random":
        for r in range(5):
            for c in range(5):
                if not _in_corner_patch(r, c) and rng.random() < 0.4:
                    g[r][c] = rng.choice(decoy_palette) if decoy_palette else 0
    elif center_decoy == "matching":
        for r in range(5):
            for c in range(5):
                if not _in_corner_patch(r, c):
                    g[r][c] = a
    elif center_decoy == "decoy_palette" and decoy_palette:
        for r in range(5):
            for c in range(5):
                if not _in_corner_patch(r, c):
                    g[r][c] = rng.choice(decoy_palette)
    return g


def _in_corner_patch(r, c):
    return (r in (0, 1, 3, 4)) and (c in (0, 1, 3, 4))


def _make_common(pattern, a, b):
    if pattern == "mostly_zero":
        return [[a, 0], [0, b]]
    if pattern == "two_color":
        return [[a, b], [b, a]]
    if pattern == "L_shape":
        return [[a, 0], [a, a]]
    if pattern == "diagonal":
        return [[a, 0], [0, a]]
    if pattern == "single_color":
        return [[a, a], [a, a]]
    if pattern == "corners_solid":
        return [[a, 0], [0, b]]
    return [[a, 0], [0, b]]


def _make_unique(kind, common, a, b, c):
    p = [row[:] for row in common]
    if kind == "extra_cell":
        # Add c at (0, 1) if it's currently 0
        if p[0][1] == 0:
            p[0][1] = c
        else:
            p[1][0] = c
    elif kind == "different_color":
        # Replace one cell with c.
        p[0][0] = c
    elif kind == "inverted":
        for r in range(2):
            for cc in range(2):
                p[r][cc] = (a if p[r][cc] == b else
                            b if p[r][cc] == a else p[r][cc])
        # Ensure differs from common
        if p == common:
            p[0][0] = c
    elif kind == "single_swap":
        p[0][0], p[1][1] = p[1][1], p[0][0]
        if p == common:
            p[0][1] = c
    elif kind == "all_different":
        p = [[a, b], [c, 0]]
    return p


def _draw_from_degenerate(name, rng, ctx):
    a = ctx.draw_color("a_color", exclude={0})
    b = ctx.draw_color("b_color", exclude={0, a})
    c = ctx.draw_color("c_color", exclude={0, a, b})
    g = full_grid(5, 5, 0)
    starts = [(0, 0), (0, 3), (3, 0), (3, 3)]
    if name == "all_corners_same":
        patch = [[a, 0], [0, b]]
        for r0, c0 in starts:
            for dr in range(2):
                for dc in range(2):
                    g[r0 + dr][c0 + dc] = patch[dr][dc]
        return g
    if name == "two_pairs":
        p1 = [[a, 0], [0, b]]
        p2 = [[c, 0], [0, b]]
        for i, (r0, c0) in enumerate(starts):
            patch = p1 if i < 2 else p2
            for dr in range(2):
                for dc in range(2):
                    g[r0 + dr][c0 + dc] = patch[dr][dc]
        return g
    if name == "all_different":
        patches = [[[a, 0], [0, b]], [[b, a], [0, 0]],
                   [[c, 0], [a, b]], [[a, b], [c, 0]]]
        for i, (r0, c0) in enumerate(starts):
            for dr in range(2):
                for dc in range(2):
                    g[r0 + dr][c0 + dc] = patches[i][dr][dc]
        return g
    return g
