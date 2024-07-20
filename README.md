# ntcir18-u4
[NTCIR-18 U4タスク](https://sites.google.com/view/ntcir18-u4/home?authuser=0, "NTCIR-18 U4")（**U**nifying, **U**nderstanding, and **U**tilizing **U**nstructured Data in Financial Reports
）で用いるデータセットです。\
U4タスクは、 **Table Retrievalサブタスク（以下、TRタスク）** と、 **Table QAサブタスク（以下、TQAタスク）** から構成されます。

## 更新情報
- (2024/7/20) testデータの公開
- (2024/7/11) validデータの公開

## タスク設定
以下をご参照ください。\
[TRタスク](https://sites.google.com/view/ntcir18-u4/subtasks/table-retrieval?authuser=0, "Table Retrieval")\
[TQAタスク](https://sites.google.com/view/ntcir18-u4/subtasks/table-qa?authuser=0, "Table QA")

## Baseline Scores
validディレクトリのデータセットを対象に、各タスクのベースラインを作成し、評価を行いました。

### TRタスク
準備中

### TQAタスク
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
- `table_retrieval`および`table_qa`ディレクトリ内のファイルは、EDINET 閲覧（提出）サイト（※）をもとに NTCIR-18 U4 タスクオーガナイザが作成したものです。
    - （※）例えば書類管理番号が `S100ISN0` の場合、当該ページの URL は `https://disclosure2.edinet-fsa.go.jp/WZEK0040.aspx?S100ISN0` となります。書類管理番号は、`train`/`test` ディレクトリ内の各ファイル名の先頭 8 文字です。
