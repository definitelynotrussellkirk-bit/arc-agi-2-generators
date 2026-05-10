"""Generator for ARC task 6e02f1e3.

Rule: input is 3×3 with 1, 2, or 3 distinct non-zero colors. Output is
a fixed 3×3 mark pattern by count: 1→top-row 5s, 2→main-diag 5s,
3→anti-diag 5s.

Combinatorial axes (8): color_count, palette_choice, cell_layout,
fg_density, anchor_diag, dominant_color, color_balance, position_jitter.
Degenerates: all_same, all_zero, mixed_with_zero.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "abcb59bec35f"
VERSION = "1.1.0"
TASK_ID = "abcb59bec35f"
SUMMARY = "3×3 grid with 1, 2, or 3 distinct colors; rule emits a count-keyed 5-pattern."

INVARIANTS = [
    "input is 3×3",
    "the number of distinct source colors is in {1, 2, 3}",
    "all cells are non-zero (so color count is unambiguous)",
]

CELL_LAYOUTS = ("uniform_random", "diag_anchored", "row_dominant",
                "col_dominant", "checker", "block")
DEGENERATE_TEXTURES = ("all_same", "all_zero", "mixed_with_zero")
HELPFUL_TEXTURES = CELL_LAYOUTS

AXES = {
    "color_count":   {"type": "int",  "default": "rng 1..3", "valid": "1..3"},
    "cell_layout":   {"type": "str",  "default": "rng helpful",
                      "valid": "|".join(CELL_LAYOUTS)},
    "anchor_diag":   {"type": "bool", "default": "true",  "valid": "true|false"},
    "color_balance": {"type": "str",  "default": "rng even|skew",
                      "valid": "even|skew"},
    "dominant_color": {"type": "color", "default": "= colors[0]", "valid": "1..9"},
    "position_jitter": {"type": "bool", "default": "true", "valid": "true|false"},
    "fg_density":    {"type": "float", "default": "1.0", "valid": "0..1"},
    "texture":       {"type": "str", "default": "alias for cell_layout",
                      "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index, version=VERSION,
                  task_id=TASK_ID, difficulty=difficulty, overrides=overrides)
    if difficulty == "easy":
        count_choices = [1]
    elif difficulty == "hard":
        count_choices = [3]
    else:
        count_choices = [1, 2, 3]
    rng = ctx.draw_rng("cells")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], rng)
    count = int(overrides.get("color_count",
                              ctx.draw_choice("color_count", count_choices)))
    count = max(1, min(3, count))
    colors = list(ctx.draw_distinct_colors("palette", n=count, exclude={0}))
    layout = (overrides.get("texture") or overrides.get("cell_layout")
              or ctx.draw_choice("cell_layout", list(CELL_LAYOUTS)))
    balance = overrides.get("color_balance",
                            ctx.draw_choice("color_balance", ["even", "skew"]))
    anchor = bool(overrides.get("anchor_diag", True))
    g = full_grid(3, 3, colors[0])
    if balance == "skew" and len(colors) > 1:
        weights = [3, 2, 1][:len(colors)]
    else:
        weights = [1] * len(colors)
    pool = []
    for c, w in zip(colors, weights):
        pool += [c] * w
    if layout == "diag_anchored":
        for i in range(3):
            g[i][i] = colors[i % len(colors)]
        for r in range(3):
            for c in range(3):
                if r != c:
                    g[r][c] = rng.choice(pool)
    elif layout == "row_dominant":
        for r in range(3):
            color = colors[r % len(colors)]
            for c in range(3):
                g[r][c] = color
    elif layout == "col_dominant":
        for c in range(3):
            color = colors[c % len(colors)]
            for r in range(3):
                g[r][c] = color
    elif layout == "checker":
        for r in range(3):
            for c in range(3):
                g[r][c] = colors[(r + c) % len(colors)]
    elif layout == "block":
        for r in range(3):
            for c in range(3):
                g[r][c] = colors[((r // 2) * 2 + c // 2) % len(colors)]
    else:  # uniform_random
        for r in range(3):
            for c in range(3):
                g[r][c] = rng.choice(pool)
    if anchor and len(colors) >= 1:
        for i, color in enumerate(colors):
            g[i][i] = color
    distinct = {v for row in g for v in row}
    if len(distinct) != count:
        present = sorted(distinct)
        if len(present) < count:
            for i, c in enumerate(colors):
                g[2][i % 3] = c
        elif len(present) > count:
            keep = set(colors)
            for r in range(3):
                for c in range(3):
                    if g[r][c] not in keep:
                        g[r][c] = colors[0]
    return g


def _draw_from_degenerate(name, rng):
    if name == "all_same":
        c = rng.choice([1, 2, 3, 4, 5, 6, 7, 8, 9])
        return [[c] * 3 for _ in range(3)]
    if name == "all_zero":
        return [[0] * 3 for _ in range(3)]
    if name == "mixed_with_zero":
        c1 = rng.choice([1, 2, 3])
        c2 = rng.choice([4, 5, 6])
        return [[c1, 0, c2], [0, c1, 0], [c2, 0, c1]]
    return [[1] * 3 for _ in range(3)]
