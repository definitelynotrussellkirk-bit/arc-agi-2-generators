"""Generator for puzzle 6e82a1ae.

Rule: for each non-bg 4-connected object: size 4 → 1, 3 → 2, 2 → 3,
else → 5.

Combinatorial axes: grid_h/w, n_size4, n_size3, n_size2, n_other,
input_color (any non-{0,1,2,3}).
Degenerates: only_size4, only_size3, only_size2, mixed_with_other.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid
from puzzle_generators.helpers.shape import normalize, rect_cells
from puzzle_generators.helpers.place import place_no_overlap

GENERATOR_ID = "154382a9e3e8"
VERSION = "1.1.0"
TASK_ID = "154382a9e3e8"
SUMMARY = "Components of sizes 2, 3, 4; rule recolors by size: 4→1, 3→2, 2→3, else→5."

INVARIANTS = [
    "background is 0",
    "≥1 component of size 4 (becomes 1)",
    "≥1 component of size 3 (becomes 2)",
    "≥1 component of size 2 (becomes 3)",
    "components 4-connected, non-overlapping with margin ≥ 1",
]

DEGENERATE_TEXTURES = ("only_size4", "only_size3", "only_size2", "with_size_5plus")
HELPFUL_TEXTURES = ("balanced_each_size",)

AXES = {
    "grid_h":      {"type": "int", "default": "rng 11..18", "valid": "10..22"},
    "grid_w":      {"type": "int", "default": "rng 11..18", "valid": "10..22"},
    "n_size4":     {"type": "int", "default": "rng 1..3", "valid": "1..5"},
    "n_size3":     {"type": "int", "default": "rng 1..3", "valid": "1..5"},
    "n_size2":     {"type": "int", "default": "rng 1..3", "valid": "1..5"},
    "input_color": {"type": "color", "default": "rng (≠0,1,2,3)", "valid": "4..9"},
    "texture":     {"type": "str", "default": "rng helpful",
                    "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if difficulty == "easy":
        h_lo, h_hi, n_lo, n_hi = 11, 13, 1, 1
    elif difficulty == "hard":
        h_lo, h_hi, n_lo, n_hi = 16, 18, 2, 3
    else:
        h_lo, h_hi, n_lo, n_hi = 11, 18, 1, 3
    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", h_lo, h_hi)
    rng = ctx.draw_rng("placement")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], h, w, rng)
    n_4 = int(overrides.get("n_size4", ctx.draw_int("n_size4", n_lo, n_hi)))
    n_3 = int(overrides.get("n_size3", ctx.draw_int("n_size3", n_lo, n_hi)))
    n_2 = int(overrides.get("n_size2", ctx.draw_int("n_size2", n_lo, n_hi)))
    color = int(overrides.get("input_color",
                              ctx.draw_color("input_color", exclude={0, 1, 2, 3})))
    g = full_grid(h, w, 0)
    placed = {4: 0, 3: 0, 2: 0}
    for size, n_target in [(4, n_4), (3, n_3), (2, n_2)]:
        for _ in range(n_target * 4):
            if placed[size] >= n_target:
                break
            shape = _shape_for_size(size, rng)
            if place_no_overlap(rng, g, shape, color, bg=0, margin=1, max_tries=20):
                placed[size] += 1
    if any(v < 1 for v in placed.values()):
        return [[0]]
    return g


def _shape_for_size(size, rng):
    if size == 4:
        return normalize(rect_cells(*rng.choice([(2, 2), (1, 4), (4, 1)])))
    if size == 3:
        return normalize(rect_cells(*rng.choice([(1, 3), (3, 1)])))
    if size == 2:
        return normalize(rect_cells(*rng.choice([(1, 2), (2, 1)])))
    if size == 5:
        return normalize([(0, 0), (0, 1), (0, 2), (1, 1), (2, 1)])
    return normalize(rect_cells(2, 2))


def _draw_from_degenerate(name, h, w, rng):
    color = rng.choice([4, 5, 6, 7, 8, 9])
    g = full_grid(h, w, 0)
    if name == "only_size4":
        for _ in range(4):
            place_no_overlap(rng, g, _shape_for_size(4, rng), color,
                             bg=0, margin=1, max_tries=20)
        return g
    if name == "only_size3":
        for _ in range(4):
            place_no_overlap(rng, g, _shape_for_size(3, rng), color,
                             bg=0, margin=1, max_tries=20)
        return g
    if name == "only_size2":
        for _ in range(4):
            place_no_overlap(rng, g, _shape_for_size(2, rng), color,
                             bg=0, margin=1, max_tries=20)
        return g
    if name == "with_size_5plus":
        for _ in range(2):
            place_no_overlap(rng, g, _shape_for_size(5, rng), color,
                             bg=0, margin=1, max_tries=20)
        return g
    return g
