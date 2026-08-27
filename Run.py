from playwright.sync_api import sync_playwright, expect
import time
import re

#==================#
LOGIN = 'pepsi cola'
PASSWORD = '12345678'
#==================#



playwright = sync_playwright().start()
browser = playwright.chromium.launch(headless=False)
page = browser.new_page()

page.goto("https://therebk.com/game.php")
# Проверяем первое поле
expect(page.locator("#login")).to_be_visible()
expect(page.locator("#password")).to_be_visible()


#===============loging in===========================
page.fill("#login", LOGIN)          
page.fill("#password", PASSWORD)       
page.get_by_role("button", name="Войти").click()
print('Done')

#=============waiting===========================
game_frame = page.frame_locator("[name='theframe']")
start_button = game_frame.locator("input[name='start']")

#expect(start_button).to_be_visible(timeout=0)
#start_button.click()

#=============grinding===========================





print("Ctrl+C in bash to close.")
try:
    while True:
        time.sleep(1)  # бесконечное ожидание
except KeyboardInterrupt:
    print("Killing...")
    browser.close()
    playwright.stop()

