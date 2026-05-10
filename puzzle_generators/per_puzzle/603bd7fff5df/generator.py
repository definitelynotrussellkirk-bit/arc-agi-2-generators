"""Generator for puzzle 3f7978a0.

Rule: find bbox of gray(5) cells, extract subgrid spanning that bbox
plus 1 row above and 1 row below.

Combinatorial axes (8):
  * grid_h / grid_w        — outer canvas size
  * box_h / box_w          — gray bbox dims (≥ 3 each)
  * gray_perimeter_kind    — corners_only / corners+edges / full_outline /
                             scattered (controls which cells inside the
                             bbox are gray)
  * content_palette_size   — distinct content colors (1..4)
  * content_density        — fraction of bbox interior with content
  * content_pattern        — random / cluster / line / blob / cross
  * outside_decoy_density  — non-gray cells outside the bbox (rule ignores)
  * caller-opt-in degenerates: single_gray (rule has 1×1 bbox + halo),
                              gray_at_border (rule's ±1 row goes OOB),
                              empty_inside (no content).
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "603bd7fff5df"
VERSION = "1.1.0"
TASK_ID = "603bd7fff5df"
SUMMARY = "Gray(5) cells define a bbox; rule extracts bbox + 1 row above and below."

INVARIANTS = [
    "background is 0",
    "≥2 gray(5) cells forming a bbox of ≥ 3 × 3",
    "gray bbox has ≥1 row of bg margin above AND below within the grid",
    "inside bbox: some non-bg, non-gray content cells",
]

GRAY_PERIMETERS = ("corners_only", "corners_plus_edges", "full_outline", "scattered")
CONTENT_PATTERNS = ("random", "cluster", "line", "blob", "cross", "diagonal")
DEGENERATE_TEXTURES = ("single_gray", "gray_at_border", "empty_inside")
HELPFUL_TEXTURES = GRAY_PERIMETERS

AXES = {
    "grid_h":              {"type": "int", "default": "rng 10..18", "valid": "8..22"},
    "grid_w":              {"type": "int", "default": "rng 10..18", "valid": "8..22"},
    "box_h":               {"type": "int", "default": "rng 4..7", "valid": "3..12"},
    "box_w":               {"type": "int", "default": "rng 4..7", "valid": "3..12"},
    "gray_perimeter_kind": {"type": "str", "default": "rng helpful",
                            "valid": "|".join(GRAY_PERIMETERS)},
    "content_palette_size": {"type": "int", "default": "rng 1..4", "valid": "1..6"},
    "content_density":     {"type": "float", "default": "rng 0.2..0.5", "valid": "0..1"},
    "content_pattern":     {"type": "str", "default": "rng helpful",
                            "valid": "|".join(CONTENT_PATTERNS)},
    "outside_decoy_density": {"type": "float", "default": "rng 0..0.05", "valid": "0..0.2"},
    "texture":             {"type": "str", "default": "alias for gray_perimeter_kind",
                            "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if difficulty == "easy":
        h_lo, h_hi, b_lo, b_hi = 10, 12, 3, 5
    elif difficulty == "hard":
        h_lo, h_hi, b_lo, b_hi = 15, 18, 6, 7
    else:
        h_lo, h_hi, b_lo, b_hi = 10, 18, 4, 7
    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", h_lo, h_hi)
    rng = ctx.draw_rng("placement")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], h, w, rng)
    bh = ctx.draw_int("box_h", b_lo, min(b_hi, h - 4))
    bw = ctx.draw_int("box_w", b_lo, min(b_hi, w - 4))
    perim = (overrides.get("texture") or overrides.get("gray_perimeter_kind")
             or ctx.draw_choice("gray_perimeter_kind", list(GRAY_PERIMETERS)))
    n_palette = int(overrides.get("content_palette_size",
                                  ctx.draw_int("content_palette_size", 1, 4)))
    palette = list(ctx.draw_distinct_colors("content_palette",
                                            n=max(1, n_palette), exclude={0, 5}))
    pattern = overrides.get("content_pattern",
                            ctx.draw_choice("content_pattern", list(CONTENT_PATTERNS)))
    density = float(overrides.get("content_density",
                                  ctx.draw_rng("content_density").uniform(0.2, 0.5)))
    decoy_d = float(overrides.get("outside_decoy_density",
                                  ctx.draw_rng("outside_decoy_density").uniform(0.0, 0.05)))

    rr = rng.randint(2, h - bh - 2)
    rc = rng.randint(1, w - bw - 1)
    g = full_grid(h, w, 0)
    _draw_perimeter(g, perim, rr, rc, bh, bw, rng)
    _fill_interior(g, rr, rc, bh, bw, pattern, density, palette, rng)
    if decoy_d > 0:
        for r in range(h):
            for c in range(w):
                if g[r][c] == 0 and rng.random() < decoy_d \
                        and not (rr <= r <= rr + bh - 1 and rc <= c <= rc + bw - 1):
                    g[r][c] = rng.choice(palette) if palette else 0
    return g


def _draw_perimeter(g, kind, rr, rc, bh, bw, rng):
    g[rr][rc] = 5
    g[rr][rc + bw - 1] = 5
    g[rr + bh - 1][rc] = 5
    g[rr + bh - 1][rc + bw - 1] = 5
    if kind == "corners_plus_edges":
        for _ in range(2):
            if rng.random() < 0.5:
                g[rr][rc + rng.randint(1, bw - 2)] = 5
            else:
                g[rr + rng.randint(1, bh - 2)][rc] = 5
    elif kind == "full_outline":
        for c in range(rc, rc + bw):
            g[rr][c] = 5
            g[rr + bh - 1][c] = 5
        for r in range(rr, rr + bh):
            g[r][rc] = 5
            g[r][rc + bw - 1] = 5
    elif kind == "scattered":
        for _ in range(rng.randint(1, 3)):
            er = rng.randint(rr, rr + bh - 1)
            ec = rng.randint(rc, rc + bw - 1)
            g[er][ec] = 5


def _fill_interior(g, rr, rc, bh, bw, pattern, density, palette, rng):
    if not palette:
        palette = [3]
    if bh < 3 or bw < 3:
        return
    if pattern == "random":
        for r in range(rr + 1, rr + bh - 1):
            for c in range(rc + 1, rc + bw - 1):
                if g[r][c] == 0 and rng.random() < density:
                    g[r][c] = rng.choice(palette)
    elif pattern == "cluster":
        cr = rng.randint(rr + 1, rr + bh - 2)
        cc = rng.randint(rc + 1, rc + bw - 2)
        for r in range(rr + 1, rr + bh - 1):
            for c in range(rc + 1, rc + bw - 1):
                if g[r][c] == 0 and abs(r - cr) + abs(c - cc) <= 2 \
                        and rng.random() < density:
                    g[r][c] = rng.choice(palette)
    elif pattern == "line":
        r = rng.randint(rr + 1, rr + bh - 2)
        for c in range(rc + 1, rc + bw - 1):
            if g[r][c] == 0:
                g[r][c] = palette[0]
    elif pattern == "blob":
        n = max(2, int((bh - 2) * (bw - 2) * density))
        for _ in range(n):
            r = rng.randint(rr + 1, rr + bh - 2)
            c = rng.randint(rc + 1, rc + bw - 2)
            if g[r][c] == 0:
                g[r][c] = rng.choice(palette)
    elif pattern == "cross":
        mr = (rr + rr + bh - 1) // 2
        mc = (rc + rc + bw - 1) // 2
        for c in range(rc + 1, rc + bw - 1):
            if g[mr][c] == 0:
                g[mr][c] = palette[0]
        for r in range(rr + 1, rr + bh - 1):
            if g[r][mc] == 0:
                g[r][mc] = palette[0]
    elif pattern == "diagonal":
        for k in range(min(bh - 2, bw - 2)):
            if g[rr + 1 + k][rc + 1 + k] == 0:
                g[rr + 1 + k][rc + 1 + k] = palette[k % len(palette)]
    # Force ≥1 content cell.
    if not any(g[r][c] not in {0, 5}
               for r in range(rr + 1, rr + bh - 1)
               for c in range(rc + 1, rc + bw - 1)):
        g[rr + 1][rc + 1] = palette[0]


def _draw_from_degenerate(name, h, w, rng):
    g = full_grid(h, w, 0)
    palette = list(range(1, 10))
    rng.shuffle(palette)
    palette = [c for c in palette if c != 5][:3]
    if name == "single_gray":
        g[h // 2][w // 2] = 5
        return g
    if name == "gray_at_border":
        bh = 4; bw = 4
        g[0][1] = 5; g[0][1 + bw - 1] = 5
        g[bh - 1][1] = 5; g[bh - 1][1 + bw - 1] = 5
        g[1][2] = palette[0]
        return g
    if name == "empty_inside":
        bh = 5; bw = 5
        rr = 2; rc = 2
        for c in range(rc, rc + bw):
            g[rr][c] = 5
            g[rr + bh - 1][c] = 5
        for r in range(rr, rr + bh):
            g[r][rc] = 5
            g[r][rc + bw - 1] = 5
        return g
    return g
