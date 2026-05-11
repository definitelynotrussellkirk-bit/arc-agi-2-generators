from __future__ import annotations
from collections import Counter, deque, defaultdict
import json

DIR4 = [(-1,0), (1,0), (0,-1), (0,1)]
depth_palette = [2,4,6,7,3,9]

def blank(h,w,val=0):
    return [[val for _ in range(w)] for _ in range(h)]

def clone(g):
    return [row[:] for row in g]

def size(g):
    return (len(g), len(g[0]) if g else 0)

def in_bounds(g,r,c):
    h,w=size(g)
    return 0<=r<h and 0<=c<w

def grid_from_strings(rows):
    return [[int(ch) for ch in row] for row in rows]

def strings_from_grid(g):
    return ["".join(str(v) for v in row) for row in g]

def place_shape(g, shape, top, left, overwrite_zero=False):
    h,w=size(g)
    sh,sw=size(shape)
    for r in range(sh):
        for c in range(sw):
            v=shape[r][c]
            if overwrite_zero or v!=0:
                rr,cc=top+r,left+c
                if 0<=rr<h and 0<=cc<w:
                    g[rr][cc]=v
    return g

def bbox(cells):
    rs=[r for r,c in cells]
    cs=[c for r,c in cells]
    return min(rs), min(cs), max(rs), max(cs)

def crop_bbox(g, cells=None):
    if cells is None:
        cells=[(r,c) for r,row in enumerate(g) for c,v in enumerate(row) if v!=0]
    if not cells:
        return [[0]]
    r0,c0,r1,c1=bbox(cells)
    return [row[c0:c1+1] for row in g[r0:r1+1]]

def crop_nonzero(g):
    return crop_bbox(g)

def rotate90(g):
    h,w=size(g)
    return [[g[h-1-r][c] for r in range(h)] for c in range(w)]

def rotate180(g):
    return [list(reversed(row)) for row in reversed(g)]

def rotate270(g):
    h,w=size(g)
    return [[g[r][w-1-c] for r in range(h)] for c in range(w-1,-1,-1)]

def flip_h(g):
    return [list(reversed(row)) for row in g]

def flip_v(g):
    return [row[:] for row in reversed(g)]

def apply_transform(g, cmd):
    # 0 identity,1 rot90,2 rot180,3 rot270,4 flip_h,5 flip_v
    if cmd==0:
        return clone(g)
    if cmd==1:
        return rotate90(g)
    if cmd==2:
        return rotate180(g)
    if cmd==3:
        return rotate270(g)
    if cmd==4:
        return flip_h(g)
    if cmd==5:
        return flip_v(g)
    raise ValueError(cmd)

def components_color(g):
    h,w=size(g)
    seen=set()
    comps=[]
    for r in range(h):
        for c in range(w):
            if g[r][c]==0 or (r,c) in seen:
                continue
            color=g[r][c]
            q=[(r,c)]
            seen.add((r,c))
            cells=[]
            while q:
                rr,cc=q.pop()
                cells.append((rr,cc))
                for dr,dc in DIR4:
                    nr,nc=rr+dr,cc+dc
                    if in_bounds(g,nr,nc) and (nr,nc) not in seen and g[nr][nc]==color:
                        seen.add((nr,nc))
                        q.append((nr,nc))
            comps.append({"color":color,"cells":cells})
    return comps

def components_nonzero(g):
    h,w=size(g)
    seen=set()
    comps=[]
    for r in range(h):
        for c in range(w):
            if g[r][c]==0 or (r,c) in seen:
                continue
            q=[(r,c)]
            seen.add((r,c))
            cells=[]
            while q:
                rr,cc=q.pop()
                cells.append((rr,cc))
                for dr,dc in DIR4:
                    nr,nc=rr+dr,cc+dc
                    if in_bounds(g,nr,nc) and (nr,nc) not in seen and g[nr][nc]!=0:
                        seen.add((nr,nc))
                        q.append((nr,nc))
            comps.append({"cells":cells})
    return comps

def count_holes_binary(shape):
    h,w=size(shape)
    seen=set()
    q=deque()
    for r in range(h):
        for c in range(w):
            if r in (0,h-1) or c in (0,w-1):
                if shape[r][c]==0 and (r,c) not in seen:
                    seen.add((r,c)); q.append((r,c))
    while q:
        r,c=q.popleft()
        for dr,dc in DIR4:
            nr,nc=r+dr,c+dc
            if 0<=nr<h and 0<=nc<w and shape[nr][nc]==0 and (nr,nc) not in seen:
                seen.add((nr,nc)); q.append((nr,nc))
    holes=0
    for r in range(h):
        for c in range(w):
            if shape[r][c]==0 and (r,c) not in seen:
                holes += 1
                dq=deque([(r,c)])
                seen.add((r,c))
                while dq:
                    rr,cc=dq.popleft()
                    for dr,dc in DIR4:
                        nr,nc=rr+dr,cc+dc
                        if 0<=nr<h and 0<=nc<w and shape[nr][nc]==0 and (nr,nc) not in seen:
                            seen.add((nr,nc)); dq.append((nr,nc))
    return holes

def fill_rect_outline(g,r0,c0,r1,c1,color):
    for c in range(c0,c1+1):
        g[r0][c]=color
        g[r1][c]=color
    for r in range(r0,r1+1):
        g[r][c0]=color
        g[r][c1]=color
    return g

def concat_h(grids, sep=0):
    if not grids:
        return [[0]]
    h=max(len(g) for g in grids)
    w=sum(len(g[0]) for g in grids) + sep*(len(grids)-1)
    out=blank(h,w,0)
    x=0
    for i,g in enumerate(grids):
        place_shape(out,g,0,x)
        x += len(g[0])
        if i < len(grids)-1:
            x += sep
    return out

def concat_v(grids, sep=0):
    if not grids:
        return [[0]]
    h=sum(len(g) for g in grids) + sep*(len(grids)-1)
    w=max(len(g[0]) for g in grids)
    out=blank(h,w,0)
    y=0
    for i,g in enumerate(grids):
        place_shape(out,g,y,0)
        y += len(g)
        if i < len(grids)-1:
            y += sep
    return out

def panel_split_horizontal(g):
    h,w=size(g)
    parts=[]
    c=0
    while c<w:
        while c<w and all(g[r][c]==0 for r in range(h)):
            c+=1
        if c>=w:
            break
        c0=c
        while c<w and not all(g[r][c]==0 for r in range(h)):
            c+=1
        parts.append([row[c0:c] for row in g])
    return parts

def canonicalize_transform_equiv(shape):
    variants=[clone(shape), rotate90(shape), rotate180(shape), rotate270(shape), flip_h(shape), flip_v(shape), rotate90(flip_h(shape)), rotate90(flip_v(shape))]
    canon=min(strings_from_grid(crop_nonzero(v)) for v in variants)
    return canon

def manhattan(a,b):
    return abs(a[0]-b[0]) + abs(a[1]-b[1])

def flood_regions_not_wall(g, wall=8):
    h,w=size(g)
    seen=set()
    regions=[]
    for r in range(h):
        for c in range(w):
            if g[r][c]==wall or (r,c) in seen:
                continue
            q=deque([(r,c)])
            seen.add((r,c))
            cells=[]
            while q:
                rr,cc=q.popleft()
                cells.append((rr,cc))
                for dr,dc in DIR4:
                    nr,nc=rr+dr,cc+dc
                    if in_bounds(g,nr,nc) and g[nr][nc]!=wall and (nr,nc) not in seen:
                        seen.add((nr,nc)); q.append((nr,nc))
            regions.append(cells)
    return regions

def palette_lift(template, legend, transform=None, symbol_order=None):
    """Recolor symbolic template values 1..k using legend list."""
    if transform is not None:
        template=apply_transform(template, transform)
    out=blank(*size(template),0)
    mapping={}
    if symbol_order is None:
        syms=sorted({v for row in template for v in row if v!=0})
        symbol_order=syms
    for sym,color in zip(symbol_order, legend):
        mapping[sym]=color
    h,w=size(template)
    for r in range(h):
        for c in range(w):
            v=template[r][c]
            if v!=0:
                out[r][c]=mapping.get(v,v)
    return out

def shape_area(g):
    return sum(v!=0 for row in g for v in row)

def relation_color(area_i, holes_i, area_j, holes_j, same_self=False):
    if same_self:
        return 5
    same_area = area_i == area_j
    same_holes = holes_i == holes_j
    if same_area and same_holes:
        return 6
    if same_area:
        return 2
    if same_holes:
        return 3
    return 0

def choose_component_by_cmd(comps, cmd):
    scored=[]
    for comp in comps:
        cells=comp["cells"]
        r0,c0,r1,c1=bbox(cells)
        area=len(cells)
        width=c1-c0+1
        height=r1-r0+1
        color=comp.get("color",0)
        if cmd==1: key=(area, r0, c0, color)
        elif cmd==2: key=(-area, r0, c0, color)
        elif cmd==3: key=(-width, -area, r0, c0, color)
        elif cmd==4: key=(-height, -area, r0, c0, color)
        else: key=(area, r0, c0, color)
        scored.append((key,comp))
    return sorted(scored, key=lambda t:t[0])[0][1]

def find_prototype_and_anchors(g):
    comps=components_nonzero(g)
    # prototype is component with area >1 and containing an 8
    proto_comp=None
    for comp in comps:
        vals=[g[r][c] for r,c in comp["cells"]]
        if 8 in vals and len(comp["cells"])>1:
            if proto_comp is None or len(comp["cells"])>len(proto_comp["cells"]):
                proto_comp=comp
    assert proto_comp is not None
    r0,c0,r1,c1=bbox(proto_comp["cells"])
    template=[row[c0:c1+1] for row in g[r0:r1+1]]
    origin=None
    for r in range(len(template)):
        for c in range(len(template[0])):
            if template[r][c]==8:
                origin=(r,c)
                break
        if origin: break
    anchors=[(r,c) for r,row in enumerate(g) for c,v in enumerate(row) if v==8 and (r,c) not in proto_comp["cells"]]
    anchors=[(r0+origin[0], c0+origin[1])] + anchors
    return template, origin, anchors

def overlay_template_copies_same_size(template, origin, anchors, shape_size, overlap_color=9):
    h,w=shape_size
    out=blank(h,w,0)
    for ar,ac in anchors:
        top,left = ar-origin[0], ac-origin[1]
        th,tw=size(template)
        for r in range(th):
            for c in range(tw):
                v=template[r][c]
                if v==0: 
                    continue
                rr,cc=top+r,left+c
                if 0<=rr<h and 0<=cc<w:
                    if out[rr][cc]==0:
                        out[rr][cc]=v
                    elif out[rr][cc]!=v:
                        out[rr][cc]=overlap_color
    return out

TRANSFORMS = [
    ("id", lambda g: clone(g), 0),
    ("rot90", rotate90, 1),
    ("rot180", rotate180, 2),
    ("rot270", rotate270, 3),
    ("flip_h", flip_h, 4),
    ("flip_v", flip_v, 5),
]

def rule_e113(g):
    legend=[v for v in g[0] if v!=0]
    template=[row[1:4] for row in g[2:5]]
    return palette_lift(template, legend)

def rule_e114(g):
    cells=[(r,c,v) for r,row in enumerate(g) for c,v in enumerate(row) if v!=0]
    assert len(cells)==2
    (r0,c0,color),(r1,c1,color2)=cells
    assert color==color2
    out=blank(*size(g),0)
    fill_rect_outline(out, min(r0,r1), min(c0,c1), max(r0,r1), max(c0,c1), color)
    return out

def rule_e115(g):
    h,w=size(g)
    out=clone(g)
    # rows
    for r in range(h):
        positions=defaultdict(list)
        for c,v in enumerate(g[r]):
            if v!=0:
                positions[v].append(c)
        for color, cols in positions.items():
            if len(cols)==2:
                c1,c2=sorted(cols)
                if all(g[r][c]==0 for c in range(c1+1,c2)):
                    for c in range(c1,c2+1):
                        out[r][c]=color
    # cols
    for c in range(w):
        positions=defaultdict(list)
        for r in range(h):
            v=g[r][c]
            if v!=0:
                positions[v].append(r)
        for color, rows in positions.items():
            if len(rows)==2:
                r1,r2=sorted(rows)
                if all(g[r][c]==0 for r in range(r1+1,r2)):
                    for r in range(r1,r2+1):
                        out[r][c]=color
    return out

def rule_e116(g):
    h,w=size(g)
    guide_cols=[c for c in range(w) if all(g[r][c]==8 for r in range(h))]
    assert len(guide_cols)==1
    gc=guide_cols[0]
    out=clone(g)
    for r in range(h):
        for c,v in enumerate(g[r]):
            if v!=0 and c!=gc and v!=8:
                mc = 2*gc - c
                if 0<=mc<w:
                    out[r][mc]=v
    return out

def rule_e117(g):
    out=clone(g)
    comps=components_color(g)
    # choose largest rectangular outline component? simpler: find bbox of all nonzero except one seed maybe frame cells have same color repeated >1
    color_counts=Counter(v for row in g for v in row if v!=0)
    frame_color=max(color_counts, key=lambda c: color_counts[c])
    frame_cells=[(r,c) for r,row in enumerate(g) for c,v in enumerate(row) if v==frame_color]
    r0,c0,r1,c1=bbox(frame_cells)
    # seed color is non-frame nonzero
    seed=[v for row in g for v in row if v!=0 and v!=frame_color][0]
    for r in range(r0+1,r1):
        for c in range(c0+1,c1):
            if out[r][c]==0:
                out[r][c]=seed
    return out

def rule_e118(g):
    comps=components_color(g)
    scored=[]
    for comp in comps:
        area=len(comp["cells"])
        r0,c0,_,_=bbox(comp["cells"])
        scored.append(( -area, r0, c0, comp))
    comp=sorted(scored, key=lambda t:t[:3])[0][3]
    return crop_bbox(g, comp["cells"])

def rule_e119(g):
    counts=Counter(v for row in g for v in row if v!=0)
    order=sorted(counts.items(), key=lambda kv:(-kv[1], kv[0]))
    row=[]
    for color,count in order:
        row.extend([color]*count)
    return [row]

def rule_m113(g):
    legend=[v for v in g[0] if v!=0]
    selector=[v for v in g[1] if v!=0]
    bank={}
    h,w=size(g)
    c=0
    while c<w:
        if g[3][c]!=0:
            key=g[3][c]
            bank[key]=[row[c:c+2] for row in g[4:6]]
            c += 3
        else:
            c += 1
    blocks=[palette_lift(bank[k], legend) for k in selector]
    return concat_h(blocks, sep=0)

def rule_m114(g):
    cmd=g[0][0]
    cells=[(r,c) for r,row in enumerate(g) for c,v in enumerate(row) if v!=0 and not (r==0 and c==0)]
    obj=crop_bbox(g,cells)
    return apply_transform(obj, cmd)

def rule_m115(g):
    out=clone(g)
    regions=flood_regions_not_wall(g, wall=8)
    for region in regions:
        # skip exterior if border not sealed; our cases sealed
        colors=[g[r][c] for r,c in region if g[r][c] not in (0,8)]
        if not colors:
            continue
        maj=sorted(Counter(colors).items(), key=lambda kv:(-kv[1], kv[0]))[0][0]
        for r,c in region:
            if out[r][c]==0:
                out[r][c]=maj
    return out

def rule_m116(g):
    panels=panel_split_horizontal(g)
    cropped=[crop_nonzero(p) for p in panels]
    infos=[]
    for p in cropped:
        area=shape_area(p)
        binary=[[1 if v!=0 else 0 for v in row] for row in p]
        holes=count_holes_binary(binary)
        infos.append((area,holes))
    n=len(infos)
    out=blank(n,n,0)
    for i,(ai,hi) in enumerate(infos):
        for j,(aj,hj) in enumerate(infos):
            out[i][j]=relation_color(ai,hi,aj,hj,same_self=(i==j))
    return out

def rule_m117(g):
    cmd=g[0][0]
    g2=clone(g)
    g2[0][0]=0
    comps=components_color(g2)
    comp=choose_component_by_cmd(comps, cmd)
    return crop_bbox(g2, comp["cells"])

def rule_m118(g):
    template, origin, anchors = find_prototype_and_anchors(g)
    return overlay_template_copies_same_size(template, origin, anchors, size(g), overlap_color=9)

def rule_m119(g):
    select_idx = g[0][0]  # 1-based
    cmd = g[0][1]
    body=g[1:]
    panels=panel_split_horizontal(body)
    panel=crop_nonzero(panels[select_idx-1])
    return apply_transform(panel, cmd)

def rule_h113(g):
    legend=[v for v in g[0] if v!=0]
    selector=[[g[1+r][c] for c in range(2)] for r in range(2)]
    cmds=[[g[3+r][c] for c in range(2)] for r in range(2)]
    bank={}
    h,w=size(g)
    c=0
    while c<w:
        if g[6][c]!=0:
            key=g[6][c]
            bank[key]=[row[c:c+3] for row in g[7:10]]
            c += 4
        else:
            c += 1
    rows=[]
    for r in range(2):
        row_blocks=[]
        for c in range(2):
            block=palette_lift(bank[selector[r][c]], legend, transform=cmds[r][c])
            row_blocks.append(block)
        rows.append(concat_h(row_blocks, sep=0))
    return concat_v(rows, sep=0)

def rule_h114(g):
    A,B,C = [crop_nonzero(p) for p in panel_split_horizontal(g)]
    # identify transform
    found=None
    for name,fn,cmd in TRANSFORMS:
        if fn(A)==B:
            found=cmd
            break
    if found is None:
        # canonical compare maybe due cropping? but transformations already cropped
        raise ValueError("no transform")
    return apply_transform(C, found)

def rule_h115(g):
    out=clone(g)
    h,w=size(g)
    seeds=[(r,c,v) for r,row in enumerate(g) for c,v in enumerate(row) if v not in (0,8)]
    for r in range(1,h-1):
        for c in range(1,w-1):
            if g[r][c]==0:
                dists=sorted((manhattan((r,c),(sr,sc)), color) for sr,sc,color in seeds)
                if len(dists)>=2 and dists[0][0]==dists[1][0]:
                    out[r][c]=5
                else:
                    out[r][c]=dists[0][1]
    return out

def rule_h116(g):
    comps=components_color(g)
    frames=[comp for comp in comps if comp["color"]==1]
    scored=[]
    for comp in frames:
        r0,c0,r1,c1=bbox(comp["cells"])
        area=(r1-r0+1)*(c1-c0+1)
        scored.append(( -area, r0, c0, comp))
    frames=[t[3] for t in sorted(scored, key=lambda x:x[:3])]
    out=blank(*size(g),0)
    for depth,comp in enumerate(frames):
        color=depth_palette[depth]
        for r,c in comp["cells"]:
            out[r][c]=color
    return out

def rule_h117(g):
    cmd1,cmd2 = g[0][0], g[0][1]
    cells=[(r,c) for r,row in enumerate(g) for c,v in enumerate(row) if v!=0 and not (r==0 and c in (0,1))]
    obj=crop_bbox(g,cells)
    return apply_transform(apply_transform(obj, cmd1), cmd2)

def rule_h118(g):
    panels=[crop_nonzero(p) for p in panel_split_horizontal(g)]
    canons=[canonicalize_transform_equiv([[1 if v!=0 else 0 for v in row] for row in p]) for p in panels]
    n=len(canons)
    out=blank(n,n,0)
    for i in range(n):
        for j in range(n):
            if i==j:
                out[i][j]=5
            else:
                out[i][j]=2 if canons[i]==canons[j] else 0
    return out

def rule_h119(g):
    comps=components_nonzero(g)
    proto_comp=None
    for comp in comps:
        vals=[g[r][c] for r,c in comp["cells"]]
        if 8 in vals and len(comp["cells"])>1:
            proto_comp=comp
            break
    assert proto_comp is not None
    r0,c0,r1,c1=bbox(proto_comp["cells"])
    proto=[row[c0:c1+1] for row in g[r0:r1+1]]
    origin=None
    for r in range(len(proto)):
        for c in range(len(proto[0])):
            if proto[r][c]==8:
                origin=(r,c); break
        if origin: break
    mask=[[1 if v!=0 else 0 for v in row] for row in proto]
    out=blank(*size(g),0)
    anchors=[(r,c,v) for r,row in enumerate(g) for c,v in enumerate(row) if v not in (0,1,8)]
    for ar,ac,color in anchors:
        top,left=ar-origin[0], ac-origin[1]
        mh,mw=size(mask)
        for r in range(mh):
            for c in range(mw):
                if mask[r][c]:
                    rr,cc=top+r,left+c
                    if 0<=rr<len(out) and 0<=cc<len(out[0]):
                        if out[rr][cc]==0:
                            out[rr][cc]=color
                        elif out[rr][cc]!=color:
                            out[rr][cc]=9
    return out

RULES = {
    "rule_e113": rule_e113,
    "rule_e114": rule_e114,
    "rule_e115": rule_e115,
    "rule_e116": rule_e116,
    "rule_e117": rule_e117,
    "rule_e118": rule_e118,
    "rule_e119": rule_e119,
    "rule_m113": rule_m113,
    "rule_m114": rule_m114,
    "rule_m115": rule_m115,
    "rule_m116": rule_m116,
    "rule_m117": rule_m117,
    "rule_m118": rule_m118,
    "rule_m119": rule_m119,
    "rule_h113": rule_h113,
    "rule_h114": rule_h114,
    "rule_h115": rule_h115,
    "rule_h116": rule_h116,
    "rule_h117": rule_h117,
    "rule_h118": rule_h118,
    "rule_h119": rule_h119,
}

TASKS = json.loads(r'''
[
  {
    "id": "E113",
    "title": "Neutral Glyph Recolor",
    "difficulty": "easy",
    "skills": [
      "palette mapping",
      "symbolic recoloring",
      "crop output"
    ],
    "suggested_staged_path": "Ignore the absolute colors in the lower motif. Treat 1/2/3 as abstract channels and substitute the palette from the header row.",
    "written_solution": "The top row is a legend. Read its nonzero colors from left to right. The lower 3\u00d73 motif is symbolic: replace every 1 with the first legend color, every 2 with the second, and every 3 with the third, then output only that recolored motif.",
    "program_name": "rule_e113",
    "program_source": "def rule_e113(g):\n    legend = [v for v in g[0] if v != 0]\n    template = [row[1:4] for row in g[2:5]]\n    return palette_lift(template, legend)",
    "train": [
      {
        "input": [
          "47300",
          "00000",
          "00100",
          "01210",
          "00100"
        ],
        "output": [
          "040",
          "474",
          "040"
        ]
      },
      {
        "input": [
          "62500",
          "00000",
          "01000",
          "01200",
          "00030"
        ],
        "output": [
          "600",
          "620",
          "005"
        ]
      },
      {
        "input": [
          "84100",
          "00000",
          "01000",
          "02100",
          "03210"
        ],
        "output": [
          "800",
          "480",
          "148"
        ]
      },
      {
        "input": [
          "73900",
          "00000",
          "01010",
          "01210",
          "00030"
        ],
        "output": [
          "707",
          "737",
          "009"
        ]
      }
    ],
    "test": {
      "input": [
        "26400",
        "00000",
        "01100",
        "00230",
        "00030"
      ],
      "output": [
        "220",
        "064",
        "004"
      ]
    }
  },
  {
    "id": "E114",
    "title": "Diagonal Corners to Rectangle",
    "difficulty": "easy",
    "skills": [
      "rectangle inference",
      "same-size drawing",
      "corner detection"
    ],
    "suggested_staged_path": "Only two nonzero cells matter. Use them as opposite corners of one axis-aligned rectangle.",
    "written_solution": "The two colored markers are opposite corners of a rectangle. Draw the full rectangle outline in the same color, spanning the rows and columns between those markers.",
    "program_name": "rule_e114",
    "program_source": "def rule_e114(g):\n    cells = [(r, c, v) for r, row in enumerate(g) for c, v in enumerate(row) if v != 0]\n    (r0, c0, color), (r1, c1, _) = cells\n    out = blank(*size(g), 0)\n    fill_rect_outline(out, min(r0, r1), min(c0, c1), max(r0, r1), max(c0, c1), color)\n    return out",
    "train": [
      {
        "input": [
          "00000000",
          "04000000",
          "00000000",
          "00000000",
          "00000000",
          "00000040",
          "00000000"
        ],
        "output": [
          "00000000",
          "04444440",
          "04000040",
          "04000040",
          "04000040",
          "04444440",
          "00000000"
        ]
      },
      {
        "input": [
          "003000000",
          "000000000",
          "000000000",
          "000000000",
          "000000030",
          "000000000"
        ],
        "output": [
          "003333330",
          "003000030",
          "003000030",
          "003000030",
          "003333330",
          "000000000"
        ]
      },
      {
        "input": [
          "00000000",
          "00000000",
          "60000000",
          "00000000",
          "00000000",
          "00000000",
          "00000000",
          "00000600"
        ],
        "output": [
          "00000000",
          "00000000",
          "66666600",
          "60000600",
          "60000600",
          "60000600",
          "60000600",
          "66666600"
        ]
      },
      {
        "input": [
          "0000000000",
          "0000200000",
          "0000000000",
          "0000000000",
          "0000000000",
          "0000000000",
          "0000000002",
          "0000000000",
          "0000000000"
        ],
        "output": [
          "0000000000",
          "0000222222",
          "0000200002",
          "0000200002",
          "0000200002",
          "0000200002",
          "0000222222",
          "0000000000",
          "0000000000"
        ]
      }
    ],
    "test": {
      "input": [
        "000000000",
        "007000000",
        "000000000",
        "000000000",
        "000000000",
        "000000070",
        "000000000"
      ],
      "output": [
        "000000000",
        "007777770",
        "007000070",
        "007000070",
        "007000070",
        "007777770",
        "000000000"
      ]
    }
  },
  {
    "id": "E115",
    "title": "Terminal Run Completion",
    "difficulty": "easy",
    "skills": [
      "segment filling",
      "axis alignment",
      "pair matching"
    ],
    "suggested_staged_path": "Look for equal-colored endpoints on a single row or column with only zeroes between them.",
    "written_solution": "Whenever two cells of the same color lie on the same row or the same column and the cells in between are empty, fill the entire straight segment between them in that color.",
    "program_name": "rule_e115",
    "program_source": "def rule_e115(g):\n    out = clone(g)\n    h, w = size(g)\n    for r in range(h):\n        positions = defaultdict(list)\n        for c, v in enumerate(g[r]):\n            if v != 0:\n                positions[v].append(c)\n        for color, cols in positions.items():\n            if len(cols) == 2:\n                c1, c2 = sorted(cols)\n                if all(g[r][c] == 0 for c in range(c1 + 1, c2)):\n                    for c in range(c1, c2 + 1):\n                        out[r][c] = color\n    for c in range(w):\n        positions = defaultdict(list)\n        for r in range(h):\n            v = g[r][c]\n            if v != 0:\n                positions[v].append(r)\n        for color, rows in positions.items():\n            if len(rows) == 2:\n                r1, r2 = sorted(rows)\n                if all(g[r][c] == 0 for r in range(r1 + 1, r2)):\n                    for r in range(r1, r2 + 1):\n                        out[r][c] = color\n    return out",
    "train": [
      {
        "input": [
          "00000040",
          "02000200",
          "00000000",
          "00000000",
          "00000040",
          "00000000",
          "00000000"
        ],
        "output": [
          "00000040",
          "02222240",
          "00000040",
          "00000040",
          "00000040",
          "00000000",
          "00000000"
        ]
      },
      {
        "input": [
          "000000000",
          "000000000",
          "007070000",
          "000000000",
          "000000000",
          "300000300",
          "000000000",
          "000000000"
        ],
        "output": [
          "000000000",
          "000000000",
          "007770000",
          "000000000",
          "000000000",
          "333333300",
          "000000000",
          "000000000"
        ]
      },
      {
        "input": [
          "0000000000",
          "0600000000",
          "0000000000",
          "0000020020",
          "0000000000",
          "0600000000",
          "0000000000"
        ],
        "output": [
          "0000000000",
          "0600000000",
          "0600000000",
          "0600022220",
          "0600000000",
          "0600000000",
          "0000000000"
        ]
      },
      {
        "input": [
          "000000000",
          "400400000",
          "000000050",
          "000000000",
          "000000000",
          "000000000",
          "000000050",
          "000030003",
          "000000000"
        ],
        "output": [
          "000000000",
          "444400000",
          "000000050",
          "000000050",
          "000000050",
          "000000050",
          "000000050",
          "000033333",
          "000000000"
        ]
      }
    ],
    "test": {
      "input": [
        "0000000000",
        "0000000030",
        "0600000600",
        "0000000000",
        "0000000000",
        "0000000030",
        "0000000000",
        "0000000000"
      ],
      "output": [
        "0000000000",
        "0000000030",
        "0666666630",
        "0000000030",
        "0000000030",
        "0000000030",
        "0000000000",
        "0000000000"
      ]
    }
  },
  {
    "id": "E116",
    "title": "Mirror Across the Guide",
    "difficulty": "easy",
    "skills": [
      "reflection",
      "guide detection",
      "same-size copying"
    ],
    "suggested_staged_path": "The solid 8-column is the mirror. Copy the colored object across it.",
    "written_solution": "Find the vertical guide made entirely of color 8. Reflect every nonzero non-guide cell across that guide, keeping the original object and adding its mirror image on the other side.",
    "program_name": "rule_e116",
    "program_source": "def rule_e116(g):\n    h, w = size(g)\n    guide_col = [c for c in range(w) if all(g[r][c] == 8 for r in range(h))][0]\n    out = clone(g)\n    for r in range(h):\n        for c, v in enumerate(g[r]):\n            if v not in (0, 8):\n                mc = 2 * guide_col - c\n                if 0 <= mc < w:\n                    out[r][mc] = v\n    return out",
    "train": [
      {
        "input": [
          "000080000",
          "000080000",
          "030080000",
          "030080000",
          "033380000",
          "000080000",
          "000080000",
          "000080000"
        ],
        "output": [
          "000080000",
          "000080000",
          "030080030",
          "030080030",
          "033383330",
          "000080000",
          "000080000",
          "000080000"
        ]
      },
      {
        "input": [
          "00000800000",
          "00000800000",
          "00000800000",
          "00000804400",
          "00000804400",
          "00000804000",
          "00000800000",
          "00000800000",
          "00000800000"
        ],
        "output": [
          "00000800000",
          "00000800000",
          "00000800000",
          "00440804400",
          "00440804400",
          "00040804000",
          "00000800000",
          "00000800000",
          "00000800000"
        ]
      },
      {
        "input": [
          "0000080000",
          "0222080000",
          "0020080000",
          "0020080000",
          "0000080000",
          "0000080000",
          "0000080000",
          "0000080000"
        ],
        "output": [
          "0000080000",
          "0222080222",
          "0020080020",
          "0020080020",
          "0000080000",
          "0000080000",
          "0000080000",
          "0000080000"
        ]
      },
      {
        "input": [
          "00000800000",
          "00000800000",
          "00000800000",
          "00000800000",
          "00000800660",
          "00000806600",
          "00000806000",
          "00000800000",
          "00000800000",
          "00000800000"
        ],
        "output": [
          "00000800000",
          "00000800000",
          "00000800000",
          "00000800000",
          "06600800660",
          "00660806600",
          "00060806000",
          "00000800000",
          "00000800000",
          "00000800000"
        ]
      }
    ],
    "test": {
      "input": [
        "000080000",
        "000080000",
        "070780000",
        "070780000",
        "077780000",
        "000080000",
        "000080000",
        "000080000",
        "000080000"
      ],
      "output": [
        "000080000",
        "000080000",
        "070787070",
        "070787070",
        "077787770",
        "000080000",
        "000080000",
        "000080000",
        "000080000"
      ]
    }
  },
  {
    "id": "E117",
    "title": "Seeded Interior Fill",
    "difficulty": "easy",
    "skills": [
      "frame detection",
      "region filling",
      "color transfer"
    ],
    "suggested_staged_path": "The repeated border color marks the container. The single interior seed gives the fill color.",
    "written_solution": "Identify the rectangular frame. Leave the frame unchanged and fill every empty interior cell with the color of the single non-frame seed cell inside it.",
    "program_name": "rule_e117",
    "program_source": "def rule_e117(g):\n    out = clone(g)\n    counts = Counter(v for row in g for v in row if v != 0)\n    frame_color = max(counts, key=lambda c: counts[c])\n    frame_cells = [(r, c) for r, row in enumerate(g) for c, v in enumerate(row) if v == frame_color]\n    r0, c0, r1, c1 = bbox(frame_cells)\n    seed_color = [v for row in g for v in row if v not in (0, frame_color)][0]\n    for r in range(r0 + 1, r1):\n        for c in range(c0 + 1, c1):\n            if out[r][c] == 0:\n                out[r][c] = seed_color\n    return out",
    "train": [
      {
        "input": [
          "000000000",
          "044444440",
          "040000040",
          "040030040",
          "040000040",
          "040000040",
          "044444440",
          "000000000"
        ],
        "output": [
          "000000000",
          "044444440",
          "043333340",
          "043333340",
          "043333340",
          "043333340",
          "044444440",
          "000000000"
        ]
      },
      {
        "input": [
          "0000000000",
          "0000000000",
          "0066666660",
          "0060000060",
          "0060002060",
          "0060000060",
          "0060000060",
          "0066666660",
          "0000000000"
        ],
        "output": [
          "0000000000",
          "0000000000",
          "0066666660",
          "0062222260",
          "0062222260",
          "0062222260",
          "0062222260",
          "0066666660",
          "0000000000"
        ]
      },
      {
        "input": [
          "00000000",
          "00077770",
          "00070070",
          "00075070",
          "00070070",
          "00077770",
          "00000000"
        ],
        "output": [
          "00000000",
          "00077770",
          "00075570",
          "00075570",
          "00075570",
          "00077770",
          "00000000"
        ]
      },
      {
        "input": [
          "0000000000",
          "0000000000",
          "0333333330",
          "0300000030",
          "0300000030",
          "0300090030",
          "0300000030",
          "0300000030",
          "0333333330",
          "0000000000"
        ],
        "output": [
          "0000000000",
          "0000000000",
          "0333333330",
          "0399999930",
          "0399999930",
          "0399999930",
          "0399999930",
          "0399999930",
          "0333333330",
          "0000000000"
        ]
      }
    ],
    "test": {
      "input": [
        "000000000",
        "005555500",
        "005000500",
        "005000500",
        "005040500",
        "005000500",
        "005000500",
        "005555500",
        "000000000"
      ],
      "output": [
        "000000000",
        "005555500",
        "005444500",
        "005444500",
        "005444500",
        "005444500",
        "005444500",
        "005555500",
        "000000000"
      ]
    }
  },
  {
    "id": "E118",
    "title": "Crop the Largest Object",
    "difficulty": "easy",
    "skills": [
      "component analysis",
      "ranking by area",
      "bbox crop"
    ],
    "suggested_staged_path": "Ignore background and compare connected components by size first, then by top-left position if needed.",
    "written_solution": "Find all connected colored objects. Choose the largest one by area; if there is a tie, take the uppermost then leftmost. Output the tight crop of that object.",
    "program_name": "rule_e118",
    "program_source": "def rule_e118(g):\n    comps = components_color(g)\n    scored = []\n    for comp in comps:\n        area = len(comp[\"cells\"])\n        r0, c0, _, _ = bbox(comp[\"cells\"])\n        scored.append((-area, r0, c0, comp))\n    best = sorted(scored, key=lambda t: t[:3])[0][3]\n    return crop_bbox(g, best[\"cells\"])",
    "train": [
      {
        "input": [
          "0000000000",
          "0200000000",
          "0200006600",
          "0222006600",
          "0000046400",
          "0000040400",
          "0000044400",
          "0000000000",
          "0000000000"
        ],
        "output": [
          "464",
          "404",
          "444"
        ]
      },
      {
        "input": [
          "000000000000",
          "003300000000",
          "000300000000",
          "033300000000",
          "000000000000",
          "000000770000",
          "002220707700",
          "002000777000",
          "002000000000",
          "000000000000"
        ],
        "output": [
          "7700",
          "7077",
          "7770"
        ]
      },
      {
        "input": [
          "00000000000",
          "00000008800",
          "00000008800",
          "00000008000",
          "05050000000",
          "05050000000",
          "05550003330",
          "00000000300",
          "00000000300"
        ],
        "output": [
          "505",
          "505",
          "555"
        ]
      },
      {
        "input": [
          "000000000000",
          "000000000000",
          "004400000000",
          "044000000000",
          "040000000000",
          "000000666000",
          "009000606000",
          "009000660000",
          "009990060000",
          "000000000000"
        ],
        "output": [
          "666",
          "606",
          "660",
          "060"
        ]
      }
    ],
    "test": {
      "input": [
        "000000000000",
        "020200000000",
        "020200000000",
        "022200000000",
        "000000000000",
        "000000077000",
        "044000007000",
        "044000777000",
        "040000000000",
        "000000000000"
      ],
      "output": [
        "202",
        "202",
        "222"
      ]
    }
  },
  {
    "id": "E119",
    "title": "Frequency Strip",
    "difficulty": "easy",
    "skills": [
      "counting",
      "sorting",
      "symbolic output"
    ],
    "suggested_staged_path": "The output is not spatial. It is a compact count summary.",
    "written_solution": "Count how many times each nonzero color appears. Sort colors by descending count and break ties by smaller color number. Output a single row where each color is repeated exactly its count.",
    "program_name": "rule_e119",
    "program_source": "def rule_e119(g):\n    counts = Counter(v for row in g for v in row if v != 0)\n    order = sorted(counts.items(), key=lambda kv: (-kv[1], kv[0]))\n    row = []\n    for color, count in order:\n        row.extend([color] * count)\n    return [row]",
    "train": [
      {
        "input": [
          "0400007",
          "0400000",
          "0020000",
          "2000000",
          "0000002"
        ],
        "output": [
          "222447"
        ]
      },
      {
        "input": [
          "30000003",
          "00006000",
          "00300000",
          "00000000",
          "08000000",
          "80000300"
        ],
        "output": [
          "3333886"
        ]
      },
      {
        "input": [
          "000000900",
          "050000050",
          "000050000",
          "000000000",
          "001000000",
          "000000001"
        ],
        "output": [
          "555119"
        ]
      },
      {
        "input": [
          "2000004",
          "0002000",
          "0000002",
          "0007000",
          "0000000",
          "0000020",
          "4000000"
        ],
        "output": [
          "2222447"
        ]
      }
    ],
    "test": {
      "input": [
        "00600000",
        "00000030",
        "00600000",
        "05000000",
        "00600000",
        "00000003"
      ],
      "output": [
        "666335"
      ]
    }
  },
  {
    "id": "M113",
    "title": "Palette-Lift Strip Assembly",
    "difficulty": "medium",
    "skills": [
      "palette lifting",
      "bank parsing",
      "strip assembly"
    ],
    "suggested_staged_path": "Read the palette first, then the selector strip, then the keyed neutral block bank.",
    "written_solution": "The first row supplies a three-color palette. The second row is an ordered selector of keyed blocks. The lower bank maps each key to a 2\u00d72 neutral block whose values 1/2/3 are symbolic. Recolor each selected block with the palette, then concatenate the recolored blocks in selector order.",
    "program_name": "rule_m113",
    "program_source": "def rule_m113(g):\n    legend = [v for v in g[0] if v != 0]\n    selector = [v for v in g[1] if v != 0]\n    bank = {}\n    c = 0\n    while c < len(g[0]):\n        if g[3][c] != 0:\n            key = g[3][c]\n            bank[key] = [row[c:c+2] for row in g[4:6]]\n            c += 3\n        else:\n            c += 1\n    blocks = [palette_lift(bank[key], legend) for key in selector]\n    return concat_h(blocks, sep=0)",
    "train": [
      {
        "input": [
          "47300000",
          "21300000",
          "00000000",
          "10020030",
          "10012001",
          "21003023"
        ],
        "output": [
          "474004",
          "037473"
        ]
      },
      {
        "input": [
          "62500000",
          "33120000",
          "00000000",
          "10020030",
          "30010012",
          "21021003"
        ],
        "output": [
          "62625060",
          "05052626"
        ]
      },
      {
        "input": [
          "84100000",
          "12100000",
          "00000000",
          "10020030",
          "12030001",
          "03021023"
        ],
        "output": [
          "841084",
          "014801"
        ]
      },
      {
        "input": [
          "73900000",
          "23120000",
          "00000000",
          "10020030",
          "01012030",
          "23003021"
        ],
        "output": [
          "73900773",
          "09373909"
        ]
      }
    ],
    "test": {
      "input": [
        "26400000",
        "13200000",
        "00000000",
        "10020030",
        "10030012",
        "21021003"
      ],
      "output": [
        "202640",
        "620462"
      ]
    }
  },
  {
    "id": "M114",
    "title": "Commanded Crop Transform",
    "difficulty": "medium",
    "skills": [
      "command decoding",
      "object crop",
      "geometric transforms"
    ],
    "suggested_staged_path": "The only thing outside the object is the command cell.",
    "written_solution": "Read the command in the top-left cell. Crop the single object from the rest of the grid and apply the corresponding transform: 1=rot90, 2=rot180, 3=rot270, 4=flip horizontally, 5=flip vertically.",
    "program_name": "rule_m114",
    "program_source": "def rule_m114(g):\n    cmd = g[0][0]\n    cells = [(r, c) for r, row in enumerate(g) for c, v in enumerate(row) if v != 0 and not (r == 0 and c == 0)]\n    obj = crop_bbox(g, cells)\n    return apply_transform(obj, cmd)",
    "train": [
      {
        "input": [
          "100000000",
          "000000000",
          "000000000",
          "000023000",
          "000020300",
          "000022200",
          "000000000",
          "000000000"
        ],
        "output": [
          "222",
          "203",
          "230"
        ]
      },
      {
        "input": [
          "200000000",
          "000000000",
          "000000000",
          "000450000",
          "000440000",
          "000405000",
          "000000000",
          "000000000"
        ],
        "output": [
          "504",
          "044",
          "054"
        ]
      },
      {
        "input": [
          "300000000",
          "000000000",
          "000006070",
          "000000600",
          "000007600",
          "000000000",
          "000000000",
          "000000000"
        ],
        "output": [
          "607",
          "066",
          "700"
        ]
      },
      {
        "input": [
          "400000000",
          "000000000",
          "000000000",
          "000000000",
          "002300000",
          "002030000",
          "002220000",
          "000000000"
        ],
        "output": [
          "032",
          "302",
          "222"
        ]
      }
    ],
    "test": {
      "input": [
        "200000000",
        "000000000",
        "000000000",
        "000060700",
        "000006000",
        "000076000",
        "000000000",
        "000000000"
      ],
      "output": [
        "067",
        "060",
        "706"
      ]
    }
  },
  {
    "id": "M115",
    "title": "Chamber Majority Flood",
    "difficulty": "medium",
    "skills": [
      "region partitioning",
      "majority vote",
      "wall-aware filling"
    ],
    "suggested_staged_path": "The 8-walls divide the board into chambers. Each chamber decides its fill color locally.",
    "written_solution": "Treat color 8 as walls. Each enclosed chamber contains a few colored seeds. Determine the majority nonzero seed color inside each chamber and fill all empty cells of that chamber with that majority color, keeping walls and original seeds unchanged.",
    "program_name": "rule_m115",
    "program_source": "def rule_m115(g):\n    out = clone(g)\n    for region in flood_regions_not_wall(g, wall=8):\n        colors = [g[r][c] for r, c in region if g[r][c] not in (0, 8)]\n        if not colors:\n            continue\n        majority = sorted(Counter(colors).items(), key=lambda kv: (-kv[1], kv[0]))[0][0]\n        for r, c in region:\n            if out[r][c] == 0:\n                out[r][c] = majority\n    return out",
    "train": [
      {
        "input": [
          "88888888888",
          "82000830008",
          "80200800308",
          "84000806008",
          "88888888888",
          "80700810008",
          "87070805008",
          "80000800108",
          "88888888888"
        ],
        "output": [
          "88888888888",
          "82222833338",
          "82222833338",
          "84222836338",
          "88888888888",
          "87777811118",
          "87777815118",
          "87777811118",
          "88888888888"
        ]
      },
      {
        "input": [
          "88888888888",
          "84000806008",
          "80400800608",
          "80040820008",
          "88888888888",
          "83000800508",
          "80070805008",
          "80300810008",
          "88888888888"
        ],
        "output": [
          "88888888888",
          "84444866668",
          "84444866668",
          "84444826668",
          "88888888888",
          "83333855558",
          "83373855558",
          "83333815558",
          "88888888888"
        ]
      },
      {
        "input": [
          "88888888888",
          "80020890008",
          "82000804008",
          "80060800908",
          "88888888888",
          "80300870008",
          "85000800708",
          "80300802008",
          "88888888888"
        ],
        "output": [
          "88888888888",
          "82222899998",
          "82222894998",
          "82262899998",
          "88888888888",
          "83333877778",
          "85333877778",
          "83333872778",
          "88888888888"
        ]
      },
      {
        "input": [
          "88888888888",
          "80010802008",
          "81000800208",
          "80400860008",
          "88888888888",
          "85000800308",
          "80500890008",
          "80050803008",
          "88888888888"
        ],
        "output": [
          "88888888888",
          "81111822228",
          "81111822228",
          "81411862228",
          "88888888888",
          "85555833338",
          "85555893338",
          "85555833338",
          "88888888888"
        ]
      }
    ],
    "test": {
      "input": [
        "88888888888",
        "86000800408",
        "80600804008",
        "80020870008",
        "88888888888",
        "80300850008",
        "83000800508",
        "80090801008",
        "88888888888"
      ],
      "output": [
        "88888888888",
        "86666844448",
        "86666844448",
        "86626874448",
        "88888888888",
        "83333855558",
        "83333855558",
        "83393851558",
        "88888888888"
      ]
    }
  },
  {
    "id": "M116",
    "title": "Area\u2013Hole Relation Matrix",
    "difficulty": "medium",
    "skills": [
      "panel parsing",
      "shape statistics",
      "relational output"
    ],
    "suggested_staged_path": "Each panel gives one object; the output compares every object with every other.",
    "written_solution": "Split the input into three object panels. For each object compute its area and number of holes. Output a 3\u00d73 relation matrix: diagonal cells are 5; use 6 if two objects share both area and hole count, 2 if they share only area, 3 if they share only hole count, and 0 otherwise.",
    "program_name": "rule_m116",
    "program_source": "def rule_m116(g):\n    panels = [crop_nonzero(p) for p in panel_split_horizontal(g)]\n    info = []\n    for p in panels:\n        area = shape_area(p)\n        holes = count_holes_binary([[1 if v != 0 else 0 for v in row] for row in p])\n        info.append((area, holes))\n    n = len(info)\n    out = blank(n, n, 0)\n    for i, (ai, hi) in enumerate(info):\n        for j, (aj, hj) in enumerate(info):\n            out[i][j] = relation_color(ai, hi, aj, hj, same_self=(i == j))\n    return out",
    "train": [
      {
        "input": [
          "222030304400",
          "202030304044",
          "222033304440"
        ],
        "output": [
          "506",
          "050",
          "605"
        ]
      },
      {
        "input": [
          "500066607777",
          "500006007007",
          "555006007007",
          "000000007777"
        ],
        "output": [
          "560",
          "650",
          "005"
        ]
      },
      {
        "input": [
          "0220044088",
          "0020440088",
          "2220400080"
        ],
        "output": [
          "533",
          "356",
          "365"
        ]
      },
      {
        "input": [
          "330006660099",
          "303306060009",
          "333006660999"
        ],
        "output": [
          "560",
          "650",
          "005"
        ]
      }
    ],
    "test": {
      "input": [
        "2000440777",
        "2000440707",
        "2220400777"
      ],
      "output": [
        "560",
        "650",
        "005"
      ]
    }
  },
  {
    "id": "M117",
    "title": "Ranked Component Selection",
    "difficulty": "medium",
    "skills": [
      "component metrics",
      "command routing",
      "crop output"
    ],
    "suggested_staged_path": "The command chooses a ranking rule, not a color.",
    "written_solution": "Ignore the top-left command cell and analyze the remaining colored objects. Command 1 selects the smallest-area component, 2 the largest-area component, 3 the widest component, and 4 the tallest component. Output the tight crop of the selected component.",
    "program_name": "rule_m117",
    "program_source": "def rule_m117(g):\n    cmd = g[0][0]\n    g2 = clone(g)\n    g2[0][0] = 0\n    comp = choose_component_by_cmd(components_color(g2), cmd)\n    return crop_bbox(g2, comp[\"cells\"])",
    "train": [
      {
        "input": [
          "100000000000",
          "002000000000",
          "002000000000",
          "002220000000",
          "000000404000",
          "066000404000",
          "060660444000",
          "066600000000",
          "000000000000",
          "000000000000"
        ],
        "output": [
          "200",
          "200",
          "222"
        ]
      },
      {
        "input": [
          "200000000000",
          "000000003300",
          "000000033000",
          "000000030000",
          "055000000000",
          "050550000000",
          "055500007700",
          "000000007700",
          "000000007000",
          "000000000000"
        ],
        "output": [
          "5500",
          "5055",
          "5550"
        ]
      },
      {
        "input": [
          "3000000000000",
          "0020000000000",
          "0020000000000",
          "0022200000000",
          "0000000044000",
          "0000000004000",
          "0606000444000",
          "0606000000000",
          "0666000000000",
          "0000000000000"
        ],
        "output": [
          "606",
          "606",
          "666"
        ]
      },
      {
        "input": [
          "400000000000",
          "000000222000",
          "000000020000",
          "000000020000",
          "040000000000",
          "040000077700",
          "044400070700",
          "000000077000",
          "000000007000",
          "000000000000"
        ],
        "output": [
          "777",
          "707",
          "770",
          "070"
        ]
      }
    ],
    "test": {
      "input": [
        "200000000000",
        "033000000000",
        "033000000000",
        "030000000000",
        "000000606000",
        "022200606000",
        "020200666000",
        "022000000000",
        "002000000000",
        "000000000000"
      ],
      "output": [
        "222",
        "202",
        "220",
        "020"
      ]
    }
  },
  {
    "id": "M118",
    "title": "Anchor Copies with Overlap",
    "difficulty": "medium",
    "skills": [
      "prototype extraction",
      "relative translation",
      "overlap handling"
    ],
    "suggested_staged_path": "There is one full prototype containing an origin 8, and the other 8s are target origins.",
    "written_solution": "Find the connected prototype that contains color 8; that 8 marks the prototype origin. Copy the whole prototype so that its origin lands on every other 8 in the grid as well as on its original location. Overlay all copies in the original canvas. If two copies write different nonzero colors to the same cell, mark the overlap as 9.",
    "program_name": "rule_m118",
    "program_source": "def rule_m118(g):\n    template, origin, anchors = find_prototype_and_anchors(g)\n    return overlay_template_copies_same_size(template, origin, anchors, size(g), overlap_color=9)",
    "train": [
      {
        "input": [
          "0000000000",
          "0820000000",
          "0220000080",
          "0023000000",
          "0000000000",
          "0000008000",
          "0000000000",
          "0000000000",
          "0000000000"
        ],
        "output": [
          "0000000000",
          "0820000000",
          "0220000082",
          "0023000022",
          "0000000002",
          "0000008200",
          "0000002200",
          "0000000230",
          "0000000000"
        ]
      },
      {
        "input": [
          "00000000000",
          "00082000000",
          "00222000000",
          "00030000000",
          "00000000000",
          "00000800000",
          "00000080000",
          "00000000000",
          "00000000000",
          "00000000000"
        ],
        "output": [
          "00000000000",
          "00082000000",
          "00222000000",
          "00030000000",
          "00000000000",
          "00000820000",
          "00002292000",
          "00000922000",
          "00000030000",
          "00000000000"
        ]
      },
      {
        "input": [
          "000000000000",
          "000000000000",
          "028000000800",
          "020300000000",
          "023000000000",
          "000000080000",
          "000000000080",
          "000000000000",
          "000000000000"
        ],
        "output": [
          "000000000000",
          "000000000000",
          "028000002800",
          "020000002000",
          "023000002300",
          "000000280000",
          "000000200280",
          "000000230200",
          "000000000230"
        ]
      },
      {
        "input": [
          "0000000000",
          "0000000800",
          "0000000000",
          "0008200000",
          "0002200000",
          "0000230000",
          "0080000000",
          "0000000000",
          "0000000000",
          "0000000000"
        ],
        "output": [
          "0000000000",
          "0000000820",
          "0000000220",
          "0008200023",
          "0002200000",
          "0000230000",
          "0082000000",
          "0022000000",
          "0002300000",
          "0000000000"
        ]
      }
    ],
    "test": {
      "input": [
        "00000000000",
        "00000000000",
        "00820000800",
        "02220000000",
        "00300000000",
        "00000000000",
        "00000080000",
        "00000000800",
        "00000000000",
        "00000000000"
      ],
      "output": [
        "00000000000",
        "00000000000",
        "00820000820",
        "02220002220",
        "00300000300",
        "00000000000",
        "00000082000",
        "00000222820",
        "00000032220",
        "00000000300"
      ]
    }
  },
  {
    "id": "M119",
    "title": "Select a Panel, Then Transform It",
    "difficulty": "medium",
    "skills": [
      "panel indexing",
      "command decoding",
      "crop and transform"
    ],
    "suggested_staged_path": "The first header value chooses which panel; the second chooses how to transform it.",
    "written_solution": "Below the header are multiple zero-separated panels. The first header number selects which panel to use (1-based). Crop that panel tightly and apply the transform given by the second header number using the same command code as in the commanded-crop task.",
    "program_name": "rule_m119",
    "program_source": "def rule_m119(g):\n    which = g[0][0]\n    cmd = g[0][1]\n    panels = panel_split_horizontal(g[1:])\n    panel = crop_nonzero(panels[which - 1])\n    return apply_transform(panel, cmd)",
    "train": [
      {
        "input": [
          "1100000000",
          "2000404066",
          "2000404066",
          "2220444060"
        ],
        "output": [
          "222",
          "200",
          "200"
        ]
      },
      {
        "input": [
          "220000000000",
          "333055000077",
          "030050550770",
          "030055500700"
        ],
        "output": [
          "0555",
          "5505",
          "0055"
        ]
      },
      {
        "input": [
          "34000000000",
          "02208000606",
          "00208000606",
          "22208880666"
        ],
        "output": [
          "606",
          "606",
          "666"
        ]
      },
      {
        "input": [
          "25000000000",
          "44002207700",
          "44022007077",
          "40020007770"
        ],
        "output": [
          "200",
          "220",
          "022"
        ]
      }
    ],
    "test": {
      "input": [
        "320000000000",
        "666030005500",
        "060030005055",
        "060033305550"
      ],
      "output": [
        "0555",
        "5505",
        "0055"
      ]
    }
  },
  {
    "id": "H113",
    "title": "Palette-Lift Matrix with Commands",
    "difficulty": "hard",
    "skills": [
      "palette lifting",
      "matrix assembly",
      "per-slot transforms"
    ],
    "suggested_staged_path": "There are three layers of control: palette, selector matrix, and command matrix.",
    "written_solution": "The top row is a three-color palette. The next 2\u00d72 block chooses which keyed neutral 3\u00d73 template to place in each output slot. The following 2\u00d72 command block tells how to transform each chosen template. Recolor every chosen template with the palette, apply its local transform, and assemble the four resulting 3\u00d73 blocks into a 2\u00d72 output matrix.",
    "program_name": "rule_h113",
    "program_source": "def rule_h113(g):\n    legend = [v for v in g[0] if v != 0]\n    selector = [[g[1 + r][c] for c in range(2)] for r in range(2)]\n    commands = [[g[3 + r][c] for c in range(2)] for r in range(2)]\n    bank = {}\n    c = 0\n    while c < len(g[0]):\n        if g[6][c] != 0:\n            key = g[6][c]\n            bank[key] = [row[c:c+3] for row in g[7:10]]\n            c += 4\n        else:\n            c += 1\n    rows = []\n    for r in range(2):\n        blocks = []\n        for c in range(2):\n            block = palette_lift(bank[selector[r][c]], legend, transform=commands[r][c])\n            blocks.append(block)\n        rows.append(concat_h(blocks, sep=0))\n    return concat_v(rows, sep=0)",
    "train": [
      {
        "input": [
          "47300000000",
          "12000000000",
          "31000000000",
          "01000000000",
          "42000000000",
          "00000000000",
          "10002000300",
          "01001000100",
          "12101200210",
          "01000030321"
        ],
        "output": [
          "040044",
          "474070",
          "040300",
          "004040",
          "047474",
          "473040"
        ]
      },
      {
        "input": [
          "62500000000",
          "23000000000",
          "12000000000",
          "30000000000",
          "15000000000",
          "00000000000",
          "10002000300",
          "11001010100",
          "02301210120",
          "00300030003"
        ],
        "output": [
          "660600",
          "020620",
          "665005",
          "006005",
          "026626",
          "550606"
        ]
      },
      {
        "input": [
          "84100000000",
          "31000000000",
          "23000000000",
          "24000000000",
          "01000000000",
          "00000000000",
          "10002000300",
          "10000100110",
          "21001210023",
          "32100100003"
        ],
        "output": [
          "100008",
          "140084",
          "088841",
          "080008",
          "848048",
          "080110"
        ]
      },
      {
        "input": [
          "73900000000",
          "13000000000",
          "21000000000",
          "52000000000",
          "10000000000",
          "00000000000",
          "10002000300",
          "10101000010",
          "12101200121",
          "00300030010"
        ],
        "output": [
          "009070",
          "737737",
          "707070",
          "077707",
          "030737",
          "900009"
        ]
      }
    ],
    "test": {
      "input": [
        "26400000000",
        "21000000000",
        "32000000000",
        "04000000000",
        "31000000000",
        "00000000000",
        "10002000300",
        "11001000101",
        "02302100121",
        "00303210003"
      ],
      "output": [
        "200022",
        "620460",
        "462400",
        "220462",
        "060620",
        "224200"
      ]
    }
  },
  {
    "id": "H114",
    "title": "Panel Analogy Transform",
    "difficulty": "hard",
    "skills": [
      "analogy",
      "transform inference",
      "panel transfer"
    ],
    "suggested_staged_path": "Use the first two panels to discover one transform, then reuse it on the third panel.",
    "written_solution": "The first panel becomes the second by one geometric transform. Infer which transform from the examples among identity, rotations, and flips. Then apply exactly the same transform to the third panel and output the transformed crop.",
    "program_name": "rule_h114",
    "program_source": "def rule_h114(g):\n    a, b, c = [crop_nonzero(p) for p in panel_split_horizontal(g)]\n    cmd = None\n    for _, fn, code in TRANSFORMS:\n        if fn(a) == b:\n            cmd = code\n            break\n    return apply_transform(c, cmd)",
    "train": [
      {
        "input": [
          "20002220404",
          "20002000404",
          "22202000444"
        ],
        "output": [
          "444",
          "400",
          "444"
        ]
      },
      {
        "input": [
          "330030066",
          "330330006",
          "300330666"
        ],
        "output": [
          "666",
          "600",
          "660"
        ]
      },
      {
        "input": [
          "05505500700",
          "55000550700",
          "50000050777"
        ],
        "output": [
          "777",
          "700",
          "700"
        ]
      },
      {
        "input": [
          "2200022200888",
          "2022020220080",
          "2220022000080"
        ],
        "output": [
          "080",
          "080",
          "888"
        ]
      }
    ],
    "test": {
      "input": [
        "30303330066",
        "30303030660",
        "33303030600"
      ],
      "output": [
        "006",
        "066",
        "660"
      ]
    }
  },
  {
    "id": "H115",
    "title": "Voronoi Frame Fill",
    "difficulty": "hard",
    "skills": [
      "distance reasoning",
      "partitioning",
      "tie handling"
    ],
    "suggested_staged_path": "Each empty interior cell belongs to its nearest seed. Ties are special.",
    "written_solution": "Inside the 8-frame are several colored seed cells. Fill every empty interior cell with the color of its nearest seed by Manhattan distance. If a cell is equally close to at least two seeds, color it 5 instead.",
    "program_name": "rule_h115",
    "program_source": "def rule_h115(g):\n    out = clone(g)\n    h, w = size(g)\n    seeds = [(r, c, v) for r, row in enumerate(g) for c, v in enumerate(row) if v not in (0, 8)]\n    for r in range(1, h - 1):\n        for c in range(1, w - 1):\n            if g[r][c] == 0:\n                dists = sorted((manhattan((r, c), (sr, sc)), color) for sr, sc, color in seeds)\n                out[r][c] = 5 if len(dists) > 1 and dists[0][0] == dists[1][0] else dists[0][1]\n    return out",
    "train": [
      {
        "input": [
          "888888888",
          "800000708",
          "802000008",
          "800000008",
          "800000408",
          "800000008",
          "888888888"
        ],
        "output": [
          "888888888",
          "822277778",
          "822227778",
          "822254448",
          "822544448",
          "822544448",
          "888888888"
        ]
      },
      {
        "input": [
          "88888888",
          "83000008",
          "80000008",
          "80000008",
          "80000008",
          "80000608",
          "80000008",
          "88888888"
        ],
        "output": [
          "88888888",
          "83333558",
          "83335668",
          "83356668",
          "83566668",
          "85666668",
          "85666668",
          "88888888"
        ]
      },
      {
        "input": [
          "8888888888",
          "8000000008",
          "8000000208",
          "8000000008",
          "8000090008",
          "8000000008",
          "8050000008",
          "8000000008",
          "8888888888"
        ],
        "output": [
          "8888888888",
          "8555552228",
          "8555552228",
          "8559995228",
          "8559999558",
          "8555999558",
          "8555599558",
          "8555599558",
          "8888888888"
        ]
      },
      {
        "input": [
          "888888888",
          "800000408",
          "800000008",
          "800020008",
          "800000008",
          "807000008",
          "800000008",
          "888888888"
        ],
        "output": [
          "888888888",
          "855554448",
          "855225448",
          "855222558",
          "877522558",
          "877755558",
          "877755558",
          "888888888"
        ]
      }
    ],
    "test": {
      "input": [
        "888888888",
        "800000008",
        "806000308",
        "800000008",
        "800000008",
        "800000008",
        "800070008",
        "800000008",
        "888888888"
      ],
      "output": [
        "888888888",
        "866653338",
        "866653338",
        "866653338",
        "866575338",
        "855777558",
        "877777778",
        "877777778",
        "888888888"
      ]
    }
  },
  {
    "id": "H116",
    "title": "Nested Frame Depth Recolor",
    "difficulty": "hard",
    "skills": [
      "nesting",
      "component ordering",
      "depth mapping"
    ],
    "suggested_staged_path": "All input frames start the same color, so depth is the only thing that changes.",
    "written_solution": "The input consists of nested rectangular outlines, all in color 1. Order the frames from outermost to innermost by bounding-box area. Recolor them by depth using the fixed palette: depth 1\u21922, depth 2\u21924, depth 3\u21926, depth 4\u21927, depth 5\u21923, depth 6\u21929.",
    "program_name": "rule_h116",
    "program_source": "def rule_h116(g):\n    frames = [comp for comp in components_color(g) if comp[\"color\"] == 1]\n    scored = []\n    for comp in frames:\n        r0, c0, r1, c1 = bbox(comp[\"cells\"])\n        area = (r1 - r0 + 1) * (c1 - c0 + 1)\n        scored.append((-area, r0, c0, comp))\n    ordered = [t[3] for t in sorted(scored, key=lambda t: t[:3])]\n    out = blank(*size(g), 0)\n    for depth, comp in enumerate(ordered):\n        color = depth_palette[depth]\n        for r, c in comp[\"cells\"]:\n            out[r][c] = color\n    return out",
    "train": [
      {
        "input": [
          "11111111111",
          "10000000001",
          "10111111101",
          "10100000101",
          "10101110101",
          "10101010101",
          "10101110101",
          "10100000101",
          "10111111101",
          "10000000001",
          "11111111111"
        ],
        "output": [
          "22222222222",
          "20000000002",
          "20444444402",
          "20400000402",
          "20406660402",
          "20406060402",
          "20406660402",
          "20400000402",
          "20444444402",
          "20000000002",
          "22222222222"
        ]
      },
      {
        "input": [
          "0111111111110",
          "0100000000010",
          "0101111111010",
          "0101000001010",
          "0101000001010",
          "0101000001010",
          "0101111111010",
          "0100000000010",
          "0111111111110"
        ],
        "output": [
          "0222222222220",
          "0200000000020",
          "0204444444020",
          "0204000004020",
          "0204000004020",
          "0204000004020",
          "0204444444020",
          "0200000000020",
          "0222222222220"
        ]
      },
      {
        "input": [
          "1111111111111",
          "1000000000001",
          "1011111111101",
          "1010000000101",
          "1010111110101",
          "1010111110101",
          "1010110110101",
          "1010111110101",
          "1010111110101",
          "1010000000101",
          "1011111111101",
          "1000000000001",
          "1111111111111"
        ],
        "output": [
          "2222222222222",
          "2000000000002",
          "2044444444402",
          "2040000000402",
          "2040666660402",
          "2040666660402",
          "2040660660402",
          "2040666660402",
          "2040666660402",
          "2040000000402",
          "2044444444402",
          "2000000000002",
          "2222222222222"
        ]
      },
      {
        "input": [
          "000000000000",
          "011111111110",
          "010000000010",
          "010111111010",
          "010100001010",
          "010100001010",
          "010111111010",
          "010000000010",
          "011111111110",
          "000000000000"
        ],
        "output": [
          "000000000000",
          "022222222220",
          "020000000020",
          "020444444020",
          "020400004020",
          "020400004020",
          "020444444020",
          "020000000020",
          "022222222220",
          "000000000000"
        ]
      }
    ],
    "test": {
      "input": [
        "111111111111",
        "100000000001",
        "101111111101",
        "101000000101",
        "101011110101",
        "101010010101",
        "101010010101",
        "101011110101",
        "101000000101",
        "101111111101",
        "100000000001",
        "111111111111"
      ],
      "output": [
        "222222222222",
        "200000000002",
        "204444444402",
        "204000000402",
        "204066660402",
        "204060060402",
        "204060060402",
        "204066660402",
        "204000000402",
        "204444444402",
        "200000000002",
        "222222222222"
      ]
    }
  },
  {
    "id": "H117",
    "title": "Compose Two Commands",
    "difficulty": "hard",
    "skills": [
      "command composition",
      "transform sequencing",
      "crop output"
    ],
    "suggested_staged_path": "Do not collapse the header to one code. Apply the first command, then the second.",
    "written_solution": "Crop the single object beneath the two-cell header. Interpret the first header number as one transform command and the second as another. Apply the first transform to the cropped object and then apply the second transform to that intermediate result.",
    "program_name": "rule_h117",
    "program_source": "def rule_h117(g):\n    cmd1, cmd2 = g[0][0], g[0][1]\n    cells = [(r, c) for r, row in enumerate(g) for c, v in enumerate(row) if v != 0 and not (r == 0 and c in (0, 1))]\n    obj = crop_bbox(g, cells)\n    return apply_transform(apply_transform(obj, cmd1), cmd2)",
    "train": [
      {
        "input": [
          "140000000",
          "000000000",
          "000000000",
          "000230000",
          "000203000",
          "000222000",
          "000000000",
          "000000000"
        ],
        "output": [
          "222",
          "302",
          "032"
        ]
      },
      {
        "input": [
          "210000000",
          "000000000",
          "000045000",
          "000044000",
          "000040500",
          "000000000",
          "000000000",
          "000000000"
        ],
        "output": [
          "005",
          "540",
          "444"
        ]
      },
      {
        "input": [
          "530000000",
          "000000000",
          "000000000",
          "000607000",
          "000060000",
          "000760000",
          "000000000",
          "000000000"
        ],
        "output": [
          "706",
          "660",
          "007"
        ]
      },
      {
        "input": [
          "420000000",
          "000000000",
          "000000000",
          "000000000",
          "002300000",
          "002030000",
          "002220000",
          "000000000"
        ],
        "output": [
          "222",
          "203",
          "230"
        ]
      }
    ],
    "test": {
      "input": [
        "340000000",
        "000000000",
        "000000000",
        "000450000",
        "000440000",
        "000405000",
        "000000000",
        "000000000"
      ],
      "output": [
        "444",
        "045",
        "500"
      ]
    }
  },
  {
    "id": "H118",
    "title": "Transform-Equivalence Matrix",
    "difficulty": "hard",
    "skills": [
      "shape normalization",
      "dihedral equivalence",
      "relational matrix"
    ],
    "suggested_staged_path": "Two panels count as equivalent if one shape can be rotated or flipped into the other.",
    "written_solution": "Split the input into three object panels. Normalize each object up to rotations and reflections. Output a 3\u00d73 matrix whose diagonal is 5 and whose off-diagonal entries are 2 exactly when the two corresponding objects are the same up to dihedral transform; otherwise use 0.",
    "program_name": "rule_h118",
    "program_source": "def rule_h118(g):\n    panels = [crop_nonzero(p) for p in panel_split_horizontal(g)]\n    canons = [canonicalize_transform_equiv([[1 if v != 0 else 0 for v in row] for row in p]) for p in panels]\n    n = len(canons)\n    out = blank(n, n, 0)\n    for i in range(n):\n        for j in range(n):\n            out[i][j] = 5 if i == j else (2 if canons[i] == canons[j] else 0)\n    return out",
    "train": [
      {
        "input": [
          "20004440606",
          "20004000606",
          "22204000666"
        ],
        "output": [
          "520",
          "250",
          "005"
        ]
      },
      {
        "input": [
          "330550077",
          "330550007",
          "300050777"
        ],
        "output": [
          "520",
          "250",
          "005"
        ]
      },
      {
        "input": [
          "2200066600444",
          "2022060604404",
          "2220066600044"
        ],
        "output": [
          "502",
          "050",
          "205"
        ]
      },
      {
        "input": [
          "03300880555",
          "33008800050",
          "30008000050"
        ],
        "output": [
          "520",
          "250",
          "005"
        ]
      }
    ],
    "test": {
      "input": [
        "2020777044",
        "2020707044",
        "2220707040"
      ],
      "output": [
        "520",
        "250",
        "005"
      ]
    }
  },
  {
    "id": "H119",
    "title": "Colorized Anchor Stamp",
    "difficulty": "hard",
    "skills": [
      "prototype extraction",
      "anchor-conditioned recoloring",
      "overlap marking"
    ],
    "suggested_staged_path": "The prototype uses 8 only to mark its origin; the external anchor colors tell you what color each copy should become.",
    "written_solution": "Extract the prototype component containing an origin cell 8. Convert it to a binary stamp: every nonzero cell of the prototype belongs to the stamp. For every external nonzero anchor cell, place one translated copy of that stamp so the prototype origin lands on the anchor. Color the whole copy with the anchor\u2019s color. When different colored copies overlap, mark those overlap cells as 9.",
    "program_name": "rule_h119",
    "program_source": "def rule_h119(g):\n    comps = components_nonzero(g)\n    proto_comp = None\n    for comp in comps:\n        vals = [g[r][c] for r, c in comp[\"cells\"]]\n        if 8 in vals and len(comp[\"cells\"]) > 1:\n            proto_comp = comp\n            break\n    r0, c0, r1, c1 = bbox(proto_comp[\"cells\"])\n    proto = [row[c0:c1+1] for row in g[r0:r1+1]]\n    origin = next((r, c) for r in range(len(proto)) for c in range(len(proto[0])) if proto[r][c] == 8)\n    mask = [[1 if v != 0 else 0 for v in row] for row in proto]\n    out = blank(*size(g), 0)\n    anchors = [(r, c, v) for r, row in enumerate(g) for c, v in enumerate(row) if v not in (0, 1, 8)]\n    for ar, ac, color in anchors:\n        top, left = ar - origin[0], ac - origin[1]\n        for r in range(len(mask)):\n            for c in range(len(mask[0])):\n                if mask[r][c]:\n                    rr, cc = top + r, left + c\n                    if 0 <= rr < len(out) and 0 <= cc < len(out[0]):\n                        if out[rr][cc] == 0:\n                            out[rr][cc] = color\n                        elif out[rr][cc] != color:\n                            out[rr][cc] = 9\n    return out",
    "train": [
      {
        "input": [
          "0000000000",
          "0810000000",
          "0110000040",
          "0011000000",
          "0000000000",
          "0000002000",
          "0000000000",
          "0000000000",
          "0000000000"
        ],
        "output": [
          "0000000000",
          "0000000000",
          "0000000044",
          "0000000044",
          "0000000004",
          "0000002200",
          "0000002200",
          "0000000220",
          "0000000000"
        ]
      },
      {
        "input": [
          "00000000000",
          "00000000000",
          "00810000300",
          "01110000000",
          "00100000000",
          "00000000000",
          "00000700000",
          "00000000000",
          "00000000000",
          "00000000000"
        ],
        "output": [
          "00000000000",
          "00000000000",
          "00000000330",
          "00000003330",
          "00000000300",
          "00000000000",
          "00000770000",
          "00007770000",
          "00000700000",
          "00000000000"
        ]
      },
      {
        "input": [
          "000000000000",
          "008100000000",
          "001010000000",
          "001100000040",
          "000000000000",
          "000000002000",
          "000000000600",
          "000000000000",
          "000000000000",
          "000000000000"
        ],
        "output": [
          "000000000000",
          "000000000000",
          "000000000000",
          "000000000044",
          "000000000040",
          "000000002244",
          "000000002660",
          "000000002900",
          "000000000660",
          "000000000000"
        ]
      },
      {
        "input": [
          "00000000000",
          "00000000500",
          "00810000000",
          "00110000000",
          "00011000000",
          "00000000000",
          "00000070000",
          "00000000000",
          "00000000000"
        ],
        "output": [
          "00000000000",
          "00000000550",
          "00000000550",
          "00000000055",
          "00000000000",
          "00000000000",
          "00000077000",
          "00000077000",
          "00000007700"
        ]
      }
    ],
    "test": {
      "input": [
        "00000000000",
        "00810000000",
        "01110002000",
        "00100000000",
        "00000000000",
        "00000000000",
        "00000400000",
        "00000006000",
        "00000000000",
        "00000000000"
      ],
      "output": [
        "00000000000",
        "00000000000",
        "00000002200",
        "00000022200",
        "00000002000",
        "00000000000",
        "00000440000",
        "00004446600",
        "00000466600",
        "00000006000"
      ]
    }
  }
]
''')

def validate(tasks=TASKS):
    total = 0
    for task in tasks:
        fn = RULES[task["program_name"]]
        for pair in task["train"]:
            inp = grid_from_strings(pair["input"])
            expected = grid_from_strings(pair["output"])
            got = fn(inp)
            total += 1
            if got != expected:
                raise AssertionError(f'{task["id"]} train failed')
        inp = grid_from_strings(task["test"]["input"])
        expected = grid_from_strings(task["test"]["output"])
        got = fn(inp)
        total += 1
        if got != expected:
            raise AssertionError(f'{task["id"]} test failed')
    return {"tasks": len(tasks), "pairs": total, "status": "ok"}

if __name__ == "__main__":
    print(json.dumps(validate(), indent=2))