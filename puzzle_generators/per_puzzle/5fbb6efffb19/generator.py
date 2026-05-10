"""Generator for arc_puzzle_bank_21_set6_s:S6_E6 — wire-length-strip output.

A red marker selects one blue wire; output is a color-6 strip of its length.

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: no_marker (no red marker → rule's selector returns
nothing), no_attached_wire (red marker isolated from any blue cell →
rule's wire-from-marker selector finds nothing, length undefined),
zero_length_wire (marker exists but adjacent wire is degenerate
single-cell → rule's length output is 1, no contrast).
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "5fbb6efffb19"
VERSION = "1.1.0"
TASK_ID = "5fbb6efffb19"

SUMMARY = "A red marker selects one blue wire; output is a color-6 strip of its length."

INVARIANTS = [
    "background is 0",
    "there is exactly one red start marker",
    "the marker has exactly one orthogonally adjacent blue wire",
    "the marked blue wire is non-branching",
    "stray blue components, if present, are unattached distractors",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_marker", "no_attached_wire", "zero_length_wire")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":            {"type": "int", "default": "rng 6..10", "valid": "5..14"},
    "grid_w":            {"type": "int", "default": "rng 8..13", "valid": "6..16"},
    "wire_shape":        {"type": "choice", "default": "rng 0..4", "valid": "0..4"},
    "stray_count":       {"type": "int", "default": "rng 0..2", "valid": "0..4"},
    "palette_kind":      {"type": "str", "default": "rng helpful",
                          "valid": "|".join(PALETTE_KINDS)},
    "palette_size":      {"type": "int", "default": "rng 2..2", "valid": "2..2"},
    "position_bias":     {"type": "str", "default": "marker_attached_wire_plus_strays",
                          "valid": "marker_attached_wire_plus_strays"},
    "n_distinct_colors": {"type": "int", "default": "rng 2..2", "valid": "2..2"},
    "density":           {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":           {"type": "str", "default": "alias for palette_kind",
                          "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}

_PATHS = [
    [(0, 1), (0, 2), (1, 2), (2, 2), (2, 3)],
    [(0, 1), (0, 2), (0, 3), (1, 3), (2, 3), (2, 4)],
    [(1, 0), (2, 0), (2, 1), (2, 2), (3, 2), (3, 3), (3, 4)],
    [(0, 1), (1, 1), (1, 2), (1, 3)],
    [(0, 1), (0, 2), (1, 2), (1, 3), (2, 3), (3, 3), (3, 4), (3, 5)],
]

_STRAYS = [
    [(0, 0), (0, 1), (1, 0), (1, 1)],
    [(0, 0), (1, 0)],
]


def _place_shape(g, rng, cells, occupied):
    h = len(g)
    w = len(g[0])
    max_r = max(r for r, _ in cells)
    max_c = max(c for _, c in cells)
    for _ in range(200):
        r0 = rng.randint(0, h - max_r - 1)
        c0 = rng.randint(0, w - max_c - 1)
        placed = [(r0 + r, c0 + c) for r, c in cells]
        if any(g[r][c] != 0 for r, c in placed):
            continue
        if any(abs(r - rr) + abs(c - cc) <= 1 for r, c in placed for rr, cc in occupied):
            continue
        for r, c in placed:
            g[r][c] = 1
        occupied.update(placed)
        return
    raise ValueError("could not place stray component")


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index, version=VERSION,
                  task_id=TASK_ID, difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 6, 7)
        w = ctx.draw_int("grid_w", 8, 9)
        stray_lo, stray_hi = 0, 0
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 12, 13)
        stray_lo, stray_hi = 1, 2
    else:
        h = ctx.draw_int("grid_h", 6, 10)
        w = ctx.draw_int("grid_w", 8, 13)
        stray_lo, stray_hi = 0, 2
    path = _PATHS[ctx.draw_choice("wire_shape", list(range(len(_PATHS))))]
    stray_count = ctx.draw_int("stray_count", stray_lo, stray_hi)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    max_r = max([0] + [r for r, _ in path])
    max_c = max([0] + [c for _, c in path])
    min_r = min([0] + [r for r, _ in path])
    min_c = min([0] + [c for _, c in path])
    r0 = rng.randint(1 - min_r, h - max_r - 2)
    c0 = rng.randint(1 - min_c, w - max_c - 2)
    g[r0][c0] = 2
    occupied = {(r0, c0)}
    for dr, dc in path:
        g[r0 + dr][c0 + dc] = 1
        occupied.add((r0 + dr, c0 + dc))
    for _ in range(stray_count):
        _place_shape(g, rng, rng.choice(_STRAYS), occupied)
    return g


def _draw_from_degenerate(name, rng):
    h, w = 8, 11
    g = full_grid(h, w, 0)
    if name == "no_marker":
        for r, c in [(2, 2), (2, 3), (3, 3), (4, 3)]: g[r][c] = 1
        return g
    if name == "no_attached_wire":
        g[3][3] = 2
        for r, c in [(6, 7), (6, 8)]: g[r][c] = 1
        return g
    if name == "zero_length_wire":
        # Marker has exactly one adjacent blue cell (length 1) — output
        # strip is degenerate single-cell.
        g[3][3] = 2
        g[3][4] = 1
        return g
    return g
