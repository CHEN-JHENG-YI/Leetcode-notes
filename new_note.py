import sys, os, re, datetime
from pathlib import Path

TEMPLATE_PATH = Path(__file__).parent / "templates" / "leetcode_note_template.md"
DOCS_DIR = Path(__file__).parent / "docs"

def slugify(title: str) -> str:
    s = title.strip().lower()
    s = re.sub(r"[^\w\s-]", "", s)        # remove punctuation
    s = re.sub(r"\s+", "-", s)            # spaces -> hyphens
    s = re.sub(r"-+", "-", s).strip("-")  # collapse hyphens
    return s

def lang_code_from_label(label: str) -> str:
    m = label.strip().lower()
    if "c++" in m or "cpp" in m:
        return "cpp"
    if "python" in m or "py" in m:
        return "python"
    if "java" in m:
        return "java"
    if "js" in m or "javascript" in m:
        return "javascript"
    if "go" in m:
        return "go"
    return ""  # default: no language hint

def main():
    if len(sys.argv) < 6:
        print("用法: python new_note.py <ID> \"<TITLE>\" \"<TOPIC>\" <DIFFICULTY> <LANGUAGE>")
        print("例子: python new_note.py 2074 \"Reverse Nodes in Even Length Groups\" \"Linked List\" Medium C++")
        sys.exit(1)

    qid = str(sys.argv[1]).strip()
    title = sys.argv[2].strip()
    topic = sys.argv[3].strip()
    difficulty = sys.argv[4].strip()
    language = sys.argv[5].strip()

    slug = slugify(title)
    filename_title = title.replace(" ", "-")
    filename_title = re.sub(r"[^\w-]", "", filename_title)
    fname = f"{qid}-{filename_title}.md"

    with open(TEMPLATE_PATH, "r", encoding="utf-8") as f:
        tpl = f.read()

    lang_code = lang_code_from_label(language)
    content = (tpl
        .replace("{{ID}}", qid)
        .replace("{{TITLE}}", title)
        .replace("{{TOPIC}}", topic)
        .replace("{{DIFFICULTY}}", difficulty)
        .replace("{{LANGUAGE}}", language)
        .replace("{{SLUG}}", slug)
        .replace("{{LANG_CODE}}", lang_code)
    )

    DOCS_DIR.mkdir(parents=True, exist_ok=True)
    out_path = DOCS_DIR / fname
    if out_path.exists():
        print(f"[警告] 檔案已存在: {out_path}")
    else:
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(content)

    print(f"已產生: {out_path}")

if __name__ == "__main__":
    main()