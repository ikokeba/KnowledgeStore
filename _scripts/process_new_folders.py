#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
新規ブックマークフォルダ処理スクリプト

機能:
- 新規ブックマークフォルダを検出
- 既存のタグ生成器を使用してタグを付与
- 「既読・整理済み: false」プロパティを自動追加
- 各マークダウンファイルの末尾にフッターテンプレートを追加
- 処理済みフォルダの記録

作成日: 2025-07-28
作成者: AI Assistant
更新履歴:
- 2025-07-28: 初版作成
- 2025-08-20: プロパティ追加機能を統合
- 2025-09-08: フッターテンプレート追加機能を実装
"""

import os
import json
from pathlib import Path
from datetime import datetime
from tag_generator import BookmarkTagGenerator
from add_read_property import ReadPropertyAdder

class NewFolderProcessor:
    def __init__(self, openai_api_key: str):
        """
        新規フォルダ処理器の初期化
        
        Args:
            openai_api_key: OpenAI APIキー
        """
        self.tag_generator = BookmarkTagGenerator(openai_api_key)
        self.property_adder = ReadPropertyAdder()
        self.processed_folders_file = "processed_folders.json"
        self.processed_folders = self._load_processed_folders()
        self.bookmarks_base_dir = "bookmarks"
        self.footer_template_file = "_templates/footer_template.md"
    
    def _load_processed_folders(self) -> set:
        """処理済みフォルダリストを読み込み"""
        if os.path.exists(self.processed_folders_file):
            try:
                with open(self.processed_folders_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    return set(data.get('processed_folders', []))
            except Exception as e:
                print(f"処理済みフォルダ読み込みエラー: {e}")
        return set()
    
    def _save_processed_folders(self):
        """処理済みフォルダリストを保存"""
        try:
            data = {
                'processed_folders': list(self.processed_folders),
                'last_updated': datetime.now().isoformat()
            }
            with open(self.processed_folders_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"処理済みフォルダ保存エラー: {e}")
    
    def find_new_bookmark_folders(self) -> list:
        """
        新規ブックマークフォルダを検出
        
        Returns:
            新規フォルダのパスリスト
        """
        new_folders = []
        bookmarks_dir = Path(self.bookmarks_base_dir)
        
        if not bookmarks_dir.exists():
            print(f"ブックマークディレクトリが存在しません: {self.bookmarks_base_dir}")
            return new_folders
        
        # x-bookmarks-で始まるフォルダを検索
        for folder in bookmarks_dir.glob("x-bookmarks-*"):
            if folder.is_dir() and str(folder) not in self.processed_folders:
                new_folders.append(str(folder))
        
        return new_folders
    
    def process_new_folders(self):
        """新規フォルダを処理"""
        new_folders = self.find_new_bookmark_folders()
        
        if not new_folders:
            print("新規フォルダは見つかりませんでした")
            return
        
        print(f"新規フォルダを発見: {len(new_folders)}個")
        
        for folder in new_folders:
            print(f"\n=== 新規フォルダを処理中: {folder} ===")
            
            try:
                # タグ生成器でフォルダを処理
                print(f"ステップ1: タグ生成中...")
                self.tag_generator.process_bookmark_directory(folder)
                
                # プロパティ追加処理（統計をリセット）
                print(f"ステップ2: 「既読・整理済み」プロパティ追加中...")
                self.property_adder.stats = {"processed": 0, "modified": 0, "skipped": 0, "errors": 0}
                folder_name = Path(folder).name
                self.property_adder.process_specific_directory(folder_name)
                
                # プロパティ追加の統計情報を表示
                stats = self.property_adder.stats
                print(f"  プロパティ追加結果: 変更 {stats['modified']} / スキップ {stats['skipped']} / エラー {stats['errors']}")
                
                # フッター追加処理
                print(f"ステップ3: フッター追加中...")
                self.add_footer_to_markdown_files(folder)
                
                # 処理済みとして記録
                self.processed_folders.add(folder)
                self._save_processed_folders()
                
                print(f"処理完了: {folder}")
                
            except Exception as e:
                print(f"フォルダ処理エラー {folder}: {e}")
    
    def list_all_bookmark_folders(self):
        """全ブックマークフォルダを一覧表示"""
        bookmarks_dir = Path(self.bookmarks_base_dir)
        
        if not bookmarks_dir.exists():
            print(f"ブックマークディレクトリが存在しません: {self.bookmarks_base_dir}")
            return
        
        folders = list(bookmarks_dir.glob("x-bookmarks-*"))
        folders.sort()
        
        print("=== 全ブックマークフォルダ ===")
        for folder in folders:
            status = "✓ 処理済み" if str(folder) in self.processed_folders else "✗ 未処理"
            print(f"{folder.name}: {status}")
    
    def reset_processed_folders(self):
        """処理済みフォルダリストをリセット"""
        self.processed_folders.clear()
        self._save_processed_folders()
        print("処理済みフォルダリストをリセットしました")
    
    def _load_footer_template(self) -> str:
        """フッターテンプレートを読み込み"""
        try:
            if os.path.exists(self.footer_template_file):
                with open(self.footer_template_file, 'r', encoding='utf-8') as f:
                    template = f.read().strip()
                    # 現在の日時でプレースホルダーを置換
                    current_time = datetime.now().strftime('%m/%d/%Y, %I:%M:%S %p')
                    return template.replace('{export_date}', current_time)
            else:
                print(f"警告: フッターテンプレートファイルが見つかりません: {self.footer_template_file}")
                return ""
        except Exception as e:
            print(f"フッターテンプレート読み込みエラー: {e}")
            return ""
    
    def add_footer_to_markdown_files(self, folder_path: str):
        """
        指定フォルダ内の全マークダウンファイルにフッターを追加
        
        Args:
            folder_path: 処理対象フォルダのパス
        """
        footer_template = self._load_footer_template()
        if not footer_template:
            print("フッターテンプレートが空のため、フッター追加をスキップします")
            return
        
        folder = Path(folder_path)
        if not folder.exists():
            print(f"フォルダが存在しません: {folder_path}")
            return
        
        md_files = list(folder.glob("*.md"))
        if not md_files:
            print(f"マークダウンファイルが見つかりません: {folder_path}")
            return
        
        processed_count = 0
        skipped_count = 0
        error_count = 0
        
        print(f"  フッター追加処理開始: {len(md_files)}個のファイル")
        
        for md_file in md_files:
            try:
                # ファイルを読み込み
                with open(md_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # 既にフッターが存在するかチェック
                if "*Exported at:" in content:
                    skipped_count += 1
                    continue
                
                # フッターを追加
                if content.strip():
                    # ファイルの最後に改行を追加してからフッターを追加
                    if not content.endswith('\n'):
                        content += '\n'
                    content += '\n' + footer_template
                else:
                    # 空ファイルの場合はフッターのみ
                    content = footer_template
                
                # ファイルに書き戻し
                with open(md_file, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                processed_count += 1
                
            except Exception as e:
                print(f"    エラー {md_file.name}: {e}")
                error_count += 1
        
        print(f"  フッター追加完了: 処理 {processed_count} / スキップ {skipped_count} / エラー {error_count}")

def main():
    """メイン関数"""
    # OpenAI APIキーを環境変数から取得
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        print("エラー: OPENAI_API_KEY環境変数が設定されていません")
        print("使用方法: $env:OPENAI_API_KEY='your-api-key'")
        return
    
    # 新規フォルダ処理器を初期化
    processor = NewFolderProcessor(api_key)
    
    # 全フォルダを一覧表示
    processor.list_all_bookmark_folders()
    
    # 新規フォルダを処理
    processor.process_new_folders()
    
    print("\n=== 処理完了 ===")

if __name__ == "__main__":
    main() 