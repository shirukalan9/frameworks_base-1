with open('/home/codespace/.gemini/antigravity-cli/brain/81a1ecb4-595a-4138-a982-e79bf6448238/cherrypick_list.md') as f:
    for line in f:
        if line.startswith('- '):
            print(line.strip()[2:].split(' ')[0])
            break
