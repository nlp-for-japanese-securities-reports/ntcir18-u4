import json
import argparse
import traceback
from pathlib import Path

GS_FILENAME = "../gold_standard_tr_valid.json"

class EvaluationException(Exception):
    pass

# JSONの読み込み
def load_json(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)

# データの確認
def check_data(eval_data, answer_data):
    for k in answer_data.keys():
        if k not in eval_data.keys():
            raise EvaluationException(f"入力データの回答が不足しています（ID: {k}）。データを確認してください。")
    for k in eval_data.keys():
        if k not in answer_data.keys():
            raise EvaluationException(f"入力データに不明な ID があります（ID: {k}）。データを確認してください。")

# Accuracyの算出
def calculate_accuracy(eval_data, answer_data):
    correct_table_id = 0
    for question_id, answer in answer_data.items():
        if eval_data[question_id] == answer:
            correct_table_id += 1
    accuracy_table_id = correct_table_id / len(answer_data)
    return accuracy_table_id

def main():
    # デフォルトのGSデータのファイルパス
    gs_data = (Path(__file__).parents[0] / GS_FILENAME)
    parser = argparse.ArgumentParser(description="NTCIR-18 U4 Table Retrieval サブタスクの評価スクリプト")
    parser.add_argument("-f", "--input-file", required=True, help="入力データを指定します")
    parser.add_argument("-g", "--gs-data", required=(not gs_data.exists()), default=gs_data, help="Gold Standard データを指定します")
    args = parser.parse_args()
    # 評価データ読み込み
    eval_data = load_json(args.input_file)
    # Gold Standardデータ読み込み
    answer_data = load_json(args.gs_data)

    check_data(eval_data, answer_data)
    result_table_id = calculate_accuracy(eval_data, answer_data)

    return json.dumps({
        "status": "success",
        "scores": {
            "table_id": result_table_id
        }
    }, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    try:
        print(main())
    except EvaluationException as e:
        print(json.dumps({"status": "failed", "message": e.args[0]}, ensure_ascii=False, indent=2))
        traceback.print_exc()
    except Exception:
        print(json.dumps({"status": "failed"}, ensure_ascii=False, indent=2))
        traceback.print_exc()
