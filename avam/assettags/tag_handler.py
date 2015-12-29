import random
from StringIO import StringIO

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
    @property
    def qr_svg_bytes(self):
        b = getattr(self, '_qr_svg_bytes', None)
        if b is None:
            b = self._qr_svg_bytes = self.get_qr_svg_bytes()
        return b
    def get_qr_svg_bytes(self):
        fh = StringIO()
        self.qr_img.save(fh)
        s = fh.getvalue()
        fh.close()
        return s
