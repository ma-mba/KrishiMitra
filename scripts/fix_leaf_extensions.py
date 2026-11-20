import os, sys

base = r'C:\Users\mekha\.gemini\antigravity\scratch\krishimitr_work'
leaf_dir = os.path.join(base, 'data', 'leaf_disease')
# Known image extensions
valid_exts = {'.jpg', '.jpeg', '.png', '.bmp', '.tif', '.tiff', '.webp', '.ppm', '.pgm'}

renamed = 0
for root, dirs, files in os.walk(leaf_dir):
    for f in files:
        name, ext = os.path.splitext(f)
        if ext.lower() not in valid_exts:
            # If there is no extension or unknown, add .jpg
            new_name = f + '.jpg' if not ext else name + '.jpg'
            src = os.path.join(root, f)
            dst = os.path.join(root, new_name)
            try:
                os.rename(src, dst)
                renamed += 1
            except Exception as e:
                print(f'Failed to rename {src}: {e}', file=sys.stderr)
print(f'Renamed {renamed} files')
