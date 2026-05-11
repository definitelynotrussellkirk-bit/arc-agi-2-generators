# New Primitive for Set 19: `slide_until_contact`

## Overview

This set introduces a reusable rigid-motion helper:

```text
slide_until_contact(board, cells, direction)
```

The primitive takes a grid, a set of occupied cells belonging to one moving object, and a direction vector such as `(0, 1)` for “move right”.
It translates the whole object step by step until the **next** step would collide with:

- the boundary of the board,
- any nonzero blocker not part of the moving object, or
- a wall structure that should remain fixed.

The result is the translated set of object cells at its final resting place.

## Why this is useful

ARC tasks often hide a very common subproblem:

1. identify the object that is allowed to move,
2. treat all other nonzero cells as blockers,
3. move the object rigidly in one direction,
4. stop exactly one cell before collision.

Without a helper, every solver has to rewrite the same loop for rigid translation, collision testing, and stopping logic.

`slide_until_contact` compresses that pattern into one operation.

## Suggested signature

```python
slide_until_contact(board, cells, direction)
```

Where:

- `board` is the current grid
- `cells` is the set of coordinates occupied by the moving object
- `direction` is a `(dr, dc)` pair such as `(-1, 0)`, `(0, 1)`, `(1, 0)`, or `(0, -1)`

## Semantics

Suppose the board contains a vertical dock of `9`s and an `L`-shaped object of `4`s:

```text
000000090
040000090
040000090
044000090
000000090
```

Sliding the object right with `direction = (0, 1)` yields:

```text
000000090
000004090
000004090
000004490
000000090
```

because one more step to the right would collide with the dock.

## Direct uses in this pack

- **E127 — Slide to Dock**  
  One object slides right until it reaches a fixed dock stripe.

- **M127 — Lane Docking**  
  Several lane-separated objects each slide right until the wall stops them.

- **H127 — Commanded Room Slides**  
  Four separate rooms each contain a command digit that determines the slide direction for the local object.

## Minimal reference implementation

```python
def slide_until_contact(board, cells, direction):
    dr, dc = direction
    current = set(cells)
    h = len(board)
    w = len(board[0])

    while True:
        blocked = False
        for r, c in current:
            nr, nc = r + dr, c + dc
            if not (0 <= nr < h and 0 <= nc < w):
                blocked = True
                break
            if board[nr][nc] != 0 and (nr, nc) not in current:
                blocked = True
                break
        if blocked:
            return current
        current = {(r + dr, c + dc) for r, c in current}
```

## What makes it new relative to recent helpers

Recent helpers in the series have emphasized masking, routing, packing, legend composition, or chamber ownership.
`slide_until_contact` is different because it focuses on **rigid motion under collision constraints**.
It is especially useful in staged-solving systems, because a model can first identify *what* should move, then repair only the stopping rule if the final position is off by a few cells.
