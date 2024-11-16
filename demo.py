import json
import csv
import time
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager


def load_params(file_path):
    """JSONファイルを読み込む"""
    try:
        with open(file_path, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"パラメータファイル {file_path} が見つかりませんでした。")
        raise
    except json.JSONDecodeError:
        print(f"パラメータファイル {file_path} の形式が正しくありません。")
        raise


def setup_driver():
    """WebDriverをセットアップ"""
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-gpu")
    options.add_argument('--headless=new')  # ヘッドレスモード
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-software-rasterizer")
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    driver.set_page_load_timeout(300)  # タイムアウトを300秒に増加
    return driver


def wait_for_page_load(driver, timeout=30):
    """ページの読み込みを待機"""
    try:
        WebDriverWait(driver, timeout).until(
            lambda d: d.execute_script(
                "return document.readyState") == "complete"
        )
    except TimeoutException:
        print(f"ページの読み込みに{timeout}秒以上かかりました。")


def get_store_urls(driver):
    """店舗URLを取得"""
    try:
        store_elements = WebDriverWait(driver, 30).until(
            EC.presence_of_all_elements_located(
                (By.CSS_SELECTOR, "a.list-rst__rst-name-target"))
        )
        return [store.get_attribute("href") for store in store_elements]
    except TimeoutException:
        print("店舗一覧の取得にタイムアウトが発生しました")
    return []


def get_restaurant_info(driver, url):
    """店舗情報を取得"""
    driver.get(url)
    wait_for_page_load(driver)
    try:
        store_name = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, '//*[@id="rst-data-head"]/table[1]/tbody/tr[1]/td/div/span'))
        ).text
        return {"店舗URL": url, "店舗名": store_name}
    except Exception as e:
        print(f"エラー: {e}")
    return None


def save_to_csv(data, filename):
    """CSVに保存"""
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["店舗URL", "店舗名"])
        writer.writeheader()
        writer.writerows(data)


def main():
    params = load_params("params.json")
    base_url = params["base_url"]
    start_page = int(params["start_page"])
    end_page = int(params["end_page"])
    output_csv = params["output_csv"]

    driver = setup_driver()
    all_data = []

    try:
        for page in range(start_page, end_page + 1):
            # url = f"{base_url.format(page)}page/{page}/"
            url = base_url.format(start_page)
            print(f"取得url: {url}")
            driver.get(url)
            wait_for_page_load(driver)
            store_urls = get_store_urls(driver)

            for store_url in store_urls:
                info = get_restaurant_info(driver, store_url)
                if info:
                    all_data.append(info)

    finally:
        driver.quit()

    save_to_csv(all_data, output_csv)
    print(f"データを {output_csv} に保存しました。")


if __name__ == "__main__":
    main()


# import csv
# import json
# import os
# import random
# import time
# from urllib.parse import urlparse, urlunparse
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.common.exceptions import TimeoutException, NoSuchElementException


# def setup_driver():
#     options = Options()
#     options.add_argument('--headless=new')  # ヘッドレスモードを有効化
#     options.add_argument('--disable-gpu')
#     options.add_argument('--no-sandbox')
#     options.add_argument('--disable-dev-shm-usage')
#     options.add_argument(
#         'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
#     )
#     driver = webdriver.Chrome(options=options)
#     driver.set_page_load_timeout(60)  # ページ読み込みタイムアウトを60秒に設定
#     return driver


# def wait_for_page_load(driver, timeout=60):
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
#         store_elements = WebDriverWait(driver, 30).until(
#             EC.presence_of_all_elements_located(
#                 (By.CSS_SELECTOR, 'a.list-rst__rst-name-target'))
#         )
#         store_urls = [store.get_attribute('href') for store in store_elements]
#     except TimeoutException:
#         print("店舗一覧の取得にタイムアウトが発生しました")
#     return store_urls


# def get_restaurant_info(driver, url, retries=3):
#     attempt = 0
#     while attempt < retries:
#         try:
#             driver.get(url)
#             wait_for_page_load(driver)
#             break  # ページ読み込み成功
#         except TimeoutException as e:
#             attempt += 1
#             print(f"ページ読み込みタイムアウト（{url}）：再試行します...（{attempt}/{retries}）")
#             if attempt == retries:
#                 print(f"ページ読み込み失敗（{url}）：{e}")
#                 return None
#     try:
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


# def save_to_csv(data, filename="restaurant-info.csv", mode='a'):
#     file_exists = os.path.isfile(filename)
#     with open(filename, mode, newline='', encoding='utf-8') as file:
#         writer = csv.DictWriter(
#             file, fieldnames=["店舗URL", "店舗名", "予約・お問い合わせ", "住所", "電話番号"]
#         )
#         if not file_exists or mode == 'w':
#             writer.writeheader()
#         for row in data:
#             writer.writerow(row)
#     print(f"データをCSVファイル（{filename}）に保存しました。")


# def modify_url_for_pagination(input_url):
#     parsed_url = urlparse(input_url)
#     path_parts = parsed_url.path.strip('/').split('/')

#     # ページ番号を示す部分を探して置き換える
#     new_path_parts = []
#     page_number_found = False
#     for part in path_parts:
#         if part.isdigit():
#             new_path_parts.append('{}')  # ページ番号と仮定
#             page_number_found = True
#         else:
#             new_path_parts.append(part)

#     # ページ番号が見つからない場合、末尾に'{}'を挿入
#     if not page_number_found:
#         new_path_parts.append('{}')

#     # 新しいパスを構築
#     new_path = '/' + '/'.join(new_path_parts) + '/'

#     # 新しいURLを生成
#     new_parsed_url = parsed_url._replace(path=new_path)
#     new_url = urlunparse(new_parsed_url)
#     return new_url


# def extract_start_page(input_url):
#     parsed_url = urlparse(input_url)
#     path_parts = parsed_url.path.strip('/').split('/')

#     for part in path_parts:
#         if part.isdigit():
#             return int(part)
#     # ページ番号が見つからない場合は1を返す
#     return 1


# def save_progress(start_page, filename='progress.json'):
#     with open(filename, 'w') as f:
#         json.dump({'start_page': start_page}, f)


# def load_progress(filename='progress.json'):
#     if os.path.exists(filename):
#         with open(filename, 'r') as f:
#             data = json.load(f)
#             return data.get('start_page', None)
#     return None


# def main():
#     # params.jsonを読み込む
#     with open('params.json', 'r') as f:
#         params = json.load(f)

#     input_url = params['url']
start_page = int(params['start_page'])
#     output_csv_filename = params['output_csv']

#     # ページネーション対応のURLと開始ページ番号を取得
#     base_url = modify_url_for_pagination(input_url)
#     start_page = extract_start_page(input_url)

#     driver = setup_driver()
#     all_data = []
#     resumed_page = load_progress()  # 進行状況の読み込み
#     start_page = resumed_page if resumed_page else start_page  # 開始ページに設定

#     max_retries = 3  # 再試行回数

#     start_time = time.time()  # 処理開始時刻を取得

#     try:
# start_page:  # ページループ処理
#             url = base_url.format(start_page)
#             attempt = 0
#             while attempt < max_retries:
#                 try:
#                     driver.get(url)
#                     wait_for_page_load(driver)
#                     break  # 正常に読み込めたらループを抜ける
#                 except TimeoutException as e:
#                     attempt += 1
#                     print(f"ページ読み込みタイムアウト（{url}）：再試行します...（{
#                           attempt}/{max_retries}）")
#                     if attempt == max_retries:
#                         print(f"ページ読み込み失敗（{url}）：{e}")
#                         break  # 再試行回数を超えたら次のページへ
#             else:
#                 start_page += 1
#                 save_progress(start_page)  # 現在のページ番号を保存
#                 continue  # 次のページへ進む

#             print(f"{start_page}ページ目を処理中...")

#             store_urls = get_store_urls(driver)
#             if not store_urls:
#                 print(f"店舗URLの取得に失敗しました（{url}）")
#                 start_page += 1
#                 save_progress(start_page)  # 現在のページ番号を保存
#                 continue  # 次のページへ

#             for store_url in store_urls:
#                 info = get_restaurant_info(driver, store_url)
#                 if info:
#                     all_data.append(info)
#                     print(f"取得した店舗情報: {info}")

#                     # **取得したデータを逐次的に保存**
#                     save_to_csv([info], filename=output_csv_filename, mode='a')
#                 else:
#                     print(f"店舗情報の取得に失敗しました（{store_url}）")
#                 time.sleep(random.uniform(1, 3))

#             start_page += 1
#             save_progress(start_page)  # 現在のページ番号を保存
#             time.sleep(random.uniform(2, 5))

#     finally:
#         driver.quit()
#         # 処理が正常終了したら進行状況ファイルを削除
#         if os.path.exists('progress.json'):
#             os.remove('progress.json')

#     end_time = time.time()
#     elapsed_time = end_time - start_time
#     print(f"処理にかかった時間: {elapsed_time:.2f}秒")

#     # CSVに保存
#     save_to_csv(all_data, filename=output_csv_filename)

# if __name__ == "__main__":
#     main()
