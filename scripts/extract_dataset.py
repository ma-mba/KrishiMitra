import os, zipfile, sys
base = r'C:\Users\mekha\.gemini\antigravity\scratch\krishimitr_work'
zip_path = os.path.join(base, 'data', 'archive.zip')
extract_to = os.path.join(base, 'data', 'leaf_disease')
if not os.path.isfile(zip_path):
    print('ZIP file not found at', zip_path)
    sys.exit(1)
if not os.path.isdir(extract_to):
    os.makedirs(extract_to, exist_ok=True)
print('Extracting...')
with zipfile.ZipFile(zip_path, 'r') as z:
    z.extractall(extract_to)
print('Extraction completed. Files extracted:', len(z.namelist()))
