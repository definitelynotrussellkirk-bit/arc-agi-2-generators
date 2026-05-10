"""Generator for ARC task e633a9e5.

Rule: `(rule! (lambda (g) (scale-map g (list 2 1 2) (list 2 1 2))))`.
Non-uniform scaling: rows 0 and 2 are duplicated (×2), row 1 stays (×1);
columns the same way. The 3 × 3 input becomes a 5 × 5 output.

Combinatorial axes:
  * grid_size           — input side (canonical is 3)
  * palette_size        — number of distinct colors
  * texture             — pattern type (noise/sparse/blob/checker/...)
  * cell_distinctness   — how clearly each cell is different from
                          neighbors (boosts the scale's visual signal)
  * caller-opt-in degenerates: monochrome (output uniform too),
                               row_uniform (rows scale to fat bands),
                               diagonal (sparse — scale less obvious)
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "ecd1058990ce"
VERSION = "1.1.0"  # bumped: deeper combinatorial axes added
TASK_ID = "ecd1058990ce"
SUMMARY = "A 3 × 3 multicolor grid; outer rows and columns each duplicate in the output."

INVARIANTS = [
    "input is 3 × 3",
    "≥2 distinct colors so the scale's effect is visible",
    "colors are sampled from a small palette",
]

HELPFUL_TEXTURES = (
    "noise", "checker", "row_distinct", "col_distinct",
    "diagonal", "frame_inner", "blob", "gradient",
)
DEGENERATE_TEXTURES = ("monochrome", "row_uniform", "col_uniform")

AXES = {
    "grid_size":         {"type": "int",   "default": "3", "valid": "3..3"},
    "palette_size":      {"type": "int",   "default": "rng 3..7", "valid": "2..10"},
    "texture":           {"type": "str",   "default": "rng helpful",
                          "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
    "cell_distinctness": {"type": "str",   "default": "rng strict|loose",
                          "valid": "strict|loose"},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)

    if difficulty == "easy":
        c_lo, c_hi = 3, 5
    elif difficulty == "hard":
        c_lo, c_hi = 6, 9
    else:
        c_lo, c_hi = 3, 7

    n_colors = ctx.draw_int("palette_size", c_lo, c_hi)
    palette = ctx.draw_distinct_colors("palette", n=n_colors)
    rng = ctx.draw_rng("cells")

    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], palette, rng)

    texture = overrides.get(
        "texture",
        ctx.draw_choice("texture", list(HELPFUL_TEXTURES)))
    distinctness = overrides.get(
        "cell_distinctness",
        ctx.draw_choice("cell_distinctness", ["strict", "loose"]))
    g = _paint_texture(texture, palette, rng)

    if distinctness == "strict":
        # Make sure adjacent cells differ so the scale produces clear bands.
        for r in range(3):
            for c in range(3):
                neighbors = [(r - 1, c), (r + 1, c), (r, c - 1), (r, c + 1)]
                for nr, nc in neighbors:
                    if 0 <= nr < 3 and 0 <= nc < 3 and g[nr][nc] == g[r][c]:
                        for alt in palette:
                            if alt != g[r][c]:
                                g[r][c] = alt
                                break
                        break

    # Invariant: ≥2 distinct colors.
    if len({v for row in g for v in row}) < 2:
        g[0][0] = palette[0]
        g[2][2] = palette[1] if len(palette) > 1 else palette[0]
    return g


def _paint_texture(texture, palette, rng):
    g = full_grid(3, 3, palette[0])
    if texture == "noise":
        for r in range(3):
            for c in range(3):
                g[r][c] = rng.choice(palette)
    elif texture == "checker":
        a, b = (palette[0], palette[1]) if len(palette) > 1 else (palette[0], palette[0])
        for r in range(3):
            for c in range(3):
                g[r][c] = a if (r + c) % 2 == 0 else b
    elif texture == "row_distinct":
        for r in range(3):
            color = palette[r % len(palette)]
            for c in range(3):
                g[r][c] = color if rng.random() < 0.7 else rng.choice(palette)
    elif texture == "col_distinct":
        for c in range(3):
            color = palette[c % len(palette)]
            for r in range(3):
                g[r][c] = color if rng.random() < 0.7 else rng.choice(palette)
    elif texture == "diagonal":
        for k in range(3):
            g[k][k] = palette[k % len(palette)]
        # fill remaining with a different color
        bg = palette[-1] if palette[-1] != palette[0] else palette[0]
        for r in range(3):
            for c in range(3):
                if r != c:
                    g[r][c] = bg
    elif texture == "frame_inner":
        if len(palette) >= 2:
            border, inner = palette[0], palette[1]
            for c in range(3):
                g[0][c] = border
                g[2][c] = border
            for r in range(3):
                g[r][0] = border
                g[r][2] = border
            g[1][1] = inner
        else:
            for r in range(3):
                for c in range(3):
                    g[r][c] = palette[0]
    elif texture == "blob":
        for r in range(3):
            for c in range(3):
                g[r][c] = palette[0] if rng.random() < 0.5 else (
                    palette[1] if len(palette) > 1 else palette[0])
        # Force at least one cell of a 3rd color if possible.
        if len(palette) >= 3:
            r = rng.randint(0, 2); c = rng.randint(0, 2)
            g[r][c] = palette[2]
    elif texture == "gradient":
        for r in range(3):
            for c in range(3):
                g[r][c] = palette[(r + c) % len(palette)]
    else:
        for r in range(3):
            for c in range(3):
                g[r][c] = rng.choice(palette)
    return g


def _draw_from_degenerate(name, palette, rng):
    """Edge-case where the scale-map signature is hidden.

    monochrome  — uniform input → uniform output; rule is invisible.
    row_uniform — every row a single color; output has fat horizontal bands.
    col_uniform — every column a single color; output has fat vertical bands.
    """
    g = full_grid(3, 3, palette[0])
    if name == "monochrome":
        color = rng.choice(palette)
        for r in range(3):
            for c in range(3):
                g[r][c] = color
        return g
    if name == "row_uniform":
        for r in range(3):
            color = palette[r % len(palette)]
            for c in range(3):
                g[r][c] = color
        return g
    if name == "col_uniform":
        for c in range(3):
            color = palette[c % len(palette)]
            for r in range(3):
                g[r][c] = color
        return g
    return g
