"""Generator for ARC task 0d3d703e.

Rule: `(rule! (recolor-map* g {1 5  2 6  3 4  4 3  5 1  6 2  8 9  9 8}))`
  Color permutation: 1↔5, 2↔6, 3↔4, 8↔9. Colors 0 and 7 unchanged.

Combinatorial axes:
  * grid_h / grid_w           — outer canvas size
  * bg                        — background color (0 or 7 — fixed by rule)
  * texture                   — pattern: noise/sparse/blob/stripes/checker/...
  * n_distinct_swap_colors    — how many of {1..6, 8, 9} appear (1..8)
  * pair_balance              — bias toward including both colors of a pair
                                vs only one side
  * neutral_density           — fraction of cells that are bg/7 (neutrals)
  * caller-opt-in degenerates: only_neutrals (no swap), one_swap_only,
                               all_pairs_balanced
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "e2f238c833a6"
VERSION = "1.1.0"  # bumped: deeper combinatorial axes added
TASK_ID = "e2f238c833a6"
SUMMARY = "Grid containing colors from the swap-set {1..6, 8, 9}; the rule applies a fixed permutation."

INVARIANTS = [
    "input contains ≥1 cell of color in {1,2,3,4,5,6,8,9}",
    "input dims in [3, 12] × [3, 12]",
    "background is one of {0, 7} (the rule's identity colors)",
]

SWAP_COLORS = (1, 2, 3, 4, 5, 6, 8, 9)
PAIRS = ((1, 5), (2, 6), (3, 4), (8, 9))
HELPFUL_TEXTURES = (
    "noise", "sparse", "blob", "stripes",
    "checker", "frame", "diagonal", "quadrants",
)
PAIR_BALANCES = ("balanced", "one_side", "skewed")
DEGENERATE_TEXTURES = ("only_neutrals", "one_swap_only", "all_pairs_balanced")

AXES = {
    "grid_h":               {"type": "int",   "default": "rng 3..12", "valid": "3..15"},
    "grid_w":               {"type": "int",   "default": "rng 3..12", "valid": "3..15"},
    "bg":                   {"type": "color", "default": "rng of {0,7}", "valid": "0|7"},
    "texture":              {"type": "str",   "default": "rng helpful",
                             "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
    "n_distinct_swap_colors": {"type": "int", "default": "rng 2..6", "valid": "1..8"},
    "pair_balance":         {"type": "str",   "default": "rng balanced|one_side|skewed",
                             "valid": "|".join(PAIR_BALANCES)},
    "neutral_density":      {"type": "float", "default": "rng 0..0.4", "valid": "0..0.9"},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)

    if difficulty == "easy":
        h_lo, h_hi, n_lo, n_hi = 3, 6, 2, 4
    elif difficulty == "hard":
        h_lo, h_hi, n_lo, n_hi = 9, 12, 5, 8
    else:
        h_lo, h_hi, n_lo, n_hi = 3, 12, 2, 6

    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", h_lo, h_hi)
    rng = ctx.draw_rng("cells")

    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], h, w, rng)

    bg = int(overrides.get("bg", ctx.draw_choice("bg", [0, 7])))
    if bg not in {0, 7}:
        bg = 0
    n_swap = int(overrides.get("n_distinct_swap_colors",
                               ctx.draw_int("n_distinct_swap_colors", n_lo, n_hi)))
    n_swap = max(1, min(8, n_swap))
    balance = overrides.get(
        "pair_balance",
        ctx.draw_choice("pair_balance", list(PAIR_BALANCES)))
    swap_palette = _select_swap_palette(n_swap, balance, rng)
    texture = overrides.get(
        "texture",
        ctx.draw_choice("texture", list(HELPFUL_TEXTURES)))
    nd = float(overrides.get(
        "neutral_density",
        ctx.draw_rng("neutral_density").uniform(0.0, 0.4)))

    g = _paint_with_texture(texture, h, w, bg, swap_palette, rng)
    if nd > 0.0:
        for r in range(h):
            for c in range(w):
                if rng.random() < nd:
                    g[r][c] = bg

    if not any(g[r][c] in SWAP_COLORS for r in range(h) for c in range(w)):
        g[rng.randint(0, h - 1)][rng.randint(0, w - 1)] = swap_palette[0]
    return g


def _select_swap_palette(n, balance, rng):
    """Pick n distinct colors from SWAP_COLORS per balance preference."""
    if balance == "balanced":
        chosen = []
        pairs = list(PAIRS)
        rng.shuffle(pairs)
        for a, b in pairs:
            if len(chosen) >= n: break
            chosen.append(a)
            if len(chosen) < n:
                chosen.append(b)
        if len(chosen) < n:
            extras = [c for c in SWAP_COLORS if c not in chosen]
            rng.shuffle(extras)
            chosen.extend(extras[:n - len(chosen)])
        return chosen[:n]
    if balance == "one_side":
        candidates = list(SWAP_COLORS)
        rng.shuffle(candidates)
        chosen = []
        used_pairs = set()
        for c in candidates:
            pair = next(p for p in PAIRS if c in p)
            if pair in used_pairs:
                continue
            chosen.append(c)
            used_pairs.add(pair)
            if len(chosen) >= n:
                break
        if len(chosen) < n:
            extras = [c for c in candidates if c not in chosen]
            chosen.extend(extras[:n - len(chosen)])
        return chosen[:n]
    candidates = list(SWAP_COLORS)
    rng.shuffle(candidates)
    return candidates[:n]


def _paint_with_texture(texture, h, w, bg, swap_palette, rng):
    g = full_grid(h, w, bg)
    if not swap_palette:
        return g
    if texture == "noise":
        for r in range(h):
            for c in range(w):
                if rng.random() < 0.6:
                    g[r][c] = rng.choice(swap_palette)
    elif texture == "sparse":
        for r in range(h):
            for c in range(w):
                if rng.random() < 0.25:
                    g[r][c] = rng.choice(swap_palette)
    elif texture == "blob":
        bh = max(1, h // 2); bw = max(1, w // 2)
        r0 = rng.randint(0, h - bh); c0 = rng.randint(0, w - bw)
        color = rng.choice(swap_palette)
        for r in range(r0, r0 + bh):
            for c in range(c0, c0 + bw):
                g[r][c] = color
        if len(swap_palette) > 1:
            color2 = rng.choice([c for c in swap_palette if c != color])
            r1 = rng.randint(0, h - bh); c1 = rng.randint(0, w - bw)
            for r in range(r1, r1 + bh):
                for c in range(c1, c1 + bw):
                    if rng.random() < 0.7:
                        g[r][c] = color2
    elif texture == "stripes":
        for r in range(h):
            color = swap_palette[r % len(swap_palette)]
            for c in range(w):
                if rng.random() < 0.7:
                    g[r][c] = color
    elif texture == "checker":
        a = swap_palette[0]
        b = swap_palette[1] if len(swap_palette) > 1 else a
        for r in range(h):
            for c in range(w):
                g[r][c] = a if (r + c) % 2 == 0 else b
    elif texture == "frame":
        border = swap_palette[0]
        inner = swap_palette[1] if len(swap_palette) > 1 else border
        for c in range(w):
            g[0][c] = border
            g[h - 1][c] = border
        for r in range(h):
            g[r][0] = border
            g[r][w - 1] = border
        for r in range(1, h - 1):
            for c in range(1, w - 1):
                if rng.random() < 0.5:
                    g[r][c] = inner
    elif texture == "diagonal":
        for k in range(min(h, w)):
            g[k][k] = swap_palette[k % len(swap_palette)]
    elif texture == "quadrants":
        for r in range(h):
            for c in range(w):
                qid = (r >= h // 2) * 2 + (c >= w // 2)
                g[r][c] = swap_palette[qid % len(swap_palette)]
    else:
        for r in range(h):
            for c in range(w):
                if rng.random() < 0.5:
                    g[r][c] = rng.choice(swap_palette)
    return g


def _draw_from_degenerate(name, h, w, rng):
    """Edge-case where the swap signature is hidden.

    only_neutrals       — only colors 0 and 7 in input; rule is no-op.
    one_swap_only       — only one swap color present; output shows just
                          that color → its pair-mate.
    all_pairs_balanced  — each pair contributes equally; output looks
                          like a coordinated re-tinting.
    """
    g = full_grid(h, w, 0)
    if name == "only_neutrals":
        for r in range(h):
            for c in range(w):
                g[r][c] = rng.choice([0, 7])
        return g
    if name == "one_swap_only":
        color = rng.choice(SWAP_COLORS)
        for r in range(h):
            for c in range(w):
                g[r][c] = color if rng.random() < 0.6 else 0
        return g
    if name == "all_pairs_balanced":
        flat = [c for pair in PAIRS for c in pair]
        for r in range(h):
            for c in range(w):
                g[r][c] = rng.choice(flat)
        return g
    return g
