"""Generator for 3ac3eb23.

Rule: top-row seeds expand into vertical zigzags. Even rows: seed
straight down. Odd rows: split left/right.

Combinatorial axes (8): grid_h/w, n_seeds, palette_size, seed_layout,
position_bias, palette_kind, seed_separation, anchor_endpoints.
Degenerates: no_seeds, single_seed, all_seeds.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "329d82eaaa63"
VERSION = "1.1.0"
TASK_ID = "329d82eaaa63"
SUMMARY = "Nonzero top-row seeds; rule expands them as zigzags downward."

INVARIANTS = [
    "only row 0 contains nonzero input cells",
    ">=2 seeds (so multiple zigzags)",
    "seeds separated by >=3 cols (so zigzags don't conflict)",
    "all seed colors are nonzero",
]

SEED_LAYOUTS = ("evenly_spaced", "left_biased", "right_biased",
                "scattered", "edges")
PALETTE_KINDS = ("warm", "cool", "broad", "small")
DEGENERATE_TEXTURES = ("no_seeds", "single_seed", "all_seeds")
HELPFUL_TEXTURES = SEED_LAYOUTS

AXES = {
    "grid_h":           {"type": "int", "default": "rng 5..14", "valid": "3..18"},
    "grid_w":           {"type": "int", "default": "rng 7..18", "valid": "5..22"},
    "n_seeds":          {"type": "int", "default": "rng 2..5", "valid": "1..8"},
    "palette_size":     {"type": "int", "default": "rng 2..5", "valid": "1..7"},
    "seed_layout":      {"type": "str", "default": "rng helpful",
                         "valid": "|".join(SEED_LAYOUTS)},
    "palette_kind":     {"type": "str", "default": "rng helpful",
                         "valid": "|".join(PALETTE_KINDS)},
    "seed_separation":  {"type": "int", "default": "3", "valid": "2..5"},
    "anchor_endpoints": {"type": "bool", "default": "false",
                         "valid": "true|false"},
    "texture":          {"type": "str", "default": "alias for seed_layout",
                         "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index, version=VERSION,
                  task_id=TASK_ID, difficulty=difficulty, overrides=overrides)
    if difficulty == "easy":
        h_lo, h_hi, w_lo, w_hi = 3, 6, 5, 9
    elif difficulty == "hard":
        h_lo, h_hi, w_lo, w_hi = 12, 18, 14, 22
    else:
        h_lo, h_hi, w_lo, w_hi = 5, 14, 7, 18
    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", w_lo, w_hi)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], h, w, rng)
    n_seeds = int(overrides.get("n_seeds",
                                ctx.draw_int("n_seeds", 2, 5)))
    n_seeds = max(2, min(8, n_seeds))
    layout = (overrides.get("texture") or overrides.get("seed_layout")
              or ctx.draw_choice("seed_layout", list(SEED_LAYOUTS)))
    palette_kind = overrides.get("palette_kind",
                                 ctx.draw_choice("palette_kind",
                                                 list(PALETTE_KINDS)))
    if palette_kind == "warm":
        pool = [3, 4, 6, 9]
    elif palette_kind == "cool":
        pool = [1, 5, 7, 8]
    elif palette_kind == "small":
        pool = [1, 2, 3]
    else:
        pool = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    rng.shuffle(pool)
    n_palette = int(overrides.get("palette_size",
                                  ctx.draw_int("palette_size", 2, 5)))
    palette = pool[:max(2, n_palette)]
    sep = int(overrides.get("seed_separation", 3))
    cols = _layout_cols(layout, w, n_seeds, sep, rng)
    g = full_grid(h, w, 0)
    if len(cols) < 2:
        cols = [1, w - 2]
    for i, c in enumerate(cols):
        g[0][c] = palette[i % len(palette)]
    if bool(overrides.get("anchor_endpoints", False)):
        g[0][0] = palette[0]
    return g


def _layout_cols(layout, w, n, sep, rng):
    if layout == "evenly_spaced":
        step = max(sep, w // (n + 1))
        cols = [step * (i + 1) for i in range(n) if step * (i + 1) < w - 1]
        return cols
    if layout == "left_biased":
        return [1 + i * sep for i in range(n) if 1 + i * sep < w - 1]
    if layout == "right_biased":
        return [w - 2 - i * sep for i in range(n) if w - 2 - i * sep > 0][::-1]
    if layout == "edges":
        cols = [1, w - 2]
        if n > 2:
            mid = list(range(2, w - 2, sep))
            rng.shuffle(mid)
            cols += mid[:n - 2]
        return sorted(cols[:n])
    cols = list(range(1, w - 1))
    rng.shuffle(cols)
    chosen = []
    for col in cols:
        if all(abs(col - prev) >= sep for prev in chosen):
            chosen.append(col)
            if len(chosen) == n:
                break
    return sorted(chosen)


def _draw_from_degenerate(name, h, w, rng):
    g = full_grid(h, w, 0)
    color = rng.choice([1, 2, 3, 4, 5, 6, 7, 8, 9])
    if name == "no_seeds":
        return g
    if name == "single_seed":
        g[0][w // 2] = color
        return g
    if name == "all_seeds":
        for c in range(0, w):
            g[0][c] = rng.choice([1, 2, 3, 4, 5, 6, 7, 8, 9])
        return g
    return g
