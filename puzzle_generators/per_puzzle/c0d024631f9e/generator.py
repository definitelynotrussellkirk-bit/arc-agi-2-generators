"""Generator for ARC task 3194b014.

Rule: find the 3rd-most-common non-bg color (by descending count).
Output is a 3 × 3 grid filled with that color.

Combinatorial axes (8):
  * grid_h / grid_w     — outer canvas size
  * n_colors            — distinct non-bg colors (≥3)
  * count_progression   — linear / exponential / random_distinct
                          (controls how the counts are spaced)
  * placement_pattern   — random / clustered / striped / quadrants /
                          banded
  * bg_density          — fraction of bg cells
  * gap_between_ranks   — minimum count difference between adjacent ranks
                          (ensures stable rank order)
  * 3rd_color_pick      — which color gets the rank-3 slot
                          (random / specific_color)
  * caller-opt-in degenerates: ties_for_3rd (rule's pick ambiguous),
                              fewer_than_3_colors (rule fails),
                              all_equal_counts.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "c0d024631f9e"
VERSION = "1.1.0"
TASK_ID = "c0d024631f9e"
SUMMARY = "Grid with distinct color frequencies; rule outputs 3 × 3 of the 3rd-ranked color."

INVARIANTS = [
    "background is 0",
    "≥3 distinct non-bg colors",
    "color counts are strictly distinct so rank-3 is unambiguous",
]

PROGRESSIONS = ("linear", "exponential", "random_distinct")
PLACEMENTS = ("random", "clustered", "striped", "quadrants", "banded")
DEGENERATE_TEXTURES = ("ties_for_3rd", "fewer_than_3_colors", "all_equal_counts")
HELPFUL_TEXTURES = PLACEMENTS

AXES = {
    "grid_h":             {"type": "int", "default": "rng 6..14", "valid": "5..18"},
    "grid_w":             {"type": "int", "default": "rng 6..14", "valid": "5..18"},
    "n_colors":           {"type": "int", "default": "rng 3..6", "valid": "3..9"},
    "count_progression":  {"type": "str", "default": "rng helpful",
                           "valid": "|".join(PROGRESSIONS)},
    "placement_pattern":  {"type": "str", "default": "rng helpful",
                           "valid": "|".join(PLACEMENTS)},
    "bg_density":         {"type": "float", "default": "rng 0.1..0.4", "valid": "0..0.8"},
    "gap_between_ranks":  {"type": "int", "default": "rng 2..5", "valid": "1..10"},
    "third_color_pick":   {"type": "str", "default": "rng random|specific",
                           "valid": "random|specific"},
    "texture":            {"type": "str", "default": "alias for placement_pattern",
                           "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if difficulty == "easy":
        h_lo, h_hi, n_lo, n_hi = 6, 9, 3, 4
    elif difficulty == "hard":
        h_lo, h_hi, n_lo, n_hi = 12, 14, 5, 7
    else:
        h_lo, h_hi, n_lo, n_hi = 6, 14, 3, 6
    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", h_lo, h_hi)
    rng = ctx.draw_rng("cells")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], h, w, rng)
    n_colors = int(overrides.get("n_colors", ctx.draw_int("n_colors", n_lo, n_hi)))
    n_colors = max(3, min(9, n_colors))
    progression = overrides.get("count_progression",
                                ctx.draw_choice("count_progression", list(PROGRESSIONS)))
    placement = overrides.get("placement_pattern",
                              ctx.draw_choice("placement_pattern", list(PLACEMENTS)))
    bg_d = float(overrides.get("bg_density",
                               ctx.draw_rng("bg_density").uniform(0.1, 0.4)))
    gap = int(overrides.get("gap_between_ranks",
                            ctx.draw_int("gap_between_ranks", 2, 5)))
    palette = list(ctx.draw_distinct_colors("palette", n=n_colors, exclude={0}))
    counts = _make_counts(progression, n_colors, h * w, bg_d, gap, rng)
    g = _place_with_pattern(placement, h, w, palette, counts, rng)
    return g


def _make_counts(progression, n_colors, total, bg_d, gap, rng):
    avail = max(n_colors * 2, int(total * (1 - bg_d)))
    if progression == "linear":
        base = max(2, avail // (n_colors * 2))
        counts = [base + i * gap for i in range(n_colors)]
    elif progression == "exponential":
        counts = [max(2, 2 ** (n_colors - i - 1)) + 1 for i in range(n_colors)]
    else:  # random_distinct
        counts = sorted(rng.sample(range(2, max(3, avail // n_colors + n_colors)), n_colors),
                        reverse=True)
    counts.sort(reverse=True)
    # Ensure strict order with gap
    for i in range(1, len(counts)):
        if counts[i - 1] - counts[i] < gap:
            counts[i] = max(1, counts[i - 1] - gap)
    # Cap so total ≤ available
    while sum(counts) > avail and counts[-1] > 1:
        for i in range(len(counts) - 1, -1, -1):
            if counts[i] > 1:
                counts[i] -= 1
                break
    return counts


def _place_with_pattern(pattern, h, w, palette, counts, rng):
    g = full_grid(h, w, 0)
    cells = [(r, c) for r in range(h) for c in range(w)]
    if pattern == "random":
        rng.shuffle(cells)
    elif pattern == "clustered":
        cr = rng.randint(0, h - 1); cc = rng.randint(0, w - 1)
        cells.sort(key=lambda rc: abs(rc[0] - cr) + abs(rc[1] - cc))
    elif pattern == "striped":
        cells = [(r, c) for r in range(0, h, 1) for c in range(w)]
        # Group by row: cells of color i go to row i
    elif pattern == "quadrants":
        cells.sort(key=lambda rc: (rc[0] >= h // 2, rc[1] >= w // 2))
    elif pattern == "banded":
        cells.sort(key=lambda rc: rc[0])
    cursor = 0
    for color, count in zip(palette, counts):
        for _ in range(count):
            if cursor >= len(cells):
                break
            r, c = cells[cursor]
            g[r][c] = color
            cursor += 1
    return g


def _draw_from_degenerate(name, h, w, rng):
    palette = list(range(1, 10))
    rng.shuffle(palette)
    g = full_grid(h, w, 0)
    if name == "ties_for_3rd":
        # 4 colors with ranks: 10, 7, 5, 5 — rank-3 and rank-4 tie.
        positions = [(r, c) for r in range(h) for c in range(w)]
        rng.shuffle(positions)
        for color, n in zip(palette[:4], [10, 7, 5, 5]):
            for _ in range(n):
                if not positions: break
                r, c = positions.pop()
                g[r][c] = color
        return g
    if name == "fewer_than_3_colors":
        # Only 2 distinct non-bg colors — rule has no rank-3.
        positions = [(r, c) for r in range(h) for c in range(w)]
        rng.shuffle(positions)
        for color in palette[:2]:
            for _ in range(8):
                if not positions: break
                r, c = positions.pop()
                g[r][c] = color
        return g
    if name == "all_equal_counts":
        # 4 colors with equal counts — ambiguous rank.
        positions = [(r, c) for r in range(h) for c in range(w)]
        rng.shuffle(positions)
        for color in palette[:4]:
            for _ in range(5):
                if not positions: break
                r, c = positions.pop()
                g[r][c] = color
        return g
    return g
