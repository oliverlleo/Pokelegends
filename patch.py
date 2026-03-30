import re

with open('index.html', 'r') as f:
    content = f.read()

target = r'const p = { systemInstruction: { parts: \[\{ text: `Você é o DEUS lendário/mítico Pokémon \$\{getDisplayName\(currentLegendary\)\}\. Base lore: \$\{extendedLoreDB\[currentLegendary\]\}\. Fale estritamente em primeira pessoa em PT-BR\. Seja direto, hostil ou divino de acordo com a lore\. Nunca diga ser IA\.` \}\] \}, contents: \[\{ role: "user", parts: \[\{ text: t \}\] \}\] };'
replacement = r'''currentChatHistory.push({ role: "user", parts: [{ text: t }] });
            const p = { systemInstruction: { parts: [{ text: `Você é o DEUS lendário/mítico Pokémon ${getDisplayName(currentLegendary)}. Base lore: ${extendedLoreDB[currentLegendary]}. Fale estritamente em primeira pessoa em PT-BR. Seja direto, hostil ou divino de acordo com a lore. Nunca diga ser IA.` }] }, contents: currentChatHistory };'''

content = re.sub(target, replacement, content)

with open('index.html', 'w') as f:
    f.write(content)
