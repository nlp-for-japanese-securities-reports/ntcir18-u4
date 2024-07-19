import copy
import json
from pathlib import Path
import random

from bs4 import BeautifulSoup as bs
from tqdm import tqdm

# valid_trディレクトリのパスを指定
path_valid = Path(__file__).parents[1] / "valid_tr"
# 質問文やコンテキスト等が記述されたJSONファイルのパスを指定
path_questions = path_valid / "questions_tr_valid.json"
# answersheetのJSONファイルのパスを指定
path_answersheet = path_valid / "answersheet_tr_valid.json"
# 有報HTMLが格納されたディレクトリのパスを指定
path_reports = path_valid / "reports_tr_valid"
# 予測結果を出力するファイルのパスを指定
path_predicts = path_valid / "predicts_tr_valid.json"

# ランダムシードの設定
random.seed(0)

# 一つの文書に含まれるTable IDを全て取得する関数
def make_tableid_list(docid):
    talbeid_list = []
    path_htmls = (path_reports / docid).glob("*.html")
    for path_html in path_htmls:
        soup = bs(open(path_html), "html.parser")
        tables = soup.find_all("table")
        for table in tables:
            # Table IDは、tableタグのtable-id属性に記載されている
            talbeid_list.append(table["table-id"])
    return talbeid_list

def pred_tableid(docid, question):
    tableid = random.choice()
    return tableid

def main():
    # 質問文やコンテキスト等が記載されたJSONを読み込む
    with open(path_questions, mode="r") as f:
        question_details = json.load(f)
    # answersheetを読み込む
    with open(path_answersheet, mode="r") as f:
        answersheet = json.load(f)
    pred = copy.deepcopy(answersheet)
    # Doc IDごとにTable IDを記録しておくための辞書を宣言
    tableid_dict = {}
    # answersheetのKeyがQuestion IDなので、これを用いて質問文等を取得し、answersheetを埋める
    for question_id in tqdm(answersheet.keys()):
        # 質問文等を取得
        question_detail = question_details[question_id]
        question = question_detail["question"]
        docid = question_detail["doc_id"]
        # tableid_listのKeyにDoc IDが存在しない場合、Table IDのリストを取得
        if docid not in tableid_dict.keys():
            tableid_dict[docid] = make_tableid_list(docid)
        # Table IDをランダムに一つ抽出し、予測結果とする
        pred[question_id] = random.choice(tableid_dict[docid])
    with open(path_predicts, mode="w", encoding="utf-8") as f:
        json.dump(pred, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    main()
