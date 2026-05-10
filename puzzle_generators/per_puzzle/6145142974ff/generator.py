"""Generator for next_b:hard_14 — select shape match and recolor by majority singleton.

Rule: color-1 template; color-3 components matching template's
normalized shape get recolored to the majority non-{1,3} singleton
color (most-frequent — ties broken by larger color value).

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: no_template (no color-1 → rule's template selector
returns nothing), no_match (no color-3 component matches template →
rule's match selector finds nothing), no_singletons (no non-{1,3}
singletons → rule's majority-color is undefined).
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "6145142974ff"
VERSION = "1.1.0"
TASK_ID = "6145142974ff"

SUMMARY = "color-1 template + 1-2 matching color-3 shapes + scattered singleton cells with majority color."

INVARIANTS = [
    "background is 0",
    "exactly one color-1 multi-cell template",
    "1-2 color-3 components matching the template's normalized cells",
    "3-4 isolated single-cell markers in distinct non-{1,3} colors with one having strictly highest count (or use ties broken by max color)",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_template", "no_match", "no_singletons")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":            {"type": "int", "default": "rng 11..13", "valid": "10..16"},
    "grid_w":            {"type": "int", "default": "rng 13..15", "valid": "12..18"},
    "palette_kind":      {"type": "str", "default": "rng helpful",
                          "valid": "|".join(PALETTE_KINDS)},
    "palette_size":      {"type": "int", "default": "rng 4..5", "valid": "3..6"},
    "position_bias":     {"type": "str", "default": "template_match_singletons",
                          "valid": "template_match_singletons"},
    "n_distinct_colors": {"type": "int", "default": "rng 4..5", "valid": "3..6"},
    "density":           {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":           {"type": "str", "default": "alias for palette_kind",
                          "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


_SHAPES = [
    [(0, 0), (0, 1), (1, 0)],
    [(0, 0), (1, 0), (1, 1)],
    [(0, 0), (0, 1), (0, 2), (1, 1)],
    [(0, 0), (1, 0), (1, 1), (2, 1)],
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
    raise ValueError(f"could not place {label}")


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 11, 11)
        w = ctx.draw_int("grid_w", 13, 13)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 13, 13)
        w = ctx.draw_int("grid_w", 15, 15)
    else:
        h = ctx.draw_int("grid_h", 11, 13)
        w = ctx.draw_int("grid_w", 13, 15)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    template = rng.choice(_SHAPES)
    _place_or_raise(g, rng, template, 1, "template (color 1)")
    _place_or_raise(g, rng, template, 3, "matching color-3 shape")
    majority_color = rng.choice([2, 5, 6, 7, 8])
    other_colors = rng.sample([c for c in [2, 4, 5, 6, 7, 8, 9] if c != majority_color], 2)
    placement_plan = ([majority_color] * rng.randint(2, 3)) + other_colors
    for color in placement_plan:
        for _ in range(60):
            r = rng.randint(0, h - 1); c = rng.randint(0, w - 1)
            if g[r][c] != 0 or _too_close(g, r, c): continue
            g[r][c] = color; break
    return g


def _draw_from_degenerate(name, rng):
    h, w = 12, 14
    g = full_grid(h, w, 0)
    if name == "no_template":
        # No color-1 — rule's template selector returns nothing.
        for dr, dc in [(0, 0), (0, 1), (1, 0)]:
            g[2 + dr][2 + dc] = 3
        g[8][9] = 4
        g[9][2] = 5
        return g
    if name == "no_match":
        # Template present but no color-3 matching shape.
        for dr, dc in [(0, 0), (0, 1), (1, 0)]:
            g[2 + dr][2 + dc] = 1
        for dr, dc in [(0, 0), (0, 1), (0, 2)]:
            g[6 + dr][6 + dc] = 3   # H-line, doesn't match L
        g[8][2] = 4; g[9][9] = 5
        return g
    if name == "no_singletons":
        # No non-{1,3} singletons — rule's majority-color is undefined.
        for dr, dc in [(0, 0), (0, 1), (1, 0)]:
            g[2 + dr][2 + dc] = 1
        for dr, dc in [(0, 0), (0, 1), (1, 0)]:
            g[6 + dr][6 + dc] = 3
        return g
    return g
