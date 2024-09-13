from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
import csv


def setup_driver():
    options = Options()
    # options.add_argument('--headless')  # デバッグ中はコメントアウト
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument(
        'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36')
    return webdriver.Chrome(options=options)


def wait_for_page_load(driver, timeout=30):
    try:
        WebDriverWait(driver, timeout).until(
            lambda d: d.execute_script(
                'return document.readyState') == 'complete'
        )
    except TimeoutException:
        print(f"ページの読み込みに{timeout}秒以上かかりました。")


def get_restaurant_info(url):
    driver = setup_driver()
    try:
        # 検索結果ページにアクセス
        driver.get(url)
        wait_for_page_load(driver)
        print("検索結果ページにアクセスしました。")

        # 最初の店舗リンクを見つける
        first_store = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, 'a.list-rst__rst-name-target'))
        )
        print("最初の店舗リンクを見つけました。")

        # リンクのURLを取得
        store_url = first_store.get_attribute('href')
        print(f"店舗ページのURL: {store_url}")

        # 新しいタブで店舗ページを開く
        driver.execute_script(f"window.open('{store_url}', '_blank');")
        driver.switch_to.window(driver.window_handles[-1])
        wait_for_page_load(driver)
        print("店舗ページを新しいタブで開きました。")

        # 店舗ページの要素が読み込まれるまで待機
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.ID, 'rst-data-head'))
        )
        print("店舗ページの主要要素が読み込まれました。")

        # 店舗名の取得
        store_name_xpath = '//*[@id="rst-data-head"]/table[1]/tbody/tr[1]/td/div/span'
        store_name = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, store_name_xpath))
        ).text
        print(f"店舗名を取得しました: {store_name}")

        # ジャンルの取得
        genre_xpath = '//*[@id="rst-data-head"]/table[1]/tbody/tr[2]/td/span'
        genre = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, genre_xpath))
        ).text
        print(f"ジャンルを取得しました: {genre}")

        # 予約・お問い合わせの取得
        reserve_num_xpath = '//*[@id="rst-data-head"]/table[1]/tbody/tr[3]/td/p/strong'
        reserve_num = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, reserve_num_xpath))
        ).text
        print(f"予約・お問い合わせを取得しました: {reserve_num}")

        return {
            "店舗名": store_name,
            "ジャンル": genre,
            "予約・お問い合わせ": reserve_num
        }

    except TimeoutException as e:
        print(f"タイムアウトが発生しました: {e}")
        print(f"現在のURL: {driver.current_url}")
    except NoSuchElementException as e:
        print(f"要素が見つかりません: {e}")
    except Exception as e:
        print(f"予期せぬエラーが発生しました: {e}")
    finally:
        driver.save_screenshot("final_state_screenshot.png")
        print("最終状態のスクリーンショットを保存しました。")
        driver.quit()

    return None


def save_to_csv(data, filename="restaurant-info.csv"):
    with open(filename, 'w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=[
                                "店舗名", "ジャンル", "予約・お問い合わせ"])
        writer.writeheader()
        writer.writerow(data)
    print(f"csvデータを{filename}に保存しました")


def main():
    url = 'https://tabelog.com/osaka/C27100/rstLst/yakiniku/?vs=1&sa=%E5%A4%A7%E9%98%AA%E5%B8%82&sk=%25E7%2584%25BC%25E8%2582%2589&lid=top_navi1&svd=20240912&svt=1900&svps=2&hfc=1&cat_sk=%E7%84%BC%E8%82%89'
    info = get_restaurant_info(url)
    if info:
        print("店舗情報:")
        for key, value in info.items():
            print(f"{key}: {value}")
        save_to_csv(info)
    else:
        print("店舗情報の取得に失敗しました。")


if __name__ == "__main__":
    main()

# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.chrome.service import Service
# from webdriver_manager.chrome import ChromeDriverManager
# from bs4 import BeautifulSoup
# import json
# import time

# # 設定
# search_url = 'https://tabelog.com/'
# search_query = '大阪 焼肉'
# driver_path = ChromeDriverManager().install()

# # Seleniumでブラウザを開く
# driver = webdriver.Chrome(service=Service(driver_path))
# driver.get(search_url)

# # ログイン
# # 以下はログインのための仮の手順です。実際のログイン要素に合わせて修正する必要があります。
# # login_button = driver.find_element(By.CSS_SELECTOR, 'button.login')
# # login_button.click()

# # 検索
# area_input = driver.find_element(By.ID, 'area-input')
# genre_input = driver.find_element(By.ID, 'genre-input')
# search_button = driver.find_element(By.ID, 'search-button')

# area_input.send_keys('大阪')
# genre_input.send_keys('焼肉')
# search_button.click()

# time.sleep(5)  # ページの読み込みを待つ

# # 検索結果ページの解析
# soup = BeautifulSoup(driver.page_source, 'html.parser')
# restaurant_links = soup.select('a.restaurant-title')  # 仮のセレクタ、実際のセレクタに合わせて修正

# restaurant_urls = [link['href'] for link in restaurant_links]

# # 店舗TOPページからデータを取得
# restaurant_data = []

# for url in restaurant_urls:
#     driver.get(url)
#     time.sleep(5)  # ページの読み込みを待つ

#     soup = BeautifulSoup(driver.page_source, 'html.parser')
#     table = soup.find(
#         'table', {'class': 'c-table c-table--form rstinfo-table__table'})

#     if table:
#         data = {}
#         for row in table.find_all('tr'):
#             th = row.find('th').get_text(strip=True)
#             td = row.find('td').get_text(strip=True)
#             data[th] = td

#         restaurant_data.append(data)

# # 結果をJSONファイルに保存
# with open('restaurant_data.json', 'w', encoding='utf-8') as f:
#     json.dump(restaurant_data, f, ensure_ascii=False, indent=4)

# driver.quit()
