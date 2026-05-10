"""Generator for arc_puzzle_bank_21_set5_s:S5_E1 — legend-color crop.

The top-left legend color selects the same-color object to crop.

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: no_target_match (no body object uses the legend color →
rule's selector finds nothing, output undefined), multiple_matches
(multiple body objects use the legend color → "the object" is
ambiguous, tie-break decides), no_distractors (only one object plus
legend → no distractor contrast, rule looks like "crop everything").
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "77d32a44a58c"
VERSION = "1.1.0"
TASK_ID = "77d32a44a58c"

SUMMARY = "The top-left legend color selects the same-color object to crop."

INVARIANTS = [
    "background is 0",
    "cell (0,0) contains the target color",
    "exactly one non-legend object has that target color",
    "distractor objects use other colors",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_target_match", "multiple_matches", "no_distractors")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..10", "valid": "6..14"},
    "grid_w":         {"type": "int", "default": "rng 8..11", "valid": "6..14"},
    "target_shape":   {"type": "choice", "default": "rng 0..3", "valid": "0..3"},
    "distractor_count": {"type": "int", "default": "rng 1..2", "valid": "0..4"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "palette_size":   {"type": "int", "default": "rng 3..4", "valid": "2..5"},
    "position_bias":  {"type": "str", "default": "legend_plus_target_plus_distractors",
                       "valid": "legend_plus_target_plus_distractors"},
    "n_distinct_colors": {"type": "int", "default": "rng 3..4", "valid": "2..5"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}

_SHAPES = [
    [(0, 0), (1, 0), (2, 0), (2, 1)],
    [(0, 0), (0, 1), (0, 2), (1, 1)],
    [(0, 1), (1, 0), (1, 1), (2, 1)],
    [(0, 0), (0, 1), (1, 0), (2, 0), (2, 1)],
]

_DISTRACTORS = [
    [(0, 0), (0, 1)],
    [(0, 0), (1, 0), (1, 1)],
    [(0, 0), (0, 1), (1, 0), (1, 1)],
]


def _place(g, rng, cells, color, occupied, *, padding=1):
    h = len(g)
    w = len(g[0])
    max_r = max(r for r, _ in cells)
    max_c = max(c for _, c in cells)
    for _ in range(300):
        r0 = rng.randint(1, h - max_r - 1)
        c0 = rng.randint(1, w - max_c - 1)
        placed = [(r0 + r, c0 + c) for r, c in cells]
        if any(g[r][c] != 0 for r, c in placed):
            continue
        if any(abs(r - rr) <= padding and abs(c - cc) <= padding
               for r, c in placed for rr, cc in occupied):
            continue
        for r, c in placed:
            g[r][c] = color
        occupied.update(placed)
        return
    raise ValueError("could not place object")


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index, version=VERSION,
                  task_id=TASK_ID, difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("grid_w", 8, 9)
        distractor_count = ctx.draw_int("distractor_count", 1, 1)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 10, 12)
        w = ctx.draw_int("grid_w", 10, 13)
        distractor_count = ctx.draw_int("distractor_count", 2, 4)
    else:
        h = ctx.draw_int("grid_h", 8, 10)
        w = ctx.draw_int("grid_w", 8, 11)
        distractor_count = ctx.draw_int("distractor_count", 1, 2)
    shape = _SHAPES[ctx.draw_choice("target_shape", list(range(len(_SHAPES))))]
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    target = ctx.draw_color("target_color", exclude={0})
    g[0][0] = target
    occupied = {(0, 0)}
    _place(g, rng, shape, target, occupied)
    colors = [c for c in range(1, 10) if c != target]
    for idx in range(distractor_count):
        _place(g, rng, rng.choice(_DISTRACTORS), colors[idx % len(colors)], occupied)
    return g


def _draw_from_degenerate(name, rng):
    h, w = 9, 10
    g = full_grid(h, w, 0)
    g[0][0] = 5
    if name == "no_target_match":
        # Legend says color 5 but no body object is color 5;
        # rule's selector finds nothing.
        for dr, dc in _DISTRACTORS[1]:
            g[3 + dr][3 + dc] = 2
        for dr, dc in _DISTRACTORS[2]:
            g[5 + dr][6 + dc] = 4
        return g
    if name == "multiple_matches":
        # Multiple body objects share the legend color 5; "the
        # object" is ambiguous, tie-break decides.
        for dr, dc in _SHAPES[0]:
            g[2 + dr][2 + dc] = 5
        for dr, dc in _SHAPES[2]:
            g[2 + dr][6 + dc] = 5
        return g
    if name == "no_distractors":
        # Only one object plus legend — no distractor contrast;
        # rule looks like "crop everything".
        for dr, dc in _SHAPES[1]:
            g[3 + dr][3 + dc] = 5
        return g
    return g
