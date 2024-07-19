import copy
import json
from pathlib import Path
import random

from bs4 import BeautifulSoup as bs
from tqdm import tqdm

# valid_tqaディレクトリのパスを指定
path_valid = Path(__file__).parents[1] / "valid_tqa"
# 質問文やコンテキスト等が記述されたJSONファイルのパスを指定
path_questions = path_valid / "questions_tqa_valid.json"
# answersheetのJSONファイルのパスを指定
path_answersheet = path_valid / "answersheet_tqa_valid.json"
# 有報HTMLが格納されたディレクトリのパスを指定
path_reports = path_valid / "reports_tqa_valid"
# 予測結果を出力するファイルのパスを指定
path_predicts = path_valid / "predicts_tqa_valid.json"

# ランダムシードの設定
random.seed(0)

# 一つの文書に含まれるCell IDとValueを全て取得する
def make_cellid_value_dict(docid):
    cellid_value_dict = {}
    path_htmls = (path_reports / docid).glob("*.html")
    for path_html in path_htmls:
        soup = bs(open(path_html), "html.parser")
        tables = soup.find_all("table")
        for table in tables:
            # Table IDは、tableタグのtable-id属性に記載されている
            table_id = (table["table-id"])
            cellid_value_dict[table_id] = []
            for cell in table.find_all(["td", "th"]):
                # Cell IDは、td, thタグのcell-id属性に記載されている
                cell_id = cell["cell-id"]
                value = cell.get_text(strip=True)
                cellid_value_dict[table_id].append([cell_id, value])
    return cellid_value_dict

def main():
    # 質問文やコンテキスト等が記載されたJSONを読み込む
    with open(path_questions, mode="r") as f:
        question_details = json.load(f)
    # answersheetを読み込む
    with open(path_answersheet, mode="r") as f:
        answersheet = json.load(f)
    pred = copy.deepcopy(answersheet)
    # Doc IDごとにCell IDとValueを記録しておくための辞書を宣言
    cellid_value_dict = {}
    # answersheetのKeyがQuestion IDなので、これを用いて質問文等を取得し、answersheetを埋める
    for question_id in tqdm(answersheet.keys()):
        # 質問文等を取得
        question_detail = question_details[question_id]
        question = question_detail["question"]
        docid = question_detail["doc_id"]
        table_id = question_detail["table_id"]
        # tableid_listのKeyにDoc IDが存在しない場合、Cell IDとValueのリストを取得
        if docid not in cellid_value_dict.keys():
            cellid_value_dict[docid] = make_cellid_value_dict(docid)
        # Cell IDとValueをそれぞれランダムに一つ抽出し、予測結果とする
        pred[question_id]["cell_id"] = random.choice(cellid_value_dict[docid][table_id])[0]
        pred[question_id]["value"] = random.choice(cellid_value_dict[docid][table_id])[1]
    with open(path_predicts, mode="w", encoding="utf-8") as f:
        json.dump(pred, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    main()
