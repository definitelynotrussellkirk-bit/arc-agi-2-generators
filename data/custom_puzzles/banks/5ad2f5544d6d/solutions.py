from __future__ import annotations

from collections import defaultdict

DIR4=[(-1,0),(1,0),(0,-1),(0,1)]

def blank(h,w,val=0):
    return [[val]*w for _ in range(h)]

def clone(g):
    return [row[:] for row in g]

def size(g):
    return len(g), len(g[0]) if g else 0

def strings_from_grid(g):
    return ["".join(str(c) for c in row) for row in g]

def bbox(cells):
    rs=[r for r,c in cells]; cs=[c for r,c in cells]
    return min(rs), min(cs), max(rs), max(cs)

def crop_bbox(g, cells=None):
    if cells is None:
        cells=[(r,c) for r,row in enumerate(g) for c,v in enumerate(row) if v!=0]
    if not cells:
        return [[0]]
    r0,c0,r1,c1=bbox(cells)
    return [row[c0:c1+1] for row in g[r0:r1+1]]

def rotate_cw(g):
    return [list(row) for row in zip(*g[::-1])]

def flip_h(g):
    return [row[::-1] for row in g]

def flip_v(g):
    return g[::-1]

def transpose(g):
    return [list(row) for row in zip(*g)]

def components_nonzero(g, treat_colors_separately=False, ignore_positions=None, ignore_colors=None):
    h,w=size(g)
    ignore_positions = set(ignore_positions or [])
    ignore_colors = set(ignore_colors or [])
    vis=[[False]*w for _ in range(h)]
    comps=[]
    for r in range(h):
        for c in range(w):
            if vis[r][c] or g[r][c]==0 or (r,c) in ignore_positions or g[r][c] in ignore_colors:
                continue
            col=g[r][c]
            vis[r][c]=True
            q=[(r,c)]
            cells=[]
            while q:
                rr,cc=q.pop()
                cells.append((rr,cc))
                for dr,dc in DIR4:
                    nr,nc=rr+dr,cc+dc
                    if 0<=nr<h and 0<=nc<w and not vis[nr][nc] and g[nr][nc]!=0 and (nr,nc) not in ignore_positions and g[nr][nc] not in ignore_colors:
                        if treat_colors_separately and g[nr][nc]!=col:
                            continue
                        vis[nr][nc]=True
                        q.append((nr,nc))
            comps.append((col,cells))
    return comps

def component_key(comp):
    col,cells=comp
    r0,c0,r1,c1=bbox(cells)
    return (r0,c0,r1-r0+1,c1-c0+1,col)

def normalize_binary(crop):
    return tuple(tuple(1 if v!=0 else 0 for v in row) for row in crop)

def dihedral_variants(bin_grid):
    g=[list(row) for row in bin_grid]
    vars=[]
    seen=set()
    curr=g
    for _ in range(4):
        for v in (curr, flip_h(curr)):
            tup=normalize_binary(v)
            if tup not in seen:
                seen.add(tup); vars.append(tup)
        curr=rotate_cw(curr)
    return vars

def pad_to(g, h, w, val=0):
    out=blank(h,w,val)
    for r,row in enumerate(g):
        for c,v in enumerate(row):
            out[r][c]=v
    return out

def count_holes(crop):
    h,w=size(crop)
    occ=[[1 if crop[r][c]!=0 else 0 for c in range(w)] for r in range(h)]
    vis=[[False]*w for _ in range(h)]
    holes=0
    for r in range(h):
        for c in range(w):
            if occ[r][c] or vis[r][c]:
                continue
            vis[r][c]=True
            q=[(r,c)]
            touches=False
            while q:
                rr,cc=q.pop()
                if rr==0 or cc==0 or rr==h-1 or cc==w-1:
                    touches=True
                for dr,dc in DIR4:
                    nr,nc=rr+dr,cc+dc
                    if 0<=nr<h and 0<=nc<w and not occ[nr][nc] and not vis[nr][nc]:
                        vis[nr][nc]=True
                        q.append((nr,nc))
            if not touches:
                holes += 1
    return holes

def rowcol_sort_components(comps):
    return sorted(comps, key=lambda comp: component_key(comp))

def straight_path(a,b):
    (r1,c1),(r2,c2)=a,b
    if r1==r2:
        step=1 if c2>=c1 else -1
        return [(r1,c) for c in range(c1,c2+step,step)]
    elif c1==c2:
        step=1 if r2>=r1 else -1
        return [(r,c1) for r in range(r1,r2+step,step)]
    else:
        raise ValueError("not aligned")

def bent_path(a,b,bend_policy="row-first"):
    (r1,c1),(r2,c2)=a,b
    if r1==r2 or c1==c2:
        return straight_path(a,b)
    if bend_policy=="row-first":
        first = straight_path((r1,c1),(r1,c2))
        second = straight_path((r1,c2),(r2,c2))
    else:
        first = straight_path((r1,c1),(r2,c1))
        second = straight_path((r2,c1),(r2,c2))
    return first + second[1:]

def link_terminals(base_grid, endpoints, color_mode="endpoint", allow_bends=False, bend_policy="row-first", overlap_color=None, include_endpoints=True):
    out=clone(base_grid)
    counts=defaultdict(int)
    path_color={}
    by_color=defaultdict(list)
    for r,c,col in endpoints:
        by_color[col].append((r,c))
    for col,pts in by_color.items():
        if len(pts)!=2:
            raise ValueError(f"color {col} has {len(pts)} endpoints")
        a,b=pts
        if a==b:
            path=[a]
        else:
            if a[0]==b[0] or a[1]==b[1]:
                path=straight_path(a,b)
            elif allow_bends:
                path=bent_path(a,b,bend_policy=bend_policy)
            else:
                raise ValueError("bend needed")
        for idx,(r,c) in enumerate(path):
            if not include_endpoints and (idx==0 or idx==len(path)-1):
                continue
            paint = col if color_mode=="endpoint" else color_mode
            counts[(r,c)] += 1
            if counts[(r,c)] == 1:
                path_color[(r,c)] = paint
            else:
                path_color[(r,c)] = overlap_color if overlap_color is not None else paint
    for (r,c),paint in path_color.items():
        out[r][c] = paint
    return out

def grid_from_strings(lines):
    return [[int(ch) for ch in row] for row in lines]

def rule_e71(g):
    endpoints=[(r,c,v) for r,row in enumerate(g) for c,v in enumerate(row) if v!=0]
    return link_terminals(g, endpoints, allow_bends=False)

def rule_e72(g):
    h,w=size(g)
    out=blank(h,w)
    colors=defaultdict(list)
    for r,row in enumerate(g):
        for c,v in enumerate(row):
            if v!=0:
                colors[v].append((r,c))
    for col,cells in colors.items():
        r0,c0,r1,c1=bbox(cells)
        for c in range(c0,c1+1):
            out[r0][c]=out[r1][c]=col
        for r in range(r0,r1+1):
            out[r][c0]=out[r][c1]=col
    return out

def rule_e73(g):
    h,w=size(g)
    out=blank(h,w)
    for r,row in enumerate(g):
        vals=[v for v in row if v!=0]
        out[r][:len(vals)] = vals
    return out

def rule_e74(g):
    h,w=size(g)
    out=clone(g)
    # full vertical 9 column
    guide_cols=[c for c in range(w) if all(g[r][c]==9 for r in range(h))]
    gc = guide_cols[0]
    for r in range(h):
        for c in range(gc):
            v=g[r][c]
            if v!=0 and v!=9:
                mc = 2*gc - c
                if 0<=mc<w:
                    out[r][mc] = v
    return out

def rule_e75(g):
    vals=[v for row in g for v in row if v!=0]
    col=vals[0]
    return [[col]*len(vals)]

def rule_e76(g):
    h,w=size(g)
    out=clone(g)
    vis=[[False]*w for _ in range(h)]
    for r in range(h):
        for c in range(w):
            if g[r][c]!=0 or vis[r][c]:
                continue
            vis[r][c]=True
            q=[(r,c)]
            region=[]
            border=False
            neigh=set()
            while q:
                rr,cc=q.pop()
                region.append((rr,cc))
                if rr==0 or cc==0 or rr==h-1 or cc==w-1:
                    border=True
                for dr,dc in DIR4:
                    nr,nc=rr+dr,cc+dc
                    if 0<=nr<h and 0<=nc<w:
                        if g[nr][nc]==0 and not vis[nr][nc]:
                            vis[nr][nc]=True; q.append((nr,nc))
                        elif g[nr][nc]!=0:
                            neigh.add(g[nr][nc])
            if not border and len(neigh)==1:
                col=next(iter(neigh))
                for rr,cc in region:
                    out[rr][cc]=col
    return out

def rule_e77(g):
    h,w=size(g)
    out=clone(g)
    motif=[row[:2] for row in g[:2]]
    markers=[(r,c) for r,row in enumerate(g) for c,v in enumerate(row) if v==9]
    for r,c in markers:
        out[r][c]=0
    for r,c in markers:
        for dr in range(2):
            for dc in range(2):
                v=motif[dr][dc]
                if v!=0:
                    out[r+dr][c+dc]=v
    return out

def rule_m71(g):
    cmd=g[0][0]
    bend='row-first' if cmd==1 else 'col-first'
    endpoints=[(r,c,v) for r,row in enumerate(g) for c,v in enumerate(row) if v!=0 and not (r==0 and c==0)]
    return link_terminals(g, endpoints, allow_bends=True, bend_policy=bend)

def rule_m72(g):
    guide=[v for v in g[0] if v!=0][0]
    cells=[(r,c) for r in range(1,len(g)) for c,v in enumerate(g[r]) if v==guide]
    return crop_bbox(g, cells)

def rule_m73(g):
    h,w=size(g)
    out=blank(h,w)
    comps=components_nonzero(g, treat_colors_separately=True)
    for col,cells in comps:
        r0,c0,r1,c1=bbox(cells)
        for c in range(c0,c1+1):
            out[r0][c]=out[r1][c]=col
        for r in range(r0,r1+1):
            out[r][c0]=out[r][c1]=col
        for r in range(r0+1,r1):
            for c in range(c0+1,c1):
                out[r][c]=col if ((r-(r0+1)) + (c-(c0+1)))%2==0 else 0
    return out

def rule_m74(g):
    comps=rowcol_sort_components(components_nonzero(g, treat_colors_separately=True))
    n=len(comps)
    areas=[len(cells) for col,cells in comps]
    out=blank(n,n)
    for i in range(n):
        for j in range(n):
            out[i][j]=8 if areas[i]==areas[j] else 0
    return out

def rule_m75(g):
    k=sum(1 for v in g[0] if v==9)
    comps=rowcol_sort_components(components_nonzero(g, treat_colors_separately=True, ignore_positions={(0,c) for c in range(len(g[0]))}, ignore_colors={9}))
    comps=sorted(comps, key=lambda comp: (len(comp[1]),) + component_key(comp))
    sel=comps[k-1]
    return crop_bbox(g, sel[1])

def rule_m76(g):
    comps=rowcol_sort_components(components_nonzero(g, treat_colors_separately=True))
    # pick first two non-divider colors with largest components? We'll design only 2
    crops=[crop_bbox(g,cells) for col,cells in comps[:2]]
    h=max(len(crops[0]), len(crops[1]))
    w=max(len(crops[0][0]), len(crops[1][0]))
    a=pad_to([[1 if v!=0 else 0 for v in row] for row in crops[0]], h,w)
    b=pad_to([[1 if v!=0 else 0 for v in row] for row in crops[1]], h,w)
    out=blank(h,w)
    for r in range(h):
        for c in range(w):
            out[r][c]=8 if a[r][c] != b[r][c] else 0
    return out

def rule_m77(g):
    legend=[v for v in g[0] if v!=0]
    comps=rowcol_sort_components(components_nonzero(g, treat_colors_separately=True, ignore_positions={(0,c) for c in range(len(g[0]))}))
    by_color={}
    for col,cells in comps:
        by_color[col]=crop_bbox(g,cells)
    crops=[by_color[col] for col in legend]
    H=max(len(c) for c in crops)
    W=sum(len(c[0]) for c in crops)+(len(crops)-1)
    out=blank(H,W)
    x=0
    for i,crop in enumerate(crops):
        for r,row in enumerate(crop):
            for c,v in enumerate(row):
                out[r][x+c]=v
        x += len(crop[0])
        if i!=len(crops)-1:
            x += 1
    return out

def rule_h71(g):
    cmd=g[0][0]
    bend='row-first' if cmd==1 else 'col-first'
    endpoints=[(r,c,v) for r,row in enumerate(g) for c,v in enumerate(row) if v!=0 and not (r==0 and c==0)]
    return link_terminals(g, endpoints, allow_bends=True, bend_policy=bend, overlap_color=8)

def rule_h72(g):
    # colors 2,3 define translation; color 4 target
    by_color=defaultdict(list)
    for r,row in enumerate(g):
        for c,v in enumerate(row):
            if v in (2,3,4):
                by_color[v].append((r,c))
    r20,c20,_,_ = bbox(by_color[2])
    r30,c30,_,_ = bbox(by_color[3])
    dr,dc = r30-r20, c30-c20
    h,w=size(g)
    out=blank(h,w)
    for r,c in by_color[4]:
        nr,nc=r+dr,c+dc
        out[nr][nc]=4
    return out

def rule_h73(g):
    h,w=size(g)
    comps=components_nonzero(g, treat_colors_separately=True)
    rects=[]
    for col,cells in comps:
        r0,c0,r1,c1=bbox(cells)
        rects.append((r0,c0,r1,c1))
    out=blank(h,w)
    for r in range(h):
        for c in range(w):
            depth=sum(1 for r0,c0,r1,c1 in rects if r0<=r<=r1 and c0<=c<=c1)
            out[r][c]=depth
    return out

def rule_h74(g):
    comps=rowcol_sort_components(components_nonzero(g, treat_colors_separately=True))
    bins=[]
    for col,cells in comps:
        crop=crop_bbox(g,cells)
        bins.append(normalize_binary(crop))
    n=len(bins)
    vars=[set(dihedral_variants(b)) for b in bins]
    out=blank(n,n)
    for i in range(n):
        for j in range(n):
            out[i][j]=8 if bins[j] in vars[i] else 0
    return out

def rule_h75(g):
    cmds=[]
    for v in g[0]:
        if v==0: break
        cmds.append(v)
    cells=[(r,c) for r in range(1,len(g)) for c,v in enumerate(g[r]) if v!=0]
    obj=crop_bbox(g,cells)
    cur=obj
    for cmd in cmds:
        if cmd==1:
            cur=rotate_cw(cur)
        elif cmd==2:
            cur=flip_h(cur)
        elif cmd==3:
            cur=flip_v(cur)
        elif cmd==4:
            cur=transpose(cur)
        else:
            raise ValueError(cmd)
    return cur

def rule_h76(g):
    h,w=size(g)
    out=blank(h,w)
    for r in range(h):
        for c in range(w):
            if g[r][c]==9:
                out[r][c]=9
    vis=[[False]*w for _ in range(h)]
    for r in range(h):
        for c in range(w):
            if g[r][c]==9 or vis[r][c]:
                continue
            vis[r][c]=True
            q=[(r,c)]
            region=[]
            colors=set()
            while q:
                rr,cc=q.pop()
                region.append((rr,cc))
                if g[rr][cc] not in (0,9):
                    colors.add(g[rr][cc])
                for dr,dc in DIR4:
                    nr,nc=rr+dr,cc+dc
                    if 0<=nr<h and 0<=nc<w and not vis[nr][nc] and g[nr][nc]!=9:
                        vis[nr][nc]=True; q.append((nr,nc))
            fill = next(iter(colors)) if len(colors)==1 else 0
            for rr,cc in region:
                if fill and g[rr][cc]==0:
                    out[rr][cc]=fill
                elif g[rr][cc]!=0 and g[rr][cc]!=9:
                    out[rr][cc]=g[rr][cc]
    return out

def rule_h77(g):
    comps=rowcol_sort_components(components_nonzero(g, treat_colors_separately=True))
    items=[]
    for idx,(col,cells) in enumerate(comps):
        crop=crop_bbox(g,cells)
        items.append((count_holes(crop), idx, crop))
    items.sort(key=lambda x:(x[0],x[1]))
    crops=[crop for _,_,crop in items]
    H=max(len(c) for c in crops)
    W=sum(len(c[0]) for c in crops)+(len(crops)-1)
    out=blank(H,W)
    x=0
    for i,crop in enumerate(crops):
        for r,row in enumerate(crop):
            for c,v in enumerate(row):
                out[r][x+c]=v
        x += len(crop[0])
        if i!=len(crops)-1:
            x += 1
    return out

RULES = {
    'rule_e71': rule_e71,
    'rule_e72': rule_e72,
    'rule_e73': rule_e73,
    'rule_e74': rule_e74,
    'rule_e75': rule_e75,
    'rule_e76': rule_e76,
    'rule_e77': rule_e77,
    'rule_m71': rule_m71,
    'rule_m72': rule_m72,
    'rule_m73': rule_m73,
    'rule_m74': rule_m74,
    'rule_m75': rule_m75,
    'rule_m76': rule_m76,
    'rule_m77': rule_m77,
    'rule_h71': rule_h71,
    'rule_h72': rule_h72,
    'rule_h73': rule_h73,
    'rule_h74': rule_h74,
    'rule_h75': rule_h75,
    'rule_h76': rule_h76,
    'rule_h77': rule_h77,
}

PUZZLES = [{'id': 'E71',
  'title': 'Straight Terminal Links',
  'difficulty': 'easy',
  'skills': ['path completion', 'endpoint pairing', 'same-size transform'],
  'staged_hint': 'Find the colored terminal pairs first. Then connect each same-colored pair with the shortest '
                 'straight segment.',
  'written_solution': "Each nonzero color appears exactly twice as aligned terminals. Connect each color's two cells "
                      'with a straight horizontal or vertical segment of that same color.',
  'uses_new_primitive': True,
  'program_name': 'rule_e71',
  'program_source': 'def rule_e71(g):\n'
                    '    endpoints=[(r,c,v) for r,row in enumerate(g) for c,v in enumerate(row) if v!=0]\n'
                    '    return link_terminals(g, endpoints, allow_bends=False)',
  'train': [{'input': ['0000000', '0200020', '0003000', '0000000', '0000000', '0003000', '0000000'],
             'output': ['0000000', '0222220', '0003000', '0003000', '0003000', '0003000', '0000000']},
            {'input': ['00000000', '00000040', '00000000', '00000000', '05000500', '00000000', '00000040', '00000000'],
             'output': ['00000000',
                        '00000040',
                        '00000040',
                        '00000040',
                        '05555540',
                        '00000040',
                        '00000040',
                        '00000000']},
            {'input': ['000000000',
                       '000000000',
                       '002000000',
                       '000000000',
                       '000000000',
                       '000000000',
                       '000060060',
                       '002000000',
                       '000000000'],
             'output': ['000000000',
                        '000000000',
                        '002000000',
                        '002000000',
                        '002000000',
                        '002000000',
                        '002066660',
                        '002000000',
                        '000000000']},
            {'input': ['000000000',
                       '030000030',
                       '000040000',
                       '000000000',
                       '000000000',
                       '050500000',
                       '000040000',
                       '000000000'],
             'output': ['000000000',
                        '033333330',
                        '000040000',
                        '000040000',
                        '000040000',
                        '055540000',
                        '000040000',
                        '000000000']}],
  'test': {'input': ['0000000000',
                     '0020000000',
                     '0000000000',
                     '0000040040',
                     '0000000000',
                     '0000000000',
                     '0000006000',
                     '0020000000',
                     '0000006000'],
           'output': ['0000000000',
                      '0020000000',
                      '0020000000',
                      '0020044440',
                      '0020000000',
                      '0020000000',
                      '0020006000',
                      '0020006000',
                      '0000006000']}},
 {'id': 'E72',
  'title': 'Complete the Rectangle',
  'difficulty': 'easy',
  'skills': ['bounding boxes', 'rectangle inference', 'border drawing'],
  'staged_hint': 'Ignore the missing corner. Use the extreme occupied rows and columns to infer the whole rectangle.',
  'written_solution': 'For each color, take the bounding box of its given corner cells and draw the full border of '
                      'that axis-aligned rectangle.',
  'uses_new_primitive': False,
  'program_name': 'rule_e72',
  'program_source': 'def rule_e72(g):\n'
                    '    h,w=size(g)\n'
                    '    out=blank(h,w)\n'
                    '    colors=defaultdict(list)\n'
                    '    for r,row in enumerate(g):\n'
                    '        for c,v in enumerate(row):\n'
                    '            if v!=0:\n'
                    '                colors[v].append((r,c))\n'
                    '    for col,cells in colors.items():\n'
                    '        r0,c0,r1,c1=bbox(cells)\n'
                    '        for c in range(c0,c1+1):\n'
                    '            out[r0][c]=out[r1][c]=col\n'
                    '        for r in range(r0,r1+1):\n'
                    '            out[r][c0]=out[r][c1]=col\n'
                    '    return out',
  'train': [{'input': ['00000000', '02000200', '00000000', '00000000', '00000000', '02000000', '00000000', '00000000'],
             'output': ['00000000',
                        '02222200',
                        '02000200',
                        '02000200',
                        '02000200',
                        '02222200',
                        '00000000',
                        '00000000']},
            {'input': ['000000000',
                       '000000000',
                       '003000000',
                       '000000000',
                       '000000000',
                       '000000000',
                       '003000300',
                       '000000000',
                       '000000000'],
             'output': ['000000000',
                        '000000000',
                        '003333300',
                        '003000300',
                        '003000300',
                        '003000300',
                        '003333300',
                        '000000000',
                        '000000000']},
            {'input': ['0000000000',
                       '0000000400',
                       '0000000000',
                       '0000000000',
                       '0000000000',
                       '0040000400',
                       '0000000000'],
             'output': ['0000000000',
                        '0044444400',
                        '0040000400',
                        '0040000400',
                        '0040000400',
                        '0044444400',
                        '0000000000']},
            {'input': ['0000000000',
                       '0000000000',
                       '0005000050',
                       '0000000000',
                       '0000000000',
                       '0000000000',
                       '0000000000',
                       '0000000050',
                       '0000000000',
                       '0000000000'],
             'output': ['0000000000',
                        '0000000000',
                        '0005555550',
                        '0005000050',
                        '0005000050',
                        '0005000050',
                        '0005000050',
                        '0005555550',
                        '0000000000',
                        '0000000000']}],
  'test': {'input': ['00000000000',
                     '00600000060',
                     '00000000000',
                     '00000000000',
                     '00000000000',
                     '00000000000',
                     '00600000000',
                     '00000000000'],
           'output': ['00000000000',
                      '00666666660',
                      '00600000060',
                      '00600000060',
                      '00600000060',
                      '00600000060',
                      '00666666660',
                      '00000000000']}},
 {'id': 'E73',
  'title': 'Left-Pack Every Row',
  'difficulty': 'easy',
  'skills': ['row-wise processing', 'order preservation', 'compression'],
  'staged_hint': 'Treat each row independently. Keep the nonzero colors in order and slide them left.',
  'written_solution': 'For every row, remove the zeros, keep the remaining colors in their original order, and place '
                      'them flush to the left with zeros filling the rest.',
  'uses_new_primitive': False,
  'program_name': 'rule_e73',
  'program_source': 'def rule_e73(g):\n'
                    '    h,w=size(g)\n'
                    '    out=blank(h,w)\n'
                    '    for r,row in enumerate(g):\n'
                    '        vals=[v for v in row if v!=0]\n'
                    '        out[r][:len(vals)] = vals\n'
                    '    return out',
  'train': [{'input': ['0200030', '0004005', '5060000', '0000000'],
             'output': ['2300000', '4500000', '5600000', '0000000']},
            {'input': ['10200304', '00000000', '05006070', '70000008', '00090000'],
             'output': ['12340000', '00000000', '56700000', '78000000', '90000000']},
            {'input': ['000000', '202033', '004040', '050600', '000000'],
             'output': ['000000', '223300', '440000', '560000', '000000']},
            {'input': ['900080700', '000000000', '102000030', '004050060'],
             'output': ['987000000', '000000000', '123000000', '456000000']}],
  'test': {'input': ['00302010', '40000005', '06070000', '00000000', '80009000'],
           'output': ['32100000', '45000000', '67000000', '00000000', '89000000']}},
 {'id': 'E74',
  'title': 'Mirror Across the Guide Wall',
  'difficulty': 'easy',
  'skills': ['reflection', 'guide detection', 'same-size transform'],
  'staged_hint': 'First identify the full vertical guide. Then reflect every colored cell on the left side to the same '
                 'offset on the right.',
  'written_solution': 'The column filled with 9s is a mirror guide. Keep the original motif and copy each nonzero '
                      'non-guide cell to its mirror position across that guide.',
  'uses_new_primitive': False,
  'program_name': 'rule_e74',
  'program_source': 'def rule_e74(g):\n'
                    '    h,w=size(g)\n'
                    '    out=clone(g)\n'
                    '    # full vertical 9 column\n'
                    '    guide_cols=[c for c in range(w) if all(g[r][c]==9 for r in range(h))]\n'
                    '    gc = guide_cols[0]\n'
                    '    for r in range(h):\n'
                    '        for c in range(gc):\n'
                    '            v=g[r][c]\n'
                    '            if v!=0 and v!=9:\n'
                    '                mc = 2*gc - c\n'
                    '                if 0<=mc<w:\n'
                    '                    out[r][mc] = v\n'
                    '    return out',
  'train': [{'input': ['000090000', '020090000', '022090000', '000090000', '300090000', '030090000', '000090000'],
             'output': ['000090000', '020090020', '022090220', '000090000', '300090003', '030090030', '000090000']},
            {'input': ['00000900000',
                       '00400900000',
                       '00400900000',
                       '00040900000',
                       '00000900000',
                       '06000900000',
                       '06600900000',
                       '00000900000'],
             'output': ['00000900000',
                        '00400900400',
                        '00400900400',
                        '00040904000',
                        '00000900000',
                        '06000900060',
                        '06600900660',
                        '00000900000']},
            {'input': ['000090000', '505090000', '050090000', '000090000', '007090000', '000090000'],
             'output': ['000090000', '505090505', '050090050', '000090000', '007090700', '000090000']},
            {'input': ['0000009000000',
                       '0000009000000',
                       '0200009000000',
                       '0220009000000',
                       '0020009000000',
                       '0000009000000',
                       '8000009000000',
                       '0880009000000',
                       '0000009000000'],
             'output': ['0000009000000',
                        '0000009000000',
                        '0200009000020',
                        '0220009000220',
                        '0020009000200',
                        '0000009000000',
                        '8000009000008',
                        '0880009000880',
                        '0000009000000']}],
  'test': {'input': ['00000900000',
                     '03000900000',
                     '00300900000',
                     '03000900000',
                     '00000900000',
                     '00400900000',
                     '04000900000',
                     '00000900000'],
           'output': ['00000900000',
                      '03000900030',
                      '00300900300',
                      '03000900030',
                      '00000900000',
                      '00400900400',
                      '04000900040',
                      '00000900000']}},
 {'id': 'E75',
  'title': 'Count to a Bar',
  'difficulty': 'easy',
  'skills': ['counting', 'dynamic-size output', 'color preservation'],
  'staged_hint': 'Only one color matters. Count how many times it appears, then output a bar of that many cells.',
  'written_solution': 'Count all nonzero marker cells and output a single row whose length equals that count, filled '
                      'with the marker color.',
  'uses_new_primitive': False,
  'program_name': 'rule_e75',
  'program_source': 'def rule_e75(g):\n'
                    '    vals=[v for row in g for v in row if v!=0]\n'
                    '    col=vals[0]\n'
                    '    return [[col]*len(vals)]',
  'train': [{'input': ['020000', '000200', '002000', '000000', '000000'], 'output': ['222']},
            {'input': ['4000000', '0000040', '0400000', '0000000', '0000004', '0004000'], 'output': ['44444']},
            {'input': ['00700700', '07000000', '00000070', '00000000'], 'output': ['7777']},
            {'input': ['0000000', '0300030', '0000000', '0003000', '0000000', '0300030', '0003000'],
             'output': ['333333']}],
  'test': {'input': ['000060000', '060000000', '000000060', '000600000', '000006000', '000000000'],
           'output': ['66666']}},
 {'id': 'E76',
  'title': 'Fill the Enclosed Hole',
  'difficulty': 'easy',
  'skills': ['enclosure', 'hole fill', 'region detection'],
  'staged_hint': 'Separate boundary-connected zeros from enclosed zeros. Only the interior zero region changes.',
  'written_solution': 'Find zero regions that do not touch the outside border. If such a region is enclosed by a '
                      'single surrounding color, fill the whole interior with that color.',
  'uses_new_primitive': False,
  'program_name': 'rule_e76',
  'program_source': 'def rule_e76(g):\n'
                    '    h,w=size(g)\n'
                    '    out=clone(g)\n'
                    '    vis=[[False]*w for _ in range(h)]\n'
                    '    for r in range(h):\n'
                    '        for c in range(w):\n'
                    '            if g[r][c]!=0 or vis[r][c]:\n'
                    '                continue\n'
                    '            vis[r][c]=True\n'
                    '            q=[(r,c)]\n'
                    '            region=[]\n'
                    '            border=False\n'
                    '            neigh=set()\n'
                    '            while q:\n'
                    '                rr,cc=q.pop()\n'
                    '                region.append((rr,cc))\n'
                    '                if rr==0 or cc==0 or rr==h-1 or cc==w-1:\n'
                    '                    border=True\n'
                    '                for dr,dc in DIR4:\n'
                    '                    nr,nc=rr+dr,cc+dc\n'
                    '                    if 0<=nr<h and 0<=nc<w:\n'
                    '                        if g[nr][nc]==0 and not vis[nr][nc]:\n'
                    '                            vis[nr][nc]=True; q.append((nr,nc))\n'
                    '                        elif g[nr][nc]!=0:\n'
                    '                            neigh.add(g[nr][nc])\n'
                    '            if not border and len(neigh)==1:\n'
                    '                col=next(iter(neigh))\n'
                    '                for rr,cc in region:\n'
                    '                    out[rr][cc]=col\n'
                    '    return out',
  'train': [{'input': ['00000000', '02222220', '02000020', '02000020', '02000020', '02222220', '00000000'],
             'output': ['00000000', '02222220', '02222220', '02222220', '02222220', '02222220', '00000000']},
            {'input': ['000000000',
                       '000000000',
                       '004444440',
                       '004000040',
                       '004000040',
                       '004000040',
                       '004444440',
                       '000000000'],
             'output': ['000000000',
                        '000000000',
                        '004444440',
                        '004444440',
                        '004444440',
                        '004444440',
                        '004444440',
                        '000000000']},
            {'input': ['0000000000', '0005555550', '0005000050', '0005000050', '0005555550', '0000000000'],
             'output': ['0000000000', '0005555550', '0005555550', '0005555550', '0005555550', '0000000000']},
            {'input': ['000000000',
                       '033333330',
                       '030000030',
                       '030000030',
                       '030000030',
                       '030000030',
                       '030000030',
                       '033333330',
                       '000000000'],
             'output': ['000000000',
                        '033333330',
                        '033333330',
                        '033333330',
                        '033333330',
                        '033333330',
                        '033333330',
                        '033333330',
                        '000000000']}],
  'test': {'input': ['0000000000',
                     '0000000000',
                     '0666666660',
                     '0600000060',
                     '0600000060',
                     '0600000060',
                     '0666666660',
                     '0000000000'],
           'output': ['0000000000',
                      '0000000000',
                      '0666666660',
                      '0666666660',
                      '0666666660',
                      '0666666660',
                      '0666666660',
                      '0000000000']}},
 {'id': 'E77',
  'title': 'Stamp the Corner Motif',
  'difficulty': 'easy',
  'skills': ['motif copying', 'marker interpretation', 'same-size transform'],
  'staged_hint': 'Read the 2×2 motif from the upper-left corner first. Then stamp that exact motif at every marker '
                 'cell.',
  'written_solution': 'Take the top-left 2×2 block as the source motif. Remove the 9 markers and paste the motif with '
                      "each marker acting as the motif's top-left anchor.",
  'uses_new_primitive': False,
  'program_name': 'rule_e77',
  'program_source': 'def rule_e77(g):\n'
                    '    h,w=size(g)\n'
                    '    out=clone(g)\n'
                    '    motif=[row[:2] for row in g[:2]]\n'
                    '    markers=[(r,c) for r,row in enumerate(g) for c,v in enumerate(row) if v==9]\n'
                    '    for r,c in markers:\n'
                    '        out[r][c]=0\n'
                    '    for r,c in markers:\n'
                    '        for dr in range(2):\n'
                    '            for dc in range(2):\n'
                    '                v=motif[dr][dc]\n'
                    '                if v!=0:\n'
                    '                    out[r+dr][c+dc]=v\n'
                    '    return out',
  'train': [{'input': ['20000000', '34000000', '00000000', '00009000', '00000000', '09000000', '00000000'],
             'output': ['20000000', '34000000', '00000000', '00002000', '00003400', '02000000', '03400000']},
            {'input': ['500000000',
                       '060000000',
                       '000009000',
                       '000000000',
                       '000000000',
                       '000090000',
                       '090000000',
                       '000000000'],
             'output': ['500000000',
                        '060000000',
                        '000005000',
                        '000000600',
                        '000000000',
                        '000050000',
                        '050006000',
                        '006000000']},
            {'input': ['2700000000',
                       '7000000000',
                       '0000000000',
                       '0090000000',
                       '0000009000',
                       '0000000000',
                       '0000000000'],
             'output': ['2700000000',
                        '7000000000',
                        '0000000000',
                        '0027000000',
                        '0070002700',
                        '0000007000',
                        '0000000000']},
            {'input': ['800000000',
                       '180000000',
                       '000900000',
                       '000000000',
                       '000000000',
                       '000009000',
                       '009000000',
                       '000000000',
                       '000000000'],
             'output': ['800000000',
                        '180000000',
                        '000800000',
                        '000180000',
                        '000000000',
                        '000008000',
                        '008001800',
                        '001800000',
                        '000000000']}],
  'test': {'input': ['2400000000',
                     '4000000000',
                     '0000000000',
                     '0000090000',
                     '0000000000',
                     '0900000000',
                     '0000000900',
                     '0000000000'],
           'output': ['2400000000',
                      '4000000000',
                      '0000000000',
                      '0000024000',
                      '0000040000',
                      '0240000000',
                      '0400000240',
                      '0000000400']}},
 {'id': 'M71',
  'title': 'Commanded L-Links',
  'difficulty': 'medium',
  'skills': ['path routing', 'command decoding', 'paired terminals'],
  'staged_hint': 'Read the command cell before tracing any paths. Then connect each color pair with a single-bend '
                 'Manhattan route that obeys that command.',
  'written_solution': 'The top-left command chooses row-first or column-first routing. Connect each same-colored '
                      'terminal pair with an L-shaped Manhattan path using that bend policy.',
  'uses_new_primitive': True,
  'program_name': 'rule_m71',
  'program_source': 'def rule_m71(g):\n'
                    '    cmd=g[0][0]\n'
                    "    bend='row-first' if cmd==1 else 'col-first'\n"
                    '    endpoints=[(r,c,v) for r,row in enumerate(g) for c,v in enumerate(row) if v!=0 and not (r==0 '
                    'and c==0)]\n'
                    '    return link_terminals(g, endpoints, allow_bends=True, bend_policy=bend)',
  'train': [{'input': ['10000000', '00000300', '04000000', '00000000', '00000000', '00300000', '00004000', '00000000'],
             'output': ['10000000',
                        '00333300',
                        '04444000',
                        '00304000',
                        '00304000',
                        '00304000',
                        '00004000',
                        '00000000']},
            {'input': ['200000000',
                       '000000500',
                       '000000000',
                       '060000000',
                       '000000000',
                       '000000000',
                       '000500000',
                       '000006000',
                       '000000000'],
             'output': ['200000000',
                        '000000500',
                        '000000500',
                        '060000500',
                        '060000500',
                        '060000500',
                        '060555500',
                        '066666000',
                        '000000000']},
            {'input': ['1000000000',
                       '0000000000',
                       '0000000300',
                       '0000000000',
                       '0070000000',
                       '0000000000',
                       '0000000000',
                       '0000300000',
                       '0000000070',
                       '0000000000'],
             'output': ['1000000000',
                        '0000000000',
                        '0000333300',
                        '0000300000',
                        '0077777770',
                        '0000300070',
                        '0000300070',
                        '0000300070',
                        '0000000070',
                        '0000000000']},
            {'input': ['2000000000',
                       '0000000040',
                       '0050000000',
                       '0000000000',
                       '0000000000',
                       '0004000000',
                       '0000000500',
                       '0000000000'],
             'output': ['2000000000',
                        '0000000040',
                        '0050000040',
                        '0050000040',
                        '0050000040',
                        '0054444440',
                        '0055555500',
                        '0000000000']}],
  'test': {'input': ['1000000000',
                     '0000000300',
                     '0000000000',
                     '0600000000',
                     '0000000000',
                     '0000000000',
                     '0030000000',
                     '0000006000',
                     '0000000000'],
           'output': ['1000000000',
                      '0033333300',
                      '0030000000',
                      '0666666000',
                      '0030006000',
                      '0030006000',
                      '0030006000',
                      '0000006000',
                      '0000000000']}},
 {'id': 'M72',
  'title': 'Guide-Color Crop',
  'difficulty': 'medium',
  'skills': ['object selection', 'color matching', 'cropping'],
  'staged_hint': 'The guide color is in the top row. Ignore the other objects and crop only the component whose color '
                 'matches that guide.',
  'written_solution': 'Read the nonzero guide color from the top row, find the object of that color in the main grid, '
                      'and output its tight bounding-box crop.',
  'uses_new_primitive': False,
  'program_name': 'rule_m72',
  'program_source': 'def rule_m72(g):\n'
                    '    guide=[v for v in g[0] if v!=0][0]\n'
                    '    cells=[(r,c) for r in range(1,len(g)) for c,v in enumerate(g[r]) if v==guide]\n'
                    '    return crop_bbox(g, cells)',
  'train': [{'input': ['3000000000',
                       '0000000000',
                       '0220033300',
                       '0200030300',
                       '0000000000',
                       '0044000000',
                       '0004400000',
                       '0000000000'],
             'output': ['333', '303']},
            {'input': ['500000000000',
                       '000000000000',
                       '005550000000',
                       '000500000000',
                       '000000033000',
                       '000000033000',
                       '066600000000',
                       '060000000000',
                       '000000000000'],
             'output': ['555', '050']},
            {'input': ['40000000000',
                       '00000000000',
                       '00200000000',
                       '02220000000',
                       '00200000000',
                       '00000044000',
                       '00000044000',
                       '00770040000',
                       '00700000000',
                       '00000000000'],
             'output': ['44', '44', '40']},
            {'input': ['6000000000000',
                       '0000000000000',
                       '0033300000000',
                       '0000300066600',
                       '0000000060600',
                       '0000550066600',
                       '0000550000000',
                       '0000000000000'],
             'output': ['666', '606', '666']}],
  'test': {'input': ['200000000000',
                     '000000000000',
                     '004440000000',
                     '000400020000',
                     '000000022000',
                     '000666002200',
                     '000606000000',
                     '000000000000',
                     '000000000000'],
           'output': ['200', '220', '022']}},
 {'id': 'M73',
  'title': 'Checkerboard Frame Fill',
  'difficulty': 'medium',
  'skills': ['frame detection', 'interior filling', 'parity patterns'],
  'staged_hint': 'First detect each rectangular frame. Then fill only its interior, using an alternating checkerboard '
                 'aligned to the interior corner.',
  'written_solution': 'For each rectangular border, keep the frame itself and fill its interior with a checkerboard of '
                      "frame color and zero, starting with the frame color at the interior's top-left cell.",
  'uses_new_primitive': False,
  'program_name': 'rule_m73',
  'program_source': 'def rule_m73(g):\n'
                    '    h,w=size(g)\n'
                    '    out=blank(h,w)\n'
                    '    comps=components_nonzero(g, treat_colors_separately=True)\n'
                    '    for col,cells in comps:\n'
                    '        r0,c0,r1,c1=bbox(cells)\n'
                    '        for c in range(c0,c1+1):\n'
                    '            out[r0][c]=out[r1][c]=col\n'
                    '        for r in range(r0,r1+1):\n'
                    '            out[r][c0]=out[r][c1]=col\n'
                    '        for r in range(r0+1,r1):\n'
                    '            for c in range(c0+1,c1):\n'
                    '                out[r][c]=col if ((r-(r0+1)) + (c-(c0+1)))%2==0 else 0\n'
                    '    return out',
  'train': [{'input': ['0000000000',
                       '0222220000',
                       '0200020000',
                       '0200020000',
                       '0200020000',
                       '0222220000',
                       '0000000000',
                       '0000000000'],
             'output': ['0000000000',
                        '0222220000',
                        '0220220000',
                        '0202020000',
                        '0220220000',
                        '0222220000',
                        '0000000000',
                        '0000000000']},
            {'input': ['000000000000',
                       '033330000000',
                       '030030055550',
                       '030030050050',
                       '030030050050',
                       '030030050050',
                       '033330050050',
                       '000000055550',
                       '000000000000'],
             'output': ['000000000000',
                        '033330000000',
                        '033030055550',
                        '030330055050',
                        '033030050550',
                        '030330055050',
                        '033330050550',
                        '000000055550',
                        '000000000000']},
            {'input': ['0000000000',
                       '0000000000',
                       '0044444400',
                       '0040000400',
                       '0040000400',
                       '0040000400',
                       '0040000400',
                       '0044444400',
                       '0000000000',
                       '0000000000'],
             'output': ['0000000000',
                        '0000000000',
                        '0044444400',
                        '0044040400',
                        '0040404400',
                        '0044040400',
                        '0040404400',
                        '0044444400',
                        '0000000000',
                        '0000000000']},
            {'input': ['0000000000000',
                       '0666660022220',
                       '0600060020020',
                       '0600060020020',
                       '0600060020020',
                       '0666660020020',
                       '0000000022220',
                       '0000000000000'],
             'output': ['0000000000000',
                        '0666660022220',
                        '0660660022020',
                        '0606060020220',
                        '0660660022020',
                        '0666660020220',
                        '0000000022220',
                        '0000000000000']}],
  'test': {'input': ['00000000000',
                     '00555555500',
                     '00500000500',
                     '00500000500',
                     '00500000500',
                     '00500000500',
                     '00555555500',
                     '00000000000',
                     '00000000000'],
           'output': ['00000000000',
                      '00555555500',
                      '00550505500',
                      '00505050500',
                      '00550505500',
                      '00505050500',
                      '00555555500',
                      '00000000000',
                      '00000000000']}},
 {'id': 'M74',
  'title': 'Area Equality Matrix',
  'difficulty': 'medium',
  'skills': ['component measurement', 'reading-order sorting', 'relation matrices'],
  'staged_hint': 'Extract the three objects and measure their areas. The output is a matrix comparing those areas '
                 'pairwise.',
  'written_solution': 'Sort the objects by reading order. Output a 3×3 matrix with 8 when two objects have the same '
                      'number of cells and 0 otherwise.',
  'uses_new_primitive': False,
  'program_name': 'rule_m74',
  'program_source': 'def rule_m74(g):\n'
                    '    comps=rowcol_sort_components(components_nonzero(g, treat_colors_separately=True))\n'
                    '    n=len(comps)\n'
                    '    areas=[len(cells) for col,cells in comps]\n'
                    '    out=blank(n,n)\n'
                    '    for i in range(n):\n'
                    '        for j in range(n):\n'
                    '            out[i][j]=8 if areas[i]==areas[j] else 0\n'
                    '    return out',
  'train': [{'input': ['000000000000',
                       '022000330000',
                       '020000033000',
                       '000000000000',
                       '000000000000',
                       '000000004400',
                       '000000004400',
                       '000000000000'],
             'output': ['800', '088', '088']},
            {'input': ['0000000000000',
                       '0000000000000',
                       '0222005550000',
                       '0020005000000',
                       '0000000000000',
                       '0000000007700',
                       '0000000007700',
                       '0000000007000',
                       '0000000000000'],
             'output': ['880', '880', '008']},
            {'input': ['000000000000',
                       '033000000000',
                       '033000000000',
                       '000000000000',
                       '000000444000',
                       '000000404000',
                       '000000000000',
                       '006600000000',
                       '006000000000',
                       '000000000000'],
             'output': ['800', '080', '008']},
            {'input': ['00000000000000',
                       '02220000006660',
                       '00020000006000',
                       '00000000000000',
                       '00000005550000',
                       '00000000500000',
                       '00000000000000',
                       '00000000000000'],
             'output': ['888', '888', '888']}],
  'test': {'input': ['000000000000',
                     '002000044400',
                     '022200040400',
                     '002000044400',
                     '000000000000',
                     '000000000000',
                     '000660000000',
                     '000660000000',
                     '000600000000'],
           'output': ['808', '080', '808']}},
 {'id': 'M75',
  'title': 'Rank-by-Area Extract',
  'difficulty': 'medium',
  'skills': ['ranking', 'component areas', 'dynamic selection'],
  'staged_hint': 'The number of top-row markers tells you which ranked object to choose. Rank the objects by area, '
                 'then crop the selected one.',
  'written_solution': 'Count the 9 markers in the top row to get rank k. Sort the objects below by area from smallest '
                      'to largest and output the tight crop of the kth object.',
  'uses_new_primitive': False,
  'program_name': 'rule_m75',
  'program_source': 'def rule_m75(g):\n'
                    '    k=sum(1 for v in g[0] if v==9)\n'
                    '    comps=rowcol_sort_components(components_nonzero(g, treat_colors_separately=True, '
                    'ignore_positions={(0,c) for c in range(len(g[0]))}, ignore_colors={9}))\n'
                    '    comps=sorted(comps, key=lambda comp: (len(comp[1]),) + component_key(comp))\n'
                    '    sel=comps[k-1]\n'
                    '    return crop_bbox(g, sel[1])',
  'train': [{'input': ['9000000000000',
                       '0000000000000',
                       '0220003300000',
                       '0200003300000',
                       '0000000000000',
                       '0000000000400',
                       '0000000004440',
                       '0000000000400',
                       '0000000000000'],
             'output': ['22', '20']},
            {'input': ['99000000000000',
                       '00000000000000',
                       '00222000000000',
                       '00200000066600',
                       '00000000060600',
                       '05500000066600',
                       '05500000000000',
                       '05000000000000',
                       '00000000000000',
                       '00000000000000'],
             'output': ['55', '55', '50']},
            {'input': ['9990000000000',
                       '0000000000000',
                       '0333000400000',
                       '0030004440000',
                       '0000000400000',
                       '0000000077770',
                       '0000000070070',
                       '0000000077770',
                       '0000000000000'],
             'output': ['7777', '7007', '7777']},
            {'input': ['990000000000000',
                       '000000000000000',
                       '000000000000000',
                       '002200005550000',
                       '002200005050000',
                       '066666000000000',
                       '060606000000000',
                       '060606000000000',
                       '060606000000000',
                       '066666000000000',
                       '000000000000000'],
             'output': ['555', '505']}],
  'test': {'input': ['99900000000000',
                     '00000000000000',
                     '02200044000000',
                     '02000044000000',
                     '00000000666660',
                     '00000000606060',
                     '00000000606060',
                     '00000000606060',
                     '00000000666660',
                     '00000000000000'],
           'output': ['66666', '60606', '60606', '60606', '66666']}},
 {'id': 'M76',
  'title': 'Normalized Shape XOR',
  'difficulty': 'medium',
  'skills': ['normalization', 'shape comparison', 'binary overlays'],
  'staged_hint': 'Ignore the colors after locating the two objects. Normalize each object to its own crop, then '
                 'compare occupancy cell by cell.',
  'written_solution': 'Crop the two objects to their own bounding boxes, align both crops to the top-left of a shared '
                      'canvas, and output 8 exactly where one occupancy mask is on and the other is off.',
  'uses_new_primitive': False,
  'program_name': 'rule_m76',
  'program_source': 'def rule_m76(g):\n'
                    '    comps=rowcol_sort_components(components_nonzero(g, treat_colors_separately=True))\n'
                    "    # pick first two non-divider colors with largest components? We'll design only 2\n"
                    '    crops=[crop_bbox(g,cells) for col,cells in comps[:2]]\n'
                    '    h=max(len(crops[0]), len(crops[1]))\n'
                    '    w=max(len(crops[0][0]), len(crops[1][0]))\n'
                    '    a=pad_to([[1 if v!=0 else 0 for v in row] for row in crops[0]], h,w)\n'
                    '    b=pad_to([[1 if v!=0 else 0 for v in row] for row in crops[1]], h,w)\n'
                    '    out=blank(h,w)\n'
                    '    for r in range(h):\n'
                    '        for c in range(w):\n'
                    '            out[r][c]=8 if a[r][c] != b[r][c] else 0\n'
                    '    return out',
  'train': [{'input': ['000000000000',
                       '022200003330',
                       '020000000300',
                       '000000000000',
                       '000000000000',
                       '000000000000',
                       '000000000000'],
             'output': ['000', '880']},
            {'input': ['0000000000000',
                       '0000000000000',
                       '0022000000000',
                       '0022000003300',
                       '0000000000330',
                       '0000000000000',
                       '0000000000000',
                       '0000000000000'],
             'output': ['000', '808']},
            {'input': ['00000000000000',
                       '00000000000000',
                       '00200000000000',
                       '02220000003330',
                       '00200000003030',
                       '00000000000000',
                       '00000000000000',
                       '00000000000000',
                       '00000000000000'],
             'output': ['808', '080', '080']},
            {'input': ['000000000000',
                       '022000003330',
                       '022000003030',
                       '020000003330',
                       '000000000000',
                       '000000000000',
                       '000000000000',
                       '000000000000'],
             'output': ['008', '088', '088']}],
  'test': {'input': ['0000000000000',
                     '0000000000000',
                     '0200000000000',
                     '0220000000000',
                     '0022000003330',
                     '0000000003000',
                     '0000000000000',
                     '0000000000000',
                     '0000000000000'],
           'output': ['088', '080', '088']}},
 {'id': 'M77',
  'title': 'Legend-Ordered Assembly',
  'difficulty': 'medium',
  'skills': ['legend decoding', 'component extraction', 'packing'],
  'staged_hint': 'Read the top-row legend left to right. Then find those colored objects and pack their crops in that '
                 'same order.',
  'written_solution': 'Treat the nonzero top row as an ordering legend. Crop the matching objects and concatenate them '
                      'left to right in legend order with one blank separator column.',
  'uses_new_primitive': False,
  'program_name': 'rule_m77',
  'program_source': 'def rule_m77(g):\n'
                    '    legend=[v for v in g[0] if v!=0]\n'
                    '    comps=rowcol_sort_components(components_nonzero(g, treat_colors_separately=True, '
                    'ignore_positions={(0,c) for c in range(len(g[0]))}))\n'
                    '    by_color={}\n'
                    '    for col,cells in comps:\n'
                    '        by_color[col]=crop_bbox(g,cells)\n'
                    '    crops=[by_color[col] for col in legend]\n'
                    '    H=max(len(c) for c in crops)\n'
                    '    W=sum(len(c[0]) for c in crops)+(len(crops)-1)\n'
                    '    out=blank(H,W)\n'
                    '    x=0\n'
                    '    for i,crop in enumerate(crops):\n'
                    '        for r,row in enumerate(crop):\n'
                    '            for c,v in enumerate(row):\n'
                    '                out[r][x+c]=v\n'
                    '        x += len(crop[0])\n'
                    '        if i!=len(crops)-1:\n'
                    '            x += 1\n'
                    '    return out',
  'train': [{'input': ['32500000000000',
                       '00000000000000',
                       '00000033000000',
                       '02200033000000',
                       '02000000000000',
                       '00000000005550',
                       '00000000000500',
                       '00000000000000',
                       '00000000000000'],
             'output': ['330220555', '330200050']},
            {'input': ['640000000000000',
                       '000000000000000',
                       '000000000000000',
                       '004400000000000',
                       '004400000666000',
                       '004000000606000',
                       '000000000666000',
                       '000000000000000',
                       '000000000000000',
                       '000000000000000'],
             'output': ['666044', '606044', '666040']},
            {'input': ['5270000000000000',
                       '0000000000000000',
                       '0555000000000000',
                       '0505022200000000',
                       '0000020000007700',
                       '0000000000000770',
                       '0000000000000000',
                       '0000000000000000',
                       '0000000000000000'],
             'output': ['55502220770', '50502000077']},
            {'input': ['46300000000000000',
                       '00000000000000000',
                       '00000000000000000',
                       '00040000000000000',
                       '00444000000000000',
                       '00040000600000000',
                       '00000000660000000',
                       '00000000066003300',
                       '00000000000003300',
                       '00000000000000000',
                       '00000000000000000'],
             'output': ['0400600033', '4440660033', '0400066000']}],
  'test': {'input': ['752000000000000',
                     '000000000000000',
                     '000000000007770',
                     '000000055507070',
                     '000000050007770',
                     '022000000000000',
                     '022000000000000',
                     '000000000000000',
                     '000000000000000',
                     '000000000000000'],
           'output': ['7770555022', '7070500022', '7770000000']}},
 {'id': 'H71',
  'title': 'Overlapping Routed Links',
  'difficulty': 'hard',
  'skills': ['path routing', 'overlap handling', 'terminal pairing'],
  'staged_hint': 'Decode the routing command first. Then route every terminal pair, and only after that handle cells '
                 'claimed by more than one path.',
  'written_solution': 'Use the command-selected bend policy to connect every same-colored terminal pair. Any cell '
                      'traversed by multiple routed paths becomes overlap color 8.',
  'uses_new_primitive': True,
  'program_name': 'rule_h71',
  'program_source': 'def rule_h71(g):\n'
                    '    cmd=g[0][0]\n'
                    "    bend='row-first' if cmd==1 else 'col-first'\n"
                    '    endpoints=[(r,c,v) for r,row in enumerate(g) for c,v in enumerate(row) if v!=0 and not (r==0 '
                    'and c==0)]\n'
                    '    return link_terminals(g, endpoints, allow_bends=True, bend_policy=bend, overlap_color=8)',
  'train': [{'input': ['10000000', '00400300', '00000000', '00000000', '00000000', '00300400', '00000000', '00000000'],
             'output': ['10000000',
                        '00888800',
                        '00300400',
                        '00300400',
                        '00300400',
                        '00300400',
                        '00000000',
                        '00000000']},
            {'input': ['200000000',
                       '000000500',
                       '000000000',
                       '000000600',
                       '000000000',
                       '000000000',
                       '060500000',
                       '000000000',
                       '000000000'],
             'output': ['200000000',
                        '000000500',
                        '000000500',
                        '000000800',
                        '000000800',
                        '000000800',
                        '066888800',
                        '000000000',
                        '000000000']},
            {'input': ['1000000000',
                       '0000000000',
                       '0007000030',
                       '0000000000',
                       '0400000000',
                       '0000000000',
                       '0000000070',
                       '0000000000',
                       '0003004000',
                       '0000000000'],
             'output': ['1000000000',
                        '0000000000',
                        '0008888880',
                        '0003000070',
                        '0448444070',
                        '0003004070',
                        '0003004070',
                        '0003004000',
                        '0003004000',
                        '0000000000']},
            {'input': ['2000000000',
                       '0005000040',
                       '0000000000',
                       '0000000000',
                       '0000000000',
                       '0000000050',
                       '0004000000',
                       '0000000000'],
             'output': ['2000000000',
                        '0005000040',
                        '0005000040',
                        '0005000040',
                        '0005000040',
                        '0005555580',
                        '0004444440',
                        '0000000000']}],
  'test': {'input': ['1000000000',
                     '0060000300',
                     '0000000000',
                     '0000400000',
                     '0000000000',
                     '0000000000',
                     '0000000600',
                     '0030400000',
                     '0000000000'],
           'output': ['1000000000',
                      '0088888800',
                      '0030000600',
                      '0030400600',
                      '0030400600',
                      '0030400600',
                      '0030400600',
                      '0030400000',
                      '0000000000']}},
 {'id': 'H72',
  'title': 'Translation Analogy',
  'difficulty': 'hard',
  'skills': ['relational analogy', 'translation vectors', 'object transfer'],
  'staged_hint': 'Compare the 2-object pair before touching the target object. The shift from color 2 to color 3 is '
                 'the only transformation that matters.',
  'written_solution': 'Colors 2 and 3 show the same shape before and after a translation. Compute that translation '
                      'vector and apply it to the color-4 object on a blank output grid.',
  'uses_new_primitive': False,
  'program_name': 'rule_h72',
  'program_source': 'def rule_h72(g):\n'
                    '    # colors 2,3 define translation; color 4 target\n'
                    '    by_color=defaultdict(list)\n'
                    '    for r,row in enumerate(g):\n'
                    '        for c,v in enumerate(row):\n'
                    '            if v in (2,3,4):\n'
                    '                by_color[v].append((r,c))\n'
                    '    r20,c20,_,_ = bbox(by_color[2])\n'
                    '    r30,c30,_,_ = bbox(by_color[3])\n'
                    '    dr,dc = r30-r20, c30-c20\n'
                    '    h,w=size(g)\n'
                    '    out=blank(h,w)\n'
                    '    for r,c in by_color[4]:\n'
                    '        nr,nc=r+dr,c+dc\n'
                    '        out[nr][nc]=4\n'
                    '    return out',
  'train': [{'input': ['000000000000',
                       '022000000000',
                       '020000000000',
                       '000003300000',
                       '000003000000',
                       '004400000000',
                       '004400000000',
                       '000000000000',
                       '000000000000'],
             'output': ['000000000000',
                        '000000000000',
                        '000000000000',
                        '000000000000',
                        '000000000000',
                        '000000000000',
                        '000000000000',
                        '000000440000',
                        '000000440000']},
            {'input': ['0000000000000',
                       '0000044400000',
                       '0022240400000',
                       '0002000000000',
                       '0000000000000',
                       '0000003330000',
                       '0000000300000',
                       '0000000000000',
                       '0000000000000',
                       '0000000000000'],
             'output': ['0000000000000',
                        '0000000000000',
                        '0000000000000',
                        '0000000000000',
                        '0000000004440',
                        '0000000004040',
                        '0000000000000',
                        '0000000000000',
                        '0000000000000',
                        '0000000000000']},
            {'input': ['00000000000000',
                       '00000000022000',
                       '00000000444000',
                       '00000000420000',
                       '00000000000000',
                       '00003300000000',
                       '00003300000000',
                       '00003000000000',
                       '00000000000000'],
             'output': ['00000000000000',
                        '00000000000000',
                        '00000000000000',
                        '00000000000000',
                        '00000000000000',
                        '00000000000000',
                        '00044400000000',
                        '00040000000000',
                        '00000000000000']},
            {'input': ['000000000000000',
                       '000000000000000',
                       '020000000000000',
                       '022000000000000',
                       '002200000000000',
                       '000444030000000',
                       '000404033000000',
                       '000444003300000',
                       '000000000000000',
                       '000000000000000',
                       '000000000000000'],
             'output': ['000000000000000',
                        '000000000000000',
                        '000000000000000',
                        '000000000000000',
                        '000000000000000',
                        '000000000000000',
                        '000000000000000',
                        '000000000000000',
                        '000000000444000',
                        '000000000404000',
                        '000000000444000']}],
  'test': {'input': ['00000000000000',
                     '00004400000000',
                     '00222440000000',
                     '00200000000000',
                     '00000000000000',
                     '00000000000000',
                     '00000003330000',
                     '00000003000000',
                     '00000000000000',
                     '00000000000000'],
           'output': ['00000000000000',
                      '00000000000000',
                      '00000000000000',
                      '00000000000000',
                      '00000000000000',
                      '00000000044000',
                      '00000000004400',
                      '00000000000000',
                      '00000000000000',
                      '00000000000000']}},
 {'id': 'H73',
  'title': 'Nested Frame Depth Map',
  'difficulty': 'hard',
  'skills': ['containment depth', 'nested rectangles', 'count-based recoloring'],
  'staged_hint': 'Ignore the original colors once you identify the frames. What matters is how many nested rectangles '
                 'contain each cell.',
  'written_solution': 'Find the rectangular frames and count, for every grid cell, how many frame bounding boxes '
                      'contain it. Output that containment depth as the new color, leaving outside cells at 0.',
  'uses_new_primitive': False,
  'program_name': 'rule_h73',
  'program_source': 'def rule_h73(g):\n'
                    '    h,w=size(g)\n'
                    '    comps=components_nonzero(g, treat_colors_separately=True)\n'
                    '    rects=[]\n'
                    '    for col,cells in comps:\n'
                    '        r0,c0,r1,c1=bbox(cells)\n'
                    '        rects.append((r0,c0,r1,c1))\n'
                    '    out=blank(h,w)\n'
                    '    for r in range(h):\n'
                    '        for c in range(w):\n'
                    '            depth=sum(1 for r0,c0,r1,c1 in rects if r0<=r<=r1 and c0<=c<=c1)\n'
                    '            out[r][c]=depth\n'
                    '    return out',
  'train': [{'input': ['000000000',
                       '022222220',
                       '020000020',
                       '020333020',
                       '020303020',
                       '020333020',
                       '020000020',
                       '022222220',
                       '000000000'],
             'output': ['000000000',
                        '011111110',
                        '011111110',
                        '011222110',
                        '011222110',
                        '011222110',
                        '011111110',
                        '011111110',
                        '000000000']},
            {'input': ['000000000000',
                       '044444444440',
                       '040000000040',
                       '040555555040',
                       '040500005040',
                       '040500005040',
                       '040555555040',
                       '040000000040',
                       '044444444440',
                       '000000000000'],
             'output': ['000000000000',
                        '011111111110',
                        '011111111110',
                        '011222222110',
                        '011222222110',
                        '011222222110',
                        '011222222110',
                        '011111111110',
                        '011111111110',
                        '000000000000']},
            {'input': ['00000000000',
                       '02222222220',
                       '02000000020',
                       '02066666020',
                       '02064446020',
                       '02064046020',
                       '02064446020',
                       '02066666020',
                       '02000000020',
                       '02222222220',
                       '00000000000'],
             'output': ['00000000000',
                        '01111111110',
                        '01111111110',
                        '01122222110',
                        '01123332110',
                        '01123332110',
                        '01123332110',
                        '01122222110',
                        '01111111110',
                        '01111111110',
                        '00000000000']},
            {'input': ['00000000000000',
                       '03333333333330',
                       '03000000000030',
                       '03055555555030',
                       '03050000005030',
                       '03050777705030',
                       '03050777705030',
                       '03050000005030',
                       '03055555555030',
                       '03000000000030',
                       '03333333333330',
                       '00000000000000'],
             'output': ['00000000000000',
                        '01111111111110',
                        '01111111111110',
                        '01122222222110',
                        '01122222222110',
                        '01122333322110',
                        '01122333322110',
                        '01122222222110',
                        '01122222222110',
                        '01111111111110',
                        '01111111111110',
                        '00000000000000']}],
  'test': {'input': ['0000000000000',
                     '0222222222220',
                     '0204444444020',
                     '0204000004020',
                     '0204066604020',
                     '0204060604020',
                     '0204066604020',
                     '0204000004020',
                     '0204444444020',
                     '0222222222220',
                     '0000000000000'],
           'output': ['0000000000000',
                      '0111111111110',
                      '0112222222110',
                      '0112222222110',
                      '0112233322110',
                      '0112233322110',
                      '0112233322110',
                      '0112222222110',
                      '0112222222110',
                      '0111111111110',
                      '0000000000000']}},
 {'id': 'H74',
  'title': 'Symmetry Equivalence Matrix',
  'difficulty': 'hard',
  'skills': ['dihedral symmetry', 'shape normalization', 'relation matrices'],
  'staged_hint': 'Normalize the objects before comparing them. Two shapes match if one can be rotated or reflected '
                 'into the other.',
  'written_solution': 'Crop the three objects, ignore their colors, and compare their binary shapes up to any rotation '
                      'or reflection. Output 8 where two objects are dihedrally equivalent and 0 otherwise.',
  'uses_new_primitive': False,
  'program_name': 'rule_h74',
  'program_source': 'def rule_h74(g):\n'
                    '    comps=rowcol_sort_components(components_nonzero(g, treat_colors_separately=True))\n'
                    '    bins=[]\n'
                    '    for col,cells in comps:\n'
                    '        crop=crop_bbox(g,cells)\n'
                    '        bins.append(normalize_binary(crop))\n'
                    '    n=len(bins)\n'
                    '    vars=[set(dihedral_variants(b)) for b in bins]\n'
                    '    out=blank(n,n)\n'
                    '    for i in range(n):\n'
                    '        for j in range(n):\n'
                    '            out[i][j]=8 if bins[j] in vars[i] else 0\n'
                    '    return out',
  'train': [{'input': ['00000000000000',
                       '02220033000000',
                       '02000003000000',
                       '00000003000000',
                       '00000000000000',
                       '00000000004440',
                       '00000000000400',
                       '00000000000000',
                       '00000000000000'],
             'output': ['880', '880', '008']},
            {'input': ['0000000000000',
                       '0220000000000',
                       '0022000000000',
                       '0000000550000',
                       '0000005500000',
                       '0000000000660',
                       '0000000000660',
                       '0000000000000'],
             'output': ['880', '880', '008']},
            {'input': ['000000000000000',
                       '000000000000000',
                       '033000044000000',
                       '033000044000000',
                       '030000004000000',
                       '000000000007770',
                       '000000000000770',
                       '000000000000000',
                       '000000000000000',
                       '000000000000000'],
             'output': ['888', '888', '888']},
            {'input': ['00000000000000',
                       '02220000000000',
                       '02020000550000',
                       '02220000550000',
                       '00000000000000',
                       '00000000000660',
                       '00000000000660',
                       '00000000000000',
                       '00000000000000'],
             'output': ['800', '088', '088']}],
  'test': {'input': ['000000000000000',
                     '022000000000000',
                     '020000000000000',
                     '000000440000000',
                     '000000040000000',
                     '000000000000000',
                     '000000000077700',
                     '000000000070700',
                     '000000000000000',
                     '000000000000000'],
           'output': ['880', '880', '008']}},
 {'id': 'H75',
  'title': 'Command Composition Transform',
  'difficulty': 'hard',
  'skills': ['sequential transforms', 'command execution', 'cropped outputs'],
  'staged_hint': 'Do not collapse the commands into one guess. Apply them in the given order to the cropped template.',
  'written_solution': 'Read the nonzero command strip from the top row left to right, crop the lower object, and apply '
                      'the listed transforms in sequence: rotate, flip, or transpose.',
  'uses_new_primitive': False,
  'program_name': 'rule_h75',
  'program_source': 'def rule_h75(g):\n'
                    '    cmds=[]\n'
                    '    for v in g[0]:\n'
                    '        if v==0: break\n'
                    '        cmds.append(v)\n'
                    '    cells=[(r,c) for r in range(1,len(g)) for c,v in enumerate(g[r]) if v!=0]\n'
                    '    obj=crop_bbox(g,cells)\n'
                    '    cur=obj\n'
                    '    for cmd in cmds:\n'
                    '        if cmd==1:\n'
                    '            cur=rotate_cw(cur)\n'
                    '        elif cmd==2:\n'
                    '            cur=flip_h(cur)\n'
                    '        elif cmd==3:\n'
                    '            cur=flip_v(cur)\n'
                    '        elif cmd==4:\n'
                    '            cur=transpose(cur)\n'
                    '        else:\n'
                    '            raise ValueError(cmd)\n'
                    '    return cur',
  'train': [{'input': ['1000000000',
                       '0000000000',
                       '0000000000',
                       '0012000000',
                       '0034000000',
                       '0000000000',
                       '0000000000',
                       '0000000000'],
             'output': ['31', '42']},
            {'input': ['21000000000',
                       '00000000000',
                       '00000000000',
                       '00000500000',
                       '00000067000',
                       '00000008000',
                       '00000000000',
                       '00000000000',
                       '00000000000'],
             'output': ['870', '060', '005']},
            {'input': ['430000000000',
                       '000000000000',
                       '000000000000',
                       '000000000000',
                       '002200000000',
                       '002030000000',
                       '000440000000',
                       '000000000000',
                       '000000000000',
                       '000000000000'],
             'output': ['034', '204', '220']},
            {'input': ['1210000000',
                       '0000000000',
                       '0000000000',
                       '0000123000',
                       '0000405000',
                       '0000000000',
                       '0000000000',
                       '0000000000',
                       '0000000000'],
             'output': ['321', '504']}],
  'test': {'input': ['34100000000',
                     '00000000000',
                     '00000000000',
                     '00000000000',
                     '00012000000',
                     '00034000000',
                     '00000000000',
                     '00000000000',
                     '00000000000'],
           'output': ['43', '21']}},
 {'id': 'H76',
  'title': 'Chamber Ownership Fill',
  'difficulty': 'hard',
  'skills': ['flood fill', 'wall topology', 'region ownership'],
  'staged_hint': 'Use the 9s only as walls. Flood the open chambers, identify which chamber contains which marker, and '
                 'then fill chamber interiors accordingly.',
  'written_solution': 'Treat 9 as an impassable wall. For each open chamber, if it contains exactly one marker color, '
                      'fill the whole chamber with that color while keeping walls unchanged.',
  'uses_new_primitive': False,
  'program_name': 'rule_h76',
  'program_source': 'def rule_h76(g):\n'
                    '    h,w=size(g)\n'
                    '    out=blank(h,w)\n'
                    '    for r in range(h):\n'
                    '        for c in range(w):\n'
                    '            if g[r][c]==9:\n'
                    '                out[r][c]=9\n'
                    '    vis=[[False]*w for _ in range(h)]\n'
                    '    for r in range(h):\n'
                    '        for c in range(w):\n'
                    '            if g[r][c]==9 or vis[r][c]:\n'
                    '                continue\n'
                    '            vis[r][c]=True\n'
                    '            q=[(r,c)]\n'
                    '            region=[]\n'
                    '            colors=set()\n'
                    '            while q:\n'
                    '                rr,cc=q.pop()\n'
                    '                region.append((rr,cc))\n'
                    '                if g[rr][cc] not in (0,9):\n'
                    '                    colors.add(g[rr][cc])\n'
                    '                for dr,dc in DIR4:\n'
                    '                    nr,nc=rr+dr,cc+dc\n'
                    '                    if 0<=nr<h and 0<=nc<w and not vis[nr][nc] and g[nr][nc]!=9:\n'
                    '                        vis[nr][nc]=True; q.append((nr,nc))\n'
                    '            fill = next(iter(colors)) if len(colors)==1 else 0\n'
                    '            for rr,cc in region:\n'
                    '                if fill and g[rr][cc]==0:\n'
                    '                    out[rr][cc]=fill\n'
                    '                elif g[rr][cc]!=0 and g[rr][cc]!=9:\n'
                    '                    out[rr][cc]=g[rr][cc]\n'
                    '    return out',
  'train': [{'input': ['999999999',
                       '920090039',
                       '900090009',
                       '900090009',
                       '999999999',
                       '940090059',
                       '900090009',
                       '900090009',
                       '999999999'],
             'output': ['999999999',
                        '922293339',
                        '922293339',
                        '922293339',
                        '999999999',
                        '944495559',
                        '944495559',
                        '944495559',
                        '999999999']},
            {'input': ['9999999999',
                       '9500092009',
                       '9000090009',
                       '9000090009',
                       '9999999999',
                       '9300094009',
                       '9000090009',
                       '9000090009',
                       '9999999999'],
             'output': ['9999999999',
                        '9555592229',
                        '9555592229',
                        '9555592229',
                        '9999999999',
                        '9333394449',
                        '9333394449',
                        '9333394449',
                        '9999999999']},
            {'input': ['99999999999',
                       '96000900039',
                       '90000900009',
                       '90000900009',
                       '99999999999',
                       '92000950009',
                       '90000900009',
                       '90000900009',
                       '99999999999'],
             'output': ['99999999999',
                        '96666933339',
                        '96666933339',
                        '96666933339',
                        '99999999999',
                        '92222955559',
                        '92222955559',
                        '92222955559',
                        '99999999999']},
            {'input': ['999999999',
                       '970090009',
                       '900090009',
                       '900090009',
                       '999999999',
                       '900090009',
                       '900050009',
                       '900090009',
                       '999999999'],
             'output': ['999999999',
                        '977790009',
                        '977790009',
                        '977790009',
                        '999999999',
                        '955595559',
                        '955555559',
                        '955595559',
                        '999999999']}],
  'test': {'input': ['9999999999',
                     '9200096009',
                     '9000090009',
                     '9000090009',
                     '9999999999',
                     '9300094009',
                     '9000090009',
                     '9000090009',
                     '9999999999'],
           'output': ['9999999999',
                      '9222296669',
                      '9222296669',
                      '9222296669',
                      '9999999999',
                      '9333394449',
                      '9333394449',
                      '9333394449',
                      '9999999999']}},
 {'id': 'H77',
  'title': 'Hole-Count Packing',
  'difficulty': 'hard',
  'skills': ['hole counting', 'object ranking', 'normalized packing'],
  'staged_hint': "Measure each object's holes before packing anything. Once ranked, just crop and place them side by "
                 'side.',
  'written_solution': "Count the enclosed holes in each object's tight crop, sort the objects by hole count from "
                      'fewest to most, and pack the cropped shapes left to right with one blank separator column.',
  'uses_new_primitive': False,
  'program_name': 'rule_h77',
  'program_source': 'def rule_h77(g):\n'
                    '    comps=rowcol_sort_components(components_nonzero(g, treat_colors_separately=True))\n'
                    '    items=[]\n'
                    '    for idx,(col,cells) in enumerate(comps):\n'
                    '        crop=crop_bbox(g,cells)\n'
                    '        items.append((count_holes(crop), idx, crop))\n'
                    '    items.sort(key=lambda x:(x[0],x[1]))\n'
                    '    crops=[crop for _,_,crop in items]\n'
                    '    H=max(len(c) for c in crops)\n'
                    '    W=sum(len(c[0]) for c in crops)+(len(crops)-1)\n'
                    '    out=blank(H,W)\n'
                    '    x=0\n'
                    '    for i,crop in enumerate(crops):\n'
                    '        for r,row in enumerate(crop):\n'
                    '            for c,v in enumerate(row):\n'
                    '                out[r][x+c]=v\n'
                    '        x += len(crop[0])\n'
                    '        if i!=len(crops)-1:\n'
                    '            x += 1\n'
                    '    return out',
  'train': [{'input': ['000000000000000000',
                       '022200000000000000',
                       '020200003330000000',
                       '022200003000000000',
                       '000000000000000000',
                       '000000000000444440',
                       '000000000000404040',
                       '000000000000404040',
                       '000000000000404040',
                       '000000000000444440',
                       '000000000000000000'],
             'output': ['3330222044444', '3000202040404', '0000222040404', '0000000040404', '0000000044444']},
            {'input': ['00000000000000000',
                       '05555500000000000',
                       '05050500002200000',
                       '05050500002200000',
                       '05050500000000000',
                       '05555566660000000',
                       '00000060060000000',
                       '00000066660000000',
                       '00000000000000000',
                       '00000000000000000'],
             'output': ['2206666055555', '2206006050505', '0006666050505', '0000000050505', '0000000055555']},
            {'input': ['000000000000000000',
                       '000000000000000000',
                       '007700000000000000',
                       '007000000000000000',
                       '000000000004444400',
                       '000000000004040400',
                       '000000000004040400',
                       '000003330004040400',
                       '000003030004444400',
                       '000003330000000000',
                       '000000000000000000',
                       '000000000000000000'],
             'output': ['770333044444', '700303040404', '000333040404', '000000040404', '000000044444']},
            {'input': ['00000000000000000',
                       '02222000000000000',
                       '02002000000000000',
                       '02222000055000000',
                       '00000000055000000',
                       '00000000050666660',
                       '00000000000606060',
                       '00000000000606060',
                       '00000000000606060',
                       '00000000000666660',
                       '00000000000000000'],
             'output': ['5502222066666', '5502002060606', '5002222060606', '0000000060606', '0000000066666']}],
  'test': {'input': ['000000000000000000',
                     '022222000000000000',
                     '020202000444000000',
                     '020202000400000000',
                     '020202000000000000',
                     '022222000000000000',
                     '000000000000066600',
                     '000000000000060600',
                     '000000000000066600',
                     '000000000000000000',
                     '000000000000000000',
                     '000000000000000000'],
           'output': ['4440666022222', '4000606020202', '0000666020202', '0000000020202', '0000000022222']}}]


def validate_all(verbose=True):
    checked = 0
    for puzzle in PUZZLES:
        rule = RULES[puzzle["program_name"]]
        for pair in puzzle["train"]:
            got = strings_from_grid(rule(grid_from_strings(pair["input"])))
            if got != pair["output"]:
                raise AssertionError(f'{puzzle["id"]} train mismatch')
            checked += 1
        got = strings_from_grid(rule(grid_from_strings(puzzle["test"]["input"])))
        if got != puzzle["test"]["output"]:
            raise AssertionError(f'{puzzle["id"]} test mismatch')
        checked += 1
    if verbose:
        print(f'validated {len(PUZZLES)} puzzles / {checked} pairs')
    return True

if __name__ == "__main__":
    validate_all()
