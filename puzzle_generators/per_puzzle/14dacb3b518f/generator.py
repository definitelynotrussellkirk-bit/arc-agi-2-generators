"""Generator for 17_bundle:m115 — recolor by hole count.

Rule: each blob with ≥1 enclosed hole → 8; solid blobs → 2.

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: all_solid (no hollow blobs → rule recolors everything to
2, no hole/solid contrast), all_hollow (no solid blobs → rule
recolors everything to 8, no contrast), single_blob (only one blob →
no hollow/solid contrast in output).
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "14dacb3b518f"
VERSION = "1.1.0"
TASK_ID = "14dacb3b518f"
SUMMARY = "1 hollow rect-frame + 1 solid blob, both color 6."

INVARIANTS = [
    "background is 0",
    "≥1 hollow rect-frame in color 6",
    "≥1 solid blob in color 6 (no hole)",
    "blobs don't 4-touch",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("all_solid", "all_hollow", "single_blob")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 9..11", "valid": "8..14"},
    "grid_w":         {"type": "int", "default": "rng 11..13", "valid": "9..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "palette_size":   {"type": "int", "default": "1", "valid": "1..1"},
    "position_bias":  {"type": "str", "default": "hollow_plus_solid",
                       "valid": "hollow_plus_solid"},
    "n_distinct_colors": {"type": "int", "default": "1", "valid": "1..1"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def _free(g, r1, c1, r2, c2):
    h, w = len(g), len(g[0])
    if r1 < 0 or c1 < 0 or r2 >= h or c2 >= w:
        return False
    for r in range(max(0, r1 - 1), min(h, r2 + 2)):
        for c in range(max(0, c1 - 1), min(w, c2 + 2)):
            if g[r][c] != 0:
                return False
    return True


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 9, 9)
        w = ctx.draw_int("grid_w", 11, 11)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 11, 14)
        w = ctx.draw_int("grid_w", 13, 16)
    else:
        h = ctx.draw_int("grid_h", 9, 11)
        w = ctx.draw_int("grid_w", 11, 13)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    color = 6
    for _ in range(40):
        fh = rng.randint(3, 4); fw = rng.randint(3, 4)
        r1 = rng.randint(0, h - fh)
        c1 = rng.randint(0, w - fw)
        r2 = r1 + fh - 1; c2 = c1 + fw - 1
        if _free(g, r1, c1, r2, c2):
            for c in range(c1, c2 + 1):
                g[r1][c] = color; g[r2][c] = color
            for r in range(r1, r2 + 1):
                g[r][c1] = color; g[r][c2] = color
            break
    used = {(r, c) for r in range(h) for c in range(w) if g[r][c] != 0}
    for _ in range(40):
        r1 = rng.randint(0, h - 2)
        c1 = rng.randint(0, w - 2)
        cells = {(r1, c1), (r1, c1 + 1), (r1 + 1, c1), (r1 + 1, c1 + 1)}
        if cells & used: continue
        ok = True
        for r, c in cells:
            for dr, dc in ((-1, 0), (1, 0), (0, -1), (0, 1)):
                nr, nc = r + dr, c + dc
                if 0 <= nr < h and 0 <= nc < w and (nr, nc) not in cells and g[nr][nc] != 0:
                    ok = False; break
            if not ok: break
        if not ok: continue
        for r, c in cells:
            g[r][c] = color
        break
    return g


def _draw_from_degenerate(name, rng):
    h, w = 10, 12
    g = full_grid(h, w, 0)
    if name == "all_solid":
        # No hollow blobs — rule recolors everything to 2; no
        # hole/solid contrast.
        for r, c in [(2, 2), (2, 3), (3, 2), (3, 3)]: g[r][c] = 6
        for r, c in [(6, 7), (6, 8), (7, 7), (7, 8)]: g[r][c] = 6
        return g
    if name == "all_hollow":
        # No solid blobs — rule recolors everything to 8; no
        # contrast across blob types.
        for c in range(1, 5): g[1][c] = 6; g[4][c] = 6
        for r in range(1, 5): g[r][1] = 6; g[r][4] = 6
        for c in range(7, 11): g[5][c] = 6; g[8][c] = 6
        for r in range(5, 9): g[r][7] = 6; g[r][10] = 6
        return g
    if name == "single_blob":
        # Only one blob — no hollow/solid contrast.
        for c in range(3, 8): g[3][c] = 6; g[6][c] = 6
        for r in range(3, 7): g[r][3] = 6; g[r][7] = 6
        return g
    return g
