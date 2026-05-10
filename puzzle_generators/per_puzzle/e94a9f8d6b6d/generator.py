"""Generator for arc_puzzle_bank_21_set22_s:S22_H6 — source-frame motif to target-frame motif lookup.

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: no_query (no third source/target frame → no query slot);
identical_keys (both training keys identical → no contrast for lookup);
blank_targets (source frames present but target frames empty → no
mapping defined).
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "e94a9f8d6b6d"
VERSION = "1.1.0"
TASK_ID = "e94a9f8d6b6d"
SUMMARY = "Learn a source-frame motif to target-frame motif mapping and fill the blank query target."

INVARIANTS = [
    "there are three source frames with marker colors 2, 3, and 4",
    "there are three target frames with marker colors 5, 6, and 7",
    "the first two source/target pairs define the lookup table",
    "the third source repeats one key and the third target starts blank",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_query", "identical_keys", "blank_targets")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "query_key":         {"type": "int", "default": "rng 0..1", "valid": "0..1"},
    "variant":           {"type": "int", "default": "rng 0..3", "valid": "0..3"},
    "palette_kind":      {"type": "str", "default": "rng helpful",
                          "valid": "|".join(PALETTE_KINDS)},
    "palette_size":      {"type": "int", "default": "rng 6..6", "valid": "6..6"},
    "position_bias":     {"type": "str", "default": "fixed_3x3_grid",
                          "valid": "fixed_3x3_grid"},
    "n_distinct_colors": {"type": "int", "default": "rng 6..6", "valid": "6..6"},
    "density":           {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":           {"type": "str", "default": "alias for palette_kind",
                          "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}

_KEY_SETS = [
    (
        [(1, -1), (2, -1), (2, 0)],
        [(-1, 1), (-1, 2), (0, 2)],
    ),
    (
        [(1, -2), (2, -2), (2, -1)],
        [(-1, 2), (0, 2), (1, 2)],
    ),
    (
        [(2, 0), (2, 1), (1, 1)],
        [(-2, 0), (-2, 1), (-1, 1)],
    ),
    (
        [(1, -1), (1, -2), (2, -2)],
        [(-1, 1), (-2, 1), (-2, 2)],
    ),
]
_VALUE_SETS = [
    (
        [((1, 1), 8), ((1, 2), 9), ((2, 2), 8)],
        [((-1, -1), 9), ((-2, -1), 8), ((-2, 0), 9)],
    ),
    (
        [((1, 1), 9), ((2, 1), 8), ((2, 2), 9)],
        [((-1, -1), 8), ((-1, -2), 9), ((0, -2), 8)],
    ),
    (
        [((1, 2), 8), ((2, 1), 9), ((2, 2), 8)],
        [((-2, 0), 9), ((-2, -1), 8), ((-1, -1), 9)],
    ),
    (
        [((0, 2), 8), ((1, 2), 9), ((2, 1), 8)],
        [((-1, 2), 9), ((-2, 1), 8), ((-2, 2), 9)],
    ),
]


def _frame(g, origin, colors):
    r, c = origin
    g[r][c] = colors[0]
    g[r][c + 1] = colors[1]
    g[r + 1][c] = colors[2]


def _paint_local(g, origin, pts, color=8):
    r0, c0 = origin
    for u, v in pts:
        g[r0 + v][c0 + u] = color


def _paint_values(g, origin, pts):
    r0, c0 = origin
    for (u, v), color in pts:
        g[r0 + v][c0 + u] = color


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index, version=VERSION,
                  task_id=TASK_ID, difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        query_key = ctx.draw_int("query_key", 0, 0)
        variant = ctx.draw_int("variant", 0, 1)
    elif difficulty == "hard":
        query_key = ctx.draw_int("query_key", 1, 1)
        variant = ctx.draw_int("variant", 2, 3)
    else:
        query_key = ctx.draw_int("query_key", 0, 1)
        variant = ctx.draw_int("variant", 0, len(_KEY_SETS) - 1)
    keys = _KEY_SETS[variant]
    values = _VALUE_SETS[variant]
    g = full_grid(25, 24, 0)
    source_origins = [(3, 4), (11, 4), (19, 4)]
    target_origins = [(3, 16), (11, 16), (19, 16)]
    for idx, origin in enumerate(source_origins):
        _frame(g, origin, (2, 3, 4))
        _paint_local(g, origin, keys[idx if idx < 2 else query_key])
    for idx, origin in enumerate(target_origins):
        _frame(g, origin, (5, 6, 7))
        if idx < 2:
            _paint_values(g, origin, values[idx])
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(25, 24, 0)
    source_origins = [(3, 4), (11, 4), (19, 4)]
    target_origins = [(3, 16), (11, 16), (19, 16)]
    keys = _KEY_SETS[0]
    values = _VALUE_SETS[0]
    if name == "no_query":
        # First two pairs but third source/target frames missing.
        for idx, origin in enumerate(source_origins[:2]):
            _frame(g, origin, (2, 3, 4))
            _paint_local(g, origin, keys[idx])
        for idx, origin in enumerate(target_origins[:2]):
            _frame(g, origin, (5, 6, 7))
            _paint_values(g, origin, values[idx])
        return g
    if name == "identical_keys":
        # Both training keys identical → no contrast in lookup.
        for idx, origin in enumerate(source_origins):
            _frame(g, origin, (2, 3, 4))
            _paint_local(g, origin, keys[0])
        for idx, origin in enumerate(target_origins):
            _frame(g, origin, (5, 6, 7))
            if idx < 2:
                _paint_values(g, origin, values[0])
        return g
    if name == "blank_targets":
        # Source frames + keys but target frames empty (no mapping defined).
        for idx, origin in enumerate(source_origins):
            _frame(g, origin, (2, 3, 4))
            _paint_local(g, origin, keys[idx if idx < 2 else 0])
        for origin in target_origins:
            _frame(g, origin, (5, 6, 7))
        return g
    return g
