"""Generator for 3b:hard_17 — center template inside every frame.

Rule: template = color-2 component. For each non-color-2 connected
component (treated as a frame), output center-places the template
inside the component's bbox, painted in the frame's color.

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: no_template (no color-2 component → rule's template
selector returns nothing), no_frames (template present but no
non-color-2 frames → rule has no targets to center inside),
template_too_large (template's bbox doesn't fit inside any frame
interior → rule's center-place produces no visible change).
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "bf5bed969a6d"
VERSION = "1.1.0"
TASK_ID = "bf5bed969a6d"

SUMMARY = "1 color-2 template + 2-3 hollow rectangular frames in distinct non-2 colors."

INVARIANTS = [
    "background is 0",
    "exactly one color-2 multi-cell template (3-4 cells)",
    "2-3 hollow rectangular frames in distinct non-{0,2} colors",
    "each frame's interior is large enough to fit the template (≥ 2 cells in each dim larger than template)",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_template", "no_frames", "template_too_large")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":            {"type": "int", "default": "rng 13..16", "valid": "12..20"},
    "grid_w":            {"type": "int", "default": "rng 14..17", "valid": "13..22"},
    "palette_kind":      {"type": "str", "default": "rng helpful",
                          "valid": "|".join(PALETTE_KINDS)},
    "palette_size":      {"type": "int", "default": "rng 3..4", "valid": "2..5"},
    "position_bias":     {"type": "str", "default": "template_plus_frames",
                          "valid": "template_plus_frames"},
    "n_distinct_colors": {"type": "int", "default": "rng 3..4", "valid": "2..5"},
    "density":           {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":           {"type": "str", "default": "alias for palette_kind",
                          "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


_SHAPES = [
    [(0, 0), (0, 1), (1, 0)],
    [(0, 0), (1, 0), (1, 1)],
    [(0, 0), (0, 1), (0, 2), (1, 1)],
]


def _free(g, r1, c1, r2, c2):
    h, w = len(g), len(g[0])
    if r1 < 0 or c1 < 0 or r2 >= h or c2 >= w: return False
    for r in range(max(0, r1 - 1), min(h, r2 + 2)):
        for c in range(max(0, c1 - 1), min(w, c2 + 2)):
            if g[r][c] != 0: return False
    return True


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 13, 14)
        w = ctx.draw_int("grid_w", 14, 15)
        n_lo, n_hi = 2, 2
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 15, 16)
        w = ctx.draw_int("grid_w", 16, 17)
        n_lo, n_hi = 3, 3
    else:
        h = ctx.draw_int("grid_h", 13, 16)
        w = ctx.draw_int("grid_w", 14, 17)
        n_lo, n_hi = 2, 3
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    template = rng.choice(_SHAPES)
    th = max(r for r, _ in template) + 1
    tw = max(c for _, c in template) + 1
    placed_t = False
    for _ in range(40):
        r0 = rng.randint(0, h - th); c0 = rng.randint(0, w - tw)
        if not _free(g, r0, c0, r0 + th - 1, c0 + tw - 1): continue
        for dr, dc in template:
            g[r0 + dr][c0 + dc] = 2
        placed_t = True; break
    if not placed_t:
        raise ValueError("could not place template")
    n_frames = rng.randint(n_lo, n_hi)
    palette = rng.sample([1, 3, 4, 5, 6, 7, 8, 9], n_frames)
    for color in palette:
        for _ in range(60):
            fh = rng.randint(th + 4, th + 5); fw = rng.randint(tw + 4, tw + 5)
            r0 = rng.randint(0, h - fh); c0 = rng.randint(0, w - fw)
            if not _free(g, r0, c0, r0 + fh - 1, c0 + fw - 1): continue
            for c in range(c0, c0 + fw): g[r0][c] = color; g[r0 + fh - 1][c] = color
            for r in range(r0, r0 + fh): g[r][c0] = color; g[r][c0 + fw - 1] = color
            break
    return g


def _draw_from_degenerate(name, rng):
    h, w = 14, 15
    g = full_grid(h, w, 0)
    if name == "no_template":
        # No color-2 — rule's template selector returns nothing.
        for c in range(2, 7): g[2][c] = 4; g[6][c] = 4
        for r in range(2, 7): g[r][2] = 4; g[r][6] = 4
        for c in range(8, 13): g[8][c] = 6; g[12][c] = 6
        for r in range(8, 13): g[r][8] = 6; g[r][12] = 6
        return g
    if name == "no_frames":
        # Template present but no frames — rule has no targets.
        for dr, dc in [(0, 0), (0, 1), (1, 0)]:
            g[3 + dr][3 + dc] = 2
        return g
    if name == "template_too_large":
        # Template bbox larger than frame interior — center-place is
        # undefined / produces no visible change.
        for dr, dc in [(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2),
                       (2, 0), (2, 1), (2, 2)]:
            g[2 + dr][2 + dc] = 2
        # Tiny 4x4 frame
        for c in range(8, 12): g[8][c] = 4; g[11][c] = 4
        for r in range(8, 12): g[r][8] = 4; g[r][11] = 4
        return g
    return g
