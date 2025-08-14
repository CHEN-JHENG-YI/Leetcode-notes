
import os, re, json
from pathlib import Path
from collections import defaultdict

DOCS = Path(__file__).parent / "docs"
TECH_DIR = DOCS / "techniques"
OUT_PROBLEMS = DOCS / "INDEX-Problems.md"
OUT_TECH = DOCS / "INDEX-Techniques.md"
OUT_TECH_BY_CAT = DOCS / "INDEX-Techniques-By-Category.md"

def parse_front_matter(text: str):
    # Expect YAML-like front matter between first two '---' lines
    if not text.lstrip().startswith("---"):
        return {}
    parts = text.split("\n---", 1)
    if len(parts) < 2:
        return {}
    first_block = text.lstrip()[3:]  # strip starting ---
    if "\n---" not in first_block:
        return {}
    fm, _ = first_block.split("\n---", 1)
    meta = {}
    # Very light YAML-ish parsing to avoid external deps: key: value
    # Lists like ["A","B"]
    for line in fm.splitlines():
        line=line.strip()
        if not line or line.startswith("#"): 
            continue
        if ":" not in line:
            continue
        key, val = line.split(":", 1)
        key = key.strip()
        val = val.strip()
        # remove surrounding quotes
        if val.startswith('"') and val.endswith('"'):
            val = val[1:-1]
        # lists like ["A","B"]
        if val.startswith("[") and val.endswith("]"):
            inner = val[1:-1].strip()
            if not inner:
                meta[key] = []
            else:
                # split by comma not inside quotes (simple approach)
                items = []
                curr = ""
                in_q = False
                for ch in inner:
                    if ch == '"':
                        in_q = not in_q
                        continue
                    if ch == "," and not in_q:
                        items.append(curr.strip())
                        curr = ""
                    else:
                        curr += ch
                if curr.strip():
                    items.append(curr.strip())
                meta[key] = [s for s in (x.strip() for x in items) if s]
        else:
            meta[key] = val
    return meta

def main():
    problems = []
    by_tech = defaultdict(list)
    techniques_pages = {}
    techniques_meta = {}
    for md in sorted(DOCS.glob("*.md")):
        if md.name.startswith("INDEX-") or md.name.startswith("TECHNIQUES"):
            continue
        text = md.read_text(encoding="utf-8", errors="ignore")
        meta = parse_front_matter(text)
        if not meta:
            continue
        pid = str(meta.get("id","")).strip()
        title = meta.get("title","").strip()
        topics = meta.get("topics", [])
        techniques = meta.get("techniques", [])
        difficulty = meta.get("difficulty","").strip()
        slug = meta.get("slug","").strip()
        rel = md.name

        problems.append({
            "id": pid, "title": title, "topics": topics, "techniques": techniques,
            "difficulty": difficulty, "file": rel, "slug": slug
        })
        for t in techniques:
            by_tech[t].append((pid, title, rel))


    # Scan technique pages
    # Consolidated technique pages (Linked List single page with sections)
    consolidated_map = {}
    consolidated_file = DOCS / "TECHNIQUES-Linked-List.md"
    if consolidated_file.exists():
        text = consolidated_file.read_text(encoding="utf-8", errors="ignore")
        # find headings like '## Name'
        for line in text.splitlines():
            if line.startswith("## "):
                name = line[3:].strip()
                slug = name.lower()
                import re as _re
                slug = _re.sub(r"[^a-z0-9\s\-]+", "", slug)
                slug = _re.sub(r"\s+", "-", slug).strip("-")
                consolidated_map[name] = f"TECHNIQUES-Linked-List.md#"+slug

    if TECH_DIR.exists():
        for md in TECH_DIR.rglob("*.md"):
            text = md.read_text(encoding="utf-8", errors="ignore")
            meta = parse_front_matter(text)
            if not meta:
                continue
            tname = meta.get("name","").strip()
            tcat = meta.get("category","").strip()
            if not tname:
                continue
            rel = md.relative_to(DOCS).as_posix()
            techniques_pages[tname] = rel
            techniques_meta[tname] = {"category": tcat, "file": rel}

    # Build Problems index
    problems.sort(key=lambda x: (x["topics"], x["id"]))
    lines = []
    lines.append("# INDEX — Problems")
    lines.append("")
    lines.append("| ID | Title | Topics | Techniques | Difficulty | Note |")
    lines.append("|---:|-------|--------|------------|------------|------|")
    for p in problems:
        topics_str = ", ".join(p["topics"]) if p["topics"] else ""
        tech_str = ", ".join(p["techniques"]) if p["techniques"] else ""
        link = f"[{p['title']}]({p['file']})" if p["file"] else p["title"]
        lines.append(f"| {p['id']} | {link} | {topics_str} | {tech_str} | {p['difficulty']} | |")
    OUT_PROBLEMS.write_text("\n".join(lines), encoding="utf-8")

    # Build Techniques index
    lines = []
    lines.append("# INDEX — Techniques")
    lines.append("")
    for tech in sorted(by_tech.keys(), key=lambda s: s.lower()):
        lines.append(f"## {tech}")
        for pid, title, rel in sorted(by_tech[tech], key=lambda x: int(x[0]) if x[0].isdigit() else x[0]):
            lines.append(f"- [{pid}] [{title}]({rel})")
        lines.append("")

    # Build Techniques index
    lines = []
    lines.append("# INDEX — Techniques")
    lines.append("")
    for tech in sorted(set(list(by_tech.keys()) + list(techniques_pages.keys())), key=lambda s: s.lower()):
        page = consolidated_map.get(tech, "") or techniques_pages.get(tech, "")
        cat = techniques_meta.get(tech, {}).get("category", "")
        header = f"## {tech}"
        if cat:
            header += f"  _(Category: {cat})_"
        lines.append(header)
        if page:
            lines.append(f"[Technique Page]({page})")
        # problems that tagged this tech
        tagged = by_tech.get(tech, [])
        if tagged:
            lines.append("**Problems using this technique:**")
            for pid, title, rel in sorted(tagged, key=lambda x: int(x[0]) if x[0].isdigit() else x[0]):
                lines.append(f"- [{pid}] [{title}]({rel})")
        else:
            lines.append("_No problems tagged yet._")
        lines.append("")
    OUT_TECH.write_text("\n".join(lines), encoding="utf-8")

    # Build Techniques by Category
    by_cat = defaultdict(list)
    for tech, meta in techniques_meta.items():
        by_cat[meta.get("category","")].append(tech)
    lines = []
    lines.append("# INDEX — Techniques by Category")
    lines.append("")
    for cat in sorted(by_cat.keys(), key=lambda s: s.lower() if isinstance(s,str) else str(s)):
        lines.append(f"## {cat}")
        for tech in sorted(by_cat[cat], key=lambda s: s.lower()):
            page = consolidated_map.get(tech, "") or techniques_pages.get(tech, "")
            if page:
                lines.append(f"- [{tech}]({page})")
            else:
                lines.append(f"- {tech}")
        lines.append("")
    OUT_TECH_BY_CAT.write_text("\n".join(lines), encoding="utf-8")
    print(f"Generated: {OUT_PROBLEMS}, {OUT_TECH} and {OUT_TECH_BY_CAT}")

if __name__ == "__main__":
    main()
