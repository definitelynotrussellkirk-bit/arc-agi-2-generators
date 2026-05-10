"""Generator for 19b:m133 — select vertically-symmetric object and crop.

Rule: among the connected components, pick the first whose normalized
binary mask is left-right (vertical-axis) mirror-symmetric. Output is
that component cropped, recolored to 8.

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: no_components (no shapes → rule has nothing to crop);
all_symmetric (every component is LR-symmetric → "exactly one"
precondition fails); all_asymmetric (no component is LR-symmetric
→ selector returns nothing).
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "92227d482198"
VERSION = "1.1.0"
TASK_ID = "92227d482198"

SUMMARY = "2-3 components; exactly one is LR-mirror symmetric."

INVARIANTS = [
    "background is 0",
    "2-3 isolated 4-connected components in distinct colors",
    "exactly one bbox-normalized binary shape is LR-mirror symmetric",
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
    "position_bias":     {"type": "str", "default": "lr_symmetric_plus_asymmetric",
                          "valid": "lr_symmetric_plus_asymmetric"},
    "n_distinct_colors": {"type": "int", "default": "rng 2..3", "valid": "2..3"},
    "density":           {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":           {"type": "str", "default": "alias for palette_kind",
                          "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


_LR_SYM = [
    [(0, 0), (0, 1), (0, 2), (1, 1), (2, 1)],
    [(0, 1), (1, 0), (1, 1), (1, 2), (2, 1)],
    [(0, 0), (0, 2), (1, 0), (1, 1), (1, 2), (2, 0), (2, 2)],
    [(0, 0), (0, 1), (0, 2), (0, 3), (1, 0), (1, 3), (2, 0), (2, 3)],
]
_ASYM = [
    [(0, 0), (1, 0), (1, 1)],
    [(0, 0), (0, 1), (1, 0)],
    [(0, 0), (1, 0), (2, 0), (2, 1)],
    [(0, 0), (0, 1), (0, 2), (1, 0)],
    [(0, 0), (0, 1), (1, 1), (2, 1)],
]


def _free(g, r1, c1, r2, c2):
    h, w = len(g), len(g[0])
    if r1 < 0 or c1 < 0 or r2 >= h or c2 >= w: return False
    for r in range(max(0, r1 - 1), min(h, r2 + 2)):
        for c in range(max(0, c1 - 1), min(w, c2 + 2)):
            if g[r][c] != 0: return False
    return True


def _place_or_raise(g, rng, shape, color, label):
    h, w = len(g), len(g[0])
    sh = max(r for r, _ in shape) + 1
    sw = max(c for _, c in shape) + 1
    for _ in range(60):
        r0 = rng.randint(0, h - sh); c0 = rng.randint(0, w - sw)
        if not _free(g, r0, c0, r0 + sh - 1, c0 + sw - 1): continue
        for dr, dc in shape:
            g[r0 + dr][c0 + dc] = color
        return
    raise ValueError(f"could not place {label} shape after 60 attempts")


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
    _place_or_raise(g, rng, rng.choice(_LR_SYM), palette[0], "symmetric")
    for color in palette[1:]:
        _place_or_raise(g, rng, rng.choice(_ASYM), color, "asymmetric")
    return g


def _draw_from_degenerate(name, rng):
    h, w = 10, 12
    g = full_grid(h, w, 0)
    if name == "no_components":
        return g
    if name == "all_symmetric":
        # Every component is LR-symmetric — "exactly one" precondition fails.
        for dr, dc in [(0, 0), (0, 1), (0, 2), (1, 1), (2, 1)]:
            g[1 + dr][1 + dc] = 1
        for dr, dc in [(0, 1), (1, 0), (1, 1), (1, 2), (2, 1)]:
            g[5 + dr][6 + dc] = 2
        return g
    if name == "all_asymmetric":
        # No component is LR-symmetric — selector returns nothing.
        for dr, dc in [(0, 0), (1, 0), (1, 1)]:
            g[1 + dr][1 + dc] = 1
        for dr, dc in [(0, 0), (0, 1), (1, 0)]:
            g[5 + dr][7 + dc] = 2
        return g
    return g
