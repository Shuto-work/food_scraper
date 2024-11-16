from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from lxml import html
import requests
import re

# 取得対象のURL
url = "https://r.gnavi.co.jp/ca04h42e0000/"

try:
    # HTTPリクエストを送信
    response = requests.get(url)
    response.raise_for_status()  # ステータスコードを確認

    # エンコーディングを修正
    response.encoding = response.apparent_encoding  # サーバーのエンコーディングに自動で合わせる

    # # HTMLを解析
    tree = html.fromstring(response.content)

    # 郵便番号と住所を取得して結合
    postal_code = tree.xpath(
        '//*[@id="info-table"]/table/tbody/tr[3]/td/p/text()')
    region = tree.xpath(
        '//*[@id="info-table"]/table/tbody/tr[3]/td/p/span[1]/text()')
    full_address = f"{''.join(postal_code).strip()} {''.join(region).strip()}"

    # 取得対象の要素を辞書にまとめる
    target_elements = {
        "shop_name": tree.xpath('//*[@id="info-name"]/text()'),
        "shop_number": tree.xpath('//*[@id="info-phone"]/td/ul[1]/li[1]/span[1]/text()'),
        "shop_address": [full_address],
        "seats": tree.xpath('//p[@class="commonAccordion_content_item_desc"]')
    }

    # 要素が正しいか確認
    for key, target in target_elements.items():
        if target:
            print("要素が見つかりました:")
            cleaned_text = re.sub(r'\s+', ' ', ' '.join(target).strip())
            print(cleaned_text)
        else:
            print("指定した要素が見つかりませんでした。セレクタを確認してください。")

except requests.exceptions.RequestException as e:
    print(f"リクエストエラー: {e}")
