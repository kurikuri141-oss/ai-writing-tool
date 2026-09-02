# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## このプロジェクトについて

- StreamlitとGemini APIで作られた個人用AIライティングツール
- データベースなし・認証なし、単一ユーザー・ローカル実行のみを前提
- 機能は3つ: ブログ記事の下書き、メール返信の下書き、文章の要約

## よく使うコマンド

- 依存パッケージのインストール(`.venv`へ)
  ```bash
  .venv/Scripts/python -m pip install -r requirements.txt
  ```
- アプリの起動
  ```bash
  streamlit run app.py
  ```
- venvを有効化していない場合の起動
  ```bash
  .venv/Scripts/python -m streamlit run app.py
  ```
- テスト・リンター・ビルド手順はこのプロジェクトには存在しない

## 設定(APIキー)

- APIキーは`python-dotenv`経由で`.env`ファイル(`GEMINI_API_KEY=...`)から読み込む
- `.env`は`.env.example`をコピーして作成する
- `gemini_client.resolve_api_key()`は、Streamlitサイドバーに入力されたキーを`.env`/環境変数より優先する
  - つまりサイドバー入力があれば、それがファイルを編集せずに`.env`の値を上書きする

## アーキテクチャ

- **`app.py`** — UI全体を担当する唯一のファイル
  - `st.set_page_config`で1ページ構成
  - サイドバー: APIキー上書き入力、モデル選択、temperature調整
  - `st.tabs`でブログ/メール/要約の3タブを表示
  - 各タブは`prompts.py`でプロンプトを組み立て、`run_generation()`(ローカルヘルパー)を呼ぶ
  - `run_generation()`が`gemini_client.generate_text()`をスピナー・エラー処理付きでラップし、`show_result()`で結果を表示する
- **`gemini_client.py`** — `google-genai` SDK(`google.genai.Client`)の薄いラッパー
  - すべてのGemini呼び出しは`generate_text()`を経由する
  - `system_instruction`は任意引数
  - APIエラーや空応答の場合は`GeminiClientError`を送出する
  - `app.py`側は生のSDK例外ではなく、常に`GeminiClientError`をキャッチする
- **`prompts.py`** — 機能ごとに「システム指示の定数」+「`build_*_prompt()`関数」を1組ずつ持つ
  - 対象: ブログ/メール/要約の3機能
  - テンプレートエンジンは使わず、条件付きの文字列連結でプロンプトを組み立てる

## 4つ目の機能を追加する場合

- `prompts.py`に新しいシステム指示定数と`build_x_prompt()`を追加する
- `app.py`に新しい`st.tabs`エントリを追加し、入力を集めて`run_generation()`を呼ぶようにする

## 利用可能なモデルを増やす場合

- `app.py`内の`MODEL_OPTIONS`辞書にハードコードされている(現在はGemini 2.5 Flash / Pro)
- ここに項目を追加すると、サイドバーの選択肢に表示される
