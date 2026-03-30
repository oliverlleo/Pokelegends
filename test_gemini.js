async function test() {
  const p = {
    systemInstruction: { parts: [{ text: `Você é um DEUS` }] },
    contents: [{ role: "user", parts: [{ text: "oi" }] }]
  };
  const r = await fetch(`https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key=dummy`, {
    method:'POST',
    headers: { 'Content-Type': 'application/json' },
    body:JSON.stringify(p)
  });
  console.log(r.status);
  const data = await r.json();
  console.log(data);
}
test();
