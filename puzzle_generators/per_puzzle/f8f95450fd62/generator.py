"""Generator for arc_puzzle_bank_21_set19_s:S19_E7.

Combinatorial axes (8): panel_h, panel_w, palette_kind, candidate_count,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_divider, no_match, multiple_matches.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid
from puzzle_generators.helpers.panels import assemble_vertical_panels

GENERATOR_ID = "f8f95450fd62"
VERSION = "1.1.0"
TASK_ID = "f8f95450fd62"
SUMMARY = "A key color selects the first candidate panel with the same leading color."

INVARIANTS = [
    "vertical panels are separated by color 9",
    "the first panel contains the key color",
    "exactly one candidate panel starts with the key color",
    "the matching candidate is recolored to 8",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_divider", "no_match", "multiple_matches")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "panel_h":        {"type": "int", "default": "rng 5..6", "valid": "4..10"},
    "panel_w":        {"type": "int", "default": "rng 5..6", "valid": "4..10"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "candidate_count":{"type": "int", "default": "rng 3..4", "valid": "2..4"},
    "palette_size":   {"type": "int", "default": "rng 4..6", "valid": "2..7"},
    "position_bias":  {"type": "str", "default": "key_plus_candidates",
                       "valid": "key_plus_candidates"},
    "n_distinct_colors": {"type": "int", "default": "rng 4..6", "valid": "2..7"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def _panel(h: int, w: int, color: int, cells: list[tuple[int, int]]):
    panel = full_grid(h, w, 0)
    for r, c in cells:
        panel[r][c] = color
    return panel


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index, version=VERSION,
                  task_id=TASK_ID, difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("panel_h", 5, 5)
        w = ctx.draw_int("panel_w", 5, 5)
        n = ctx.draw_int("candidate_count", 2, 3)
    elif difficulty == "hard":
        h = ctx.draw_int("panel_h", 6, 6)
        w = ctx.draw_int("panel_w", 6, 6)
        n = ctx.draw_int("candidate_count", 4, 4)
    else:
        h = ctx.draw_int("panel_h", 5, 6)
        w = ctx.draw_int("panel_w", 5, 6)
        n = ctx.draw_int("candidate_count", 3, 4)
    rng = ctx.draw_rng("layout")
    key_color = ctx.draw_choice("key_color", [2, 3, 4, 5, 6, 7, 8])
    key = full_grid(h, 2, 0)
    key[1][1] = key_color
    match_idx = ctx.draw_int("match_index", 0, n - 1)
    other_colors = [c for c in [2, 3, 4, 5, 6, 7, 8] if c != key_color]
    rng.shuffle(other_colors)
    candidates = []
    for idx in range(n):
        cells = [(1, 1), (h - 2, w - 2), (h // 2, w // 2)]
        color = key_color if idx == match_idx else other_colors[idx]
        candidates.append(_panel(h, w, color, cells))
    return assemble_vertical_panels([key] + candidates)


def _draw_from_degenerate(name, rng):
    h, w = 5, 5
    if name == "no_divider":
        # candidates concatenated without color-9 dividers → no panel boundary
        g = full_grid(h, 2 + w * 3, 0)
        g[1][1] = 4
        for i in range(3):
            base = 2 + i * w
            color = [4, 6, 7][i]
            g[1][base + 1] = color
        return g
    if name == "no_match":
        # no candidate has the key color → nothing to recolor
        key = full_grid(h, 2, 0); key[1][1] = 4
        candidates = []
        for color in [6, 7, 3]:
            p = full_grid(h, w, 0); p[1][1] = color
            candidates.append(p)
        return assemble_vertical_panels([key] + candidates)
    if name == "multiple_matches":
        # multiple candidates start with key color → ambiguous selection
        key = full_grid(h, 2, 0); key[1][1] = 4
        candidates = []
        for color in [4, 4, 6]:
            p = full_grid(h, w, 0); p[1][1] = color
            candidates.append(p)
        return assemble_vertical_panels([key] + candidates)
    return full_grid(h, w, 0)
