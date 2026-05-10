"""Generator for puzzle e26a3af2.

Rule: noisy bands (V or H). Output cleans to pure bands using more-
coherent axis.

Combinatorial axes (8): grid_h/w, orientation, palette_kind,
palette_size, noise_density, anchor_corner, asymmetry_force,
band_pattern.
Degenerates: no_noise, all_noise, single_band.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "90082143f2ec"
VERSION = "1.1.0"
TASK_ID = "90082143f2ec"
SUMMARY = "Noisy bands; rule cleans to pure bands using more-coherent axis."

INVARIANTS = [
    "bands run along one axis (rows or cols)",
    "adjacent bands use different colors",
    "noise density < 25% so band axis dominates",
]

ORIENTATIONS = ("vertical", "horizontal", "rng")
PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_noise", "all_noise", "single_band")
HELPFUL_TEXTURES = ORIENTATIONS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..14", "valid": "6..18"},
    "grid_w":         {"type": "int", "default": "rng 8..14", "valid": "6..18"},
    "orientation":    {"type": "str", "default": "rng helpful",
                       "valid": "|".join(ORIENTATIONS)},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "palette_size":   {"type": "int", "default": "rng 2..4", "valid": "2..6"},
    "noise_density":  {"type": "float", "default": "rng 0.08..0.15",
                       "valid": "0.02..0.25"},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "texture":        {"type": "str", "default": "alias for orientation",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if difficulty == "easy":
        h_lo, h_hi = 6, 9
    elif difficulty == "hard":
        h_lo, h_hi = 14, 18
    else:
        h_lo, h_hi = 8, 14
    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", h_lo, h_hi)
    rng = ctx.draw_rng("placement")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], h, w, rng)
    orientation = (overrides.get("texture") or
                   overrides.get("orientation")
                   or ctx.draw_choice("orientation",
                                      list(ORIENTATIONS)))
    if orientation == "rng":
        orientation = rng.choice(["vertical", "horizontal"])
    palette_kind = overrides.get("palette_kind",
                                 ctx.draw_choice("palette_kind",
                                                 list(PALETTE_KINDS)))
    palette_size = int(overrides.get("palette_size",
                                     ctx.draw_int("palette_size", 2, 4)))
    palette_size = max(2, min(6, palette_size))
    palette = _build_palette(palette_kind, palette_size, rng)
    noise_d = float(overrides.get("noise_density",
                                  ctx.draw_rng("noise_density")
                                  .uniform(0.08, 0.15)))
    g = full_grid(h, w, 0)
    if orientation == "vertical":
        col_colors = []
        for c in range(w):
            choices = [p for p in palette if not col_colors or p != col_colors[-1]]
            col_colors.append(rng.choice(choices))
        for r in range(h):
            for c in range(w):
                g[r][c] = col_colors[c]
    else:
        row_colors = []
        for r in range(h):
            choices = [p for p in palette if not row_colors or p != row_colors[-1]]
            row_colors.append(rng.choice(choices))
        for r in range(h):
            for c in range(w):
                g[r][c] = row_colors[r]
    n_noise = int(h * w * noise_d)
    for _ in range(n_noise):
        r = rng.randint(0, h - 1); c = rng.randint(0, w - 1)
        others = [p for p in palette if p != g[r][c]]
        if others:
            g[r][c] = rng.choice(others)
    return g


def _build_palette(kind, n, rng):
    if kind == "warm":
        pool = [2, 3, 4, 6, 9]
    elif kind == "cool":
        pool = [1, 5, 7, 8]
    elif kind == "primary":
        pool = [1, 2, 3, 4]
    else:
        pool = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    rng.shuffle(pool)
    if len(pool) < n:
        for c in [1, 2, 3, 4, 5, 6, 7, 8, 9]:
            if c not in pool:
                pool.append(c)
            if len(pool) >= n:
                break
    return pool[:n]


def _draw_from_degenerate(name, h, w, rng):
    g = full_grid(h, w, 0)
    palette = rng.sample([1, 2, 3, 4, 5, 6, 7, 8, 9], 3)
    if name == "no_noise":
        # Pure bands
        col_colors = [palette[c % 3] for c in range(w)]
        for r in range(h):
            for c in range(w):
                g[r][c] = col_colors[c]
        return g
    if name == "all_noise":
        for r in range(h):
            for c in range(w):
                g[r][c] = rng.choice(palette)
        return g
    if name == "single_band":
        for r in range(h):
            for c in range(w):
                g[r][c] = palette[0]
        return g
    return g
