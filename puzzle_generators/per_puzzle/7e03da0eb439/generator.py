"""Generator for ARC task cce03e0d.

Rule: `(rule! (lambda (g) (self-tile g (lambda (v) (= v 2)))))`. For
every cell that equals 2, paint a copy of the whole input centered at
that cell. Output dims: H² × W² (here 9 × 9 since input is 3 × 3).

Combinatorial axes:
  * grid_size           — input side length (kept at 3 in canonical)
  * n_2_cells           — how many cells get value 2 (the trigger)
  * non_2_pattern       — what fills the non-trigger cells: zero / mixed_low /
                          mixed_full / sparse_high
  * non_2_palette       — set of colors that fills the non-2 cells
  * trigger_layout      — where the 2s sit: random / corners / row /
                          column / cross
  * caller-opt-in degenerates: no_2_cells (rule no-op), all_2_cells
                               (output blows up to 9×9 same shape), monochrome_2
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "7e03da0eb439"
VERSION = "1.1.0"  # bumped: deeper combinatorial axes added
TASK_ID = "7e03da0eb439"
SUMMARY = "A 3×3 tile with selected color-2 cells; those cells receive full tile copies."

INVARIANTS = [
    "input is 3×3",
    "color 2 appears at least once (else rule is no-op)",
    "non-2 cells use any color (must include enough variety to keep the tile interesting)",
]

NON_2_PATTERNS = ("zero", "mixed_low", "mixed_full", "sparse_high")
TRIGGER_LAYOUTS = ("random", "corners", "row", "column", "cross")
DEGENERATE_TEXTURES = ("no_2_cells", "all_2_cells", "monochrome_2")
HELPFUL_TEXTURES = NON_2_PATTERNS

AXES = {
    "grid_size":      {"type": "int", "default": "3", "valid": "3..3"},
    "n_2_cells":      {"type": "int", "default": "rng 1..5", "valid": "1..9"},
    "non_2_pattern":  {"type": "str", "default": "rng helpful",
                       "valid": "|".join(NON_2_PATTERNS)},
    "trigger_layout": {"type": "str", "default": "rng random|corners|row|column|cross",
                       "valid": "|".join(TRIGGER_LAYOUTS)},
    "non_2_palette_size": {"type": "int", "default": "rng 1..3", "valid": "0..6"},
    "texture":        {"type": "str", "default": "alias for non_2_pattern",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)

    if difficulty == "easy":
        n_lo, n_hi, p_lo, p_hi = 1, 3, 1, 1
    elif difficulty == "hard":
        n_lo, n_hi, p_lo, p_hi = 4, 6, 2, 3
    else:
        n_lo, n_hi, p_lo, p_hi = 1, 6, 1, 3

    rng = ctx.draw_rng("cells")

    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], rng)

    n2 = int(overrides.get("n_2_cells", ctx.draw_int("n_2_cells", n_lo, n_hi)))
    n2 = max(1, min(8, n2))
    layout = overrides.get(
        "trigger_layout",
        ctx.draw_choice("trigger_layout", list(TRIGGER_LAYOUTS)))
    pattern = (overrides.get("texture")
               or overrides.get("non_2_pattern")
               or ctx.draw_choice("non_2_pattern", list(NON_2_PATTERNS)))
    n_palette = int(overrides.get("non_2_palette_size",
                                  ctx.draw_int("non_2_palette_size", p_lo, p_hi)))
    non_2_palette = ctx.draw_distinct_colors(
        "non_2_palette", n=max(1, n_palette), exclude={2})

    g = full_grid(3, 3, 0)
    trigger_cells = _trigger_layout(layout, n2, rng)
    for r, c in trigger_cells:
        g[r][c] = 2

    # Fill non-trigger cells per pattern.
    other_cells = [(r, c) for r in range(3) for c in range(3)
                   if (r, c) not in set(trigger_cells)]
    rng.shuffle(other_cells)
    if pattern == "zero":
        for r, c in other_cells:
            g[r][c] = 0
    elif pattern == "mixed_low":
        for r, c in other_cells:
            g[r][c] = rng.choice(non_2_palette) if rng.random() < 0.4 else 0
    elif pattern == "mixed_full":
        for r, c in other_cells:
            g[r][c] = rng.choice(non_2_palette)
    else:  # sparse_high
        for r, c in other_cells:
            g[r][c] = rng.choice(non_2_palette) if rng.random() < 0.7 else 0
    return g


def _trigger_layout(layout, n, rng):
    if layout == "corners":
        candidates = [(0, 0), (0, 2), (2, 0), (2, 2)]
    elif layout == "row":
        r = rng.randint(0, 2)
        candidates = [(r, 0), (r, 1), (r, 2)]
    elif layout == "column":
        c = rng.randint(0, 2)
        candidates = [(0, c), (1, c), (2, c)]
    elif layout == "cross":
        candidates = [(0, 1), (1, 0), (1, 1), (1, 2), (2, 1)]
    else:  # random
        candidates = [(r, c) for r in range(3) for c in range(3)]
    rng.shuffle(candidates)
    n = min(n, len(candidates))
    out = candidates[:n]
    if not out:
        out = [(rng.randint(0, 2), rng.randint(0, 2))]
    return out


def _draw_from_degenerate(name, rng):
    """Edge-case where the self-tile signature is hidden.

    no_2_cells     — input has no 2s; rule is identity.
    all_2_cells    — every cell is 2; output is 3×3 copies of the all-2
                     grid → just an all-2 9×9.
    monochrome_2   — all cells same value (which is 2); same as all_2_cells
                     but kept for symmetry.
    """
    g = full_grid(3, 3, 0)
    if name == "no_2_cells":
        palette = [c for c in range(10) if c != 2]
        for r in range(3):
            for c in range(3):
                g[r][c] = rng.choice(palette)
        return g
    if name == "all_2_cells" or name == "monochrome_2":
        for r in range(3):
            for c in range(3):
                g[r][c] = 2
        return g
    return g
