from playwright.sync_api import sync_playwright
import time

#==================#
LOGIN = 'pepsi cola'
PASSWORD = '12345678'
#==================#



playwright = sync_playwright().start()
browser = playwright.chromium.launch(headless=False)
page = browser.new_page()

page.goto("https://therebk.com/game.php")
page.wait_for_load_state("networkidle")

#===============loging in===========================
page.fill("#login", LOGIN)          
page.fill("#password", PASSWORD)       
page.click("button:has-text('Войти')")
print('Done')
#=============waiting===========================










print("Ctrl+C in bash to close.")
try:
    while True:
        time.sleep(1)  # бесконечное ожидание
except KeyboardInterrupt:
    print("Killing...")
    browser.close()
    playwright.stop()

