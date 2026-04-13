import os
import re
import json

base_path = "C:/Users/Administrator.DESKTOP-EGNE9ND/.claude/skills/"
results = []

for root, dirs, files in os.walk(base_path):
    if "SKILL.md" in files:
        file_path = os.path.join(root, "SKILL.md")
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                # 提取 frontmatter
                match = re.search(r'^---\n(.*?)\n---', content, re.DOTALL)
                description = ""
                name = os.path.basename(root)
                if match:
                    frontmatter = match.group(1)
                    desc_match = re.search(r'^description:\s*(.*)', frontmatter, re.MULTILINE)
                    if desc_match:
                        description = desc_match.group(1).strip()
                    name_match = re.search(r'^name:\s*(.*)', frontmatter, re.MULTILINE)
                    if name_match:
                        name = name_match.group(1).strip()

                results.append({
                    "name": name,
                    "path": file_path,
                    "description": description
                })
        except Exception as e:
            pass

with open('C:/Users/Administrator.DESKTOP-EGNE9ND/.claude/skills/skill-stocktake/inventory.json', 'w', encoding='utf-8') as outfile:
    json.dump(results, outfile, indent=2, ensure_ascii=False)
