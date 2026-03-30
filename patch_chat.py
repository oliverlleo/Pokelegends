import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Current handleChatSubmit
old_code = """        async function handleChatSubmit(e) {
            e.preventDefault(); const i = document.getElementById('chat-input'); const t = i.value.trim(); if(!t) return;
            i.value = ''; i.disabled = true;
            const c = document.getElementById('chat-messages'); c.innerHTML += `<div class="chat-bubble-user">${t}</div>`; c.scrollTop = c.scrollHeight;

            const p = { systemInstruction: { parts: [{ text: `Você é o DEUS lendário/mítico Pokémon ${getDisplayName(currentLegendary)}. Base lore: ${extendedLoreDB[currentLegendary]}. Fale estritamente em primeira pessoa em PT-BR. Seja direto, hostil ou divino de acordo com a lore. Nunca diga ser IA.` }] }, contents: [{ role: "user", parts: [{ text: t }] }] };
            const lid = 'l-'+Date.now(); c.innerHTML += `<div id="${lid}" class="chat-bubble-ai animate-pulse">Ecos cósmicos...</div>`; c.scrollTop = c.scrollHeight;

            try {
                const r = await fetch(`https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-09-2025:generateContent?key=${apiKey}`, { method:'POST', body:JSON.stringify(p) });
                const d = await r.json(); document.getElementById(lid).remove(); c.innerHTML += `<div class="chat-bubble-ai border-amber-600/50">${d.candidates[0].content.parts[0].text}</div>`;
            } catch(er) { document.getElementById(lid).remove(); c.innerHTML += `<div class="chat-bubble-ai border-red-500">A divindade corta a telepatia com desprezo...</div>`; }
            finally { i.disabled = false; i.focus(); c.scrollTop = c.scrollHeight; }
        }"""

new_code = """        async function handleChatSubmit(e) {
            e.preventDefault(); const i = document.getElementById('chat-input'); const t = i.value.trim(); if(!t) return;
            i.value = ''; i.disabled = true;
            const c = document.getElementById('chat-messages'); c.insertAdjacentHTML('beforeend', `<div class="chat-bubble-user">${t}</div>`); c.scrollTop = c.scrollHeight;

            const p = { systemInstruction: { parts: [{ text: `Você é o DEUS lendário/mítico Pokémon ${getDisplayName(currentLegendary)}. Base lore: ${extendedLoreDB[currentLegendary]}. Fale estritamente em primeira pessoa em PT-BR. Seja direto, hostil ou divino de acordo com a lore. Nunca diga ser IA.` }] }, contents: [{ role: "user", parts: [{ text: t }] }] };
            const lid = 'l-'+Date.now(); c.insertAdjacentHTML('beforeend', `<div id="${lid}" class="chat-bubble-ai animate-pulse">Ecos cósmicos...</div>`); c.scrollTop = c.scrollHeight;

            try {
                const r = await fetch(`https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-09-2025:generateContent?key=${apiKey}`, { method:'POST', headers: { 'Content-Type': 'application/json' }, body:JSON.stringify(p) });
                const d = await r.json();
                const el = document.getElementById(lid); if (el) el.remove();
                let msg = d.candidates && d.candidates[0] && d.candidates[0].content && d.candidates[0].content.parts && d.candidates[0].content.parts[0] ? d.candidates[0].content.parts[0].text : "A divindade hesita... [Erro de comunicação]";
                c.insertAdjacentHTML('beforeend', `<div class="chat-bubble-ai border-amber-600/50">${msg}</div>`);
            } catch(er) {
                console.error("Chat error:", er);
                const el = document.getElementById(lid); if (el) el.remove();
                c.insertAdjacentHTML('beforeend', `<div class="chat-bubble-ai border-red-500">A divindade corta a telepatia com desprezo...</div>`);
            }
            finally { i.disabled = false; i.focus(); c.scrollTop = c.scrollHeight; }
        }"""

if old_code in content:
    content = content.replace(old_code, new_code)
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(content)
    print("Code successfully replaced.")
else:
    print("Old code not found in index.html.")
