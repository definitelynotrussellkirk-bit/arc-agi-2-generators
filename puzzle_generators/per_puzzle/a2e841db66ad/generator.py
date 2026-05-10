"""Generator for arc_puzzle_bank_21_set14_s:S14_E6 — header-count selects bbox-height.

A top header count selects the first component whose tight bbox has that many rows.

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: no_header (row 0 empty → rule's k=0 → no component
matches, output undefined), no_matching_height (no component has
bbox-height == k → rule's selector finds nothing), tied_heights
(≥2 components share height k → "first" tie-break decides).
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "a2e841db66ad"
VERSION = "1.1.0"
TASK_ID = "a2e841db66ad"
SUMMARY = "A top header count selects the first component whose tight bbox has that many rows."

INVARIANTS = [
    "row 0 contains exactly k color-1 header cells",
    "below the header there is exactly one component with bbox height k",
    "distractor components have different bbox heights",
    "the selected component is cropped and recolored to 8",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_header", "no_matching_height", "tied_heights")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "height":         {"type": "int", "default": "rng 11..14", "valid": "9..17"},
    "width":          {"type": "int", "default": "rng 12..15", "valid": "10..18"},
    "selected_rows": {"type": "int", "default": "rng 2..4", "valid": "1..6"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "palette_size":   {"type": "int", "default": "rng 3..4", "valid": "2..4"},
    "position_bias":  {"type": "str", "default": "header_plus_components",
                       "valid": "header_plus_components"},
    "n_distinct_colors": {"type": "int", "default": "rng 3..4", "valid": "2..4"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}

_BY_HEIGHT = {
    1: [[(0, 0), (0, 1), (0, 2)]],
    2: [[(0, 0), (0, 1), (1, 1)], [(0, 0), (1, 0), (1, 1)]],
    3: [[(0, 0), (1, 0), (2, 0), (2, 1)], [(0, 1), (1, 0), (1, 1), (2, 1)]],
    4: [[(0, 0), (1, 0), (2, 0), (3, 0), (3, 1)]],
}


def _size(shape):
    return max(r for r, _ in shape) + 1, max(c for _, c in shape) + 1


def _free(g, r0, c0, shape, pad=1):
    h, w = len(g), len(g[0])
    sh, sw = _size(shape)
    if r0 < 1 or c0 < 0 or r0 + sh > h or c0 + sw > w:
        return False
    for r in range(max(1, r0 - pad), min(h, r0 + sh + pad)):
        for c in range(max(0, c0 - pad), min(w, c0 + sw + pad)):
            if g[r][c] != 0:
                return False
    return True


def _place(g, rng, shape, color):
    h, w = len(g), len(g[0])
    sh, sw = _size(shape)
    for _ in range(120):
        r0 = rng.randint(1, h - sh)
        c0 = rng.randint(0, w - sw)
        if _free(g, r0, c0, shape):
            for dr, dc in shape:
                g[r0 + dr][c0 + dc] = color
            return
    raise ValueError("could not place component")


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index, version=VERSION,
                  task_id=TASK_ID, difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("height", 11, 12)
        w = ctx.draw_int("width", 12, 13)
        k = ctx.draw_int("selected_rows", 2, 3)
    elif difficulty == "hard":
        h = ctx.draw_int("height", 13, 16)
        w = ctx.draw_int("width", 14, 17)
        k = ctx.draw_int("selected_rows", 3, 4)
    else:
        h = ctx.draw_int("height", 11, 14)
        w = ctx.draw_int("width", 12, 15)
        k = ctx.draw_int("selected_rows", 2, 4)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    for c in range(k):
        g[0][c] = 1
    colors = [2, 3, 4]
    rng.shuffle(colors)
    _place(g, rng, rng.choice(_BY_HEIGHT[k]), colors[0])
    other_heights = [v for v in [1, 2, 3, 4] if v != k]
    rng.shuffle(other_heights)
    for color, height in zip(colors[1:], other_heights[:2]):
        _place(g, rng, rng.choice(_BY_HEIGHT[height]), color)
    return g


def _draw_from_degenerate(name, rng):
    h, w = 12, 14
    g = full_grid(h, w, 0)
    if name == "no_header":
        # Row 0 empty — rule's k=0; no component can match, output
        # undefined.
        for dr, dc in _BY_HEIGHT[2][0]:
            g[2 + dr][2 + dc] = 2
        for dr, dc in _BY_HEIGHT[3][0]:
            g[6 + dr][8 + dc] = 3
        return g
    if name == "no_matching_height":
        # Header says k=3 but no component has bbox-height 3; rule's
        # selector finds nothing.
        for c in range(3):
            g[0][c] = 1
        for dr, dc in _BY_HEIGHT[1][0]:
            g[3 + dr][2 + dc] = 2
        for dr, dc in _BY_HEIGHT[4][0]:
            g[5 + dr][8 + dc] = 3
        return g
    if name == "tied_heights":
        # Two components share bbox-height k=2 → "first" tie-break
        # (by position) decides.
        for c in range(2):
            g[0][c] = 1
        for dr, dc in _BY_HEIGHT[2][0]:
            g[3 + dr][2 + dc] = 2
        for dr, dc in _BY_HEIGHT[2][1]:
            g[3 + dr][8 + dc] = 3
        for dr, dc in _BY_HEIGHT[4][0]:
            g[7 + dr][5 + dc] = 4
        return g
    return g
