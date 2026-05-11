# ARC-style Puzzle Bank — 21 more puzzles (set 20)

This twentieth bank leans into **motif search, window matching, transformed copies, near-match repair, and tiny lookup libraries**. The core move is to stop treating a board as a single undifferentiated image and instead reason over local windows: find exact copies of a template, accept rotated or reflected copies when needed, repair windows that are almost correct, count matches across candidates, or use a matched key panel to retrieve a paired value panel.

The core primitive introduced here is:

```text
find_template_matches(board, template, wildcard=0, transforms=('id',))
Slide a template-sized window across a board and return every location where the
template matches. The default mode demands literal equality, but the same
framework can be widened to quarter-turn rotations, reflections, or richer
near-match checks such as one-hole or two-hole completion.
```

The reference programs assume the shared helpers in `arc_puzzle_bank_21_set20_reference.py`.

## Index

### Easy

- **S20_E1** — Mark the Centers of Exact Matches

- **S20_E2** — Recolor Every Exact Match Window

- **S20_E3** — Keep Only the Exact Match Windows

- **S20_E4** — Selector Color Fills the Matches

- **S20_E5** — Which Candidate Contains the Template?

- **S20_E6** — Row Strip of Match Counts

- **S20_E7** — Mark the Bottom-Right Corners of Matches

### Medium

- **S20_M1** — Rotated Match Centers

- **S20_M2** — Dihedral Match Union

- **S20_M3** — Repair One-Hole Instances

- **S20_M4** — Selector Chooses Which Template to Search

- **S20_M5** — Which Candidate Contains a Rotated Match?

- **S20_M6** — Draw Boxes Around the Matches

- **S20_M7** — Only Count Matches With Blank Borders

### Hard

- **S20_H1** — Odd Candidate Under Dihedral Equivalence

- **S20_H2** — Match Up to Color Remapping

- **S20_H3** — Repair Rotated Two-Hole Instances

- **S20_H4** — Template-Key Library Lookup

- **S20_H5** — Dihedral Congruence Matrix

- **S20_H6** — Learn the Transform and Apply It

- **S20_H7** — Which Board Has the Most Rotated Matches?


# Easy


## S20_E1 — Mark the Centers of Exact Matches
**Skills:** template extraction, exact window matching, center marking

**Primitive note:** This is the basic use of find_template_matches: detect exact matches and convert each top-left coordinate into a derived marker position.

**Scaffold:**

- Crop the small template from the left panel and search the board on the right.
- Every exact 3×3 occurrence counts as a match.
- For each match, mark only its center cell in color 8.

**Train 1 input**

```text
20092000000
20092000000
22292220200
00090222200
00090200222
00097200000
```
**Train 1 output**

```text
0000000
0800000
0000000
0000080
0000000
0000000
```
**Train 2 input**

```text
20093000222
20090020002
22290020002
00090022200
00092000000
00092000000
00092220000
```
**Train 2 output**

```text
0000000
0000000
0008000
0000000
0000000
0800000
0000000
```
**Test input**

```text
200902000000
200902002220
222902222000
000900002200
000920000200
000920000222
000922200000
```
**Test output**

```text
00000000
00800000
00000000
00000000
00000080
08000000
00000000
```
**Written solution:** Extract the template panel, then slide it across the board looking for exact matches. Whenever the full template matches a 3×3 window, compute that window’s center cell and place an 8 there on an otherwise blank board.

**Reference program:**

```python
def solve_S20_E1(grid):
    template, board = parse_template_board(grid)
    th, tw = dims(template)
    cells = [(r + th//2, c + tw//2) for r, c, _, _ in find_template_matches(board, template, 'id')]
    return render_board(*dims(board), cells, 8)
```

## S20_E2 — Recolor Every Exact Match Window
**Skills:** exact motif search, union of matched cells, same-size blank output

**Primitive note:** find_template_matches supplies the match locations; the output is the union of the matched template footprints.

**Scaffold:**

- Find all windows that match the template exactly.
- Take the union of all occupied template cells across those windows.
- Render that union in a single color on a blank board.

**Train 1 input**

```text
33393330000
03090300000
03090333300
00090003333
00090000030
00096000030
```
**Train 1 output**

```text
8880000
0800000
0800000
0000888
0000080
0000080
```
**Train 2 input**

```text
33390000003
03090333333
03090030003
00090030000
00090003330
00090000300
00090000300
```
**Train 2 output**

```text
0000000
0888000
0080000
0080000
0008880
0000800
0000800
```
**Test input**

```text
333900333000
030900030000
030900030000
000900000333
000933300030
000903000030
000903000000
```
**Test output**

```text
00888000
00080000
00080000
00000888
88800080
08000080
08000000
```
**Written solution:** Search the board for exact copies of the template. For each copy, add all of that window’s nonzero template cells to a union set. Output a blank board of the same size with that union painted in color 8.

**Reference program:**

```python
def solve_S20_E2(grid):
    template, board = parse_template_board(grid)
    matches = find_template_matches(board, template, 'id')
    return board_union_matches(board, matches, 8)
```

## S20_E3 — Keep Only the Exact Match Windows
**Skills:** window filtering, exact template detection, preserve original colors

**Primitive note:** The same match coordinates can drive a filter instead of a marker: keep matched cells, drop everything else.

**Scaffold:**

- Ignore everything except windows that match the template exactly.
- Copy the original board colors only inside those matched windows.
- Set every other cell to 0.

**Train 1 input**

```text
06690660006
06090600000
66096600000
00090666066
00090006060
00097000660
```
**Train 1 output**

```text
0660000
0600000
6600000
0000066
0000060
0000660
```
**Train 2 input**

```text
06690000066
06090006660
66090006060
00090066000
00090660000
00090600000
00096600003
```
**Train 2 output**

```text
0000000
0006600
0006000
0066000
0660000
0600000
6600000
```
**Test input**

```text
066900660600
060900600666
660906600006
000906600000
000906000660
000966000600
000900006600
```
**Test output**

```text
00660000
00600000
06600000
06600000
06000660
66000600
00006600
```
**Written solution:** Locate every exact match of the template in the larger board. Start from a blank board, then copy the original board’s colors only inside the matched windows. All unmatched regions are erased to 0.

**Reference program:**

```python
def solve_S20_E3(grid):
    template, board = parse_template_board(grid)
    matches = find_template_matches(board, template, 'id')
    return board_copy_matches(board, matches)
```

## S20_E4 — Selector Color Fills the Matches
**Skills:** exact matching, metadata extraction, color transfer

**Primitive note:** This combines find_template_matches with a tiny metadata panel that chooses the output color.

**Scaffold:**

- Read the single selector color from the narrow middle panel.
- Find the exact matches of the template in the board.
- Fill the matched template footprints with the selector color.

**Train 1 input**

```text
0509790050000
5559090555000
0509090050000
0009095550050
0009090500555
0009090000050
```
**Train 1 output**

```text
0070000
0777000
0070000
0000070
0000777
0000070
```
**Train 2 input**

```text
0509690000550
5559090500555
0509095550050
0009090500000
0009090000500
0009090005550
0009090000500
```
**Train 2 output**

```text
0000060
0600666
6660060
0600000
0000600
0006660
0000600
```
**Test input**

```text
05098900050000
55590900555000
05090900050000
00090900000050
00090905000555
00090955500050
00090905000000
```
**Test output**

```text
00080000
00888000
00080000
00000080
08000888
88800080
08000000
```
**Written solution:** The middle metadata panel tells you which color to paint with. Find every exact match of the template in the board, take the union of their occupied template cells, and render that union in the selector color.

**Reference program:**

```python
def solve_S20_E4(grid):
    template, color, board = parse_template_selector_board(grid)
    matches = find_template_matches(board, template, 'id')
    return board_union_matches(board, matches, color)
```

## S20_E5 — Which Candidate Contains the Template?
**Skills:** template search inside candidates, candidate selection, symbolic strip output

**Primitive note:** Instead of searching one board, reuse find_template_matches across a list of candidates and summarize the results symbolically.

**Scaffold:**

- Treat each right-hand panel as its own search board.
- Check whether the template appears exactly in each candidate.
- Mark the matching candidate positions in a 1×N strip.

**Train 1 input**

```text
270960000900000902700
222902220902700902020
202900270902220902020
000902200902020900050
000900000900003900000
```
**Train 1 output**

```text
080
```
**Train 2 input**

```text
270900000790020209400000
222900200090022209000000
202900222090007209027000
000900202090000009022200
000900000096000009020200
```
**Train 2 output**

```text
008
```
**Test input**

```text
270900000096000009000270
222900220090000009000222
202907200090027009000202
000902220090022209000000
000900000090020009000000
000900000590000009200000
```
**Test output**

```text
008
```
**Written solution:** Search each candidate panel independently for an exact occurrence of the template. Output a one-row strip with 8 underneath every candidate that contains at least one exact match, and 0 under the others.

**Reference program:**

```python
def solve_S20_E5(grid):
    template, candidates = parse_template_candidates(grid)
    hits = [i for i, board in enumerate(candidates) if find_template_matches(board, template, 'id')]
    return strip_mark(len(candidates), hits, 8)
```

## S20_E6 — Row Strip of Match Counts
**Skills:** exact matching, counting by row, symbolic numeric output

**Primitive note:** find_template_matches gives top-left coordinates; here they are aggregated by row rather than painted spatially.

**Scaffold:**

- Find every exact template match.
- Group matches by their top-left row.
- Write those per-row counts as colors in a single row strip.

**Train 1 input**

```text
666966600666
600960000606
666966606666
000960006000
000966606660
000900000000
```
**Train 1 output**

```text
202000
```
**Train 2 input**

```text
666930000000
600900666666
666900600600
000900666666
000906660000
000906000000
000906660000
```
**Train 2 output**

```text
0200100
```
**Test input**

```text
6669066600666
6009060000006
6669066600666
0009666006660
0009606666000
0009666006660
0009006660000
```
**Test output**

```text
1002100
```
**Written solution:** Count how many exact template matches start in each row of the board. Output a 1×H strip whose entries are those counts, using ARC colors as small integers.

**Reference program:**

```python
def solve_S20_E6(grid):
    template, board = parse_template_board(grid)
    counts = [0] * dims(board)[0]
    for r, c, _, _ in find_template_matches(board, template, 'id'):
        counts[r] += 1
    return [counts]
```

## S20_E7 — Mark the Bottom-Right Corners of Matches
**Skills:** exact matching, coordinate derivation, spatial markers

**Primitive note:** Once matches are known, any fixed offset inside the window can be marked; this puzzle uses the bottom-right corner.

**Scaffold:**

- Find every exact template match.
- Convert each match window into its bottom-right corner coordinate.
- Mark those coordinates on a blank board.

**Train 1 input**

```text
06690066000
06090060000
66090660000
00090600066
00096600060
00090000660
```
**Train 1 output**

```text
0000000
0000000
0008000
0000000
0080000
0000008
```
**Train 2 input**

```text
06690000005
06090660000
66090600000
00096600000
00090000660
00090000600
00090006600
```
**Train 2 output**

```text
0000000
0000000
0000000
0080000
0000000
0000000
0000080
```
**Test input**

```text
066906600600
060906000666
660966066006
000900060000
000900660066
000900000060
000900000660
```
**Test output**

```text
00000000
00000000
00800000
00000000
00008000
00000000
00000008
```
**Written solution:** Search for exact matches of the template. For each match window, compute its bottom-right cell and place an 8 there on an otherwise blank board of the same size as the search board.

**Reference program:**

```python
def solve_S20_E7(grid):
    template, board = parse_template_board(grid)
    th, tw = dims(template)
    cells = [(r + th - 1, c + tw - 1) for r, c, _, _ in find_template_matches(board, template, 'id')]
    return render_board(*dims(board), cells, 8)
```

# Medium


## S20_M1 — Rotated Match Centers
**Skills:** rotation variants, transformed motif search, center marking

**Primitive note:** This is the first transform-aware extension of find_template_matches: search across rot4 instead of only the identity.

**Scaffold:**

- Do not require the board copy to have the same orientation as the template.
- Accept any quarter-turn rotation of the template.
- Mark the center of each rotated match.

**Train 1 input**

```text
270927000222
222922200007
202920202220
000900000270
000902022200
000902220000
000900720000
```
**Train 1 output**

```text
00000000
08000000
00000000
00000800
00000000
00800000
00000000
```
**Train 2 input**

```text
270900000000
222900022000
202900720000
000920222000
000922200222
000907200027
000900000220
```
**Train 2 output**

```text
00000000
00000000
00080000
00000000
08000000
00000080
00000000
```
**Test input**

```text
270902220000
222900270000
202927200000
000922202020
000920202220
000902200720
000972000000
000922200000
```
**Test output**

```text
00000000
00000000
00000000
08000000
00000800
00000000
08000000
00000000
```
**Written solution:** Generate the four quarter-turn rotations of the template and search the board for all of them. Whenever any rotated variant matches, mark the center of that matched window with an 8.

**Reference program:**

```python
def solve_S20_M1(grid):
    template, board = parse_template_board(grid)
    cells = [(r + dims(t)[0]//2, c + dims(t)[1]//2) for r, c, _, t in find_template_matches(board, template, 'rot4')]
    return render_board(*dims(board), set(cells), 8)
```

## S20_M2 — Dihedral Match Union
**Skills:** reflection handling, rotation handling, union of transformed matches

**Primitive note:** find_template_matches can be widened from rot4 to the full dihedral family when mirror images should also count.

**Scaffold:**

- Allow both rotations and reflections of the template.
- Any dihedral-equivalent copy counts as a match.
- Paint the union of all matched footprints in color 8.

**Train 1 input**

```text
200920000000
200920000000
222922200020
000902220020
000902002220
000902000006
```
**Train 1 output**

```text
80000000
80000000
88800080
08880080
08008880
08000000
```
**Train 2 input**

```text
200900000002
200900020002
222900020222
000902220000
000900002220
000900000020
000900000020
```
**Train 2 output**

```text
00000008
00080008
00080888
08880000
00008880
00000080
00000080
```
**Test input**

```text
2009222000000
2009200000000
2229200022200
0009000000200
0009000200200
0009000200000
0009022200000
```
**Test output**

```text
888000000
800000000
800088800
000000800
000800800
000800000
088800000
```
**Written solution:** Search the board using the full dihedral family of the template: rotations and reflections. Collect every matched window footprint and render the union of those occupied cells on a blank board in color 8.

**Reference program:**

```python
def solve_S20_M2(grid):
    template, board = parse_template_board(grid)
    matches = find_template_matches(board, template, 'dihedral')
    return board_union_matches(board, matches, 8)
```

## S20_M3 — Repair One-Hole Instances
**Skills:** near-match detection, local repair, exact template completion

**Primitive note:** A one-hole extension of template matching: accept windows with exactly one missing occupied template cell, then patch the hole.

**Scaffold:**

- Look for windows that are almost the template but missing exactly one required occupied cell.
- That missing cell appears as 0 where the template expects a nonzero color.
- Fill only the missing cells and leave the rest of the board as-is.

**Train 1 input**

```text
05090000000
55590555000
05090050000
00090000050
00090000055
00096000050
```
**Train 1 output**

```text
0050000
0555000
0050000
0000050
0000555
6000050
```
**Train 2 input**

```text
05090000000
55590500000
05095500000
00090500000
00090000500
00090005550
00090000000
```
**Train 2 output**

```text
0000000
0500000
5550000
0500000
0000500
0005550
0000500
```
**Test input**

```text
050900050000
555900055000
050900050000
000900000000
000955500050
000905000555
000900000000
```
**Test output**

```text
00050000
00555000
00050000
05000000
55500050
05000555
00000050
```
**Written solution:** Slide the template over the board and detect windows that match everywhere except for one missing required template cell, which shows up as 0. Restore that one missing cell with the template’s expected color, preserving all other board cells.

**Reference program:**

```python
def solve_S20_M3(grid):
    template, board = parse_template_board(grid)
    out = copyg(board)
    for r, c, name, t, missing in exact_or_one_hole_matches(board, template, 'id', holes=1):
        for mr, mc, tv in missing:
            out[mr][mc] = tv
    return out
```

## S20_M4 — Selector Chooses Which Template to Search
**Skills:** multi-template inputs, selector metadata, conditional search

**Primitive note:** This keeps the same search primitive but routes between multiple possible templates via a selector panel.

**Scaffold:**

- There are two candidate templates, not one.
- Read the selector panel to decide which template is active.
- Search only for that chosen template and render its matched union.

**Train 1 input**

```text
200933392920000000
200903090920000000
222903090922220000
000900090900020333
000900090900022230
000900090900000030
```
**Train 1 output**

```text
80000000
80000000
88880000
00080000
00088800
00000000
```
**Train 2 input**

```text
200933393900000000
200903090903330000
222903090900300000
000900090900300000
000900090933302000
000900090903002000
000900090903002220
```
**Train 2 output**

```text
00000000
08880000
00800000
00800000
88800000
08000000
08000000
```
**Test input**

```text
2009333939020003330
2009030909020000300
2229030909022200300
0009000909000000000
0009000909200333000
0009000909200030000
0009000909222030000
```
**Test output**

```text
000008880
000000800
000000800
000000000
000888000
000080000
000080000
```
**Written solution:** Extract the two templates from the left panels, then read the selector panel to determine which one matters. Search the right-hand board for exact matches of only that chosen template, and paint the union of those matched cells in color 8.

**Reference program:**

```python
def solve_S20_M4(grid):
    t1, t2, color, board = parse_two_templates_selector_board(grid)
    template = t1 if color == 2 else t2
    return board_union_matches(board, find_template_matches(board, template, 'id'), 8)
```

## S20_M5 — Which Candidate Contains a Rotated Match?
**Skills:** candidate search, rotation-tolerant matching, symbolic selection

**Primitive note:** The match primitive is now used as a candidate filter over rot4 variants.

**Scaffold:**

- Each candidate panel may contain the template in a different orientation.
- Accept quarter-turn rotations as valid matches.
- Mark the successful candidates in a symbolic strip.

**Train 1 input**

```text
066940000900066900002900000
060900660900000906000900000
660900600900660906660900600
000900600900000900060906000
000900000900003900000976000
```
**Train 1 output**

```text
0080
```
**Train 2 input**

```text
0669000000930000090660009000006
0609000600900000090600009000000
6609000600900660090600009000000
0009006600900600090000009000066
0009000000906600090000009000000
0009000005900000097000009000660
```
**Train 2 output**

```text
0800
```
**Test input**

```text
0669000000950000090060009000007
0609006600900000090066609000000
6609006000900600090000609000000
0009060000906000090000009000066
0009000000966000090000009000060
0009000001900000092000009000060
```
**Test output**

```text
0080
```
**Written solution:** Search each candidate panel for any quarter-turn rotation of the template. Output a one-row strip with 8 under the candidates that contain at least one rotated match and 0 under the rest.

**Reference program:**

```python
def solve_S20_M5(grid):
    template, candidates = parse_template_candidates(grid)
    hits = [i for i, board in enumerate(candidates) if find_template_matches(board, template, 'rot4')]
    return strip_mark(len(candidates), hits, 8)
```

## S20_M6 — Draw Boxes Around the Matches
**Skills:** exact matching, window geometry, rectangular border rendering

**Primitive note:** The primitive supplies window locations; the output is based on each window’s bounding rectangle rather than its occupied cells.

**Scaffold:**

- Find the exact match windows.
- Ignore the template’s internal shape for output.
- Draw the full rectangular border of each matched window.

**Train 1 input**

```text
200902000000
200902000000
222922220000
000920002000
000920002000
000900002220
```
**Train 1 output**

```text
08880000
08080000
08880000
00008880
00008080
00008880
```
**Train 2 input**

```text
200900002000
200920002000
222920002200
000922200000
000900000200
000900000200
000900000222
```
**Train 2 output**

```text
00000000
88800000
80800000
88800000
00000888
00000808
00000888
```
**Test input**

```text
2009200000000
2009200000000
2229222002000
0009000002000
0009002002220
0009002000000
0009002220000
```
**Test output**

```text
888000000
808000000
888008880
000008080
008888880
008080000
008880000
```
**Written solution:** Locate every exact template match in the board. For each match, draw the border of the entire matched window as a rectangle in color 8 on a blank board of the same size.

**Reference program:**

```python
def solve_S20_M6(grid):
    template, board = parse_template_board(grid)
    matches = find_template_matches(board, template, 'id')
    return border_boxes(board, matches, 8)
```

## S20_M7 — Only Count Matches With Blank Borders
**Skills:** context-sensitive matching, border inspection, filtered markers

**Primitive note:** This puzzle adds a border-condition filter on top of exact match detection.

**Scaffold:**

- An exact template match is not enough on its own.
- The one-cell ring around the matched window must also be blank.
- Only those isolated matches get center markers.

**Train 1 input**

```text
333933300000
030903000000
030903006000
000900003330
000900300300
000933300300
000900300000
```
**Train 1 output**

```text
00000000
08000000
00000000
00000000
00000000
00000000
00000000
```
**Train 2 input**

```text
333900000000
030903330000
030900300000
000900300020
000900000333
000900000030
000900000030
```
**Train 2 output**

```text
00000000
00000000
00800000
00000000
00000000
00000000
00000000
```
**Test input**

```text
333900333000
030900030000
030900030000
000900000700
000933300333
000903000030
000903000030
000900000000
```
**Test output**

```text
00000000
00000000
00000000
00000000
00000000
08000000
00000000
00000000
```
**Written solution:** Search for exact template matches, but then inspect the one-cell ring around each matched window. Keep only the matches whose surrounding ring is entirely 0, and mark the center of each surviving match with an 8.

**Reference program:**

```python
def solve_S20_M7(grid):
    template, board = parse_template_board(grid)
    th, tw = dims(template)
    cells = [(r + th//2, c + tw//2) for r, c, _, _ in exact_with_border_clear(board, template)]
    return render_board(*dims(board), cells, 8)
```

# Hard


## S20_H1 — Odd Candidate Under Dihedral Equivalence
**Skills:** dihedral normalization, candidate comparison, odd-one-out selection

**Primitive note:** Instead of searching a larger board, the match primitive is used as direct shape equivalence under the dihedral group.

**Scaffold:**

- Compare each candidate to the prototype up to rotation or reflection.
- Most candidates are equivalent to the prototype under that rule.
- Mark the candidate that is not dihedrally equivalent.

**Train 1 input**

```text
2709222907292009202
2229027922292009222
2029220920292229072
```
**Train 1 output**

```text
0080
```
**Train 2 input**

```text
2709066902292709222
2229060972092229720
2029660922292029022
```
**Train 2 output**

```text
8000
```
**Test input**

```text
2709202922092709333
2229222902792229030
2029072922292029030
```
**Test output**

```text
0008
```
**Written solution:** Treat the leftmost panel as the prototype. Normalize candidate shapes up to rotation and reflection, then compare each candidate with the prototype under that equivalence class. Output a strip marking the candidate that does not belong to the prototype’s dihedral class.

**Reference program:**

```python
def solve_S20_H1(grid):
    template, candidates = parse_template_candidates(grid)
    odd = [i for i, panel in enumerate(candidates) if not dihedral_equiv(template, panel)]
    return strip_mark(len(candidates), odd, 8)
```

## S20_H2 — Match Up to Color Remapping
**Skills:** structural pattern matching, color-equivalence reasoning, symbolic detection

**Primitive note:** This extends matching beyond literal equality to structural color remapping.

**Scaffold:**

- The board copy does not need to use the same actual colors as the template.
- What matters is the pattern of equal and different nonzero template colors.
- Accept windows that realize the same structure under a consistent one-to-one color remapping.

**Train 1 input**

```text
2309570000000
0329075000000
2039507000000
0009000004600
0009088000640
0009008804060
0009080800000
```
**Train 1 output**

```text
000000000
080000000
000000000
000000000
000000800
000000000
000000000
```
**Train 2 input**

```text
230900000359
032900610053
203900016305
000900601000
000974000000
000904700000
000970400000
```
**Train 2 output**

```text
00000000
00000000
00080000
00000000
00000000
08000000
00000000
```
**Test input**

```text
230909400000
032900490000
203909040000
000966000000
000906605200
000960600250
000900005020
000900000000
```
**Test output**

```text
00000000
00800000
00000000
00000000
00000000
00000800
00000000
00000000
```
**Written solution:** Search the board for windows that have the same zero pattern and the same equality structure as the template, even if the concrete nonzero colors are different. A valid match must admit a consistent injective mapping from template colors to board colors. Mark the center of each such window with an 8.

**Reference program:**

```python
def solve_S20_H2(grid):
    template, board = parse_template_board(grid)
    th, tw = dims(template)
    cells = [(r + th//2, c + tw//2) for r, c, _ in color_pattern_match(board, template)]
    return render_board(*dims(board), cells, 8)
```

## S20_H3 — Repair Rotated Two-Hole Instances
**Skills:** rotation-tolerant near-match detection, multi-hole repair, local completion

**Primitive note:** This combines transform-aware matching with exact-two-hole repair.

**Scaffold:**

- The board contains rotated versions of the template.
- Each near-match is missing exactly two required occupied cells.
- Fill those missing cells while preserving the rest of the board.

**Train 1 input**

```text
270920000000
222922200000
202900200000
000900002220
000900000200
000900002000
000900000000
```
**Train 1 output**

```text
27200000
22200000
27200000
00002220
00000270
00002200
00000000
```
**Train 2 input**

```text
270900000000
222900002000
202900220000
000900072000
000900000002
000900000720
000900000220
```
**Train 2 output**

```text
00000000
00202000
00222000
00072000
00000022
00000720
00000222
```
**Test input**

```text
270902700000
222900220000
202902000000
000900002200
000900000070
000920202200
000922200000
000907200000
```
**Test output**

```text
02700000
02220000
02020000
00002220
00000270
20202200
22200000
07200000
```
**Written solution:** Generate the quarter-turn rotations of the template and scan the board for windows that match one of those rotations except for exactly two missing occupied cells. Restore those missing cells with the appropriate colors from the matching rotated template.

**Reference program:**

```python
def solve_S20_H3(grid):
    template, board = parse_template_board(grid)
    out = copyg(board)
    for r, c, name, t, missing in exact_or_one_hole_matches(board, template, 'rot4', holes=2):
        for mr, mc, tv in missing:
            out[mr][mc] = tv
    return out
```

## S20_H4 — Template-Key Library Lookup
**Skills:** key detection, lookup dispatch, match-driven value retrieval

**Primitive note:** Matching drives symbolic lookup here: the matched key panel selects the output panel.

**Scaffold:**

- The first and third panels are keys; the second and fourth panels are their values.
- Find which key appears in the query board on the far right.
- Return the value panel paired with that matched key.

**Train 1 input**

```text
2009880090669808090000000
2009088090609088090200000
2229008896609888890200000
0009000890009800090222600
0009000090009000090000666
0009000090009000090000006
```
**Train 1 output**

```text
8800
0880
0088
0008
```
**Train 2 input**

```text
2009880090669808092220000
2009088090609088092000000
2229008896609888892000660
0009000890009800090000600
0009000090009000090006600
0009000090009000090000000
```
**Train 2 output**

```text
8080
0880
8888
8000
```
**Test input**

```text
20098800906698080900000066
20090880906090880900000060
22290088966098888900000660
00090008900098000900000000
00090000900090000920000000
00090000900090000920000000
00090000900090000922000000
```
**Test output**

```text
8080
0880
8888
8000
```
**Written solution:** Treat the left side as a tiny key-value library: key1 maps to value1 and key2 maps to value2. Search the query board for an exact occurrence of either key, then output the value panel associated with the key that was found.

**Reference program:**

```python
def solve_S20_H4(grid):
    k1, v1, k2, v2, query = parse_key_values_query(grid)
    return v1 if find_template_matches(query, k1, 'id') else v2
```

## S20_H5 — Dihedral Congruence Matrix
**Skills:** pairwise comparison, equivalence classes, symbolic matrix construction

**Primitive note:** This generalizes dihedral matching from one prototype-vs-candidates check to a full pairwise relation matrix.

**Scaffold:**

- Compare every candidate panel with every other candidate panel.
- Two panels are linked if one can be rotated or reflected into the other.
- Write the result as a square matrix of 8s and 0s.

**Train 1 input**

```text
200922290669066
200920090609060
222920096609660
```
**Train 1 output**

```text
8800
8800
0088
0088
```
**Train 2 input**

```text
270907293339050
222922290309555
202920290309050
```
**Train 2 output**

```text
8800
8800
0080
0008
```
**Test input**

```text
066906696609200
060906090609200
660966090669222
```
**Test output**

```text
8880
8880
8880
0008
```
**Written solution:** For every pair of candidate panels, test whether they are dihedrally equivalent: one can be transformed into the other by a rotation or reflection. Output a square matrix whose (i, j) entry is 8 when the pair is equivalent and 0 otherwise.

**Reference program:**

```python
def solve_S20_H5(grid):
    panels = [crop_nonzero(p) for p in split_panels(grid)]
    n = len(panels)
    out = blank(n, n, 0)
    for i in range(n):
        for j in range(n):
            if dihedral_equiv(panels[i], panels[j]):
                out[i][j] = 8
    return out
```

## S20_H6 — Learn the Transform and Apply It
**Skills:** transform inference, analogy, dihedral action on a query shape

**Primitive note:** Here the primitive is used one level up: infer the transform class from an example pair, then reapply it to a new shape.

**Scaffold:**

- The first two panels show an example input-output pair.
- Infer the single dihedral transform that turns the first into the second.
- Apply that same transform to the third panel.

**Train 1 input**

```text
20092229066
20092009060
22292009660
```
**Train 1 output**

```text
600
666
006
```
**Train 2 input**

```text
27092229333
22290279030
20292209030
```
**Train 2 output**

```text
003
333
003
```
**Test input**

```text
06696009666
06096669600
66090069666
```
**Test output**

```text
666
606
606
```
**Written solution:** Use the example source and example target panels to infer one dihedral transform—such as a quarter-turn rotation or reflection. Then apply that same transform to the query panel and output the transformed query.

**Reference program:**

```python
def solve_S20_H6(grid):
    src, tgt, query = parse_example_transform_query(grid)
    name = detect_transform(src, tgt)
    return apply_transform(query, name)
```

## S20_H7 — Which Board Has the Most Rotated Matches?
**Skills:** counting transformed matches, candidate comparison, symbolic argmax output

**Primitive note:** This is an argmax puzzle over rotated match counts rather than a yes/no filter.

**Scaffold:**

- Search each candidate board for quarter-turn rotations of the template.
- Count how many rotated matches each candidate contains.
- Mark the candidate with the highest count.

**Train 1 input**

```text
270927000009222000090000006
222922200009027000090000000
202920200009220000090002200
000900000009000500090072000
000900000009000020290022200
000900000009000022290000000
000900000039000007290000000
```
**Train 1 output**

```text
080
```
**Train 2 input**

```text
270927000222900000006900000000
222922200027900220000900000000
202920200220907200000900000000
000900000000902220000900022200
000900000000900000000900002700
000900202000900000270900022000
000900222000900000222900000000
000900072004900000202950000000
```
**Train 2 output**

```text
800
```
**Test input**

```text
270920200000960002700900000000
222922200000900002220900000000
202907200000900002020900022000
000900000000922200000900720000
000900000000902700000900222000
000900000222922000202900000000
000900000027900000222900000000
000900000224900000072950000000
```
**Test output**

```text
080
```
**Written solution:** For each candidate board, count the number of matches of the template across all four quarter-turn rotations. Compare those counts and output a one-row strip marking the board or boards that achieve the maximum.

**Reference program:**

```python
def solve_S20_H7(grid):
    template, candidates = parse_template_candidates(grid)
    counts = [len(find_template_matches(board, template, 'rot4')) for board in candidates]
    best = max(counts)
    return strip_mark(len(candidates), [i for i, c in enumerate(counts) if c == best and c > 0], 8)
```
