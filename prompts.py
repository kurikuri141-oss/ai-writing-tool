"""各機能のプロンプトテンプレート。"""

BLOG_SYSTEM_INSTRUCTION = (
    "あなたはプロのブログライターです。読者にとって分かりやすく、"
    "自然な日本語で魅力的な記事を書いてください。見出しや箇条書きを"
    "適切に使い、Markdown形式で出力してください。"
)


def build_blog_prompt(topic: str, tone: str, length: str, keywords: str, outline: str) -> str:
    parts = [f"以下の条件でブログ記事を作成してください。\n\nテーマ: {topic}"]
    if tone:
        parts.append(f"文体・トーン: {tone}")
    if length:
        parts.append(f"文章の長さの目安: {length}")
    if keywords:
        parts.append(f"含めたいキーワード: {keywords}")
    if outline:
        parts.append(f"構成・盛り込みたい内容:\n{outline}")
    parts.append("タイトル案も1つ提案してください。")
    return "\n\n".join(parts)


EMAIL_SYSTEM_INSTRUCTION = (
    "あなたは丁寧で的確なビジネスメール作成のアシスタントです。"
    "日本のビジネスマナーに沿った自然な敬語を使い、簡潔で分かりやすい"
    "返信メール文面を作成してください。"
)


def build_email_prompt(original_email: str, intent: str, tone: str, sender_name: str) -> str:
    parts = [f"以下の受信メールに対する返信メールの文面を作成してください。\n\n【受信メール】\n{original_email}"]
    if intent:
        parts.append(f"【返信で伝えたい内容】\n{intent}")
    if tone:
        parts.append(f"【トーン】{tone}")
    if sender_name:
        parts.append(f"【差出人名】{sender_name}")
    parts.append("件名案と本文をそれぞれ分かる形で出力してください。")
    return "\n\n".join(parts)


SUMMARY_SYSTEM_INSTRUCTION = (
    "あなたは文章要約の専門家です。与えられた文章の要点を漏らさず、"
    "簡潔で分かりやすい日本語に要約してください。"
)


def build_summary_prompt(text: str, style: str, length: str) -> str:
    parts = [f"以下の文章を要約してください。\n\n【原文】\n{text}"]
    if style:
        parts.append(f"【要約の形式】{style}")
    if length:
        parts.append(f"【要約の長さの目安】{length}")
    return "\n\n".join(parts)
