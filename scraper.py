from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import json
import time

# 設定
search_url = 'https://tabelog.com/'
search_query = '大阪 焼肉'
driver_path = ChromeDriverManager().install()

# Seleniumでブラウザを開く
driver = webdriver.Chrome(service=Service(driver_path))
driver.get(search_url)

# ログイン
# 以下はログインのための仮の手順です。実際のログイン要素に合わせて修正する必要があります。
# login_button = driver.find_element(By.CSS_SELECTOR, 'button.login')
# login_button.click()

# 検索
area_input = driver.find_element(By.ID, 'area-input')
genre_input = driver.find_element(By.ID, 'genre-input')
search_button = driver.find_element(By.ID, 'search-button')

area_input.send_keys('大阪')
genre_input.send_keys('焼肉')
search_button.click()

time.sleep(5)  # ページの読み込みを待つ

# 検索結果ページの解析
soup = BeautifulSoup(driver.page_source, 'html.parser')
restaurant_links = soup.select('a.restaurant-title')  # 仮のセレクタ、実際のセレクタに合わせて修正

restaurant_urls = [link['href'] for link in restaurant_links]

# 店舗TOPページからデータを取得
restaurant_data = []

for url in restaurant_urls:
    driver.get(url)
    time.sleep(5)  # ページの読み込みを待つ

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    table = soup.find(
        'table', {'class': 'c-table c-table--form rstinfo-table__table'})

    if table:
        data = {}
        for row in table.find_all('tr'):
            th = row.find('th').get_text(strip=True)
            td = row.find('td').get_text(strip=True)
            data[th] = td

        restaurant_data.append(data)

# 結果をJSONファイルに保存
with open('restaurant_data.json', 'w', encoding='utf-8') as f:
    json.dump(restaurant_data, f, ensure_ascii=False, indent=4)

driver.quit()
