import streamlit as st
import json
import sys
import subprocess

st.title("Tabelog Scraper")

with st.expander("使い方"):
    st.markdown("""
        1. **「URL」を入力**:
            - 検索条件を絞り込んだ後の食べログのURLを入力。
            - 検索条件が細かいほどパフォーマンスは上がる傾向にあります。
        2. **「データ取得ページ数」を入力**:
            - 必要に応じたページ数を指定できます。
        3. **実行ボタンを押す**:
            - 1ページあたり約20分かかります。現状、これがサーバーに負担をかけない範囲での処理時間となります。
        4. **CSVダウンロードボタンを押す**:
            - スクレイピング終了後に表示されます。
    """)

st.divider()

with st.form(key="url_form"):
    url = st.text_input("URLを入力")
    max_search_page = st.number_input(
        "データ取得ページ数", step=1, value=1, min_value=1)
    output_csv = st.text_input("出力するCSVファイル名", "食べログ飲食店リスト.csv")
    action_btn = st.form_submit_button("実行")

if action_btn:
    params = {
        "url": url,
        "max_search_page": max_search_page,
        "output_csv": output_csv
    }

    with open('params.json', 'w') as f:
        json.dump(params, f)

    st.subheader('スクレイピング実行中です...')
    st.text(f'検索URL：「{url}」')
    st.text(f'データ取得ページ数：「{max_search_page}」')
    st.text(f'出力CSVファイル名：「{output_csv}」')

    # **ダウンロードボタン用のプレースホルダーを作成**
    download_placeholder = st.empty()

    # ログ表示用のプレースホルダーを作成
    log_area = st.empty()

    # Pythonのフルパスを取得
    python_path = sys.executable

    # subprocess.Popenを使用してリアルタイムでログを取得
    process = subprocess.Popen(
        [python_path, 'demo.py'],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1
    )

    log_lines = []
    # スクレイピングのログをリアルタイムで取得して表示
    for line in process.stdout:
        log_lines.append(line)
        # ログを更新
        log_area.text(''.join(log_lines))

    process.wait()

    if process.returncode == 0:
        st.success('実行完了')

        # 生成されたCSVファイルを読み込む
        with open(output_csv, 'rb') as f:
            csv_data = f.read()

        # **ダウンロードボタンをプレースホルダーに挿入**
        download_placeholder.download_button(
            label="CSVファイルをダウンロード",
            data=csv_data,
            file_name=output_csv,
            mime='text/csv'
        )
    else:
        st.error('エラーが発生しました')


# import streamlit as st
# import json
# import sys
# import subprocess

# st.title("Tabelog Scraper")

# with st.expander("使い方"):
#     st.markdown("""
#               1. **「URL」を入力**:
#               - 検索条件を絞り込んだ後の食べログのURLを入力。
#               - 検索条件が細かいほどパフォーマンスは上がりる傾向にあります
#               2. **「データ取得ページ数」を入力**:
#               - 必要に応じたページ数を指定できます。
#               3. **実行ボタンを押す**:
#               - 1ページあたり約20分かかります。現状、これがサーバーに負担をかけない範囲での処理時間となります。
#               4. **CSVダウンロードボタンを押す**:
#               - スクレイピング終了後に表示されます。
#               """)
# st.divider()

# with st.form(key="url_form"):
#     url = st.text_input("URLを入力")
#     max_search_page = st.number_input(
#         "データ取得ページ数", step=1, value=1, min_value=1,)
#     output_csv = st.text_input("出力するCSVファイル名", "食べログ飲食店リスト.csv")
#     action_btn = st.form_submit_button("実行")

# if action_btn:
#     st.subheader('スクレイピング実行中です...')
#     st.text(f'検索URL：「{url}」')
#     st.text(f'データ取得ページ数：「{max_search_page}」')
#     st.text(f'出力CSVファイル名：「{output_csv}」')

#     params = {
#         "url": url,
#         "max_search_page": max_search_page,
#         "output_csv": output_csv
#     }
#     with open('params.json', 'w') as f:
#         json.dump(params, f)

#     # Pythonのフルパスを取得
#     python_path = sys.executable

#     # subprocess.runを使ってスクリプトを実行。Python実行環境を明示的に指定。
#     result = subprocess.run([python_path, 'demo.py'],
#                             capture_output=True,
#                             text=True
#                             )

#     if result.returncode == 0:
#         st.success('実行完了')

#         # 生成されたCSVファイルを読み込む
#         with open(output_csv, 'rb') as f:
#             csv_data = f.read()

#         # CSVファイルをダウンロードするためのボタンを表示
#         st.download_button(
#             label="CSVファイルをダウンロード",
#             data=csv_data,
#             file_name=output_csv,
#             mime='text/csv'
#         )
#     else:
#         st.error('エラーが発生しました: ' + result.stderr)
