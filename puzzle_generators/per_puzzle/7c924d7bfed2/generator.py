"""Generator for d749d46f.

Rule: K solid colored rectangles on a uniform bg; output is two
stacks (thin/long top, long/thin bottom).

Combinatorial axes (8): grid_h/w, palette_kind, anchor_corner,
asymmetry_force, palette_size, position_bias, n_rects, bg_kind.
Degenerates: no_rects, single_rect, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, draw_rect

GENERATOR_ID = "7c924d7bfed2"
VERSION = "1.1.0"
TASK_ID = "7c924d7bfed2"
SUMMARY = "Rectangles assembled into thin/long top and long/thin bottom stacks."

INVARIANTS = [
    "bg is the most common color and uniform outside rectangles",
    "two or three solid colored rectangles each in a distinct color",
    "long dimension is at most 9",
    "rectangles separated by bg margin of at least one cell",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary")
BG_KINDS = ("black", "cyan", "gray")
DEGENERATE_TEXTURES = ("no_rects", "single_rect", "full_grid")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 14..18", "valid": "12..22"},
    "grid_w":         {"type": "int", "default": "rng 14..18", "valid": "12..22"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "3", "valid": "3"},
    "position_bias":  {"type": "str", "default": "rng", "valid": "rng"},
    "n_rects":        {"type": "int", "default": "3", "valid": "2..3"},
    "bg_kind":        {"type": "str", "default": "rng",
                       "valid": "|".join(BG_KINDS)},
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
        h_lo, h_hi = 14, 14
    elif difficulty == "hard":
        h_lo, h_hi = 18, 22
    else:
        h_lo, h_hi = 14, 18
    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", h_lo, h_hi)
    bg = rng.choice([0, 8, 5])
    palette_kind = (overrides.get("texture") or
                    overrides.get("palette_kind") or
                    ctx.draw_choice("palette_kind", list(PALETTE_KINDS)))
    pool = _build_palette(palette_kind, bg, rng)
    if len(pool) < 3:
        pool = pool + [c for c in [1, 2, 3, 4, 5, 6, 7, 8, 9] if c not in pool and c != bg]
    palette = pool[:3]
    g = full_grid(h, w, bg)
    placed = []
    for color in palette:
        for _try in range(20):
            rh = rng.randint(2, 4)
            rw = rng.randint(2, 4)
            if rh == rw:
                rw += 1
            rr = rng.randint(0, h - rh)
            rc = rng.randint(0, w - rw)
            ok = True
            for r in range(max(0, rr - 1), min(h, rr + rh + 1)):
                for c in range(max(0, rc - 1), min(w, rc + rw + 1)):
                    if g[r][c] != bg:
                        ok = False; break
                if not ok: break
            if not ok:
                continue
            draw_rect(g, rr, rc, rh, rw, color)
            placed.append((rr, rc, rh, rw, color))
            break
    if len(placed) < 2:
        return [[bg]]
    return g


def _build_palette(kind, bg, rng):
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
    return pool


def _draw_from_degenerate(name, rng):
    h, w = 14, 14
    g = full_grid(h, w, 0)
    if name == "no_rects":
        return g
    if name == "single_rect":
        draw_rect(g, 4, 4, 3, 4, 2)
        return g
    if name == "full_grid":
        for r in range(h):
            for c in range(w):
                g[r][c] = 2
        return g
    return g
