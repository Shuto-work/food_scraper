from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import re

# Seleniumのオプション設定
options = Options()
options.add_argument("--headless")  # ヘッドレスモード（ブラウザを非表示）

# ChromeDriverの設定
driver = webdriver.Chrome(options=options)

# 取得対象のURL
url = "https://r.gnavi.co.jp/ca04h42e0000/"

try:
    # ページを開く
    driver.get(url)

    # 店名を取得
    shop_name = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="info-name"]'))
    ).text.strip()

    # 電話番号を取得
    shop_number = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.XPATH, '//*[@id="info-phone"]/td/ul[1]/li[1]/span[1]'))
    ).text.strip()

    # 住所（郵便番号＋住所）を取得
    postal_code = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.XPATH, '//*[@id="info-table"]/table/tbody/tr[3]/td/p'))
    ).text.strip()
    region = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.XPATH, '//*[@id="info-table"]/table/tbody/tr[3]/td/p/span[1]'))
    ).text.strip()
    full_address = f"{postal_code} {region}"

    # 座席数を取得
    seats = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.XPATH, '//p[@class="commonAccordion_content_item_desc"]'))
    ).text.strip()

    # 辞書形式で結果をまとめる
    target_elements = {
        "shop_name": shop_name,
        "shop_number": shop_number,
        "shop_address": full_address,
        "seats": seats
    }

    # 結果を出力
    for key, value in target_elements.items():
        print(f"{key}: {value}")

except TimeoutException:
    print("指定した要素が見つかりませんでした。")
finally:
    # ブラウザを閉じる
    driver.quit()
