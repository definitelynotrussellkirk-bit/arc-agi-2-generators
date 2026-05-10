"""Generator for ARC task 332efdb3.

Rule: `(rule! (lambda (g) (grid-from-fn h w (lambda (r c) (if (and (= 1 (mod r 2)) (= 1 (mod c 2))) 0 1)))))`.
Output is a fixed lattice (1 everywhere except odd-row + odd-col cells
which are 0). Input contents are ignored — only h and w matter.

Combinatorial axes: side, input_decoration, decoration_palette_size.
Degenerates: structured_decoy_lattice (input mimics output to mislead),
max_size, min_size.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "4056ed281704"
VERSION = "1.1.0"
TASK_ID = "4056ed281704"
SUMMARY = "Square input grid; rule emits a fixed 1/0 parity-lattice mask of the same dims."

INVARIANTS = [
    "input is an odd square (side ∈ {5, 7, 9, 11, 13})",
    "input contents do not affect output",
    "output is fixed by dims",
]

INPUT_DECORATIONS = ("all_zero", "random", "sparse", "blob", "structured")
DEGENERATE_TEXTURES = ("structured_decoy_lattice", "max_size", "min_size")
HELPFUL_TEXTURES = INPUT_DECORATIONS

AXES = {
    "side":              {"type": "choice", "default": "rng odd 5..13",
                          "valid": "5|7|9|11|13"},
    "input_decoration":  {"type": "str", "default": "rng helpful",
                          "valid": "|".join(INPUT_DECORATIONS)},
    "decoration_palette_size": {"type": "int", "default": "rng 1..3", "valid": "1..6"},
    "texture":           {"type": "str", "default": "alias for input_decoration",
                          "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if difficulty == "easy":
        side_choices = [5, 7]
    elif difficulty == "hard":
        side_choices = [11, 13]
    else:
        side_choices = [5, 7, 9, 11, 13]
    side = ctx.draw_choice("side", side_choices)
    rng = ctx.draw_rng("cells")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], side, rng)
    n_palette = int(overrides.get("decoration_palette_size",
                                  ctx.draw_int("decoration_palette_size", 1, 3)))
    palette = list(ctx.draw_distinct_colors("palette", n=max(1, n_palette), exclude={0}))
    decoration = (overrides.get("texture")
                  or overrides.get("input_decoration")
                  or ctx.draw_choice("input_decoration", list(INPUT_DECORATIONS)))
    g = full_grid(side, side, 0)
    if decoration == "all_zero":
        return g
    if decoration == "random":
        for r in range(side):
            for c in range(side):
                if rng.random() < 0.5:
                    g[r][c] = rng.choice(palette)
        return g
    if decoration == "sparse":
        for r in range(side):
            for c in range(side):
                if rng.random() < 0.2:
                    g[r][c] = rng.choice(palette)
        return g
    if decoration == "blob":
        bh = side // 2; bw = side // 2
        r0 = rng.randint(0, side - bh); c0 = rng.randint(0, side - bw)
        color = palette[0]
        for r in range(r0, r0 + bh):
            for c in range(c0, c0 + bw):
                g[r][c] = color
        return g
    if decoration == "structured":
        c0 = palette[0]
        for c in range(side):
            g[0][c] = c0; g[side - 1][c] = c0
        for r in range(side):
            g[r][0] = c0; g[r][side - 1] = c0
        return g
    return g


def _draw_from_degenerate(name, side, rng):
    palette = list(range(1, 10))
    rng.shuffle(palette)
    if name == "max_size":
        side = 13
    elif name == "min_size":
        side = 5
    g = full_grid(side, side, 0)
    if name == "structured_decoy_lattice":
        c = palette[0]
        for r in range(side):
            for cc in range(side):
                if not (r % 2 == 1 and cc % 2 == 1):
                    g[r][cc] = c
        return g
    return g
