
# User Manual — LeetCode Notes System (VS Code + GitHub + Technique Index)

This manual shows how to create **problem notes**, **technique tags**, and **auto-generated indexes**, then sync to GitHub.

---

## 0. Prerequisites (one-time)
- **VS Code** installed
- **Git** installed (`git --version` works)
- **Python 3** installed (`python --version` or `python3 --version`)
- **GitHub** account (optional but recommended)

> When you open this project in VS Code, accept the recommended extensions (Markdown / GitLens / C++ etc.).

---

## 1. Project Layout
```
leetcode-notes-starter/
├─ docs/
│  ├─ TECHNIQUES-Linked-List.md          # Single-page linked-list techniques
│  ├─ INDEX-Problems.md                  # Problem matrix (generated)
│  ├─ INDEX-Techniques.md                # Technique → problems (generated)
│  └─ INDEX-Techniques-By-Category.md    # Technique categories (generated)
├─ templates/
│  └─ leetcode_note_template.md          # Note template (with YAML front matter)
├─ new_note.py                           # Create a new note
├─ generate_index.py                     # Build the indexes
└─ .vscode/extensions.json               # Recommended VS Code extensions
```

---

## 2. Create Your First Note
Open VS Code terminal in the project root and run:
```bash
python new_note.py 2074 "Reverse Nodes in Even Length Groups" "Linked List" "Medium" "C++"
# or
python3 new_note.py 2074 "Reverse Nodes in Even Length Groups" "Linked List" "Medium" "C++"
```
This generates:
```
docs/2074-Reverse-Nodes-in-Even-Length-Groups.md
```

### 2.1 Edit the Note (YAML matters)
Top of each note:
```yaml
---
id: 2074
title: "Reverse Nodes in Even Length Groups"
topics: ["Linked List"]
techniques: ["Dummy Head", "Group Reversal"]  # Must match section titles in the techniques page
difficulty: "Medium"
language: "C++"
slug: "reverse-nodes-in-even-length-groups"
---
```
- `topics`: high-level categories, can be many (e.g., `["Linked List","Two Pointers"]`)
- `techniques`: finer-grained tools used; **names must exactly match** the section titles in `TECHNIQUES-Linked-List.md`

---

## 3. Build Indexes
Whenever you add/edit notes or techniques:
```bash
python generate_index.py
# or
python3 generate_index.py
```
It updates:
- `INDEX-Problems.md` — matrix view (ID / Title / Topics / Techniques / Difficulty)
- `INDEX-Techniques.md` — for each technique, list all problems and link to the section
- `INDEX-Techniques-By-Category.md` — techniques grouped by category

---

## 4. Technique Pages (Linked List — single page)
Edit `docs/TECHNIQUES-Linked-List.md`. Each technique is a `##` section:
```markdown
## Dummy Head
(when to use / steps / pitfalls / snippet)
```
**Rule**: the names you put in a problem note’s `techniques: [...]` must match these section titles exactly.

---

## 5. Push to GitHub (pick one)

### 5.1 Command line
```bash
git init
git add .
git commit -m "Initial commit: notes & techniques"
git branch -M main
git remote add origin https://github.com/<your-account>/leetcode-notes.git
git push -u origin main
```
Subsequent updates:
```bash
git add .
git commit -m "add: 2074 notes + update indexes"
git push
```

### 5.2 GitHub Desktop / VS Code Source Control
- **GitHub Desktop**: Add local repo → Commit → Publish / Push  
- **VS Code**: Source Control panel → Stage → Commit → Push

---

## 6. Daily Workflow Checklist
1. `python new_note.py <ID> "<Title>" "<Topic>" <Difficulty> <Language>`  
2. Fill in **summary / approach / code / complexity**; set `topics` and `techniques`.  
3. `python generate_index.py` to update indexes.  
4. `git add . && git commit -m "..." && git push` to sync to GitHub.  

Optional: create a Notion database index (columns: ID, Title, Difficulty, Topic, Status, Link to GitHub file).

---

## 7. Naming & Conventions
- File name: `<ID>-<Hyphen-Title>.md` (auto-generated)  
- Keep technique section titles stable; if you rename a technique, update all notes’ `techniques` tags accordingly.

---

## 8. FAQ
**Python not found?** Try `python3` (macOS/Linux) or `py` (Windows).  
**`remote origin already exists`?**  
```bash
git remote set-url origin https://github.com/<your-account>/leetcode-notes.git
```
**Indexes missing a technique you added?** Ensure the note’s `techniques` names exactly match the `##` titles in the techniques page; then rerun the generator.

---

Happy grinding!
