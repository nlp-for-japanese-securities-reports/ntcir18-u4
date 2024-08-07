# Table Retrievalサブタスク
[Table Retrievalサブタスク](https://sites.google.com/view/ntcir18-u4/subtasks/table-retrieval?authuser=0, "Table Retrieval") は、単一の文書（有価証券報告書）から、質問の答えに該当するデータが含まれる表を検索するタスクです。\

## タスク設定
以下をご参照ください。\
[TRタスクの設定](https://sites.google.com/view/ntcir18-u4/subtasks/table-retrieval?authuser=0, "Table Retrieval")

## 配布ファイル
このリポジトリには、以下のファイルが含まれます。
- `reports_tr_{type}`
    - 各企業が発行した有価証券報告書に情報を追加したもので、入力として用います。
- `questions_tr_{type}.json`
    - 質問文やコンテキストが記載されたファイルです。入力として用います。
- `gold_standard_tr_{type}.json`
    - 正解データです。評価に用います。
    - `test_tr`には含まれません。
- `answersheet_tr_{type}.json`
    - 出力ファイルのテンプレートです。Valueを埋める形で、出力ファイルを作成してください。
- `src/eval.py`
    - 評価スクリプトです。`-f`オプションで評価したいファイルのパス、`-g`オプションで正解データファイルのパスを指定してください。
- `src/sample_tr_random.py`
    - サンプルプログラムです。各質問に対し、ランダムなTable IDを付与し、出力ファイルを作成します。

## 入力ファイル形式
### HTMLファイル
各企業が発行した有価証券報告書（HTML 形式）に、必要なアノテーションを行ったものを利用します。

`reports_tr_{type}/{doc_id}/*.html` は、各企業が発行した有価証券報告書に、以下の修正を加えたものです。

- `table` タグに `table-id` 属性を追加。
    - `table-id`は、テーブルを一意に識別する文字列で、`[書類管理番号(DocID)]-[ファイル名]-tab[テーブル連番]`の形式です。
    - 例：`S100IHTB-0000000-tab1`

- `th` タグ及び `td` タグに `cell-id` 属性を追加。
    - `table-id`は、テーブルを一意に識別する文字列で、`[書類管理番号(DocID)]-[ファイル名]-tab[テーブル連番]-r[列番号]c[行番号]`の形式です。
    - 例：`S100IHTB-0000000-tab1-r3c2`

### JSONファイル
`questions_tr_{type}.json` は、

```json
{
    "QuestionID": {
        "question": "質問文",
        "doc_id": "Doc ID",
        "table_id": "Table ID"
    },
}
```

各パラメータの詳細を以下に示します。

| 要素名 | 型 | 説明 | 例 |
| --- | --- | --- | --- |
| question | string | 質問文。Queryとして用いる。 | 大和ハウス工業の2019年の個別のShareholdersEquityにおける「自己株式の処分」を含む表は？ |
| doc_id | string | 検索対象のHTMLが格納されたディレクトリ名。 <br> Contextとして用いる。 | S100ITAZ |
| table_id | string | 任意の`table`タグに付与された、`table-id`属性。 <br> TRタスクにおける予測対象。 | S100ITAZ-2020-tab1 |

## 出力ファイル形式
`answersheet_tr_test.json`の解答部分を埋める形式で、出力ファイルを作成してください。

## Baseline Scores
validディレクトリのデータセットを対象に、ベースライン手法を作成し、評価を行いました。

| 手法 | Accuracy | 正解数 / 質問数 |
| --- | --- | --- |
| text-embedding-3-small + Cell Text | 0.0128 | 40 / 3131 |
| text-embedding-3-large + Cell Text | 0.0125 | 39 / 3131 |
| text-embedding-3-small + HTML Text | 0.1843 | 577 / 3131 |
| text-embedding-3-large + HTML Text | 0.1418 | 444 / 3131 |
| text-embedding-3-small + Markdown Text | 0.1233 | 386 / 3131 |
| text-embedding-3-large + Markdown Text | 0.1383 | 433 / 3131 |

## 特記事項
- データセットについて、Question IDは各タスクで連番になっていませんが、これはタスク間でQuestionの重複を防ぐためです。

## 出典
- `table_retrieval`ディレクトリ内のファイルは、EDINET 閲覧（提出）サイト（※）をもとに NTCIR-18 U4 タスクオーガナイザが作成したものです。
    - （※）例えば書類管理番号が `S100ISN0` の場合、当該ページの URL は `https://disclosure2.edinet-fsa.go.jp/WZEK0040.aspx?S100ISN0` となります。書類管理番号は、`train`/`test` ディレクトリ内の各ファイル名の先頭 8 文字です。
