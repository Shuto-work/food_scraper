import requests
from lxml import html
import time
import csv
import logging
import random
from urllib.parse import urljoin
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse


# ログの設定
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# 定数としてXPathを定義
XPATHS = {
    'shop_links': '//*[@id="__next"]//main//article/div[1]/a',
    'shop_name': '//*[@id="info-name"]/text()',
    'shop_number': '//*[@id="info-phone"]/td/ul[1]/li[1]/span[1]/text()',
    'postal_code': '//*[@id="info-table"]/table/tbody/tr[3]/td/p/text()',
    'region': '//*[@id="info-table"]/table/tbody/tr[3]/td/p/span[1]/text()',
    'seats': '//p[@class="commonAccordion_content_item_desc"]/text()',
}


def get_shop_links(page_content, base_url):
    tree = html.fromstring(page_content)
    shop_link_elements = tree.xpath(XPATHS['shop_links'])
    shop_urls = [urljoin(base_url, elem.get('href'))
                 for elem in shop_link_elements]
    return shop_urls


def get_shop_data(shop_url):
    try:
        response = requests.get(shop_url)
        response.raise_for_status()
        response.encoding = response.apparent_encoding
        tree = html.fromstring(response.content)

        # データの抽出
        shop_name = ''.join(tree.xpath(XPATHS['shop_name'])).strip()
        shop_number = ''.join(tree.xpath(XPATHS['shop_number'])).strip()
        postal_code = ''.join(tree.xpath(XPATHS['postal_code'])).strip()
        region = ''.join(tree.xpath(XPATHS['region'])).strip()
        full_address = f"{postal_code} {region}".strip()

        # 座席数を取得
        seats = ''.join(tree.xpath(XPATHS['seats'])).strip()
        if not seats:
            logging.info(f"座席情報が見つかりませんでした。")

        data = {
            '店舗名': shop_name,
            '電話番号': shop_number,
            '住所': full_address,
            'URL': shop_url,
            '座席数': seats
        }
        return data
    except Exception as e:
        logging.error(f"店舗ページの取得中にエラーが発生しました {shop_url}: {e}")
        return None


def main(base_url, start_page, end_page):
    collected_data = []
    session = requests.Session()
    headers = {'User-Agent': 'Mozilla/5.0'}

    start_time = time.time()

    for page_num in range(start_page, end_page + 1):
        # URLを解析
        parsed_url = urlparse(base_url)
        # 既存のクエリパラメータを取得
        query_params = parse_qs(parsed_url.query)
        # 'p'パラメータを追加または更新
        query_params['p'] = [str(page_num)]
        # 新しいクエリ文字列を作成
        new_query = urlencode(query_params, doseq=True)
        # 新しいURLを構築
        page_url = urlunparse(parsed_url._replace(query=new_query))

        logging.info(f"ページ{page_num}を処理しています: {page_url}")

        try:
            response = session.get(page_url, headers=headers)
            response.raise_for_status()
            response.encoding = response.apparent_encoding
            page_content = response.content
            shop_urls = get_shop_links(page_content, base_url)
            logging.info(f"{len(shop_urls)} 件の店舗が見つかりました。")

            for shop_url in shop_urls:
                shop_data = get_shop_data(shop_url)
                if shop_data:
                    collected_data.append(shop_data)
                time.sleep(random.uniform(1, 10))  # 店舗間のリクエスト間隔を設定

        except Exception as e:
            logging.error(f"ページの処理中にエラーが発生しました {page_url}: {e}")
        time.sleep(random.uniform(3, 10))  # ページ間のリクエスト間隔を設定

    # CSVへの書き込み
    fieldnames = ['店舗名', '電話番号', '住所', 'URL', '座席数']
    with open('shop_data.csv', 'w', newline='', encoding='utf-8-sig') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for data in collected_data:
            writer.writerow(data)
    logging.info("データの収集が完了しました。'shop_data.csv' に保存されました。")

    end_time = time.time()
    diff_time = end_time - start_time
    logging.info(f"処理にかかった時間：{diff_time}秒")


if __name__ == "__main__":
    base_url = input("ベースURLを入力してください: ").strip()
    start_page = int(input("開始ページ番号を入力してください: ").strip())
    end_page = int(input("終了ページ番号を入力してください: ").strip())
    main(base_url, start_page, end_page)
