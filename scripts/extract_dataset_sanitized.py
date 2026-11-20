import os, zipfile, sys, shutil

base = r'C:\Users\mekha\.gemini\antigravity\scratch\krishimitr_work'
zip_path = os.path.join(base, 'data', 'archive.zip')
extract_to = os.path.join(base, 'data', 'leaf_disease')

if not os.path.isfile(zip_path):
    print('ZIP not found at', zip_path)
    sys.exit(1)

# Remove any previous extraction
if os.path.isdir(extract_to):
    shutil.rmtree(extract_to, ignore_errors=True)
os.makedirs(extract_to, exist_ok=True)

print('Starting sanitized extraction...')

def sanitize(name, max_len=100):
    # Replace spaces and problematic chars with underscore, truncate
    safe = ''.join(c if c.isalnum() or c in ('_', '-') else '_' for c in name)
    return safe[:max_len]

with zipfile.ZipFile(zip_path, 'r') as z:
    for member in z.infolist():
        # Skip directory entries
        if member.is_dir():
            continue
        # member.filename uses '/' as separator inside zip
        parts = member.filename.split('/')
        # Remove leading empty parts or top‑level repo folder (usually first part = repo name)
        if len(parts) > 0 and parts[0].lower().startswith('plantvillage'):
            parts = parts[1:]
        # Expected structure: ['plantvillage dataset', 'color', '<class>', '<image>.JPG']
        # We'll keep the class folder hierarchy but sanitize names
        sanitized_parts = [sanitize(p) for p in parts]
        target_path = os.path.abspath(os.path.join(extract_to, *sanitized_parts))
        parent_dir = os.path.dirname(target_path)
        os.makedirs(parent_dir, exist_ok=True)
        with z.open(member) as src, open(target_path, 'wb') as dst:
            shutil.copyfileobj(src, dst)
print('Sanitized extraction completed. Files extracted:', len(z.namelist()))
