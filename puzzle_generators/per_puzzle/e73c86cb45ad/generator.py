"""Generator for 17b:m117 — select rotation match and recolor.

Rule: target color at (0, w-1). The largest color-1 shape is the
reference. Among other shapes, find one rotation-equivalent to the
reference. Output: that shape cropped, recolored to target.

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: no_target (cell (0, w-1) is bg → rule has no recolor
target); no_reference (no color-1 shape → rule has no reference);
no_match (reference but no rotation-equivalent candidate → rule's
selector returns nothing).
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "e73c86cb45ad"
VERSION = "1.1.0"
TASK_ID = "e73c86cb45ad"
SUMMARY = "Target color at (0, w-1) + color-1 ref + 2-3 other shapes (one rotation-match)."

INVARIANTS = [
    "background is 0",
    "cell (0, w-1) is the target color",
    "exactly one color-1 reference shape",
    "2-3 other shapes; exactly one is rotation-equivalent to the reference",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_target", "no_reference", "no_match")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":            {"type": "int", "default": "rng 11..13", "valid": "10..16"},
    "grid_w":            {"type": "int", "default": "rng 12..14", "valid": "11..16"},
    "palette_kind":      {"type": "str", "default": "rng helpful",
                          "valid": "|".join(PALETTE_KINDS)},
    "palette_size":      {"type": "int", "default": "rng 4..4", "valid": "4..4"},
    "position_bias":     {"type": "str", "default": "target_corner_plus_ref_and_candidates",
                          "valid": "target_corner_plus_ref_and_candidates"},
    "n_distinct_colors": {"type": "int", "default": "rng 4..4", "valid": "4..4"},
    "density":           {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":           {"type": "str", "default": "alias for palette_kind",
                          "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def _free(g, r1, c1, r2, c2):
    h, w = len(g), len(g[0])
    if r1 < 0 or c1 < 0 or r2 >= h or c2 >= w: return False
    for r in range(max(0, r1 - 1), min(h, r2 + 2)):
        for c in range(max(0, c1 - 1), min(w, c2 + 2)):
            if g[r][c] != 0: return False
    return True


def _place(g, rng, shape, color):
    h, w = len(g), len(g[0])
    sh = max(r for r, _ in shape) + 1
    sw = max(c for _, c in shape) + 1
    for _ in range(40):
        r0 = rng.randint(1, h - sh); c0 = rng.randint(0, w - sw - 1)
        if not _free(g, r0, c0, r0 + sh - 1, c0 + sw - 1): continue
        for dr, dc in shape:
            g[r0 + dr][c0 + dc] = color
        return True
    return False


def _rotate_cw(shape):
    rs = [r for r, _ in shape]
    h = max(rs) + 1
    return sorted([(c, h - 1 - r) for r, c in shape])


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 11, 12)
        w = ctx.draw_int("grid_w", 12, 13)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 12, 13)
        w = ctx.draw_int("grid_w", 13, 14)
    else:
        h = ctx.draw_int("grid_h", 11, 13)
        w = ctx.draw_int("grid_w", 12, 14)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    target_color = rng.choice([2, 3, 4, 5, 6, 7, 8, 9])
    g[0][w - 1] = target_color
    base_shapes = [
        [(0, 0), (0, 1), (1, 0)],
        [(0, 0), (1, 0), (1, 1), (2, 1)],
        [(0, 0), (0, 1), (0, 2), (1, 1)],
        [(0, 0), (0, 1), (1, 0), (1, 1)],
    ]
    base = rng.choice(base_shapes)
    rotated = base
    for _ in range(rng.randint(1, 3)):
        rotated = _rotate_cw(rotated)
    other = rng.choice([s for s in base_shapes if s != base])
    _place(g, rng, base, 1)
    other_color = rng.choice([c for c in [2, 3, 4, 5, 6, 7, 8, 9] if c != target_color])
    _place(g, rng, rotated, other_color)
    other_color2 = rng.choice([c for c in [2, 3, 4, 5, 6, 7, 8, 9] if c not in (target_color, other_color)])
    _place(g, rng, other, other_color2)
    return g


def _draw_from_degenerate(name, rng):
    h, w = 12, 13
    g = full_grid(h, w, 0)
    if name == "no_target":
        # Cell (0, w-1) is bg — rule has no recolor target.
        for dr, dc in [(0, 0), (0, 1), (1, 0)]:
            g[3 + dr][3 + dc] = 1
        for dr, dc in [(0, 1), (1, 0), (1, 1)]:
            g[7 + dr][7 + dc] = 4
        return g
    if name == "no_reference":
        # Target + candidates but no color-1 reference.
        g[0][w - 1] = 6
        for dr, dc in [(0, 0), (0, 1), (1, 0)]:
            g[3 + dr][3 + dc] = 4
        for dr, dc in [(0, 0), (0, 1), (1, 0), (1, 1)]:
            g[7 + dr][7 + dc] = 5
        return g
    if name == "no_match":
        # Reference is L-tromino but candidates are 2x2 squares (different class).
        g[0][w - 1] = 6
        for dr, dc in [(0, 0), (0, 1), (1, 0)]:
            g[3 + dr][3 + dc] = 1
        for dr, dc in [(0, 0), (0, 1), (1, 0), (1, 1)]:
            g[7 + dr][3 + dc] = 4
        for dr, dc in [(0, 0), (0, 1), (1, 0), (1, 1)]:
            g[7 + dr][8 + dc] = 5
        return g
    return g
