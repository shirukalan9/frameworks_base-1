#!/bin/bash
commits="256c31a09402e9cac3f8d209633c15c8515d697a d9ec9ad767b26d6168ebd46e647cbee7bd9d5d91 e83ec9403ebbf716520c560527fafad8896a0efc 42158ecb9c85a23c2f4805b26cac4f4867ee963f febf673208bf53a199c5c99ea148253cea8ee4d4"

for hash in $commits; do
    echo "======================================"
    echo "Downloading patch for $hash..."
    curl -sL "https://github.com/LOSModified/android_frameworks_base/commit/${hash}.patch" -o temp.patch
    subject=$(grep -m 1 "^Subject: " temp.patch | sed -E 's/^Subject: (\[[^]]+\] )?//')
    echo "Attempting git am: $subject"
    
    git am temp.patch
    if [ $? -eq 0 ]; then
        echo "[+] Successfully applied $hash with git am!"
    else
        echo "[!] git am failed. Aborting and trying patch -p1..."
        git am --abort
        
        patch -p1 --forward < temp.patch
        if [ $? -eq 0 ]; then
            echo "[+] Successfully applied $hash with patch -p1 fallback!"
            git add .
            git commit -m "$subject"
        else
            echo "[!] patch -p1 also failed/skipped. Reverting changes..."
            git checkout -- .
        fi
    fi
done
