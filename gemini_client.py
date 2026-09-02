"""Gemini API 呼び出し用の薄いラッパー。"""

import os

from google import genai
from google.genai import errors as genai_errors


class GeminiClientError(Exception):
    """Gemini API呼び出しに関するエラー。"""


def get_client(api_key: str) -> genai.Client:
    if not api_key:
        raise GeminiClientError("APIキーが設定されていません。サイドバーから入力するか.envに設定してください。")
    return genai.Client(api_key=api_key)


def generate_text(
    api_key: str,
    model: str,
    prompt: str,
    system_instruction: str | None = None,
    temperature: float = 0.7,
) -> str:
    """プロンプトを送信し、生成されたテキストを返す。"""
    client = get_client(api_key)

    config = {"temperature": temperature}
    if system_instruction:
        config["system_instruction"] = system_instruction

    try:
        response = client.models.generate_content(
            model=model,
            contents=prompt,
            config=config,
        )
    except genai_errors.APIError as e:
        raise GeminiClientError(f"Gemini APIエラー: {e}") from e

    if not response.text:
        raise GeminiClientError("Geminiから空の応答が返されました。プロンプトを見直してください。")

    return response.text


def resolve_api_key(session_key: str | None) -> str:
    """サイドバー入力を優先し、なければ環境変数から取得する。"""
    if session_key:
        return session_key
    return os.environ.get("GEMINI_API_KEY", "")
