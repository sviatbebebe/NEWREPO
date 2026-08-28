from playwright.sync_api import sync_playwright, expect
import time

LOGIN = 'pepsi cola'
PASSWORD = '12345678'

playwright = sync_playwright().start()
browser = playwright.chromium.launch(headless=False)
page = browser.new_page()

page.goto("https://therebk.com/game.php")
expect(page.locator("#login")).to_be_visible()
expect(page.locator("#password")).to_be_visible()

page.fill("#login", LOGIN)
page.fill("#password", PASSWORD)
page.get_by_role("button", name="Войти").click()
print('Done')
time.sleep(1)
game_frame = page.frame_locator("[name='theframe']")

def wait_for_loading():
    loading = game_frame.locator("#progressbar-container")
    while True:
        if loading.count() == 0 or not loading.is_visible():
            break
        time.sleep(0.5)
    time.sleep(0.1)

def move(num):
    for _ in range(num):
        wait_for_loading()
        page.keyboard.press("W")
        print('w')
        wait_for_loading()
        time.sleep(0.1)

def turn(side):
    if side == 'r':
        page.keyboard.press("E")
        print('e')
    if side == 'l':
        page.keyboard.press("Q")
        print('q')
    time.sleep(0.2)

def fight():
    enemy = game_frame.locator('div.item img[onclick*="OpenMenu"]')
    if enemy.count() == 0 or not enemy.first.is_visible():
        print("Сбился с пути")
        move(1)
        return

    enemy.first.click()
    time.sleep(0.3)

    game_frame.get_by_text("Напасть", exact=True).click()
    print('Напасть')
    time.sleep(0.2)

    while True:
        # Сначала проверяем, не закончился ли бой
        return_btn = game_frame.locator("input[value='Вернуться']")
        if return_btn.count() > 0 and return_btn.is_visible():
            return_btn.click()
            print("fight is over")
            time.sleep(0.5)
            break

        # Если бой не закончен, пробуем нажать "Авто" (если доступна)
        auto_btn = game_frame.locator("input[value='Авто']")
        if auto_btn.count() > 0 and auto_btn.is_visible() and auto_btn.is_enabled():
            auto_btn.click()
            print("Auto")
            time.sleep(0.3)
        else:
            # Если "Авто" недоступна, просто ждём и повторяем проверку
            time.sleep(0.3)

    move(1)

    # Сбор предметов с пола
    while True:
        items = game_frame.locator('.items a')
        if items.count() == 0:
            break
        items.first.click()
        print('item collected')
        time.sleep(0.3)

    time.sleep(0.3)

    move(1)

    while True:
        items = game_frame.locator('.items a')
        if items.count() == 0:
            break
        items.first.click()
        print('item collected')
        time.sleep(0.3)  # пауза для исчезновения предмета

    time.sleep(0.3)

def loot():
    turn('l')
    time.sleep(0.3)
    chest = game_frame.locator('div.item img[onclick*="sunduk"]')
    if chest.count() > 0 and chest.is_visible():
        chest.click()
        print('chest')
    else:
        print('Сундука нет')
    time.sleep(0.5)
    turn('r')

def heal():
    ...

def finish():
    try:
        def handle_dialog(dialog):
            dialog.accept()
        page.on("dialog", handle_dialog)
        link = game_frame.locator("a.exit-link[href*='cexit']")
        link.scroll_into_view_if_needed()
        link.click(force=True)
        time.sleep(0.5)
        page.remove_listener("dialog", handle_dialog)
    except Exception as e:
        print(f"Ошибка в finish: {e}")

time.sleep(10)
print("Ctrl+C in bash to close.")

try:
    wait_for_loading()
    while True:
        while True:
            try:
                game_frame = page.frame_locator("[name='theframe']")
                create_group_btn = game_frame.locator("input[value='Создать группу']")
                if create_group_btn.count() > 0 and create_group_btn.is_visible():
                    create_group_btn.click()
                    break
                else:
                    refresh_btn = page.locator("#header-refresh-btn")
                    refresh_btn.click()
                time.sleep(1)
            except Exception as e:
                print('retrying...')
                time.sleep(1)

        time.sleep(1)
        game_frame.locator("input[name='start']").click()
        time.sleep(1)

        for _ in range(3):
            for __ in range(3):
                fight()
                loot()
                move(2)
            turn('l')

        for __ in range(2):
            fight()
            move(2)
        fight()
        turn('l')
        for __ in range(2):
            move(2)
            fight()
        move(1)
        turn('l')
        for __ in range(2):
            move(1)
            fight()
        move(1)
        turn('l')
        move(1)
        fight()
        move(2)
        fight()
        turn('l')
        move(2)
        fight()

        time.sleep(1)
        finish()

except KeyboardInterrupt:
    print("Killing...")
    browser.close()
    playwright.stop()
except Exception as e:
    print(f"Произошла ошибка: {e}")
    try:
        finish()
    except:
        pass
    print("Завершаем работу...")
    try:
        browser.close()
        playwright.stop()
    except:
        pass