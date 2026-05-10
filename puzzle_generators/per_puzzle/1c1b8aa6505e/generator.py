"""Generator for puzzle 8597cfd7.

Rule: gray(5) divider row + red(2)/yellow(4) cells in top/bottom
halves. Output: 2x2 of whichever color has larger |top-bot| diff.

Combinatorial axes (8): grid_h/w, divider_position, red_top, red_bot,
yellow_top, yellow_bot, anchor_corner, asymmetry_force.
Degenerates: tied_diff, no_red, no_yellow.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "1c1b8aa6505e"
VERSION = "1.1.0"
TASK_ID = "1c1b8aa6505e"
SUMMARY = "Gray divider + red/yellow halves; rule outputs 2x2 by larger |diff|."

INVARIANTS = [
    "exactly one row entirely gray(5)",
    "gray row is interior",
    ">=1 cell each of 2 and 4",
    "|red_top - red_bot| != |yellow_top - yellow_bot| (winner unambiguous)",
]

DIVIDER_POSITIONS = ("center", "upper", "lower", "spread")
DEGENERATE_TEXTURES = ("tied_diff", "no_red", "no_yellow")
HELPFUL_TEXTURES = DIVIDER_POSITIONS

AXES = {
    "grid_h":           {"type": "int", "default": "rng 9..14", "valid": "7..18"},
    "grid_w":           {"type": "int", "default": "rng 8..14", "valid": "6..18"},
    "divider_position": {"type": "str", "default": "rng helpful",
                         "valid": "|".join(DIVIDER_POSITIONS)},
    "red_top":          {"type": "int", "default": "3", "valid": "0..8"},
    "red_bot":          {"type": "int", "default": "1", "valid": "0..8"},
    "yellow_top":       {"type": "int", "default": "4", "valid": "0..8"},
    "yellow_bot":       {"type": "int", "default": "1", "valid": "0..8"},
    "anchor_corner":    {"type": "bool", "default": "false",
                         "valid": "true|false"},
    "texture":          {"type": "str", "default": "alias for divider_position",
                         "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if difficulty == "easy":
        h_lo, h_hi = 7, 10
    elif difficulty == "hard":
        h_lo, h_hi = 13, 18
    else:
        h_lo, h_hi = 9, 14
    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", h_lo - 1, h_hi)
    rng = ctx.draw_rng("placement")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], h, w, rng)
    pos = (overrides.get("texture") or
           overrides.get("divider_position")
           or ctx.draw_choice("divider_position",
                              list(DIVIDER_POSITIONS)))
    div = _pick_divider(pos, h, rng)
    g = full_grid(h, w, 0)
    for c in range(w):
        g[div][c] = 5
    rt = int(overrides.get("red_top",
                           ctx.draw_int("red_top", 2, max(2, div))))
    rb = int(overrides.get("red_bot",
                           ctx.draw_int("red_bot", 1,
                                        max(1, h - div - 1))))
    yt = int(overrides.get("yellow_top",
                           ctx.draw_int("yellow_top", 1, max(1, div))))
    yb = int(overrides.get("yellow_bot",
                           ctx.draw_int("yellow_bot", 1,
                                        max(1, h - div - 1))))
    # Ensure |red_diff| != |yellow_diff|
    if abs(rt - rb) == abs(yt - yb):
        yt = max(0, min(div, yt + 1))
    targets = {(2, "top"): rt, (2, "bot"): rb,
               (4, "top"): yt, (4, "bot"): yb}
    for (color, half), n in targets.items():
        top = (half == "top")
        for _ in range(n):
            for _ in range(20):
                if top:
                    if div == 0:
                        break
                    r = rng.randint(0, div - 1)
                else:
                    if div >= h - 1:
                        break
                    r = rng.randint(div + 1, h - 1)
                c = rng.randint(0, w - 1)
                if g[r][c] == 0:
                    g[r][c] = color
                    break
    return g


def _pick_divider(pos, h, rng):
    if pos == "upper":
        return rng.randint(2, max(2, h // 2 - 1))
    if pos == "lower":
        return rng.randint(h // 2 + 1, max(h // 2 + 1, h - 3))
    if pos == "center":
        return h // 2
    return rng.randint(2, h - 3)


def _draw_from_degenerate(name, h, w, rng):
    g = full_grid(h, w, 0)
    div = h // 2
    for c in range(w):
        g[div][c] = 5
    if name == "tied_diff":
        # |red_diff| == |yellow_diff| → ambiguous
        for c in range(2):
            g[1][c] = 2
            g[h - 2][c] = 4
        return g
    if name == "no_red":
        for c in range(2):
            g[1][c] = 4
            g[h - 2][c] = 4
        return g
    if name == "no_yellow":
        for c in range(2):
            g[1][c] = 2
            g[h - 2][c] = 2
        return g
    return g
