import os, zipfile, shutil, sys

base = r'C:\Users\mekha\.gemini\antigravity\scratch\krishimitr_work'
zip_path = os.path.join(base, 'data', 'archive.zip')
extract_to = os.path.join(base, 'data', 'leaf_disease')

if not os.path.isfile(zip_path):
    print('ZIP not found at', zip_path)
    sys.exit(1)

# Clean target directory
if os.path.isdir(extract_to):
    shutil.rmtree(extract_to, ignore_errors=True)
os.makedirs(extract_to, exist_ok=True)

print('Starting extraction...')
with zipfile.ZipFile(zip_path, 'r') as z:
    for member in z.infolist():
        # Build absolute target path
        target_path = os.path.abspath(os.path.join(extract_to, member.filename))
        # Ensure parent directory exists (normal path)
        parent_dir = os.path.dirname(target_path)
        os.makedirs(parent_dir, exist_ok=True)
        if member.is_dir():
            continue
        # Use Windows extended-length prefix for the file write only
        # The prefix must be "\\?\" followed by the absolute path (no extra backslashes)
        target_path_ext = r'\\?\' + target_path
        with z.open(member) as src, open(target_path_ext, 'wb') as dst:
            shutil.copyfileobj(src, dst)
print('Extraction completed. Files extracted:', len(z.namelist()))
