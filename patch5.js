const fs = require('fs');
let content = fs.readFileSync('index.html', 'utf8');

const targetStr = `        function animateDetailImg() {
            const img = document.getElementById('detail-img');
            const anims = ['anim-lunge-player', 'anim-lunge-enemy', 'anim-damage', 'anim-shake'];
            const randomAnim = anims[Math.floor(Math.random() * anims.length)];

            img.classList.remove('anim-lunge-player', 'anim-lunge-enemy', 'anim-damage', 'anim-shake');
            void img.offsetWidth; // force reflow
            img.classList.add(randomAnim);

            setTimeout(() => {
                img.classList.remove(randomAnim);
            }, 500);
        }`;

const newStr = `        function animateDetailImg() {
            const img = document.getElementById('detail-img');
            const anims = ['anim-lunge-player', 'anim-lunge-enemy', 'anim-damage', 'anim-shake'];
            const randomAnim = anims[Math.floor(Math.random() * anims.length)];

            img.classList.remove('anim-lunge-player', 'anim-lunge-enemy', 'anim-damage', 'anim-shake');
            void img.offsetWidth; // force reflow
            img.classList.add(randomAnim);

            // Secret event 5% chance
            if (Math.random() < 0.05) {
                playCry(currentCries?.legacy);
                spawnVFX('drawer-header', '#fbbf24');
            } else {
                playCry(currentCries?.latest);
            }

            setTimeout(() => {
                img.classList.remove(randomAnim);
            }, 500);
        }`;

content = content.replace(targetStr, newStr);

fs.writeFileSync('index.html', content);
