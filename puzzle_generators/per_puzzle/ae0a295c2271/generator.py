"""Generator for puzzle b230c067.

Rule: for each non-bg object, count objects with the same normalized
shape; if 1 (unique) → recolor 2; else → recolor 1.

Combinatorial axes: grid_h/w, n_twin_pairs, n_uniques, twin_kinds,
unique_kinds, palette_for_input.
Degenerates: all_unique, all_twins, single_object.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid
from puzzle_generators.helpers.shape import normalize, rect_cells
from puzzle_generators.helpers.place import place_no_overlap

GENERATOR_ID = "ae0a295c2271"
VERSION = "1.1.0"
TASK_ID = "ae0a295c2271"
SUMMARY = "Multiple objects; rule colors twin-shape pairs blue(1), unique shapes red(2)."

INVARIANTS = [
    "background is 0",
    "≥2 objects have the same shape (twin branch fires)",
    "≥1 object has a unique shape (singleton branch fires)",
    "objects 4-connected, non-overlapping with margin ≥ 1",
]

SHAPE_KINDS = ("L", "T", "Z", "I", "S", "tri", "plus", "ell")
DEGENERATE_TEXTURES = ("all_unique", "all_twins", "single_object")
HELPFUL_TEXTURES = SHAPE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 12..20", "valid": "10..25"},
    "grid_w":         {"type": "int", "default": "rng 12..20", "valid": "10..25"},
    "n_twin_pairs":   {"type": "int", "default": "rng 1..2", "valid": "1..3"},
    "n_uniques":      {"type": "int", "default": "rng 2..3", "valid": "1..5"},
    "twin_kind":      {"type": "str", "default": "rng helpful",
                       "valid": "|".join(SHAPE_KINDS)},
    "input_color":    {"type": "color", "default": "rng (≠0,1,2)", "valid": "3..9"},
    "texture":        {"type": "str", "default": "alias for twin_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def _shape(kind):
    if kind == "L":
        return normalize([(0, 0), (1, 0), (2, 0), (2, 1)])
    if kind == "T":
        return normalize([(0, 0), (0, 1), (0, 2), (1, 1)])
    if kind == "Z":
        return normalize([(0, 0), (0, 1), (1, 1), (1, 2)])
    if kind == "I":
        return normalize([(0, 0), (1, 0), (2, 0)])
    if kind == "S":
        return normalize(rect_cells(2, 2))
    if kind == "plus":
        return normalize([(0, 1), (1, 0), (1, 1), (1, 2), (2, 1)])
    if kind == "ell":
        return normalize([(0, 0), (1, 0), (1, 1), (1, 2)])
    return normalize([(0, 0), (0, 1), (1, 0)])  # tri


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if difficulty == "easy":
        h_lo, h_hi, t_lo, t_hi, u_lo, u_hi = 12, 14, 1, 1, 1, 2
    elif difficulty == "hard":
        h_lo, h_hi, t_lo, t_hi, u_lo, u_hi = 18, 20, 2, 2, 3, 3
    else:
        h_lo, h_hi, t_lo, t_hi, u_lo, u_hi = 12, 20, 1, 2, 2, 3
    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", h_lo, h_hi)
    rng = ctx.draw_rng("placement")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], h, w, rng)
    n_pairs = int(overrides.get("n_twin_pairs",
                                ctx.draw_int("n_twin_pairs", t_lo, t_hi)))
    n_uniques = int(overrides.get("n_uniques",
                                  ctx.draw_int("n_uniques", u_lo, u_hi)))
    twin_kind = (overrides.get("texture") or overrides.get("twin_kind")
                 or ctx.draw_choice("twin_kind", list(SHAPE_KINDS)))
    color = int(overrides.get("input_color",
                              ctx.draw_color("input_color", exclude={0, 1, 2})))
    g = full_grid(h, w, 0)
    twin_cells = _shape(twin_kind)
    placed_twins = 0
    for _ in range(n_pairs * 2):
        if place_no_overlap(rng, g, twin_cells, color, bg=0, margin=1, max_tries=40):
            placed_twins += 1
    others = [k for k in SHAPE_KINDS if k != twin_kind]
    rng.shuffle(others)
    placed_unique = 0
    for kind in others[:n_uniques]:
        cells = _shape(kind)
        if place_no_overlap(rng, g, cells, color, bg=0, margin=1, max_tries=30):
            placed_unique += 1
    if placed_twins < 2 or placed_unique < 1:
        return [[0]]
    return g


def _draw_from_degenerate(name, h, w, rng):
    g = full_grid(h, w, 0)
    color = rng.choice([3, 4, 5, 6, 7, 8, 9])
    if name == "all_unique":
        kinds = list(SHAPE_KINDS)
        rng.shuffle(kinds)
        for kind in kinds[:4]:
            cells = _shape(kind)
            place_no_overlap(rng, g, cells, color, bg=0, margin=1, max_tries=30)
        return g
    if name == "all_twins":
        kind = rng.choice(SHAPE_KINDS)
        cells = _shape(kind)
        for _ in range(4):
            place_no_overlap(rng, g, cells, color, bg=0, margin=1, max_tries=30)
        return g
    if name == "single_object":
        cells = _shape(rng.choice(SHAPE_KINDS))
        place_no_overlap(rng, g, cells, color, bg=0, margin=1, max_tries=30)
        return g
    return g
