"""Generator for puzzle feca6190.

Rule: input is 1 × w with nz non-zero cells. Output is (nz*w) × (nz*w):
each output[r][c] = g[0][idx] if 0 ≤ idx = c - (sz-1) + r < w, else 0.
Diagonal extension from row 0 — each non-bg cell makes a diagonal stripe.

Combinatorial axes (8): grid_w, nz_count, palette_size,
nz_layout (random/clustered/spread/edges/regular), nz_color_distribution,
nz_position_bias (left/right/center/spread), bg_decoy_density.
Degenerates: all_zero, all_filled, single_nz.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "82bce7d23c06"
VERSION = "1.1.0"
TASK_ID = "82bce7d23c06"
SUMMARY = "1 × w input; rule projects each non-bg cell into a diagonal of (nz*w)×(nz*w) output."

INVARIANTS = [
    "h = 1",
    "bg = 0",
    "1 ≤ nz ≤ w and nz * w ≤ 30",
]

NZ_LAYOUTS = ("random", "clustered", "spread", "edges", "regular_spaced")
NZ_BIASES = ("left", "right", "center", "spread")
NZ_COLOR_DISTS = ("all_distinct", "two_colors", "single_color")
DEGENERATE_TEXTURES = ("all_zero", "all_filled", "single_nz")
HELPFUL_TEXTURES = NZ_LAYOUTS

AXES = {
    "grid_w":           {"type": "int", "default": "rng 2..7", "valid": "2..10"},
    "nz_count":         {"type": "int", "default": "rng 1..min(w,5)", "valid": "1..min(w,7)"},
    "palette_size":     {"type": "int", "default": "rng 1..nz", "valid": "1..9"},
    "nz_layout":        {"type": "str", "default": "rng helpful",
                         "valid": "|".join(NZ_LAYOUTS)},
    "nz_color_dist":    {"type": "str", "default": "rng helpful",
                         "valid": "|".join(NZ_COLOR_DISTS)},
    "nz_position_bias": {"type": "str", "default": "rng helpful",
                         "valid": "|".join(NZ_BIASES)},
    "include_zero_decoy": {"type": "bool", "default": "false", "valid": "true|false"},
    "texture":          {"type": "str", "default": "alias for nz_layout",
                         "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if difficulty == "easy":
        w_lo, w_hi = 2, 4
    elif difficulty == "hard":
        w_lo, w_hi = 6, 7
    else:
        w_lo, w_hi = 2, 7
    w = ctx.draw_int("grid_w", w_lo, w_hi)
    rng = ctx.draw_rng("placement")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], w, rng)
    max_nz = min(w, 5, 30 // w)
    nz = int(overrides.get("nz_count", ctx.draw_int("nz_count", 1, max(1, max_nz))))
    nz = max(1, min(max_nz, nz))
    layout = (overrides.get("texture") or overrides.get("nz_layout")
              or ctx.draw_choice("nz_layout", list(NZ_LAYOUTS)))
    color_dist = overrides.get("nz_color_dist",
                               ctx.draw_choice("nz_color_dist", list(NZ_COLOR_DISTS)))
    bias = overrides.get("nz_position_bias",
                         ctx.draw_choice("nz_position_bias", list(NZ_BIASES)))
    palette = list(ctx.draw_distinct_colors("palette", n=max(1, nz), exclude={0}))
    locs = _layout_positions(layout, bias, w, nz, rng)
    g = full_grid(1, w, 0)
    if color_dist == "all_distinct":
        for i, j in enumerate(locs):
            g[0][j] = palette[i % len(palette)]
    elif color_dist == "two_colors":
        a = palette[0]; b = palette[1] if len(palette) > 1 else a
        for i, j in enumerate(locs):
            g[0][j] = a if i % 2 == 0 else b
    else:
        for j in locs:
            g[0][j] = palette[0]
    return g


def _layout_positions(layout, bias, w, nz, rng):
    candidates = list(range(w))
    if bias == "left":
        candidates = list(range(0, max(1, w // 2)))
    elif bias == "right":
        candidates = list(range(max(0, w // 2), w))
    elif bias == "center":
        candidates = list(range(max(0, w // 4), max(1, 3 * w // 4)))
    if not candidates:
        candidates = list(range(w))
    if layout == "clustered":
        center = candidates[len(candidates) // 2]
        candidates.sort(key=lambda c: abs(c - center))
        return candidates[:nz]
    if layout == "spread":
        step = max(1, len(candidates) // nz)
        return candidates[::step][:nz]
    if layout == "edges":
        edges = []
        if 0 in candidates: edges.append(0)
        if w - 1 in candidates: edges.append(w - 1)
        rest = [c for c in candidates if c not in edges]
        rng.shuffle(rest)
        return (edges + rest)[:nz]
    if layout == "regular_spaced":
        step = max(1, len(candidates) // nz)
        return [candidates[i * step] for i in range(nz) if i * step < len(candidates)]
    rng.shuffle(candidates)
    return sorted(candidates[:nz])


def _draw_from_degenerate(name, w, rng):
    g = full_grid(1, w, 0)
    fg = rng.choice([1, 2, 3, 4, 5, 6, 7, 8, 9])
    if name == "all_zero":
        # nz=0 → output dim is 0×0 — invalid. Add 1 cell.
        g[0][0] = fg
        return g
    if name == "all_filled":
        # nz = w
        for c in range(w):
            g[0][c] = fg
        return g
    if name == "single_nz":
        g[0][rng.randint(0, w - 1)] = fg
        return g
    return g
