import unittest
from unittest.mock import patch, MagicMock
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time
import csv
import json

# モック対象の関数をインポートしてテストする
from scraper import setup_driver, wait_for_page_load, get_store_urls, get_restaurant_info, save_to_csv, save_to_json


class TestWebScrapingFunctions(unittest.TestCase):

    @patch('selenium.webdriver.Chrome')
    def test_setup_driver(self, MockWebDriver):
        # 本物のOptionsオブジェクトを使用してセットアップ
        mock_options = MagicMock(spec=Options)
        MockWebDriver.return_value = MagicMock()

        driver = setup_driver()

        # Chromeの呼び出しに渡されたoptionsオブジェクトを確認
        MockWebDriver.assert_called_once_with(options=mock_options)
        self.assertIsInstance(driver, MagicMock)

    @patch('selenium.webdriver.support.ui.WebDriverWait')
    def test_wait_for_page_load(self, MockWebDriverWait):
        mock_driver = MagicMock()

        # execute_scriptのモックを作成
        mock_driver.execute_script.return_value = 'complete'

        # WebDriverWaitのモックが呼ばれるか確認
        wait_for_page_load(mock_driver)

        MockWebDriverWait.assert_called_once()

    @patch('selenium.webdriver.support.ui.WebDriverWait')
    def test_get_store_urls(self, MockWebDriverWait):
        # get_store_urls関数が店舗URLを正しく取得するかをテスト
        mock_driver = MagicMock()
        mock_element = MagicMock()
        mock_element.get_attribute.return_value = "http://example.com/store1"
        mock_driver.find_elements.return_value = [mock_element]

        store_urls = get_store_urls(mock_driver)
        self.assertEqual(store_urls, ["http://example.com/store1"])

    @patch('selenium.webdriver.support.ui.WebDriverWait')
    def test_get_restaurant_info(self, MockWebDriverWait):
        # get_restaurant_info関数が店舗情報を正しく取得するかをテスト
        mock_driver = MagicMock()
        mock_driver.get.return_value = None
        mock_driver.find_element.return_value.text = "テスト店舗"
        mock_driver.find_elements.return_value = ["テスト店舗"]

        url = "http://example.com/store1"
        info = get_restaurant_info(mock_driver, url)
        self.assertIsNotNone(info)
        self.assertEqual(info['店舗名'], "テスト店舗")

    @patch('builtins.open', new_callable=MagicMock)
    def test_save_to_csv(self, mock_open):
        # save_to_csv関数がCSVファイルに正しく保存するかをテスト
        mock_data = [
            {"店舗URL": "http://example.com", "店舗名": "テスト店舗",
                "予約・お問い合わせ": "012-345-6789", "住所": "テスト住所", "電話番号": "012-345-6789"}
        ]
        save_to_csv(mock_data)
        mock_open.assert_called_once_with(
            'restaurant-info.csv', 'w', newline='', encoding='utf-8')

    @patch('builtins.open', new_callable=MagicMock)
    def test_save_to_json(self, mock_open):
        # save_to_json関数がJSONファイルに正しく保存するかをテスト
        mock_data = [
            {"店舗URL": "http://example.com", "店舗名": "テスト店舗",
                "予約・お問い合わせ": "012-345-6789", "住所": "テスト住所", "電話番号": "012-345-6789"}
        ]
        save_to_json(mock_data)
        mock_open.assert_called_once_with(
            'restaurant-info.json', 'w', encoding='utf-8')


if __name__ == '__main__':
    unittest.main()
