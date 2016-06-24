import os
import io
import shlex
import subprocess
import tempfile
import shutil

from bs4 import BeautifulSoup

from PyPDF2 import PdfFileMerger

def do_export(infile, outfile, dpi):
    args = '-z --export-pdf={outfile} --export-dpi={dpi} --export-area-page {infile}'
    args = args.format(infile=infile, outfile=outfile, dpi=dpi)
    args = ' '.join(['inkscape', args])
    s = subprocess.check_output(shlex.split(args))
    print(s)

def merge_pdfs(pdfs):
    merger = PdfFileMerger()
    for pdf in pdfs:
        merger.append(pdf)
    fh = io.BytesIO()
    merger.write(fh)
    merger.close()
    s = fh.getvalue()
    fh.close()
    return s

def render_from_html(s, context_data):
    doc = BeautifulSoup(s, 'html5lib')
    svgs = doc.find_all('svg')
    pdfs = []
    tmp_dir = tempfile.mkdtemp()
    dpi = context_data['dpi']
    for i, svg in enumerate(svgs):
        base_fn = os.path.join(tmp_dir, '%02d' % (i))
        svg_fn = '.'.join([base_fn, 'svg'])
        pdf_fn = '.'.join([base_fn, 'pdf'])
        pdfs.append(pdf_fn)
        with open(svg_fn, 'w') as f:
            f.write(str(svg))
        do_export(svg_fn, pdf_fn, dpi)
    s = merge_pdfs(pdfs)
    #shutil.rmtree(tmp_dir)
    return s
