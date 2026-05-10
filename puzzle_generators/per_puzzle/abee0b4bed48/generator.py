"""Generator for puzzle 17cae0c1.

Rule: 3x(3*N) grid with N 3x3 zones. Each zone has 5s in a deliberate
pattern. Rule recolors each zone by its 5-count + position:
1=4, 8=3, 3-with-top-row=6, 3-with-bottom-row=1, else 9.

Combinatorial axes (8): n_zones, pattern_distribution, pattern_kinds,
include_repeats, anchor_corner, asymmetry_force, position_bias,
include_decoy.
Degenerates: empty_zones, all_full, single_pattern.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid
from puzzle_generators.helpers.shape import RING_3X3

GENERATOR_ID = "abee0b4bed48"
VERSION = "1.1.0"
TASK_ID = "abee0b4bed48"
SUMMARY = "3x(3N) grid with N 3x3 zones; rule recolors by 5-count + pattern."

INVARIANTS = [
    "h=3, w=3*N for N in [3, 5]",
    "each zone has 5-count in {1, 8, 3}",
    "for count=3: 5s form top row, bottom row, or middle row",
]

PATTERN_DISTRIBUTIONS = ("all_distinct", "row_focus", "edges_focus",
                         "centered_focus", "scattered")
DEGENERATE_TEXTURES = ("empty_zones", "all_full", "single_pattern")
HELPFUL_TEXTURES = PATTERN_DISTRIBUTIONS

AXES = {
    "n_zones":             {"type": "int", "default": "rng 3..5", "valid": "3..6"},
    "pattern_distribution":{"type": "str", "default": "rng helpful",
                            "valid": "|".join(PATTERN_DISTRIBUTIONS)},
    "include_repeats":     {"type": "bool", "default": "false",
                            "valid": "true|false"},
    "anchor_corner":       {"type": "bool", "default": "false",
                            "valid": "true|false"},
    "asymmetry_force":     {"type": "bool", "default": "false",
                            "valid": "true|false"},
    "position_bias":       {"type": "str", "default": "scattered",
                            "valid": "|".join(PATTERN_DISTRIBUTIONS)},
    "include_3_mid":       {"type": "bool", "default": "true",
                            "valid": "true|false"},
    "texture":             {"type": "str", "default": "alias for pattern_distribution",
                            "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


PATTERNS = {
    "one": [(1, 1)],
    "eight": RING_3X3,
    "three_top": [(0, 0), (0, 1), (0, 2)],
    "three_bot": [(2, 0), (2, 1), (2, 2)],
    "three_mid": [(1, 0), (1, 1), (1, 2)],
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], rng)
    if difficulty == "easy":
        n_lo, n_hi = 3, 3
    elif difficulty == "hard":
        n_lo, n_hi = 4, 6
    else:
        n_lo, n_hi = 3, 5
    n = int(overrides.get("n_zones", ctx.draw_int("n_zones", n_lo, n_hi)))
    n = max(3, min(6, n))
    distribution = (overrides.get("texture") or
                    overrides.get("pattern_distribution")
                    or ctx.draw_choice("pattern_distribution",
                                       list(PATTERN_DISTRIBUTIONS)))
    include_3_mid = bool(overrides.get("include_3_mid", True))
    repeats_ok = bool(overrides.get("include_repeats", False))
    pattern_keys = list(PATTERNS.keys())
    if not include_3_mid:
        pattern_keys = [k for k in pattern_keys if k != "three_mid"]
    chosen = _pick_patterns(distribution, pattern_keys, n, repeats_ok, rng)
    h = 3; w = 3 * n
    g = full_grid(h, w, 0)
    for zi, key in enumerate(chosen):
        cells = PATTERNS[key]
        zc = zi * 3
        for dr, dc in cells:
            g[dr][zc + dc] = 5
    return g


def _pick_patterns(distribution, keys, n, repeats_ok, rng):
    if distribution == "row_focus":
        # Mostly three_top + three_bot
        focus = ["three_top", "three_bot"]
        rest = [k for k in keys if k not in focus]
        if repeats_ok:
            return [rng.choice(focus + rest) for _ in range(n)]
        result = focus * (n // 2 + 1)
        rng.shuffle(result)
        rest2 = list(rest); rng.shuffle(rest2)
        return (result + rest2)[:n]
    if distribution == "edges_focus":
        focus = ["one", "eight"]
        rest = [k for k in keys if k not in focus]
        if repeats_ok:
            return [rng.choice(focus + rest) for _ in range(n)]
        result = focus * (n // 2 + 1)
        rng.shuffle(result)
        rest2 = list(rest); rng.shuffle(rest2)
        return (result + rest2)[:n]
    if distribution == "centered_focus":
        focus = ["three_mid"] if "three_mid" in keys else [keys[0]]
        rest = [k for k in keys if k not in focus]
        result = list(focus)
        rest2 = list(rest); rng.shuffle(rest2)
        return (result + rest2)[:n]
    if repeats_ok:
        return [rng.choice(keys) for _ in range(n)]
    if n <= len(keys):
        return rng.sample(keys, n)
    extras = []
    while len(extras) < n - len(keys):
        extras.append(rng.choice(keys))
    return list(keys) + extras


def _draw_from_degenerate(name, rng):
    n = 3
    h = 3; w = 3 * n
    g = full_grid(h, w, 0)
    if name == "empty_zones":
        return g
    if name == "all_full":
        for r in range(h):
            for c in range(w):
                g[r][c] = 5
        return g
    if name == "single_pattern":
        # All zones share one pattern
        for zi in range(n):
            zc = zi * 3
            g[1][zc + 1] = 5
        return g
    return g
