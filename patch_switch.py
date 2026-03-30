with open('index.html', 'r') as f:
    content = f.read()

# Make sure the UI labels match the user's new definition:
# The user wants "NO FACIL COLOCA 3 SLOT NA LINHA DE CIMA E 3 NA DE BAIXO"
# To achieve this, we can set the grid styling on `team-slots`.

old_slots = '<div id="team-slots" class="flex flex-wrap justify-center gap-4 mb-6"></div>'
new_slots = '<div id="team-slots" class="grid grid-cols-3 gap-3 mb-6 mx-auto justify-items-center"></div>'

content = content.replace(old_slots, new_slots)

with open('index.html', 'w') as f:
    f.write(content)

print("Patched team-slots UI layout")
