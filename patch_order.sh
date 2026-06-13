#!/bin/bash
hash1="db53a5da8e91cdb628bc962b2754226254798fda"
hash2="b82819e54df482791f2620e1cdd1c4e9ad006a9a"

curl -sL "https://github.com/LOSModified/android_frameworks_base/commit/${hash1}.patch" -o patch1.patch
curl -sL "https://github.com/LOSModified/android_frameworks_base/commit/${hash2}.patch" -o patch2.patch

subj1=$(grep -m 1 "^Subject: " patch1.patch | sed -E 's/^Subject: (\[[^]]+\] )?//')
subj2=$(grep -m 1 "^Subject: " patch2.patch | sed -E 's/^Subject: (\[[^]]+\] )?//')

echo "=== Attempting Order 1: $hash1 then $hash2 ==="
git am patch1.patch
if [ $? -eq 0 ]; then
    echo "[+] Applied 1"
    git am patch2.patch
    if [ $? -eq 0 ]; then
        echo "[+] Applied 2. Success!"
        exit 0
    else
        echo "[!] Order 1 failed on patch 2. Aborting..."
        git am --abort
        git reset --hard HEAD~1
    fi
else
    echo "[!] Order 1 failed on patch 1. Aborting..."
    git am --abort
fi

echo "=== Attempting Order 2 (Reversed): $hash2 then $hash1 ==="
git am patch2.patch
if [ $? -eq 0 ]; then
    echo "[+] Applied 2"
    git am patch1.patch
    if [ $? -eq 0 ]; then
        echo "[+] Applied 1. Success!"
        exit 0
    else
        echo "[!] Order 2 failed on patch 1. Aborting..."
        git am --abort
        git reset --hard HEAD~1
    fi
else
    echo "[!] Order 2 failed on patch 2. Aborting..."
    git am --abort
fi

echo "=== Both Git AM orders failed. Falling back to patch -p1 ==="
for patchfile in patch1.patch patch2.patch; do
    if [ "$patchfile" = "patch1.patch" ]; then
        subject=$subj1
    else
        subject=$subj2
    fi
    echo "Applying $subject via patch -p1..."
    patch -p1 --forward < $patchfile
    if [ $? -eq 0 ]; then
        echo "[+] Successfully applied via patch -p1!"
        git add .
        git commit -m "$subject"
    else
        echo "[!] patch -p1 failed/skipped."
        git checkout -- .
    fi
done
