import re

with open('index.html', 'r') as f:
    content = f.read()

# 1. State Variables
content = content.replace(
    "let myTeam = [];",
    "let legendariesList = Object.keys(extendedLoreDB);\n        let myTeam = [];\n        let currentDifficulty = 'normal';\n        let currentGameMode = 'standard';\n        let maxTeamSize = 3;"
)

# 2. UI Injection
new_ui = """
                    <h3 class="text-amber-500 font-bold mb-3 text-center text-sm tracking-widest uppercase mt-4">Selecionar Modo de Batalha</h3>
                    <div class="flex flex-col sm:flex-row gap-2 justify-center mb-4">
                        <label class="flex-1 cursor-pointer">
                            <input type="radio" name="gameMode" value="standard" class="peer hidden" onchange="changeGameMode('standard')" checked>
                            <div class="text-center p-2 rounded-lg border-2 border-slate-600 peer-checked:border-blue-500 peer-checked:bg-blue-500/20 text-slate-300 peer-checked:text-blue-400 transition-all font-bold text-sm">
                                Clássico (Comum vs Lenda)
                            </div>
                        </label>
                        <label class="flex-1 cursor-pointer">
                            <input type="radio" name="gameMode" value="rivalry" class="peer hidden" onchange="changeGameMode('rivalry')">
                            <div class="text-center p-2 rounded-lg border-2 border-slate-600 peer-checked:border-fuchsia-500 peer-checked:bg-fuchsia-500/20 text-slate-300 peer-checked:text-fuchsia-400 transition-all font-bold text-sm">
                                Rivalidade (Lenda vs Lenda)
                            </div>
                        </label>
                    </div>

                    <div id="difficulty-selector" class="mb-4">
                        <h3 class="text-amber-500 font-bold mb-3 text-center text-xs tracking-widest uppercase">Dificuldade (Clássico)</h3>
                        <div class="flex flex-col sm:flex-row gap-2 justify-center">
                            <label class="flex-1 cursor-pointer">
                                <input type="radio" name="difficulty" value="easy" class="peer hidden" onchange="changeDifficulty('easy')">
                                <div class="text-center py-1 px-2 rounded-lg border-2 border-slate-600 peer-checked:border-green-500 peer-checked:bg-green-500/20 text-slate-400 peer-checked:text-green-400 transition-all font-bold text-xs">
                                    Fácil (6 Pkmn)
                                </div>
                            </label>
                            <label class="flex-1 cursor-pointer">
                                <input type="radio" name="difficulty" value="normal" class="peer hidden" onchange="changeDifficulty('normal')" checked>
                                <div class="text-center py-1 px-2 rounded-lg border-2 border-slate-600 peer-checked:border-amber-500 peer-checked:bg-amber-500/20 text-slate-400 peer-checked:text-amber-400 transition-all font-bold text-xs">
                                    Normal (3 Pkmn)
                                </div>
                            </label>
                            <label class="flex-1 cursor-pointer">
                                <input type="radio" name="difficulty" value="hard" class="peer hidden" onchange="changeDifficulty('hard')">
                                <div class="text-center py-1 px-2 rounded-lg border-2 border-slate-600 peer-checked:border-red-500 peer-checked:bg-red-500/20 text-slate-400 peer-checked:text-red-400 transition-all font-bold text-xs">
                                    Difícil (1 Pkmn)
                                </div>
                            </label>
                        </div>
                    </div>
"""

old_ui_start = '<p class="text-slate-400 text-sm text-center mb-4">Selecione 3 Pokémon comuns (Lvl 65) para enfrentar esta Lenda (Lvl 100).</p>'
new_ui_start = '<p class="text-slate-400 text-sm text-center mb-4" id="mode-desc">Selecione Pokémon comuns (Nv 65) ou lute no Difícil (Nv 75) contra esta Lenda (Nv 100).</p>' + new_ui

content = content.replace(old_ui_start, new_ui_start)

# Update the team slots markup
old_slots = """<div class="flex justify-center gap-3 mb-6">
                    <div id="slot-0" class="w-16 h-16 sm:w-20 sm:h-20 rounded-xl border-2 border-dashed border-slate-600 flex items-center justify-center bg-slate-800 relative cursor-pointer" onclick="removeSlot(0)"></div>
                    <div id="slot-1" class="w-16 h-16 sm:w-20 sm:h-20 rounded-xl border-2 border-dashed border-slate-600 flex items-center justify-center bg-slate-800 relative cursor-pointer" onclick="removeSlot(1)"></div>
                    <div id="slot-2" class="w-16 h-16 sm:w-20 sm:h-20 rounded-xl border-2 border-dashed border-slate-600 flex items-center justify-center bg-slate-800 relative cursor-pointer" onclick="removeSlot(2)"></div>
                </div>"""
new_slots = '<div id="team-slots" class="flex flex-wrap justify-center gap-4 mb-6"></div>'
content = content.replace(old_slots, new_slots)

# Update placeholder text
content = content.replace('placeholder="Pesquisar Pokémon Comum..."', 'placeholder="Pesquisar Pokémon Comum..."')


# 3. Javascript Logic Injection
js_funcs = """
        function changeGameMode(mode) {
            currentGameMode = mode;
            document.getElementById('difficulty-selector').style.display = (mode === 'standard') ? 'block' : 'none';
            document.getElementById('poke-search').placeholder = (mode === 'standard') ? 'Pesquisar Pokémon Comum...' : 'Pesquisar Lendário/Mítico...';
            document.getElementById('mode-desc').innerText = (mode === 'standard') ? 'Selecione Pokémon comuns (Nv 65) ou lute no Difícil (Nv 75) contra esta Lenda (Nv 100).' : 'Escolha um Deus para uma Batalha de Rivalidade 1v1 (Nv 100).';

            if (mode === 'rivalry') {
                maxTeamSize = 1;
            } else {
                changeDifficulty(currentDifficulty); // Reset to selected difficulty
                return;
            }

            if (myTeam.length > maxTeamSize) myTeam = myTeam.slice(0, maxTeamSize);
            renderTeamSlots();
            checkBattleReady();
            filterSearch();
        }

        function changeDifficulty(diff) {
            currentDifficulty = diff;
            if (currentGameMode === 'rivalry') return;

            if (diff === 'easy') maxTeamSize = 6;
            else if (diff === 'normal') maxTeamSize = 3;
            else if (diff === 'hard') maxTeamSize = 1;

            if (myTeam.length > maxTeamSize) {
                myTeam = myTeam.slice(0, maxTeamSize);
            }
            renderTeamSlots();
            checkBattleReady();
        }
"""
content = content.replace("function switchTab(tab) {", js_funcs + "\n        function switchTab(tab) {")

# 4. Modifying existing javascript functions
# fetch originals to not exclude legendaries yet
old_fetch = """            fetch('https://pokeapi.co/api/v2/pokemon?limit=1200').then(r=>r.json()).then(d => {
                const legendKeys = Object.keys(extendedLoreDB);
                globalPokedex = d.results.filter(p => !legendKeys.includes(p.name) && !p.name.includes('-'));
                renderSearch(globalPokedex.slice(0, 20));
            });"""
new_fetch = """            fetch('https://pokeapi.co/api/v2/pokemon?limit=1200').then(r=>r.json()).then(d => {
                globalPokedex = d.results.filter(p => !p.name.includes('-'));
                filterSearch(); // use our new filter logic
            });"""
content = content.replace(old_fetch, new_fetch)

# update filterSearch
old_filter = """        function filterSearch() {
            const q = document.getElementById('poke-search').value.toLowerCase();
            renderSearch(globalPokedex.filter(p => p.name.includes(q)).slice(0, 20));
        }"""
new_filter = """        function filterSearch() {
            const q = document.getElementById('poke-search').value.toLowerCase();
            let filtered = globalPokedex.filter(p => p.name.includes(q));

            if (currentGameMode === 'rivalry') {
                filtered = filtered.filter(p => legendariesList.includes(p.name));
            } else {
                filtered = filtered.filter(p => !legendariesList.includes(p.name));
            }

            renderSearch(filtered.slice(0, 20));
        }"""
content = content.replace(old_filter, new_filter)

# addToTeam hardcoded 3 -> maxTeamSize
content = content.replace("if(myTeam.length >= 3", "if(myTeam.length >= maxTeamSize")

# checkBattleReady
old_cbr = """        function checkBattleReady() {
            const btn = document.getElementById('btn-start-battle');
            if(myTeam.length === 3) { btn.disabled = false; btn.classList.remove('opacity-50', 'cursor-not-allowed'); btn.innerText = "INICIAR BATALHA ÉPICA"; }
            else { btn.disabled = true; btn.classList.add('opacity-50', 'cursor-not-allowed'); btn.innerText = "Selecionar 3 para Iniciar"; }
        }"""
new_cbr = """        function checkBattleReady() {
            const btn = document.getElementById('btn-start-battle');
            if(myTeam.length === maxTeamSize) { btn.disabled = false; btn.classList.remove('opacity-50', 'cursor-not-allowed'); btn.innerText = "INICIAR BATALHA ÉPICA"; }
            else { btn.disabled = true; btn.classList.add('opacity-50', 'cursor-not-allowed'); btn.innerText = `Selecionar ${maxTeamSize} para Iniciar`; }
        }"""
content = content.replace(old_cbr, new_cbr)

# renderTeamSlots hardcoded HTML
old_rts = """        function renderTeamSlots() {
            for(let i=0; i<3; i++) {
                const slot = document.getElementById(`slot-${i}`);
                if(myTeam[i]) {
                    slot.innerHTML = `<img src="${myTeam[i].sprite}" class="w-full h-full object-contain pixelated-img"><div class="absolute -top-2 -right-2 bg-red-500 text-white rounded-full w-5 h-5 flex items-center justify-center text-xs shadow-lg">X</div>`;
                    slot.classList.replace('border-dashed', 'border-solid'); slot.classList.replace('border-slate-600', 'border-amber-500');
                } else {
                    slot.innerHTML = `<span class="text-slate-600 font-bold text-xl">+</span>`;
                    slot.classList.replace('border-solid', 'border-dashed'); slot.classList.replace('border-amber-500', 'border-slate-600');
                }
            }
            checkBattleReady();
        }"""
new_rts = """        function renderTeamSlots() {
            const container = document.getElementById('team-slots');
            container.innerHTML = '';
            for(let i=0; i<maxTeamSize; i++) {
                const slot = document.createElement('div');
                slot.id = `slot-${i}`;
                slot.className = "w-16 h-16 sm:w-20 sm:h-20 rounded-xl border-2 flex items-center justify-center bg-slate-800/50 relative overflow-visible cursor-pointer transition-colors";
                if(myTeam[i]) {
                    slot.innerHTML = `<img src="${myTeam[i].sprite}" class="w-full h-full object-contain pixelated-img"><div class="absolute -top-2 -right-2 bg-red-500 text-white rounded-full w-5 h-5 flex items-center justify-center text-xs shadow-lg">X</div>`;
                    slot.classList.add('border-solid', 'border-amber-500');
                    slot.onclick = () => removeSlot(i);
                } else {
                    slot.innerHTML = `<span class="text-slate-600 font-bold text-xl">+</span>`;
                    slot.classList.add('border-dashed', 'border-slate-600');
                    slot.onclick = null;
                }
                container.appendChild(slot);
            }
            checkBattleReady();
        }"""
content = content.replace(old_rts, new_rts)

# startBattle logic
old_sb = """                const enemy = await buildFighter(currentLegendary, 100, true);
                const p1 = await buildFighter(myTeam[0].name, 65, false);
                const p2 = await buildFighter(myTeam[1].name, 65, false);
                const p3 = await buildFighter(myTeam[2].name, 65, false);

                battleState = { playerTeam: [p1, p2, p3], enemyTeam: [enemy], activePlayerIdx: 0, activeEnemyIdx: 0, isOver: false };"""

new_sb = """                const enemy = await buildFighter(currentLegendary, 100, true);
                let pLevel = currentDifficulty === 'hard' ? 75 : 65;
                if (currentGameMode === 'rivalry') pLevel = 100;

                const playerTeam = [];
                for(let i=0; i<maxTeamSize; i++) {
                    const p = await buildFighter(myTeam[i].name, pLevel, false);
                    playerTeam.push(p);
                }

                battleState = { playerTeam: playerTeam, enemyTeam: [enemy], activePlayerIdx: 0, activeEnemyIdx: 0, isOver: false };"""
content = content.replace(old_sb, new_sb)

# fix the visual bug (GIFs) and skill types
# First: Upscale GIFs via CSS
content = content.replace(".pixelated-img { image-rendering: pixelated; }", ".pixelated-img { image-rendering: pixelated; transform: scale(1.5); transform-origin: bottom center; }")

# Second: Colorize VFX via skill type
old_vfx = """        function spawnVFX(containerId) {
            const container = document.getElementById(containerId);
            const vfx = document.createElement('div');
            vfx.className = 'vfx-impact';
            container.appendChild(vfx);
            setTimeout(() => vfx.remove(), 500);
        }"""
new_vfx = """        function spawnVFX(containerId, color) {
            const container = document.getElementById(containerId);
            const vfx = document.createElement('div');
            vfx.className = 'vfx-impact';
            if(color) vfx.style.background = `radial-gradient(circle, #fff 0%, ${color} 40%, transparent 80%)`;
            container.appendChild(vfx);
            setTimeout(() => vfx.remove(), 500);
        }"""
content = content.replace(old_vfx, new_vfx)

# pass type to spawnVFX
old_impact = "spawnVFX(containerId);"
new_impact = "spawnVFX(containerId, typeColors[m.type]);"
content = content.replace(old_impact, new_impact)

with open('index.html', 'w') as f:
    f.write(content)

print("Done resetting and patching.")
