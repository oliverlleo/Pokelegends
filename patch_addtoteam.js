let pendingPokemon = null;
let currentAvailableMoves = [];
let selectedMoves = [];

async function addToTeam(name, url) {
    if(myTeam.length >= maxTeamSize || myTeam.find(p => p.name === name)) return;

    const id = url.split('/').filter(Boolean).pop();
    const sprite = `https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/${id}.png`;

    pendingPokemon = { name, url, sprite };
    selectedMoves = [];
    currentAvailableMoves = [];

    document.getElementById('move-selection-img').src = sprite;
    document.getElementById('move-selection-name').innerText = getDisplayName(name);
    document.getElementById('move-selection-count').innerText = "0 / 4 Selecionados";
    document.getElementById('move-list-container').innerHTML = '';
    document.getElementById('btn-confirm-moves').disabled = true;
    document.getElementById('btn-confirm-moves').classList.add('opacity-50', 'cursor-not-allowed');

    document.getElementById('move-selection-modal').classList.remove('hidden');
    document.getElementById('move-selection-modal').classList.add('flex', 'flex-col');
    document.getElementById('move-list-loading').classList.remove('hidden');
    document.getElementById('move-list-loading').classList.add('flex');

    try {
        const query = `
        query {
            pokemon_v2_pokemon(where: {name: {_eq: "${name}"}}) {
                pokemon_v2_pokemonmoves(distinct_on: move_id) {
                    pokemon_v2_move {
                        name
                        power
                        pokemon_v2_type {
                            name
                        }
                    }
                }
            }
        }`;

        const response = await fetch('https://beta.pokeapi.co/graphql/v1beta', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ query })
        });

        const data = await response.json();

        if (data.data && data.data.pokemon_v2_pokemon.length > 0) {
            const movesRaw = data.data.pokemon_v2_pokemon[0].pokemon_v2_pokemonmoves;
            const validMoves = movesRaw
                .map(m => m.pokemon_v2_move)
                .filter(m => m && m.power !== null && m.power > 0)
                .map(m => ({
                    name: m.name,
                    power: m.power,
                    type: m.pokemon_v2_type.name
                }));

            // Remove duplicates just in case
            const uniqueMoves = [];
            const seen = new Set();
            for (const m of validMoves) {
                if (!seen.has(m.name)) {
                    seen.add(m.name);
                    uniqueMoves.push(m);
                }
            }

            currentAvailableMoves = uniqueMoves.sort((a, b) => b.power - a.power);
            renderMoveSelectionList();
        } else {
            // Fallback se não encontrar
            currentAvailableMoves = [{ name: 'Struggle', power: 50, type: 'normal' }];
            renderMoveSelectionList();
        }
    } catch (e) {
        console.error("Error fetching moves:", e);
        currentAvailableMoves = [{ name: 'Struggle', power: 50, type: 'normal' }];
        renderMoveSelectionList();
    } finally {
        document.getElementById('move-list-loading').classList.add('hidden');
        document.getElementById('move-list-loading').classList.remove('flex');
    }
}

function renderMoveSelectionList() {
    const container = document.getElementById('move-list-container');
    container.innerHTML = currentAvailableMoves.map((m, index) => {
        const isSelected = selectedMoves.some(sm => sm.name === m.name);
        const bg = isSelected ? 'bg-amber-600/30 border-amber-500' : 'bg-slate-800 border-slate-700 hover:border-slate-500';
        const typeColor = typeColors[m.type] || '#A8A77A'; // Default to normal if unknown

        return `
            <div onclick="toggleMoveSelection(${index})" class="p-3 rounded-lg border-2 cursor-pointer transition-all ${bg} flex justify-between items-center group">
                <div class="flex flex-col">
                    <span class="text-white font-bold capitalize group-hover:text-amber-300 transition-colors">${m.name.replace('-', ' ')}</span>
                    <span class="text-xs text-slate-400">Poder: <span class="text-slate-200 font-bold">${m.power}</span></span>
                </div>
                <span class="type-badge" style="background:${typeColor}">${m.type}</span>
            </div>
        `;
    }).join('');
}

function toggleMoveSelection(index) {
    const move = currentAvailableMoves[index];
    const selectedIndex = selectedMoves.findIndex(m => m.name === move.name);

    if (selectedIndex > -1) {
        selectedMoves.splice(selectedIndex, 1);
    } else {
        if (selectedMoves.length >= 4) return; // Máximo 4
        selectedMoves.push(move);
    }

    document.getElementById('move-selection-count').innerText = `${selectedMoves.length} / 4 Selecionados`;

    const btn = document.getElementById('btn-confirm-moves');
    if (selectedMoves.length === 4) {
        btn.disabled = false;
        btn.classList.remove('opacity-50', 'cursor-not-allowed');
    } else {
        btn.disabled = true;
        btn.classList.add('opacity-50', 'cursor-not-allowed');
    }

    renderMoveSelectionList();
}

function closeMoveSelection() {
    document.getElementById('move-selection-modal').classList.add('hidden');
    document.getElementById('move-selection-modal').classList.remove('flex', 'flex-col');
    pendingPokemon = null;
    selectedMoves = [];
    currentAvailableMoves = [];
}

function confirmMoveSelection() {
    if (selectedMoves.length !== 4 || !pendingPokemon) return;

    myTeam.push({
        name: pendingPokemon.name,
        url: pendingPokemon.url,
        sprite: pendingPokemon.sprite,
        selectedMoves: [...selectedMoves]
    });

    closeMoveSelection();
    renderTeamSlots();
}
