"""Generator for puzzle 281123b4.

Rule: input is 4 × 19 = 4 sections of 4 cols each, separated by 1-col
dividers (cols 4, 9, 14, value 3). Output is 4 × 4: for each cell pick
first non-zero from sections in priority order [2, 3, 0, 1].
(Section indices: 0 left, 3 right.)

Combinatorial axes (8):
  * grid_h               — h (canonical 4)
  * section colors (4)   — colors for sections 0, 1, 2, 3 (each distinct)
  * sec_density_*        — per-section density of fg cells
  * section_pattern      — random / blob / stripes / diagonal / border
  * priority_overlap     — how much sections overlap on the same cell positions
  * divider_color        — color of the divider columns (canonical: 3)
  * caller-opt-in degenerates: only_section_0, only_section_3,
                              all_sections_overlap.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "9000d0ea6484"
VERSION = "1.1.0"
TASK_ID = "9000d0ea6484"
SUMMARY = "Fixed-shape 4-section grid; rule outputs 4×4 priority-OR (priority [2,3,0,1])."

INVARIANTS = [
    "grid is h × 19 (4 sections × 4 cols + 3 dividers)",
    "cols 4, 9, 14 are dividers (color 3)",
    "≥1 cell non-zero in each priority-relevant section",
]

SECTION_PATTERNS = ("random", "blob", "stripes", "diagonal", "border", "scatter")
DEGENERATE_TEXTURES = ("only_section_0", "only_section_3", "all_sections_overlap")
HELPFUL_TEXTURES = SECTION_PATTERNS

AXES = {
    "grid_h":           {"type": "int", "default": "rng 4..14", "valid": "1..18"},
    "sec0_color":       {"type": "color", "default": "rng (≠0,3)", "valid": "1..9"},
    "sec1_color":       {"type": "color", "default": "rng (≠0,3,sec0)", "valid": "1..9"},
    "sec2_color":       {"type": "color", "default": "rng (≠0,3,sec0,sec1)", "valid": "1..9"},
    "sec3_color":       {"type": "color", "default": "rng (≠0,3,others)", "valid": "1..9"},
    "section_pattern":  {"type": "str", "default": "rng helpful",
                         "valid": "|".join(SECTION_PATTERNS)},
    "section_density":  {"type": "float", "default": "rng 0.3..0.6", "valid": "0..1"},
    "priority_overlap": {"type": "float", "default": "rng 0..0.4", "valid": "0..1"},
    "texture":          {"type": "str", "default": "alias for section_pattern",
                         "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if difficulty == "easy":
        h_lo, h_hi = 4, 6
    elif difficulty == "hard":
        h_lo, h_hi = 11, 14
    else:
        h_lo, h_hi = 4, 14
    h = ctx.draw_int("grid_h", h_lo, h_hi)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], h, rng)
    sec_colors = []
    excluded = {0, 3}
    for i in range(4):
        c = int(overrides.get(f"sec{i}_color",
                              ctx.draw_color(f"sec{i}_color", exclude=excluded)))
        sec_colors.append(c)
        excluded.add(c)
    pattern = (overrides.get("texture") or overrides.get("section_pattern")
               or ctx.draw_choice("section_pattern", list(SECTION_PATTERNS)))
    density = float(overrides.get("section_density",
                                  ctx.draw_rng("section_density").uniform(0.3, 0.6)))
    overlap = float(overrides.get("priority_overlap",
                                  ctx.draw_rng("priority_overlap").uniform(0.0, 0.4)))
    g = full_grid(h, 19, 0)
    for r in range(h):
        g[r][4] = 3; g[r][9] = 3; g[r][14] = 3
    sec_starts = [0, 5, 10, 15]
    for si in range(4):
        _fill_section(g, sec_starts[si], h, pattern, density, sec_colors[si], rng)
    # Priority overlap: sometimes paint cells in lower-priority sections
    # at positions where higher-priority sections also have content.
    if overlap > 0:
        priority_order = [2, 3, 0, 1]  # rule's priority
        for r in range(h):
            for c_off in range(4):
                # Find the highest-priority section painting (r, c_off)
                hits = [si for si in priority_order
                        if g[r][sec_starts[si] + c_off] != 0]
                if hits and rng.random() < overlap:
                    # Add a paint to the next-lower priority section too
                    for si in priority_order:
                        if si not in hits and rng.random() < 0.5:
                            g[r][sec_starts[si] + c_off] = sec_colors[si]
                            break
    return g


def _fill_section(g, c0, h, pattern, density, color, rng):
    if pattern == "random":
        for r in range(h):
            for c in range(c0, c0 + 4):
                if rng.random() < density:
                    g[r][c] = color
    elif pattern == "blob":
        bh = max(1, int(h * density)); bw = max(1, int(4 * density))
        rr = rng.randint(0, h - bh); cc = rng.randint(c0, c0 + 4 - bw)
        for r in range(rr, rr + bh):
            for c in range(cc, cc + bw):
                g[r][c] = color
    elif pattern == "stripes":
        for r in range(h):
            if r % 2 == 0:
                for c in range(c0, c0 + 4):
                    g[r][c] = color
    elif pattern == "diagonal":
        for k in range(min(h, 4)):
            g[k][c0 + k] = color
    elif pattern == "border":
        for c in range(c0, c0 + 4):
            g[0][c] = color; g[h - 1][c] = color
        for r in range(h):
            g[r][c0] = color; g[r][c0 + 3] = color
    elif pattern == "scatter":
        for r in range(h):
            for c in range(c0, c0 + 4):
                if (r + c) % 2 == 0 and rng.random() < density * 1.5:
                    g[r][c] = color


def _draw_from_degenerate(name, h, rng):
    g = full_grid(h, 19, 0)
    for r in range(h):
        g[r][4] = 3; g[r][9] = 3; g[r][14] = 3
    palette = list(range(1, 10))
    rng.shuffle(palette)
    palette = [c for c in palette if c != 3][:4]
    if name == "only_section_0":
        for r in range(h):
            for c in range(4):
                if rng.random() < 0.5:
                    g[r][c] = palette[0]
        return g
    if name == "only_section_3":
        for r in range(h):
            for c in range(15, 19):
                if rng.random() < 0.5:
                    g[r][c] = palette[3]
        return g
    if name == "all_sections_overlap":
        # Every section has every cell filled — output is purely priority winner.
        for si, c0 in enumerate([0, 5, 10, 15]):
            for r in range(h):
                for c in range(c0, c0 + 4):
                    g[r][c] = palette[si]
        return g
    return g
