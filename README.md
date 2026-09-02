# AIライティングツール

個人用のAIライティングアシスタント。ブログ記事の執筆、メール返信の作成、文章の要約をGemini APIで行う。

## 技術スタック

- Python
- Streamlit
- Gemini API (google-genai SDK)

## セットアップ

```bash
pip install -r requirements.txt
```

`.env.example` を `.env` にコピーし、Gemini APIキーを設定する。

```bash
cp .env.example .env
```

`.env`:

```
GEMINI_API_KEY=your_api_key_here
```

APIキーは [Google AI Studio](https://aistudio.google.com/apikey) で取得できる。
`.env` を使わず、アプリ起動後にサイドバーへ直接入力することも可能。

## 起動

```bash
streamlit run app.py
```

## 機能

- **ブログ記事**: テーマ・トーン・キーワードなどを入力して記事を生成
- **メール返信**: 受信メールと伝えたい内容から返信文面を生成
- **文章要約**: 長文を箇条書き/一段落/見出し付きなどの形式で要約
