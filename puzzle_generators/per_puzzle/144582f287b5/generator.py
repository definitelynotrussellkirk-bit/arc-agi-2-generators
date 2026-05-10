"""Generator for ARC task 66e6c45b.

Rule: output is h × w with corners set to specific input cells:
  out[0][0]    = g[1][1]
  out[0][w-1]  = g[1][2]
  out[h-1][0]  = g[2][1]
  out[h-1][w-1] = g[2][2]
All other output cells = 0.

Combinatorial axes (8): grid_h/w, center_palette_size,
center_color_distinctness, decoy_density, decoy_palette_size,
center_pattern (mixed_4 / two_pairs / one_color / clockwise_distinct),
include_zero_in_center, decoy_layout.
Degenerates: all_zero_center, monochrome, single_corner.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "144582f287b5"
VERSION = "1.1.0"
TASK_ID = "144582f287b5"
SUMMARY = "Center 2 × 2 (rows/cols 1-2) becomes the 4 output corners; all else 0."

INVARIANTS = [
    "h ≥ 4 and w ≥ 4",
    "≥1 center cell ≠ 0 so output has ≥1 non-zero corner",
]

CENTER_PATTERNS = ("mixed_4", "two_pairs", "one_color", "clockwise_distinct",
                   "diagonal_match")
DECOY_LAYOUTS = ("random", "border_only", "row_band", "blob")
DEGENERATE_TEXTURES = ("all_zero_center", "monochrome", "single_corner")
HELPFUL_TEXTURES = CENTER_PATTERNS

AXES = {
    "grid_h":            {"type": "int", "default": "rng 4..14", "valid": "4..18"},
    "grid_w":            {"type": "int", "default": "rng 4..14", "valid": "4..18"},
    "center_palette_size": {"type": "int", "default": "rng 1..4", "valid": "1..6"},
    "center_pattern":    {"type": "str", "default": "rng helpful",
                          "valid": "|".join(CENTER_PATTERNS)},
    "decoy_density":     {"type": "float", "default": "rng 0..0.2", "valid": "0..0.5"},
    "decoy_palette_size": {"type": "int", "default": "rng 0..3", "valid": "0..6"},
    "decoy_layout":      {"type": "str", "default": "rng helpful",
                          "valid": "|".join(DECOY_LAYOUTS)},
    "include_zero_in_center": {"type": "bool", "default": "false", "valid": "true|false"},
    "texture":           {"type": "str", "default": "alias for center_pattern",
                          "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if difficulty == "easy":
        h_lo, h_hi = 4, 6
    elif difficulty == "hard":
        h_lo, h_hi = 11, 14
    else:
        h_lo, h_hi = 4, 14
    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", h_lo, h_hi)
    rng = ctx.draw_rng("cells")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], h, w, rng)
    n_palette = int(overrides.get("center_palette_size",
                                  ctx.draw_int("center_palette_size", 1, 4)))
    palette = list(ctx.draw_distinct_colors("palette", n=max(1, n_palette), exclude={0}))
    pattern = (overrides.get("texture") or overrides.get("center_pattern")
               or ctx.draw_choice("center_pattern", list(CENTER_PATTERNS)))
    decoy_d = float(overrides.get("decoy_density",
                                  ctx.draw_rng("decoy_density").uniform(0.0, 0.2)))
    n_decoy = int(overrides.get("decoy_palette_size",
                                ctx.draw_int("decoy_palette_size", 0, 3)))
    decoy_layout = overrides.get("decoy_layout",
                                 ctx.draw_choice("decoy_layout", list(DECOY_LAYOUTS)))
    include_zero = bool(overrides.get("include_zero_in_center", False))
    g = full_grid(h, w, 0)
    center = _make_center(pattern, palette, include_zero, rng)
    g[1][1], g[1][2] = center[0], center[1]
    g[2][1], g[2][2] = center[2], center[3]
    decoy_palette = [c for c in range(1, 10)]
    rng.shuffle(decoy_palette)
    decoy_palette = decoy_palette[:max(0, n_decoy)]
    if decoy_palette:
        cells = _decoy_cells(decoy_layout, h, w, rng)
        for r, c in cells:
            if (r, c) in {(1, 1), (1, 2), (2, 1), (2, 2)}:
                continue
            if rng.random() < decoy_d:
                g[r][c] = rng.choice(decoy_palette)
    return g


def _make_center(pattern, palette, include_zero, rng):
    if pattern == "mixed_4":
        chosen = list(palette[:4])
        while len(chosen) < 4:
            chosen.append(rng.choice(palette))
        if include_zero:
            chosen[rng.randint(0, 3)] = 0
        return chosen
    if pattern == "two_pairs":
        a = palette[0]; b = palette[1] if len(palette) > 1 else a
        return [a, b, b, a]
    if pattern == "one_color":
        return [palette[0]] * 4
    if pattern == "clockwise_distinct":
        chosen = list(palette[:4]) if len(palette) >= 4 else palette + [palette[0]] * (4 - len(palette))
        return chosen
    if pattern == "diagonal_match":
        a = palette[0]; b = palette[1] if len(palette) > 1 else a
        return [a, b, b, a]  # both diagonals share colors
    return [rng.choice(palette) for _ in range(4)]


def _decoy_cells(layout, h, w, rng):
    if layout == "random":
        cells = [(r, c) for r in range(h) for c in range(w)]
        rng.shuffle(cells)
        return cells
    if layout == "border_only":
        return [(r, c) for r in range(h) for c in range(w)
                if r in (0, h - 1) or c in (0, w - 1)]
    if layout == "row_band":
        r = rng.randint(3, h - 1)
        return [(r, c) for c in range(w)]
    if layout == "blob":
        cr, cc = rng.randint(3, h - 1), rng.randint(3, w - 1)
        return [(r, c) for r in range(max(0, cr - 1), min(h, cr + 2))
                for c in range(max(0, cc - 1), min(w, cc + 2))]
    return [(r, c) for r in range(h) for c in range(w)]


def _draw_from_degenerate(name, h, w, rng):
    palette = list(range(1, 10))
    rng.shuffle(palette)
    g = full_grid(h, w, 0)
    if name == "all_zero_center":
        # Center all 0 → output all 0.
        return g
    if name == "monochrome":
        c0 = palette[0]
        for r in range(h):
            for c in range(w):
                g[r][c] = c0
        return g
    if name == "single_corner":
        # Only one center cell non-zero — output has only 1 corner.
        g[1][1] = palette[0]
        return g
    return g
