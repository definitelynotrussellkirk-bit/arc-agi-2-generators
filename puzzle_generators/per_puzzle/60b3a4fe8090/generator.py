"""Generator for arc_additional_puzzles_21_set19_bundle:H127 — commanded room slides.

Rule: 9-walls divide a 13×13 board into four 5×5 rooms. Each room's top-left
cell is a command (1=up, 2=right, 3=down, 4=left). Slide that room's colored
object as far as possible in the commanded direction (within the room, walls
included). Walls and slid object preserved; command marker is removed.

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: no_walls (no 9-walls → rule cannot identify rooms);
no_commands (rooms present but no command markers → rule has no
direction); no_objects (rooms + commands but no colored objects to
slide → rule has nothing to move).
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "60b3a4fe8090"
VERSION = "1.1.0"
TASK_ID = "60b3a4fe8090"

SUMMARY = "13×13 board, 4 rooms walled by 9; each room has a command + colored object."

INVARIANTS = [
    "background is 0",
    "9-walls form a 2x2 chamber layout (outer 13x13 frame + horizontal divider at row 6 + vertical divider at col 6)",
    "each room's top-left cell holds a command (1, 2, 3, or 4)",
    "each room has a small connected colored object (3-4 cells) in a non-{0, 9, 1..4} color",
    "object is at least 1 cell from the room's TL command and from walls",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_walls", "no_commands", "no_objects")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "command":           {"type": "int", "default": "rng 1..4 per room", "valid": "1..4"},
    "object_size":       {"type": "int", "default": "rng 2..4 per room", "valid": "2..4"},
    "object_color":      {"type": "color-set", "default": "permutation of 5..8", "valid": "5..8"},
    "palette_kind":      {"type": "str", "default": "rng helpful",
                          "valid": "|".join(PALETTE_KINDS)},
    "palette_size":      {"type": "int", "default": "rng 8..8", "valid": "8..8"},
    "position_bias":     {"type": "str", "default": "four_walled_rooms_with_commands",
                          "valid": "four_walled_rooms_with_commands"},
    "n_distinct_colors": {"type": "int", "default": "rng 8..8", "valid": "8..8"},
    "density":           {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":           {"type": "str", "default": "alias for palette_kind",
                          "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    rng = ctx.draw_rng("layout")
    g = full_grid(13, 13, 0)
    for c in range(13):
        g[0][c] = 9
        g[6][c] = 9
        g[12][c] = 9
    for r in range(13):
        g[r][0] = 9
        g[r][6] = 9
        g[r][12] = 9
    rooms = [(0, 0), (0, 6), (6, 0), (6, 6)]
    avail_colors = [5, 6, 7, 8]
    rng.shuffle(avail_colors)
    for i, (r0, c0) in enumerate(rooms):
        cmd = rng.randint(1, 4)
        g[r0 + 1][c0 + 1] = cmd
        color = avail_colors[i]
        cells = [(r, c) for r in range(r0 + 1, r0 + 6) for c in range(c0 + 1, c0 + 6) if (r, c) != (r0 + 1, c0 + 1)]
        for _ in range(60):
            start = rng.choice(cells)
            built = [start]
            seen = {start}
            target_size = rng.randint(2, 4)
            while len(built) < target_size:
                r, c = rng.choice(built)
                dr, dc = rng.choice([(-1, 0), (1, 0), (0, -1), (0, 1)])
                nr, nc = r + dr, c + dc
                if (nr, nc) in cells and (nr, nc) not in seen:
                    built.append((nr, nc))
                    seen.add((nr, nc))
                else:
                    break
            if len(built) >= 2:
                for r, c in built:
                    g[r][c] = color
                break
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(13, 13, 0)
    if name == "no_walls":
        # No 9-walls — rule cannot identify rooms.
        g[1][1] = 1; g[2][2] = 5; g[2][3] = 5
        g[1][8] = 2; g[3][9] = 6; g[3][10] = 6
        return g
    if name == "no_commands":
        # Walls present but no command markers.
        for c in range(13):
            g[0][c] = 9; g[6][c] = 9; g[12][c] = 9
        for r in range(13):
            g[r][0] = 9; g[r][6] = 9; g[r][12] = 9
        g[2][2] = 5; g[2][3] = 5
        g[2][9] = 6; g[3][9] = 6
        g[8][2] = 7; g[8][3] = 7
        g[8][9] = 8; g[9][9] = 8
        return g
    if name == "no_objects":
        # Walls + commands but no objects to slide.
        for c in range(13):
            g[0][c] = 9; g[6][c] = 9; g[12][c] = 9
        for r in range(13):
            g[r][0] = 9; g[r][6] = 9; g[r][12] = 9
        g[1][1] = 1; g[1][7] = 2; g[7][1] = 3; g[7][7] = 4
        return g
    return g
