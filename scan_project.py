import os

ROOT = "."        # المجلد الحالي
IGNORE_DIRS = {
    "venv",
    "__pycache__",
    ".git",
    "node_modules",
    "dist",
    ".vite",
    ".pytest_cache",
    ".idea",
    ".vscode",
    "coverage",
}


def scan(folder, level=0):
    try:
        items = sorted(os.listdir(folder))
    except PermissionError:
        return

    for item in items:
        path = os.path.join(folder, item)

        if os.path.isdir(path):
            if item in IGNORE_DIRS:
                continue

            print("  " * level + f"[DIR] {item}")
            scan(path, level + 1)

        else:
            print("  " * level + f"- {item}")


if __name__ == "__main__":
    print("\nPROJECT STRUCTURE:\n")
    scan(ROOT)