"""Generator for ARC task 0520fde7.

Rule: input is h × 7 with a separator at col 3. Output is h × 3:
left[r][c]==1 AND right[r][c]==1 → 2, else 0.

Combinatorial axes:
  * grid_h               — height
  * sep_color            — color of the separator column (≠ 0, ≠ 1)
  * left_density         — fraction of 1s in left panel
  * right_density        — fraction of 1s in right panel
  * panel_pattern        — random / blob / stripes / checker / border / diagonal
  * aligned_pairs_target — minimum aligned 1+1 pairs (output ≥ this many 2s)
  * caller-opt-in degenerates: no_aligned (output all 0),
                               all_aligned (output all 2 in 3 cols),
                               same_panels
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "79353e95283d"
VERSION = "1.1.0"
TASK_ID = "79353e95283d"
SUMMARY = "Two 3-column 0/1 panels separated by a marker; aligned 1+1 cells become 2."

INVARIANTS = [
    "input width is 7 (3 left + 1 separator + 3 right)",
    "left and right panels use 0/1",
    "≥1 aligned 1+1 cell so output has ≥1 two",
]

PANEL_PATTERNS = ("random", "blob", "stripes", "checker", "border", "diagonal")
DEGENERATE_TEXTURES = ("no_aligned", "all_aligned", "same_panels")
HELPFUL_TEXTURES = PANEL_PATTERNS

AXES = {
    "grid_h":            {"type": "int", "default": "rng 3..12", "valid": "1..18"},
    "sep_color":         {"type": "color", "default": "rng (≠0,1)", "valid": "2..9"},
    "left_density":      {"type": "float", "default": "rng 0.4..0.7", "valid": "0..1"},
    "right_density":     {"type": "float", "default": "rng 0.4..0.7", "valid": "0..1"},
    "panel_pattern":     {"type": "str", "default": "rng helpful",
                          "valid": "|".join(PANEL_PATTERNS)},
    "aligned_pairs_target": {"type": "int", "default": "rng 1..h", "valid": "1..h*3"},
    "texture":           {"type": "str", "default": "alias for panel_pattern",
                          "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)

    if difficulty == "easy":
        h_lo, h_hi = 3, 5
    elif difficulty == "hard":
        h_lo, h_hi = 9, 12
    else:
        h_lo, h_hi = 3, 12

    h = ctx.draw_int("grid_h", h_lo, h_hi)
    rng = ctx.draw_rng("panels")

    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], h, rng)

    sep = int(overrides.get("sep_color",
                            ctx.draw_color("sep_color", exclude={0, 1})))
    ld = float(overrides.get("left_density",
                             ctx.draw_rng("left_density").uniform(0.4, 0.7)))
    rd = float(overrides.get("right_density",
                             ctx.draw_rng("right_density").uniform(0.4, 0.7)))
    pattern = (overrides.get("texture")
               or overrides.get("panel_pattern")
               or ctx.draw_choice("panel_pattern", list(PANEL_PATTERNS)))

    g = full_grid(h, 7, 0)
    for r in range(h):
        g[r][3] = sep
    _fill_panel(g, 0, 3, h, pattern, ld, rng)
    _fill_panel(g, 4, 7, h, pattern, rd, rng)

    target = int(overrides.get(
        "aligned_pairs_target",
        ctx.draw_int("aligned_pairs_target", 1, max(1, h))))
    _ensure_aligned(g, h, target, rng)
    return g


def _fill_panel(g, c0, c1, h, pattern, density, rng):
    if pattern == "random":
        for r in range(h):
            for c in range(c0, c1):
                g[r][c] = 1 if rng.random() < density else 0
    elif pattern == "blob":
        bh = max(1, int(h * density))
        bw = max(1, int((c1 - c0) * density))
        r0 = rng.randint(0, h - bh)
        cc0 = rng.randint(c0, c1 - bw)
        for r in range(r0, r0 + bh):
            for c in range(cc0, cc0 + bw):
                g[r][c] = 1
    elif pattern == "stripes":
        for r in range(h):
            if r % 2 == 0:
                for c in range(c0, c1):
                    g[r][c] = 1
    elif pattern == "checker":
        for r in range(h):
            for c in range(c0, c1):
                if (r + c) % 2 == 0:
                    g[r][c] = 1
    elif pattern == "border":
        for c in range(c0, c1):
            g[0][c] = 1
            g[h - 1][c] = 1
        for r in range(h):
            g[r][c0] = 1
            g[r][c1 - 1] = 1
    elif pattern == "diagonal":
        for k in range(min(h, c1 - c0)):
            g[k][c0 + k] = 1


def _ensure_aligned(g, h, target, rng):
    have = sum(1 for r in range(h) for c in range(3)
               if g[r][c] == 1 and g[r][c + 4] == 1)
    if have >= target:
        return
    cells = [(r, c) for r in range(h) for c in range(3)]
    rng.shuffle(cells)
    for (r, c) in cells:
        if have >= target: break
        g[r][c] = 1
        g[r][c + 4] = 1
        have += 1


def _draw_from_degenerate(name, h, rng):
    """Edge-case where the AND-mask signal collapses.

    no_aligned   — no aligned 1+1 pair; output is all 0 (rule no-op).
    all_aligned  — every cell aligned 1+1; output is all 2.
    same_panels  — left and right identical; rule's AND collapses to
                    "show 1s of either panel" (visually misleading).
    """
    g = full_grid(h, 7, 0)
    sep = rng.choice([2, 3, 4, 5, 6, 7, 8, 9])
    for r in range(h):
        g[r][3] = sep
    if name == "no_aligned":
        for r in range(h):
            g[r][0] = 1; g[r][1] = 1
        return g
    if name == "all_aligned":
        for r in range(h):
            for c in range(3):
                g[r][c] = 1
                g[r][c + 4] = 1
        return g
    if name == "same_panels":
        for r in range(h):
            for c in range(3):
                v = 1 if rng.random() < 0.5 else 0
                g[r][c] = v
                g[r][c + 4] = v
        return g
    return g
