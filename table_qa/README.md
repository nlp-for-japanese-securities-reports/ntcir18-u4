# Table QAサブタスク
[Table QAサブタスク](https://sites.google.com/view/ntcir18-u4/subtasks/table-qa?authuser=0, "Table QA") は、有価証券報告書に含まれる単一の表から、質問の答えに該当するデータを抽出するタスクです。\

## タスク設定
以下をご参照ください。\
[TQAタスクの設定](https://sites.google.com/view/ntcir18-u4/subtasks/table-qa?authuser=0, "Table QA")

## 配布ファイル
このリポジトリには、以下のファイルが``含まれます。
- `reports`
    - 各企業が発行した有価証券報告書に情報を追加したもので、入力として用います。
- `questions.json`
    - 質問文やコンテキストが記載されたファイルです。入力として用います。
- `gold_standard.json`
    - 正解データです。評価に用います。
    - `test_tqa`には含まれません。
- `answersheet.json`
    - 出力ファイルのテンプレートです。`value`、`cell_id`のどちらか、あるいは両方を埋める形で、出力ファイルを作成してください。
- `src/eval.py`
    - 評価スクリプトです。`-f`オプションで評価したいファイルのパス、`-g`オプションで正解データファイルのパスを指定してください。
- `src/eval.py`
    - 解答となる`value`と回答された`value`の表現を統一し、適切に評価を行うための関数が記述されたファイルです。リーダーボードでの評価においても、同じ関数が使用されています。
- `src/sample_random.py`
    - サンプルプログラムです。各質問に対し、ランダムなTable IDを付与し、出力ファイルを作成します。

## 入力ファイル形式
### HTMLファイル
各企業が発行した有価証券報告書（HTML 形式）に、必要なアノテーションを行ったものを利用します。

`reports/{doc_id}/*.html` は、各企業が発行した有価証券報告書に、以下の修正を加えたものです。

- `table` タグに `table-id` 属性を追加。
    - `table-id`は、テーブルを一意に識別する文字列で、`[書類管理番号(DocID)]-[ファイル名]-tab[テーブル連番]`の形式です。
    - 例：`S100IHTB-0000000-tab1`

- `th` タグ及び `td` タグに `cell-id` 属性を追加。
    - `table-id`は、テーブルを一意に識別する文字列で、`[書類管理番号(DocID)]-[ファイル名]-tab[テーブル連番]-r[列番号]c[行番号]`の形式です。
    - 例：`S100IHTB-0000000-tab1-r3c2`

### JSONファイル
`questions.json` は、以下のフォーマットです。

```json
{
    "QuestionID": {
        "question": "質問文",
        "doc_id": "Doc ID",
        "table_id": "Table ID",
        "cell_id": "Cell ID",
        "value": "セルの値"
    },
}
```

各パラメータの詳細を以下に示します。

| 要素名 | 型 | 説明 | 例 |
| --- | --- | --- | --- |
| question | string | 質問文。Queryとして用いる。 | 大和ハウス工業の2019年の個別のShareholdersEquityにおける「自己株式の処分」を含む表は？ |
| doc_id | string | 検索対象のHTMLが格納されたディレクトリ名。 <br> Contextとして用いる。 | S100ITAZ |
| table_id | string | 任意の`table`タグに付与された、`table-id`属性。 <br> Contextとして用いる。 | S100ITAZ-2020-tab1 |
| cell_id | string | 任意の`tr`あるいは`td`タグに付与された、`cell-id`属性。 <br> TQAタスクにおける予測対象の一つ。 | S100ITAZ-2020-tab1-r3c2 |
| value | string | 任意のセルの値。金額表現の場合は、桁数を考慮したものとなる。 <br> TQAタスクにおける予測対象の一つ。 | 3812000000 |

## 出力ファイル形式
`answersheet_tqa_test.json`の解答部分を埋める形式で、出力ファイルを作成してください。
- `answer_id`と`value`の2種類の回答箇所が存在します。いずれか片方のみ、あるいは両方に回答していただいて構いません。
    - `answer_id`には、`S100ITAZ-0101010-tab1-r3c2`というように、予測したCellIDを入力してください。
    - `value`には、`3812000000`というように、予測したデータそのものを入力してください。
- リーダーボードにおけるランキングは、valueのスコアを参照します。

## Baseline Scores
validディレクトリのデータセットを対象に、ベースライン手法を作成し、評価を行いました。

| モデル | 詳細モデル名 | Accuracy | 正解数 / 総質問数 |
| --- | --- | --- | --- |
| GPT-4o | gpt-4o-2024-05-13 | 0.6475 | 2028 / 3132 |
| GPT-3.5-turbo | gpt-3.5-turbo-0125 | 0.3493 | 1094 / 3132 |
| Gemini 1.5 Pro | gemini-1.5-pro-001 | 0.5744 | 1799 / 3132 |
| Gemini 1.5 Flash | gemini-1.5-flash-001 | 0.4898 | 1534 / 3132 |
| Claude 3 Opus | claude-3-opus-20240229 | 0.7471 | 2340 / 3132 |
| Claude 3 Haiku | claude-3-haiku-20240307 | 0.3209 | 1005 / 3132 |

## 特記事項
- データセットについて、Question IDは各タスクで連番になっていませんが、これはタスク間でQuestionの重複を防ぐためです。

## 出典
- `table_qa`ディレクトリ内のファイルは、EDINET 閲覧（提出）サイト（※）をもとに NTCIR-18 U4 タスクオーガナイザが作成したものです。
    - （※）例えば書類管理番号が `S100ISN0` の場合、当該ページの URL は `https://disclosure2.edinet-fsa.go.jp/WZEK0040.aspx?S100ISN0` となります。書類管理番号は、`train`/`test` ディレクトリ内の各ファイル名の先頭 8 文字です。
