import os, zipfile, shutil, sys

base = r'C:\Users\mekha\.gemini\antigravity\scratch\krishimitr_work'
zip_path = os.path.join(base, 'data', 'archive.zip')
extract_to = os.path.join(base, 'data', 'leaf_disease')

if not os.path.isfile(zip_path):
    print('ZIP not found at', zip_path)
    sys.exit(1)

# Clean target folder
if os.path.isdir(extract_to):
    for root, dirs, files in os.walk(extract_to, topdown=False):
        for name in files:
            try:
                os.remove(os.path.join(root, name))
            except Exception:
                pass
        for name in dirs:
            try:
                os.rmdir(os.path.join(root, name))
            except Exception:
                pass
else:
    os.makedirs(extract_to, exist_ok=True)

print('Starting extraction...')
with zipfile.ZipFile(zip_path, 'r') as z:
    for member in z.infolist():
        target_path = os.path.abspath(os.path.join(extract_to, member.filename))
        # Use Windows extended-length prefix to bypass MAX_PATH
        target_path_ext = '\\?\\' + target_path
        if member.is_dir():
            os.makedirs(target_path_ext, exist_ok=True)
            continue
        parent_dir = os.path.dirname(target_path_ext)
        os.makedirs(parent_dir, exist_ok=True)
        with z.open(member) as src, open(target_path_ext, 'wb') as dst:
            shutil.copyfileobj(src, dst)
print('Extraction completed. Files extracted:', len(z.namelist()))
