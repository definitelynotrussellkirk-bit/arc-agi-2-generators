"""Generator for ARC task 48f8583b.

Rule: `(rule! (lambda (g) (self-tile g (lambda (v) (= v (minority g))))))`.
Self-tile gated on cells equal to the LEAST-frequent color (the
minority). Output is H² × W² with the input duplicated where the
minority color appears.

Combinatorial axes:
  * grid_size              — kept at 3 (canonical)
  * minority_color         — the singleton color
  * minority_count         — how many cells take the minority (1..2;
                             must be strictly fewer than the others)
  * other_palette_size     — number of distinct non-minority colors
  * other_layout           — how the majority colors arrange:
                             uniform / two_colors / striped /
                             checker / diagonal_split
  * caller-opt-in degenerates: tied_minorities, monochrome, all_unique
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "120c8532b351"
VERSION = "1.1.0"  # bumped: deeper combinatorial axes added
TASK_ID = "120c8532b351"
SUMMARY = "A 3 × 3 grid with one singleton color; minority cells receive tile copies."

INVARIANTS = [
    "input is 3 × 3",
    "the minority color appears strictly fewer times than every other color",
    "≥2 distinct colors so the rule has visible effect",
]

OTHER_LAYOUTS = ("uniform", "two_colors", "striped", "checker", "diagonal_split")
DEGENERATE_TEXTURES = ("tied_minorities", "monochrome", "all_unique")
HELPFUL_TEXTURES = OTHER_LAYOUTS

AXES = {
    "grid_size":          {"type": "int",   "default": "3", "valid": "3..3"},
    "minority_color":     {"type": "color", "default": "rng", "valid": "0..9"},
    "minority_count":     {"type": "int",   "default": "rng 1..2", "valid": "1..2"},
    "other_palette_size": {"type": "int",   "default": "rng 1..3", "valid": "1..6"},
    "other_layout":       {"type": "str",   "default": "rng helpful",
                           "valid": "|".join(OTHER_LAYOUTS)},
    "texture":            {"type": "str",   "default": "alias for other_layout",
                           "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)

    if difficulty == "easy":
        m_lo, m_hi, p_lo, p_hi = 1, 1, 1, 1
    elif difficulty == "hard":
        m_lo, m_hi, p_lo, p_hi = 1, 2, 2, 3
    else:
        m_lo, m_hi, p_lo, p_hi = 1, 2, 1, 3

    rng = ctx.draw_rng("cells")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], ctx, rng)

    minority = int(overrides.get("minority_color",
                                 ctx.draw_color("minority_color")))
    n_other_palette = int(overrides.get("other_palette_size",
                                        ctx.draw_int("other_palette_size", p_lo, p_hi)))
    other_palette = ctx.draw_distinct_colors(
        "other_palette", n=max(1, n_other_palette), exclude={minority})
    n_minority = int(overrides.get("minority_count",
                                   ctx.draw_int("minority_count", m_lo, m_hi)))
    n_minority = max(1, min(2, n_minority))  # need strict minority on 9 cells
    layout = (overrides.get("texture")
              or overrides.get("other_layout")
              or ctx.draw_choice("other_layout", list(OTHER_LAYOUTS)))

    g = full_grid(3, 3, other_palette[0])

    # Lay out the 9 - n_minority "majority" cells per layout.
    cells = [(r, c) for r in range(3) for c in range(3)]
    minority_positions = rng.sample(cells, n_minority)
    other_positions = [c for c in cells if c not in minority_positions]

    if layout == "uniform":
        # All majority same color.
        color = other_palette[0]
        for r, c in other_positions:
            g[r][c] = color
    elif layout == "two_colors" and len(other_palette) >= 2:
        a = other_palette[0]; b = other_palette[1]
        # Distribute roughly equally with a > minority count.
        rng.shuffle(other_positions)
        split = max(2 + n_minority, len(other_positions) // 2 + 1)
        for r, c in other_positions[:split]:
            g[r][c] = a
        for r, c in other_positions[split:]:
            g[r][c] = b
    elif layout == "striped":
        for r, c in other_positions:
            g[r][c] = other_palette[r % len(other_palette)]
    elif layout == "checker":
        a = other_palette[0]
        b = other_palette[1] if len(other_palette) > 1 else a
        for r, c in other_positions:
            g[r][c] = a if (r + c) % 2 == 0 else b
    elif layout == "diagonal_split":
        a = other_palette[0]
        b = other_palette[1] if len(other_palette) > 1 else a
        for r, c in other_positions:
            g[r][c] = a if r >= c else b
    else:
        for r, c in other_positions:
            g[r][c] = rng.choice(other_palette)

    for r, c in minority_positions:
        g[r][c] = minority

    # Sanity: minority must be strictly less frequent than every other color.
    counts: dict = {}
    for r in range(3):
        for c in range(3):
            counts[g[r][c]] = counts.get(g[r][c], 0) + 1
    if minority in counts:
        for color, n in counts.items():
            if color != minority and n <= counts[minority]:
                # Bump majority by overwriting one minority position.
                if minority_positions:
                    r, c = minority_positions.pop()
                    g[r][c] = color
                    counts[color] = counts.get(color, 0) + 1
                    counts[minority] -= 1
                    if counts[minority] == 0:
                        del counts[minority]
                    break
    return g


def _draw_from_degenerate(name, ctx, rng):
    """Edge-case where the minority-gated self-tile signal collapses.

    tied_minorities — two colors share the lowest count; minority is
                      ambiguous.
    monochrome      — uniform input; minority is undefined / non-existent.
    all_unique      — every cell a different color; many "minorities".
    """
    palette = ctx.draw_distinct_colors("palette", n=9)
    g = full_grid(3, 3, palette[0])
    if name == "tied_minorities":
        # Two cells of color A, two of B (tie for minority), rest a third color.
        for r in range(3):
            for c in range(3):
                g[r][c] = palette[2]
        cells = [(r, c) for r in range(3) for c in range(3)]
        rng.shuffle(cells)
        g[cells[0][0]][cells[0][1]] = palette[0]
        g[cells[1][0]][cells[1][1]] = palette[0]
        g[cells[2][0]][cells[2][1]] = palette[1]
        g[cells[3][0]][cells[3][1]] = palette[1]
        return g
    if name == "monochrome":
        color = rng.choice(palette)
        for r in range(3):
            for c in range(3):
                g[r][c] = color
        return g
    if name == "all_unique":
        rng.shuffle(palette)
        for i, color in enumerate(palette[:9]):
            g[i // 3][i % 3] = color
        return g
    return g
