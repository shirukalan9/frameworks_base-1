import subprocess

def run_cmd(cmd):
    return subprocess.check_output(cmd, shell=True).decode('utf-8').strip().split('\n')

# Get the 26 hwui commits
with open('hwui_to_pick.txt') as f:
    hwui_commits = set([line.strip() for line in f if line.strip()])

# Get all commits in 16.2 in reverse topological order (oldest parent to newest child)
topo_commits = run_cmd("git rev-list --topo-order --reverse 16.2")

sorted_hwui = []
for h in topo_commits:
    # the rev-list outputs full hashes. Our hwui_commits might be short hashes.
    # Actually, they are full hashes! Let's check length.
    short_h = h[:7]
    # Check if this full hash is in hwui_commits
    if h in hwui_commits:
        sorted_hwui.append(h)
    else:
        # Just in case hwui_commits are 12-char
        for hc in hwui_commits:
            if h.startswith(hc):
                sorted_hwui.append(h)
                break

with open('hwui_topo_sorted.txt', 'w') as f:
    for h in sorted_hwui:
        f.write(h + '\n')

print(f"Found {len(sorted_hwui)} out of {len(hwui_commits)} commits in topo order.")
