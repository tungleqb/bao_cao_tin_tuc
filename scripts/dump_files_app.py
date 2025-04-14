import os

def dump_all_files(root_dir_list: str, output_file: str):
    SKIP_EXT = {'.pyc', '.pyo', '.exe', '.dll', '.so', '.class'}
    with open(output_file, 'w', encoding='utf-8') as out:
        for root_dir in root_dir_list:
            for dirpath, _, filenames in os.walk(root_dir):
                for filename in filenames:
                    ext = os.path.splitext(filename)[1]
                    if ext in SKIP_EXT:
                        continue
                    full_path = os.path.join(dirpath, filename)
                    rel_path = os.path.relpath(full_path, root_dir)
                    try:
                        with open(full_path, 'r', encoding='utf-8') as f:
                            content = f.read()
                    except Exception:
                        # Skip unreadable (binary or corrupted) files silently
                        continue
                    out.write(f"\n===== FILE: {root_dir}/{rel_path} =====\n")
                    out.write(content)
                    out.write("\n")

if __name__ == "__main__":
    dump_all_files(["app", "tests"], "project_dump.txt")
