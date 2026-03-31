const fs = require('fs');
let content = fs.readFileSync('index.html', 'utf8');

const targetStr = `const lid = 'l-'+Date.now(); c.insertAdjacentHTML('beforeend', \`<div id="\${lid}" class="chat-bubble-ai animate-pulse">Ecos cósmicos...</div>\`); c.scrollTop = c.scrollHeight;`;
const newStr = `const lid = 'l-'+Date.now(); c.insertAdjacentHTML('beforeend', \`<div id="\${lid}" class="chat-bubble-ai animate-pulse">Ecos cósmicos...</div>\`); c.scrollTop = c.scrollHeight;
            playCry(currentCries?.latest);`;

content = content.replace(targetStr, newStr);

fs.writeFileSync('index.html', content);
