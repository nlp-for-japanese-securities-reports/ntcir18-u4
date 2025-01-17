#!/usr/bin/env python3

import json
import argparse
import traceback
from pathlib import Path

from normalize import normalize_text

GS_FILENAME = "gold_standard_tqa_pub.json"

class EvaluationException(Exception):
    pass

# JSONの読み込み
def load_json(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        try:
            data = json.load(f)
        except ValueError:
            raise EvaluationException("JSONファイルのデコードに失敗しました。データを確認してください。")
    if type(data) != dict or not all(type(k) == str and type(v) == dict and type(v.get("cell_id", None)) == str and type(v.get("value", None)) == str for k, v in data.items()):
        raise EvaluationException("JSONファイルの形式が不正です。データを確認してください。")
    return data

# データの確認
def check_data(eval_data, answer_data, public_only=False):
    for k in answer_data.keys():
        if k not in eval_data.keys():
            raise EvaluationException(f"入力データの回答が不足しています（ID: {k}）。データを確認してください。")
    if not public_only:
        for k in eval_data.keys():
            if k not in answer_data.keys():
                raise EvaluationException(f"入力データに不明な ID があります（ID: {k}）。データを確認してください。")

# Accuracyの算出
def calculate_accuracy(eval_data, answer_data):
    correct_cell_id = 0
    correct_value = 0
    for question_id, answers in answer_data.items():
        pred_answers = eval_data[question_id]
        if pred_answers["cell_id"] == answers["cell_id"]:
            correct_cell_id += 1
        if normalize_text(pred_answers["value"]) == normalize_text(answers["value"]):
            correct_value += 1
    accuracy_cell_id = correct_cell_id / len(answer_data)
    accuracy_value = correct_value / len(answer_data)
    return accuracy_cell_id, accuracy_value

def main():
    # デフォルトのGSデータのファイルパス
    gs_data = (Path(__file__).parents[0] / GS_FILENAME)
    parser = argparse.ArgumentParser(description="NTCIR-18 U4 Table QA サブタスクの評価スクリプト")
    parser.add_argument("-f", "--input-file", required=True, help="入力データを指定します")
    parser.add_argument("-g", "--gs-data", required=(not gs_data.exists()), default=gs_data, help="Gold Standard データを指定します")
    parser.add_argument("-p", "--gs-data-private", required=False, default=None, help="Gold Standard データ (Private) を指定します")
    args = parser.parse_args()
    # 評価データ読み込み
    eval_data = load_json(args.input_file)
    # Gold Standardデータ読み込み
    answer_data = load_json(args.gs_data)
    private_data = load_json(args.gs_data_private) if args.gs_data_private is not None else {}

    check_data(eval_data, {**answer_data, **private_data}, args.gs_data_private is None)
    result_cell_id, result_value = calculate_accuracy(eval_data, answer_data)
    result_cell_id_private, result_value_private = calculate_accuracy(eval_data, private_data) if args.gs_data_private is not None else (0, 0)

    return json.dumps({
        "status": "success",
        "scores": [
            result_cell_id, # cell_id
            result_value,   # value
            result_cell_id_private,
            result_value_private,
        ]
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
