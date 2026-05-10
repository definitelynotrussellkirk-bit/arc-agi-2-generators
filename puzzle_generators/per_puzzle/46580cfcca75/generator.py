"""Generator for `arc_puzzle_bank_21_more:easy_b04` — every solid
monochrome rectangle becomes a hollow frame (perimeter only).

Concept membership: 2 puzzles share this rule (same behavior as
`arc_additional_puzzle_bank_volume2:M14` but a different syntactic
canonical form, so a separate concept_hash).

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: no_rectangles, only_2x2, non_rectangular_blob.

Invariants:
  - background is 0
  - >=1 solid rectangle of a non-bg color, at least 3x3 (so the
    perimeter has visible interior after the rule fires)
  - rectangles are non-overlapping with margin >= 1
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, draw_rect

GENERATOR_ID = "46580cfcca75"
VERSION = "1.1.0"
TASK_ID = "46580cfcca75"
SUMMARY = "Several solid rectangles; rule turns each into its perimeter."

INVARIANTS = [
    "background is 0",
    ">=1 solid rectangle, each at least 3x3",
    "rectangles non-overlapping with margin >= 1",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_rectangles", "only_2x2", "non_rectangular_blob")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 12..18", "valid": "10..22"},
    "grid_w":         {"type": "int", "default": "rng 12..18", "valid": "10..22"},
    "n_rects":        {"type": "int", "default": "rng 2..4", "valid": "1..6"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "palette_size":   {"type": "int", "default": "rng 2..4", "valid": "1..6"},
    "position_bias":  {"type": "str", "default": "scattered_rectangles",
                       "valid": "scattered_rectangles"},
    "n_distinct_colors": {"type": "int", "default": "rng 2..4", "valid": "1..6"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 12, 13)
        w = ctx.draw_int("grid_w", 12, 13)
        n_rects = ctx.draw_int("n_rects", 2, 2)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 16, 21)
        w = ctx.draw_int("grid_w", 16, 21)
        n_rects = ctx.draw_int("n_rects", 4, 6)
    else:
        h = ctx.draw_int("grid_h", 12, 18)
        w = ctx.draw_int("grid_w", 12, 18)
        n_rects = ctx.draw_int("n_rects", 2, 4)
    rng = ctx.draw_rng("placement")

    g = full_grid(h, w, 0)
    placed = 0
    placed_boxes: list[tuple[int, int, int, int]] = []
    palette = list(range(1, 10))
    for _ in range(n_rects):
        for _try in range(30):
            rh = rng.randint(3, max(3, h // 3))
            rw = rng.randint(3, max(3, w // 3))
            rr = rng.randint(1, h - rh - 1)
            rc = rng.randint(1, w - rw - 1)
            ok = all(not (rr - 1 <= or2 and rr + rh >= or1
                           and rc - 1 <= oc2 and rc + rw >= oc1)
                      for (or1, oc1, or2, oc2) in placed_boxes)
            if not ok: continue
            color = rng.choice(palette)
            draw_rect(g, rr, rc, rh, rw, color)
            placed_boxes.append((rr, rc, rr + rh - 1, rc + rw - 1))
            placed += 1
            break
    if placed == 0:
        return [[0]]
    return g


def _draw_from_degenerate(name, rng):
    h, w = 14, 14
    g = full_grid(h, w, 0)
    if name == "no_rectangles":
        # Empty grid — rule has no rectangles to hollow.
        return g
    if name == "only_2x2":
        # 2x2 rectangles only — rule's "perimeter" leaves no
        # interior to clear; rule's effect is invisible.
        draw_rect(g, 2, 2, 2, 2, 4)
        draw_rect(g, 2, 8, 2, 2, 6)
        draw_rect(g, 8, 5, 2, 2, 7)
        return g
    if name == "non_rectangular_blob":
        # An L-shape (not a rectangle) — rule's "solid rectangle"
        # filter excludes; output equals input.
        for r, c in [(3, 3), (3, 4), (3, 5), (4, 3), (5, 3)]: g[r][c] = 4
        return g
    return g
