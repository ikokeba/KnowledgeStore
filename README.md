# Xブックマーク管理システム

XのブックマークをObsidianで管理し、分野・技術スタック・用途別にタグを付与してDataviewJSで動的に表示できるシステムです。

## 🎯 機能

- **自動タグ生成**: OpenAI APIを使用してブックマークコンテンツを分析し、適切なタグを自動生成
- **Obsidianプロパティ形式**: YAML frontmatterでタグを管理（`tags: - tag_name1 - tag_name2`）
- **分野別分類**: AI、機械学習、Web開発、データサイエンスなどの分野タグ
- **技術スタック分類**: Python、JavaScript、Docker、Gitなどの技術タグ（優先表示）
- **用途別分類**: チュートリアル、ツール、ライブラリ、記事などの用途タグ
- **新規フォルダ自動検出**: 新しいブックマークフォルダを自動検出して処理
- **外部リンク要約**: WaterCrawl公式Pythonクライアント（watercrawl-py）を使用して外部リンクの要約を自動取得
- **Obsidian DataviewJS対応**: 動的なタグ別表示と検索機能
- **スタイリッシュな表示**: 絵文字と階層構造で見やすい表示

## 📁 ディレクトリ構造

```
X_bookmarks/
├── bookmarks/                    # ブックマークファイル格納
│   ├── x-bookmarks-2025-07-23_sikibuton_cover/
│   └── x-bookmarks-2025-07-23_ikokeba/
├── _scripts/                     # 本番用スクリプトファイル
│   ├── tag_generator.py         # タグ自動生成・Obsidian形式追加スクリプト（メイン）
│   └── process_new_folders.py   # 新規フォルダ処理スクリプト
├── _tests/                       # テスト用スクリプトファイル
│   ├── test_system.py           # システムテストスクリプト
│   ├── simple_watercrawl_test.py # WaterCrawl単体テスト（Markdown保存機能付き）
│   ├── test_watercrawl_qiita.py # WaterCrawl Qiitaテスト
│   ├── test_watercrawl_final.py # WaterCrawl最終テスト
│   ├── test_watercrawl_correct.py # WaterCrawl正しいパラメータテスト
│   ├── test_watercrawl_alternative.py # WaterCrawl代替テスト
│   ├── debug_watercrawl.py      # WaterCrawlデバッグスクリプト
│   └── example_watercrawl_usage.py # WaterCrawl使用例スクリプト
├── javascript/                   # DataviewJS用JavaScriptファイル
│   ├── bookmark_tags.js         # タグ別表示用JS
│   ├── popular_tags.js          # 人気タグ表示用JS
│   └── all_tags.js              # 全タグ一覧表示用JS
├── _templates/                   # テンプレートファイル
├── watercrawl_output/           # WaterCrawlテスト用出力ディレクトリ
├── X_bookmarks_summary.md       # Obsidian用サマリーページ
├── requirements.txt             # Python依存関係
├── README.md                    # このファイル
└── log.md                       # プロジェクトログ
```

## 🚀 セットアップ

### 1. 依存関係のインストール

```bash
pip install -r requirements.txt
```

### 2. APIキーの設定

#### OpenAI APIキー（必須）

PowerShellで環境変数を設定：

```powershell
$env:OPENAI_API_KEY='your-openai-api-key'
```

#### WaterCrawl APIキー（オプション）

外部リンク要約機能を使用する場合：

```powershell
$env:WATERCRAWL_API_KEY='your-watercrawl-api-key'
```

または、システム環境変数として設定してください。

## 📖 使用方法

### 🎯 本番用スクリプト（タグ管理用）

#### 利用可能なディレクトリの確認

```bash
cd _scripts
python tag_generator.py --list
```

#### 指定したディレクトリのみタグ生成・Obsidian形式追加

```bash
cd _scripts
python tag_generator.py -d bookmarks/x-bookmarks-2025-01-27_new
```

#### すべてのディレクトリをタグ生成・Obsidian形式追加

```bash
cd _scripts
python tag_generator.py --all
```

#### 新規ブックマークフォルダの処理

```bash
cd _scripts
python process_new_folders.py
```

### 🧪 テスト用スクリプト（開発・デバッグ用）

#### システムテストの実行

```bash
cd _tests
python test_system.py
```

#### WaterCrawl単体テスト（Markdown保存機能付き）

```bash
cd _tests
python simple_watercrawl_test.py
```

#### WaterCrawl機能のテスト

```bash
cd _tests
python example_watercrawl_usage.py
```

#### WaterCrawl Qiitaテスト

```bash
cd _tests
python test_watercrawl_qiita.py
```

#### WaterCrawlデバッグ

```bash
cd _tests
python debug_watercrawl.py
```

## 🏷️ タグ体系

### 技術スタックタグ（優先表示）
- `Python` - Python関連
- `JavaScript` - JavaScript関連
- `Docker` - Docker関連
- `Git` - Git関連
- `Obsidian` - Obsidian関連

### 分野タグ
- `AI` - 人工知能関連
- `機械学習` - 機械学習関連
- `データサイエンス` - データサイエンス関連
- `生成AI` - 生成AI関連
- `Web開発` - Web開発関連
- `プログラミング` - プログラミング全般

### 用途タグ
- `チュートリアル` - チュートリアル記事
- `Tips` - 小技・Tips
- `基礎学習` - 基礎学習記事
- `ツール` - ツール紹介
- `ライブラリ` - ライブラリ紹介
- `記事` - 一般的な記事

## 📊 Obsidianでの表示

### サマリーページの表示

`X_bookmarks_summary.md`をObsidianで開くと、以下の情報が動的に表示されます：

- **タグ別表示**: 技術スタックタグを優先した階層表示
- **人気タグランキング**: 上位10件のタグ
- **全タグ一覧**: すべてのタグとその件数

### 外部リンク要約の表示

WaterCrawl APIキーが設定されている場合、ブックマークファイルに以下のセクションが自動追加されます：

```markdown
## External Link Summaries

### https://example.com
このページは技術的な内容を含んでおり、開発者向けの情報を提供しています。

### https://docs.example.com
公式ドキュメントでは、APIの使用方法とサンプルコードが詳しく説明されています。
```

### DataviewJS機能

システムは以下のJavaScriptファイルを使用して動的な表示を実現：

- `javascript/bookmark_tags.js`: タグ別のブックマーク表示
- `javascript/popular_tags.js`: 人気タグランキング
- `javascript/all_tags.js`: 全タグ一覧

### 表示の特徴

- **技術スタックタグ優先**: 最も重要な技術タグを一番上に表示
- **絵文字による視覚的区別**: 🔧（カテゴリ）、🏷️（タグ）
- **階層構造**: 見出しレベルで情報を整理
- **クリック可能なリンク**: Obsidianの内部リンク形式で確実に動作

## 🔧 カスタマイズ

### タグ生成の調整

`_scripts/tag_generator.py`の`generate_tags_with_openai`メソッドで、タグ生成のプロンプトを調整できます。

### タグカテゴリの追加

`javascript/bookmark_tags.js`の`categorizeTag`関数で、新しいタグカテゴリを追加できます：

```javascript
function categorizeTag(tag) {
    const fieldTags = ["AI", "機械学習", "データサイエンス", "生成AI", "Web開発", "プログラミング"];
    const techTags = ["Python", "JavaScript", "Docker", "Git", "Obsidian"];
    const usageTags = ["チュートリアル", "Tips", "基礎学習", "ツール", "ライブラリ", "記事"];
    
    // 新しいカテゴリを追加
    const newCategoryTags = ["新しいタグ1", "新しいタグ2"];
    
    if (techTags.includes(tag)) {
        return "技術スタックタグ";
    } else if (fieldTags.includes(tag)) {
        return "分野タグ";
    } else if (usageTags.includes(tag)) {
        return "用途タグ";
    } else if (newCategoryTags.includes(tag)) {
        return "新しいカテゴリ";
    } else {
        return "その他のタグ";
    }
}
```

### 新規フォルダの検出

`_scripts/process_new_folders.py`の`find_new_bookmark_folders`メソッドで、フォルダ検出の条件を調整できます。

## 🧪 テスト用スクリプトの説明

### テスト用スクリプトの用途

- **`test_system.py`**: システム全体の動作確認（依存関係、APIキー、ディレクトリ構造）
- **`simple_watercrawl_test.py`**: WaterCrawl APIの単体テスト（Markdown保存機能付き）
- **`test_watercrawl_qiita.py`**: QiitaサイトでのWaterCrawl動作確認
- **`test_watercrawl_final.py`**: WaterCrawl APIの最終動作確認
- **`test_watercrawl_correct.py`**: WaterCrawl APIの正しいパラメータ確認
- **`test_watercrawl_alternative.py`**: WaterCrawl APIの代替使用方法確認
- **`debug_watercrawl.py`**: WaterCrawl APIのデバッグ用
- **`example_watercrawl_usage.py`**: WaterCrawl機能の使用例

### テスト用スクリプトの実行タイミング

- **初回セットアップ時**: `test_system.py`でシステム全体の動作確認
- **WaterCrawl API設定時**: `simple_watercrawl_test.py`でAPI動作確認
- **問題発生時**: 各デバッグスクリプトで詳細な調査
- **機能確認時**: 各テストスクリプトで個別機能の動作確認

## 📝 ログ

処理状況は`log.md`に記録されます。また、以下のファイルも生成されます：

- `bookmark_tags_cache.json` - タグ生成のキャッシュ
- `processed_folders.json` - 処理済みフォルダの記録

## ⚠️ 注意事項

1. **OpenAI API使用料**: タグ生成にはOpenAI APIを使用するため、使用料が発生します
2. **WaterCrawl API使用料**: 外部リンク要約にはWaterCrawl公式Pythonクライアントを使用するため、使用料が発生する場合があります
3. **API制限**: OpenAI APIとWaterCrawl APIの制限に注意してください
4. **キャッシュ**: 一度生成したタグはキャッシュされるため、再処理時は高速です
5. **外部リンク処理**: 外部リンクの要約取得には時間がかかる場合があります
6. **Obsidian DataviewJS**: DataviewJSプラグインが必要です
7. **JavaScriptファイル**: `javascript/`フォルダ内のJSファイルは外部参照用です
8. **スクリプトの使い分け**: 本番用は`_scripts/`、テスト用は`_tests/`ディレクトリを使用してください
9. **テスト用スクリプト**: 開発・デバッグ時以外は使用しないでください

## 🤝 貢献

バグ報告や機能要望は、プロジェクトログに記載してください。

## 📄 ライセンス

このプロジェクトはMITライセンスの下で公開されています。 