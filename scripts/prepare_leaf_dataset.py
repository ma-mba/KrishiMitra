import os, shutil

base = r'C:\Users\mekha\.gemini\antigravity\scratch\krishimitr_work'
leaf_dir = os.path.join(base, 'data', 'leaf_disease')
color_dir = os.path.join(leaf_dir, 'color')

if not os.path.isdir(color_dir):
    print('Color directory not found:', color_dir)
    exit(1)

# Move each class folder from color_dir up to leaf_dir
for entry in os.listdir(color_dir):
    src = os.path.join(color_dir, entry)
    dst = os.path.join(leaf_dir, entry)
    if os.path.isdir(src):
        if os.path.exists(dst):
            # If destination exists, merge contents
            for item in os.listdir(src):
                s = os.path.join(src, item)
                d = os.path.join(dst, item)
                shutil.move(s, d)
            shutil.rmtree(src)
        else:
            shutil.move(src, dst)

# Optionally clean up now-empty subfolders (grayscale, segmented)
for sub in ['grayscale', 'segmented']:
    sub_path = os.path.join(leaf_dir, sub)
    if os.path.isdir(sub_path):
        shutil.rmtree(sub_path, ignore_errors=True)

print('Preparation completed. Classes now at:', leaf_dir)
