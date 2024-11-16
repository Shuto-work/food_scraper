import streamlit as st
import json
import sys
import subprocess

st.title("Tabelog Scraper")

with st.expander("使い方"):
    st.markdown("""
        1. **「URL」を入力**:
        - 検索条件を絞り込んだ後のURLを入力。
        2. **「データ取得範囲」を入力**:
        - 開始ページと終了ページを指定。
        3. **「実行ボタン」を押す**:
        - スクレイピングを開始します。
        4. **「CSVダウンロードボタン」を押す**:
        - 取得結果をCSV形式でダウンロードできます。
    """)

# 入力フォーム
with st.form(key="scraper_form"):
    base_url = st.text_input(
        "検索結果URL（ページ番号は{}に書き換える）",
        placeholder=""
    )
    start_page = st.number_input("取得開始ページ", min_value=1, value=1, step=1)
    end_page = st.number_input("取得終了ページ", min_value=1, value=1, step=1)
    output_csv = st.text_input("出力CSVファイル名", "shop_info.csv")
    submit_button = st.form_submit_button("スクレイピングを実行")

if submit_button:
    st.write("スクレイピングを開始します...")
    st.text(f"URL: {base_url}")
    st.text(f"取得範囲: {start_page}ページ目から{end_page}ページ目")
    st.text(f"出力ファイル名: {output_csv}")

    # パラメータをJSONファイルに保存
    params = {
        "base_url": base_url,
        "start_page": start_page,
        "end_page": end_page,
        "output_csv": output_csv
    }
    with open("params.json", "w") as f:
        json.dump(params, f)

    # scraper.pyを実行
    python_path = sys.executable
    result = subprocess.run([python_path, "demo.py"],
                            capture_output=True, text=True)

    if result.returncode == 0:
        st.success("スクレイピングが完了しました。結果をダウンロードしてください。")

        # ダウンロードボタンを表示
        with open(output_csv, "rb") as f:
            st.download_button(
                label="CSVをダウンロード",
                data=f,
                file_name=output_csv,
                mime="text/csv"
            )
    else:
        st.error("エラーが発生しました。詳細: " + result.stderr)


# import streamlit as st
# import json
# import sys
# import subprocess
# import os  # osモジュールをインポート

# st.title("Tabelog Scraper")

# with st.expander("使い方"):
#     st.markdown("""
#         1. **「URL」を入力**:
#             - 検索条件を絞り込んだ後の食べログのURLを入力。
#             - 検索条件が細かいほどパフォーマンスは上がる傾向にあります。
#         2. **「データ取得ページ数」を入力**:
#             - 必要に応じたページ数を指定できます。
#         3. **実行ボタンを押す**:
#             - 1ページあたり約20分かかります。現状、これがサーバーに負担をかけない範囲での処理時間となります。
#         4. **CSVダウンロードボタンを押す**:
#             - スクレイピング終了後に表示されます。
#     """)

# st.divider()

# with st.form(key="url_form"):
#     url = st.text_input("URLを入力")
#     start_page = st.number_input(
#         "データ取得ページ数", step=1, value=1, min_value=1)
#     output_csv = st.text_input("出力するCSVファイル名", "食べログ飲食店リスト.csv")
#     action_btn = st.form_submit_button("実行")

# if action_btn:
#     params = {
#         "url": url,
#         "start_page": start_page,
#         "output_csv": output_csv
#     }

#     with open('params.json', 'w') as f:
#         json.dump(params, f)

#     st.subheader('スクレイピング実行中です...')
#     st.text(f'検索URL：「{url}」')
#     st.text(f'データ取得ページ数：「{start_page}」')
#     st.text(f'出力CSVファイル名：「{output_csv}」')

#     # **ダウンロードボタン用のプレースホルダーを作成**
#     download_placeholder = st.empty()

#     # ログ表示用のプレースホルダーを作成
#     log_area = st.empty()

#     # Pythonのフルパスを取得
#     python_path = sys.executable

#     # subprocess.Popenを使用してリアルタイムでログを取得
#     process = subprocess.Popen(
#         [python_path, 'demo.py'],
#         stdout=subprocess.PIPE,
#         stderr=subprocess.STDOUT,
#         text=True,
#         bufsize=1
#     )

#     log_lines = []
#     # スクレイピングのログをリアルタイムで取得して表示
#     for line in process.stdout:
#         log_lines.append(line)
#         # ログを更新
#         log_area.text(''.join(log_lines))

#     process.wait()  # プロセスが完了するのを待つ

#     # processが定義されていることを確認してから使用
#     if process.returncode == 0:
#         st.success('実行完了')

#         # CSVファイルが存在するか確認
#         if os.path.exists(output_csv):
#             # 生成されたCSVファイルを読み込む
#             with open(output_csv, 'rb') as f:
#                 csv_data = f.read()

#             # **ダウンロードボタンをプレースホルダーに挿入**
#             download_placeholder.download_button(
#                 label="CSVファイルをダウンロード",
#                 data=csv_data,
#                 file_name=output_csv,
#                 mime='text/csv'
#             )
#         else:
#             st.warning('データが取得できなかったため、CSVファイルが生成されませんでした。')
#     else:
#         st.error('エラーが発生しました')
