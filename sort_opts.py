import subprocess

def run_cmd(cmd):
    return subprocess.check_output(cmd, shell=True).decode('utf-8').strip().split('\n')

opt_data = {}
with open('/home/codespace/.gemini/antigravity-cli/brain/81a1ecb4-595a-4138-a982-e79bf6448238/optimization_commits.md', 'r') as f:
    for line in f:
        if line.startswith('- `'):
            parts = line.split('`')
            short_h = parts[1]
            rest = parts[2].strip()
            full_h = subprocess.check_output(f"git rev-parse {short_h}^{{commit}}", shell=True).decode('utf-8').strip()
            opt_data[full_h] = line.strip()

topo_commits = run_cmd("git rev-list --topo-order --reverse 16.2")

sorted_opts = []
for th in topo_commits:
    if th in opt_data:
        sorted_opts.append((th, opt_data[th]))

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
        f.write(f"git cherry-pick {full_h[:10]} || exit 1\n")

print(f"Sorted {len(sorted_opts)} commits out of {len(opt_data)}")
