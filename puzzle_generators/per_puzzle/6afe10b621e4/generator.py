"""Generator for puzzle 5f3e1b4e.

Rule: keep largest red(2) object → recolor to 4, keep largest green(3)
object → recolor to 1; everything else cleared to 0.

Combinatorial axes (8): grid_h/w, n_red_objs, n_green_objs,
red_size_diff, green_size_diff, distractor_color, position_bias,
asymmetry_force.
Degenerates: tied_largest, single_object, no_red.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid
from puzzle_generators.helpers.shape import normalize, rect_cells
from puzzle_generators.helpers.place import place_no_overlap

GENERATOR_ID = "6afe10b621e4"
VERSION = "1.1.0"
TASK_ID = "6afe10b621e4"
SUMMARY = "Multiple red+green objects; rule keeps the largest of each."

INVARIANTS = [
    "background is 0",
    ">=2 red(2) objects, ≥2 green(3) objects",
    "the largest red object is unique (no tie)",
    "the largest green object is unique (no tie)",
]

POSITION_BIASES = ("spread", "corners", "clustered", "edges")
DEGENERATE_TEXTURES = ("tied_largest", "single_object", "no_red")
HELPFUL_TEXTURES = POSITION_BIASES

AXES = {
    "grid_h":            {"type": "int", "default": "rng 9..14", "valid": "7..18"},
    "grid_w":            {"type": "int", "default": "rng 9..14", "valid": "7..18"},
    "n_red_objs":        {"type": "int", "default": "rng 2..3", "valid": "2..5"},
    "n_green_objs":      {"type": "int", "default": "rng 2..3", "valid": "2..5"},
    "largest_size":      {"type": "int", "default": "rng 5..8", "valid": "3..12"},
    "smallest_size":     {"type": "int", "default": "rng 1..3", "valid": "1..4"},
    "position_bias":     {"type": "str", "default": "rng helpful",
                          "valid": "|".join(POSITION_BIASES)},
    "include_distractor":{"type": "bool", "default": "true",
                          "valid": "true|false"},
    "texture":           {"type": "str", "default": "alias for position_bias",
                          "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if difficulty == "easy":
        h_lo, h_hi = 7, 10
    elif difficulty == "hard":
        h_lo, h_hi = 14, 18
    else:
        h_lo, h_hi = 9, 14
    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", h_lo, h_hi)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], h, w, rng)
    n_red = int(overrides.get("n_red_objs",
                              ctx.draw_int("n_red_objs", 2, 3)))
    n_green = int(overrides.get("n_green_objs",
                                ctx.draw_int("n_green_objs", 2, 3)))
    n_red = max(2, min(5, n_red))
    n_green = max(2, min(5, n_green))
    largest = int(overrides.get("largest_size",
                                ctx.draw_int("largest_size", 5, 8)))
    smallest = int(overrides.get("smallest_size",
                                 ctx.draw_int("smallest_size", 1, 3)))
    largest = max(3, min(12, largest))
    smallest = max(1, min(largest - 1, smallest))
    g = full_grid(h, w, 0)
    # Place red objects: 1 large + (n_red - 1) small
    _place_color(g, 2, n_red, largest, smallest, rng)
    _place_color(g, 3, n_green, largest - 1, smallest, rng)
    if bool(overrides.get("include_distractor", True)):
        # Single-cell distractor of an unrelated color (rule clears it)
        for _ in range(20):
            r = rng.randint(0, h - 1); c = rng.randint(0, w - 1)
            if g[r][c] == 0:
                g[r][c] = rng.choice([4, 5, 6, 7, 8, 9])
                break
    return g


def _place_color(g, color, n, largest, smallest, rng):
    # Place largest first, then smaller ones
    sizes = [largest] + [rng.randint(smallest, max(smallest, largest - 2))
                          for _ in range(n - 1)]
    sizes.sort(reverse=True)
    # Ensure largest is strictly bigger than the next
    if len(sizes) > 1 and sizes[0] == sizes[1]:
        sizes[0] += 1
    for sz in sizes:
        cells = _shape_for_size(sz, rng)
        place_no_overlap(rng, g, cells, color, bg=0,
                         margin=1, max_tries=30)


def _shape_for_size(sz, rng):
    if sz == 1:
        return [(0, 0)]
    if sz == 2:
        return [(0, 0), (0, 1)]
    if sz == 3:
        return [(0, 0), (0, 1), (1, 0)]
    if sz == 4:
        return normalize(rect_cells(2, 2))
    # blob-ish growth
    cells = [(0, 0)]
    for _ in range(sz * 2):
        if len(cells) >= sz:
            break
        r, c = rng.choice(cells)
        dr, dc = rng.choice([(-1, 0), (1, 0), (0, -1), (0, 1)])
        new = (r + dr, c + dc)
        if new not in cells:
            cells.append(new)
    return normalize(cells)


def _draw_from_degenerate(name, h, w, rng):
    g = full_grid(h, w, 0)
    if name == "tied_largest":
        # Two red objects same size, two green objects same size — rule
        # output is non-deterministic in the racket sort; the smoke
        # validator should catch this as degenerate.
        place_no_overlap(rng, g, [(0, 0), (0, 1), (1, 0)], 2,
                         bg=0, margin=1, max_tries=30)
        place_no_overlap(rng, g, [(0, 0), (0, 1), (1, 0)], 2,
                         bg=0, margin=1, max_tries=30)
        place_no_overlap(rng, g, [(0, 0), (0, 1)], 3,
                         bg=0, margin=1, max_tries=30)
        place_no_overlap(rng, g, [(0, 0), (0, 1)], 3,
                         bg=0, margin=1, max_tries=30)
        return g
    if name == "single_object":
        place_no_overlap(rng, g, [(0, 0), (0, 1), (1, 0), (1, 1)], 2,
                         bg=0, margin=1, max_tries=30)
        return g
    if name == "no_red":
        place_no_overlap(rng, g, [(0, 0), (0, 1), (1, 0)], 3,
                         bg=0, margin=1, max_tries=30)
        place_no_overlap(rng, g, [(0, 0), (0, 1)], 3,
                         bg=0, margin=1, max_tries=30)
        return g
    return g
