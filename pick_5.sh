#!/bin/bash
# Find the exact topological order
commits="f9755e3 02d480d 7a2706b 4763c7a 5e0765b"
echo "Sorting commits..."
ordered=""
for h in $(git rev-list --topo-order --reverse 16.2); do
    for c in $commits; do
        if [[ $h == $c* ]]; then
            ordered="$ordered $h"
        fi
    done
done

echo "Ordered commits:$ordered"

for full_h in $ordered; do
    short_h=${full_h:0:7}
    echo "======================================"
    echo "Attempting to pick $short_h"
    git cherry-pick $full_h
    if [ $? -ne 0 ]; then
        echo "[!] Conflict on $short_h. Aborting..."
        git cherry-pick --abort
    else
        echo "[+] Successfully picked $short_h"
    fi
done
