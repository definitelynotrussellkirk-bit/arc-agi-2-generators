"""Generator for arc_puzzle_bank_21_set15:S15_E6 — copy color-2 stencil from 1-anchor to 3-anchor.

Color-2 cells are copied by preserving offsets from a color-1 source
anchor to a color-3 target anchor.

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: no_source_anchor (no color-1 → rule's source-anchor
selector returns nothing, no offsets to copy), no_target_anchor (no
color-3 → rule has nowhere to copy to), no_stencil (no color-2 cells
near 1-anchor → rule's stencil is empty, copy is no-op).
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "57b3d1e61318"
VERSION = "1.1.0"
TASK_ID = "57b3d1e61318"
SUMMARY = "Color-2 cells are copied by preserving offsets from a color-1 source anchor to a color-3 target anchor."

INVARIANTS = [
    "background is 0",
    "there is exactly one color-1 source anchor",
    "there is exactly one color-3 target anchor",
    "all color-2 source cells fit when moved by the source-to-target anchor vector",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_source_anchor", "no_target_anchor", "no_stencil")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "height":            {"type": "int", "default": "rng 9..12", "valid": "7..15"},
    "width":             {"type": "int", "default": "rng 11..14", "valid": "9..17"},
    "offset_pattern":    {"type": "choice", "default": "rng centered stencil",
                          "valid": "small nonzero offset sets"},
    "palette_kind":      {"type": "str", "default": "rng helpful",
                          "valid": "|".join(PALETTE_KINDS)},
    "palette_size":      {"type": "int", "default": "rng 3..3", "valid": "3..3"},
    "position_bias":     {"type": "str", "default": "source_target_anchors",
                          "valid": "source_target_anchors"},
    "n_distinct_colors": {"type": "int", "default": "rng 3..3", "valid": "3..3"},
    "density":           {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":           {"type": "str", "default": "alias for palette_kind",
                          "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}

_OFFSET_PATTERNS = [
    [(-1, 0), (0, 1), (1, 0), (1, 1)],
    [(0, -1), (0, 1), (1, 1), (2, 1)],
    [(-1, -1), (-1, 0), (0, 1), (1, 1)],
    [(-2, 0), (-1, 0), (0, 1), (1, 1)],
    [(-1, 1), (0, -1), (0, 0), (1, -1)],
]


def _fits(h, w, anchor, offsets):
    ar, ac = anchor
    return all(0 <= ar + dr < h and 0 <= ac + dc < w for dr, dc in offsets)


def _near_nonzero(g, r, c, radius=1):
    h, w = len(g), len(g[0])
    for rr in range(max(0, r - radius), min(h, r + radius + 1)):
        for cc in range(max(0, c - radius), min(w, c + radius + 1)):
            if g[rr][cc] != 0:
                return True
    return False


def _place_source(g, rng, offsets):
    h, w = len(g), len(g[0])
    for _ in range(120):
        ar = rng.randint(2, h - 3)
        ac = rng.randint(2, w - 3)
        if not _fits(h, w, (ar, ac), offsets):
            continue
        if _near_nonzero(g, ar, ac):
            continue
        cells = [(ar + dr, ac + dc) for dr, dc in offsets]
        if all(g[r][c] == 0 for r, c in cells):
            g[ar][ac] = 1
            for r, c in cells:
                if (r, c) != (ar, ac):
                    g[r][c] = 2
            return
    raise ValueError("could not place source anchor")


def _place_target(g, rng, offsets):
    h, w = len(g), len(g[0])
    for _ in range(160):
        ar = rng.randint(1, h - 2)
        ac = rng.randint(1, w - 2)
        if not _fits(h, w, (ar, ac), offsets):
            continue
        if not _near_nonzero(g, ar, ac, radius=2):
            g[ar][ac] = 3
            return
    raise ValueError("could not place target anchor")


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index, version=VERSION,
                  task_id=TASK_ID, difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("height", 9, 10)
        w = ctx.draw_int("width", 11, 12)
    elif difficulty == "hard":
        h = ctx.draw_int("height", 12, 12)
        w = ctx.draw_int("width", 13, 14)
    else:
        h = ctx.draw_int("height", 9, 12)
        w = ctx.draw_int("width", 11, 14)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    offsets = rng.choice(_OFFSET_PATTERNS)
    _place_source(g, rng, offsets)
    _place_target(g, rng, offsets)
    return g


def _draw_from_degenerate(name, rng):
    h, w = 10, 12
    g = full_grid(h, w, 0)
    if name == "no_source_anchor":
        # No color-1 — rule's source-anchor selector returns nothing.
        g[2][2] = 2; g[2][3] = 2; g[3][2] = 2
        g[6][7] = 3
        return g
    if name == "no_target_anchor":
        # No color-3 — rule has nowhere to copy to.
        g[2][2] = 1
        g[2][3] = 2; g[3][2] = 2
        return g
    if name == "no_stencil":
        # Source anchor exists but no color-2 cells — rule's stencil
        # is empty; copy is no-op.
        g[2][2] = 1
        g[6][7] = 3
        return g
    return g
