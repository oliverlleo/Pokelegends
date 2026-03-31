const fs = require('fs');
let content = fs.readFileSync('index.html', 'utf8');

// Update selectLegendary to set currentCries and play the cry
content = content.replace(
    'currentLegendary = pokeName;',
    'currentLegendary = pokeName;\n            currentCries = null;'
);

const searchStr = `const gifUrl = data.sprites.other?.showdown?.front_default;`;
const replaceStr = `currentCries = data.cries;
            playCry(currentCries?.latest);

            const gifUrl = data.sprites.other?.showdown?.front_default;`;

content = content.replace(searchStr, replaceStr);

fs.writeFileSync('index.html', content);
