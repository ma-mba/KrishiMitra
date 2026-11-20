import os, zipfile, shutil, sys

base = r'C:\Users\mekha\.gemini\antigravity\scratch\krishimitr_work'
zip_path = os.path.join(base, 'data', 'archive.zip')
extract_to = os.path.join(base, 'data', 'leaf_disease')

if not os.path.isfile(zip_path):
    print('ZIP not found at', zip_path)
    sys.exit(1)

# Clean target folder (remove existing files)
if os.path.isdir(extract_to):
    shutil.rmtree(extract_to, ignore_errors=True)
os.makedirs(extract_to, exist_ok=True)

print('Starting extraction...')
with zipfile.ZipFile(zip_path, 'r') as z:
    for member in z.infolist():
        # Normal target path without extended prefix
        target_path = os.path.abspath(os.path.join(extract_to, member.filename))
        # Ensure its parent directory exists
        parent_dir = os.path.dirname(target_path)
        os.makedirs(parent_dir, exist_ok=True)
        if member.is_dir():
            continue
        # Use extended-length prefix only for the actual file write to avoid MAX_PATH limits
        target_path_ext = '\\?\\' + target_path
        with z.open(member) as src, open(target_path_ext, 'wb') as dst:
            shutil.copyfileobj(src, dst)
print('Extraction completed. Files extracted:', len(z.namelist()))
