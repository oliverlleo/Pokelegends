const fs = require('fs');
let content = fs.readFileSync('index.html', 'utf8');

// Step 1: Add currentCries variable
content = content.replace('let currentLegendary = null;', 'let currentLegendary = null;\n        let currentCries = null;');

// Step 1: Add playCry function
const playCryFunc = `
        function playCry(url) {
            if (url) {
                const audio = new Audio(url);
                audio.volume = 0.5; // default reasonable volume
                audio.play().catch(e => console.log("Audio play blocked/failed:", e));
            }
        }
`;
content = content.replace('function getDisplayName(name) {', playCryFunc + '\n        function getDisplayName(name) {');

fs.writeFileSync('index.html', content);
