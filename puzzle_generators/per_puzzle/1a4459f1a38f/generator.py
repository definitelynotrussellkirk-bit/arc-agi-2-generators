"""Generator for arc_puzzle_bank_thirteenth_21_bundle:easy_89_crop_largest_component.

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: no_components, equal_sizes, single_only.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "1a4459f1a38f"
VERSION = "1.1.0"
TASK_ID = "1a4459f1a38f"

SUMMARY = "The largest connected colored component is selected and cropped."

INVARIANTS = [
    "background is 0",
    "there is one largest component by area",
    "smaller distractor components are separated from the largest",
    "the selected crop preserves the component's original colors",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_components", "equal_sizes", "single_only")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..12", "valid": "5..20"},
    "grid_w":         {"type": "int", "default": "rng 9..14", "valid": "5..24"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "palette_size":   {"type": "int", "default": "2", "valid": "2..3"},
    "position_bias":  {"type": "str", "default": "main_with_distractors",
                       "valid": "main_with_distractors"},
    "n_distinct_colors": {"type": "int", "default": "2", "valid": "2..3"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def _free(g, cells):
    h, w = len(g), len(g[0])
    for r, c in cells:
        if not (0 <= r < h and 0 <= c < w):
            return False
        for rr in range(max(0, r - 1), min(h, r + 2)):
            for cc in range(max(0, c - 1), min(w, c + 2)):
                if g[rr][cc] != 0:
                    return False
    return True


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index, version=VERSION,
                  task_id=TASK_ID, difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("grid_w", 9, 10)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 11, 14)
        w = ctx.draw_int("grid_w", 13, 16)
    else:
        h = ctx.draw_int("grid_h", 8, 12)
        w = ctx.draw_int("grid_w", 9, 14)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    color = rng.choice([1, 2, 3, 4, 5, 6, 7, 8, 9])
    shape = [(0, 0), (0, 1), (0, 2), (1, 0), (1, 2), (2, 0), (2, 1), (2, 2)]
    r0 = rng.randint(1, h - 4)
    c0 = rng.randint(1, w - 4)
    for dr, dc in shape:
        g[r0 + dr][c0 + dc] = color
    for size in (3, 2):
        for _ in range(60):
            cells = []
            r = rng.randint(0, h - 2)
            c = rng.randint(0, w - 2)
            for i in range(size):
                cells.append((r, min(w - 1, c + i)))
            if _free(g, cells):
                fill = rng.choice([x for x in range(1, 10) if x != color])
                for rr, cc in cells:
                    g[rr][cc] = fill
                break
    return g


def _draw_from_degenerate(name, rng):
    h, w = 9, 11
    g = full_grid(h, w, 0)
    if name == "no_components":
        # Empty grid — rule has no component to crop.
        return g
    if name == "equal_sizes":
        # Two components of equal area — "largest" is ambiguous.
        for c in range(3, 6): g[2][c] = 4
        for c in range(3, 6): g[6][c] = 5
        return g
    if name == "single_only":
        # Only one component (no distractors) — crop is just identity-on-bbox.
        for r in range(2, 5):
            for c in range(2, 5): g[r][c] = 4
        return g
    return g
