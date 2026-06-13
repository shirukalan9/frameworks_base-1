#!/bin/bash
commits="ae64325 58a748a 7ba07d8 4fe5b7e"

for hash in $commits; do
    echo "======================================"
    echo "Attempting to pick $hash"
    git cherry-pick $hash
    if [ $? -ne 0 ]; then
        echo "[!] Conflict on $hash. Aborting..."
        git cherry-pick --abort
        
        echo "--> Checking missing prerequisites..."
        # Get files touched by this commit
        files=$(git show --name-only --format= $hash | grep -v '^$')
        for f in $files; do
            echo "   File: $f"
            # List commits missing in ax that modified this file, strictly before this hash
            git log --oneline --reverse ax..${hash}^ -- "$f" | sed 's/^/      /'
        done
    else
        echo "[+] Successfully picked $hash"
    fi
done
