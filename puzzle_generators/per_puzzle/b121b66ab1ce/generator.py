"""Generator for next_b:m11 — keep shape matching template.

Rule: a color-1 template shape; among color-3 shapes, keep those
whose normalized binary mask exactly matches the template; recolor
those to 8.

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: no_template, no_match, all_match.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "b121b66ab1ce"
VERSION = "1.1.0"
TASK_ID = "b121b66ab1ce"

SUMMARY = "1 color-1 template + 1-2 color-3 shapes (one matching, others not)."

INVARIANTS = [
    "background is 0",
    "exactly one color-1 template shape",
    "1-2 color-3 shapes; exactly one's normalized cells match the template's",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_template", "no_match", "all_match")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 9..11", "valid": "8..14"},
    "grid_w":         {"type": "int", "default": "rng 10..12", "valid": "9..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "palette_size":   {"type": "int", "default": "2", "valid": "2..2"},
    "position_bias":  {"type": "str", "default": "template_with_candidates",
                       "valid": "template_with_candidates"},
    "n_distinct_colors": {"type": "int", "default": "2", "valid": "2..2"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


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
    raise ValueError(f"could not place {label}")


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 9, 9)
        w = ctx.draw_int("grid_w", 10, 10)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 11, 13)
        w = ctx.draw_int("grid_w", 12, 14)
    else:
        h = ctx.draw_int("grid_h", 9, 11)
        w = ctx.draw_int("grid_w", 10, 12)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    base_shapes = [
        [(0, 0), (0, 1), (1, 1), (1, 2)],
        [(0, 0), (1, 0), (1, 1), (2, 1)],
        [(0, 0), (0, 1), (0, 2), (1, 1)],
        [(0, 0), (1, 0), (1, 1)],
    ]
    template = rng.choice(base_shapes)
    other = rng.choice([s for s in base_shapes if s != template])
    _place_or_raise(g, rng, template, 1, "template (color 1)")
    _place_or_raise(g, rng, template, 3, "matching color-3 shape")
    if rng.random() < 0.7:
        _place_or_raise(g, rng, other, 3, "different color-3 shape")
    return g


def _draw_from_degenerate(name, rng):
    h, w = 10, 11
    g = full_grid(h, w, 0)
    if name == "no_template":
        # Color-3 shapes but no color-1 template — rule's match
        # criterion has no reference; keep branch never fires.
        for r, c in [(2, 2), (2, 3), (3, 3), (3, 4)]: g[r][c] = 3
        for r, c in [(7, 7), (8, 7), (8, 8)]: g[r][c] = 3
        return g
    if name == "no_match":
        # Template + only non-matching color-3 shapes — rule's
        # keep branch finds no matches; output erases everything.
        for r, c in [(1, 1), (1, 2), (2, 2), (2, 3)]: g[r][c] = 1
        for r, c in [(6, 6), (7, 6), (7, 7)]: g[r][c] = 3
        return g
    if name == "all_match":
        # Template + only matching color-3 shapes — rule's keep
        # branch keeps all; rule's discrimination invisible.
        for r, c in [(1, 1), (1, 2), (2, 2), (2, 3)]: g[r][c] = 1
        for r, c in [(5, 5), (5, 6), (6, 6), (6, 7)]: g[r][c] = 3
        for r, c in [(7, 1), (7, 2), (8, 2), (8, 3)]: g[r][c] = 3
        return g
    return g
