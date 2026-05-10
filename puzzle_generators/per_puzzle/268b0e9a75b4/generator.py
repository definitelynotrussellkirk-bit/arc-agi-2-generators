"""Generator for arc_additional_puzzles_21_set16_bundle:E109 — Crop the unique-color object.

Rule: find the color that appears in exactly one object. Crop the
input to that object's bbox.

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: no_unique (every color repeats — rule's "exactly one
object" filter finds nothing); all_unique (every color is its own
single object — multiple unique colors, selection ambiguous);
single_object (only one object total — trivially "unique", no
contrast against repeated colors).
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "268b0e9a75b4"
VERSION = "1.1.0"
TASK_ID = "268b0e9a75b4"

SUMMARY = "2-3 distinct colors, one appears in exactly one object, others in multiple."

INVARIANTS = [
    "exactly one color appears in exactly one object (the unique one)",
    "each other color appears in 2+ objects",
    "objects don't touch (separated by ≥1 bg cell)",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_unique", "all_unique", "single_object")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 7..10", "valid": "5..12"},
    "grid_w":         {"type": "int", "default": "rng 9..12", "valid": "8..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "palette_size":   {"type": "int", "default": "2", "valid": "2..3"},
    "position_bias":  {"type": "str", "default": "unique_plus_repeated",
                       "valid": "unique_plus_repeated"},
    "n_distinct_colors": {"type": "int", "default": "2", "valid": "2..3"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}

SHAPES = [
    [(0, 0), (0, 1)],                          # 1x2
    [(0, 0), (0, 1), (1, 0), (1, 1)],          # 2x2
    [(0, 0), (1, 0)],                          # 2x1
    [(0, 0), (0, 1), (0, 2)],                  # 1x3
]


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 7, 7)
        w = ctx.draw_int("grid_w", 9, 9)
        n_repeated_max = 2
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 9, 12)
        w = ctx.draw_int("grid_w", 11, 14)
        n_repeated_max = 3
    else:
        h = ctx.draw_int("grid_h", 7, 10)
        w = ctx.draw_int("grid_w", 9, 12)
        n_repeated_max = 3
    g = full_grid(h, w, 0)
    rng = ctx.draw_rng("layout")
    palette = rng.sample([1, 2, 3, 4, 6, 7, 8, 9], 2)
    unique_color, repeated_color = palette
    n_unique = 1
    n_repeated = rng.randint(2, n_repeated_max)
    occupied = [[False] * w for _ in range(h)]

    def place(color):
        shape = rng.choice(SHAPES)
        sh = max(r for r, c in shape) + 1
        sw = max(c for r, c in shape) + 1
        for _ in range(60):
            r0 = rng.randint(0, h - sh)
            c0 = rng.randint(0, w - sw)
            if any(occupied[rr][cc]
                   for rr in range(max(0, r0 - 1), min(h, r0 + sh + 1))
                   for cc in range(max(0, c0 - 1), min(w, c0 + sw + 1))):
                continue
            for dr, dc in shape:
                g[r0 + dr][c0 + dc] = color
            for rr in range(max(0, r0 - 1), min(h, r0 + sh + 1)):
                for cc in range(max(0, c0 - 1), min(w, c0 + sw + 1)):
                    occupied[rr][cc] = True
            return True
        return False

    for _ in range(n_unique):
        place(unique_color)
    for _ in range(n_repeated):
        place(repeated_color)
    return g


def _draw_from_degenerate(name, rng):
    h, w = 8, 10
    g = full_grid(h, w, 0)
    if name == "no_unique":
        # Every color appears in 2+ objects → rule's "exactly one
        # object of this color" filter excludes all colors; output
        # undefined.
        for cells, color, base in [([(0, 0), (0, 1)], 3, (1, 1)),
                                   ([(0, 0), (1, 0)], 3, (1, 6)),
                                   ([(0, 0), (0, 1)], 4, (5, 1)),
                                   ([(0, 0), (0, 1)], 4, (5, 6))]:
            for dr, dc in cells:
                g[base[0] + dr][base[1] + dc] = color
        return g
    if name == "all_unique":
        # Every color appears in exactly one object → multiple
        # candidates for "the unique one"; rule's selector ambiguous.
        for cells, color, base in [([(0, 0), (0, 1)], 3, (1, 1)),
                                   ([(0, 0), (1, 0)], 4, (1, 6)),
                                   ([(0, 0), (0, 1)], 6, (5, 4))]:
            for dr, dc in cells:
                g[base[0] + dr][base[1] + dc] = color
        return g
    if name == "single_object":
        # Only one object — trivially the "unique-color" winner;
        # no contrast against repeated-color motifs.
        for r, c in [(3, 4), (3, 5), (4, 4)]: g[r][c] = 3
        return g
    return g
