"""Generator for ARC task 1e81d6f9.

Rule: target = g[1][1]. For each cell: if v == target AND (r, c) != (1, 1)
→ 0; else keep v. (Erase all duplicates of the (1,1) value, except (1,1)
itself.)

Combinatorial axes: grid_h/w, target_color, n_target_copies (≥1 outside
(1,1)), other_palette_size, decoy_density, target_layout.
Degenerates: only_target_at_11 (rule no-op), target_everywhere,
no_decoys.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "7fc997c58be3"
VERSION = "1.1.0"
TASK_ID = "7fc997c58be3"
SUMMARY = "Multicolor grid; the color at (1,1) appears elsewhere — rule erases duplicates."

INVARIANTS = [
    "grid is at least 3 × 3",
    "the target color appears at (1, 1)",
    "≥1 other occurrence of the target color so the rule has effect",
]

TARGET_LAYOUTS = ("scattered", "cluster", "row", "column", "corners")
DEGENERATE_TEXTURES = ("only_target_at_11", "target_everywhere", "no_decoys")
HELPFUL_TEXTURES = TARGET_LAYOUTS

AXES = {
    "grid_h":              {"type": "int", "default": "rng 5..15", "valid": "3..22"},
    "grid_w":              {"type": "int", "default": "rng 5..15", "valid": "3..22"},
    "target_color":        {"type": "color", "default": "rng (≠0)", "valid": "1..9"},
    "n_target_copies":     {"type": "int", "default": "rng 2..6", "valid": "1..15"},
    "other_palette_size":  {"type": "int", "default": "rng 2..5", "valid": "1..8"},
    "decoy_density":       {"type": "float", "default": "rng 0.2..0.5", "valid": "0..1"},
    "target_layout":       {"type": "str", "default": "rng helpful",
                            "valid": "|".join(TARGET_LAYOUTS)},
    "texture":             {"type": "str", "default": "alias for target_layout",
                            "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if difficulty == "easy":
        h_lo, h_hi, n_lo, n_hi = 5, 8, 1, 3
    elif difficulty == "hard":
        h_lo, h_hi, n_lo, n_hi = 13, 15, 5, 8
    else:
        h_lo, h_hi, n_lo, n_hi = 5, 15, 2, 6
    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", h_lo, h_hi)
    rng = ctx.draw_rng("cells")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], h, w, ctx, rng)
    target = int(overrides.get("target_color", ctx.draw_color("target_color", exclude={0})))
    n_copies = int(overrides.get("n_target_copies",
                                 ctx.draw_int("n_target_copies", n_lo, n_hi)))
    n_other = int(overrides.get("other_palette_size",
                                ctx.draw_int("other_palette_size", 2, 5)))
    others = list(ctx.draw_distinct_colors("others", n=max(1, n_other), exclude={0, target}))
    decoy_d = float(overrides.get("decoy_density",
                                  ctx.draw_rng("decoy_density").uniform(0.2, 0.5)))
    layout = (overrides.get("texture") or overrides.get("target_layout")
              or ctx.draw_choice("target_layout", list(TARGET_LAYOUTS)))
    g = full_grid(h, w, 0)
    # Decoys
    for r in range(h):
        for c in range(w):
            if rng.random() < decoy_d:
                g[r][c] = rng.choice(others)
    # Place target at (1, 1) and additional copies.
    g[1][1] = target
    target_positions = _target_layout(layout, h, w, n_copies, rng)
    placed = 0
    for (r, c) in target_positions:
        if (r, c) == (1, 1):
            continue
        g[r][c] = target
        placed += 1
        if placed >= n_copies:
            break
    if placed == 0:
        # Force at least one other copy.
        for r in range(h):
            for c in range(w):
                if (r, c) != (1, 1) and g[r][c] != target:
                    g[r][c] = target
                    return g
    return g


def _target_layout(layout, h, w, n, rng):
    if layout == "cluster":
        cr = rng.randint(0, h - 1); cc = rng.randint(0, w - 1)
        cells = [(r, c) for r in range(h) for c in range(w)]
        cells.sort(key=lambda rc: abs(rc[0] - cr) + abs(rc[1] - cc))
        return cells[:n + 5]
    if layout == "row":
        r = rng.randint(0, h - 1)
        cells = [(r, c) for c in range(w)]
        rng.shuffle(cells)
        return cells[:n + 5]
    if layout == "column":
        c = rng.randint(0, w - 1)
        cells = [(r, c) for r in range(h)]
        rng.shuffle(cells)
        return cells[:n + 5]
    if layout == "corners":
        cands = [(0, 0), (0, w - 1), (h - 1, 0), (h - 1, w - 1)]
        rng.shuffle(cands)
        return cands[:n + 5]
    cells = [(r, c) for r in range(h) for c in range(w)]
    rng.shuffle(cells)
    return cells[:n + 5]


def _draw_from_degenerate(name, h, w, ctx, rng):
    target = ctx.draw_color("target_color", exclude={0})
    others = list(ctx.draw_distinct_colors("others", n=3, exclude={0, target}))
    g = full_grid(h, w, 0)
    if name == "only_target_at_11":
        # Only one copy of target, at (1,1). Rule no-op.
        g[1][1] = target
        for r in range(h):
            for c in range(w):
                if (r, c) != (1, 1) and rng.random() < 0.4:
                    g[r][c] = rng.choice(others)
        return g
    if name == "target_everywhere":
        for r in range(h):
            for c in range(w):
                g[r][c] = target
        return g
    if name == "no_decoys":
        # Only target color; (1,1) plus other copies. Rule erases duplicates.
        g[1][1] = target
        for r, c in [(0, 0), (h - 1, w - 1), (h // 2, w // 2)]:
            if (r, c) != (1, 1):
                g[r][c] = target
        return g
    return g
