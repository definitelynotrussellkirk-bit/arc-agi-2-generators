"""Generator for ARC task 9caf5b84.

Rule: identify the two most frequent colors. Recolor everything that's
NOT in the top-2 to color 7.

Combinatorial axes (8): grid_h/w, palette_size, top1_count, top2_count,
minor_distribution, color_layout, decoy_palette_size, separation_buffer.
Degenerates: monochrome, top_two_only, all_distinct.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "1563be9f6591"
VERSION = "1.1.0"
TASK_ID = "1563be9f6591"
SUMMARY = "Multicolor grid with two dominant colors; non-dominant colors map to 7."

INVARIANTS = [
    "the two dominant colors have STRICTLY higher counts than the rest",
    "the gap between count(top1)+count(top2) and the next color is >=1",
    "at least one non-dominant color appears (so rule has a visible effect)",
    "color 7 does NOT appear in input (avoid ambiguity with replacement target)",
]

COLOR_LAYOUTS = ("random", "stripes", "block", "checker", "gradient")
MINOR_DISTRIBUTIONS = ("uniform", "ascending", "single_minor", "long_tail")
DEGENERATE_TEXTURES = ("monochrome", "top_two_only", "all_distinct")
HELPFUL_TEXTURES = COLOR_LAYOUTS

AXES = {
    "grid_h":             {"type": "int", "default": "rng 5..10", "valid": "3..14"},
    "grid_w":             {"type": "int", "default": "rng 5..10", "valid": "3..14"},
    "palette_size":       {"type": "int", "default": "rng 3..6",  "valid": "3..9"},
    "top1_fraction":      {"type": "float", "default": "rng 0.30..0.45",
                           "valid": "0.2..0.7"},
    "top2_fraction":      {"type": "float", "default": "rng 0.20..0.30",
                           "valid": "0.15..0.5"},
    "minor_distribution": {"type": "str", "default": "rng helpful",
                           "valid": "|".join(MINOR_DISTRIBUTIONS)},
    "color_layout":       {"type": "str", "default": "rng helpful",
                           "valid": "|".join(COLOR_LAYOUTS)},
    "texture":            {"type": "str", "default": "alias for color_layout",
                           "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index, version=VERSION,
                  task_id=TASK_ID, difficulty=difficulty, overrides=overrides)
    if difficulty == "easy":
        h_lo, h_hi, c_lo, c_hi = 4, 6, 3, 4
    elif difficulty == "hard":
        h_lo, h_hi, c_lo, c_hi = 9, 12, 5, 7
    else:
        h_lo, h_hi, c_lo, c_hi = 5, 10, 3, 6
    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", h_lo, h_hi)
    rng = ctx.draw_rng("cells")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], h, w, rng)
    n_colors = int(overrides.get("palette_size",
                                 ctx.draw_int("palette_size", c_lo, c_hi)))
    n_colors = max(3, min(7, n_colors))
    palette = list(ctx.draw_distinct_colors("palette", n=n_colors, exclude={7}))
    layout = (overrides.get("texture") or overrides.get("color_layout")
              or ctx.draw_choice("color_layout", list(COLOR_LAYOUTS)))
    minor_dist = overrides.get("minor_distribution",
                               ctx.draw_choice("minor_distribution",
                                               list(MINOR_DISTRIBUTIONS)))
    top1_f = float(overrides.get("top1_fraction",
                                 ctx.draw_rng("top1_fraction").uniform(0.30, 0.45)))
    top2_f = float(overrides.get("top2_fraction",
                                 ctx.draw_rng("top2_fraction").uniform(0.20, 0.30)))
    total = h * w
    n_top1 = max(2, int(total * top1_f))
    n_top2 = max(2, int(total * top2_f))
    if n_top1 <= n_top2:
        n_top1 = n_top2 + 1
    rem = max(0, total - n_top1 - n_top2)
    minors = palette[2:]
    minor_counts = _draw_minor_counts(minor_dist, len(minors), rem, rng)
    while sum(minor_counts) < rem:
        minor_counts[0] += 1
    while sum(minor_counts) > rem:
        for i in range(len(minor_counts) - 1, -1, -1):
            if minor_counts[i] > 0:
                minor_counts[i] -= 1
                break
    max_minor = max(minor_counts) if minor_counts else 0
    if max_minor >= n_top2:
        n_top2 = max_minor + 1
        diff = (n_top1 + n_top2 + sum(minor_counts)) - total
        if diff > 0:
            n_top1 -= diff
        if n_top1 <= n_top2:
            return _draw_from_degenerate("top_two_only", h, w, rng)
    values = [palette[0]] * n_top1 + [palette[1]] * n_top2
    for i, count in enumerate(minor_counts):
        values += [minors[i]] * count
    while len(values) < total:
        values.append(palette[0])
    g = _layout_grid(layout, h, w, values, palette, rng)
    return g


def _draw_minor_counts(dist, n_minors, total, rng):
    if n_minors == 0 or total == 0:
        return [0] * n_minors
    if dist == "single_minor":
        counts = [0] * n_minors
        counts[0] = total
        return counts
    if dist == "ascending":
        counts = [(i + 1) for i in range(n_minors)]
        s = sum(counts)
        counts = [(c * total) // s for c in counts]
        return counts
    if dist == "long_tail":
        counts = [0] * n_minors
        counts[0] = total // 2
        for i in range(1, n_minors):
            counts[i] = max(1, total // (4 * i))
        return counts
    base = total // max(1, n_minors)
    counts = [base] * n_minors
    return counts


def _layout_grid(layout, h, w, values, palette, rng):
    g = full_grid(h, w, palette[0])
    if layout == "stripes":
        rng.shuffle(values)
        idx = 0
        for r in range(h):
            for c in range(w):
                g[r][c] = values[idx % len(values)]
                idx += 1
        return g
    if layout == "block":
        idx = 0
        for r in range(h):
            for c in range(w):
                if idx < len(values):
                    g[r][c] = values[idx]
                    idx += 1
        return g
    if layout == "checker":
        rng.shuffle(values)
        idx = 0
        for r in range(h):
            for c in range(w):
                g[r][c] = values[idx]
                idx = (idx + 1) % len(values)
        return g
    if layout == "gradient":
        idx = 0
        for r in range(h):
            for c in range(w):
                g[r][c] = values[(r + c) % len(values)] if values else palette[0]
                idx += 1
        return g
    rng.shuffle(values)
    for idx, v in enumerate(values):
        g[idx // w][idx % w] = v
    return g


def _draw_from_degenerate(name, h, w, rng):
    palette = [c for c in range(1, 10) if c != 7]
    rng.shuffle(palette)
    if name == "monochrome":
        return full_grid(h, w, palette[0])
    if name == "top_two_only":
        c1, c2 = palette[0], palette[1]
        g = full_grid(h, w, c1)
        for r in range(h):
            for c in range(w):
                g[r][c] = c1 if (r + c) % 3 < 2 else c2
        return g
    if name == "all_distinct":
        g = full_grid(h, w, palette[0])
        idx = 0
        for r in range(h):
            for c in range(w):
                g[r][c] = palette[idx % len(palette)]
                idx += 1
        return g
    return [[0]]
