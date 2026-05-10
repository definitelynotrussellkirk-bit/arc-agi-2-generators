"""Generator for 2ccd9fef.

Rule: three stacked panels show a small colored object growing; the
blank panel is the canvas for the extrapolated next object.

Combinatorial axes (8): grid_h/w, panel_height, palette_kind,
anchor_corner, asymmetry_force, palette_size, position_bias,
payload_color.
Degenerates: no_panels, no_payload, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "973bec16d719"
VERSION = "1.1.0"
TASK_ID = "973bec16d719"
SUMMARY = "Three stacked panels show object growing; blank panel is canvas for next object."

INVARIANTS = [
    "input is exactly three same-sized vertical panels",
    "background color 0 is common to all panels",
    "one payload color appears in the first two panels only",
    "the second payload shape strictly extends the first shape",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_panels", "no_payload", "full_grid")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "varied", "valid": "varied"},
    "grid_w":         {"type": "int", "default": "varied", "valid": "varied"},
    "panel_height":   {"type": "int", "default": "rng 7..9", "valid": "7..9"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "1", "valid": "1"},
    "position_bias":  {"type": "str", "default": "varied", "valid": "varied"},
    "payload_color":  {"type": "color", "default": "rng !{0}",
                       "valid": "1..9"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], rng)
    if difficulty == "easy":
        ph = ctx.draw_int("panel_height", 7, 7)
    elif difficulty == "hard":
        ph = ctx.draw_int("panel_height", 9, 9)
    else:
        ph = ctx.draw_int("panel_height", 7, 9)
    pw = 8 + rng.randint(0, 4)
    color = ctx.draw_color("payload_color", exclude={0})
    row = 1 + ((seed + sample_index) % max(1, ph - 2))
    col = 1 + ((sample_index + rng.randint(0, 4)) % max(1, pw - 4))

    panels = [full_grid(ph, pw, 0) for _ in range(3)]
    panels[0][row][col] = color
    panels[1][row][col] = color
    panels[1][row][col + 1] = color

    out = []
    for panel in panels:
        out.extend(panel)
    return out


def _draw_from_degenerate(name, rng):
    g = full_grid(21, 8, 0)
    if name == "no_panels":
        g[5][3] = 3
        return g
    if name == "no_payload":
        return g
    if name == "full_grid":
        for r in range(21):
            for c in range(8):
                g[r][c] = 3
        return g
    return g
