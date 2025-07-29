# Xブックマーク管理サマリー

作成日: 2025-07-28
更新日: 2025-07-28

## 📊 統計情報

### 総ブックマーク数
```dataview
TABLE length(rows) as "ブックマーク数"
FROM "bookmarks"
WHERE file.name != "index"
```

### 日付別ブックマーク数
```dataview
TABLE length(rows) as "ブックマーク数"
FROM "bookmarks"
WHERE file.name != "index"
GROUP BY file.folder
SORT file.folder DESC
```

## 🏷️ タグ別表示

### 全タグ一覧
```dataview
TABLE length(rows) as "ブックマーク数"
FROM "bookmarks"
WHERE file.name != "index" AND tags
FLATTEN tags as tag
GROUP BY tag
SORT length(rows) DESC
```

### 分野別タグ
```dataview
TABLE file.name as "タイトル", file.folder as "日付"
FROM "bookmarks"
WHERE file.name != "index" AND (tags = "#AI" OR tags = "#機械学習" OR tags = "#データサイエンス" OR tags = "#Web開発" OR tags = "#プログラミング")
SORT file.folder DESC
```

### 技術スタック別タグ
```dataview
TABLE file.name as "タイトル", file.folder as "日付"
FROM "bookmarks"
WHERE file.name != "index" AND (tags = "#Python" OR tags = "#JavaScript" OR tags = "#Docker" OR tags = "#Git" OR tags = "#Obsidian")
SORT file.folder DESC
```

### 用途別タグ
```dataview
TABLE file.name as "タイトル", file.folder as "日付"
FROM "bookmarks"
WHERE file.name != "index" AND (tags = "#チュートリアル" OR tags = "#ツール" OR tags = "#ライブラリ" OR tags = "#記事" OR tags = "#Tips")
SORT file.folder DESC
```

## 📅 日付別表示

### 最新のブックマーク（最新10件）
```dataview
TABLE file.name as "タイトル", tags as "タグ"
FROM "bookmarks"
WHERE file.name != "index"
SORT file.folder DESC
LIMIT 10
```

### 特定日付のブックマーク
```dataview
TABLE file.name as "タイトル", tags as "タグ"
FROM "bookmarks"
WHERE file.name != "index" AND file.folder = "bookmarks/x-bookmarks-2025-07-23_sikibuton_cover"
SORT file.name
```

## 🔍 検索機能

### キーワード検索
```dataview
TABLE file.name as "タイトル", file.folder as "日付", tags as "タグ"
FROM "bookmarks"
WHERE file.name != "index" AND (file.name CONTAINS "AI" OR file.name CONTAINS "Python" OR file.name CONTAINS "機械学習")
SORT file.folder DESC
```

### 複数タグ検索
```dataview
TABLE file.name as "タイトル", file.folder as "日付"
FROM "bookmarks"
WHERE file.name != "index" AND tags AND (tags = "#AI" AND tags = "#Python")
SORT file.folder DESC
```

## 📈 人気タグ（上位10件）
```dataview
TABLE length(rows) as "ブックマーク数"
FROM "bookmarks"
WHERE file.name != "index" AND tags
FLATTEN tags as tag
GROUP BY tag
SORT length(rows) DESC
LIMIT 10
```

## 🔗 関連リンク

- [[log.md|プロジェクトログ]]
- [[_scripts/tag_generator.py|タグ生成スクリプト]]
- [[_scripts/process_new_folders.py|新規フォルダ処理スクリプト]]

## 📝 使用方法

1. **新規ブックマークフォルダの処理**:
   ```bash
   cd _scripts
   python process_new_folders.py
   ```

2. **既存フォルダの再処理**:
   ```bash
   cd _scripts
   python tag_generator.py
   ```

3. **環境変数の設定**:
   ```powershell
   $env:OPENAI_API_KEY='your-api-key'
   ```

## 🏷️ タグ体系

### 分野タグ
- #AI - 人工知能関連
- #機械学習 - 機械学習関連
- #データサイエンス - データサイエンス関連
- #Web開発 - Web開発関連
- #プログラミング - プログラミング全般

### 技術スタックタグ
- #Python - Python関連
- #JavaScript - JavaScript関連
- #Docker - Docker関連
- #Git - Git関連
- #Obsidian - Obsidian関連

### 用途タグ
- #チュートリアル - チュートリアル記事
- #ツール - ツール紹介
- #ライブラリ - ライブラリ紹介
- #記事 - 一般的な記事
- #Tips - 小技・Tips 