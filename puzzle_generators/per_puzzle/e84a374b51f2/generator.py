"""Generator for c1990cce.

Rule: input is 1×N row. Output is N×N: a 2-diamond on top half + 1s
periodic pattern. Rule's output depends ONLY on N = cols(input); input
content is otherwise ignored — but we still vary input distribution
to expose the model to varied perceptual cues.

Combinatorial axes (8): grid_n, marker_position, n_distractors,
distractor_palette_size, distractor_layout, decoy_color_kind,
include_marker, anchor_endpoints.
Degenerates: empty_row, all_same_color, no_marker.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "e84a374b51f2"
VERSION = "1.1.0"
TASK_ID = "e84a374b51f2"
SUMMARY = "1×N row; rule produces N×N diamond+stripes from N alone."

INVARIANTS = [
    "1-row grid (h = 1)",
    "N (= cols) odd in {5, 7, 9, 11, 13, 15}",
    "input may have decoy non-bg cells but they don't affect rule",
]

DISTRACTOR_LAYOUTS = ("scattered", "left_biased", "right_biased",
                      "alternating", "edges_only", "center_only")
DEGENERATE_TEXTURES = ("empty_row", "all_same_color", "no_marker")
HELPFUL_TEXTURES = DISTRACTOR_LAYOUTS

AXES = {
    "grid_n":                {"type": "int", "default": "rng 5..15 odd",
                              "valid": "5..15 odd"},
    "marker_position":       {"type": "int", "default": "n//2", "valid": "0..n-1"},
    "n_distractors":         {"type": "int", "default": "rng 0..3", "valid": "0..6"},
    "distractor_palette_size": {"type": "int", "default": "rng 1..3",
                                "valid": "1..7"},
    "distractor_layout":     {"type": "str", "default": "rng helpful",
                              "valid": "|".join(DISTRACTOR_LAYOUTS)},
    "include_marker":        {"type": "bool", "default": "true",
                              "valid": "true|false"},
    "decoy_color_kind":      {"type": "str", "default": "rng warm|cool|mixed",
                              "valid": "warm|cool|mixed"},
    "texture":               {"type": "str", "default": "alias for distractor_layout",
                              "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    rng = ctx.draw_rng("layout")
    if difficulty == "easy":
        n_choices = [5, 7]
    elif difficulty == "hard":
        n_choices = [11, 13, 15]
    else:
        n_choices = [5, 7, 9, 11, 13, 15]
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        n = rng.choice(n_choices)
        return _draw_from_degenerate(overrides["texture"], n, rng)
    n = int(overrides.get("grid_n", rng.choice(n_choices)))
    if n % 2 == 0:
        n += 1
    n = max(5, min(15, n))
    g = full_grid(1, n, 0)
    if bool(overrides.get("include_marker", True)):
        marker_pos = int(overrides.get("marker_position", n // 2))
        marker_pos = max(0, min(n - 1, marker_pos))
        g[0][marker_pos] = 2
    n_distractors = int(overrides.get("n_distractors",
                                      ctx.draw_int("n_distractors", 0, 3)))
    n_distractors = max(0, min(n - 1, n_distractors))
    distractor_pal_size = int(overrides.get("distractor_palette_size",
                                            ctx.draw_int("distractor_palette_size",
                                                         1, 3)))
    decoy_kind = overrides.get("decoy_color_kind",
                               ctx.draw_choice("decoy_color_kind",
                                               ["warm", "cool", "mixed"]))
    if decoy_kind == "warm":
        decoy_pool = [3, 4, 6, 9]
    elif decoy_kind == "cool":
        decoy_pool = [1, 5, 7, 8]
    else:
        decoy_pool = [3, 4, 5, 6, 7, 8, 9]
    rng.shuffle(decoy_pool)
    distractor_palette = decoy_pool[:max(1, distractor_pal_size)]
    layout = (overrides.get("texture") or overrides.get("distractor_layout")
              or ctx.draw_choice("distractor_layout", list(DISTRACTOR_LAYOUTS)))
    candidate_cols = [c for c in range(n) if g[0][c] == 0]
    chosen_cols = _pick_distractor_cols(layout, candidate_cols, n_distractors,
                                        n, rng)
    for c in chosen_cols:
        g[0][c] = rng.choice(distractor_palette)
    return g


def _pick_distractor_cols(layout, candidate, k, n, rng):
    if not candidate or k <= 0:
        return []
    if layout == "left_biased":
        candidate = sorted(candidate)
        return candidate[:k]
    if layout == "right_biased":
        candidate = sorted(candidate, reverse=True)
        return candidate[:k]
    if layout == "edges_only":
        edges = [c for c in candidate if c == 0 or c == n - 1]
        return edges[:k] if edges else candidate[:k]
    if layout == "center_only":
        center = n // 2
        candidate = sorted(candidate, key=lambda c: abs(c - center))
        return candidate[:k]
    if layout == "alternating":
        return [c for c in candidate if c % 2 == 0][:k]
    rng.shuffle(candidate)
    return candidate[:k]


def _draw_from_degenerate(name, n, rng):
    g = full_grid(1, n, 0)
    if name == "empty_row":
        return g
    if name == "all_same_color":
        c = rng.choice([1, 3, 4, 5, 6, 7, 8, 9])
        for j in range(n):
            g[0][j] = c
        return g
    if name == "no_marker":
        for j in range(n):
            if rng.random() < 0.4:
                g[0][j] = rng.choice([1, 3, 4, 5, 6, 7, 8, 9])
        return g
    return g
