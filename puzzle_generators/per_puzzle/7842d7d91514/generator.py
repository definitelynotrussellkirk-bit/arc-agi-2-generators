"""Generator for round3_md:find_the_candidate_matching_the_template — 5-template + 2-candidates; match → 4, else 1.

Rule: 5-shape is template. For each 2-shape, if normalized shape
matches template → recolor to 4, else → 1.

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: no_template, no_candidates, all_match.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, paint_at

GENERATOR_ID = "7842d7d91514"
VERSION = "1.1.0"
TASK_ID = "7842d7d91514"
SUMMARY = "1 5-template shape + 2 candidate 2-shapes (1 matching, 1 not)."

INVARIANTS = [
    "exactly 1 5-shape (template)",
    "≥2 2-shapes, ≥1 matches template's normalized shape",
    "≥1 2-shape doesn't match",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_template", "no_candidates", "all_match")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 6..8", "valid": "5..12"},
    "grid_w":         {"type": "int", "default": "rng 11..13", "valid": "9..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "palette_size":   {"type": "int", "default": "2", "valid": "2..2"},
    "position_bias":  {"type": "str", "default": "template_left_candidates_right",
                       "valid": "template_left_candidates_right"},
    "n_distinct_colors": {"type": "int", "default": "2", "valid": "2..2"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}



def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 6, 6)
        w = ctx.draw_int("grid_w", 11, 11)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 8, 10)
        w = ctx.draw_int("grid_w", 13, 15)
    else:
        h = ctx.draw_int("grid_h", 6, 8)
        w = ctx.draw_int("grid_w", 11, 13)
    g = full_grid(h, w, 0)
    rng = ctx.draw_rng("layout")
    template = rng.choice([
        [(0, 0), (1, 0), (1, 1)],
        [(0, 0), (0, 1), (1, 0)],
        [(0, 0), (0, 1), (1, 1), (2, 1)],
    ])
    different = rng.choice([
        [(0, 0), (0, 1), (0, 2)],
        [(0, 0), (1, 0), (1, 1), (1, 2)],
    ])
    while sorted(different) == sorted(template):
        different = rng.choice([
            [(0, 0), (0, 1), (0, 2)],
            [(0, 0), (1, 0), (1, 1), (1, 2)],
        ])
    paint_at(g, rng.randint(0, 1), rng.randint(0, 2), template, 5)
    paint_at(g, rng.randint(0, 1), rng.randint(5, 7), template, 2)
    paint_at(g, rng.randint(h - 4, h - 3), rng.randint(7, 9), different, 2)
    for _ in range(rng.randint(1, 2)):
        for _ in range(20):
            r = rng.randint(0, h - 1); c = rng.randint(0, w - 1)
            if g[r][c] == 0:
                g[r][c] = rng.choice([3, 4, 6, 7, 8, 9])
                break
    return g


def _draw_from_degenerate(name, rng):
    h, w = 7, 12
    g = full_grid(h, w, 0)
    template = [(0, 0), (1, 0), (1, 1)]
    different = [(0, 0), (0, 1), (0, 2)]
    if name == "no_template":
        # Candidate 2-shapes but no 5-template — rule has no reference
        # shape to compare against.
        paint_at(g, 1, 5, template, 2)
        paint_at(g, 4, 8, different, 2)
        return g
    if name == "no_candidates":
        # 5-template but no 2-candidates — rule has nothing to recolor.
        paint_at(g, 1, 1, template, 5)
        return g
    if name == "all_match":
        # All candidates have the same shape as the template — rule's
        # branch for "doesn't match" never fires; output uses only
        # color 4.
        paint_at(g, 1, 1, template, 5)
        paint_at(g, 1, 5, template, 2)
        paint_at(g, 4, 8, template, 2)
        return g
    return g
