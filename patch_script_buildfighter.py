import re

with open('index.html', 'r') as f:
    content = f.read()

old_func = """async function buildFighter(name, level, isEnemy) {
            const r = await fetch(`https://pokeapi.co/api/v2/pokemon/${name}`); const d = await r.json();
            const getStat = (n) => d.stats.find(s=>s.stat.name===n).base_stat;
            const hp = Math.floor(0.01 * (2 * getStat('hp') + 31) * level) + level + 10;
            const atk = Math.floor(0.01 * (2 * getStat('attack') + 31) * level) + 5;
            const def = Math.floor(0.01 * (2 * getStat('defense') + 31) * level) + 5;
            const sprite = isEnemy ? (d.sprites.other?.showdown?.front_default || d.sprites.front_default) : (d.sprites.other?.showdown?.back_default || d.sprites.back_default || d.sprites.front_default);

            const mList = d.moves.map(m=>m.move.url).sort(() => 0.5 - Math.random()).slice(0, 10);
            let fMoves = [];
            for(let url of mList) {
                if(fMoves.length === 4) break;
                const mr = await fetch(url); const md = await mr.json();
                if(md.power > 0) fMoves.push({ name: md.name, power: md.power, type: md.type.name });
            }
            if(fMoves.length === 0) fMoves.push({name: "Struggle", power: 50, type: "normal"});

            return { name: d.name, level, types: d.types.map(t=>t.type.name), hpMax: hp, hpCurrent: hp, atk, def, sprite, moves: fMoves };
        }"""

with open('patch_buildfighter.js', 'r') as f:
    new_func = f.read()

# Indent new_func to match
indented_new_func = ""
for line in new_func.splitlines():
    indented_new_func += "        " + line + "\n"

content = content.replace(old_func, indented_new_func.strip())

with open('index.html', 'w') as f:
    f.write(content)
