"""Generator for 5b:m33 — extract bisymmetric component.

Rule: of the connected components, exactly one is both H- and V-mirror
symmetric (its bbox-cropped binary shape). Output is that component cropped.

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: no_components (no shapes → rule has nothing to extract);
all_symmetric (every component is bisymmetric → "exactly one"
precondition fails); all_asymmetric (no component is bisymmetric →
selector returns nothing).
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "50a9716052c7"
VERSION = "1.1.0"
TASK_ID = "50a9716052c7"
SUMMARY = "2-3 components; exactly one is H+V mirror-symmetric in its bbox."

INVARIANTS = [
    "background is 0",
    "2-3 isolated connected components, distinct colors",
    "exactly one is bi-symmetric (H and V mirror) — others are asymmetric",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_components", "all_symmetric", "all_asymmetric")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":            {"type": "int", "default": "rng 9..12", "valid": "8..14"},
    "grid_w":            {"type": "int", "default": "rng 11..14", "valid": "10..16"},
    "palette_kind":      {"type": "str", "default": "rng helpful",
                          "valid": "|".join(PALETTE_KINDS)},
    "palette_size":      {"type": "int", "default": "rng 2..3", "valid": "2..3"},
    "position_bias":     {"type": "str", "default": "bisymmetric_plus_asymmetric",
                          "valid": "bisymmetric_plus_asymmetric"},
    "n_distinct_colors": {"type": "int", "default": "rng 2..3", "valid": "2..3"},
    "density":           {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":           {"type": "str", "default": "alias for palette_kind",
                          "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


_SYMMETRIC = [
    [(0, 0), (0, 1), (0, 2), (1, 0), (1, 2), (2, 0), (2, 1), (2, 2)],
    [(0, 1), (1, 0), (1, 1), (1, 2), (2, 1)],
    [(0, 0), (0, 1), (1, 0), (1, 1)],
    [(0, 0), (0, 2), (1, 1), (2, 0), (2, 2)],
    [(0, 0), (0, 1), (0, 2), (1, 1), (2, 0), (2, 1), (2, 2)],
]
_ASYM = [
    [(0, 0), (1, 0), (1, 1)],
    [(0, 0), (0, 1), (1, 0)],
    [(0, 0), (1, 0), (2, 0), (2, 1)],
    [(0, 0), (0, 1), (1, 1), (1, 2)],
    [(0, 0), (0, 1), (0, 2), (1, 0)],
]


def _free_box(g, r1, c1, r2, c2):
    h, w = len(g), len(g[0])
    if r1 < 1 or c1 < 1 or r2 >= h - 1 or c2 >= w - 1:
        if r1 < 0 or c1 < 0 or r2 >= h or c2 >= w:
            return False
    for r in range(max(0, r1 - 1), min(h, r2 + 2)):
        for c in range(max(0, c1 - 1), min(w, c2 + 2)):
            if g[r][c] != 0:
                return False
    return True


def _try_place(g, rng, shape, color, attempts=40):
    h, w = len(g), len(g[0])
    sh = max(r for r, _ in shape) + 1
    sw = max(c for _, c in shape) + 1
    for _ in range(attempts):
        r0 = rng.randint(0, h - sh)
        c0 = rng.randint(0, w - sw)
        if not _free_box(g, r0, c0, r0 + sh - 1, c0 + sw - 1):
            continue
        for dr, dc in shape:
            g[r0 + dr][c0 + dc] = color
        return True
    return False


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 11, 12)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 11, 12)
        w = ctx.draw_int("grid_w", 13, 14)
    else:
        h = ctx.draw_int("grid_h", 9, 12)
        w = ctx.draw_int("grid_w", 11, 14)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    n_asym = rng.randint(1, 2)
    palette = rng.sample([1, 2, 3, 4, 6, 7, 8, 9], 1 + n_asym)
    sym_color = palette[0]
    asym_colors = palette[1:]
    _try_place(g, rng, rng.choice(_SYMMETRIC), sym_color)
    for ac in asym_colors:
        _try_place(g, rng, rng.choice(_ASYM), ac)
    return g


def _draw_from_degenerate(name, rng):
    h, w = 10, 12
    g = full_grid(h, w, 0)
    if name == "no_components":
        return g
    if name == "all_symmetric":
        # Every component is bisymmetric — "exactly one" precondition fails.
        for dr, dc in [(0, 0), (0, 1), (1, 0), (1, 1)]:
            g[1 + dr][1 + dc] = 1
        for dr, dc in [(0, 0), (0, 1), (1, 0), (1, 1)]:
            g[5 + dr][7 + dc] = 2
        return g
    if name == "all_asymmetric":
        # No component is bisymmetric — selector returns nothing.
        for dr, dc in [(0, 0), (1, 0), (1, 1)]:
            g[1 + dr][1 + dc] = 1
        for dr, dc in [(0, 0), (0, 1), (1, 0)]:
            g[5 + dr][7 + dc] = 2
        return g
    return g
