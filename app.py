"""個人用AIライティングツール(ブログ執筆 / メール返信作成 / 文章要約)。"""

import streamlit as st
from dotenv import load_dotenv

from gemini_client import GeminiClientError, generate_text, resolve_api_key
from prompts import (
    BLOG_SYSTEM_INSTRUCTION,
    EMAIL_SYSTEM_INSTRUCTION,
    SUMMARY_SYSTEM_INSTRUCTION,
    build_blog_prompt,
    build_email_prompt,
    build_summary_prompt,
)

load_dotenv()

st.set_page_config(page_title="AIライティングツール", page_icon="✍️", layout="wide")

MODEL_OPTIONS = {
    "Gemini 2.5 Flash (高速・低コスト)": "gemini-2.5-flash",
    "Gemini 2.5 Pro (高品質)": "gemini-2.5-pro",
}

with st.sidebar:
    st.header("設定")
    api_key_input = st.text_input(
        "Gemini APIキー",
        type="password",
        placeholder=".envに設定済みの場合は空欄でOK",
        help="環境変数 GEMINI_API_KEY が設定されていればこの入力は不要です。",
    )
    model_label = st.selectbox("モデル", list(MODEL_OPTIONS.keys()))
    model_name = MODEL_OPTIONS[model_label]
    temperature = st.slider("創造性 (temperature)", 0.0, 1.0, 0.7, 0.05)

api_key = resolve_api_key(api_key_input)

st.title("✍️ AIライティングツール")
st.caption("ブログ記事の執筆 / メール返信の作成 / 文章の要約")

tab_blog, tab_email, tab_summary = st.tabs(["📝 ブログ記事", "✉️ メール返信", "📄 文章要約"])


def show_result(text: str):
    st.subheader("生成結果")
    st.markdown(text)
    st.text_area("コピー用テキスト", value=text, height=250)


def run_generation(system_instruction: str, prompt: str):
    if not api_key:
        st.error("Gemini APIキーが未設定です。サイドバーに入力するか.envに設定してください。")
        return
    with st.spinner("生成中..."):
        try:
            result = generate_text(
                api_key=api_key,
                model=model_name,
                prompt=prompt,
                system_instruction=system_instruction,
                temperature=temperature,
            )
        except GeminiClientError as e:
            st.error(str(e))
            return
    show_result(result)


with tab_blog:
    st.subheader("ブログ記事を作成")
    blog_topic = st.text_input("テーマ・タイトル案", key="blog_topic")
    col1, col2 = st.columns(2)
    with col1:
        blog_tone = st.text_input("文体・トーン(例: カジュアル、専門的)", key="blog_tone")
    with col2:
        blog_length = st.text_input("長さの目安(例: 1000字程度)", key="blog_length")
    blog_keywords = st.text_input("含めたいキーワード(カンマ区切り)", key="blog_keywords")
    blog_outline = st.text_area("構成メモ・盛り込みたい内容(任意)", key="blog_outline", height=150)

    if st.button("記事を生成", type="primary", key="blog_button"):
        if not blog_topic:
            st.warning("テーマを入力してください。")
        else:
            prompt = build_blog_prompt(blog_topic, blog_tone, blog_length, blog_keywords, blog_outline)
            run_generation(BLOG_SYSTEM_INSTRUCTION, prompt)

with tab_email:
    st.subheader("メール返信を作成")
    email_original = st.text_area("受信したメール本文", key="email_original", height=200)
    email_intent = st.text_area("返信で伝えたい内容(箇条書きでOK)", key="email_intent", height=100)
    col1, col2 = st.columns(2)
    with col1:
        email_tone = st.text_input("トーン(例: 丁寧、フォーマル、フランク)", key="email_tone")
    with col2:
        email_sender = st.text_input("差出人名(任意)", key="email_sender")

    if st.button("返信を生成", type="primary", key="email_button"):
        if not email_original or not email_intent:
            st.warning("受信メール本文と伝えたい内容を入力してください。")
        else:
            prompt = build_email_prompt(email_original, email_intent, email_tone, email_sender)
            run_generation(EMAIL_SYSTEM_INSTRUCTION, prompt)

with tab_summary:
    st.subheader("文章を要約")
    summary_text = st.text_area("要約したい文章", key="summary_text", height=250)
    col1, col2 = st.columns(2)
    with col1:
        summary_style = st.selectbox(
            "要約の形式",
            ["箇条書き", "一段落の文章", "見出し付きまとめ"],
            key="summary_style",
        )
    with col2:
        summary_length = st.text_input("長さの目安(例: 3行程度)", key="summary_length")

    if st.button("要約を生成", type="primary", key="summary_button"):
        if not summary_text:
            st.warning("要約したい文章を入力してください。")
        else:
            prompt = build_summary_prompt(summary_text, summary_style, summary_length)
            run_generation(SUMMARY_SYSTEM_INSTRUCTION, prompt)
