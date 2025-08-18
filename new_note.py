import sys, re
from pathlib import Path

TEMPLATE_PATH = Path(__file__).parent / "templates" / "leetcode_note_template.md"
DOCS_DIR = Path(__file__).parent / "docs"

def slugify(title: str) -> str:
    s = title.strip().lower()
    s = re.sub(r"[^\w\s-]", "", s)        # remove punctuation
    s = re.sub(r"\s+", "-", s)            # spaces -> hyphens
    s = re.sub(r"-+", "-", s).strip("-")  # collapse hyphens
    return s

def main():
    if len(sys.argv) < 5:
        print("Usage: python new_note.py <ID> \"<TITLE>\" \"<TOPIC>\" <DIFFICULTY>")
        print("Example: python new_note.py 2074 \"Reverse Nodes in Even Length Groups\" \"Linked List\" Medium")
        sys.exit(1)

    qid = str(sys.argv[1]).strip()
    title = sys.argv[2].strip()
    topic = sys.argv[3].strip()
    difficulty = sys.argv[4].strip()

    slug = slugify(title)

    filename_title = title.replace(" ", "-")
    filename_title = re.sub(r"[^\w-]", "", filename_title)
    fname = f"{qid}-{filename_title}.md"

    with open(TEMPLATE_PATH, "r", encoding="utf-8") as f:
        tpl = f.read()

    content = (tpl
        .replace("{{ID}}", qid)
        .replace("{{TITLE}}", title)
        .replace("{{TOPIC}}", topic)
        .replace("{{SLUG}}", slug)
        .replace("{{DIFFICULTY}}", difficulty)
    )

    DOCS_DIR.mkdir(parents=True, exist_ok=True)
    out_path = DOCS_DIR / fname
    if out_path.exists():
        print(f"[Warning] File already exists: {out_path}")
    else:
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(content)

    print(f"Generated: {out_path}")

if __name__ == "__main__":
    main()
