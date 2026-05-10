"""Generator for puzzle 0becf7df.

Rule: top-left 2 × 2 = (ka, kb, kc, kd). For each cell outside the
top-left 2 × 2: ka↔kb, kc↔kd; other colors unchanged.

Combinatorial axes (8): grid_h/w, key_palette (ka, kb, kc, kd),
body_pattern (random/blob/scatter/grid), body_density,
key_color_distribution, swap_visibility (ensure ≥1 cell of each key
color exists in body so swap is visible), include_zero_in_body.
Degenerates: keys_all_same, no_swap_targets, body_uses_only_keys.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, paint_at

GENERATOR_ID = "fb1897956172"
VERSION = "1.1.0"
TASK_ID = "fb1897956172"
SUMMARY = "Top-left 2 × 2 holds 4 keys; rule swaps (ka↔kb, kc↔kd) elsewhere."

INVARIANTS = [
    "top-left 2 × 2 has 4 distinct non-zero colors (ka, kb, kc, kd)",
    "≥1 cell outside top-left has color in {ka, kb, kc, kd} (so swap is visible)",
]

BODY_PATTERNS = ("random", "blob", "scatter", "grid", "stripes", "border")
DEGENERATE_TEXTURES = ("keys_all_same", "no_swap_targets", "body_uses_non_keys")
HELPFUL_TEXTURES = BODY_PATTERNS

AXES = {
    "grid_h":              {"type": "int", "default": "rng 8..14", "valid": "5..18"},
    "grid_w":              {"type": "int", "default": "rng 8..14", "valid": "5..18"},
    "ka_color":            {"type": "color", "default": "rng (≠0)", "valid": "1..9"},
    "kb_color":            {"type": "color", "default": "rng (≠0,ka)", "valid": "1..9"},
    "kc_color":            {"type": "color", "default": "rng (≠0,ka,kb)", "valid": "1..9"},
    "kd_color":            {"type": "color", "default": "rng (≠0,others)", "valid": "1..9"},
    "body_pattern":        {"type": "str", "default": "rng helpful",
                            "valid": "|".join(BODY_PATTERNS)},
    "body_density":        {"type": "float", "default": "rng 0.2..0.5", "valid": "0..1"},
    "include_zero_in_body": {"type": "bool", "default": "rng", "valid": "true|false"},
    "texture":             {"type": "str", "default": "alias for body_pattern",
                            "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if difficulty == "easy":
        h_lo, h_hi = 8, 10
    elif difficulty == "hard":
        h_lo, h_hi = 13, 14
    else:
        h_lo, h_hi = 8, 14
    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", h_lo, h_hi)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], h, w, rng)
    keys = []
    excluded = {0}
    for kn in ("ka_color", "kb_color", "kc_color", "kd_color"):
        c = int(overrides.get(kn, ctx.draw_color(kn, exclude=excluded)))
        keys.append(c)
        excluded.add(c)
    ka, kb, kc, kd = keys
    pattern = (overrides.get("texture") or overrides.get("body_pattern")
               or ctx.draw_choice("body_pattern", list(BODY_PATTERNS)))
    density = float(overrides.get("body_density",
                                  ctx.draw_rng("body_density").uniform(0.2, 0.5)))
    inc_zero = bool(overrides.get("include_zero_in_body",
                                  ctx.draw_choice("include_zero_in_body", [True, False])))
    g = full_grid(h, w, 0)
    g[0][0] = ka; g[0][1] = kb; g[1][0] = kc; g[1][1] = kd
    body_palette = list(keys)
    if inc_zero:
        body_palette.append(0)
    _fill_body(g, pattern, density, body_palette, rng)
    if not any(g[r][c] in keys for r in range(h) for c in range(w)
               if not (r <= 1 and c <= 1)):
        g[2][2] = ka
    return g


def _fill_body(g, pattern, density, palette, rng):
    h = len(g); w = len(g[0])
    for r in range(h):
        for c in range(w):
            if r <= 1 and c <= 1:
                continue
            if pattern == "random":
                if rng.random() < density:
                    g[r][c] = rng.choice(palette)
            elif pattern == "blob":
                pass  # handled below
            elif pattern == "scatter":
                if (r + c) % 2 == 0 and rng.random() < density * 1.5:
                    g[r][c] = rng.choice(palette)
            elif pattern == "grid":
                if r % 2 == 0 and c % 2 == 0:
                    g[r][c] = rng.choice(palette)
            elif pattern == "stripes":
                if r % 2 == 0 and rng.random() < density:
                    g[r][c] = rng.choice(palette)
            elif pattern == "border":
                if r in (0, h - 1) or c in (0, w - 1):
                    if not (r <= 1 and c <= 1):
                        g[r][c] = rng.choice(palette)
    if pattern == "blob":
        bh = max(1, int(h * density)); bw = max(1, int(w * density))
        r0 = rng.randint(2, h - bh); c0 = rng.randint(2, w - bw)
        color = rng.choice(palette)
        for r in range(r0, r0 + bh):
            for c in range(c0, c0 + bw):
                g[r][c] = color


def _draw_from_degenerate(name, h, w, rng):
    g = full_grid(h, w, 0)
    palette = list(range(1, 10)); rng.shuffle(palette)
    if name == "keys_all_same":
        c0 = palette[0]
        g[0][0] = c0; g[0][1] = c0; g[1][0] = c0; g[1][1] = c0
        for r in range(2, h):
            for c in range(2, w):
                if rng.random() < 0.3:
                    g[r][c] = rng.choice(palette[1:5])
        return g
    if name == "no_swap_targets":
        # Body uses only colors NOT in {ka, kb, kc, kd}.
        keys = palette[:4]
        body = palette[4:8]
        g[0][0] = keys[0]; g[0][1] = keys[1]; g[1][0] = keys[2]; g[1][1] = keys[3]
        for r in range(h):
            for c in range(w):
                if r <= 1 and c <= 1: continue
                if rng.random() < 0.4:
                    g[r][c] = rng.choice(body)
        return g
    if name == "body_uses_non_keys":
        keys = palette[:4]
        non_keys = palette[4:8]
        g[0][0] = keys[0]; g[0][1] = keys[1]; g[1][0] = keys[2]; g[1][1] = keys[3]
        for r in range(h):
            for c in range(w):
                if r <= 1 and c <= 1: continue
                if rng.random() < 0.4:
                    g[r][c] = rng.choice(non_keys)
        return g
    return g
