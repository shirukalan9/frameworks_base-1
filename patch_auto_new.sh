#!/bin/bash
commits="21dea741a455ebbacbd21695365957092462f1ab 9815990172b48e96c9cd6be365cacaacff9ddbe7 a0bb6ec5f08138b1dd6a0a8e3f8a0e699029a374 24fed1a3a76d37288cb1494a10a7e907d626b0c8 c33768aae322b7900ad7fff465e923cd7f2cf69f"

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
