import re

with open('index.html', 'r') as f:
    content = f.read()

old_func = """async function addToTeam(name, url) {
            if(myTeam.length >= maxTeamSize || myTeam.find(p => p.name === name)) return;
            const id = url.split('/').filter(Boolean).pop();
            myTeam.push({ name, url, sprite: `https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/${id}.png` });
            renderTeamSlots();
        }"""

with open('patch_addtoteam.js', 'r') as f:
    new_func = f.read()

# Indent new_func to match
indented_new_func = ""
for line in new_func.splitlines():
    indented_new_func += "        " + line + "\n"

content = content.replace(old_func, indented_new_func.strip())

with open('index.html', 'w') as f:
    f.write(content)
