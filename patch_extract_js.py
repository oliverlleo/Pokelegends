import re
import os

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

start = content.find('<script>')
end = content.find('</script>', start)

js_code = content[start+8:end]
with open('script.js', 'w', encoding='utf-8') as f:
    f.write(js_code)
