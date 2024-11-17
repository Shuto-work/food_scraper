import streamlit as st
import pandas as pd
from scraper_gurunavi import main
import time


st.title("Gurunavi Scraper")

with st.expander("使い方"):
    st.markdown("""
        1. **「ベースURL」を入力**:
           - 検索条件を絞り込んだ後のURLを入力してください。
        2. **「データ取得範囲」を入力**:
           - 開始ページと終了ページを指定します。
        3. **「スクレイピングを実行」ボタンを押す**:
           - スクレイピングを開始します。
        4. **「CSVをダウンロード」ボタンを押す**:
           - 取得したデータをCSV形式でダウンロードできます。
    """)

# 入力フォーム
with st.form(key="scraper_form"):
    base_url = st.text_input("ベースURLを入力してください", placeholder="")
    start_page = st.number_input("開始ページ番号", min_value=1, value=1, step=1)
    end_page = st.number_input("終了ページ番号", min_value=1, value=1, step=1)
    output_csv = st.text_input(
        "出力CSVファイル名", "shop_info.csv")
    submit_button = st.form_submit_button("スクレイピングを実行")

if submit_button:
    start_time = time.time()
    st.write("スクレイピングを開始します...")
    st.text(f"URL: {base_url}")
    st.text(f"取得範囲: {start_page}ページ目から{end_page}ページ目")

    # スクレイピング関数を呼び出す
    with st.spinner("データを収集しています..."):
        collected_data = main(base_url, start_page, end_page)

    if collected_data:
        end_time = time.time()
        diff_time = end_time - start_time
        st.success(f"処理にかかった時間：{diff_time}秒")
        st.success("スクレイピングが完了しました。結果をダウンロードしてください。")

        # データフレームに変換
        df = pd.DataFrame(collected_data)

        # CSVをバイトストリームに変換
        csv = df.to_csv(index=False).encode('utf-8-sig')

        # ダウンロードボタンを表示
        st.download_button(
            label="CSVをダウンロード",
            data=csv,
            file_name=output_csv,
            mime='text/csv'
        )
    else:
        st.error("データの取得に失敗しました。")
