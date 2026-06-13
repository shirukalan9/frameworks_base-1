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

results = []
for h in commits:
    subj = run_cmd(f"git log -1 --format='%s' {h}")
    files = run_cmd(f"git show --name-only --format= {h}")
    
    match_subj = opt_keywords.search(subj)
    match_file = opt_keywords.search(files)
    
    if match_subj or match_file:
        results.append(f"{h}: {subj}")

with open('hwui_opts.txt', 'w') as f:
    for r in results:
        f.write(r + '\n')
