"""Generator for ARC task b1948b0a.

Rule: `(rule! (lambda (g) (recolor-map* g {6 2})))`
  Replace every magenta(6) cell with red(2). Other colors unchanged.

Combinatorial axes:
  * grid_h / grid_w     — outer canvas size
  * texture             — pattern type that holds the 6-cells (and others)
  * fg_density_6        — fraction of fg cells that are 6 (the rule's target)
  * distractor_palette  — which other colors live alongside the 6s
  * bg_color            — usually 0; can be any non-6 color
  * placement_pattern   — how 6-cells are clustered: scattered/blob/line/border
  * noise_overlay       — perturb a few cells (must not introduce new 6s)
  * caller-opt-in degenerates: solid_6, no_6 (rule no-op), single_6
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "00d3fcfaf257"
VERSION = "1.1.0"  # bumped: deeper combinatorial axes added
TASK_ID = "00d3fcfaf257"
SUMMARY = "Random grid containing magenta(6) cells alongside distractors; the rule recolors 6→2."

INVARIANTS = [
    "input contains at least one magenta(6) cell (rule has visible effect)",
    "input may contain distractors of other colors that stay unchanged",
    "background can be any non-6 color (default 0)",
]

HELPFUL_TEXTURES = (
    "scattered", "blob", "line_h", "line_v", "border",
    "rect", "L_shape", "checker_subgrid", "diagonal",
)
DEGENERATE_TEXTURES = ("solid_6", "no_6", "single_6")

AXES = {
    "grid_h":             {"type": "int",   "default": "rng 4..14", "valid": "3..18"},
    "grid_w":             {"type": "int",   "default": "rng 4..14", "valid": "3..18"},
    "texture":            {"type": "str",   "default": "rng helpful",
                           "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
    "fg_density_6":       {"type": "float", "default": "rng 0.10..0.45", "valid": "0.05..0.9"},
    "distractor_count":   {"type": "int",   "default": "rng 1..4",  "valid": "0..6"},
    "bg_color":           {"type": "color", "default": "0",         "valid": "0..9 (≠6)"},
    "placement_pattern":  {"type": "str",   "default": "alias for texture",
                           "valid": "|".join(HELPFUL_TEXTURES)},
    "noise_overlay":      {"type": "float", "default": "rng 0..0.05", "valid": "0..0.3"},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)

    if difficulty == "easy":
        h_lo, h_hi, d_lo, d_hi = 4, 7, 1, 2
    elif difficulty == "hard":
        h_lo, h_hi, d_lo, d_hi = 11, 14, 3, 4
    else:
        h_lo, h_hi, d_lo, d_hi = 4, 14, 1, 4

    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", h_lo, h_hi)
    rng = ctx.draw_rng("layout")

    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], h, w, rng)

    bg = int(overrides.get("bg_color", 0))
    if bg == 6:
        bg = 0  # never let bg collide with the target color
    n_dist = int(overrides.get("distractor_count",
                               ctx.draw_int("distractor_count", d_lo, d_hi)))
    distractor_palette = [c for c in range(10) if c not in {bg, 6}]
    rng.shuffle(distractor_palette)
    distractors = distractor_palette[:max(0, n_dist)]

    texture = overrides.get(
        "texture",
        ctx.draw_choice("texture", list(HELPFUL_TEXTURES)))
    density_6 = float(overrides.get(
        "fg_density_6",
        ctx.draw_rng("fg_density_6").uniform(0.10, 0.45)))

    g = _paint_with_texture(texture, h, w, bg, distractors, density_6, rng)

    no = float(overrides.get(
        "noise_overlay",
        ctx.draw_rng("noise_overlay").uniform(0.0, 0.05)))
    if no > 0.0 and distractors:
        # Sprinkle distractor colors only — never introduce new 6s here.
        for _ in range(max(1, int(h * w * no))):
            r = rng.randint(0, h - 1)
            c = rng.randint(0, w - 1)
            if g[r][c] != 6:
                g[r][c] = rng.choice(distractors)

    # Invariant: at least one 6 must be present.
    if not any(g[r][c] == 6 for r in range(h) for c in range(w)):
        g[rng.randint(0, h - 1)][rng.randint(0, w - 1)] = 6
    return g


def _paint_with_texture(texture, h, w, bg, distractors, density_6, rng):
    g = full_grid(h, w, bg)

    def stamp_distractors():
        # Lay a low-density distractor base before the 6s land on top.
        if not distractors:
            return
        for r in range(h):
            for c in range(w):
                if rng.random() < 0.20:
                    g[r][c] = rng.choice(distractors)

    if texture == "scattered":
        stamp_distractors()
        for r in range(h):
            for c in range(w):
                if rng.random() < density_6:
                    g[r][c] = 6
    elif texture == "blob":
        stamp_distractors()
        bh = max(1, int(h * (0.3 + density_6 * 0.5)))
        bw = max(1, int(w * (0.3 + density_6 * 0.5)))
        r0 = rng.randint(0, h - bh)
        c0 = rng.randint(0, w - bw)
        for r in range(r0, r0 + bh):
            for c in range(c0, c0 + bw):
                g[r][c] = 6
    elif texture == "line_h":
        stamp_distractors()
        r = rng.randint(0, h - 1)
        for c in range(w):
            g[r][c] = 6
    elif texture == "line_v":
        stamp_distractors()
        c = rng.randint(0, w - 1)
        for r in range(h):
            g[r][c] = 6
    elif texture == "border":
        for c in range(w):
            g[0][c] = 6
            g[h - 1][c] = 6
        for r in range(h):
            g[r][0] = 6
            g[r][w - 1] = 6
        # interior gets distractors
        if distractors:
            for r in range(1, h - 1):
                for c in range(1, w - 1):
                    if rng.random() < 0.4:
                        g[r][c] = rng.choice(distractors)
    elif texture == "rect":
        stamp_distractors()
        rh = max(2, int(h * 0.5))
        rw = max(2, int(w * 0.5))
        rr = rng.randint(0, h - rh)
        rc = rng.randint(0, w - rw)
        for r in range(rr, rr + rh):
            for c in range(rc, rc + rw):
                g[r][c] = 6
    elif texture == "L_shape":
        stamp_distractors()
        rh = max(2, h - 1)
        rw = max(2, w - 1)
        rr = rng.randint(0, h - rh)
        rc = rng.randint(0, w - rw)
        for r in range(rr, rr + rh):
            g[r][rc] = 6
        for c in range(rc, rc + rw):
            g[rr + rh - 1][c] = 6
    elif texture == "checker_subgrid":
        stamp_distractors()
        for r in range(h):
            for c in range(w):
                if (r + c) % 2 == 0 and rng.random() < density_6 * 2:
                    g[r][c] = 6
    elif texture == "diagonal":
        stamp_distractors()
        for k in range(min(h, w)):
            g[k][k] = 6
    else:  # fall back to scattered
        stamp_distractors()
        for r in range(h):
            for c in range(w):
                if rng.random() < density_6:
                    g[r][c] = 6
    return g


def _draw_from_degenerate(name, h, w, rng):
    """Edge-case where the recolor signature is hidden.

    solid_6   — entire grid is 6, output is solid 2; could be confused
                with "fill with 2" rules.
    no_6      — zero 6s in input; rule is a no-op (output == input).
                Demonstration carries no rule signal.
    single_6  — one 6 cell only; very low signal-to-noise.
    """
    bg = 0
    g = full_grid(h, w, bg)
    if name == "solid_6":
        for r in range(h):
            for c in range(w):
                g[r][c] = 6
        return g
    if name == "no_6":
        # Random grid with everything except 6.
        palette = [c for c in range(10) if c != 6]
        for r in range(h):
            for c in range(w):
                g[r][c] = rng.choice(palette)
        return g
    if name == "single_6":
        palette = [c for c in range(10) if c not in {bg, 6}]
        for r in range(h):
            for c in range(w):
                if rng.random() < 0.4:
                    g[r][c] = rng.choice(palette)
        g[rng.randint(0, h - 1)][rng.randint(0, w - 1)] = 6
        return g
    return g
