import subprocess
import re

def run_cmd(cmd):
    try:
        return subprocess.check_output(cmd, shell=True, stderr=subprocess.DEVNULL).decode('utf-8', errors='ignore')
    except subprocess.CalledProcessError:
        return ""

commits = []
with open('/home/codespace/.gemini/antigravity-cli/brain/81a1ecb4-595a-4138-a982-e79bf6448238/cherrypick_list.md') as f:
    for line in f:
        if line.startswith('- '):
            commits.append(line.strip()[2:].split(' ')[0])

log_removals = []
optimizations = []

log_keywords = re.compile(r'\b(Log\.|Slog\.|ALOG|Rlog\.|println|Logcat)\b')
opt_keywords_diff = re.compile(r'\b(ArrayMap|SparseArray|LruCache|Pools\.|\.recycle\(\)|== null)\b')

for h in commits:
    diff_out = run_cmd(f"git show -U0 {h}")
    if not diff_out: continue
    
    diff = diff_out.split('\n')
    adds = 0
    dels = 0
    log_dels = 0
    added_lines = []
    deleted_lines = []
    
    for line in diff:
        if line.startswith('+++') or line.startswith('---'): continue
        if line.startswith('+') and not line.startswith('++'):
            adds += 1
            added_lines.append(line[1:])
        elif line.startswith('-') and not line.startswith('--'):
            dels += 1
            deleted_lines.append(line[1:])
            if log_keywords.search(line):
                log_dels += 1
                
    total_changes = adds + dels
    if total_changes == 0:
        continue
        
    is_log_removal = False
    if dels > 0 and log_dels / dels >= 0.5 and adds <= 5:
        is_log_removal = True
    elif adds > 0 and dels > 0:
        for al, dl in zip(added_lines, deleted_lines):
            if 'DEBUG' in dl and 'true' in dl and 'false' in al:
                is_log_removal = True
                break

    if is_log_removal:
        subj = run_cmd(f"git log -1 --format='%s' {h}").strip()
        log_removals.append((h, subj, adds, dels))
        continue
        
    if total_changes <= 50 and total_changes > 0:
        is_opt = False
        for l in added_lines:
            if opt_keywords_diff.search(l):
                is_opt = True
                break
        
        allocs_del = sum(1 for l in deleted_lines if 'new ' in l)
        allocs_add = sum(1 for l in added_lines if 'new ' in l)
        if allocs_del > 0 and allocs_add == 0:
            is_opt = True
            
        if is_opt:
            subj = run_cmd(f"git log -1 --format='%s' {h}").strip()
            optimizations.append((h, subj, adds, dels))

with open('/home/codespace/.gemini/antigravity-cli/brain/81a1ecb4-595a-4138-a982-e79bf6448238/log_opt_commits.md', 'w') as f:
    f.write("# Commit Hapus Log & Optimisasi Kecil\n\n")
    f.write("Sesuai permintaan Anda, saya telah memeriksa **isi diff kode (bukan sekadar judul)** dari keseluruhan daftar commit untuk mendeteksi mana yang murni menghapus log, serta mana yang merupakan optimisasi kecil (mengurangi alokasi memori, menggunakan ArrayMap/cache, dll).\n\n")
    f.write(f"## 🗑️ Menghapus Log / Debugging ({len(log_removals)} commit)\n")
    for r in log_removals:
        f.write(f"- `{r[0][:7]}`: {r[1]} (+{r[2]} -{r[3]})\n")
    f.write(f"\n## ⚡ Optimisasi Kecil (Berdasarkan Diff Kode) ({len(optimizations)} commit)\n")
    for r in optimizations:
        f.write(f"- `{r[0][:7]}`: {r[1]} (+{r[2]} -{r[3]})\n")

