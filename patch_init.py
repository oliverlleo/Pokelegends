import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# I need to see where init() is defined.
idx = content.find("function init() {")
if idx == -1:
    idx = content.find("async function init() {")

if idx != -1:
    print(content[idx-100:idx+500])
else:
    print("Not found")
