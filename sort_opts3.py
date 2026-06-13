import subprocess
import re

def run_cmd(cmd):
    try:
        return subprocess.check_output(cmd, shell=True, stderr=subprocess.DEVNULL).decode('utf-8', errors='ignore').strip().split('\n')
    except:
        return []

commits = []
with open('/home/codespace/.gemini/antigravity-cli/brain/81a1ecb4-595a-4138-a982-e79bf6448238/cherrypick_list.md') as f:
    for line in f:
        if line.startswith('- '):
            commits.append(line.strip()[2:].split(' ')[0])

opt_keywords = re.compile(r'hwui|libui|skia|render|opengl|vulkan|optimiz|perf|cache|leak|speed|fast|reduce|alloc|inline', re.IGNORECASE)

results = {}

for h in commits:
    info = subprocess.check_output(f"git log -1 --format='%s|%an' {h}", shell=True).decode('utf-8').strip()
    if not info: continue
    parts = info.split('|', 1)
    if len(parts) != 2: continue
    subj, author = parts
    
    files = "\n".join(run_cmd(f"git show --name-only --format= {h}"))
    
    if opt_keywords.search(subj) or opt_keywords.search(files):
        results[h] = f"- `{h[:7]}`: **{subj}** (Author: *{author}*)"

topo_commits = run_cmd("git rev-list --topo-order --reverse 16.2")

sorted_opts = []
for th in topo_commits:
    for h in results:
        if th.startswith(h):
            sorted_opts.append((th, results[h]))
            break

with open('/home/codespace/.gemini/antigravity-cli/brain/81a1ecb4-595a-4138-a982-e79bf6448238/optimization_commits.md', 'w') as f:
    f.write("# Daftar Lengkap Commit Optimisasi (Diurutkan secara Topological)\n\n")
    f.write("Berikut adalah daftar 76 commit optimisasi (termasuk manajemen RAM, pencegahan leak, performa HWUI, dan efisiensi IPC).\n")
    f.write("**PENTING:** Daftar ini telah diurutkan berdasarkan **Strict Topological Order** (urutan parent-child sejati di Git). Lakukan cherry-pick secara berurutan dari atas ke bawah untuk menghindari merge conflict!\n\n")
    for full_h, line_content in sorted_opts:
        f.write(f"{line_content}\n")

with open('/home/codespace/.gemini/antigravity-cli/brain/81a1ecb4-595a-4138-a982-e79bf6448238/cherrypick_optimizations.sh', 'w') as f:
    f.write("#!/bin/bash\n")
    f.write("# Script untuk otomatis cherry-pick 76 commit optimisasi ke branch ax\n")
    f.write("# Diurutkan secara strict topo-order untuk mencegah konflik.\n\n")
    for full_h, line_content in sorted_opts:
        f.write(f"git cherry-pick {full_h} || exit 1\n")

print(f"Sorted {len(sorted_opts)} commits.")
