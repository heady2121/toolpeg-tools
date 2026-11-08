# -*- coding: utf-8 -*-
"""Patches YOUR gen_image_tools.py in place (keeps a .bak copy).
Run it from the folder that contains gen_image_tools.py:   python patch_compressor_seo.py
"""
import os, re, shutil, sys

path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "gen_image_tools.py")
if not os.path.exists(path):
    sys.exit("gen_image_tools.py not found next to this script.")

src = open(path, encoding="utf-8").read()
out = src
changes = []

# 1) Title: add "Online"
new_title = 'title="Image Compressor Online &mdash; Shrink Image Size Free | Toolpeg"'
out, n = re.subn(r'title="Image Compressor[^"]*"', new_title, out, count=1)
changes.append(("title", n))

# 2) Description: JPG or PNG -> JPG, PNG or WebP (only inside the compressor's description)
out, n = re.subn(r'(description="Compress )JPG or PNG( images)', r'\1JPG, PNG or WebP\2', out, count=1)
changes.append(("description", n))

for name, n in changes:
    print(("changed " if n else "NOT FOUND ") + name)

if out == src:
    print("\nNothing was changed. Either it's already patched, or your file words these lines differently.")
    print("Make the edits by hand:")
    print('  title="Image Compressor Online &mdash; Shrink Image Size Free | Toolpeg"')
    print('  description="Compress JPG, PNG or WebP images with ... "')
else:
    shutil.copyfile(path, path + ".bak")
    open(path, "w", encoding="utf-8").write(out)
    print("\nSaved. Backup of the original: gen_image_tools.py.bak")
