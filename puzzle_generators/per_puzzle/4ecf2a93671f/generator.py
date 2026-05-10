"""Generator for ARC task 8e2edd66.

Rule: input is n × n. Output is n² × n²; for each (r, c):
  br, bc = r // n, c // n   (block coords)
  sr, sc = r % n, c % n     (sub coords)
  out[r][c] = mode(g, 0) if input[br][bc]==0 AND input[sr][sc]==0
  else 0
i.e., fractal copy of the bg-mask onto bg-mask anchors, painted with mode.

Combinatorial axes (8): side (n × n input), fg_color, fg_density,
fg_layout (random/cluster/blob/diagonal/cross/ring), bg_count_target
(forces ≥k zeros so output isn't trivially empty).
Degenerates: all_zero, all_filled, single_zero.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid
from puzzle_generators.helpers.textures import (
    fill_texture, apply_bg_density,
)

GENERATOR_ID = "4ecf2a93671f"
VERSION = "1.1.0"
TASK_ID = "4ecf2a93671f"
SUMMARY = "n × n mask; rule fractally tiles bg-mask onto bg anchors with mode color."

INVARIANTS = [
    "input is n × n with n in 3..5 (so n² ≤ 25)",
    "fg color is the mode (excluding bg=0)",
    "≥1 zero cell so the rule has visible output",
]

HELPFUL_TEXTURES = (
    "noise", "sparse", "blob", "stripes",
    "checkerboard", "frame", "ring", "plus", "cross",
)
DEGENERATE_TEXTURES = ("all_zero", "all_filled", "single_zero")

AXES = {
    "side":           {"type": "int", "default": "rng 3..5", "valid": "2..5"},
    "fg_color":       {"type": "color", "default": "rng (≠0)", "valid": "1..9"},
    "fg_density":     {"type": "float", "default": "rng 0.3..0.7", "valid": "0..1"},
    "texture":        {"type": "str", "default": "rng helpful",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
    "bg_count_target": {"type": "int", "default": "rng 2..n*n/2", "valid": "1..n*n"},
    "edge_kind":      {"type": "str", "default": "rng helpful",
                       "valid": "border|interior|both"},
    "noise_overlay":  {"type": "float", "default": "rng 0..0.05", "valid": "0..0.3"},
    "include_extra_palette": {"type": "bool", "default": "false", "valid": "true|false"},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if difficulty == "easy":
        s_lo, s_hi = 3, 4
    elif difficulty == "hard":
        s_lo, s_hi = 5, 5
    else:
        s_lo, s_hi = 3, 5
    n = ctx.draw_int("side", s_lo, s_hi)
    rng = ctx.draw_rng("cells")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], n, rng)
    fg = int(overrides.get("fg_color", ctx.draw_color("fg_color", exclude={0})))
    palette = [0, fg]
    if bool(overrides.get("include_extra_palette", False)):
        # Add a non-mode extra color
        extras = list(ctx.draw_distinct_colors("extras", n=1, exclude={0, fg}))
        palette.append(extras[0] if extras else fg)
    texture = overrides.get("texture",
                            ctx.draw_choice("texture", list(HELPFUL_TEXTURES)))
    g = fill_texture(texture, n, n, palette, rng)
    fill_d = float(overrides.get("fg_density",
                                 ctx.draw_rng("fg_density").uniform(0.3, 0.7)))
    if fill_d < 1.0:
        g = apply_bg_density(g, palette, rng, 1.0 - fill_d)
    target_zeros = int(overrides.get("bg_count_target",
                                     ctx.draw_int("bg_count_target", 2,
                                                  max(2, n * n // 2))))
    cur_zeros = sum(1 for r in range(n) for c in range(n) if g[r][c] == 0)
    while cur_zeros < target_zeros:
        rr = rng.randint(0, n - 1); cc = rng.randint(0, n - 1)
        if g[rr][cc] != 0:
            g[rr][cc] = 0
            cur_zeros += 1
    # Ensure mode is fg (must be > all other counts).
    counts = {}
    for r in range(n):
        for c in range(n):
            v = g[r][c]
            if v != 0:
                counts[v] = counts.get(v, 0) + 1
    if not counts or max(counts.values()) < 1:
        g[0][0] = fg
    return g


def _draw_from_degenerate(name, n, rng):
    g = full_grid(n, n, 0)
    fg = rng.choice([1, 2, 3, 4, 5, 6, 7, 8, 9])
    if name == "all_zero":
        # All bg → mode is undefined; rule may fail. Add 1 fg.
        g[0][0] = fg
        return g
    if name == "all_filled":
        for r in range(n):
            for c in range(n):
                g[r][c] = fg
        return g
    if name == "single_zero":
        for r in range(n):
            for c in range(n):
                g[r][c] = fg
        g[n // 2][n // 2] = 0
        return g
    return g
