import re
import unicodedata

def normalize_text(text):
    # 全角を半角に揃える
    normalized_text = unicodedata.normalize('NFKC', text)
    # 空白文字を削除する
    normalized_text = re.sub(r"\s", "", normalized_text)
    # カンマを削除する
    normalized_text = normalized_text.replace(',', '')
    # 三角記号をマイナス記号に統一する
    triangles = ['▲', '△', '▴', '▵']
    for triangle in triangles:
        normalized_text = normalized_text.replace(triangle, '-')
    # 位取りの置換
    if normalized_text == '0百万円':
        normalized_text = '0'
    elif normalized_text.endswith('百万円'):
        normalized_text = normalized_text.replace('百万円', '000000')
    elif normalized_text.endswith('千円'):
        normalized_text = normalized_text.replace('千円', '000')
    # 末尾の「円」「株」「個」を削除する
    normalized_text = normalized_text.rstrip('円株個')
    return normalized_text
