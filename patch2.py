import re

with open('index.html', 'r') as f:
    content = f.read()

target1 = r'msg = d\.candidates\[0\]\.content\.parts\[0\]\.text;\n                    c\.insertAdjacentHTML\(\'beforeend\', `<div class="chat-bubble-ai border-amber-600/50">\$\{msg\}</div>`\);'
rep1 = r'''msg = d.candidates[0].content.parts[0].text;
                    currentChatHistory.push({ role: "model", parts: [{ text: msg }] });
                    c.insertAdjacentHTML('beforeend', `<div class="chat-bubble-ai border-amber-600/50">${msg}</div>`);'''

target2 = r'msg = "A divindade corta a telepatia com desprezo\.\.\. \[" \+ d\.error\.message \+ "\]";'
rep2 = r'''currentChatHistory.pop();
                    msg = "A divindade corta a telepatia com desprezo... [" + d.error.message + "]";'''

target3 = r'msg = "A divindade hesita\.\.\. \[Resposta não reconhecida ou vazia do modelo\.\]";'
rep3 = r'''currentChatHistory.pop();
                    msg = "A divindade hesita... [Resposta não reconhecida ou vazia do modelo.]";'''

target4 = r'console\.error\("Chat error:", er\);'
rep4 = r'''currentChatHistory.pop();
                console.error("Chat error:", er);'''

content = re.sub(target1, rep1, content)
content = re.sub(target2, rep2, content)
content = re.sub(target3, rep3, content)
content = re.sub(target4, rep4, content)

with open('index.html', 'w') as f:
    f.write(content)
