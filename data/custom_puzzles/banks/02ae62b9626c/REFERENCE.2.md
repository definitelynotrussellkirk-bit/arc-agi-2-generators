# New Primitive for Set 14 — `legend_compose`

## Signature

```text
legend_compose(row_keys, col_keys, resolver)
```

## Purpose

Compose outputs from two short symbolic legends: one legend indexed by rows and one indexed by columns.

Many ARC-style tasks use a tiny header row and header column as a compact program. The interior is not described cell by cell; instead, each location is determined by a pair of legend values. `legend_compose` makes that structure explicit.

## Arguments

- `row_keys`: the ordered legend values that govern rows
- `col_keys`: the ordered legend values that govern columns
- `resolver`: a function that takes `(row_key, col_key)` and returns the value or tile that should be placed for that pair

## Semantics

At its simplest, `legend_compose` builds a matrix whose `(i, j)` entry is:

```text
resolver(row_keys[i], col_keys[j])
```

The resolver can return:

- a single color value for a one-cell matrix,
- a small tile for an expanded mosaic,
- or a transformed motif selected by the row/column pair.

That makes the helper useful for both flat row-by-column lookups and larger compositional tasks.

## Why this helper matters

Without an explicit helper, header-driven ARC rules often collapse into awkward nested loops that obscure the real idea. `legend_compose` keeps the solver focused on the conceptual move:

1. read the row legend,
2. read the column legend,
3. decide what each pair means,
4. assemble the interior from those pairwise decisions.

It is especially well suited to staged solving because the model can first identify the legend values, then identify the resolver, and only then expand to the full output.

## Direct uses in this pack

- **E92** — interior cell is the matching legend color when the row and column legends agree
- **M92** — each legend pair expands into a 2×2 weave tile
- **H92** — one legend chooses a transform and the other chooses a motif, producing a tiled transformed-motif mosaic
