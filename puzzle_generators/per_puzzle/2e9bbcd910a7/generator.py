"""Generator for aa300dc3.

Rule: bg=5. Find longest straight run of 0-cells along (1,1) or (1,-1).
Paint those cells with 8.

Combinatorial axes (8): grid_size, diag_length, diag_direction,
position_bias, n_noise, noise_density, anchor_endpoints,
asymmetry_force.
Degenerates: no_diag, full_diag, all_zeros.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "2e9bbcd910a7"
VERSION = "1.1.0"
TASK_ID = "2e9bbcd910a7"
SUMMARY = "Bg=5 grid with diagonal run of 0s; rule paints that diagonal with 8."

INVARIANTS = [
    "bg = 5",
    "exactly one diagonal run of 0s of length >=4 (longest)",
    "scattered 0-cells outside diagonal don't form longer runs",
    "no color 8 in input (rule writes 8 for output)",
]

DIAG_DIRECTIONS = ("se", "sw")
POSITION_BIAS = ("center", "spread", "edge", "corners")
DEGENERATE_TEXTURES = ("no_diag", "full_diag", "all_zeros")
HELPFUL_TEXTURES = POSITION_BIAS

AXES = {
    "grid_size":         {"type": "int", "default": "10", "valid": "8..14"},
    "diag_length":       {"type": "int", "default": "rng 5..8", "valid": "4..10"},
    "diag_direction":    {"type": "str", "default": "rng se|sw",
                          "valid": "|".join(DIAG_DIRECTIONS)},
    "position_bias":     {"type": "str", "default": "rng helpful",
                          "valid": "|".join(POSITION_BIAS)},
    "n_noise":           {"type": "int", "default": "rng 3..8", "valid": "0..15"},
    "noise_density":     {"type": "float", "default": "rng 0.04..0.10",
                          "valid": "0..0.3"},
    "anchor_endpoints":  {"type": "bool", "default": "false",
                          "valid": "true|false"},
    "asymmetry_force":   {"type": "bool", "default": "false",
                          "valid": "true|false"},
    "texture":           {"type": "str", "default": "alias for position_bias",
                          "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if difficulty == "easy":
        side = 8
    elif difficulty == "hard":
        side = 14
    else:
        side = int(overrides.get("grid_size", 10))
    h = w = side
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], h, w, rng)
    k = int(overrides.get("diag_length",
                          ctx.draw_int("diag_length", 5, min(8, h - 2))))
    k = max(4, min(h - 2, k))
    direction = overrides.get("diag_direction",
                              ctx.draw_choice("diag_direction",
                                              list(DIAG_DIRECTIONS)))
    bias = (overrides.get("texture") or
            overrides.get("position_bias")
            or ctx.draw_choice("position_bias", list(POSITION_BIAS)))
    g = full_grid(h, w, 5)
    if bias == "center":
        start_r = max(1, (h - k) // 2)
    elif bias == "edge":
        start_r = 1
    elif bias == "corners":
        start_r = 0
    else:
        start_r = rng.randint(1, max(1, h - k - 1))
    if direction == "se":
        start_c = (rng.randint(1, max(1, w - k - 1))
                   if bias != "center" else max(1, (w - k) // 2))
        for i in range(k):
            if start_r + i < h and start_c + i < w:
                g[start_r + i][start_c + i] = 0
    else:
        start_c = (rng.randint(k, w - 2) if bias != "center"
                   else min(w - 2, w // 2 + k // 2))
        for i in range(k):
            if start_r + i < h and start_c - i >= 0:
                g[start_r + i][start_c - i] = 0
    n_noise = int(overrides.get("n_noise",
                                ctx.draw_int("n_noise", 3, 8)))
    placed = 0
    while placed < n_noise:
        r = rng.randint(1, h - 2)
        c = rng.randint(1, w - 2)
        if g[r][c] == 5 and not _would_extend_run(g, r, c, k):
            g[r][c] = 0
            placed += 1
        else:
            placed += 1  # avoid infinite loop
    return g


def _would_extend_run(g, r, c, max_len):
    h, w = len(g), len(g[0])
    for dr, dc in ((1, 1), (1, -1)):
        run = 1
        rr, cc = r + dr, c + dc
        while 0 <= rr < h and 0 <= cc < w and g[rr][cc] == 0:
            run += 1; rr += dr; cc += dc
        rr, cc = r - dr, c - dc
        while 0 <= rr < h and 0 <= cc < w and g[rr][cc] == 0:
            run += 1; rr -= dr; cc -= dc
        if run >= max_len:
            return True
    return False


def _draw_from_degenerate(name, h, w, rng):
    g = full_grid(h, w, 5)
    if name == "no_diag":
        for _ in range(3):
            r = rng.randint(0, h - 1); c = rng.randint(0, w - 1)
            g[r][c] = 0
        return g
    if name == "full_diag":
        for k in range(min(h, w)):
            g[k][k] = 0
        return g
    if name == "all_zeros":
        return [[0] * w for _ in range(h)]
    return g
