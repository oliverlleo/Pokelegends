with open('index.html', 'r') as f:
    content = f.read()

# Let's fix the legendary filtering so it actually works properly.
# The user noticed legendaries are in Classic.
# That means my "legendariesList" doesn't have all legendaries, or my logic is wrong.

# We will populate legendariesList from hierarchyTiers when the page loads
old_init = """        async function init() {
            const container = document.getElementById('pyramid-content');
            hierarchyTiers.forEach(tier => {"""

new_init = """        async function init() {
            legendariesList = [];
            hierarchyTiers.forEach(tier => {
                tier.pokemon.forEach(p => legendariesList.push(p));
            });
            const container = document.getElementById('pyramid-content');
            hierarchyTiers.forEach(tier => {"""

content = content.replace(old_init, new_init)

with open('index.html', 'w') as f:
    f.write(content)
