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

        # # 住所
        # address_xpath = '//p[@class="rstinfo-table__address"]'
        # address = WebDriverWait(driver, 10).until(
        #     EC.presence_of_element_located((By.XPATH, address_xpath))
        # ).text
        # print(f"住所を取得しました: {address_xpath}")

        # 営業時間
        open_time_xpath = '//*[@id="rst-data-head"]/table[1]/tbody/tr[7]/td/ul/li/ul/li'
        open_time = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, open_time_xpath))
        ).text
        print(f"営業時間を取得しました: {open_time_xpath}")

        # 座席
        seat_count_xpath = '//*[@id="rst-data-head"]/table[2]/tbody/tr[1]/td/p'
        seat_count = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, seat_count_xpath))
        ).text
        print(f"営業時間を取得しました: {seat_count_xpath}")

        # 最大予約可能人数
        max_reserve_xpath = '//*[@id="rst-data-head"]/table[2]/tbody/tr[2]/td/p'
        max_reserve = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, max_reserve_xpath))
        ).text
        print(f"最大予約可能人数を取得しました: {max_reserve_xpath}")

        # ホームページ
        Website_xpath = '//*[@id="rst-data-head"]/table[4]/tbody/tr[4]/td/p/a/span/text()'
        website = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, Website_xpath))
        ).text
        print(f"ホームページを取得しました: {website}")

        # 公式アカウント
        official_account_xpath = '//*[@id="rst-data-head"]/table[4]/tbody/tr[5]/td/div/a/span'
        official_account = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, official_account_xpath))
        ).text
        print(f"公式アカウントを取得しました: {official_account}")

        # オープン日
        open_day_xpath = '//*[@id="rst-data-head"]/table[4]/tbody/tr[6]/td/p'
        open_day = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, open_day_xpath))
        ).text
        print(f"公式アカウントを取得しました: {open_day}")

        # 電話番号
        phone_number_xpath = '//*[@id="rst-data-head"]/table[4]/tbody/tr[7]/td/p/strong'
        phone_number = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, phone_number_xpath))
        ).text
        print(f"公式アカウントを取得しました: {phone_number}")

        return {
            "店舗名": store_name,
            "ジャンル": genre,
            "予約・お問い合わせ": reserve_num,
            # "住所": address,
            "営業時間": open_time,
            "座席": seat_count,
            "最大予約可能人数": max_reserve,
            "ホームページ": website,
            "公式アカウント": official_account,
            "オープン日": open_day,
            "電話番号": phone_number
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
                                "店舗名", "ジャンル", "予約・お問い合わせ", "営業時間", "座席", "最大予約可能人数", "ホームページ", "公式アカウント", "オープン日", "電話番号"])
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
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.common.exceptions import TimeoutException, NoSuchElementException
# from selenium.webdriver.common.action_chains import ActionChains
# import csv


# def setup_driver():
#     options = Options()
#     # options.add_argument('--headless')  # デバッグ中はコメントアウト
#     options.add_argument('--no-sandbox')
#     options.add_argument('--disable-dev-shm-usage')
#     options.add_argument(
#         'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36')
#     return webdriver.Chrome(options=options)


# def wait_for_page_load(driver, timeout=30):
#     try:
#         WebDriverWait(driver, timeout).until(
#             lambda d: d.execute_script(
#                 'return document.readyState') == 'complete'
#         )
#     except TimeoutException:
#         print(f"ページの読み込みに{timeout}秒以上かかりました。")


# def get_restaurant_info(url):
#     driver = setup_driver()
#     try:
#         # ... [前述のコードは同じ] ...

#         # 店舗情報の取得
#         info = {}
#         items = {
#             "店名": '//*[@id="rst-data-head"]/table[1]/tbody/tr[1]/td/div/span',
#             "ジャンル": '//*[@id="rst-data-head"]/table[1]/tbody/tr[2]/td/span',
#             "予約・お問い合わせ": '//*[@id="rst-data-head"]/table[1]/tbody/tr[3]/td/p/strong',
#             "住所": '//p[@class="rstinfo-table__address"]',
#             "営業時間": '//*[@id="rst-data-head"]/table[1]/tbody/tr[7]/td/ul/li/ul/li',
#             "席数": '//*[@id="rst-data-head"]/table[2]/tbody/tr[1]/td/p',
#             "最大予約可能人数": '//*[@id="rst-data-head"]/table[2]/tbody/tr[2]/td/p',
#             "ホームページ": '//*[@id="rst-data-head"]/table[4]/tbody/tr[4]/td/p/a/span',
#             "公式アカウント": '//*[@id="rst-data-head"]/table[4]/tbody/tr[5]/td/div/a/span',
#             "オープン日": '//*[@id="rst-data-head"]/table[4]/tbody/tr[6]/td/p',
#             "電話番号": '//*[@id="rst-data-head"]/table[4]/tbody/tr[7]/td/p/strong'
#         }

#         for key, xpath in items.items():
#             try:
#                 element = WebDriverWait(driver, 10).until(
#                     EC.presence_of_element_located((By.XPATH, xpath))
#                 )
#                 info[key] = element.text
#                 print(f"{key}を取得しました: {info[key]}")
#             except Exception as e:
#                 print(f"{key}の取得に失敗しました: {e}")
#                 info[key] = "N/A"

#         return info

#     except TimeoutException as e:
#         print(f"タイムアウトが発生しました: {e}")
#         print(f"現在のURL: {driver.current_url}")
#     except NoSuchElementException as e:
#         print(f"要素が見つかりません: {e}")
#     except Exception as e:
#         print(f"予期せぬエラーが発生しました: {e}")
#     finally:
#         driver.save_screenshot("final_state_screenshot.png")
#         print("最終状態のスクリーンショットを保存しました。")
#         driver.quit()

#     return None


# def save_to_csv(data, filename="restaurant-info.csv"):
#     with open(filename, 'w', newline='', encoding='utf-8') as file:
#         writer = csv.DictWriter(file, fieldnames=data.keys())
#         writer.writeheader()
#         writer.writerow(data)
#     print(f"CSVデータを{filename}に保存しました")


# def main():
#     url = 'https://tabelog.com/osaka/C27100/rstLst/yakiniku/?vs=1&sa=%E5%A4%A7%E9%98%AA%E5%B8%82&sk=%25E7%2584%25BC%25E8%2582%2589&lid=top_navi1&svd=20240912&svt=1900&svps=2&hfc=1&cat_sk=%E7%84%BC%E8%82%89'
#     info = get_restaurant_info(url)
#     if info:
#         print("店舗情報:")
#         for key, value in info.items():
#             print(f"{key}: {value}")
#         save_to_csv(info)
#     else:
#         print("店舗情報の取得に失敗しました。")


# if __name__ == "__main__":
#     main()
