import subprocess

def run_cmd(cmd):
    return subprocess.check_output(cmd, shell=True).decode('utf-8').strip().split('\n')

# 1. Get the 1157 truly missing
with open('final_missing.txt') as f:
    truly_missing = [line.strip().split(' ', 1)[1] for line in f if line.startswith('MISSING:')]

# 2. Get the 54 different ones from pairs.
# I need to rerun the diff logic to get the 54, or just parse the twin_commits_analysis.md
different_commits = []
in_diff_section = False
with open('/home/codespace/.gemini/antigravity-cli/brain/81a1ecb4-595a-4138-a982-e79bf6448238/twin_commits_analysis.md') as f:
    for line in f:
        if line.startswith('## 🔴 Berbeda'):
            in_diff_section = True
            continue
        if in_diff_section and line.startswith('- `'):
            # line looks like: - `410d19d` vs `76ac877` (SUBJECT)
            h1_short = line.split('`')[1]
            different_commits.append(h1_short)

# We need full hashes for the 54. 
# We can find them from missing_16.2_in_ax.txt
full_hashes = {}
with open('missing_16.2_in_ax.txt') as f:
    for line in f:
        if not line.strip(): continue
        h = line.split(' ')[0]
        full_hashes[h[:7]] = line.strip()

missing_list = truly_missing + [full_hashes[h] for h in different_commits if h in full_hashes]

# Now we need to sort them by chronological order (oldest first) so cherry-pick works cleanly
commit_times = {}
for line in missing_list:
    h = line.split(' ')[0]
    t = run_cmd(f"git log -1 --format='%ct' {h}")[0]
    commit_times[line] = int(t)

missing_list.sort(key=lambda x: commit_times[x])

# Output the final list
with open('/home/codespace/.gemini/antigravity-cli/brain/81a1ecb4-595a-4138-a982-e79bf6448238/cherrypick_list.md', 'w') as f:
    f.write("# Daftar Commit untuk di-Cherry-Pick ke ax\n\n")
    f.write(f"Berikut adalah **{len(missing_list)} commit** dari `16.2` yang tidak ada di `ax` (termasuk 54 commit yang namanya mirip tapi kodenya berbeda).\n")
    f.write("Daftar ini telah **diurutkan dari yang paling lama ke yang paling baru** agar Anda terhindar dari konflik jika melakukan cherry-pick.\n\n")
    for item in missing_list:
        f.write(f"- {item}\n")

# Output a bash script for automated cherry-picking if the user wants
with open('/home/codespace/.gemini/antigravity-cli/brain/81a1ecb4-595a-4138-a982-e79bf6448238/do_cherrypick.sh', 'w') as f:
    f.write("#!/bin/bash\n")
    f.write("# Script untuk otomatis cherry-pick 1211 commit yang hilang ke branch ax\n")
    f.write("# Harap jalankan script ini saat Anda berada di branch ax\n\n")
    for item in missing_list:
        h = item.split(' ')[0]
        f.write(f"git cherry-pick {h} || exit 1\n")

