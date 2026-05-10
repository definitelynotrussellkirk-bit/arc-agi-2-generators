"""Generator for arc_puzzle_bank_21_set20_s:S20_E5.

Combinatorial axes (8): panel_h, panel_w, palette_kind, candidate_count,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_template, no_hits, all_hits.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid
from puzzle_generators.helpers.panels import assemble_vertical_panels, paste

GENERATOR_ID = "4256bbb98042"
VERSION = "1.1.0"
TASK_ID = "4256bbb98042"
SUMMARY = "A strip flags candidate panels that contain the template."

INVARIANTS = [
    "divider color is 9",
    "first panel contains the template",
    "subsequent panels are candidates",
    "some candidates contain an exact template match",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_template", "no_hits", "all_hits")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "panel_h":        {"type": "int", "default": "rng 7..9", "valid": "5..14"},
    "panel_w":        {"type": "int", "default": "rng 5..7", "valid": "5..7"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "candidate_count": {"type": "int", "default": "rng 3..4", "valid": "2..4"},
    "palette_size":   {"type": "int", "default": "8", "valid": "8..8"},
    "position_bias":  {"type": "str", "default": "template_plus_candidates",
                       "valid": "template_plus_candidates"},
    "n_distinct_colors": {"type": "int", "default": "8", "valid": "8..8"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}

TEMPLATE = [[5, 6, 7], [8, 2, 3], [4, 5, 6]]


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index, version=VERSION,
                  task_id=TASK_ID, difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("panel_h", 7, 7)
        n = ctx.draw_int("candidate_count", 3, 3)
    elif difficulty == "hard":
        h = ctx.draw_int("panel_h", 8, 9)
        n = ctx.draw_int("candidate_count", 4, 4)
    else:
        h = ctx.draw_int("panel_h", 7, 9)
        n = ctx.draw_int("candidate_count", 3, 4)
    max_w = (30 - 5 - n) // n
    w = ctx.draw_int("panel_w", 5, max_w)
    rng = ctx.draw_rng("layout")
    template_panel = full_grid(h, 5, 0)
    paste(template_panel, TEMPLATE, 1, 1)
    hit_idxs = set(rng.sample(range(n), rng.randint(1, n - 1)))
    candidates = []
    for i in range(n):
        panel = full_grid(h, w, 0)
        if i in hit_idxs:
            paste(panel, TEMPLATE, rng.randint(0, h - 3), rng.randint(0, w - 3))
        else:
            panel[h // 2][w // 2] = rng.choice([1, 2, 3, 4, 5, 6, 7, 8])
        candidates.append(panel)
    return assemble_vertical_panels([template_panel] + candidates)


def _draw_from_degenerate(name, rng):
    h, w, n = 7, 5, 3
    if name == "no_template":
        # candidates without template → no pattern to flag matches against
        template_panel = full_grid(h, 5, 0)
        candidates = []
        for i in range(n):
            panel = full_grid(h, w, 0)
            paste(panel, TEMPLATE, 1, 1)
            candidates.append(panel)
        return assemble_vertical_panels([template_panel] + candidates)
    if name == "no_hits":
        # template present but no candidates contain it → "some hits" precondition fails
        template_panel = full_grid(h, 5, 0)
        paste(template_panel, TEMPLATE, 1, 1)
        candidates = [full_grid(h, w, 0) for _ in range(n)]
        for panel in candidates:
            panel[h // 2][w // 2] = 4
        return assemble_vertical_panels([template_panel] + candidates)
    if name == "all_hits":
        # all candidates match → no negative contrast (rule flags everything)
        template_panel = full_grid(h, 5, 0)
        paste(template_panel, TEMPLATE, 1, 1)
        candidates = []
        for i in range(n):
            panel = full_grid(h, w, 0)
            paste(panel, TEMPLATE, 1, 1)
            candidates.append(panel)
        return assemble_vertical_panels([template_panel] + candidates)
    return full_grid(h, w * (n + 1) + n, 0)
