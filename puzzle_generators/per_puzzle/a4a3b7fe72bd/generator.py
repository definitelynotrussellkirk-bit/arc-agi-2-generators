"""Generator for puzzle 3ee1011a.

Rule: each non-bg color forms a line segment; rule sorts by length desc
and outputs N×N concentric rings (N = max length).

Combinatorial axes (8): grid_h/w, n_colors, length_distribution,
palette_kind, line_orientation, position_bias, inter_line_margin,
asymmetry_force.
Degenerates: same_lengths, no_lines, all_one_line.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "a4a3b7fe72bd"
VERSION = "1.1.0"
TASK_ID = "a4a3b7fe72bd"
SUMMARY = "Line segments of varying lengths; rule outputs concentric rings by length."

INVARIANTS = [
    "background is 0",
    "2-4 distinct non-bg colors",
    "each color's cells form a horizontal or vertical line segment",
    "line lengths are pairwise distinct",
    "max line length <= 8",
]

LENGTH_DISTRIBUTIONS = ("ascending", "wide_spread", "tight_spread", "shuffled")
LINE_ORIENTATIONS = ("mixed", "horizontal_only", "vertical_only")
PALETTE_KINDS = ("warm", "cool", "broad", "small")
DEGENERATE_TEXTURES = ("same_lengths", "no_lines", "all_one_line")
HELPFUL_TEXTURES = LENGTH_DISTRIBUTIONS

AXES = {
    "grid_h":             {"type": "int", "default": "rng 10..16", "valid": "8..20"},
    "grid_w":             {"type": "int", "default": "rng 10..16", "valid": "8..20"},
    "n_colors":           {"type": "int", "default": "rng 2..4", "valid": "2..5"},
    "length_distribution": {"type": "str", "default": "rng helpful",
                            "valid": "|".join(LENGTH_DISTRIBUTIONS)},
    "line_orientation":   {"type": "str", "default": "rng helpful",
                           "valid": "|".join(LINE_ORIENTATIONS)},
    "palette_kind":       {"type": "str", "default": "rng helpful",
                           "valid": "|".join(PALETTE_KINDS)},
    "position_bias":      {"type": "str", "default": "rng spread|center",
                           "valid": "spread|center"},
    "inter_line_margin":  {"type": "int", "default": "1", "valid": "0..3"},
    "texture":            {"type": "str", "default": "alias for length_distribution",
                           "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if difficulty == "easy":
        h_lo, h_hi, n_lo, n_hi = 8, 11, 2, 2
    elif difficulty == "hard":
        h_lo, h_hi, n_lo, n_hi = 14, 20, 3, 4
    else:
        h_lo, h_hi, n_lo, n_hi = 10, 16, 2, 4
    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", h_lo, h_hi)
    rng = ctx.draw_rng("placement")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], h, w, rng)
    n_colors = int(overrides.get("n_colors",
                                 ctx.draw_int("n_colors", n_lo, n_hi)))
    n_colors = max(2, min(4, n_colors))
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
    palette = pool[:n_colors]
    if len(palette) < n_colors:
        extras = [c for c in range(1, 10) if c not in palette]
        rng.shuffle(extras)
        palette += extras[:n_colors - len(palette)]
    palette = palette[:n_colors]
    dist = (overrides.get("texture") or
            overrides.get("length_distribution")
            or ctx.draw_choice("length_distribution",
                               list(LENGTH_DISTRIBUTIONS)))
    orient_kind = overrides.get("line_orientation",
                                ctx.draw_choice("line_orientation",
                                                list(LINE_ORIENTATIONS)))
    lengths = _draw_lengths(dist, n_colors, rng)
    g = full_grid(h, w, 0)
    placed = 0
    for color, length in zip(palette, lengths):
        for _ in range(40):
            orient = _pick_orient(orient_kind, rng)
            if orient == "h":
                r = rng.randint(0, h - 1)
                c = rng.randint(0, w - length)
                if any(g[r][c + dc] != 0 for dc in range(length)):
                    continue
                ok = True
                for dc in range(length):
                    for dr in (-1, 1):
                        nr = r + dr
                        if 0 <= nr < h and g[nr][c + dc] != 0:
                            ok = False; break
                    if not ok: break
                if not ok:
                    continue
                for dc in range(length):
                    g[r][c + dc] = color
            else:
                c = rng.randint(0, w - 1)
                r = rng.randint(0, h - length)
                if any(g[r + dr][c] != 0 for dr in range(length)):
                    continue
                ok = True
                for dr in range(length):
                    for dc in (-1, 1):
                        nc = c + dc
                        if 0 <= nc < w and g[r + dr][nc] != 0:
                            ok = False; break
                    if not ok: break
                if not ok:
                    continue
                for dr in range(length):
                    g[r + dr][c] = color
            placed += 1
            break
    if placed < n_colors:
        # fallback: stack horizontally
        g = full_grid(h, w, 0)
        for i, (color, length) in enumerate(zip(palette, lengths)):
            r = i * 2
            if r >= h: break
            for c in range(min(length, w)):
                g[r][c] = color
    return g


def _pick_orient(kind, rng):
    if kind == "horizontal_only":
        return "h"
    if kind == "vertical_only":
        return "v"
    return rng.choice(["h", "v"])


def _draw_lengths(dist, n_colors, rng):
    if dist == "ascending":
        start = rng.randint(2, max(2, 8 - n_colors))
        return [start + i for i in range(n_colors)]
    if dist == "tight_spread":
        base = rng.randint(2, max(2, 5))
        return [base + i for i in range(n_colors)]
    if dist == "wide_spread":
        return rng.sample(range(2, 8), n_colors)
    return rng.sample(range(2, 8), n_colors)


def _draw_from_degenerate(name, h, w, rng):
    g = full_grid(h, w, 0)
    palette = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    rng.shuffle(palette)
    if name == "same_lengths":
        for i, color in enumerate(palette[:3]):
            r = i * 2
            for c in range(3):
                if r < h and c < w:
                    g[r][c] = color
        return g
    if name == "no_lines":
        return g
    if name == "all_one_line":
        for c in range(min(5, w)):
            g[0][c] = palette[0]
        return g
    return g
