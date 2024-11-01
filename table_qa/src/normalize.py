import re
import unicodedata

# 文字列が数値データか判定する関数
def is_num(text):
    try:
        float(text)
    except ValueError:
        return False
    else:
        return True

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
    elif normalized_text.endswith('千'):
        normalized_text = normalized_text.replace('千', '000')
    # 末尾がパーセントであり、それ以外が数値である場合、末尾の単位を削除して位取りを変更する
    if normalized_text and normalized_text[-1] in ["%", "％"]:
        percentage_num_data = normalized_text.rstrip("%％")
        if is_num(percentage_num_data):
            normalized_text = str(float(percentage_num_data) / 100)
    # 末尾の「円」「株」「個」「倍」「人」「年」であり、それ以外が数値である場合、末尾の単位を削除する
    # 最終的に、文字列全てが数値であった場合、float型に変換し、有効数字を4桁にする
    num_data = normalized_text.rstrip('円株個倍人年')
    if is_num(num_data):
        normalized_text = format(float(num_data), ".4f")
    # -0の場合、0にする
    if normalized_text == "-0.0000":
        normalized_text = "0.0000"
    return normalized_text
