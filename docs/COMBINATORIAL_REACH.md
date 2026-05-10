# Combinatorial reach

The framework for each puzzle is two artifacts: an **explicit Racket
program** for `f: [array] → [array]`, and a **Python generator** that
emits intentionally-shaped input arrays parameterized by free axes
(`grid_h`, `palette_size`, `texture`, …). Pipe one through the other
and you get a fresh `(input, output)` pair, output computed (not
authored).

**Combinatorial reach** is how many distinct *configurations* of those
free axes the corpus can produce — i.e., how many qualitatively
different inputs the generators are willing to emit. Each
configuration produces a different example through the same
`f`; the seed dimension multiplies that further (every config × any
seed → another fresh example).

This document is the static snapshot of
`scripts/combinatorial_reach.py`. Re-run that script to refresh the
numbers.

## Headline

```
generators:                    3,889
total bounded configurations:  2.56 × 10¹¹  (255,693,762,612)
with seed budget 1,000:        2.56 × 10¹⁴  (255,693,762,612,000)
per-generator median:          48,384
generators with unbounded axes: 3,480 of 3,889
```

These numbers are a **lower bound**. The calculator only counts axes
whose `valid` field parses as an enumerable range (`A..B`) or
pipe-delimited choice (`X|Y|Z`). Free-form descriptive axes
(`valid: "varied"`, `valid: "sparse"`) contribute 1, even though they
typically have a real cardinality of 3–10.

## Top-10 generators by bounded reach

| rank | task_id | reach | axes |
|---:|---|---:|---:|
| 1 | `2f7883fbd26f` | 8.71 × 10¹⁰ | 9 |
| 2 | `29f732637b01` | 2.07 × 10¹⁰ | 9 |
| 3 | `0d6d64e90301` | 1.94 × 10¹⁰ | 7 |
| 4 | `f7c6c7bbc781` | 1.11 × 10¹⁰ | 8 |
| 5 | `09636f05e06e` | 9.72 × 10⁹ | 9 |
| 6 | `48732ebd41f9` * | 8.94 × 10⁹ | 9 |
| 7 | `c6c61bbe7a2c` | 8.74 × 10⁹ | 9 |
| 8 | `603bd7fff5df` | 4.54 × 10⁹ | 10 |
| 9 | `449ea8b9619c` | 4.35 × 10⁹ | 9 |
| 10 | `dd09ba465298` | 4.25 × 10⁹ | 10 |

`*` indicates the generator also has at least one unbounded axis, so
the true reach is strictly larger than the bounded value.

## Per-bank totals (top 10)

| bank | generators | bounded reach |
|---|---:|---:|
| training (ARC) | 539 | 2.17 × 10¹¹ |
| augmented | 461 | 3.52 × 10¹⁰ |
| custom | 30 | 9.59 × 10⁸ |
| arc_puzzle_bank_seventh_21_bundle | 21 | 2.39 × 10⁸ |
| arc_puzzle_bank_nineteenth_21_bundle | 21 | 1.80 × 10⁸ |
| arc_puzzle_bank_twentyfirst_21_bundle | 21 | 7.77 × 10⁷ |
| arc_puzzle_bank_twelfth_21_bundle | 21 | 7.00 × 10⁷ |
| arc_puzzle_bank_tenth21 | 21 | 6.12 × 10⁷ |
| arc_puzzle_bank_eighteenth_21_bundle | 21 | 5.07 × 10⁷ |
| arc_puzzle_bank_twelfth21 | 21 | 5.02 × 10⁷ |

## Axis parser-tag distribution

| tag | count |
|---|---:|
| `int-range` (e.g. `1..10`) | 15,224 |
| `choices` (e.g. `noise\|sparse\|...`) | 8,433 |
| `unparsed:sparse` | 2,178 |
| `bool` | 1,843 |
| `unparsed:3` | 644 |
| `unparsed:fixed` | 559 |
| `unparsed:2` | 541 |
| `unparsed:1` | 409 |
| `unparsed:4` | 272 |
| `float-range-100-buckets` | 259 |
| `unparsed:varied` | 222 |
| `unparsed:scattered_colored_motifs` | 208 |

The `unparsed:*` tags above represent axes whose `valid` field is a
single descriptive token rather than a range or pipe-list. These
contribute 1 to the bounded reach. Tightening these strings to enumerable
ranges in the generator source would raise the headline number by
roughly 1–2 orders of magnitude.

## Reproducing

```bash
python3 scripts/combinatorial_reach.py
python3 scripts/combinatorial_reach.py --json /tmp/per_gen.jsonl
python3 scripts/combinatorial_reach.py --seed-budget 10000
```
