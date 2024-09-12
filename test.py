# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.chrome.service import Service
# from webdriver_manager.chrome import ChromeDriverManager

# # 手動でパスを指定する場合
# driver_path = "/usr/local/bin/chromedriver"  # ChromeDriverのパス
# # service = Service(driver_path)

# # WebDriverのセットアップ
# driver = webdriver.Chrome(service=service)
# or
# driver = webdriver.Chrome()

# # # 任意のウェブサイトにアクセス
# driver.get('https://tabelog.com')

# element = driver.find_element(By.ID, "sa")
# placeholder = element.get_attribute("placeholder")
# print(placeholder)

# # # 必要な操作を行う

# # ブラウザを閉じる
# driver.quit()

#  ーーーーー  test_page_load_strategy_eager() ーーーーーーーー
from selenium import webdriver
from selenium.webdriver.common.by import By


def test_page_load_strategy_eager():
    options = webdriver.ChromeOptions()

    options.page_load_strategy = 'eager'
    driver = webdriver.Chrome(options=options)

    driver.get("https://tabelog.com")

    element = driver.find_element(By.ID, "sa")
    placeholder = element.get_attribute("placeholder")
    print(placeholder)

    driver.quit()

test_page_load_strategy_eager()