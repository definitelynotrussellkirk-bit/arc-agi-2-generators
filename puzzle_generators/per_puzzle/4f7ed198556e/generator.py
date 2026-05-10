"""Generator for ARC task 2072aba6.

Rule: `(rule! (lambda (g) (stamp-grid g (grid (list (list 1 2) (list 2 1))))))`.
At every foreground cell (color 5 in canonical), stamp the 2 × 2
checker `[[1,2],[2,1]]`.

Combinatorial axes:
  * grid_size           — input side (canonical 3; here exposed)
  * trigger_count       — how many cells are color 5 (1..8)
  * trigger_layout      — random/cluster/border/row/column/corners/cross/diagonal
  * filler_pattern      — non-trigger fill: zero / sparse_decoy / mixed_decoy
  * filler_palette_size — colors used for non-trigger cells
  * caller-opt-in degenerates: no_triggers, all_triggers, single_trigger
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "4f7ed198556e"
VERSION = "1.1.0"  # bumped: deeper combinatorial axes added
TASK_ID = "4f7ed198556e"
SUMMARY = "A small pattern with color-5 triggers; every fg cell expands into a fixed 2 × 2 stamp."

INVARIANTS = [
    "input is 3 × 3 (canonical)",
    "foreground trigger color is 5",
    "≥1 foreground cell so the rule has visible effect",
]

TRIGGER_LAYOUTS = (
    "random", "cluster", "border", "row", "column",
    "corners", "cross", "diagonal",
)
FILLER_PATTERNS = ("zero", "sparse_decoy", "mixed_decoy")
DEGENERATE_TEXTURES = ("no_triggers", "all_triggers", "single_trigger")
HELPFUL_TEXTURES = TRIGGER_LAYOUTS

AXES = {
    "grid_size":          {"type": "int", "default": "3", "valid": "3..3"},
    "trigger_count":      {"type": "int", "default": "rng 2..6", "valid": "1..9"},
    "trigger_layout":     {"type": "str", "default": "rng helpful",
                           "valid": "|".join(TRIGGER_LAYOUTS)},
    "filler_pattern":     {"type": "str", "default": "rng zero|sparse_decoy|mixed_decoy",
                           "valid": "|".join(FILLER_PATTERNS)},
    "filler_palette_size": {"type": "int", "default": "rng 1..3", "valid": "0..6"},
    "texture":            {"type": "str", "default": "alias for trigger_layout",
                           "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)

    if difficulty == "easy":
        n_lo, n_hi = 1, 2
    elif difficulty == "hard":
        n_lo, n_hi = 5, 7
    else:
        n_lo, n_hi = 2, 6

    rng = ctx.draw_rng("cells")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], rng)

    n_trigger = int(overrides.get("trigger_count",
                                  ctx.draw_int("trigger_count", n_lo, n_hi)))
    n_trigger = max(1, min(8, n_trigger))
    layout = (overrides.get("texture")
              or overrides.get("trigger_layout")
              or ctx.draw_choice("trigger_layout", list(TRIGGER_LAYOUTS)))
    filler = overrides.get(
        "filler_pattern",
        ctx.draw_choice("filler_pattern", list(FILLER_PATTERNS)))
    n_palette = int(overrides.get("filler_palette_size",
                                  ctx.draw_int("filler_palette_size", 1, 3)))
    palette = ctx.draw_distinct_colors(
        "filler_palette", n=max(1, n_palette), exclude={0, 1, 2, 5})

    g = full_grid(3, 3, 0)
    triggers = _trigger_layout(layout, n_trigger, rng)
    for r, c in triggers:
        g[r][c] = 5

    other_cells = [(r, c) for r in range(3) for c in range(3)
                   if (r, c) not in set(triggers)]
    if filler == "zero":
        pass
    elif filler == "sparse_decoy":
        for r, c in other_cells:
            if rng.random() < 0.3:
                g[r][c] = rng.choice(palette)
    elif filler == "mixed_decoy":
        for r, c in other_cells:
            if rng.random() < 0.6:
                g[r][c] = rng.choice(palette)
    return g


def _trigger_layout(layout, n, rng):
    if layout == "cluster":
        center = (rng.randint(0, 2), rng.randint(0, 2))
        cells = [(r, c) for r in range(3) for c in range(3)]
        cells.sort(key=lambda rc: abs(rc[0] - center[0]) + abs(rc[1] - center[1]))
    elif layout == "border":
        cells = [(r, c) for r in range(3) for c in range(3)
                 if r in {0, 2} or c in {0, 2}]
        rng.shuffle(cells)
    elif layout == "row":
        r = rng.randint(0, 2)
        cells = [(r, c) for c in range(3)]
    elif layout == "column":
        c = rng.randint(0, 2)
        cells = [(r, c) for r in range(3)]
    elif layout == "corners":
        cells = [(0, 0), (0, 2), (2, 0), (2, 2)]
        rng.shuffle(cells)
    elif layout == "cross":
        cells = [(0, 1), (1, 0), (1, 1), (1, 2), (2, 1)]
        rng.shuffle(cells)
    elif layout == "diagonal":
        cells = [(0, 0), (1, 1), (2, 2)] if rng.random() < 0.5 \
            else [(0, 2), (1, 1), (2, 0)]
    else:
        cells = [(r, c) for r in range(3) for c in range(3)]
        rng.shuffle(cells)
    return cells[:max(1, min(n, len(cells)))]


def _draw_from_degenerate(name, rng):
    """Edge-case where the stamp signal collapses.

    no_triggers     — no 5s in input; rule is no-op (output == input).
    all_triggers    — every cell is 5; output is a uniform big checker.
    single_trigger  — single 5; minimal rule signal.
    """
    g = full_grid(3, 3, 0)
    if name == "no_triggers":
        for r in range(3):
            for c in range(3):
                g[r][c] = 0 if rng.random() < 0.4 else 4
        return g
    if name == "all_triggers":
        for r in range(3):
            for c in range(3):
                g[r][c] = 5
        return g
    if name == "single_trigger":
        r = rng.randint(0, 2); c = rng.randint(0, 2)
        g[r][c] = 5
        return g
    return g
