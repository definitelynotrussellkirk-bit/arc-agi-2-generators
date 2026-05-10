"""Generator for arc_puzzle_bank_21_set17_s:S17_H5.

Top panels define color-labeled stencils around a local 9 anchor. Body cells
with those colors are expanded by the corresponding stencil offsets.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_entries,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_library, no_body, color_not_in_library.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "fdffdd0bbde7"
VERSION = "1.1.0"
TASK_ID = "fdffdd0bbde7"
SUMMARY = "Use top color-keyed stencil panels to stamp offsets at body cells."

INVARIANTS = [
    "top library panels are separated by full color-9 columns",
    "each panel has one color-9 anchor and one non-9 stencil color",
    "a blank row separates the library from the body",
    "each body cell color has a matching library entry",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_library", "no_body", "color_not_in_library")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "10", "valid": "10..10"},
    "grid_w":         {"type": "int", "default": "14", "valid": "14..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_entries":      {"type": "int", "default": "rng 2..3", "valid": "2..3"},
    "palette_size":   {"type": "int", "default": "rng 2..3", "valid": "2..3"},
    "position_bias":  {"type": "str", "default": "library_top_body_bottom",
                       "valid": "library_top_body_bottom"},
    "n_distinct_colors": {"type": "int", "default": "rng 2..3", "valid": "2..3"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}

_OFFSETS = [
    [(0, 1), (1, 0), (1, 1)],
    [(0, -1), (1, 0), (1, 1)],
    [(-1, 0), (0, 1), (1, 0)],
]


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(
        seed=seed,
        sample_index=sample_index,
        version=VERSION,
        task_id=TASK_ID,
        difficulty=difficulty,
        overrides=overrides,
    )
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    rng = ctx.draw_rng("layout")
    if difficulty == "easy":
        n_entries = ctx.draw_int("n_entries", 2, 2)
    elif difficulty == "hard":
        n_entries = ctx.draw_int("n_entries", 3, 3)
    else:
        n_entries = ctx.draw_int("n_entries", 2, 3)
    colors = rng.sample([2, 3, 4, 5, 6, 7, 8], n_entries)
    g = full_grid(10, 14, 0)

    for sep in [4, 9]:
        for r in range(3):
            g[r][sep] = 9
    anchors = [(1, 1), (1, 6), (1, 11)]
    for idx, color in enumerate(colors):
        ar, ac = anchors[idx]
        g[ar][ac] = 9
        for dr, dc in _OFFSETS[idx]:
            g[ar + dr][ac + dc] = color

    body_positions = [(5, 2), (6, 7), (8, 4), (7, 11)]
    rng.shuffle(body_positions)
    for idx, pos in enumerate(body_positions[: n_entries + 1]):
        g[pos[0]][pos[1]] = colors[idx % n_entries]
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(10, 14, 0)
    if name == "no_library":
        # body cells without library panels → no stencils to apply
        for r, c in [(5, 2), (6, 7), (8, 4)]: g[r][c] = 4
        return g
    if name == "no_body":
        # library only, no body cells → nothing to expand
        for sep in [4, 9]:
            for r in range(3):
                g[r][sep] = 9
        for (ar, ac), offsets in zip([(1, 1), (1, 6)], _OFFSETS[:2]):
            g[ar][ac] = 9
            for dr, dc in offsets:
                g[ar + dr][ac + dc] = 4
        return g
    if name == "color_not_in_library":
        # body uses color absent from library → no matching stencil
        for sep in [4, 9]:
            for r in range(3):
                g[r][sep] = 9
        for (ar, ac), offsets in zip([(1, 1)], [_OFFSETS[0]]):
            g[ar][ac] = 9
            for dr, dc in offsets:
                g[ar + dr][ac + dc] = 4
        # body uses color 7 — not in library
        for r, c in [(5, 2), (6, 7), (8, 4)]: g[r][c] = 7
        return g
    return g
