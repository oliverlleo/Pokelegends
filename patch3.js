const fs = require('fs');
let content = fs.readFileSync('index.html', 'utf8');

const targetStr = `<div id="detail-types" class="flex justify-center gap-2"></div>\n            </div>`;

const newButtonHTML = `<div id="detail-types" class="flex justify-center gap-2"></div>
                <button id="btn-play-cry" onclick="playCry(currentCries?.latest)" class="mt-3 mx-auto bg-slate-800 hover:bg-slate-700 text-amber-400 border border-amber-600/50 rounded-full px-4 py-1 text-xs uppercase font-bold flex items-center gap-2 transition-colors">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15.536 8.464a5 5 0 010 7.072M17.657 6.343a8 8 0 010 11.314M12 4v16m0 0l-4-4H4a2 2 0 01-2-2V10a2 2 0 012-2h4l4-4z" />
                    </svg>
                    Ouvir presença
                </button>
            </div>`;

content = content.replace(targetStr, newButtonHTML);
fs.writeFileSync('index.html', content);
