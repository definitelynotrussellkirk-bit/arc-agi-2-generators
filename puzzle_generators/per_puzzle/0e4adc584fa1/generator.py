"""Generator for 11b:m73 — rotate source by control color.

Rule: cells with no 4-neighbor are 'isolated'; the LAST isolated
(scan-order) provides a transform code via its color. The main shape
(all other non-bg cells) is cropped to its bbox and transformed.

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: no_control (no isolated single-cell marker → rule's
control selector returns nothing, transform undefined), no_shape
(control marker present but no multi-cell shape → rule has nothing
to transform), identity_control (control color = identity-equivalent
code → rule's transform produces no change).
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "0e4adc584fa1"
VERSION = "1.1.0"
TASK_ID = "0e4adc584fa1"

SUMMARY = "1 multi-cell shape + 1 isolated single-cell control marker."

INVARIANTS = [
    "background is 0",
    "exactly one isolated single-cell control marker (no 4-neighbor)",
    "exactly one multi-cell shape elsewhere; isolated from the marker",
    "control color is in {1..7}",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_control", "no_shape", "identity_control")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":            {"type": "int", "default": "rng 8..10", "valid": "7..14"},
    "grid_w":            {"type": "int", "default": "rng 9..11", "valid": "8..14"},
    "palette_kind":      {"type": "str", "default": "rng helpful",
                          "valid": "|".join(PALETTE_KINDS)},
    "palette_size":      {"type": "int", "default": "rng 2..2", "valid": "2..2"},
    "position_bias":     {"type": "str", "default": "shape_plus_control_marker",
                          "valid": "shape_plus_control_marker"},
    "n_distinct_colors": {"type": "int", "default": "rng 2..2", "valid": "2..2"},
    "density":           {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":           {"type": "str", "default": "alias for palette_kind",
                          "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


_ASYM_SHAPES = [
    [(0, 0), (1, 0), (2, 0), (2, 1)],
    [(0, 0), (0, 1), (1, 0)],
    [(0, 0), (1, 0), (1, 1), (2, 1)],
    [(0, 0), (0, 1), (0, 2), (1, 0)],
]


def _free(g, r1, c1, r2, c2):
    h, w = len(g), len(g[0])
    if r1 < 0 or c1 < 0 or r2 >= h or c2 >= w: return False
    for r in range(max(0, r1 - 1), min(h, r2 + 2)):
        for c in range(max(0, c1 - 1), min(w, c2 + 2)):
            if g[r][c] != 0: return False
    return True


def _too_close(g, r, c) -> bool:
    h, w = len(g), len(g[0])
    for dr in (-1, 0, 1):
        for dc in (-1, 0, 1):
            rr, cc = r + dr, c + dc
            if 0 <= rr < h and 0 <= cc < w and g[rr][cc] != 0:
                return True
    return False


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
        h = ctx.draw_int("grid_h", 10, 10)
        w = ctx.draw_int("grid_w", 11, 11)
    else:
        h = ctx.draw_int("grid_h", 8, 10)
        w = ctx.draw_int("grid_w", 9, 11)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    palette = rng.sample([2, 3, 4, 5, 6, 7, 8, 9], 2)
    shape_color, control_color = palette
    control_code = rng.randint(1, 5)
    shape = rng.choice(_ASYM_SHAPES)
    sh = max(r for r, _ in shape) + 1
    sw = max(c for _, c in shape) + 1
    placed = False
    for _ in range(40):
        r0 = rng.randint(0, h - sh); c0 = rng.randint(0, w - sw)
        if not _free(g, r0, c0, r0 + sh - 1, c0 + sw - 1): continue
        for dr, dc in shape:
            g[r0 + dr][c0 + dc] = shape_color
        placed = True; break
    if not placed:
        raise ValueError("could not place main shape")
    for _ in range(60):
        r = rng.randint(0, h - 1); c = rng.randint(0, w - 1)
        if g[r][c] != 0 or _too_close(g, r, c):
            continue
        g[r][c] = control_code
        return g
    raise ValueError("could not place isolated control marker")


def _draw_from_degenerate(name, rng):
    h, w = 9, 10
    g = full_grid(h, w, 0)
    if name == "no_control":
        # No isolated single-cell — rule's control selector finds nothing.
        for dr, dc in [(0, 0), (1, 0), (1, 1), (2, 1)]:
            g[2 + dr][2 + dc] = 4
        return g
    if name == "no_shape":
        # Control marker present but no multi-cell shape — rule has
        # nothing to transform.
        g[5][5] = 3
        return g
    if name == "identity_control":
        # Control marker color encodes identity transform — output =
        # cropped input with no transformation.
        for dr, dc in [(0, 0), (1, 0), (1, 1), (2, 1)]:
            g[2 + dr][2 + dc] = 4
        g[7][7] = 1   # identity-equivalent code
        return g
    return g
