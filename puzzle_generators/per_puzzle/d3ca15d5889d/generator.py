"""Generator for ARC task 9565186b.

Rule: keep the nonzero mode color, map every other (non-bg) cell to 5.

Combinatorial axes:
  * grid_h / grid_w        — outer canvas size
  * keep_color             — the mode color (will survive the rule)
  * mode_density           — fraction of cells that are the mode color
                             (must be > all other colors individually)
  * distractor_palette_size — number of distinct distractor colors (1..4)
  * distractor_layout      — random / clustered / one_each / striped
  * include_bg             — bool: should bg(0) appear among the cells
  * caller-opt-in degenerates: monochrome (only mode → output all mode),
                               tied_modes (rule's "unique mode" assumption
                               breaks),
                               no_distractors (rule no-op for fg)
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "d3ca15d5889d"
VERSION = "1.1.0"  # bumped: deeper combinatorial axes added
TASK_ID = "d3ca15d5889d"
SUMMARY = "Grid with a unique most-common nonzero color; non-mode cells become gray(5)."

INVARIANTS = [
    "there is a unique most-common nonzero color",
    "at least one non-mode cell appears",
    "zero may appear but does not count toward the mode",
]

DISTRACTOR_LAYOUTS = ("random", "clustered", "one_each", "striped", "border")
DEGENERATE_TEXTURES = ("monochrome", "tied_modes", "no_distractors")
HELPFUL_TEXTURES = DISTRACTOR_LAYOUTS

AXES = {
    "grid_h":                {"type": "int",   "default": "rng 3..12", "valid": "1..18"},
    "grid_w":                {"type": "int",   "default": "rng 3..12", "valid": "1..18"},
    "keep_color":            {"type": "color", "default": "rng",       "valid": "1..9 (≠5)"},
    "mode_density":          {"type": "float", "default": "rng 0.5..0.85",
                              "valid": "0.4..0.95"},
    "distractor_palette_size": {"type": "int", "default": "rng 1..3",  "valid": "1..6"},
    "distractor_layout":     {"type": "str",   "default": "rng helpful",
                              "valid": "|".join(DISTRACTOR_LAYOUTS)},
    "include_bg":            {"type": "bool",  "default": "rng",       "valid": "true|false"},
    "texture":               {"type": "str",   "default": "alias for distractor_layout",
                              "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)

    if difficulty == "easy":
        h_lo, h_hi, p_lo, p_hi = 3, 5, 1, 1
    elif difficulty == "hard":
        h_lo, h_hi, p_lo, p_hi = 9, 12, 3, 4
    else:
        h_lo, h_hi, p_lo, p_hi = 3, 12, 1, 3

    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", h_lo, h_hi)
    rng = ctx.draw_rng("cells")

    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], h, w, ctx, rng)

    keep = int(overrides.get("keep_color",
                             ctx.draw_color("keep_color", exclude={0, 5})))
    n_distractors = int(overrides.get("distractor_palette_size",
                                      ctx.draw_int("distractor_palette_size", p_lo, p_hi)))
    distractors = ctx.draw_distinct_colors(
        "distractors", n=max(1, n_distractors), exclude={0, 5, keep})
    density = float(overrides.get(
        "mode_density",
        ctx.draw_rng("mode_density").uniform(0.5, 0.85)))
    layout = (overrides.get("texture")
              or overrides.get("distractor_layout")
              or ctx.draw_choice("distractor_layout", list(DISTRACTOR_LAYOUTS)))
    include_bg = bool(overrides.get(
        "include_bg",
        ctx.draw_choice("include_bg", [True, False])))

    g = full_grid(h, w, keep)
    n_cells = h * w
    n_other_total = max(1, n_cells - max(int(n_cells * density),
                                         n_cells // 2 + 1))

    positions = _layout_positions(layout, h, w, n_other_total, rng)
    other_colors = list(distractors) + ([0] if include_bg else [])
    if not other_colors:
        other_colors = list(distractors) or [3]
    for i, (r, c) in enumerate(positions):
        g[r][c] = other_colors[i % len(other_colors)]

    # Sanity: keep must remain strictly the mode of the nonzero cells.
    nonzero_counts: dict = {}
    for r in range(h):
        for c in range(w):
            v = g[r][c]
            if v != 0:
                nonzero_counts[v] = nonzero_counts.get(v, 0) + 1
    if not nonzero_counts:
        g[0][0] = keep
    elif keep not in nonzero_counts:
        g[0][0] = keep
    else:
        max_other = max((n for v, n in nonzero_counts.items() if v != keep),
                        default=0)
        if nonzero_counts[keep] <= max_other:
            for r in range(h):
                for c in range(w):
                    if g[r][c] != keep:
                        g[r][c] = keep
                        return g
    return g


def _layout_positions(layout, h, w, n, rng):
    if n <= 0:
        return []
    cells = [(r, c) for r in range(h) for c in range(w)]
    if layout == "clustered":
        cr = rng.randint(0, h - 1); cc = rng.randint(0, w - 1)
        cells.sort(key=lambda rc: abs(rc[0] - cr) + abs(rc[1] - cc))
        return cells[:n]
    if layout == "one_each":
        rng.shuffle(cells)
        return cells[:n]
    if layout == "striped":
        chosen = []
        for r in range(h):
            if r % 2 == 0:
                for c in range(w):
                    chosen.append((r, c))
        rng.shuffle(chosen)
        return chosen[:n]
    if layout == "border":
        chosen = [(r, c) for r in range(h) for c in range(w)
                  if r in {0, h - 1} or c in {0, w - 1}]
        rng.shuffle(chosen)
        return chosen[:n]
    rng.shuffle(cells)
    return cells[:n]


def _draw_from_degenerate(name, h, w, ctx, rng):
    """Edge-case where the keep-mode-recolor signal is hidden.

    monochrome     — every fg cell is the mode → output is identical
                     (rule has nothing to recolor).
    tied_modes     — two colors tie for most-common; the rule's "unique
                     mode" assumption breaks (output is implementation-dep).
    no_distractors — only mode and bg(0) appear; output equals input.
    """
    keep = ctx.draw_color("keep_color", exclude={0, 5})
    distractors = ctx.draw_distinct_colors(
        "distractors", n=2, exclude={0, 5, keep})
    g = full_grid(h, w, keep)
    if name == "monochrome":
        return g
    if name == "tied_modes":
        cells = [(r, c) for r in range(h) for c in range(w)]
        rng.shuffle(cells)
        # Half mode, half tie color
        half = len(cells) // 2
        for r, c in cells[:half]:
            g[r][c] = keep
        for r, c in cells[half:half * 2]:
            g[r][c] = distractors[0]
        return g
    if name == "no_distractors":
        for r in range(h):
            for c in range(w):
                g[r][c] = 0 if rng.random() < 0.4 else keep
        # ensure ≥1 keep cell
        g[0][0] = keep
        return g
    return g
