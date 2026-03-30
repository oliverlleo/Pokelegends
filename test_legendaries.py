from playwright.sync_api import sync_playwright

def run_cuj(page):
    page.goto("http://localhost:8000")
    page.wait_for_timeout(2000)

    # Try getting length of legendariesList
    length = page.evaluate("legendariesList.length")
    print(f"legendariesList length: {length}")

    # Check if a known legendary is in the list
    has_mewtwo = page.evaluate("legendariesList.includes('mewtwo')")
    print(f"Has Mewtwo: {has_mewtwo}")

if __name__ == "__main__":
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        run_cuj(page)
        browser.close()
