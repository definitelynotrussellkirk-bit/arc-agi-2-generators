"""Generator for arc_additional_puzzles_21_set12_bundle:H78 — zone commands transform and pack.

Rule: row 0 holds N commands (each non-zero cell = transform code 1..4) at distinct
columns. Below row 0 there are N components; each is associated with the nearest top-row
command (by horizontal-center distance). Apply that command's transform to the cropped
component, sort transforms by (cell_count desc, min_color asc), and pack the
transformed crops left-to-right starting at row 1, col 0 with one blank column
between them. Output is same size as input.

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: no_commands (row 0 empty → rule has no transforms);
no_objects (commands but no body components → rule has nothing to
transform); identity_commands (all command codes = identity → output
== input shape order).
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "2827181c35c3"
VERSION = "1.1.0"
TASK_ID = "2827181c35c3"

SUMMARY = "Top-row N commands; N components below; each transformed by nearest command, packed."

INVARIANTS = [
    "background is 0",
    "row 0 has 2-3 non-zero cells (transform codes 1..4) at distinct columns",
    "below row 0, exactly that many isolated 4-connected components in distinct colors",
    "components are placed in horizontal zones near their assigned command",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_commands", "no_objects", "identity_commands")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":            {"type": "int", "default": "rng 11..13", "valid": "10..16"},
    "grid_w":            {"type": "int", "default": "rng 14..18", "valid": "12..20"},
    "n_objs":            {"type": "int", "default": "rng 2..3", "valid": "2..3"},
    "palette_kind":      {"type": "str", "default": "rng helpful",
                          "valid": "|".join(PALETTE_KINDS)},
    "palette_size":      {"type": "int", "default": "rng 3..4", "valid": "3..5"},
    "position_bias":     {"type": "str", "default": "row0_commands_with_zoned_objects",
                          "valid": "row0_commands_with_zoned_objects"},
    "n_distinct_colors": {"type": "int", "default": "rng 3..4", "valid": "3..5"},
    "density":           {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":           {"type": "str", "default": "alias for palette_kind",
                          "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


_SHAPES = [
    [(0, 0), (0, 1), (1, 0)],
    [(0, 0), (1, 0), (1, 1), (2, 1)],
    [(0, 0), (0, 1), (0, 2), (1, 1)],
    [(0, 0), (1, 0), (1, 1), (2, 0)],
    [(0, 0), (0, 1), (0, 2), (1, 0)],
]


def _free(g, r1, c1, r2, c2):
    h, w = len(g), len(g[0])
    if r1 < 0 or c1 < 0 or r2 >= h or c2 >= w: return False
    for r in range(max(0, r1 - 1), min(h, r2 + 2)):
        for c in range(max(0, c1 - 1), min(w, c2 + 2)):
            if g[r][c] != 0: return False
    return True


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 11, 12)
        w = ctx.draw_int("grid_w", 14, 15)
        n_objs = ctx.draw_int("n_objs", 2, 2)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 12, 13)
        w = ctx.draw_int("grid_w", 16, 18)
        n_objs = ctx.draw_int("n_objs", 3, 3)
    else:
        h = ctx.draw_int("grid_h", 11, 13)
        w = ctx.draw_int("grid_w", 14, 18)
        n_objs = ctx.draw_int("n_objs", 2, 3)
    rng = ctx.draw_rng("layout")

    for outer in range(40):
        g = full_grid(h, w, 0)
        zone_w = w // n_objs
        cmd_cols = []
        for i in range(n_objs):
            cstart = i * zone_w
            cend = (i + 1) * zone_w - 1 if i < n_objs - 1 else w - 1
            cmd_cols.append(rng.randint(cstart, min(cend, w - 1)))
        codes = [rng.randint(1, 4) for _ in range(n_objs)]
        for cc, code in zip(cmd_cols, codes):
            g[0][cc] = code

        colors = rng.sample([2, 3, 4, 5, 6, 7, 8, 9], n_objs)
        ok = True
        for i in range(n_objs):
            cstart = i * zone_w
            cend = (i + 1) * zone_w - 1 if i < n_objs - 1 else w - 1
            placed = False
            for _ in range(60):
                shape = rng.choice(_SHAPES)
                sh = max(r for r, _ in shape) + 1
                sw = max(c for _, c in shape) + 1
                r0 = rng.randint(2, h - sh)
                c0 = rng.randint(cstart, max(cstart, cend - sw + 1))
                if c0 + sw - 1 > cend: continue
                if not _free(g, r0, c0, r0 + sh - 1, c0 + sw - 1): continue
                for dr, dc in shape:
                    g[r0 + dr][c0 + dc] = colors[i]
                placed = True
                break
            if not placed:
                ok = False
                break
        if ok:
            return g
    raise ValueError("could not realize zone-commands layout in 40 attempts")


def _draw_from_degenerate(name, rng):
    h, w = 12, 16
    g = full_grid(h, w, 0)
    if name == "no_commands":
        # Row 0 empty — rule has no transforms.
        for dr, dc in [(0, 0), (0, 1), (1, 0)]:
            g[3 + dr][3 + dc] = 4
        for dr, dc in [(0, 0), (1, 0), (1, 1)]:
            g[3 + dr][11 + dc] = 5
        return g
    if name == "no_objects":
        # Commands but no objects.
        g[0][3] = 1; g[0][11] = 2
        return g
    if name == "identity_commands":
        # All command codes = 1 (identity) — output unchanged.
        g[0][3] = 1; g[0][11] = 1
        for dr, dc in [(0, 0), (0, 1), (1, 0)]:
            g[3 + dr][3 + dc] = 4
        for dr, dc in [(0, 0), (1, 0), (1, 1)]:
            g[3 + dr][11 + dc] = 5
        return g
    return g
