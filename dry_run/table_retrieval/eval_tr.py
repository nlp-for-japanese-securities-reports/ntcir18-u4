import json
import argparse
import unicodedata
import re

def load_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def calculate_accuracy(eval_data, answer_data, detailed_output=False):
    correct = 0
    total = 0
    details = []
    
    for question_id, eval_answer in eval_data.items():
        if eval_answer == answer_data:
            correct += 1
            result = "Correct"
        else:
            result = "Incorrect"
        if detailed_output:
            details.append((question_id, "Question ID", eval_answer, answer_data[question_id], result))
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
    
    correct, total, details = calculate_accuracy(eval_data, answer_data, detailed_output)
    
    if detailed_output:
        print("\nDetailed Results:")
        if details:
            print("\nDetails:")
            for detail in details:
                print(f"{detail[0]}, {detail[1]}, Eval: {detail[2]}, Answer: {detail[3]}, Result: {detail[4]}")

    if total > 0:
        cell_id_accuracy = correct / total
        print(f"cell_id accuracy: {cell_id_accuracy:.4f} ({correct}/{total})")
    else:
        print("No table_id evaluations found.")

if __name__ == "__main__":
    main()