#!/bin/bash
# 1. Cherry-pick the requested commits in chronological order
echo "Cherry-picking requested commits..."
for hash in $(grep -E '7b09728|5b9d591|e3d75dc|b3d04c6|d443555|2f05351|9103107|1cf4c07|e3a53a7|25b866b|6d3d30d|e01ce2e|9ddd028' /home/codespace/.gemini/antigravity-cli/brain/81a1ecb4-595a-4138-a982-e79bf6448238/cherrypick_list.md | awk '{print $2}'); do
    echo "Picking $hash"
    git cherry-pick $hash || { echo "Conflict on $hash"; git cherry-pick --abort; exit 1; }
done
echo "Cherry-pick successful."

# 2. Find hwui/libui optimization commits among the missing ones
echo "Searching for hwui/libui optimizations..."
> hwui_opts.txt
while read -r line; do
    hash=$(echo $line | awk '{print $2}')
    # Check if commit touches hwui or ui, or subject mentions it
    git log -1 --format="%s" $hash | grep -iE 'hwui|libui|skia|render|opengl|vulkan|optimiz|perf|cache|leak|speed|fast|reduce|alloc|inline' > /dev/null
    if [ $? -eq 0 ]; then
        echo "$hash: $(git log -1 --format='%s' $hash)" >> hwui_opts.txt
    else
        # check files changed
        git show --name-only --format= $hash | grep -iE 'hwui|libui' > /dev/null
        if [ $? -eq 0 ]; then
            echo "$hash: $(git log -1 --format='%s' $hash) [Touches hwui/libui]" >> hwui_opts.txt
        fi
    fi
done < <(grep '^- ' /home/codespace/.gemini/antigravity-cli/brain/81a1ecb4-595a-4138-a982-e79bf6448238/cherrypick_list.md)

