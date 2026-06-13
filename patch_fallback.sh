#!/bin/bash
commits="b8c3420ded82036dc618b5bbcf87a623e3bab511 b0ea4276e437bddd07dc0142ad28dea0e9a39ffe 792d1b1e610a8a9e6a90c092e4b717cd076327cb"

for hash in $commits; do
    echo "======================================"
    echo "Downloading patch for $hash..."
    curl -sL "https://github.com/LOSModified/android_frameworks_base/commit/${hash}.patch" -o temp.patch
    subject=$(grep -m 1 "^Subject: " temp.patch | sed -E 's/^Subject: (\[[^]]+\] )?//')
    echo "Applying via patch -p1: $subject"
    patch -p1 --forward < temp.patch
    if [ $? -eq 0 ]; then
        echo "[+] Successfully applied $hash with patch -p1!"
        git add .
        git commit -m "$subject"
    else
        echo "[!] patch -p1 failed for $hash. Reverting changes..."
        git checkout -- .
    fi
done
