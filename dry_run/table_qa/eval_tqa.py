import json
import argparse
import unicodedata
import re

def load_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def normalize_text(text):
    # 空白文字を削除する
    normalized_text = re.sub(r"\s", "", text)
    # 全角を半角に揃える
    normalized_text = unicodedata.normalize('NFKC', normalized_text)
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

def calculate_accuracy(eval_data, answer_data, evaluation_type, detailed_output=False):
    correct = 0
    total = 0
    details = []
    
    for question_id, eval_answer in eval_data.items():
        if question_id in answer_data:
            answer = answer_data[question_id]
            if evaluation_type == 'cell_id' and 'cell_id' in eval_answer and 'cell_id' in answer:
                if eval_answer['cell_id'] == answer['cell_id']:
                    correct += 1
                    result = "Correct"
                else:
                    result = "Incorrect"
                if detailed_output:
                    details.append((question_id, "Question ID", eval_answer['cell_id'], answer['cell_id'], result))
                total += 1
            elif evaluation_type == 'value' and 'value' in eval_answer and 'value' in answer:
                eval_value_normalized = normalize_text(eval_answer['value'])
                answer_value_normalized = normalize_text(answer['value'])
                if eval_value_normalized == answer_value_normalized:
                    correct += 1
                    result = "Correct"
                else:
                    result = "Incorrect"
                if detailed_output:
                    details.append((question_id, eval_value_normalized, answer_value_normalized, result))
                total += 1
    
    return correct, total, details

def main():
    parser = argparse.ArgumentParser(description="Evaluate JSON files.")
    parser.add_argument('-f', '--evaluation_json', required=True, help="Path to the evaluation JSON file")
    parser.add_argument('-g', '--answer_json', required=True, help="Path to the answer JSON file")
    parser.add_argument('-v', '--verbose', action='store_true', help="Output detailed results")
    
    args = parser.parse_args()
    
    eval_json_path = args.evaluation_json
    answer_json_path = args.answer_json
    detailed_output = args.verbose
    
    eval_data = load_json(eval_json_path)
    answer_data = load_json(answer_json_path)
    
    cell_id_correct, cell_id_total, cell_id_details = calculate_accuracy(eval_data, answer_data, 'cell_id', detailed_output)
    value_correct, value_total, value_details = calculate_accuracy(eval_data, answer_data, 'value', detailed_output)
    
    if detailed_output:
        print("\nDetailed Results:")
        if cell_id_details:
            print("\ncell_id Details:")
            for detail in cell_id_details:
                print(f"{detail[0]}, {detail[1]}, Eval: {detail[2]}, Answer: {detail[3]}, Result: {detail[4]}")
        if value_details:
            print("\nResult Details:")
            for detail in value_details:
                print(f"{detail[0]}, Eval value: {detail[1]}, Answer value: {detail[2]}, Result: {detail[3]}")

    if cell_id_total > 0:
        cell_id_accuracy = cell_id_correct / cell_id_total
        print(f"cell_id accuracy: {cell_id_accuracy:.4f} ({cell_id_correct}/{cell_id_total})")
    else:
        print("No cell_id evaluations found.")
    
    if value_total > 0:
        value_accuracy = value_correct / value_total
        print(f"value accuracy: {value_accuracy:.4f} ({value_correct}/{value_total})")
    else:
        print("No value evaluations found.")

if __name__ == "__main__":
    main()