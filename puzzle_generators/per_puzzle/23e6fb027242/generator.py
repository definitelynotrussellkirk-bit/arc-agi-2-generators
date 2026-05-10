"""Generator for 21b:hard_146 — select object by border-touch signature, scale 2x.

Rule: top row holds codes in {1, 2, 3, 4} = {top, right, bottom, left}.
Of the body components (rows 1+), find one whose bbox touches exactly
the borders named (1=row 1 top edge, 2=last col, 3=last row, 4=col 0).
Scale 2x.

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: no_codes (row 0 empty → rule has no signature);
no_objects (codes but no body components → selector has no
candidates); no_match (codes specify a signature no body component
satisfies → selector returns nothing).
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "23e6fb027242"
VERSION = "1.1.0"
TASK_ID = "23e6fb027242"

SUMMARY = "Top row codes (1-4 subset) + body shapes; one component matches the border signature."

INVARIANTS = [
    "background is 0",
    "row 0 holds 1-2 distinct codes in {1, 2, 3, 4} (border-touch signature)",
    "body (rows 1+) holds 2-3 components; exactly one's bbox touches the named borders",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_codes", "no_objects", "no_match")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":            {"type": "int", "default": "rng 8..10", "valid": "7..14"},
    "grid_w":            {"type": "int", "default": "rng 9..11", "valid": "8..14"},
    "palette_kind":      {"type": "str", "default": "rng helpful",
                          "valid": "|".join(PALETTE_KINDS)},
    "palette_size":      {"type": "int", "default": "rng 4..5", "valid": "3..6"},
    "position_bias":     {"type": "str", "default": "row0_codes_with_target_at_border",
                          "valid": "row0_codes_with_target_at_border"},
    "n_distinct_colors": {"type": "int", "default": "rng 4..5", "valid": "3..6"},
    "density":           {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":           {"type": "str", "default": "alias for palette_kind",
                          "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


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
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("grid_w", 9, 10)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 10, 11)
    else:
        h = ctx.draw_int("grid_h", 8, 10)
        w = ctx.draw_int("grid_w", 9, 11)
    rng = ctx.draw_rng("layout")
    code_set = sorted(rng.sample([1, 2, 3, 4], rng.randint(1, 2)))
    g = full_grid(h, w, 0)
    code_cols = rng.sample(range(0, w), len(code_set))
    for c, code in zip(code_cols, code_set): g[0][c] = code

    def touches_signature(r1, c1, r2, c2):
        sig = []
        if r1 == 1: sig.append(1)
        if c2 == w - 1: sig.append(2)
        if r2 == h - 1: sig.append(3)
        if c1 == 0: sig.append(4)
        return sorted(sig)
    palette = rng.sample([2, 3, 4, 5, 6, 7, 8, 9], 3)
    for outer in range(40):
        gg = [row[:] for row in g]
        sh = rng.randint(2, 4); sw = rng.randint(2, 4)
        r1_options = [1] if 1 in code_set else list(range(1, h - sh))
        c1_options = [0] if 4 in code_set else list(range(1, w - sw))
        if 3 in code_set:
            r1_options = [h - sh]
        if 2 in code_set:
            c1_options = [w - sw]
        if not r1_options or not c1_options: continue
        r0 = rng.choice(r1_options); c0 = rng.choice(c1_options)
        r2_target, c2_target = r0 + sh - 1, c0 + sw - 1
        if touches_signature(r0, c0, r2_target, c2_target) != code_set:
            continue
        if not _free(gg, r0, c0, r2_target, c2_target): continue
        for r in range(r0, r2_target + 1):
            for c in range(c0, c2_target + 1):
                gg[r][c] = palette[0]
        n_others = rng.randint(1, 2)
        ok = True
        for color in palette[1:1 + n_others]:
            placed = False
            for _ in range(60):
                osh = rng.randint(2, 3); osw = rng.randint(2, 3)
                or0 = rng.randint(2, h - osh - 2)
                oc0 = rng.randint(2, w - osw - 2)
                if or0 < 2 or oc0 < 2: continue
                or2 = or0 + osh - 1; oc2 = oc0 + osw - 1
                if touches_signature(or0, oc0, or2, oc2): continue
                if not _free(gg, or0, oc0, or2, oc2): continue
                for r in range(or0, or2 + 1):
                    for c in range(oc0, oc2 + 1):
                        gg[r][c] = color
                placed = True; break
            if not placed: ok = False; break
        if ok:
            return gg
    raise ValueError("could not lay out target with border signature")


def _draw_from_degenerate(name, rng):
    h, w = 9, 10
    g = full_grid(h, w, 0)
    if name == "no_codes":
        # Row 0 empty — rule has no signature.
        for r in range(2):
            for c in range(2):
                g[3 + r][3 + c] = 4
        for r in range(2):
            for c in range(2):
                g[6 + r][7 + c] = 5
        return g
    if name == "no_objects":
        # Codes but no body components.
        g[0][2] = 1; g[0][6] = 4
        return g
    if name == "no_match":
        # Codes specify "left+right" but no component touches both.
        g[0][2] = 4; g[0][6] = 2
        # Object touches neither left nor right.
        for r in range(2):
            for c in range(2):
                g[3 + r][3 + c] = 4
        for r in range(2):
            for c in range(2):
                g[6 + r][5 + c] = 5
        return g
    return g
