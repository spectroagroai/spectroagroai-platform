# save as: export_project_code.py
# run with:
# python export_project_code.py

from pathlib import Path

ROOT = Path(".").resolve()
OUTPUT = ROOT / "project_code_dump.txt"

INCLUDE_EXTENSIONS = {
    ".py",
    ".ts",
    ".tsx",
    ".js",
    ".jsx",
    ".json",
    ".yaml",
    ".yml",
    ".md",
    ".txt",
    ".css",
    ".html",
    ".env.example",
}

EXCLUDE_DIRS = {
    ".git",
    ".venv",
    "venv",
    "__pycache__",
    "node_modules",
    "dist",
    "build",
    ".next",
    ".northflank",
    ".vercel",
    ".idea",
    ".vscode",
    "coverage",
    ".pytest_cache",
    "artifacts",
    "data",
    "logs",
}

EXCLUDE_FILES = {
    "project_code_dump.txt",
    ".env",
    ".env.local",
    ".env.production",
    ".env.development",
}


def should_include(path: Path) -> bool:
    if path.name in EXCLUDE_FILES:
        return False

    for part in path.parts:
        if part in EXCLUDE_DIRS:
            return False

    if path.suffix in INCLUDE_EXTENSIONS:
        return True

    # include special files without suffix
    special = {
        "Dockerfile",
        "requirements.txt",
        "production.txt",
        "package.json",
        "package-lock.json",
        "vite.config.ts",
        "tsconfig.json",
    }

    return path.name in special


all_files = []

for path in ROOT.rglob("*"):
    if path.is_file() and should_include(path):
        all_files.append(path)

all_files.sort()

with open(OUTPUT, "w", encoding="utf-8") as out:
    out.write(f"PROJECT ROOT: {ROOT}\n")
    out.write("=" * 100 + "\n\n")

    for file_path in all_files:
        rel = file_path.relative_to(ROOT)

        out.write("=" * 100 + "\n")
        out.write(f"FILE: {rel}\n")
        out.write("=" * 100 + "\n\n")

        try:
            content = file_path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            try:
                content = file_path.read_text(encoding="utf-8-sig")
            except Exception as e:
                content = f"<<FAILED TO READ FILE: {e}>>"

        out.write(content)
        out.write("\n\n")

print(f"[OK] Exported {len(all_files)} files to:")
print(OUTPUT)