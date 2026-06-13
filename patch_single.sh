#!/bin/bash
hash="8fda7c4fec56b9bb2801aa1d889cf0bd85bdb4a8"
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
