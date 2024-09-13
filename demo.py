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
        try:
            store_name_xpath = '//*[@id="rst-data-head"]/table[1]/tbody/tr[1]/td/div/span'
            store_name = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, store_name_xpath))
            ).text
            print(f"店舗名を取得しました: {store_name}")
        except (NoSuchElementException, TimeoutException) as e:
            store_name = None
            print(f"店舗名が見つかりませんでした: {e}")
        
        # ジャンルの取得
        try:
            genre_xpath = '//*[@id="rst-data-head"]/table[1]/tbody/tr[2]/td/span'
            genre = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, genre_xpath))
            ).text
            print(f"ジャンルを取得しました: {genre}")
        except (NoSuchElementException, TimeoutException) as e:
            genre = None
            print(f"ジャンルが見つかりませんでした: {e}")
        
        # 予約・お問い合わせの取得
        try:
            reserve_num_xpath = '//*[@id="rst-data-head"]/table[1]/tbody/tr[3]/td/p/strong'
            reserve_num = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, reserve_num_xpath))
            ).text
            print(f"予約・お問い合わせを取得しました: {reserve_num}")
        except (NoSuchElementException, TimeoutException) as e:
            reserve_num = None
            print(f"予約・お問い合わせが見つかりませんでした: {e}")
        
        # 住所
        try:
            address_xpath = '//p[@class="rstinfo-table__address"]'
            address = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, address_xpath))
            ).text.strip()
            print(f"住所を取得しました: {address}")
        except (NoSuchElementException, TimeoutException) as e:
            address = None
            print(f"住所が見つかりませんでした: {e}")
        
        # 営業時間
        try:
            open_time_xpath = '//*[@id="rst-data-head"]/table[1]/tbody/tr[7]/td/ul/li/ul/li'
            open_time = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, open_time_xpath))
            ).text
            print(f"営業時間を取得しました: {open_time}")
        except (NoSuchElementException, TimeoutException) as e:
            open_time = None
            print(f"営業時間が見つかりませんでした: {e}")

        # 座席
        try:
            seat_count_xpath = '//*[@id="rst-data-head"]/table[2]/tbody/tr[1]/td/p'
            seat_count = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, seat_count_xpath))
            ).text
            print(f"座席数を取得しました: {seat_count}")
        except (NoSuchElementException, TimeoutException) as e:
            seat_count = None
            print(f"座席数が見つかりませんでした: {e}")
            
        # 最大予約可能人数
        try:
            max_reserve_xpath = '//*[@id="rst-data-head"]/table[2]/tbody/tr[2]/td/p'
            max_reserve = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, max_reserve_xpath))
            ).text
        except Exception as e:
            max_reserve = None
            print(f"最大予約可能人数を取得しました: {max_reserve_xpath}")
        
        # ホームページ
        try:
            website_xpath = "//th[contains(text(), 'ホームページ')]/following-sibling::td//a"
            website_element = driver.find_element(By.XPATH, website_xpath)
            website_fullURL = website_element.get_attribute('href')
            print(f"ホームページを取得しました: {website_fullURL}")
        except NoSuchElementException:
            website_fullURL = None
            print("ホームページが見つかりませんでした。")

        # 公式アカウント
        try:
            # official_account_xpath = "//th[contains(text(), '公式アカウント')]/following-sibling::td//a/span"
            official_account_xpath = '//a[contains(@class, "rstinfo-sns-link") and contains(@class, "rstinfo-sns-twitter")]'

            official_account_element = driver.find_element(
                By.XPATH, official_account_xpath)
            official_account = official_account_element.get_attribute('href')
            print(f"公式アカウントを取得しました: {official_account}")
        except NoSuchElementException:
            official_account = None
            print("公式アカウントが見つかりませんでした。")

        # オープン日
        try:
            open_day_xpath = "//th[contains(text(), 'オープン日')]/following-sibling::td/p"
            open_day = driver.find_element(By.XPATH, open_day_xpath).text
            print(f"オープン日を取得しました: {open_day}")
        except NoSuchElementException:
            open_day = None
            print("オープン日が見つかりませんでした。")

        # 電話番号
        try:
            phone_number_xpath = "//th[contains(text(), '電話番号')]/following-sibling::td/p/strong"
            phone_number = driver.find_element(
                By.XPATH, phone_number_xpath).text
            print(f"電話番号を取得しました: {phone_number}")
        except NoSuchElementException:
            phone_number = None
            print("電話番号が見つかりませんでした。")

        return {
            "店舗名": store_name,
            "ジャンル": genre,
            "予約・お問い合わせ": reserve_num,
            "住所": address,
            "営業時間": open_time,
            "座席": seat_count,
            "最大予約可能人数": max_reserve,
            "ホームページ": website_fullURL,
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
                                "店舗名", "ジャンル", "予約・お問い合わせ","住所", "営業時間", "座席", "最大予約可能人数", "ホームページ", "公式アカウント", "オープン日", "電話番号"])
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