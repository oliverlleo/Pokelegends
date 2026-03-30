with open('index.html', 'r') as f:
    content = f.read()

# Wait, he said: "NO FACIL COLOCA 3 SLOT NA LINHA DE CIMA E 3 NA DE BAIXO"
# But he also said: "e se for facil e para ser 1 so" -> No, read again: "quando ta na facil eu so consigo seleciona 3 dos 6 porra" -> So easy is 6 slots.

# Fix checkBattleReady mapping text to not hardcode "Selecionar 3 para Iniciar" if disabled. It should be maxTeamSize.
# Wait, it IS maxTeamSize: `btn.innerText = \`Selecionar ${maxTeamSize} para Iniciar\`;`
# BUT what if the DOM has the text hardcoded? Let's check the HTML.

import re
content = re.sub(
    r'<button id="btn-start-battle"([^>]+)>Selecionar 3 para Iniciar</button>',
    r'<button id="btn-start-battle"\1>Selecionar Equipa</button>',
    content
)

with open('index.html', 'w') as f:
    f.write(content)

print("Patched button initial text")
