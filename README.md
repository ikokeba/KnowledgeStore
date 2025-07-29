# Xブックマーク管理システム

XのブックマークをObsidianで管理し、分野・技術スタック・用途別にタグを付与してDataviewで表示できるシステムです。

## 🎯 機能

- **自動タグ生成**: OpenAI APIを使用してブックマークコンテンツを分析し、適切なタグを自動生成
- **分野別分類**: AI、機械学習、Web開発、データサイエンスなどの分野タグ
- **技術スタック分類**: Python、JavaScript、Docker、Gitなどの技術タグ
- **用途別分類**: チュートリアル、ツール、ライブラリ、記事などの用途タグ
- **新規フォルダ自動検出**: 新しいブックマークフォルダを自動検出して処理
- **Obsidian Dataview対応**: タグ別・日付別の表示と検索機能

## 📁 ディレクトリ構造

```
X_bookmarks/
├── bookmarks/                    # ブックマークファイル格納
│   ├── x-bookmarks-2025-07-23_sikibuton_cover/
│   └── x-bookmarks-2025-07-23_ikokeba/
├── _scripts/                     # スクリプトファイル
│   ├── tag_generator.py         # タグ自動生成スクリプト
│   └── process_new_folders.py   # 新規フォルダ処理スクリプト
├── _templates/                   # テンプレートファイル
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

### 2. OpenAI APIキーの設定

PowerShellで環境変数を設定：

```powershell
$env:OPENAI_API_KEY='your-openai-api-key'
```

または、システム環境変数として設定してください。

## 📖 使用方法

### 利用可能なディレクトリの確認

```bash
cd _scripts
python tag_generator.py --list
```

### 指定したディレクトリのみタグ生成

```bash
cd _scripts
python tag_generator.py -d bookmarks/x-bookmarks-2025-01-27_new
```

### すべてのディレクトリをタグ生成

```bash
cd _scripts
python tag_generator.py --all
```

### タグ生成・Obsidianプロパティ形式追加（一括処理）

```bash
cd _scripts
# 指定したディレクトリのみ（タグ生成→Obsidian形式追加を一括実行）
python tag_generator.py -d bookmarks/x-bookmarks-2025-01-27_new

# すべてのディレクトリ（タグ生成→Obsidian形式追加を一括実行）
python tag_generator.py --all
```

### 新規ブックマークフォルダの処理

```bash
cd _scripts
python process_new_folders.py
```

## 🏷️ タグ体系

### 分野タグ
- `#AI` - 人工知能関連
- `#機械学習` - 機械学習関連
- `#データサイエンス` - データサイエンス関連
- `#Web開発` - Web開発関連
- `#プログラミング` - プログラミング全般

### 技術スタックタグ
- `#Python` - Python関連
- `#JavaScript` - JavaScript関連
- `#Docker` - Docker関連
- `#Git` - Git関連
- `#Obsidian` - Obsidian関連

### 用途タグ
- `#チュートリアル` - チュートリアル記事
- `#ツール` - ツール紹介
- `#ライブラリ` - ライブラリ紹介
- `#記事` - 一般的な記事
- `#Tips` - 小技・Tips

## 📊 Obsidianでの表示

### サマリーページの表示

`X_bookmarks_summary.md`をObsidianで開くと、以下の情報が表示されます：

- 総ブックマーク数
- 日付別ブックマーク数
- タグ別表示
- 最新のブックマーク
- 人気タグランキング

### Dataviewクエリ例

```dataview
# AI関連のブックマーク
TABLE file.name as "タイトル", file.folder as "日付"
FROM "bookmarks"
WHERE file.name != "index" AND tags = "#AI"
SORT file.folder DESC
```

```dataview
# Python関連の最新記事
TABLE file.name as "タイトル", tags as "タグ"
FROM "bookmarks"
WHERE file.name != "index" AND tags = "#Python"
SORT file.folder DESC
LIMIT 10
```

## 🔧 カスタマイズ

### タグ生成の調整

`_scripts/tag_generator.py`の`generate_tags_with_openai`メソッドで、タグ生成のプロンプトを調整できます。

### 新規フォルダの検出

`_scripts/process_new_folders.py`の`find_new_bookmark_folders`メソッドで、フォルダ検出の条件を調整できます。

## 📝 ログ

処理状況は`log.md`に記録されます。また、以下のファイルも生成されます：

- `bookmark_tags_cache.json` - タグ生成のキャッシュ
- `processed_folders.json` - 処理済みフォルダの記録

## ⚠️ 注意事項

1. **OpenAI API使用料**: タグ生成にはOpenAI APIを使用するため、使用料が発生します
2. **API制限**: OpenAI APIの制限に注意してください
3. **キャッシュ**: 一度生成したタグはキャッシュされるため、再処理時は高速です

## 🤝 貢献

バグ報告や機能要望は、プロジェクトログに記載してください。

## 📄 ライセンス

このプロジェクトはMITライセンスの下で公開されています。 