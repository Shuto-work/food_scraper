import streamlit as st
import json
import sys
import subprocess

st.write("Hello world")

st.divider()  # 👈 Another horizontal rule

with st.form(key="url_form"):
    max_search_page = st.number_input(
        "データ取得ページ数", step=1, value=1, min_value=1,)
    output_csv = st.text_input("出力するCSVファイル名", "食べログ飲食店リスト.csv")
    action_btn = st.form_submit_button("実行")

    if action_btn:
        st.subheader('スクレイピング実行中です...')
        st.text(f'検索URL：「{url}」')
        st.text(f'データ取得ページ数：「{max_search_page}」')
        st.text(f'出力CSVファイル名：「{output_csv}」')

    params = {
        "url": url,
        "max_search_page": max_search_page,
        "output_csv": output_csv
    }
    with open('params.json', 'w') as f:
        json.dump(params, f)

        # Pythonのフルパスを取得
        python_path = sys.executable

        # subprocess.runを使ってスクリプトを実行。Python実行環境を明示的に指定。
        result = subprocess.run([python_path, 'scraper.py'],
                                capture_output=True,
                                text=True
                                )

        # CSVデータの準備
        if result.returncode == 0:
            csv_data = result.stdout
            st.session_state.csv_data = csv_data
            st.session_state.csv_file_name = output_csv
            st.success('実行完了')
        else:
            st.error('エラーが発生しました: ' + result.stderr)
