from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Chromeドライバーの設定
options = webdriver.ChromeOptions()
# options.add_argument('--headless')  # ヘッドレスモードを使用する場合

# デバイスドライバーの起動
driver = webdriver.Chrome(options=options)

# 検索結果ページにアクセス
search_url = 'https://tabelog.com/osaka/C27100/rstLst/yakiniku/?vs=1&sa=%E5%A4%A7%E9%98%AA%E5%B8%82&sk=%25E7%2584%25BC%25E8%2582%2589&lid=top_navi1&svd=20240912&svt=1900&svps=2&hfc=1&cat_sk=%E7%84%BC%E8%82%89'
# search_url = 'https://tabelog.com/osaka/A2701/A270108/27130478/'
driver.get(search_url)

try:
    # 最初の店舗タイトルをクリックするまで待つ
    first_store = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, '.list-rst__rst-name-target'))
    )
    first_store.click()

    # ページが完全に読み込まれるまで待つ
    time.sleep(5)  # 5秒待機

    # print(driver.page_source)

    # 店舗ページでデータを取得
    try:
        # 店名の取得
        # store_name = driver.find_element(
        #     By.XPATH, "//div[@class='rstinfo-table__name-wrap']/span").text
        # store_name = driver.find_element(
        #     By.CSS_SELECTOR, '.rstinfo-table__name-wrap span').text

        store_name = driver.find_element(
            By.CSS_SELECTOR, ".rstinfo-table__name-wrap > span").text
        print(f"店名: {store_name}")
    except Exception as e:
        print(f"店名の取得エラー: {e}")

    try:
        # ジャンルの取得
        # genre = driver.find_element(
        #     By.XPATH, "//tr[th[contains(text(),'ジャンル')]]/td/span").text
        # 例: `ジャンル` を含む `tr` を見つけ、その `td` の中の `span` を選択
        # genre = driver.find_element(
        #     By.XPATH, "//tr[th[text()='ジャンル']]/td/span").text
        genre = driver.find_element(
            By.CSS_SELECTOR, "tr th:contains('ジャンル') + td > span").text

        print(f"ジャンル: {genre}")
    except Exception as e:
        print(f"ジャンルの取得エラー: {e}")

finally:
    # ドライバーを終了
    driver.quit()


# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# import time

# # Chromeドライバーのパスを指定
# options = webdriver.ChromeOptions()
# # options.add_argument('--headless')  # ヘッドレスモードを使用する場合

# #デバイスドライバーの起動
# driver = webdriver.Chrome(options=options)

# # 検索結果ページにアクセス
# search_url = 'https://tabelog.com/osaka/C27100/rstLst/yakiniku/?vs=1&sa=%E5%A4%A7%E9%98%AA%E5%B8%82&sk=%25E7%2584%25BC%25E8%2582%2589&lid=top_navi1&svd=20240912&svt=1900&svps=2&hfc=1&cat_sk=%E7%84%BC%E8%82%89'

# driver.get(search_url)


# # 最初の店舗タイトルをクリックするまで待つ
# try:
#     first_store = WebDriverWait(driver, 10).until(
#         EC.presence_of_element_located(
#             (By.CSS_SELECTOR, '.list-rst__rst-name-target'))
#     )
#     first_store.click()

#     # 店舗ページが開くまで待機（10秒）
#     time.sleep(10)  # ページの読み込み時間を調整

#     # 店舗ページでデータを取得
#     try:
#         # 店名の取得
#         store_name = driver.find_element(
#             By.CSS_SELECTOR, '.rstinfo-table__name-wrap span').text
#         print(f"店名: {store_name}")
#     except Exception as e:
#         print("店名の取得エラー:", e)

#     try:
#         # ジャンルの取得
#         genre = driver.find_element(
#             By.XPATH, "//tr[th[contains(text(),'ジャンル')]]/td/span").text
#         print(f"ジャンル: {genre}")
#     except Exception as e:
#         print("ジャンルの取得エラー:", e)

# finally:
#     # ドライバーを終了
#     driver.quit()
