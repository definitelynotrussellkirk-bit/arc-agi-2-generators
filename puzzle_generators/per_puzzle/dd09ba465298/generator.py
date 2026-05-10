"""Generator for ARC task 08ed6ac7.

Rule: `(rule! recolor-by-rank)` — relabel each connected component with
its size rank (largest=1, 2nd=2, …). Input colors are irrelevant; the
rule overrides them.

Combinatorial axes:
  * grid_h / grid_w           — outer canvas size
  * n_objects                 — how many connected components to plant (2..6)
  * object_kind               — shape variety per object (rect/L/hollow/blob/cross/line_h/line_v)
  * size_progression          — how object sizes are spaced (linear/exponential/random_distinct)
  * placement                 — random / corners / row / column
  * input_palette_mode        — same_color / all_distinct / alternating
  * bg_color                  — usually 0; can be any color
  * noise_overlay             — sprinkle a few decoy single cells
  * caller-opt-in degenerates: single_object, ties_for_largest, all_equal_size
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "dd09ba465298"
VERSION = "1.1.0"  # bumped: deeper combinatorial axes added
TASK_ID = "dd09ba465298"
SUMMARY = "Several separated objects of varied sizes; the rule recolors them by descending size."

INVARIANTS = [
    "background is one color (usually zero)",
    "objects are 4-disconnected (each is its own component)",
    "object sizes are distinct so the rank order is unambiguous",
]

OBJECT_KINDS = (
    "rect", "L_shape", "hollow_ring", "random_blob",
    "cross", "line_h", "line_v",
)
PROGRESSIONS = ("linear", "exponential", "random_distinct")
PLACEMENTS = ("random", "corners", "row", "column", "grid")
PALETTE_MODES = ("same_color", "all_distinct", "alternating")
DEGENERATE_TEXTURES = ("single_object", "ties_for_largest", "all_equal_size")
HELPFUL_TEXTURES = OBJECT_KINDS  # texture is an alias for object_kind

AXES = {
    "grid_h":          {"type": "int", "default": "rng 9..16",  "valid": "8..22"},
    "grid_w":          {"type": "int", "default": "rng 9..16",  "valid": "8..22"},
    "n_objects":       {"type": "int", "default": "rng 2..5",   "valid": "1..6"},
    "object_kind":     {"type": "str", "default": "rng helpful",
                        "valid": "|".join(OBJECT_KINDS)},
    "size_progression": {"type": "str", "default": "rng linear|exponential|random_distinct",
                         "valid": "|".join(PROGRESSIONS)},
    "placement":       {"type": "str", "default": "rng random|corners|row|column|grid",
                        "valid": "|".join(PLACEMENTS)},
    "input_palette_mode": {"type": "str", "default": "rng same_color|all_distinct|alternating",
                           "valid": "|".join(PALETTE_MODES)},
    "bg_color":        {"type": "int", "default": "0", "valid": "0..9"},
    "noise_overlay":   {"type": "float", "default": "rng 0..0.05", "valid": "0..0.3"},
    "texture":         {"type": "str", "default": "alias for object_kind",
                        "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)

    if difficulty == "easy":
        h_lo, h_hi, n_lo, n_hi = 9, 12, 2, 3
    elif difficulty == "hard":
        h_lo, h_hi, n_lo, n_hi = 14, 16, 4, 5
    else:
        h_lo, h_hi, n_lo, n_hi = 9, 16, 2, 5

    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", h_lo, h_hi)
    rng = ctx.draw_rng("layout")

    texture_override = overrides.get("texture")
    if texture_override in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(texture_override, h, w, ctx, rng)

    n_obj = int(overrides.get("n_objects", ctx.draw_int("n_objects", n_lo, n_hi)))
    kind = (texture_override
            or overrides.get("object_kind")
            or ctx.draw_choice("object_kind", list(OBJECT_KINDS)))
    progression = overrides.get(
        "size_progression",
        ctx.draw_choice("size_progression", list(PROGRESSIONS)))
    placement = overrides.get(
        "placement",
        ctx.draw_choice("placement", list(PLACEMENTS)))
    palette_mode = overrides.get(
        "input_palette_mode",
        ctx.draw_choice("input_palette_mode", list(PALETTE_MODES)))
    bg = int(overrides.get("bg_color", 0))

    sizes = _make_sizes(n_obj, progression, rng)
    colors = ctx.draw_distinct_colors("colors", n=max(2, n_obj + 1),
                                      exclude={bg})
    obj_colors = _colors_for_mode(palette_mode, colors, n_obj, rng)

    g = full_grid(h, w, bg)
    anchors = _anchors_for_placement(placement, h, w, n_obj, sizes, rng)

    for i, ((ar, ac), s, color) in enumerate(zip(anchors, sizes, obj_colors)):
        _paint_object(g, kind, ar, ac, s, color, rng, bg)

    no = float(overrides.get(
        "noise_overlay",
        ctx.draw_rng("noise_overlay").uniform(0.0, 0.05)))
    if no > 0.0:
        # Decoy single cells — must be ≤2 cells each so they're smaller
        # than every real object (preserves rank stability).
        for _ in range(max(1, int(h * w * no))):
            r = rng.randint(0, h - 1)
            c = rng.randint(0, w - 1)
            if g[r][c] == bg:
                g[r][c] = rng.choice(obj_colors)
    return g


def _make_sizes(n, progression, rng):
    """Return n strictly-decreasing distinct positive sizes."""
    if progression == "linear":
        base = rng.randint(2, 4)
        return [base + 2 * (n - i - 1) for i in range(n)][::-1]
    if progression == "exponential":
        return [max(1, 2 ** (n - i - 1) + 1) for i in range(n)][::-1]
    # random_distinct
    pool = list(range(2, 12))
    rng.shuffle(pool)
    return sorted(pool[:n], reverse=True)


def _colors_for_mode(mode, palette, n, rng):
    """Produce n input colors per palette mode."""
    if mode == "same_color":
        return [palette[0]] * n
    if mode == "all_distinct":
        if len(palette) >= n:
            return rng.sample(palette, n)
        return [rng.choice(palette) for _ in range(n)]
    # alternating
    a = palette[0]
    b = palette[1] if len(palette) > 1 else palette[0]
    return [a if i % 2 == 0 else b for i in range(n)]


def _anchors_for_placement(placement, h, w, n, sizes, rng):
    """Return n (r, c) top-left anchors for objects of bbox-bounded sizes."""
    margin = 2
    if placement == "corners":
        candidates = [(margin, margin), (margin, w - margin - 4),
                      (h - margin - 4, margin), (h - margin - 4, w - margin - 4)]
        return candidates[:n]
    if placement == "row":
        gap = max(1, (w - 2 * margin) // max(1, n))
        return [(rng.randint(margin, max(margin, h // 2)), margin + i * gap)
                for i in range(n)]
    if placement == "column":
        gap = max(1, (h - 2 * margin) // max(1, n))
        return [(margin + i * gap, rng.randint(margin, max(margin, w // 2)))
                for i in range(n)]
    if placement == "grid":
        cols = 2 if n <= 4 else 3
        rows = (n + cols - 1) // cols
        return [(margin + (i // cols) * max(3, h // (rows + 1)),
                 margin + (i % cols) * max(3, w // (cols + 1)))
                for i in range(n)]
    # random with rejection so objects don't overlap
    placed: list[tuple[int, int, int]] = []
    out: list[tuple[int, int]] = []
    for s in sizes:
        bbox = max(2, int(s ** 0.5) + 1)
        for _ in range(40):
            r = rng.randint(margin, max(margin, h - bbox - margin))
            c = rng.randint(margin, max(margin, w - bbox - margin))
            ok = all(abs(r - pr) > pb + 1 or abs(c - pc) > pb + 1
                     for pr, pc, pb in placed)
            if ok:
                placed.append((r, c, bbox))
                out.append((r, c))
                break
        else:
            out.append((margin, margin))
    return out


def _paint_object(g, kind, rr, rc, target_size, color, rng, bg):
    """Paint one object with approximately target_size cells, kind kind."""
    h, w = len(g), len(g[0])
    side = max(2, int(target_size ** 0.5) + 1)
    sh = min(side, h - rr - 1)
    sw = min(side, w - rc - 1)
    if sh < 1 or sw < 1:
        return

    cells: list[tuple[int, int]] = []
    if kind == "rect":
        for dr in range(sh):
            for dc in range(sw):
                cells.append((rr + dr, rc + dc))
    elif kind == "L_shape":
        for dr in range(sh):
            cells.append((rr + dr, rc))
        for dc in range(1, sw):
            cells.append((rr + sh - 1, rc + dc))
    elif kind == "hollow_ring":
        for dc in range(sw):
            cells.append((rr, rc + dc))
            if sh > 1:
                cells.append((rr + sh - 1, rc + dc))
        for dr in range(1, sh - 1):
            cells.append((rr + dr, rc))
            if sw > 1:
                cells.append((rr + dr, rc + sw - 1))
    elif kind == "cross":
        mr, mc = sh // 2, sw // 2
        for dc in range(sw):
            cells.append((rr + mr, rc + dc))
        for dr in range(sh):
            if dr != mr:
                cells.append((rr + dr, rc + mc))
    elif kind == "line_h":
        for dc in range(sw):
            cells.append((rr, rc + dc))
    elif kind == "line_v":
        for dr in range(sh):
            cells.append((rr + dr, rc))
    else:  # random_blob
        cells.append((rr, rc))
        while len(cells) < target_size:
            r0, c0 = rng.choice(cells)
            for dr, dc in ((-1, 0), (1, 0), (0, -1), (0, 1)):
                nr, nc = r0 + dr, c0 + dc
                if (rr <= nr < rr + sh and rc <= nc < rc + sw
                        and (nr, nc) not in cells):
                    cells.append((nr, nc))
                    break
            else:
                break

    # Paint, capping at target_size so rank order stays correct.
    for r, c in cells[:target_size]:
        if 0 <= r < h and 0 <= c < w:
            g[r][c] = color


def _draw_from_degenerate(name, h, w, ctx, rng):
    """Edge-case input where the rank signal collapses.

    single_object    — only one object; rank-1 trivially applies, but
                       the demonstration shows no ordering.
    ties_for_largest — two objects share the maximum size; tie-break
                       is implementation-dependent.
    all_equal_size   — every object the same size; rank order depends
                       only on traversal direction.
    """
    bg = 0
    g = full_grid(h, w, bg)
    colors = ctx.draw_distinct_colors("colors", n=4, exclude={bg})
    if name == "single_object":
        size = rng.randint(3, max(3, min(6, h - 4, w - 4)))
        _paint_object(g, "rect", 2, 2, size * size, colors[0], rng, bg)
        return g
    if name == "ties_for_largest":
        s = 4
        _paint_object(g, "rect", 2, 2, s * s, colors[0], rng, bg)
        _paint_object(g, "rect", 2, w - s - 2, s * s, colors[1], rng, bg)
        _paint_object(g, "rect", h - s - 2, w // 2, 4, colors[2], rng, bg)
        return g
    if name == "all_equal_size":
        anchors = [(2, 2), (2, w - 5), (h - 5, 2), (h - 5, w - 5)]
        for i, (r, c) in enumerate(anchors[:4]):
            _paint_object(g, "rect", r, c, 4, colors[i % len(colors)], rng, bg)
        return g
    return g
