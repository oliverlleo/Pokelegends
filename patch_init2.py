import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

idx = content.find("async function init() {")
print(content[idx:idx+2000])
