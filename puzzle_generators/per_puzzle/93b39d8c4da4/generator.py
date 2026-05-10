"""Generator for 4b:hard_24 — stamp template at every mask cell.

Rule: template = color-2 cells (binary). For each color-3 cell (mask
position), stamp the template (recolored to 8) at that position.

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: no_template, no_marks, mark_oob.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "93b39d8c4da4"
VERSION = "1.1.0"
TASK_ID = "93b39d8c4da4"
SUMMARY = "Color-2 template + 2-4 color-3 mask cells."

INVARIANTS = [
    "background is 0",
    "exactly one connected color-2 template (3-5 cells)",
    "2-4 color-3 mask cells, isolated, not overlapping the template",
    "template stamped at each mask position fits in-bounds",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_template", "no_marks", "mark_oob")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 11..14", "valid": "10..18"},
    "grid_w":         {"type": "int", "default": "rng 12..14", "valid": "11..18"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "palette_size":   {"type": "int", "default": "2", "valid": "2..2"},
    "position_bias":  {"type": "str", "default": "template_with_marks",
                       "valid": "template_with_marks"},
    "n_distinct_colors": {"type": "int", "default": "2", "valid": "2..2"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


_TEMPLATES = [
    [(0, 0), (0, 1), (1, 0)],
    [(0, 0), (1, 0), (1, 1)],
    [(0, 0), (0, 1), (1, 1)],
    [(0, 0), (0, 1), (0, 2)],
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
        h = ctx.draw_int("grid_h", 11, 11)
        w = ctx.draw_int("grid_w", 12, 12)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 14, 17)
        w = ctx.draw_int("grid_w", 14, 17)
    else:
        h = ctx.draw_int("grid_h", 11, 14)
        w = ctx.draw_int("grid_w", 12, 14)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    template = rng.choice(_TEMPLATES)
    th = max(r for r, _ in template) + 1
    tw = max(c for _, c in template) + 1
    for _ in range(40):
        r0 = rng.randint(0, h - th); c0 = rng.randint(0, w - tw)
        if not _free(g, r0, c0, r0 + th - 1, c0 + tw - 1): continue
        for dr, dc in template:
            g[r0 + dr][c0 + dc] = 2
        break
    n_marks = rng.randint(2, 4)
    placed = 0; attempts = 0
    while placed < n_marks and attempts < 60:
        attempts += 1
        r = rng.randint(0, h - th); c = rng.randint(0, w - tw)
        if not _free(g, r, c, r + th - 1, c + tw - 1): continue
        g[r][c] = 3; placed += 1
    return g


def _draw_from_degenerate(name, rng):
    h, w = 12, 13
    g = full_grid(h, w, 0)
    if name == "no_template":
        # Marks but no template — rule's stamp source is undefined;
        # stamp branch never fires.
        g[3][3] = 3; g[7][8] = 3
        return g
    if name == "no_marks":
        # Template but no marks — rule has no stamp positions;
        # output equals input.
        for r, c in [(2, 2), (2, 3), (3, 2)]: g[r][c] = 2
        return g
    if name == "mark_oob":
        # Mark in bottom-right corner — stamping the template
        # there would extend OOB; rule's stamp clips/drops.
        for r, c in [(2, 2), (2, 3), (3, 2)]: g[r][c] = 2
        g[h - 1][w - 1] = 3
        return g
    return g
