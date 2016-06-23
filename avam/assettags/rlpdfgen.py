import os
import tempfile
import json
import shutil

from reportlab.pdfgen.canvas import Canvas
from reportlab import platypus
from reportlab.platypus.figures import ImageFigure
from reportlab.lib import units as rl_units

def unit_to_rl(*units):
    for unit in units:
        lbl = getattr(unit, 'unit_label', None)
        if lbl is None or lbl == 'px':
            yield unit.value
        else:
            clsname = unit.__class__.__name__.lower()
            rl_unit = getattr(rl_units, clsname)
            yield unit.value * rl_unit

def unit_to_str(*units):
    for unit in units:
        lbl = getattr(unit, 'unit_label', None)
        if lbl is None or lbl == 'px':
            yield '{}pt'.format(unit.value)
        else:
            yield str(unit)

class Document(object):
    def __init__(self, context_data):
        self.context_data = context_data
        self.temp_dir = None
        self.frames = {}
        self.pages = {}
        self.tags = {}
    def open(self):
        if self.temp_dir is not None:
            return
        self.temp_dir = tempfile.mkdtemp()
        self.tag_dir = os.path.join(self.temp_dir, 'tag_pngs')
        os.makedirs(self.tag_dir)
        self.filename = os.path.join(self.temp_dir, 'tag_sheet.pdf')
    def close(self):
        if self.temp_dir is not None:
            shutil.rmtree(self.temp_dir)
            self.temp_dir = None
    def __enter__(self):
        self.open()
        self.render()
        return self
    def __exit__(self, *args):
        self.close()
    def render(self):
        self.open()
        self.canvas = self.build_canvas()
        self.canvas_size = self.canvas._pagesize
        for page, row, col, tag, cell in self.context_data['cell_iter']:
            self.add_tag(page, row, col, tag, cell)
        self.page_template = platypus.PageTemplate(
            id=None,
            frames=[f.frame for f in self.frames.values()],
        )
        for page_num in sorted(self.pages.keys()):
            page = self.pages[page_num]
            page.render()
            self.canvas.showPage()
        self.canvas.save()
    def build_canvas(self):
        b = self.context_data['page_box']
        c = Canvas(
            filename=self.filename,
            pagesize=[v for v in unit_to_rl(b.w, b.h)],
        )
        return c
    def add_frame(self, row, col, cell):
        f = Frame(row, col, cell)
        self.frames[f.id] = f
        return f
    def add_page(self, page_num):
        page = Page(self, page_num)
        self.pages[page_num] = page
        return page
    def add_tag(self, page, row, col, tag, cell):
        if page not in self.tags:
            self.tags[page] = {}
        obj = Tag(self, page, row, col, tag, cell)
        self.tags[page][obj.id] = obj
        return obj

class Frame(object):
    def __init__(self, row, col, cell):
        self.cell = cell
        self.id = (row, col)
        keys = (('x', 'x1'), ('y', 'y1'), ('w', 'width'), ('h', 'height'))
        vals = [v for v in unit_to_rl(*[getattr(cell, k[0]) for k in keys])]
        fkwargs = {k[1]:v for k, v in zip(keys, vals)}
        fkwargs['id'] = '{}_{}'.format(*self.id)
        fkwargs['showBoundary'] = 1
        self.frame = platypus.Frame(**fkwargs)

class Page(object):
    def __init__(self, doc, page_num):
        self.doc = doc
        self.page_num = page_num
    def get_tags(self):
        return self.doc.tags[self.page_num]
    def render(self):
        for tag in self.get_tags().values():
            tag.render()

class Tag(object):
    def __init__(self, doc, page, row, col, tag, cell):
        self.doc = doc
        self.tag = tag
        self.cell = cell
        self.id = (row, col)
        frame = doc.frames.get(self.id)
        if frame is None:
            frame = doc.add_frame(row, col, cell)
        self.frame = frame
        page_obj = doc.pages.get(page)
        if page_obj is None:
            page_obj = doc.add_page(page)
        self.page = page_obj
    def render(self):
        if self.tag is None:
            return
        fn = '.'.join([self.tag.asset_tag.code, 'png'])
        fn = os.path.join(self.doc.tag_dir, fn)
        s = self.tag.get_png_string(full_tag=True)
        with open(fn, 'wb') as f:
            f.write(s)
        w, h = [v for v in unit_to_rl(self.cell.w, self.cell.h)]
        image = ImageFigure(fn, caption='')#, width=w, height=h)
        self.frame.frame.addFromList([image], self.doc.canvas)
