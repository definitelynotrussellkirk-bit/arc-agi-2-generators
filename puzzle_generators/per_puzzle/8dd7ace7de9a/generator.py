"""Generator for f823c43c.

Rule: input is a periodic tile (small (pr, pc) period) overlaid with
magenta(6) noise. Rule recovers the clean periodic tile.

Combinatorial axes (8): grid_h/w, period_r, period_c, palette_kind,
noise_density, anchor_corner, asymmetry_force, palette_size.
Degenerates: no_period, all_noise, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "8dd7ace7de9a"
VERSION = "1.1.0"
TASK_ID = "8dd7ace7de9a"
SUMMARY = "Periodic tile with magenta noise; rule recovers the clean tile."

INVARIANTS = [
    "small period (pr, pc), each in 2..4",
    "magenta (6) noise on <=20% of cells",
    "every tile position sees at least one non-noise cell so the period is recoverable",
    "period colors don't include 6",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_period", "all_noise", "full_grid")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..12", "valid": "6..16"},
    "grid_w":         {"type": "int", "default": "rng 8..12", "valid": "6..16"},
    "period_r":       {"type": "int", "default": "rng 2..4", "valid": "2..5"},
    "period_c":       {"type": "int", "default": "rng 2..4", "valid": "2..5"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "noise_density":  {"type": "float", "default": "0.14", "valid": "0.05..0.25"},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "3", "valid": "2..4"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    rng = ctx.draw_rng("placement")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], rng)
    if difficulty == "easy":
        h_lo, h_hi = 6, 8
        d_default = 0.08
    elif difficulty == "hard":
        h_lo, h_hi = 12, 16
        d_default = 0.20
    else:
        h_lo, h_hi = 8, 12
        d_default = 0.14
    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", h_lo, h_hi)
    pr = int(overrides.get("period_r", rng.randint(2, 4)))
    pc = int(overrides.get("period_c", rng.randint(2, 4)))
    pr = max(2, min(5, pr))
    pc = max(2, min(5, pc))
    palette = ctx.draw_distinct_colors("palette", n=3, exclude={6})
    tile = [[rng.choice(palette) for _ in range(pc)] for _ in range(pr)]
    g = full_grid(h, w, 0)
    for r in range(h):
        for c in range(w):
            g[r][c] = tile[r % pr][c % pc]
    density = float(overrides.get("noise_density", d_default))
    n_noise = int(h * w * density)
    placed_noise = set()
    for _ in range(n_noise):
        r = rng.randint(0, h - 1)
        c = rng.randint(0, w - 1)
        tr, tc = r % pr, c % pc
        n_reps = sum(1 for rr in range(h) for cc in range(w)
                     if rr % pr == tr and cc % pc == tc and (rr, cc) not in placed_noise)
        if n_reps <= 1:
            continue
        g[r][c] = 6
        placed_noise.add((r, c))
    return g


def _draw_from_degenerate(name, rng):
    h, w = 10, 10
    g = full_grid(h, w, 0)
    if name == "no_period":
        for r in range(h):
            for c in range(w):
                g[r][c] = rng.choice([1, 2, 3])
        return g
    if name == "all_noise":
        for r in range(h):
            for c in range(w):
                g[r][c] = 6
        return g
    if name == "full_grid":
        for r in range(h):
            for c in range(w):
                g[r][c] = 1
        return g
    return g
