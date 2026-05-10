"""Generator for 12422b43.

Rule: gray(5) markers in column 0 of top rows define source rows.
Below the visible pattern, repeat source rows cyclically with markers
erased.

Combinatorial axes (8): grid_w, source_rows, tail_rows, repeat_rows,
palette_size, fill_density, source_layout, asymmetry_force.
Degenerates: no_sources, full_sources, single_source.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "cb02d14d307f"
VERSION = "1.1.0"
TASK_ID = "cb02d14d307f"
SUMMARY = "Gray-marked source rows; rule copies them cyclically below tail."

INVARIANTS = [
    "background is 0",
    ">=1 source row (col 0 == 5) at top",
    ">=1 tail row below source rows",
    "repeat rows are all-bg below tail",
    "each source row has >=1 non-gray color cell (so output is non-trivial)",
    "no gray cells outside col 0 of source rows",
]

SOURCE_LAYOUTS = ("scattered", "blob", "diagonal", "stripes",
                  "left_biased", "right_biased")
DEGENERATE_TEXTURES = ("no_sources", "full_sources", "single_source")
HELPFUL_TEXTURES = SOURCE_LAYOUTS

AXES = {
    "grid_w":           {"type": "int", "default": "rng 5..10", "valid": "4..14"},
    "source_rows":      {"type": "int", "default": "rng 2..4", "valid": "1..6"},
    "tail_rows":        {"type": "int", "default": "rng 1..3", "valid": "0..5"},
    "repeat_rows":      {"type": "int", "default": "rng 4..10", "valid": "1..18"},
    "palette_size":     {"type": "int", "default": "rng 2..5", "valid": "1..7"},
    "fill_density":     {"type": "float", "default": "rng 0.3..0.7",
                         "valid": "0.1..1"},
    "source_layout":    {"type": "str", "default": "rng helpful",
                         "valid": "|".join(SOURCE_LAYOUTS)},
    "asymmetry_force":  {"type": "bool", "default": "false",
                         "valid": "true|false"},
    "texture":          {"type": "str", "default": "alias for source_layout",
                         "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if difficulty == "easy":
        w_lo, w_hi, sr_lo, sr_hi = 4, 6, 2, 2
    elif difficulty == "hard":
        w_lo, w_hi, sr_lo, sr_hi = 9, 14, 3, 6
    else:
        w_lo, w_hi, sr_lo, sr_hi = 5, 10, 2, 4
    w = ctx.draw_int("grid_w", w_lo, w_hi)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], w, rng)
    source_rows = int(overrides.get("source_rows",
                                    ctx.draw_int("source_rows", sr_lo, sr_hi)))
    tail_rows = int(overrides.get("tail_rows",
                                  ctx.draw_int("tail_rows", 1, 3)))
    repeat_rows = int(overrides.get("repeat_rows",
                                    ctx.draw_int("repeat_rows", 4, 10)))
    h = source_rows + tail_rows + repeat_rows
    n_palette = int(overrides.get("palette_size",
                                  ctx.draw_int("palette_size", 2, 5)))
    palette = list(ctx.draw_distinct_colors("colors",
                                            n=max(2, n_palette),
                                            exclude={0, 5}))
    layout = (overrides.get("texture") or overrides.get("source_layout")
              or ctx.draw_choice("source_layout", list(SOURCE_LAYOUTS)))
    density = float(overrides.get("fill_density",
                                  ctx.draw_rng("fill_density")
                                  .uniform(0.3, 0.7)))
    g = full_grid(h, w, 0)
    for r in range(source_rows):
        g[r][0] = 5
        cols = _source_cols(layout, w - 1, density, rng)
        for c in cols:
            if 1 + c < w:
                g[r][1 + c] = rng.choice(palette)
    for r in range(source_rows, source_rows + tail_rows):
        cols = _source_cols(layout, w - 1, density, rng)
        for c in cols:
            if 1 + c < w:
                g[r][1 + c] = rng.choice(palette)
    for r in range(source_rows):
        if not any(g[r][c] != 0 and g[r][c] != 5 for c in range(w)):
            g[r][1] = palette[0]
    return g


def _source_cols(layout, n_cols, density, rng):
    cols = list(range(n_cols))
    if layout == "blob":
        cr = rng.randint(0, n_cols - 1) if n_cols > 0 else 0
        cols.sort(key=lambda c: abs(c - cr))
        n = max(1, int(n_cols * density))
        return cols[:n]
    if layout == "diagonal":
        return cols[:1]
    if layout == "stripes":
        return [c for c in cols if c % 2 == 0]
    if layout == "left_biased":
        n = max(1, int(n_cols * density))
        return cols[:n]
    if layout == "right_biased":
        n = max(1, int(n_cols * density))
        return cols[-n:]
    rng.shuffle(cols)
    n = max(1, min(n_cols, int(n_cols * density) + 1))
    return cols[:n]


def _draw_from_degenerate(name, w, rng):
    if name == "no_sources":
        h = 8
        g = full_grid(h, w, 0)
        for r in range(2):
            color = rng.choice([1, 2, 3, 4, 6, 7, 8, 9])
            for c in range(1, w):
                if rng.random() < 0.3:
                    g[r][c] = color
        return g
    if name == "full_sources":
        h = 8
        g = full_grid(h, w, 0)
        for r in range(4):
            g[r][0] = 5
            for c in range(1, w):
                g[r][c] = rng.choice([1, 2, 3, 4, 6, 7, 8, 9])
        return g
    if name == "single_source":
        h = 6
        g = full_grid(h, w, 0)
        g[0][0] = 5
        g[0][1] = rng.choice([1, 2, 3, 4, 6, 7, 8, 9])
        for c in range(1, w):
            if rng.random() < 0.3:
                g[1][c] = rng.choice([1, 2, 3, 4, 6, 7, 8, 9])
        return g
    return [[0]]
