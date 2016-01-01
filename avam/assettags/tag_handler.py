import random
import xml.etree.ElementTree as ET

import qrcode
from qrcode.image.svg import SvgPathFillImage

from assettags import settings

def _generate_code(num_chars=None):
    if num_chars is None:
        num_chars = settings.ASSET_TAG_LENGTH
    choices = settings.ASSET_TAG_CHARS
    return ''.join(random.choice(choices) for i in range(num_chars))
    
def generate_code(num_chars=None):
    f = settings.ASSET_TAG_GENERATE_FUNCTION
    if f is not None:
        return f(num_chars)
    return _generate_code(num_chars)

class SvgScaledImage(SvgPathFillImage):
    def __init__(self, *args, **kwargs):
        super(SvgScaledImage, self).__init__(*args, **kwargs)
    def to_string(self):
        self._img.append(self.make_path())
        return ET.tostring(self._img)
    def get_path_centered(self):
        main_g = ET.Element('g', id='qr-box-outer')
        inner_g = ET.Element(
            'g',
            id='qr-box-inner',
            transform='translate(-14.5, -14.5)',
        )
        inner_g.append(self.make_path())
        main_g.append(inner_g)
        return main_g
#    def _svg(self, viewBox=None, **kwargs):
#        elem = super(SvgScaledImage, self)._svg(viewBox, **kwargs)
#        elem.set('width', self.scale)
#        elem.set('height', self.scale)
#        return elem

def build_qr_svg(code_str, **kwargs):
    kwargs.setdefault('image_factory', SvgScaledImage)
    return qrcode.make(code_str, **kwargs)

class AssetTagImage(object):
    def __init__(self, **kwargs):
        self.asset_tag = kwargs.get('asset_tag')
        self.template = kwargs.get('template')
        self.image_format = kwargs.get('image_format', 'svg')
        self.qr_img = build_qr_svg(self.asset_tag.code)
        self.qr_img._img.set('width', '100%')
        self.qr_img._img.set('height', '100%')
        self.svg = self.build_svg()
    @property
    def qr_svg_bytes(self):
        b = getattr(self, '_qr_svg_bytes', None)
        if b is None:
            b = self._qr_svg_bytes = self.get_qr_svg_bytes()
        return b
    def get_qr_svg_bytes(self):
        return ET.tostring(self.svg)
    def build_svg(self):
        w = self.template.width
        h = self.template.height
        root = ET.Element(
            'svg',
            width='%spx' % (w),
            height='%spx' % (h),
            viewBox='0 0 %s %s' % (w, h),
            version='1.1',
        )
        root.set('xmlns', SvgPathFillImage._SVG_namespace)
        root.extend(self.build_svg_content())
        return root
    def build_svg_content(self):
        elems = []
        w = self.template.width
        h = self.template.height
        elems.append(ET.Element(
            'rect',
            width=str(w),
            height=str(h),
            id='bg-rect',
            style='fill:white;stroke:black;',
        ))
        if self.template.header_text:
            elems.append(self.build_header())
        code_text = self.build_code_text()
        if code_text is not None:
            elems.append(code_text)
        elems.append(self.build_qr_group())
        return elems
    def build_header(self):
        w = self.template.width
        g = ET.Element('g', id='header-group', transform='translate(%s, 0.0)' % (w / 2.))
        t = ET.Element(
            'text',
            id='header-text',
            x='0',
            y='0',
            style='font-size:13px;font-style:normal;font-weight:normal;text-align:center;line-height:125%;letter-spacing:0px;word-spacing:0px;text-anchor:middle;fill:#000000;fill-opacity:1;stroke:none;font-family:sans-serif;dominant-baseline:text-before-edge',
        )
        t.set('xml:space', 'preserve')
        tspan = ET.Element('tspan', x='0', y='0', id='header-tspan')
        tspan.text = self.template.header_text
        t.append(tspan)
        g.append(t)
        return g
    def build_code_text(self):
        x = self.template.width / 2.
        h = self.template.height
        loc = self.template.get_code_text_location_display()
        if loc == 'Above':
            y = h * .1
            baseline = 'hanging'
        elif loc == 'Below':
            y = h - (h * .05)
            baseline = 'no-change'
        else:
            return None
        g = ET.Element('g', id='code-text-group', transform='translate(%s, %s)' % (x, y))
        t = ET.Element(
            'text',
            id='code-text',
            x='0',
            y='0',
            style='font-size:9px;font-style:normal;font-weight:normal;text-align:center;line-height:125%;letter-spacing:0px;word-spacing:0px;text-anchor:middle;fill:#000000;fill-opacity:1;stroke:none;font-family:sans-serif;dominant-baseline:{0}'.format(baseline),
        )
        t.set('xml:space', 'preserve')
        tspan = ET.Element('tspan', x='0', y='0', id='code-text-tspan')
        tspan.text = str(self.asset_tag.code)
        t.append(tspan)
        g.append(t)
        return g
    def build_qr_group(self):
        w = self.template.width
        h = self.template.height
        loc = self.template.get_code_text_location_display()
        x = w / 2.
        y = h / 2.
        if loc == 'Above':
            y += h * .1
        scale = 3
        g = self.qr_img.get_path_centered()
        g.set('transform', 'matrix(%s, 0, 0, %s, %s, %s)' % (scale, scale, x, y))
        return g

class AssetTagSheet(object):
    def __init__(self, **kwargs):
        self.asset_tags = kwargs.get('asset_tags')
        self.asset_tag_template = kwargs.get('asset_tag_template')
        self.page_template = kwargs.get('page_template')
        self.full_area = self.page_template.get_full_area()
        self.print_area = self.page_template.get_printable_area()
        self.cells = self.page_template.get_cells()
        self.tag_scale = self.calc_tag_scale()
    def build_all(self):
        svgs = []
        svg, tags = self.build_svg()
        svgs.append(svg)
        while len(tags):
            svg, tags = self.build_svg(tags)
            svgs.append(svg)
        return svgs
    def build_svg(self, asset_tags=None):
        if asset_tags is None:
            asset_tags = self.asset_tags
        box = self.full_area
        root = ET.Element(
            'svg',
            width='%spx' % (box.w),
            height='%spx' % (box.h),
            viewBox='0 0 %s %s' % (box.w, box.h),
            version='1.1',
        )
        root.set('xmlns', SvgPathFillImage._SVG_namespace)
        cells, tags_remaining = self.build_cells(asset_tags)
        root.extend(cells)
        return root, tags_remaining
    def build_cells(self, asset_tags):
        built_cells = []
        asset_tags = list(asset_tags)[:]
        for cell in self.cells:
            if not len(asset_tags):
                break
            asset_tag = asset_tags[0]
            asset_tags = asset_tags[1:]
            built_cells.append(self.build_cell(asset_tag, cell))
        return built_cells, asset_tags
    def build_cell(self, asset_tag, cell):
        g = ET.Element(
            'g',
            width=str(cell.w),
            height=str(cell.h),
            transform='translate(%s,%s)' % (cell.x, cell.y),
        )
        rect = ET.Element(
            'rect',
            width=str(cell.w),
            height=str(cell.h),
            style='fill:white;stroke:black;',
        )
        g.append(rect)
        t = self.asset_tag_template
        x = (cell.w / 2.) - (t.width / 2.)
        y = (cell.h / 2.) - (t.height / 2.)
        sub_g = ET.Element(
            'g',
            transform='translate(%s,%s)' % (x, y),
        )
        timage = AssetTagImage(asset_tag=asset_tag, template=self.asset_tag_template)
        sub_g.extend(timage.build_svg_content())
        g.append(sub_g)
        return g
    def calc_tag_scale(self):
        cell = self.cells[0]
        template = self.asset_tag_template
        wscale = cell.w / template.width
        hscale = cell.h / template.height
        if template.width * wscale > cell.w or template.height * wscale > cell.h:
            return hscale
        return wscale

def sheet_test():
    from assettags.models import AssetTag,AssetTagImageTemplate,AssetTagPrintTemplate
    ts = AssetTagSheet(
        asset_tags=AssetTag.objects.all(),
        asset_tag_template=AssetTagImageTemplate.get_default_template(),
        page_template=AssetTagPrintTemplate.objects.first(),
    )
    svg, tags = ts.build_svg()
    t = ET.ElementTree(svg)
    t.write('sheettest2.svg')
