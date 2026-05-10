"""Generator for ARC task 5582e5ca.

Rule: `(rule! (lambda (g) (let ((m (mode g))) (grid-from-fn (rows g) (cols g) (lambda (r c) m)))))`.
Fill the whole grid with the (nonzero) mode color.

Combinatorial axes:
  * grid_h / grid_w        — outer canvas size
  * mode_color             — the dominant color (will become output)
  * mode_density           — fraction of cells that are the mode
  * distractor_palette_size — number of other (non-mode) colors
  * distractor_layout      — random / clustered / striped / one_each /
                             border / corners
  * include_bg             — bool: should bg(0) appear among the cells
  * caller-opt-in degenerates: monochrome (input == output),
                               tied_modes (rule's "unique mode" assumption
                               breaks),
                               only_bg_and_one_mode (visually trivial)
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "8b0844e3951e"
VERSION = "1.1.0"  # bumped: deeper combinatorial axes added
TASK_ID = "8b0844e3951e"
SUMMARY = "Multicolor grid with one dominant nonzero color; output is the entire grid in that color."

INVARIANTS = [
    "there is a unique most-common nonzero color",
    "at least one non-mode cell appears so the output changes from input",
    "zero may appear but does not count toward the mode",
]

DISTRACTOR_LAYOUTS = ("random", "clustered", "striped", "one_each", "border", "corners")
DEGENERATE_TEXTURES = ("monochrome", "tied_modes", "only_bg_and_one_mode")
HELPFUL_TEXTURES = DISTRACTOR_LAYOUTS

AXES = {
    "grid_h":                {"type": "int",   "default": "rng 3..12", "valid": "1..18"},
    "grid_w":                {"type": "int",   "default": "rng 3..12", "valid": "1..18"},
    "mode_color":            {"type": "color", "default": "rng",       "valid": "1..9"},
    "mode_density":          {"type": "float", "default": "rng 0.5..0.85", "valid": "0.4..0.95"},
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

    mode_color = int(overrides.get("mode_color",
                                   ctx.draw_color("mode_color", exclude={0})))
    n_distractors = int(overrides.get("distractor_palette_size",
                                      ctx.draw_int("distractor_palette_size", p_lo, p_hi)))
    distractors = list(ctx.draw_distinct_colors(
        "distractors", n=max(1, n_distractors), exclude={0, mode_color}))
    density = float(overrides.get(
        "mode_density",
        ctx.draw_rng("mode_density").uniform(0.5, 0.85)))
    layout = (overrides.get("texture")
              or overrides.get("distractor_layout")
              or ctx.draw_choice("distractor_layout", list(DISTRACTOR_LAYOUTS)))
    include_bg = bool(overrides.get(
        "include_bg",
        ctx.draw_choice("include_bg", [True, False])))

    g = full_grid(h, w, mode_color)
    n_cells = h * w
    n_other = max(1, n_cells - max(int(n_cells * density),
                                   n_cells // 2 + 1))
    positions = _layout_positions(layout, h, w, n_other, rng)
    other_colors = distractors + ([0] if include_bg else [])
    if not other_colors:
        other_colors = distractors or [3]
    for i, (r, c) in enumerate(positions):
        g[r][c] = other_colors[i % len(other_colors)]

    # Sanity: mode must be strictly the unique most-common nonzero color.
    counts: dict = {}
    for r in range(h):
        for c in range(w):
            v = g[r][c]
            if v != 0:
                counts[v] = counts.get(v, 0) + 1
    if mode_color not in counts:
        g[0][0] = mode_color
        counts[mode_color] = counts.get(mode_color, 0) + 1
    max_other = max((n for v, n in counts.items() if v != mode_color),
                    default=0)
    if counts[mode_color] <= max_other:
        for r in range(h):
            for c in range(w):
                if g[r][c] != mode_color and g[r][c] != 0:
                    g[r][c] = mode_color
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
    if layout == "striped":
        chosen = []
        for r in range(0, h, 2):
            for c in range(w):
                chosen.append((r, c))
        rng.shuffle(chosen)
        return chosen[:n]
    if layout == "border":
        chosen = [(r, c) for r in range(h) for c in range(w)
                  if r in {0, h - 1} or c in {0, w - 1}]
        rng.shuffle(chosen)
        return chosen[:n]
    if layout == "corners":
        chosen = [(0, 0), (0, w - 1), (h - 1, 0), (h - 1, w - 1)]
        rng.shuffle(chosen)
        return chosen[:n]
    if layout == "one_each":
        rng.shuffle(cells)
        return cells[:n]
    rng.shuffle(cells)
    return cells[:n]


def _draw_from_degenerate(name, h, w, ctx, rng):
    """Edge-case where the mode-fill signal collapses.

    monochrome           — uniform input → output equals input;
                            rule is invisible.
    tied_modes           — two colors share the highest count; "unique
                            mode" assumption breaks.
    only_bg_and_one_mode — only mode color and bg(0) — minimal signal,
                            output is uniform mode color.
    """
    mode_color = ctx.draw_color("mode_color", exclude={0})
    g = full_grid(h, w, mode_color)
    if name == "monochrome":
        return g
    if name == "tied_modes":
        other = ctx.draw_color("other", exclude={0, mode_color})
        cells = [(r, c) for r in range(h) for c in range(w)]
        rng.shuffle(cells)
        half = len(cells) // 2
        for r, c in cells[:half]:
            g[r][c] = mode_color
        for r, c in cells[half:half * 2]:
            g[r][c] = other
        return g
    if name == "only_bg_and_one_mode":
        for r in range(h):
            for c in range(w):
                g[r][c] = 0 if rng.random() < 0.4 else mode_color
        g[0][0] = mode_color  # ensure ≥1 mode cell
        return g
    return g
