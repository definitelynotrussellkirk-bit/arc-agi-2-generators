"""Generator for puzzle f0df5ff0.

Rule: for each 1-cell, draw 3×3 block of 1s around it; non-bg cells
keep their value (rule only overwrites bg).

Combinatorial axes (8): grid_h/w, n_blues, blue_layout, position_bias,
n_decoys, decoy_palette_size, blue_separation, palette_kind.
Degenerates: no_blues, single_blue, all_blues.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "724d5770b986"
VERSION = "1.1.0"
TASK_ID = "724d5770b986"
SUMMARY = "Sparse blue cells + decoys; rule expands each blue to 3×3 block of 1s."

INVARIANTS = [
    "background is 0",
    ">=2 blue(1) cells with margin >=1 from grid edges",
    "blues separated by >=4 cells (so 3×3 expansions don't collide)",
    ">=1 non-blue non-bg cell adjacent to a blue",
]

BLUE_LAYOUTS = ("scattered", "diag", "row", "col", "corners", "spread")
PALETTE_KINDS = ("warm", "cool", "broad", "small")
DEGENERATE_TEXTURES = ("no_blues", "single_blue", "all_blues")
HELPFUL_TEXTURES = BLUE_LAYOUTS

AXES = {
    "grid_h":          {"type": "int", "default": "rng 8..14", "valid": "5..18"},
    "grid_w":          {"type": "int", "default": "rng 8..14", "valid": "5..18"},
    "n_blues":         {"type": "int", "default": "rng 2..4", "valid": "1..6"},
    "blue_layout":     {"type": "str", "default": "rng helpful",
                        "valid": "|".join(BLUE_LAYOUTS)},
    "position_bias":   {"type": "str", "default": "rng spread|center|edge",
                        "valid": "spread|center|edge"},
    "n_decoys":        {"type": "int", "default": "rng 1..4", "valid": "0..8"},
    "decoy_palette_size": {"type": "int", "default": "rng 2..4",
                           "valid": "1..7"},
    "palette_kind":    {"type": "str", "default": "rng helpful",
                        "valid": "|".join(PALETTE_KINDS)},
    "blue_separation": {"type": "int", "default": "4", "valid": "3..6"},
    "texture":         {"type": "str", "default": "alias for blue_layout",
                        "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if difficulty == "easy":
        h_lo, h_hi = 5, 8
    elif difficulty == "hard":
        h_lo, h_hi = 13, 18
    else:
        h_lo, h_hi = 8, 14
    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", h_lo, h_hi)
    rng = ctx.draw_rng("placement")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], h, w, rng)
    n_blues = int(overrides.get("n_blues",
                                ctx.draw_int("n_blues", 2, 4)))
    n_blues = max(1, min(6, n_blues))
    layout = (overrides.get("texture") or
              overrides.get("blue_layout")
              or ctx.draw_choice("blue_layout", list(BLUE_LAYOUTS)))
    bias = overrides.get("position_bias",
                         ctx.draw_choice("position_bias",
                                         ["spread", "center", "edge"]))
    sep = int(overrides.get("blue_separation", 4))
    g = full_grid(h, w, 0)
    blue_pos = _layout_blues(layout, h, w, n_blues, sep, bias, rng)
    for r, c in blue_pos:
        g[r][c] = 1
    palette_kind = overrides.get("palette_kind",
                                 ctx.draw_choice("palette_kind",
                                                 list(PALETTE_KINDS)))
    if palette_kind == "warm":
        decoy_pool = [3, 4, 6, 9]
    elif palette_kind == "cool":
        decoy_pool = [5, 7, 8]
    elif palette_kind == "small":
        decoy_pool = [2, 3]
    else:
        decoy_pool = [2, 3, 4, 5, 6, 7, 8, 9]
    rng.shuffle(decoy_pool)
    n_decoy_pal = int(overrides.get("decoy_palette_size",
                                    ctx.draw_int("decoy_palette_size", 2, 4)))
    decoy_palette = decoy_pool[:max(1, n_decoy_pal)]
    n_decoys = int(overrides.get("n_decoys",
                                 ctx.draw_int("n_decoys", 1, 4)))
    if not blue_pos:
        return _draw_from_degenerate("no_blues", h, w, rng)
    placed_decoys = 0
    for _ in range(n_decoys * 5):
        if placed_decoys >= n_decoys:
            break
        pr, pc = rng.choice(blue_pos)
        for _try in range(8):
            dr = rng.randint(-2, 2); dc = rng.randint(-2, 2)
            r, c = pr + dr, pc + dc
            if 0 <= r < h and 0 <= c < w and g[r][c] == 0:
                g[r][c] = rng.choice(decoy_palette)
                placed_decoys += 1
                break
    return g


def _layout_blues(layout, h, w, n, sep, bias, rng):
    candidates = [(r, c) for r in range(1, h - 1)
                  for c in range(1, w - 1)]
    if layout == "diag":
        candidates = [(k, k) for k in range(1, min(h, w) - 1)]
    elif layout == "row":
        r = h // 2
        candidates = [(r, c) for c in range(1, w - 1)]
    elif layout == "col":
        c = w // 2
        candidates = [(r, c) for r in range(1, h - 1)]
    elif layout == "corners":
        candidates = [(1, 1), (1, w - 2), (h - 2, 1), (h - 2, w - 2)]
    elif layout == "spread":
        step_r = max(sep, (h - 2) // (n + 1))
        step_c = max(sep, (w - 2) // (n + 1))
        candidates = [(1 + step_r * i, 1 + step_c * i) for i in range(n)
                      if 1 + step_r * i < h - 1
                      and 1 + step_c * i < w - 1]
    if bias == "center":
        cr, cc = h // 2, w // 2
        candidates = sorted(candidates,
                            key=lambda rc: abs(rc[0] - cr) + abs(rc[1] - cc))
    elif bias == "edge":
        candidates = sorted(candidates,
                            key=lambda rc: -min(rc[0], h - 1 - rc[0],
                                                rc[1], w - 1 - rc[1]))
    else:
        rng.shuffle(candidates)
    placed = []
    for r, c in candidates:
        if all(abs(r - pr) >= sep or abs(c - pc) >= sep for pr, pc in placed):
            placed.append((r, c))
        if len(placed) >= n:
            break
    return placed


def _draw_from_degenerate(name, h, w, rng):
    g = full_grid(h, w, 0)
    if name == "no_blues":
        for _ in range(3):
            r = rng.randint(1, h - 2); c = rng.randint(1, w - 2)
            g[r][c] = rng.choice([2, 3, 4, 5, 6, 7, 8, 9])
        return g
    if name == "single_blue":
        g[h // 2][w // 2] = 1
        return g
    if name == "all_blues":
        for r in range(1, h - 1):
            for c in range(1, w - 1):
                g[r][c] = 1
        return g
    return g
