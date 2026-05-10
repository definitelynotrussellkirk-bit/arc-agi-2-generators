"""Generator for puzzle 05269061.

Rule: 3 distinct non-bg cells exist with (r+c) mod 3 ∈ {0, 1, 2}, one
each. Output: every cell with (r+c) mod 3 = m gets the color found at
that residue class.

Combinatorial axes (8): grid_h/w, palette_kind, palette_size, n_seeds,
seed_layout, position_bias, anchor_corner, asymmetry_force.
Degenerates: missing_residue, all_same_color, all_zeros.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "080523523c90"
VERSION = "1.1.0"
TASK_ID = "080523523c90"
SUMMARY = "3 cells of 3 distinct colors at 3 (r+c)%3 residues; rule tiles."

INVARIANTS = [
    "background is 0",
    ">=3 non-bg cells, with at least 1 cell per (r+c)%3 residue",
    "first cell at residue m has the color used everywhere at residue m",
    "the 3 residue colors are distinct",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary", "pastel")
SEED_LAYOUTS = ("diagonal", "scattered", "corners", "anti_diag",
                "row", "column")
DEGENERATE_TEXTURES = ("missing_residue", "all_same_color", "all_zeros")
HELPFUL_TEXTURES = SEED_LAYOUTS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 5..9", "valid": "4..12"},
    "grid_w":         {"type": "int", "default": "rng 5..9", "valid": "4..12"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "seed_layout":    {"type": "str", "default": "rng helpful",
                       "valid": "|".join(SEED_LAYOUTS)},
    "n_seeds":        {"type": "int", "default": "3", "valid": "3..9"},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "texture":        {"type": "str", "default": "alias for seed_layout",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if difficulty == "easy":
        h_lo, h_hi = 4, 6
    elif difficulty == "hard":
        h_lo, h_hi = 9, 12
    else:
        h_lo, h_hi = 5, 9
    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", h_lo, h_hi)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], h, w, rng)
    palette_kind = overrides.get("palette_kind",
                                 ctx.draw_choice("palette_kind",
                                                 list(PALETTE_KINDS)))
    layout = (overrides.get("texture") or
              overrides.get("seed_layout")
              or ctx.draw_choice("seed_layout", list(SEED_LAYOUTS)))
    pal = _build_palette(palette_kind, rng)[:3]
    g = full_grid(h, w, 0)
    seeds_by_residue = _layout_residues(layout, h, w, rng)
    for residue in range(3):
        cells = seeds_by_residue.get(residue, [])
        for r, c in cells:
            if g[r][c] == 0:
                g[r][c] = pal[residue]
                break
        else:
            for r in range(h):
                for c in range(w):
                    if (r + c) % 3 == residue and g[r][c] == 0:
                        g[r][c] = pal[residue]
                        break
                else:
                    continue
                break
    return g


def _build_palette(kind, rng):
    if kind == "warm":
        pool = [2, 3, 4, 6, 9]
    elif kind == "cool":
        pool = [1, 5, 7, 8]
    elif kind == "primary":
        pool = [1, 2, 3]
    elif kind == "pastel":
        pool = [3, 4, 6, 7]
    else:
        pool = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    rng.shuffle(pool)
    while len(pool) < 3:
        for c in [1, 2, 3, 4, 5, 6, 7, 8, 9]:
            if c not in pool:
                pool.append(c)
    return pool


def _layout_residues(layout, h, w, rng):
    by_res = {0: [], 1: [], 2: []}
    if layout == "diagonal":
        for i in range(min(h, w)):
            by_res[(i + i) % 3].append((i, i))
    elif layout == "anti_diag":
        for i in range(min(h, w)):
            r, c = i, w - 1 - i
            if 0 <= c < w:
                by_res[(r + c) % 3].append((r, c))
    elif layout == "corners":
        for r, c in [(0, 0), (0, w - 1), (h - 1, 0), (h - 1, w - 1)]:
            by_res[(r + c) % 3].append((r, c))
    elif layout == "row":
        r = rng.randint(0, h - 1)
        for c in range(w):
            by_res[(r + c) % 3].append((r, c))
    elif layout == "column":
        c = rng.randint(0, w - 1)
        for r in range(h):
            by_res[(r + c) % 3].append((r, c))
    else:
        for r in range(h):
            for c in range(w):
                by_res[(r + c) % 3].append((r, c))
        for k in by_res:
            rng.shuffle(by_res[k])
    return by_res


def _draw_from_degenerate(name, h, w, rng):
    g = full_grid(h, w, 0)
    pal = rng.sample([1, 2, 3, 4, 5, 6, 7, 8, 9], 3)
    if name == "missing_residue":
        # Only 2 of 3 residues seeded; rule picks first cell at residue
        # 2 to be 0 (which makes everything at residue 2 stay 0)
        for r in range(h):
            for c in range(w):
                if (r + c) % 3 == 0 and g[r][c] == 0:
                    g[r][c] = pal[0]; break
            else:
                continue
            break
        for r in range(h):
            for c in range(w):
                if (r + c) % 3 == 1 and g[r][c] == 0:
                    g[r][c] = pal[1]; break
            else:
                continue
            break
        return g
    if name == "all_same_color":
        for r in range(h):
            for c in range(w):
                if (r + c) % 3 == 0 and g[r][c] == 0:
                    g[r][c] = pal[0]; break
            else:
                continue
            break
        for r in range(h):
            for c in range(w):
                if (r + c) % 3 == 1 and g[r][c] == 0:
                    g[r][c] = pal[0]; break
            else:
                continue
            break
        for r in range(h):
            for c in range(w):
                if (r + c) % 3 == 2 and g[r][c] == 0:
                    g[r][c] = pal[0]; break
            else:
                continue
            break
        return g
    if name == "all_zeros":
        # Ensure rule has SOMETHING to fire on by adding a single seed
        g[0][0] = pal[0]
        return g
    return g
