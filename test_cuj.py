from playwright.sync_api import sync_playwright

def run_cuj(page):
    page.goto("http://127.0.0.1:8000/index.html")
    page.wait_for_timeout(2000)

    # Click on a legendary pokemon to open the modal
    page.click("#node-mewtwo")
    page.wait_for_timeout(2000)

    # Click on "Telepatia" tab
    page.click("#tab-btn-chat")
    page.wait_for_timeout(1000)

    # Fill and submit a chat message
    page.fill("#chat-input", "Quem é você?")
    page.click("#chat-send-btn")
    page.wait_for_timeout(3000)

    # Take screenshot at the key moment
    page.screenshot(path="verification.png")
    page.wait_for_timeout(1000)

if __name__ == "__main__":
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            record_video_dir="videos"
        )
        page = context.new_page()
        try:
            run_cuj(page)
        finally:
            context.close()
            browser.close()
