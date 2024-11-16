from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import csv
import time
import json


def setup_driver():
    options = Options()
    proxy = "39.162.78.109:8080"  # プロキシIPとポート
    options.add_argument('--headless=new')  # ヘッドレスモード
    options.add_argument(f"--proxy-server=http://{proxy}")  # プロキシを指定
    options.add_argument('--disable-gpu')
    options.add_argument('--disable-software-rasterizer')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--remote-debugging-port=9222')
    options.add_argument(
        'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36'
    )
    return webdriver.Chrome(options=options)


def wait_for_page_load(driver, timeout=150):
    try:
        WebDriverWait(driver, timeout).until(
            lambda d: d.execute_script(
                'return document.readyState') == 'complete'
        )
    except TimeoutException:
        print(f"ページの読み込みに{timeout}秒以上かかりました。")


def get_store_urls(driver):
    try:
        # 店舗リンクを全て取得
        store_elements = WebDriverWait(driver, 30).until(
            EC.presence_of_all_elements_located(
                (By.CSS_SELECTOR, 'a.list-rst__rst-name-target'))
        )
        return [store.get_attribute('href') for store in store_elements]
    except TimeoutException:
        print("店舗一覧の取得にタイムアウトが発生しました")
    return []


def get_restaurant_info(driver, url):
    driver.get(url)
    wait_for_page_load(driver)
    try:
        store_name = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, '//*[@id="rst-data-head"]/table[1]/tbody/tr[1]/td/div/span'))
        ).text
        reserve_num = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, '//*[@id="rst-data-head"]/table[1]/tbody/tr[3]/td/p/strong'))
        ).text
        address = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, '//p[@class="rstinfo-table__address"]'))
        ).text
        phone_number = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//th[contains(text(), '電話番号')]/following-sibling::td/p/strong"))
        ).text

        return {
            "店舗URL": url,
            "店舗名": store_name,
            "予約・お問い合わせ": reserve_num,
            "住所": address,
            "電話番号": phone_number
        }
    except (TimeoutException, NoSuchElementException) as e:
        print(f"情報取得エラー（{url}）：{e}")
    return None


def save_to_csv(data, filename="restaurant-info.csv"):
    with open(filename, 'w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(
            file, fieldnames=["店舗URL", "店舗名", "予約・お問い合わせ", "住所", "電話番号"]
        )
        writer.writeheader()
        for row in data:
            writer.writerow(row)
    print(f"CSVファイルを{filename}に保存しました。")


def save_to_json(data, filename="restaurant-info.json"):
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)
    print(f"JSONファイルを{filename}に保存しました。")


def main():
    # ベースURL。ページ番号部分を`{}`で指定
    # base_url = 'https://tabelog.com/osaka/C27100/rstLst/yakiniku/{}/'

    base_url = 'https://tabelog.com/osaka/C27100/rstLst/RC21/{}/?sk=%E5%B1%85%E9%85%92%E5%B1%8B&svd=20241111&svt=1900&svps=2'
    driver = setup_driver()
    all_data = []
    current_page = 30  # 開始ページ
    end_pages = 30     # 終了ページ

    start_time = time.time()  # 処理開始時刻

    try:
        while current_page <= end_pages:
            # ページ番号を埋め込んでURL生成
            url = base_url.format(current_page)
            print(f"取得中のURL: {url}")
            driver.get(url)
            wait_for_page_load(driver)

            # 現在のページから店舗URLを取得
            store_urls = get_store_urls(driver)
            print(f"{len(store_urls)}店舗のURLを取得しました。")

            for store_url in store_urls:
                info = get_restaurant_info(driver, store_url)
                if info:
                    all_data.append(info)
                    print(f"取得した店舗情報: {info}")

            current_page += 1
            time.sleep(5)  # 過剰負荷防止のための遅延

    finally:
        driver.quit()

    elapsed_time = time.time() - start_time
    print(f"処理にかかった時間: {elapsed_time:.2f}秒")

    # データ保存
    save_to_csv(all_data)
    save_to_json(all_data)


if __name__ == "__main__":
    main()


# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.common.exceptions import TimeoutException, NoSuchElementException
# from urllib.parse import urlparse, urlunparse
# import csv
# import time
# import json


# def setup_driver():
#     options = Options()
#     options.add_argument('--headless=new')  # ヘッドレス。画面表示せずバックグラウンドで実行
#     options.add_argument('--disable-gpu')  # GPU使用しない
#     options.add_argument('--disable-software-rasterizer')  # GPU使用しない
#     options.add_argument('--no-sandbox')  # サンドボックス使用しない
#     options.add_argument('--disable-dev-shm-usage')
#     options.add_argument('--remote-debugging-port=9222')
#     options.add_argument(
#         'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36'
#     )
#     return webdriver.Chrome(options=options)


# def wait_for_page_load(driver, timeout=30):
#     try:
#         WebDriverWait(driver, timeout).until(
#             lambda d: d.execute_script(
#                 'return document.readyState') == 'complete'
#         )
#     except TimeoutException:
#         print(f"ページの読み込みに{timeout}秒以上かかりました。")


# def get_store_urls(driver):
#     store_urls = []
#     try:
#         # 店舗一覧ページの店舗リンクを全て取得
#         store_elements = WebDriverWait(driver, 30).until(
#             EC.presence_of_all_elements_located(
#                 (By.CSS_SELECTOR, 'a.list-rst__rst-name-target'))
#         )
#         store_urls = [store.get_attribute('href') for store in store_elements]
#     except TimeoutException:
#         print("店舗一覧の取得にタイムアウトが発生しました")
#     return store_urls


# def get_restaurant_info(driver, url):
#     driver.get(url)
#     wait_for_page_load(driver)
#     try:
#         # 各要素を個別に待機して取得
#         store_name = WebDriverWait(driver, 10).until(
#             EC.presence_of_element_located(
#                 (By.XPATH, '//*[@id="rst-data-head"]/table[1]/tbody/tr[1]/td/div/span'))
#         ).text
#         reserve_num = WebDriverWait(driver, 10).until(
#             EC.presence_of_element_located(
#                 (By.XPATH, '//*[@id="rst-data-head"]/table[1]/tbody/tr[3]/td/p/strong'))
#         ).text
#         address = WebDriverWait(driver, 10).until(
#             EC.presence_of_element_located(
#                 (By.XPATH, '//p[@class="rstinfo-table__address"]'))
#         ).text
#         phone_number = WebDriverWait(driver, 10).until(
#             EC.presence_of_element_located(
#                 (By.XPATH, "//th[contains(text(), '電話番号')]/following-sibling::td/p/strong"))
#         ).text

#         return {
#             "店舗URL": url,
#             "店舗名": store_name,
#             "予約・お問い合わせ": reserve_num,
#             "住所": address,
#             "電話番号": phone_number
#         }
#     except (TimeoutException, NoSuchElementException) as e:
#         print(f"情報取得エラー（{url}）：{e}")
#     return None


# def modify_url_for_pagination(input_url):
#     parsed_url = urlparse(input_url)
#     path_parts = parsed_url.path.strip('/').split('/')

#     # 数字（ページ番号）を含む部分を探して置き換える
#     new_path_parts = []
#     page_number_found = False
#     for part in path_parts:
#         if part.isdigit():
#             new_path_parts.append('{}')  # ページ番号をプレースホルダーに置き換え
#             page_number_found = True
#         else:
#             new_path_parts.append(part)

#     # ページ番号が見つからない場合、適切な位置に'{}'を挿入
#     if not page_number_found:
#         # 末尾が空でない場合、末尾に挿入
#         if path_parts[-1]:
#             new_path_parts.append('{}')
#         else:
#             new_path_parts.insert(-1, '{}')

#     # 新しいパスを構築
#     new_path = '/' + '/'.join(new_path_parts) + '/'
#     # 新しいURLを生成
#     new_parsed_url = parsed_url._replace(path=new_path)
#     new_url = urlunparse(new_parsed_url)
#     return new_url


# def save_to_csv(data, filename="restaurant-info.csv"):
#     with open(filename, 'w', newline='', encoding='utf-8') as file:
#         writer = csv.DictWriter(
#             file, fieldnames=["店舗URL", "店舗名", "予約・お問い合わせ", "住所", "電話番号"]
#         )
#         writer.writeheader()
#         for row in data:
#             writer.writerow(row)
#     print(f"CSVファイルを{filename}に保存しました。")


# def main():
#     base_url = 'https://tabelog.com/osaka/rstLst/RC1203/5/'
#     driver = setup_driver()
#     all_data = []
#     current_page = 3  # 現在のページ数を初期化
#     end_pages = 1     # 最大取得ページ数を設定

#     start_time = time.time()  # 処理開始時刻を取得

#     try:
#         while current_page <= end_pages:  # ページループ処理
#             url = base_url.format(current_page)
#             driver.get(url)
#             wait_for_page_load(driver)
#             print(f"{current_page}ページ目を処理中...")

#             store_urls = get_store_urls(driver)  # 現在のページのすべての店舗URLを取得
#             for store_url in store_urls:
#                 info = get_restaurant_info(driver, store_url)
#                 if info:
#                     all_data.append(info)
#                     print(f"取得した店舗情報: {info}")

#             current_page += 1  # ページ数をインクリメント

#     finally:
#         driver.quit()

#     end_time = time.time()  # 処理終了時刻を取得
#     elapsed_time = end_time - start_time  # 経過時間を計算

#     print(f"処理にかかった時間: {elapsed_time:.2f}秒")

#     # CSVに保存
#     save_to_csv(all_data)


# if __name__ == "__main__":
#     main()
