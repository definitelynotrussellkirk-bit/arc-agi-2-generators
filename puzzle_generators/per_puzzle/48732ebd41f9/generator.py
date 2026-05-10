"""Generator for puzzle 3eda0437.

Rule: find the tallest rectangle of 0-cells (min height ≥ 2); fill
its 0-cells with color 6.

Combinatorial axes (8):
  * grid_h / grid_w        — outer canvas size
  * fg_color               — non-bg color (canonical: 1)
  * fg_density             — fraction of fg cells
  * empty_block_h / empty_block_w — dims of the carved 0-rect
  * fg_layout              — random / scattered / clusters / stripes /
                             borders
  * empty_block_position   — center / left / right / top / random
  * other_blocks_density   — extra small 0-blocks (rule still picks tallest)
  * caller-opt-in degenerates: no_empty_block (rule fails),
                              two_equal_blocks (tie-break),
                              full_empty (whole grid is 0).
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "48732ebd41f9"
VERSION = "1.1.0"
TASK_ID = "48732ebd41f9"
SUMMARY = "Scattered fg cells with a clear tall 0-rectangle; rule fills the tallest 0-rect with 6."

INVARIANTS = [
    "≥1 0-rectangle of height ≥ 2 exists",
    "fg color ≠ 6 (output marker)",
    "the tallest 0-rect is unambiguously larger than alternatives",
]

FG_LAYOUTS = ("random", "scattered", "clusters", "stripes", "borders")
BLOCK_POSITIONS = ("center", "left", "right", "top", "bottom", "random")
DEGENERATE_TEXTURES = ("no_empty_block", "two_equal_blocks", "full_empty")
HELPFUL_TEXTURES = FG_LAYOUTS

AXES = {
    "grid_h":               {"type": "int", "default": "rng 2..10", "valid": "2..15"},
    "grid_w":               {"type": "int", "default": "rng 14..28", "valid": "12..30"},
    "fg_color":             {"type": "color", "default": "rng (≠0,6)", "valid": "1..9 (≠6)"},
    "fg_density":            {"type": "float", "default": "rng 0.3..0.6", "valid": "0..0.9"},
    "empty_block_w":        {"type": "int", "default": "rng 4..7", "valid": "2..15"},
    "fg_layout":            {"type": "str", "default": "rng helpful",
                             "valid": "|".join(FG_LAYOUTS)},
    "empty_block_position": {"type": "str", "default": "rng helpful",
                             "valid": "|".join(BLOCK_POSITIONS)},
    "other_blocks_density": {"type": "float", "default": "rng 0..0.1", "valid": "0..0.3"},
    "texture":              {"type": "str", "default": "alias for fg_layout",
                             "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if difficulty == "easy":
        h_lo, h_hi, w_lo, w_hi = 2, 3, 14, 18
    elif difficulty == "hard":
        h_lo, h_hi, w_lo, w_hi = 6, 10, 24, 28
    else:
        h_lo, h_hi, w_lo, w_hi = 2, 10, 14, 28
    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", w_lo, w_hi)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], h, w, rng)
    fg = int(overrides.get("fg_color", ctx.draw_color("fg_color", exclude={0, 6})))
    density = float(overrides.get("fg_density",
                                  ctx.draw_rng("fg_density").uniform(0.3, 0.6)))
    block_w = int(overrides.get("empty_block_w",
                                ctx.draw_int("empty_block_w", 4, max(4, w // 4))))
    block_w = min(block_w, w - 4)
    layout = (overrides.get("texture") or overrides.get("fg_layout")
              or ctx.draw_choice("fg_layout", list(FG_LAYOUTS)))
    position = overrides.get("empty_block_position",
                             ctx.draw_choice("empty_block_position",
                                             list(BLOCK_POSITIONS)))
    other_d = float(overrides.get("other_blocks_density",
                                  ctx.draw_rng("other_blocks_density").uniform(0.0, 0.1)))
    g = full_grid(h, w, 0)
    _fill_fg(g, layout, density, fg, rng)
    # Carve the empty block (full-height, block_w wide)
    block_c = _block_position(position, block_w, w, rng)
    for r in range(h):
        for c in range(block_c, block_c + block_w):
            g[r][c] = 0
    # Maybe carve smaller competing blocks (still smaller than the main one)
    if other_d > 0:
        for _ in range(max(1, int(w * other_d))):
            sw = max(2, block_w - 2)
            sc = rng.randint(0, w - sw)
            sr_start = rng.randint(0, max(0, h - 1))
            sr_end = sr_start + 1  # height < h
            for r in range(sr_start, sr_end + 1):
                for c in range(sc, sc + sw):
                    if 0 <= r < h:
                        g[r][c] = 0
    return g


def _fill_fg(g, layout, density, fg, rng):
    h = len(g); w = len(g[0])
    if layout == "random":
        for r in range(h):
            for c in range(w):
                if rng.random() < density:
                    g[r][c] = fg
    elif layout == "scattered":
        for r in range(0, h, 2):
            for c in range(w):
                if rng.random() < density:
                    g[r][c] = fg
    elif layout == "clusters":
        n_clusters = max(1, int(w * density / 3))
        for _ in range(n_clusters):
            cr = rng.randint(0, h - 1); cc = rng.randint(0, w - 1)
            for dr in (-1, 0, 1):
                for dc in (-1, 0, 1):
                    if 0 <= cr + dr < h and 0 <= cc + dc < w \
                            and rng.random() < 0.7:
                        g[cr + dr][cc + dc] = fg
    elif layout == "stripes":
        for r in range(h):
            if r % 2 == 0:
                for c in range(w):
                    if rng.random() < density:
                        g[r][c] = fg
    elif layout == "borders":
        for c in range(w):
            g[0][c] = fg
            g[h - 1][c] = fg


def _block_position(position, block_w, w, rng):
    if position == "center":
        return (w - block_w) // 2
    if position == "left":
        return 1
    if position == "right":
        return w - block_w - 1
    if position == "top":
        return rng.randint(0, max(0, w // 2 - block_w))
    if position == "bottom":
        return rng.randint(max(0, w // 2), w - block_w)
    return rng.randint(2, max(2, w - block_w - 2))


def _draw_from_degenerate(name, h, w, rng):
    g = full_grid(h, w, 0)
    fg = rng.choice([1, 2, 3, 4, 5, 7, 8, 9])
    if name == "no_empty_block":
        for r in range(h):
            for c in range(w):
                if rng.random() < 0.7:
                    g[r][c] = fg
        return g
    if name == "two_equal_blocks":
        # Two equal-tall 0-rects — tie.
        for r in range(h):
            for c in range(w):
                if rng.random() < 0.4:
                    g[r][c] = fg
        bw = 4
        for c in range(2, 2 + bw):
            for r in range(h):
                g[r][c] = 0
        for c in range(w - 2 - bw, w - 2):
            for r in range(h):
                g[r][c] = 0
        return g
    if name == "full_empty":
        return g
    return g
