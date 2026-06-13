import subprocess

def run_cmd(cmd):
    return subprocess.check_output(cmd, shell=True).decode('utf-8').strip().split('\n')

ax_commits = run_cmd("git log --format='%H|%an|%ad|%s' --date=unix ax")
missing_commits = run_cmd("cat missing_16.2_in_ax.txt")

# Build indices
author_map = {}
subject_map = {}

for line in ax_commits:
    if not line: continue
    parts = line.split('|', 3)
    if len(parts) == 4:
        h, an, ad, s = parts
        author_map[f"{an}|{ad}"] = h
        subject_map[s] = h

pairs = []
with open("pairs.txt", "w") as f:
    for line in missing_commits:
        if not line: continue
        h = line.split(' ')[0]
        # Get details
        details = run_cmd(f"git log -1 --format='%an|%ad|%s' --date=unix {h}")[0].split('|', 2)
        if len(details) == 3:
            an, ad, s = details
            if s in subject_map:
                f.write(f"PAIR_SUBJECT {h} {subject_map[s]}\n")
            elif f"{an}|{ad}" in author_map:
                f.write(f"PAIR_AUTHOR {h} {author_map[f'{an}|{ad}']}\n")

