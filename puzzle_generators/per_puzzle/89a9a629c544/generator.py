"""Generator for puzzle e74e1818.

Rule: for each non-bg color, flip its cells vertically within their bbox
(per-color layer flip independent of others).

Combinatorial axes: grid_h/w, n_colors, color_layout, layer_density,
asymmetric_layers (must be ud-asymmetric so flip is visible).
Degenerates: monochrome, all_layers_ud_symmetric (rule no-op),
single_color.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "89a9a629c544"
VERSION = "1.1.0"
TASK_ID = "89a9a629c544"
SUMMARY = "Multi-color grid; rule flips each non-bg color's layer vertically (within its bbox)."

INVARIANTS = [
    "background is 0",
    "≥2 non-bg colors so the rule is informative",
    "at least one color's layer is UD-asymmetric within its bbox",
]

COLOR_LAYOUTS = ("scattered", "blob_per_color", "stripes", "diagonal", "row_per_color")
DEGENERATE_TEXTURES = ("monochrome", "all_layers_ud_symmetric", "single_color")
HELPFUL_TEXTURES = COLOR_LAYOUTS

AXES = {
    "grid_h":          {"type": "int", "default": "rng 5..14", "valid": "3..18"},
    "grid_w":          {"type": "int", "default": "rng 5..14", "valid": "3..18"},
    "n_colors":        {"type": "int", "default": "rng 2..5", "valid": "2..7"},
    "color_layout":    {"type": "str", "default": "rng helpful",
                        "valid": "|".join(COLOR_LAYOUTS)},
    "layer_density":   {"type": "float", "default": "rng 0.15..0.4", "valid": "0.05..0.7"},
    "texture":         {"type": "str", "default": "alias for color_layout",
                        "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if difficulty == "easy":
        h_lo, h_hi, n_lo, n_hi = 5, 7, 2, 3
    elif difficulty == "hard":
        h_lo, h_hi, n_lo, n_hi = 11, 14, 4, 5
    else:
        h_lo, h_hi, n_lo, n_hi = 5, 14, 2, 5
    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", h_lo, h_hi)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], h, w, ctx, rng)
    n = int(overrides.get("n_colors", ctx.draw_int("n_colors", n_lo, n_hi)))
    palette = list(ctx.draw_distinct_colors("palette", n=max(2, n), exclude={0}))
    layout = (overrides.get("texture") or overrides.get("color_layout")
              or ctx.draw_choice("color_layout", list(COLOR_LAYOUTS)))
    density = float(overrides.get("layer_density",
                                  ctx.draw_rng("layer_density").uniform(0.15, 0.4)))
    g = full_grid(h, w, 0)
    for i, color in enumerate(palette):
        cells = _layer_cells(layout, h, w, density, i, len(palette), rng)
        for (r, c) in cells:
            if g[r][c] == 0:
                g[r][c] = color
    # Force at least one color to have UD-asymmetry within its bbox.
    _force_one_asymmetric(g, palette, rng)
    return g


def _layer_cells(layout, h, w, density, idx, total, rng):
    n = max(1, int(h * w * density))
    if layout == "scattered":
        cells = [(r, c) for r in range(h) for c in range(w)]
        rng.shuffle(cells)
        return cells[:n]
    if layout == "blob_per_color":
        bh = max(1, h // (total + 1)); bw = max(1, w // 2)
        r0 = rng.randint(0, max(0, h - bh))
        c0 = rng.randint(0, max(0, w - bw))
        return [(r, c) for r in range(r0, r0 + bh) for c in range(c0, c0 + bw)]
    if layout == "stripes":
        # Each color gets every (idx + total)-th row.
        return [(r, c) for r in range(idx, h, total) for c in range(w)
                if rng.random() < density * 1.5]
    if layout == "diagonal":
        return [(k, (k + idx) % w) for k in range(min(h, w * 2))][:n]
    if layout == "row_per_color":
        r = idx % h
        return [(r, c) for c in range(w)]
    cells = [(r, c) for r in range(h) for c in range(w)]
    rng.shuffle(cells)
    return cells[:n]


def _force_one_asymmetric(g, palette, rng):
    """Ensure ≥1 color's layer is UD-asymmetric within its bbox."""
    h = len(g); w = len(g[0])
    for color in palette:
        cells = [(r, c) for r in range(h) for c in range(w) if g[r][c] == color]
        if not cells:
            continue
        rs = [r for r, _ in cells]; cs = [c for _, c in cells]
        r1, r2 = min(rs), max(rs)
        c1, c2 = min(cs), max(cs)
        cells_set = set(cells)
        is_sym = all(((r, c) in cells_set) == ((r1 + r2 - r, c) in cells_set)
                     for r in range(r1, r2 + 1) for c in range(c1, c2 + 1))
        if not is_sym:
            return  # already asymmetric
    # Otherwise: add a single cell of the first color to break symmetry.
    if palette:
        for r in range(h):
            for c in range(w):
                if g[r][c] == 0:
                    g[r][c] = palette[0]
                    return


def _draw_from_degenerate(name, h, w, ctx, rng):
    palette = list(ctx.draw_distinct_colors("palette", n=4, exclude={0}))
    g = full_grid(h, w, 0)
    if name == "monochrome":
        c0 = palette[0]
        for r in range(h):
            for c in range(w):
                if rng.random() < 0.4:
                    g[r][c] = c0
        # ensure ≥1 cell
        g[0][0] = c0
        return g
    if name == "all_layers_ud_symmetric":
        # Each color's layer is UD-symmetric within its bbox.
        for color in palette[:3]:
            r1, r2 = rng.randint(0, h // 2 - 1), rng.randint(h // 2 + 1, h - 1)
            c1, c2 = rng.randint(0, w // 2), rng.randint(w // 2, w - 1)
            mid = (r1 + r2) // 2
            for r in range(r1, mid + 1):
                for c in range(c1, c2 + 1):
                    if rng.random() < 0.5:
                        g[r][c] = color
                        g[r1 + r2 - r][c] = color
        return g
    if name == "single_color":
        c0 = palette[0]
        for r in range(h):
            for c in range(w):
                if rng.random() < 0.3:
                    g[r][c] = c0
        g[0][0] = c0
        return g
    return g
