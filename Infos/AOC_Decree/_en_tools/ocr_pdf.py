#!/usr/bin/env python3
"""OCR a decree PDF with macOS Vision. Usage: ocr_pdf.py <slug> [a-b]  -> prints text"""
import sys, os, subprocess, tempfile, fitz
HERE = os.path.dirname(os.path.abspath(__file__))
slug = sys.argv[1]
d = fitz.open(os.path.join(os.path.dirname(HERE), "decrees", slug + ".pdf"))
rng = range(d.page_count)
if len(sys.argv) > 2: a, b = map(int, sys.argv[2].split("-")); rng = range(a - 1, b)
tmp = tempfile.mkdtemp(); imgs = []
for i in rng:
    f = os.path.join(tmp, "p%03d.png" % (i + 1)); d[i].get_pixmap(dpi=220).save(f); imgs.append(f)
print(subprocess.run([os.path.join(HERE, "ocr")] + imgs, capture_output=True, text=True).stdout)
