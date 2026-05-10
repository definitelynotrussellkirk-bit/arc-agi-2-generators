"""Generator for ARC task c3e719e8.

Rule: `(rule! (lambda (g) (self-tile g (lambda (v) (= v (mode g))))))`.
Same rule as 27f8ce4f but the canonical examples use a 3 × 3 input
exclusively. Kept independent so each task contributes its own slice.

Combinatorial axes:
  * grid_size              — kept at 3 (canonical) but axis exposed for
                             override
  * mode_color             — which color is the mode
  * minority_palette_size  — distinct minority colors (1..3)
  * minority_count         — how many cells are minority (1..4)
                             (mode count is 9 - minority_count)
  * minority_layout        — where minorities sit
  * caller-opt-in degenerates: tied_modes, monochrome, all_minority_unique
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "b09f5ee22328"
VERSION = "1.1.0"  # bumped: deeper combinatorial axes added
TASK_ID = "b09f5ee22328"
SUMMARY = "A 3 × 3 grid with a unique most-frequent color; mode cells receive tile copies."

INVARIANTS = [
    "input is 3 × 3",
    "the modal color is unique (strictly more frequent than any other)",
    "≥1 non-modal cell so the rule has visible effect",
]

MINORITY_LAYOUTS = ("random", "corner", "row", "column", "cross", "diagonal")
DEGENERATE_TEXTURES = ("tied_modes", "monochrome", "all_minority_unique")
HELPFUL_TEXTURES = MINORITY_LAYOUTS

AXES = {
    "grid_size":             {"type": "int",   "default": "3", "valid": "3..3"},
    "mode_color":            {"type": "color", "default": "rng", "valid": "0..9"},
    "minority_palette_size": {"type": "int",   "default": "rng 1..3", "valid": "1..6"},
    "minority_count":        {"type": "int",   "default": "rng 1..4", "valid": "1..8"},
    "minority_layout":       {"type": "str",   "default": "rng helpful",
                              "valid": "|".join(MINORITY_LAYOUTS)},
    "texture":               {"type": "str",   "default": "alias for minority_layout",
                              "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)

    if difficulty == "easy":
        m_lo, m_hi, p_lo, p_hi = 1, 2, 1, 1
    elif difficulty == "hard":
        m_lo, m_hi, p_lo, p_hi = 3, 4, 2, 3
    else:
        m_lo, m_hi, p_lo, p_hi = 1, 4, 1, 3

    rng = ctx.draw_rng("cells")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], ctx, rng)

    n_palette = int(overrides.get("minority_palette_size",
                                  ctx.draw_int("minority_palette_size", p_lo, p_hi)))
    palette = ctx.draw_distinct_colors("palette", n=n_palette + 1)
    mode_color = palette[0]
    minority = palette[1:] if len(palette) > 1 else palette

    n_minority = int(overrides.get("minority_count",
                                   ctx.draw_int("minority_count", m_lo, m_hi)))
    n_minority = max(1, min(4, n_minority))  # mode must remain >50% of 9
    layout = (overrides.get("texture")
              or overrides.get("minority_layout")
              or ctx.draw_choice("minority_layout", list(MINORITY_LAYOUTS)))

    g = full_grid(3, 3, mode_color)
    minority_positions = _layout_positions(layout, n_minority, rng)
    for i, (r, c) in enumerate(minority_positions):
        g[r][c] = minority[i % len(minority)]
    return g


def _layout_positions(layout, n, rng):
    if layout == "corner":
        candidates = [(0, 0), (0, 2), (2, 0), (2, 2)]
    elif layout == "row":
        r = rng.randint(0, 2)
        candidates = [(r, 0), (r, 1), (r, 2)]
    elif layout == "column":
        c = rng.randint(0, 2)
        candidates = [(0, c), (1, c), (2, c)]
    elif layout == "cross":
        candidates = [(0, 1), (1, 0), (1, 2), (2, 1)]
    elif layout == "diagonal":
        candidates = [(0, 0), (1, 1), (2, 2)] if rng.random() < 0.5 \
            else [(0, 2), (1, 1), (2, 0)]
    else:
        candidates = [(r, c) for r in range(3) for c in range(3)]
    rng.shuffle(candidates)
    return candidates[:max(0, min(n, len(candidates)))]


def _draw_from_degenerate(name, ctx, rng):
    """Edge-case where the mode-gated self-tile signal collapses.

    tied_modes          — two colors tie for most common; mode is ambiguous.
    monochrome          — uniform input; output is uniform 9 × 9.
    all_minority_unique — every non-mode cell is a unique color.
    """
    palette = ctx.draw_distinct_colors("palette", n=4)
    g = full_grid(3, 3, palette[0])
    if name == "tied_modes":
        # 4 of one color, 4 of another, 1 wild.
        cells = [(r, c) for r in range(3) for c in range(3)]
        rng.shuffle(cells)
        for i, (r, c) in enumerate(cells):
            if i < 4:
                g[r][c] = palette[0]
            elif i < 8:
                g[r][c] = palette[1]
            else:
                g[r][c] = palette[2] if len(palette) > 2 else palette[0]
        return g
    if name == "monochrome":
        color = rng.choice(palette)
        for r in range(3):
            for c in range(3):
                g[r][c] = color
        return g
    if name == "all_minority_unique":
        # Mode at center + 4 mode neighbors; minorities each unique.
        for r in range(3):
            for c in range(3):
                g[r][c] = palette[0]
        unique_cells = [(0, 0), (0, 2), (2, 0), (2, 2)]
        rng.shuffle(unique_cells)
        for i, (r, c) in enumerate(unique_cells[:min(3, len(palette) - 1)]):
            g[r][c] = palette[1 + i]
        return g
    return g
