import os
import sys
import shutil

from_dir = sys.argv[1]
to_dir = sys.argv[2]
max_depth = 0

if "--max_depth" in sys.argv:
    idx = sys.argv.index("--max_depth")
    max_depth = int(sys.argv[idx + 1])

os.makedirs(to_dir, exist_ok=True)

file_counter = {}

for root, _, files in os.walk(from_dir):
    relative_path = os.path.relpath(root, from_dir)
    if relative_path == '.':
        depth = 0
    else:
        depth = relative_path.count(os.sep) + 1
    if max_depth > 0 and depth > max_depth:
        continue

    for file in files:
        base, ext = os.path.splitext(file)
        count = file_counter.get(file, 0)
        while True:
            new_name = f"{base}_{count}{ext}" if count else file
            dst_path = os.path.join(to_dir, new_name)
            if not os.path.exists(dst_path):
                break
            count += 1

        file_counter[file] = count + 1
        src_path = os.path.join(root, file)
        shutil.copy2(src_path, dst_path)
