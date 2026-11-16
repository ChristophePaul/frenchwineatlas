"""Read shape geometry out of « Drawing France the Easy way.pptx » (the drawing slides).
leaves(zipfile, slide_no) -> {shape_id: dict(name, prst, d, m, w, h, text)} in slide points (720 x 540)."""
import math
import xml.etree.ElementTree as ET

NS = {'p': 'http://schemas.openxmlformats.org/presentationml/2006/main',
      'a': 'http://schemas.openxmlformats.org/drawingml/2006/main'}
EMU = 12700.0


class M:
    def __init__(s, a=1, b=0, c=0, d=1, e=0, f=0):
        s.v = (a, b, c, d, e, f)

    def __mul__(s, o):
        a, b, c, d, e, f = s.v
        A, B, C, D, E, F = o.v
        return M(a * A + c * B, b * A + d * B, a * C + c * D, b * C + d * D, a * E + c * F + e, b * E + d * F + f)

    def pt(s, x, y):
        a, b, c, d, e, f = s.v
        return a * x + c * y + e, b * x + d * y + f

    def svg(s):
        return 'matrix(%s)' % ','.join(('%.4f' % x).rstrip('0').rstrip('.') for x in s.v)


def T(x, y): return M(1, 0, 0, 1, x, y)
def S(x, y): return M(x, 0, 0, y, 0, 0)


def R(deg):
    r = math.radians(deg)
    return M(math.cos(r), math.sin(r), -math.sin(r), math.cos(r), 0, 0)


def _box(x):
    off = x.find('a:off', NS); ext = x.find('a:ext', NS)
    X, Y = int(off.get('x')) / EMU, int(off.get('y')) / EMU
    w, h = int(ext.get('cx')) / EMU, int(ext.get('cy')) / EMU
    rot = int(x.get('rot', '0')) / 60000.0
    fh, fv = x.get('flipH') == '1', x.get('flipV') == '1'
    return T(X + w / 2, Y + h / 2) * R(rot) * S(-1 if fh else 1, -1 if fv else 1) * T(-w / 2, -h / 2), w, h


def _adj(el, name, default):
    for gd in el.iterfind('.//a:prstGeom/a:avLst/a:gd', NS):
        if gd.get('name') == name:
            return int(gd.get('fmla').split()[1])
    return default


def _ell(rx, ry, ang):
    a = math.radians(ang)
    phi = math.atan2(rx * math.sin(a), ry * math.cos(a))
    return rx + rx * math.cos(phi), ry + ry * math.sin(phi)


def _path(el, prst, w, h):
    f = lambda v: ('%.2f' % v).rstrip('0').rstrip('.')
    if prst in ('line', 'straightConnector1'):
        return 'M0,0L%s,%s' % (f(w), f(h))
    if prst == 'hexagon':
        a = _adj(el, 'adj', 25000); vf = _adj(el, 'vf', 115470)
        x1 = min(w, h) * a / 100000.0; dy = h / 2 * vf / 100000.0 * math.sin(math.radians(60)); vc = h / 2
        pts = [(0, vc), (x1, vc - dy), (w - x1, vc - dy), (w, vc), (w - x1, vc + dy), (x1, vc + dy)]
        return 'M' + 'L'.join('%s,%s' % (f(p[0]), f(p[1])) for p in pts) + 'Z'
    if prst == 'arc':
        st = _adj(el, 'adj1', 16200000) / 60000.0; en = _adj(el, 'adj2', 0) / 60000.0
        p0 = _ell(w / 2, h / 2, st); p1 = _ell(w / 2, h / 2, en)
        return 'M%s,%sA%s,%s 0 %d 1 %s,%s' % (f(p0[0]), f(p0[1]), f(w / 2), f(h / 2), 1 if (en - st) % 360 > 180 else 0, f(p1[0]), f(p1[1]))
    if prst in ('ellipse', 'donut'):
        return 'M0,%sA%s,%s 0 1 1 %s,%sA%s,%s 0 1 1 0,%sZ' % (f(h / 2), f(w / 2), f(h / 2), f(w), f(h / 2), f(w / 2), f(h / 2), f(h / 2))
    return None


def _adj_from(lf, name, default):
    return lf['adj'].get(name, default)


def leaves(zf, n):
    root = ET.fromstring(zf.read('ppt/slides/slide%d.xml' % n))
    out = {}

    def walk(el, pm, grp):
        tag = el.tag.split('}')[1]
        if tag == 'grpSp':
            x = el.find('./p:grpSpPr/a:xfrm', NS)
            m, w, h = _box(x)
            co = x.find('a:chOff', NS); ce = x.find('a:chExt', NS)
            sx = w / (int(ce.get('cx')) / EMU) if int(ce.get('cx')) else 1
            sy = h / (int(ce.get('cy')) / EMU) if int(ce.get('cy')) else 1
            cm = pm * m * S(sx, sy) * T(-int(co.get('x')) / EMU, -int(co.get('y')) / EMU)
            gid = el.find('.//p:cNvPr', NS).get('id')
            for ch in el:
                if ch.tag.split('}')[1] in ('sp', 'cxnSp', 'grpSp'):
                    walk(ch, cm, grp + [gid])
            return
        x = el.find('./p:spPr/a:xfrm', NS)
        if x is None:
            return
        m, w, h = _box(x)
        nv = el.find('.//p:cNvPr', NS)
        g = el.find('./p:spPr/a:prstGeom', NS)
        prst = g.get('prst') if g is not None else 'rect'
        text = '\n'.join(''.join(r.text or '' for r in p.iterfind('.//a:t', NS)) for p in el.iterfind('.//p:txBody/a:p', NS)).strip()
        adj = {gd.get('name'): int(gd.get('fmla').split()[1]) for gd in el.iterfind('.//a:prstGeom/a:avLst/a:gd', NS)}
        out[nv.get('id')] = dict(name=nv.get('name'), prst=prst, d=_path(el, prst, w, h), m=pm * m, w=w, h=h,
                                 text=text, groups=grp, adj=adj)

    for el in root.find('.//p:cSld/p:spTree', NS):
        if el.tag.split('}')[1] in ('sp', 'cxnSp', 'grpSp'):
            walk(el, M(), [])
    return out
