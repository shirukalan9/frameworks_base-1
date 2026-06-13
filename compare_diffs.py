import subprocess

def run_cmd(cmd):
    return subprocess.check_output(cmd, shell=True).decode('utf-8').strip().split('\n')

ax_commits = run_cmd("git log --format='%H|%an|%ad|%s' --date=unix ax")
missing_commits = run_cmd("cat missing_16.2_in_ax.txt")

author_map = {}
subject_map = {}

for line in ax_commits:
    if not line: continue
    parts = line.split('|', 3)
    if len(parts) == 4:
        author_map[f"{parts[1]}|{parts[2]}"] = parts[0]
        subject_map[parts[3]] = parts[0]

pairs = []
for line in missing_commits:
    if not line: continue
    h1 = line.split(' ')[0]
    info = run_cmd(f"git log -1 --format='%an|%ad|%s' --date=unix {h1}")[0].split('|', 2)
    if len(info) == 3:
        an, ad, s = info
        if s in subject_map:
            pairs.append(('SUBJECT', h1, subject_map[s], s, s))
        elif f"{an}|{ad}" in author_map:
            h2 = author_map[f"{an}|{ad}"]
            s2 = run_cmd(f"git log -1 --format='%s' {h2}")[0]
            pairs.append(('AUTHOR', h1, h2, s, s2))

def get_clean_diff(h):
    diff = run_cmd(f"git show -U0 -w --format= {h}")
    res = []
    for l in diff:
        if l.startswith('index ') or l.startswith('diff --git') or l.startswith('+++') or l.startswith('---') or l.startswith('@@ '):
            continue
        if l.strip(): res.append(l)
    return '\n'.join(res)

identical = []
different = []

for p in pairs:
    t, h1, h2, s1, s2 = p
    d1 = get_clean_diff(h1)
    d2 = get_clean_diff(h2)
    if d1 == d2:
        identical.append(p)
    else:
        different.append(p)

with open('/home/codespace/.gemini/antigravity-cli/brain/81a1ecb4-595a-4138-a982-e79bf6448238/twin_commits_analysis.md', 'w') as f:
    f.write("# Analisis Mendalam Commit Kembar (16.2 vs ax)\n\n")
    f.write(f"Dari {len(pairs)} pasangan commit yang terdeteksi kembar, **{len(identical)}** identik kodenya, sedangkan **{len(different)}** memiliki perbedaan kode.\n\n")
    f.write("## 🟢 Identik (Hanya Beda Konteks/Nama)\n")
    for p in identical:
        f.write(f"- `{p[1][:7]}` == `{p[2][:7]}` ({p[0]})\n")
        f.write(f"  - {p[3]}\n")
    f.write("\n## 🔴 Berbeda (Terdapat Perbedaan Kode)\n")
    for p in different:
        f.write(f"- `{p[1][:7]}` vs `{p[2][:7]}` ({p[0]})\n")
        f.write(f"  - 16.2: {p[3]}\n  - ax: {p[4]}\n")
