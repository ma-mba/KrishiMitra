import os, zipfile, shutil, sys
base = r'C:\Users\mekha\.gemini\antigravity\scratch\krishimitr_work'
zip_path = os.path.join(base, 'data', 'archive.zip')
extract_to = os.path.join(base, 'data', 'leaf_disease')
if not os.path.isfile(zip_path):
    print('ZIP not found', zip_path)
    sys.exit(1)
if os.path.isdir(extract_to):
    shutil.rmtree(extract_to)
os.makedirs(extract_to, exist_ok=True)
with zipfile.ZipFile(zip_path, 'r') as z:
    z.extractall(extract_to)
print('extracted')
