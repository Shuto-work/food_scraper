from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Chromeドライバーのパスを指定
options = webdriver.ChromeOptions()

#デバイスドライバーの起動
driver = webdriver.Chrome(options=options)

# 検索結果ページにアクセス
search_url = 'https://tabelog.com/osaka/C27100/rstLst/yakiniku/?vs=1&sa=%E5%A4%A7%E9%98%AA%E5%B8%82&sk=%25E7%2584%25BC%25E8%2582%2589&lid=top_navi1&svd=20240912&svt=1900&svps=2&hfc=1&cat_sk=%E7%84%BC%E8%82%89'
driver.get(search_url)

print(search_url)
# 最初の店舗タイトルをクリックするまで待つ
try:
    first_store = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, '.list-rst__rst-name a'))
    )
    first_store.click()

    # 店舗ページが開くまで10秒待つ
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '.display-name'))
    )

    # 店舗ページでデータを取得
    # 店名の取得
    store_name = driver.find_element(By.CSS_SELECTOR, '.display-name').text

    # ジャンルの取得
    genre = driver.find_element(
        By.CSS_SELECTOR, '.rstinfo-table__genre span').text

    print(f"店名: {store_name}")
    print(f"ジャンル: {genre}")

finally:
    # ドライバーを終了
    driver.quit()