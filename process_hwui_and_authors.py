import subprocess
import re

def run_cmd(cmd):
    try:
        return subprocess.check_output(cmd, shell=True, stderr=subprocess.DEVNULL).decode('utf-8', errors='ignore').strip()
    except:
        return ""

commits = []
with open('/home/codespace/.gemini/antigravity-cli/brain/81a1ecb4-595a-4138-a982-e79bf6448238/cherrypick_list.md') as f:
    for line in f:
        if line.startswith('- '):
            commits.append(line.strip()[2:].split(' ')[0])

opt_keywords = re.compile(r'hwui|libui|skia|render|opengl|vulkan|optimiz|perf|cache|leak|speed|fast|reduce|alloc|inline', re.IGNORECASE)
hwui_keywords = re.compile(r'hwui|libui|skia|render|opengl|vulkan', re.IGNORECASE)

results = []
hwui_commits = []

for h in commits:
    info = run_cmd(f"git log -1 --format='%s|%an' {h}")
    if not info: continue
    
    parts = info.split('|', 1)
    if len(parts) != 2: continue
    subj, author = parts
    
    files = run_cmd(f"git show --name-only --format= {h}")
    
    match_opt = opt_keywords.search(subj) or opt_keywords.search(files)
    match_hwui = hwui_keywords.search(subj) or hwui_keywords.search(files)
    
    if match_opt:
        results.append((h, subj, author))
    if match_hwui:
        hwui_commits.append(h)

# Write hwui commits to a file so we can cherry pick them
with open('hwui_to_pick.txt', 'w') as f:
    for hc in hwui_commits:
        f.write(hc + '\n')

# Write the final artifact with authors
with open('/home/codespace/.gemini/antigravity-cli/brain/81a1ecb4-595a-4138-a982-e79bf6448238/optimization_commits.md', 'w') as f:
    f.write("# Daftar Lengkap Commit Optimisasi (Berdasarkan Broad Scan)\n\n")
    f.write("Berikut adalah hasil pemindaian luas untuk commit yang menyentuh hwui, manajemen RAM, dan performa secara umum.\n\n")
    for r in results:
        f.write(f"- `{r[0][:7]}`: **{r[1]}** (Author: *{r[2]}*)\n")

