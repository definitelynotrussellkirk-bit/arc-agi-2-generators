"""Generator for ARC task be94b721.

Rule: `(rule! extract-largest)` — return a crop of the largest connected
non-zero object, by cell count.

Combinatorial axes:
  * grid_h / grid_w        — outer canvas size
  * largest_kind           — shape of the dominant object (rect / L / hollow / blob / cross / line_h / line_v)
  * largest_h / largest_w  — bbox of the dominant object
  * n_distractors          — number of other objects (1..6)
  * distractor_size_dist   — "tiny" (all 1-2 cells), "mixed" (1-4 cells),
                              "close" (one distractor up to ~70% of largest)
  * placement              — where the largest sits (random / center / corner)
  * caller-opt-in degenerates: ties_for_largest, single_object
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import draw_rect, full_grid

GENERATOR_ID = "fea6a4ce763f"
VERSION = "1.1.0"  # bumped: deeper combinatorial axes added
TASK_ID = "fea6a4ce763f"
SUMMARY = "Several separated colored objects; the rule crops the largest object."

INVARIANTS = [
    "background is zero",
    "there is exactly one object with strictly largest cell count",
    "objects are spatially separated (4-connected components don't merge)",
]

LARGEST_KINDS = (
    "rect", "L_shape", "hollow_ring", "random_blob",
    "cross", "line_h", "line_v",
)
DISTRACTOR_SHAPES = ("rect", "single", "line_h", "line_v", "L_shape")
SIZE_DISTRIBUTIONS = ("tiny", "mixed", "close")
PLACEMENTS = ("random", "left_half", "center", "corner")
HELPFUL_TEXTURES = LARGEST_KINDS  # "texture" maps to largest_kind for symmetry with other gens
DEGENERATE_TEXTURES = ("ties_for_largest", "single_object")

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..22",  "valid": "8..30"},
    "grid_w":         {"type": "int", "default": "rng 10..26", "valid": "10..30"},
    "largest_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(LARGEST_KINDS)},
    "largest_h":      {"type": "int", "default": "rng 3..10",   "valid": "3..12"},
    "largest_w":      {"type": "int", "default": "rng 3..10",   "valid": "3..12"},
    "n_distractors":  {"type": "int", "default": "rng 2..6",    "valid": "1..8"},
    "distractor_size_dist": {"type": "str", "default": "rng tiny|mixed|close",
                             "valid": "|".join(SIZE_DISTRIBUTIONS)},
    "placement":      {"type": "str", "default": "rng random|left_half|center|corner",
                       "valid": "|".join(PLACEMENTS)},
    "texture":        {"type": "str", "default": "rng helpful (alias for largest_kind)",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)

    if difficulty == "easy":
        h_lo, h_hi, w_lo, w_hi = 8, 11, 10, 14
    elif difficulty == "hard":
        h_lo, h_hi, w_lo, w_hi = 16, 22, 18, 26
    else:
        h_lo, h_hi, w_lo, w_hi = 8, 22, 10, 26

    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", w_lo, w_hi)
    rng = ctx.draw_rng("placement")

    # Caller-opt-in degenerate path.
    texture_override = overrides.get("texture")
    if texture_override in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(texture_override, h, w, ctx, rng)

    # Pick the dominant-object kind. `texture` and `largest_kind` are aliases.
    kind = (texture_override
            or overrides.get("largest_kind")
            or ctx.draw_choice("largest_kind", list(LARGEST_KINDS)))

    lh = ctx.draw_int("largest_h", 4, min(10, h - 3))
    lw = ctx.draw_int("largest_w", 3, min(10, (w // 2) - 1))

    # Draw enough colors for one dominant + n_distractors.
    n_dist = int(overrides.get("n_distractors", ctx.draw_int("n_distractors", 2, 6)))
    n_colors = max(2, n_dist + 1)
    colors = ctx.draw_distinct_colors("colors", n=min(9, n_colors), exclude={0})

    # Placement of dominant object.
    placement = overrides.get(
        "placement",
        ctx.draw_choice("placement", list(PLACEMENTS)),
    )
    lr, lc = _place_largest(placement, h, w, lh, lw, rng)

    g = full_grid(h, w, 0)
    _paint_object(g, kind, lr, lc, lh, lw, colors[0], rng)
    largest_area = sum(1 for r in range(lr, lr + lh) for c in range(lc, lc + lw)
                       if g[r][c] == colors[0])

    # Distractors. Their sizes are bounded so the dominant remains strictly largest.
    size_dist = overrides.get(
        "distractor_size_dist",
        ctx.draw_choice("distractor_size_dist", list(SIZE_DISTRIBUTIONS)),
    )
    _plant_distractors(g, n_dist, colors[1:], size_dist, largest_area, rng)
    return g


def _place_largest(placement, h, w, lh, lw, rng):
    """Pick (lr, lc) — top-left of the largest object's bbox — given placement."""
    if placement == "left_half":
        return (rng.randint(1, h - lh - 1),
                rng.randint(1, max(1, (w // 2) - lw - 1)))
    if placement == "center":
        return ((h - lh) // 2, (w - lw) // 2)
    if placement == "corner":
        corners = [(1, 1), (1, w - lw - 1),
                   (h - lh - 1, 1), (h - lh - 1, w - lw - 1)]
        return rng.choice(corners)
    # random
    return (rng.randint(1, h - lh - 1),
            rng.randint(1, w - lw - 1))


def _paint_object(g, kind, rr, rc, sh, sw, color, rng):
    """Paint one object of given kind into g[rr:rr+sh, rc:rc+sw]."""
    if kind == "rect":
        for dr in range(sh):
            for dc in range(sw):
                g[rr + dr][rc + dc] = color
    elif kind == "L_shape":
        for dr in range(sh):
            g[rr + dr][rc] = color
        for dc in range(sw):
            g[rr + sh - 1][rc + dc] = color
    elif kind == "hollow_ring":
        for dc in range(sw):
            g[rr][rc + dc] = color
            g[rr + sh - 1][rc + dc] = color
        for dr in range(sh):
            g[rr + dr][rc] = color
            g[rr + dr][rc + sw - 1] = color
    elif kind == "random_blob":
        # Solid plus random sprinkle to ensure connectivity.
        for dr in range(sh):
            for dc in range(sw):
                if rng.random() < 0.65:
                    g[rr + dr][rc + dc] = color
        # Force corners so the bbox extent is well-defined.
        g[rr][rc] = color
        g[rr][rc + sw - 1] = color
        g[rr + sh - 1][rc] = color
        g[rr + sh - 1][rc + sw - 1] = color
    elif kind == "cross":
        mr, mc = sh // 2, sw // 2
        for dc in range(sw):
            g[rr + mr][rc + dc] = color
        for dr in range(sh):
            g[rr + dr][rc + mc] = color
    elif kind == "line_h":
        mid = sh // 2
        for dc in range(sw):
            g[rr + mid][rc + dc] = color
    elif kind == "line_v":
        mid = sw // 2
        for dr in range(sh):
            g[rr + dr][rc + mid] = color
    else:
        # Fallback: solid rect.
        for dr in range(sh):
            for dc in range(sw):
                g[rr + dr][rc + dc] = color


def _plant_distractors(g, n, palette, size_dist, largest_area, rng):
    """Place n distractor objects, each bounded so largest remains strictly largest."""
    h, w = len(g), len(g[0])
    if size_dist == "close":
        max_size = max(2, int(largest_area * 0.7))
    elif size_dist == "tiny":
        max_size = 2
    else:  # mixed
        max_size = max(2, int(largest_area * 0.4))

    for i in range(n):
        color = palette[i % len(palette)] if palette else 0
        # Try a few placements until one fits and doesn't overlap existing fg.
        for _ in range(15):
            ds = max(1, min(max_size, rng.randint(1, max_size)))
            dh = max(1, min(rng.randint(1, ds), h - 2))
            dw = max(1, min(max(1, ds // max(dh, 1)), w - 2))
            shape = rng.choice(DISTRACTOR_SHAPES)
            rr = rng.randint(1, h - dh - 1)
            rc = rng.randint(1, w - dw - 1)
            # Check non-overlap (4-connected, with 1-cell gap).
            collide = False
            for r in range(max(0, rr - 1), min(h, rr + dh + 1)):
                for c in range(max(0, rc - 1), min(w, rc + dw + 1)):
                    if g[r][c] != 0:
                        collide = True
                        break
                if collide:
                    break
            if not collide:
                # Cap distractor area to <= max_size cells.
                _paint_object(g, shape, rr, rc, dh, dw, color, rng)
                # Trim if shape exceeded max_size.
                cells = [(r, c) for r in range(rr, rr + dh)
                                  for c in range(rc, rc + dw)
                                  if g[r][c] == color]
                if len(cells) > max_size:
                    extras = cells[max_size:]
                    for r, c in extras:
                        g[r][c] = 0
                break


def _draw_from_degenerate(name, h, w, ctx, rng):
    """Edge-case where the rule's "largest object" signature is hidden.

    ties_for_largest — two objects of identical cell count exist. The rule
                       returns one of them (Racket's `pick-max` is
                       deterministic), but the demonstration is ambiguous
                       to a model that hasn't internalized the tie-break.
    single_object    — only one foreground object exists, so any "select"
                       rule (largest, smallest, by-color) produces the
                       same output. Demonstration carries less rule signal.
    """
    g = full_grid(h, w, 0)
    colors = ctx.draw_distinct_colors("colors", n=3, exclude={0})
    if name == "ties_for_largest":
        # Place two identical-size 4x4 rectangles plus one smaller distractor.
        size = 4
        draw_rect(g, 1, 1, size, size, colors[0])
        draw_rect(g, 1, w - size - 1, size, size, colors[1])
        draw_rect(g, h - 3, max(1, w // 2 - 1), 2, 2, colors[2])
        return g
    if name == "single_object":
        size = rng.randint(3, max(3, min(6, h - 2, w - 2)))
        draw_rect(g, 1, 1, size, size, colors[0])
        return g
    return g
