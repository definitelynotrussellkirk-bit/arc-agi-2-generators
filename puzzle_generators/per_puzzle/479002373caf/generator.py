"""Generator for ARC task 137eaa0f.

Rule: `(rule! (lambda (g) (set-cell (assemble-at g 5 3) 1 1 5)))`.
Scattered color-5 anchors carry local 3×3 fragments. The rule gathers
each fragment around its anchor into a single 3×3 tile (the assemble-at
step), then writes a 5 to cell (1, 1) of that tile.

Combinatorial axes:
  * grid_size           — outer canvas (kept at 11 × 11 in canonical)
  * anchor_count        — how many anchors to plant (1..5)
  * anchor_layout       — how anchors sit: random / row / column /
                          corners / center_plus
  * fragment_density    — how many cells per fragment (1..7)
  * fragment_palette    — colors used in fragments (excludes 5)
  * fragment_overlap    — how much each anchor's fragment can extend
                          (1-cell ring vs full 3×3 vs partial cells)
  * caller-opt-in degenerates: single_anchor (output is one fragment),
                               empty_fragments (anchors only, no cells around),
                               overlapping_anchors (anchors too close)
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "479002373caf"
VERSION = "1.1.0"  # bumped: deeper combinatorial axes added
TASK_ID = "479002373caf"
SUMMARY = "Scattered color-5 anchors carry local 3×3 fragments that assemble into one tile."

INVARIANTS = [
    "input is 11×11",
    "each anchor is color 5 with nearby nonzero fragment cells",
    "fragment colors exclude anchor color 5",
    "anchors are spatially separated (3-cell margin) so their fragments don't merge",
]

ANCHOR_LAYOUTS = ("random", "row", "column", "corners", "center_plus")
FRAGMENT_OVERLAPS = ("ring_only", "full_3x3", "partial")
DEGENERATE_TEXTURES = ("single_anchor", "empty_fragments", "overlapping_anchors")
HELPFUL_TEXTURES = ANCHOR_LAYOUTS

AXES = {
    "grid_size":         {"type": "int", "default": "11", "valid": "9..15"},
    "anchor_count":      {"type": "int", "default": "rng 2..5", "valid": "1..6"},
    "anchor_layout":     {"type": "str", "default": "rng helpful",
                          "valid": "|".join(ANCHOR_LAYOUTS)},
    "fragment_density":  {"type": "int", "default": "rng 2..7", "valid": "1..8"},
    "fragment_palette_size": {"type": "int", "default": "rng 2..4", "valid": "1..7"},
    "fragment_overlap":  {"type": "str", "default": "rng ring_only|full_3x3|partial",
                          "valid": "|".join(FRAGMENT_OVERLAPS)},
    "texture":           {"type": "str", "default": "alias for anchor_layout",
                          "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)

    if difficulty == "easy":
        a_lo, a_hi, p_lo, p_hi, d_lo, d_hi = 2, 3, 2, 3, 2, 4
    elif difficulty == "hard":
        a_lo, a_hi, p_lo, p_hi, d_lo, d_hi = 4, 5, 3, 4, 5, 7
    else:
        a_lo, a_hi, p_lo, p_hi, d_lo, d_hi = 2, 5, 2, 4, 2, 7

    rng = ctx.draw_rng("fragments")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], rng, ctx)

    n_anchors = int(overrides.get("anchor_count",
                                  ctx.draw_int("anchor_count", a_lo, a_hi)))
    layout = (overrides.get("texture")
              or overrides.get("anchor_layout")
              or ctx.draw_choice("anchor_layout", list(ANCHOR_LAYOUTS)))
    n_palette = int(overrides.get("fragment_palette_size",
                                  ctx.draw_int("fragment_palette_size", p_lo, p_hi)))
    palette = ctx.draw_distinct_colors(
        "fragment_palette", n=max(1, n_palette), exclude={0, 5})
    density = int(overrides.get("fragment_density",
                                ctx.draw_int("fragment_density", d_lo, d_hi)))
    overlap = overrides.get(
        "fragment_overlap",
        ctx.draw_choice("fragment_overlap", list(FRAGMENT_OVERLAPS)))

    g = full_grid(11, 11, 0)
    anchors = _anchor_pool(layout, n_anchors, rng)

    for i, (ar, ac) in enumerate(anchors):
        g[ar][ac] = 5
        offsets = _offsets_for(overlap)
        rng.shuffle(offsets)
        n_frag = max(1, min(density, len(offsets)))
        for j, (dr, dc) in enumerate(offsets[:n_frag]):
            r = ar + dr; c = ac + dc
            if 0 <= r < 11 and 0 <= c < 11 and g[r][c] == 0:
                g[r][c] = palette[(i + j) % len(palette)]
    return g


def _anchor_pool(layout, n, rng):
    """Pick n (r, c) anchor positions on the 11×11 grid with ≥3-cell margin."""
    if layout == "row":
        r = rng.randint(2, 8)
        cols = [2, 5, 8]
        return [(r, c) for c in cols][:n]
    if layout == "column":
        c = rng.randint(2, 8)
        rows = [2, 5, 8]
        return [(r, c) for r in rows][:n]
    if layout == "corners":
        return [(2, 2), (2, 8), (8, 2), (8, 8)][:n]
    if layout == "center_plus":
        return [(5, 5), (2, 5), (5, 2), (5, 8), (8, 5)][:n]
    # random with separation guarantee
    placed = []
    candidates = [(r, c) for r in range(2, 9) for c in range(2, 9)]
    rng.shuffle(candidates)
    for (r, c) in candidates:
        if all(abs(r - pr) > 2 or abs(c - pc) > 2 for (pr, pc) in placed):
            placed.append((r, c))
            if len(placed) >= n:
                break
    return placed[:n]


def _offsets_for(overlap):
    if overlap == "ring_only":
        return [(-1, -1), (-1, 0), (-1, 1),
                (0, -1),           (0, 1),
                (1, -1),  (1, 0),  (1, 1)]
    if overlap == "full_3x3":
        return [(dr, dc) for dr in (-1, 0, 1) for dc in (-1, 0, 1)
                if not (dr == 0 and dc == 0)]
    # partial — corners + cardinals (8 cells, but mixed gating)
    return [(-1, -1), (-1, 1), (1, -1), (1, 1),
            (-1, 0), (1, 0), (0, -1), (0, 1)]


def _draw_from_degenerate(name, rng, ctx):
    """Edge-case where the assemble-at signature is hidden.

    single_anchor       — only one anchor; the assembled tile is just
                          its fragment; the rule still works but
                          there's no "gathering" to demonstrate.
    empty_fragments     — anchors only, no nearby cells; output is mostly
                          empty with just a 5 written at center.
    overlapping_anchors — anchors too close so fragments overlap; the
                          assemble-at result is ambiguous.
    """
    g = full_grid(11, 11, 0)
    palette = ctx.draw_distinct_colors("palette", n=3, exclude={0, 5})
    if name == "single_anchor":
        ar, ac = 5, 5
        g[ar][ac] = 5
        for dr, dc in [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1)]:
            g[ar + dr][ac + dc] = rng.choice(palette)
        return g
    if name == "empty_fragments":
        for (r, c) in [(2, 2), (2, 8), (8, 5)]:
            g[r][c] = 5
        return g
    if name == "overlapping_anchors":
        # Two anchors only 1 cell apart — fragments collide.
        g[5][4] = 5
        g[5][6] = 5
        for dr, dc in [(-1, -1), (-1, 0), (-1, 1)]:
            g[5 + dr][4 + dc] = rng.choice(palette)
            g[5 + dr][6 + dc] = rng.choice(palette)
        return g
    return g
