"""Generator for 19b:m130 — find exemplar match and recolor.

Rule: a 5x5 exemplar region at (0,0) holds a binary shape. Among the
other components, find the one whose normalized binary equals the
exemplar's. Output is that component cropped, recolored to 2.

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: no_exemplar (5x5 region empty → rule has no template);
no_match (exemplar present but no body component matches → selector
returns nothing); tied_match (two body components both match
exemplar → "exactly one" precondition fails).
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "6be2608558c4"
VERSION = "1.1.0"
TASK_ID = "6be2608558c4"
SUMMARY = "5x5 exemplar at (0,0) + 2-3 body components, one matching exemplar shape."

INVARIANTS = [
    "background is 0",
    "5x5 region at (0,0) contains the exemplar in some non-bg color",
    "2-3 body components elsewhere, distinct colors; exactly one has the same normalized binary shape as the exemplar",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_exemplar", "no_match", "tied_match")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":            {"type": "int", "default": "rng 11..13", "valid": "10..16"},
    "grid_w":            {"type": "int", "default": "rng 12..14", "valid": "11..16"},
    "palette_kind":      {"type": "str", "default": "rng helpful",
                          "valid": "|".join(PALETTE_KINDS)},
    "palette_size":      {"type": "int", "default": "rng 4..4", "valid": "4..4"},
    "position_bias":     {"type": "str", "default": "exemplar_at_corner_with_body_candidates",
                          "valid": "exemplar_at_corner_with_body_candidates"},
    "n_distinct_colors": {"type": "int", "default": "rng 4..4", "valid": "4..4"},
    "density":           {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":           {"type": "str", "default": "alias for palette_kind",
                          "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


_EXEMPLARS = [
    [(0, 0), (1, 0), (1, 1), (2, 1)],
    [(0, 0), (0, 1), (1, 0)],
    [(0, 0), (0, 1), (0, 2), (1, 1)],
    [(0, 0), (1, 0), (2, 0), (2, 1)],
]
_OTHERS = [
    [(0, 0), (0, 1), (1, 0), (1, 1)],
    [(0, 0), (1, 0), (1, 1)],
    [(0, 0), (0, 1), (0, 2)],
    [(0, 0), (1, 0)],
]


def _free(g, r1, c1, r2, c2):
    h, w = len(g), len(g[0])
    if r1 < 0 or c1 < 0 or r2 >= h or c2 >= w: return False
    for r in range(max(0, r1 - 1), min(h, r2 + 2)):
        for c in range(max(0, c1 - 1), min(w, c2 + 2)):
            if g[r][c] != 0: return False
    return True


def _place(g, rng, shape, color, r_min=0, c_min=0):
    h, w = len(g), len(g[0])
    sh = max(r for r, _ in shape) + 1
    sw = max(c for _, c in shape) + 1
    for _ in range(40):
        r0 = rng.randint(r_min, h - sh); c0 = rng.randint(c_min, w - sw)
        if not _free(g, r0, c0, r0 + sh - 1, c0 + sw - 1): continue
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
    palette = rng.sample([1, 3, 4, 5, 6, 7, 8, 9], 4)
    exemplar_color = palette[0]
    match_color = palette[1]
    other_colors = palette[2:]
    exemplar = rng.choice(_EXEMPLARS)
    sh = max(r for r, _ in exemplar) + 1
    sw = max(c for _, c in exemplar) + 1
    r0 = rng.randint(0, max(0, 4 - sh)); c0 = rng.randint(0, max(0, 4 - sw))
    for dr, dc in exemplar:
        g[r0 + dr][c0 + dc] = exemplar_color
    _place(g, rng, exemplar, match_color, r_min=6, c_min=0)
    for color in rng.sample(other_colors, rng.randint(1, 2)):
        _place(g, rng, rng.choice(_OTHERS), color, r_min=6, c_min=0)
    return g


def _draw_from_degenerate(name, rng):
    h, w = 12, 13
    g = full_grid(h, w, 0)
    if name == "no_exemplar":
        # 5x5 region empty — rule has no template.
        for dr, dc in [(0, 0), (0, 1), (1, 0), (1, 1)]:
            g[7 + dr][3 + dc] = 4
        for dr, dc in [(0, 0), (1, 0)]:
            g[8 + dr][9 + dc] = 5
        return g
    if name == "no_match":
        # Exemplar L-tromino but body candidates are 2x2 squares (different class).
        for dr, dc in [(0, 0), (0, 1), (1, 0)]:
            g[1 + dr][1 + dc] = 4
        for dr, dc in [(0, 0), (0, 1), (1, 0), (1, 1)]:
            g[7 + dr][3 + dc] = 5
        for dr, dc in [(0, 0), (0, 1), (1, 0), (1, 1)]:
            g[7 + dr][9 + dc] = 6
        return g
    if name == "tied_match":
        # Two body components match exemplar — selector ambiguous.
        for dr, dc in [(0, 0), (0, 1), (1, 0)]:
            g[1 + dr][1 + dc] = 4
        for dr, dc in [(0, 0), (0, 1), (1, 0)]:
            g[7 + dr][3 + dc] = 5
        for dr, dc in [(0, 0), (0, 1), (1, 0)]:
            g[7 + dr][9 + dc] = 6
        return g
    return g
