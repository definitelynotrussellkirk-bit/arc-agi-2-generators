"""Generator for puzzle 981add89.

Rule: top row has markers (non-bg, non-equal to row 1 in that col).
For each marker column, sweeps down: cells equal to marker → bg,
other body cells → marker (XOR-like).

Combinatorial axes (8): grid_h/w, bg_color, n_markers, palette_kind,
body_density, marker_distribution, anchor_corner, asymmetry_force.
Degenerates: no_markers, all_markers, body_empty.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "b38782448e7b"
VERSION = "1.1.0"
TASK_ID = "b38782448e7b"
SUMMARY = "Top markers + body; rule XOR-sweeps each marker column."

INVARIANTS = [
    "mode color is bg",
    ">=2 columns have a row-0 marker that differs from row-1 in that column",
    "body has mix of bg + marker-color cells",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary")
MARKER_DISTRIBUTIONS = ("scattered", "left_heavy", "right_heavy",
                        "evenly_spaced", "clustered")
DEGENERATE_TEXTURES = ("no_markers", "all_markers", "body_empty")
HELPFUL_TEXTURES = MARKER_DISTRIBUTIONS

AXES = {
    "grid_h":             {"type": "int", "default": "rng 7..14", "valid": "5..18"},
    "grid_w":             {"type": "int", "default": "rng 6..12", "valid": "5..16"},
    "bg_color":           {"type": "color", "default": "rng", "valid": "0..9"},
    "n_markers":          {"type": "int", "default": "rng 2..4", "valid": "2..6"},
    "palette_kind":       {"type": "str", "default": "rng helpful",
                          "valid": "|".join(PALETTE_KINDS)},
    "body_density":       {"type": "float", "default": "rng 0.2..0.5",
                          "valid": "0.05..0.7"},
    "marker_distribution":{"type": "str", "default": "rng helpful",
                          "valid": "|".join(MARKER_DISTRIBUTIONS)},
    "anchor_corner":      {"type": "bool", "default": "false",
                          "valid": "true|false"},
    "texture":            {"type": "str", "default": "alias for marker_distribution",
                          "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if difficulty == "easy":
        h_lo, h_hi = 5, 8
    elif difficulty == "hard":
        h_lo, h_hi = 14, 18
    else:
        h_lo, h_hi = 7, 14
    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", h_lo - 1, h_hi - 2)
    rng = ctx.draw_rng("placement")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], h, w, rng)
    bg = int(overrides.get("bg_color", ctx.draw_color("bg_color")))
    palette_kind = overrides.get("palette_kind",
                                 ctx.draw_choice("palette_kind",
                                                 list(PALETTE_KINDS)))
    palette = _build_palette(palette_kind, bg, 3, rng)
    n_markers = int(overrides.get("n_markers",
                                  ctx.draw_int("n_markers", 2, 4)))
    n_markers = max(2, min(min(w, 6), n_markers))
    body_density = float(overrides.get("body_density",
                                       ctx.draw_rng("body_density")
                                       .uniform(0.2, 0.5)))
    distribution = (overrides.get("texture") or
                    overrides.get("marker_distribution")
                    or ctx.draw_choice("marker_distribution",
                                       list(MARKER_DISTRIBUTIONS)))
    g = full_grid(h, w, bg)
    marker_cols = _pick_marker_cols(distribution, w, n_markers, rng)
    for c in marker_cols:
        marker = rng.choice(palette)
        g[0][c] = marker
        for r in range(1, h):
            if rng.random() < body_density:
                g[r][c] = rng.choice(palette)
    return g


def _build_palette(kind, bg, n, rng):
    if kind == "warm":
        pool = [2, 3, 4, 6, 9]
    elif kind == "cool":
        pool = [1, 5, 7, 8]
    elif kind == "primary":
        pool = [1, 2, 3, 4]
    else:
        pool = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    pool = [c for c in pool if c != bg]
    rng.shuffle(pool)
    while len(pool) < n:
        for c in [1, 2, 3, 4, 5, 6, 7, 8, 9]:
            if c not in pool and c != bg:
                pool.append(c)
    return pool[:max(1, n)]


def _pick_marker_cols(distribution, w, n, rng):
    if distribution == "left_heavy":
        return list(range(min(n, w)))
    if distribution == "right_heavy":
        return list(range(max(0, w - n), w))
    if distribution == "evenly_spaced":
        step = max(1, w // (n + 1))
        return [step * (i + 1) for i in range(n) if step * (i + 1) < w][:n]
    if distribution == "clustered":
        start = rng.randint(0, max(0, w - n))
        return list(range(start, start + n))
    return rng.sample(range(w), n)


def _draw_from_degenerate(name, h, w, rng):
    bg = rng.choice([0, 1, 5, 8])
    g = full_grid(h, w, bg)
    if name == "no_markers":
        return g
    if name == "all_markers":
        marker = rng.choice([c for c in [2, 3, 4, 6, 7, 9] if c != bg])
        for c in range(w):
            g[0][c] = marker
        return g
    if name == "body_empty":
        # Top row has markers but body is all bg
        marker = rng.choice([c for c in [2, 3, 4, 6, 7, 9] if c != bg])
        for c in range(0, w, 2):
            g[0][c] = marker
        return g
    return g
