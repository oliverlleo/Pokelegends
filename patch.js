const fs = require('fs');
let html = fs.readFileSync('index.html', 'utf8');

const targetStr = `                let msg = d.candidates && d.candidates[0] && d.candidates[0].content && d.candidates[0].content.parts && d.candidates[0].content.parts[0] ? d.candidates[0].content.parts[0].text : "A divindade hesita... [Erro de comunicação. Verifique se sua chave API é válida.]";
                c.insertAdjacentHTML('beforeend', \`<div class="chat-bubble-ai border-amber-600/50">\${msg}</div>\`);`;

const replaceStr = `                let msg = "";
                if (d.error && d.error.message) {
                    msg = "A divindade corta a telepatia com desprezo... [" + d.error.message + "]";
                } else if (d.candidates && d.candidates[0] && d.candidates[0].content && d.candidates[0].content.parts && d.candidates[0].content.parts[0]) {
                    msg = d.candidates[0].content.parts[0].text;
                } else {
                    msg = "A divindade hesita... [Resposta não reconhecida ou vazia do modelo.]";
                }
                c.insertAdjacentHTML('beforeend', \`<div class="chat-bubble-ai border-amber-600/50">\${msg}</div>\`);`;

if (html.includes(targetStr)) {
    html = html.replace(targetStr, replaceStr);
    fs.writeFileSync('index.html', html, 'utf8');
    console.log("Replaced successfully");
} else {
    console.log("Could not find target string");
}
