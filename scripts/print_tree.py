import os

# Các thư mục hoặc file không cần hiển thị
EXCLUDED = {
    "__pycache__", ".git", ".venv", ".idea", "node_modules", "env", "venv",
    ".DS_Store", ".mypy_cache", ".pytest_cache", "scripts"
}

# Các phần mở rộng file không cần hiển thị
EXCLUDED_SUFFIX = {
    ".pyc", ".log", ".tmp", ".swp", ".zip", ".tar", ".tar.gz", ".sqlite3"
}

def print_tree(startpath, prefix="", output_lines=None):
    if output_lines is None:
        output_lines = []

    entries = sorted(os.listdir(startpath))
    entries = [e for e in entries if e not in EXCLUDED and not any(e.endswith(suf) for suf in EXCLUDED_SUFFIX)]

    for idx, entry in enumerate(entries):
        path = os.path.join(startpath, entry)
        connector = "└── " if idx == len(entries) - 1 else "├── "
        line = prefix + connector + entry
        output_lines.append(line)

        if os.path.isdir(path):
            extension = "    " if idx == len(entries) - 1 else "│   "
            print_tree(path, prefix + extension, output_lines)

    return output_lines

if __name__ == '__main__':
    import sys

    # Nếu có đối số truyền vào thì dùng, không thì lấy thư mục hiện tại
    if len(sys.argv) == 2:
        start_path = sys.argv[1]
    else:
        # Mặc định lấy thư mục đang chạy script (thường là thư mục gốc workspace trong VSCode)
        start_path = os.getcwd()

    tree_lines = [start_path]
    tree_lines += print_tree(start_path)

    output_file = os.path.join(start_path, "tree.md")
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("\n".join(tree_lines))

    print(f"Cây thư mục đã được ghi vào {output_file}")
