"""Generator for puzzle 91714a58.

Rule: keep largest solid rectangle, clear everything else.

Combinatorial axes (8): grid_h/w, rect_h, rect_w, palette_kind,
noise_density, position_bias, anchor_corner, asymmetry_force.
Degenerates: tied_rects, no_rect, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, draw_rect

GENERATOR_ID = "061566027b67"
VERSION = "1.1.0"
TASK_ID = "061566027b67"
SUMMARY = "Largest rect + scattered noise; rule keeps only the rect."

INVARIANTS = [
    "background is 0",
    "1 strictly-largest solid rectangle of any non-bg color",
    "noise cells don't form rects >= winner's area",
]

POSITION_BIASES = ("scattered", "centered", "corner", "spread")
PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("tied_rects", "no_rect", "full_grid")
HELPFUL_TEXTURES = POSITION_BIASES

AXES = {
    "grid_h":         {"type": "int", "default": "rng 14..20", "valid": "12..24"},
    "grid_w":         {"type": "int", "default": "rng 14..20", "valid": "12..24"},
    "rect_h":         {"type": "int", "default": "rng 4..6", "valid": "3..8"},
    "rect_w":         {"type": "int", "default": "rng 4..6", "valid": "3..8"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "noise_density":  {"type": "float", "default": "rng 0.06..0.12",
                       "valid": "0.02..0.2"},
    "position_bias":  {"type": "str", "default": "rng helpful",
                       "valid": "|".join(POSITION_BIASES)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "texture":        {"type": "str", "default": "alias for position_bias",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if difficulty == "easy":
        h_lo, h_hi = 12, 14
    elif difficulty == "hard":
        h_lo, h_hi = 18, 24
    else:
        h_lo, h_hi = 14, 20
    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", h_lo, h_hi)
    rng = ctx.draw_rng("placement")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], h, w, rng)
    rh = int(overrides.get("rect_h",
                           ctx.draw_int("rect_h", 4, 6)))
    rw = int(overrides.get("rect_w",
                           ctx.draw_int("rect_w", 4, 6)))
    rh = max(3, min(8, rh))
    rw = max(3, min(8, rw))
    palette_kind = overrides.get("palette_kind",
                                 ctx.draw_choice("palette_kind",
                                                 list(PALETTE_KINDS)))
    palette = _build_palette(palette_kind, 4, rng)
    winner_color = palette[0]
    noise_palette = palette[1:]
    noise_d = float(overrides.get("noise_density",
                                  ctx.draw_rng("noise_density")
                                  .uniform(0.06, 0.12)))
    bias = (overrides.get("texture") or
            overrides.get("position_bias")
            or ctx.draw_choice("position_bias",
                               list(POSITION_BIASES)))
    g = full_grid(h, w, 0)
    rr, rc = _pick_position(bias, h, w, rh, rw, rng)
    draw_rect(g, rr, rc, rh, rw, winner_color)
    n_noise = int(h * w * noise_d)
    for _ in range(n_noise):
        r = rng.randint(0, h - 1); c = rng.randint(0, w - 1)
        if rr <= r < rr + rh and rc <= c < rc + rw:
            continue
        nc = rng.choice(noise_palette)
        ok = True
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr, ncol = r + dr, c + dc
            if 0 <= nr < h and 0 <= ncol < w and g[nr][ncol] == nc:
                ok = False; break
        if ok:
            g[r][c] = nc
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


def _pick_position(bias, h, w, rh, rw, rng):
    if bias == "centered":
        return max(0, (h - rh) // 2), max(0, (w - rw) // 2)
    if bias == "corner":
        return rng.choice([(0, 0), (0, w - rw), (h - rh, 0),
                           (h - rh, w - rw)])
    return rng.randint(0, h - rh), rng.randint(0, w - rw)


def _draw_from_degenerate(name, h, w, rng):
    g = full_grid(h, w, 0)
    if name == "tied_rects":
        # 2 rects same size → ambiguous winner
        draw_rect(g, 2, 2, 4, 4, 3)
        draw_rect(g, h - 6, w - 6, 4, 4, 4)
        return g
    if name == "no_rect":
        for _ in range(20):
            r = rng.randint(0, h - 1); c = rng.randint(0, w - 1)
            if g[r][c] == 0:
                g[r][c] = rng.choice([1, 2, 3, 4])
        return g
    if name == "full_grid":
        for r in range(h):
            for c in range(w):
                g[r][c] = 3
        return g
    return g
