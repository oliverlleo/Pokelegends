from playwright.sync_api import sync_playwright

def test_add_to_team():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto("http://localhost:8000")

        # Esperar que os nodes existam
        page.wait_for_selector(".poke-node")
        page.wait_for_timeout(2000)

        # Clicar num lendário (Arceus, por exemplo)
        page.click(".poke-node")

        # Mudar para aba batalha
        page.click("#tab-btn-battle")

        # Pesquisar e adicionar pikachu
        page.fill("#poke-search", "pikachu")
        page.wait_for_selector("#search-results div")
        page.click("#search-results div:has-text('pikachu')")

        # Verificar se o modal abriu
        page.wait_for_selector("#move-selection-modal:not(.hidden)")

        # Esperar carregar golpes
        page.wait_for_selector("#move-list-container div.group", timeout=60000)

        # Precisamos de obter novamente os elementos pois podem ser recriados no DOM
        for i in range(4):
            # Obtemos os elementos sempre do DOM atual
            moves = page.query_selector_all("#move-list-container div.group")
            if i < len(moves):
                moves[i].click()
                page.wait_for_timeout(500)

        # Verificar se botão habilitou e confirmar
        assert not page.is_disabled("#btn-confirm-moves")
        page.click("#btn-confirm-moves")

        # Verificar se adicionou à equipa
        page.wait_for_selector("#team-slots img")

        print("Success: Move selection works!")
        browser.close()

test_add_to_team()
