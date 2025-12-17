#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ブックマーク管理統合スクリプト

すべてのブックマーク処理機能を統合したメインスクリプトです。
タグ生成、プロパティ追加、フッター追加、重複タグ削除などの機能を提供します。

使用方法:
  python bookmark_manager.py --help                    # ヘルプ表示
  python bookmark_manager.py --list                    # 利用可能なディレクトリを表示
  python bookmark_manager.py process -d <ディレクトリ>  # 指定ディレクトリを処理（全機能）
  python bookmark_manager.py process --all            # 全ディレクトリを処理
  python bookmark_manager.py tags -d <ディレクトリ>    # タグ生成のみ
  python bookmark_manager.py property -d <ディレクトリ> # プロパティ追加のみ
  python bookmark_manager.py footer -d <ディレクトリ>  # フッター追加のみ
  python bookmark_manager.py dedup -d <ディレクトリ>  # 重複タグ削除のみ
"""

import os
import re
import sys
import json
import argparse
from pathlib import Path
from typing import List, Dict, Tuple, Optional
from datetime import datetime

# 親ディレクトリをパスに追加
sys.path.insert(0, str(Path(__file__).parent))

try:
    import openai
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False


class BookmarkManager:
    """ブックマーク管理統合クラス"""
    
    def __init__(self, bookmarks_dir: str = "bookmarks", dry_run: bool = False):
        """
        初期化
        
        Args:
            bookmarks_dir: ブックマークディレクトリのパス
            dry_run: ドライランモード（True時は実際の変更を行わない）
        """
        self.bookmarks_dir = Path(bookmarks_dir)
        self.dry_run = dry_run
        self.property_key = "既読・整理済み"
        self.property_value = "false"
        self.footer_template_file = "_templates/footer_template.md"
        
        # 統計情報
        self.stats = {
            "processed": 0,
            "modified": 0,
            "skipped": 0,
            "errors": 0
        }
    
    # ==================== ディレクトリ操作 ====================
    
    def find_bookmark_directories(self) -> List[Path]:
        """
        ブックマークディレクトリ内のサブディレクトリを検索
        
        Returns:
            ブックマークディレクトリのリスト
        """
        if not self.bookmarks_dir.exists():
            print(f"エラー: ブックマークディレクトリが見つかりません: {self.bookmarks_dir}")
            return []
        
        directories = []
        for item in self.bookmarks_dir.iterdir():
            if item.is_dir() and not item.name.startswith('.'):
                directories.append(item)
        
        return sorted(directories)
    
    def find_markdown_files(self, directory: Path) -> List[Path]:
        """
        指定ディレクトリ内の.mdファイルを検索
        
        Args:
            directory: 検索対象ディレクトリ
            
        Returns:
            Markdownファイルのリスト
        """
        markdown_files = []
        for file in directory.glob("*.md"):
            if file.is_file() and file.name != "index.md":
                markdown_files.append(file)
        
        return sorted(markdown_files)
    
    def list_directories(self) -> None:
        """利用可能なブックマークディレクトリを一覧表示"""
        directories = self.find_bookmark_directories()
        
        if not directories:
            print("ブックマークディレクトリが見つかりません")
            return
        
        print("[利用可能なブックマークディレクトリ]:")
        for i, directory in enumerate(directories, 1):
            markdown_count = len(self.find_markdown_files(directory))
            print(f"  {i:2d}. {directory.name} ({markdown_count} files)")
    
    # ==================== プロパティ追加機能 ====================
    
    def parse_frontmatter(self, content: str) -> Tuple[Optional[str], str]:
        """
        Markdownファイルからフロントマターを抽出
        
        Args:
            content: ファイルの内容
            
        Returns:
            (フロントマター, 本文) のタプル。フロントマターがない場合はNone
        """
        frontmatter_pattern = r'^---\s*\n(.*?)\n---\s*\n(.*)'
        match = re.match(frontmatter_pattern, content, re.DOTALL)
        if match:
            frontmatter = match.group(1)
            body = match.group(2)
            return frontmatter, body
        
        return None, content
    
    def check_property_exists(self, frontmatter: str) -> bool:
        """
        フロントマターに既読・整理済みプロパティが既に存在するかチェック
        
        Args:
            frontmatter: YAMLフロントマターの内容
            
        Returns:
            プロパティが存在する場合True
        """
        property_pattern = rf'^{re.escape(self.property_key)}\s*:'
        
        for line in frontmatter.split('\n'):
            if re.match(property_pattern, line.strip()):
                return True
        
        return False
    
    def add_property_to_frontmatter(self, frontmatter: str) -> str:
        """
        フロントマターに「既読・整理済み」プロパティを追加
        
        Args:
            frontmatter: 既存のYAMLフロントマター
            
        Returns:
            プロパティが追加された新しいフロントマター
        """
        lines = frontmatter.split('\n')
        new_lines = []
        
        tags_section_found = False
        tags_section_ended = False
        
        for line in lines:
            new_lines.append(line)
            
            if line.strip() == 'tags:':
                tags_section_found = True
                continue
            
            if tags_section_found and not tags_section_ended:
                stripped_line = line.strip()
                
                if not stripped_line.startswith('- ') and stripped_line != '':
                    new_lines.insert(-1, f"{self.property_key}: {self.property_value}")
                    tags_section_ended = True
        
        if tags_section_found and not tags_section_ended:
            new_lines.append(f"{self.property_key}: {self.property_value}")
        
        if not tags_section_found:
            new_lines.append(f"{self.property_key}: {self.property_value}")
        
        return '\n'.join(new_lines)
    
    def create_frontmatter_if_missing(self) -> str:
        """
        フロントマターが存在しない場合の新規作成
        
        Returns:
            新しいフロントマター
        """
        return f"tags:\n{self.property_key}: {self.property_value}"
    
    def add_property_to_file(self, file_path: Path) -> bool:
        """
        単一のMarkdownファイルにプロパティを追加
        
        Args:
            file_path: 処理対象ファイルのパス
            
        Returns:
            ファイルが変更された場合True
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            self.stats["processed"] += 1
            
            frontmatter, body = self.parse_frontmatter(content)
            
            if frontmatter is None:
                new_frontmatter = self.create_frontmatter_if_missing()
                new_content = f"---\n{new_frontmatter}\n---\n{content}"
            else:
                if self.check_property_exists(frontmatter):
                    self.stats["skipped"] += 1
                    return False
                
                new_frontmatter = self.add_property_to_frontmatter(frontmatter)
                new_content = f"---\n{new_frontmatter}\n---\n{body}"
            
            if not self.dry_run:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
            
            self.stats["modified"] += 1
            return True
            
        except Exception as e:
            print(f"  エラー: {file_path.name} - {str(e)}")
            self.stats["errors"] += 1
            return False
    
    def add_property_to_directory(self, directory: Path) -> None:
        """指定ディレクトリ内の全Markdownファイルにプロパティを追加"""
        print(f"\n[プロパティ追加中]: {directory.name}")
        
        markdown_files = self.find_markdown_files(directory)
        if not markdown_files:
            print("  Markdownファイルが見つかりません")
            return
        
        print(f"  対象ファイル数: {len(markdown_files)}")
        
        for file_path in markdown_files:
            self.add_property_to_file(file_path)
    
    # ==================== フッター追加機能 ====================
    
    def load_footer_template(self) -> str:
        """フッターテンプレートを読み込み"""
        try:
            if os.path.exists(self.footer_template_file):
                with open(self.footer_template_file, 'r', encoding='utf-8') as f:
                    template = f.read().strip()
                    current_time = datetime.now().strftime('%m/%d/%Y, %I:%M:%S %p')
                    return template.replace('{export_date}', current_time)
            else:
                print(f"警告: フッターテンプレートファイルが見つかりません: {self.footer_template_file}")
                return ""
        except Exception as e:
            print(f"フッターテンプレート読み込みエラー: {e}")
            return ""
    
    def add_footer_to_file(self, file_path: Path) -> bool:
        """
        単一のMarkdownファイルにフッターを追加
        
        Args:
            file_path: 処理対象ファイルのパス
            
        Returns:
            ファイルが変更された場合True
        """
        try:
            footer_template = self.load_footer_template()
            if not footer_template:
                return False
            
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            if "*Exported at:" in content:
                return False
            
            if content.strip():
                if not content.endswith('\n'):
                    content += '\n'
                content += '\n' + footer_template
            else:
                content = footer_template
            
            if not self.dry_run:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
            
            return True
            
        except Exception as e:
            print(f"  エラー: {file_path.name} - {str(e)}")
            return False
    
    def add_footer_to_directory(self, directory: Path) -> None:
        """指定ディレクトリ内の全Markdownファイルにフッターを追加"""
        print(f"\n[フッター追加中]: {directory.name}")
        
        markdown_files = self.find_markdown_files(directory)
        if not markdown_files:
            print("  Markdownファイルが見つかりません")
            return
        
        processed_count = 0
        skipped_count = 0
        error_count = 0
        
        print(f"  対象ファイル数: {len(markdown_files)}")
        
        for md_file in markdown_files:
            if self.add_footer_to_file(md_file):
                processed_count += 1
            else:
                skipped_count += 1
        
        print(f"  フッター追加完了: 処理 {processed_count} / スキップ {skipped_count}")
    
    # ==================== 重複タグ削除機能 ====================
    
    def remove_duplicate_tags_from_file(self, file_path: Path) -> bool:
        """
        単一のMarkdownファイルから重複タグを削除
        
        Args:
            file_path: 処理対象ファイルのパス
            
        Returns:
            ファイルが変更された場合True
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            tags_match = re.search(r'^tags:\s*\n((?:  - .+\n?)+)', content, re.MULTILINE)
            if not tags_match:
                return False
            
            tags_section = tags_match.group(1)
            tags = [tag.strip() for tag in tags_section.split('\n') if tag.strip()]
            
            unique_tags = []
            seen = set()
            for tag in tags:
                if tag not in seen:
                    unique_tags.append(tag)
                    seen.add(tag)
            
            if len(unique_tags) == len(tags):
                return False
            
            new_tags_section = '\n'.join(unique_tags) + '\n'
            
            new_content = re.sub(
                r'^tags:\s*\n((?:  - .+\n?)+)',
                f'tags:\n{new_tags_section}',
                content,
                flags=re.MULTILINE
            )
            
            if not self.dry_run:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
            
            return True
            
        except Exception as e:
            print(f"  エラー: {file_path.name} - {str(e)}")
            return False
    
    def remove_duplicate_tags_from_directory(self, directory: Path) -> None:
        """指定ディレクトリ内の全Markdownファイルから重複タグを削除"""
        print(f"\n[重複タグ削除中]: {directory.name}")
        
        markdown_files = self.find_markdown_files(directory)
        if not markdown_files:
            print("  Markdownファイルが見つかりません")
            return
        
        processed_count = 0
        skipped_count = 0
        
        print(f"  対象ファイル数: {len(markdown_files)}")
        
        for md_file in markdown_files:
            if self.remove_duplicate_tags_from_file(md_file):
                processed_count += 1
            else:
                skipped_count += 1
        
        print(f"  重複タグ削除完了: 変更 {processed_count} / スキップ {skipped_count}")
    
    # ==================== 手動タグ追加機能 ====================
    
    def extract_tags_from_content(self, filename: str, content: str) -> List[str]:
        """
        ファイル名と内容からタグを抽出（キーワードベース）
        
        Args:
            filename: ファイル名
            content: ファイルの内容
            
        Returns:
            抽出されたタグのリスト
        """
        tags = []
        filename_lower = filename.lower()
        
        # 教育・子育て関連
        if any(keyword in filename for keyword in ['子ども', '子供', '幼児', '子育て', '教育', '読み聞かせ', '絵本', '父親', '母親', '発達', '謝罪', '仲直り', '信頼', '読書']):
            tags.extend(['教育', '子育て'])
            if '読み聞かせ' in filename or '絵本' in filename:
                tags.extend(['絵本', '読み聞かせ', '幼児教育'])
            if '父親' in filename or '母親' in filename:
                tags.append('親子関係')
            if '発達' in filename:
                tags.append('子どもの発達')
            if '研究' in filename or '研究' in content[:500]:
                tags.append('研究')
            if '心理学' in filename or '心理' in content[:500]:
                tags.append('心理学')
        
        # AI・機械学習関連
        if any(keyword in filename_lower for keyword in ['ai', 'llm', 'gpt', 'gemini', 'claude', 'rag', 'ocr', '機械学習', 'deepseek']):
            tags.append('AI')
            if 'rag' in filename_lower:
                tags.extend(['RAG', '機械学習'])
            if 'ocr' in filename_lower:
                tags.extend(['OCR', '画像認識'])
            if 'llm' in filename_lower or 'gpt' in filename_lower or 'gemini' in filename_lower:
                tags.append('LLM')
            if 'エージェント' in filename or 'agent' in filename_lower:
                tags.append('エージェント')
        
        # プログラミング・開発ツール関連
        if any(keyword in filename_lower for keyword in ['cursor', 'vscode', 'python', 'github', 'git', 'obsidian', 'mcp', 'webdriver']):
            tags.append('プログラミング')
            if 'cursor' in filename_lower:
                tags.extend(['Cursor', '開発ツール'])
            if 'github' in filename_lower or 'git' in filename_lower:
                tags.extend(['GitHub', '開発'])
            if 'obsidian' in filename_lower:
                tags.append('Obsidian')
            if 'python' in filename_lower:
                tags.append('Python')
            if 'mcp' in filename_lower:
                tags.append('MCP')
        
        # ハードウェア・組み込み関連
        if any(keyword in filename_lower for keyword in ['arduino', 'esp32', 'm5stack', 'raspberry', 'psram', 'sram']):
            tags.extend(['ハードウェア', '組み込み開発'])
            if 'arduino' in filename_lower or 'esp32' in filename_lower:
                tags.extend(['Arduino', 'ESP32'])
            if 'm5stack' in filename_lower:
                tags.append('M5Stack')
            if 'raspberry' in filename_lower:
                tags.append('Raspberry Pi')
        
        # 論文・研究関連
        if any(keyword in filename for keyword in ['論文', '研究', '査読', '投稿', '執筆', '学会', '発表', '先行研究', 'phd', 'arxiv']):
            tags.extend(['論文', '研究'])
            if '査読' in filename or '投稿' in filename:
                tags.extend(['査読', '投稿'])
            if '執筆' in filename:
                tags.append('執筆')
            if '学会' in filename or '発表' in filename:
                tags.append('学会発表')
            if 'arxiv' in filename_lower:
                tags.append('arXiv')
        
        # データサイエンス関連
        if any(keyword in filename_lower for keyword in ['pytorch', 'torchvision', 'opencv', 'pandas', 'データ', '統計', '相関係数']):
            tags.append('データサイエンス')
            if 'pytorch' in filename_lower:
                tags.append('PyTorch')
            if '統計' in filename:
                tags.append('統計')
        
        # その他のカテゴリ
        if 'pdf' in filename_lower or 'pdf' in content[:200].lower():
            tags.append('PDF')
        if 'スライド' in filename or 'presentation' in filename_lower:
            tags.append('プレゼンテーション')
        if 'デザイン' in filename or 'design' in filename_lower:
            tags.append('デザイン')
        if 'ツール' in filename or 'tool' in filename_lower:
            tags.append('ツール')
        if '記事' in filename or 'article' in filename_lower:
            tags.append('記事')
        
        return list(dict.fromkeys(tags))  # 重複削除
    
    def add_manual_tags_to_file(self, file_path: Path) -> bool:
        """
        単一のMarkdownファイルに手動タグを追加（キーワードベース）
        
        Args:
            file_path: 処理対象ファイルのパス
            
        Returns:
            ファイルが変更された場合True
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # タグが空かチェック
            if not re.search(r'^tags:\s*$', content, re.MULTILINE):
                return False
            
            # タグを抽出
            tags = self.extract_tags_from_content(file_path.name, content)
            
            if not tags:
                return False
            
            # タグを追加
            tags_yaml = '\n'.join([f'  - {tag}' for tag in tags])
            new_content = re.sub(
                r'^tags:\s*$',
                f'tags:\n{tags_yaml}',
                content,
                flags=re.MULTILINE
            )
            
            if not self.dry_run:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
            
            return True
            
        except Exception as e:
            print(f"  エラー: {file_path.name} - {str(e)}")
            return False
    
    def add_manual_tags_to_directory(self, directory: Path) -> None:
        """指定ディレクトリ内の全Markdownファイルに手動タグを追加"""
        print(f"\n[手動タグ追加中]: {directory.name}")
        
        markdown_files = self.find_markdown_files(directory)
        if not markdown_files:
            print("  Markdownファイルが見つかりません")
            return
        
        processed_count = 0
        skipped_count = 0
        
        print(f"  対象ファイル数: {len(markdown_files)}")
        
        for md_file in markdown_files:
            if self.add_manual_tags_to_file(md_file):
                processed_count += 1
            else:
                skipped_count += 1
        
        print(f"  手動タグ追加完了: 追加 {processed_count} / スキップ {skipped_count}")
    
    # ==================== 統合処理機能 ====================
    
    def process_directory(self, directory: Path, 
                         add_property: bool = True,
                         add_footer: bool = True,
                         remove_duplicates: bool = True) -> None:
        """
        指定ディレクトリを統合処理
        
        Args:
            directory: 処理対象ディレクトリ
            add_property: プロパティ追加を実行するか
            add_footer: フッター追加を実行するか
            remove_duplicates: 重複タグ削除を実行するか
        """
        print(f"\n=== {directory.name} を処理中 ===")
        
        if add_property:
            self.add_property_to_directory(directory)
        
        if add_footer:
            self.add_footer_to_directory(directory)
        
        if remove_duplicates:
            self.remove_duplicate_tags_from_directory(directory)
        
        print(f"\n=== {directory.name} 処理完了 ===")
    
    def process_all_directories(self,
                                add_property: bool = True,
                                add_footer: bool = True,
                                remove_duplicates: bool = True) -> None:
        """全ブックマークディレクトリを統合処理"""
        directories = self.find_bookmark_directories()
        
        if not directories:
            print("処理対象のディレクトリが見つかりません")
            return
        
        print(f"[処理対象ディレクトリ数]: {len(directories)}")
        
        for directory in directories:
            self.process_directory(directory, add_property, add_footer, remove_duplicates)
    
    def process_specific_directory(self, target_dir: str,
                                  add_property: bool = True,
                                  add_footer: bool = True,
                                  remove_duplicates: bool = True) -> None:
        """
        指定されたディレクトリのみを処理
        
        Args:
            target_dir: 処理対象ディレクトリ名
            add_property: プロパティ追加を実行するか
            add_footer: フッター追加を実行するか
            remove_duplicates: 重複タグ削除を実行するか
        """
        target_path = Path(target_dir)
        
        if not target_path.is_absolute():
            if '/' in target_dir or '\\' in target_dir:
                target_path = Path(target_dir)
            else:
                target_path = self.bookmarks_dir / target_dir
        
        if not target_path.exists():
            print(f"エラー: 指定されたディレクトリが見つかりません: {target_path}")
            return
        
        if not target_path.is_dir():
            print(f"エラー: 指定されたパスはディレクトリではありません: {target_path}")
            return
        
        self.process_directory(target_path, add_property, add_footer, remove_duplicates)
    
    def print_summary(self) -> None:
        """処理結果のサマリーを表示"""
        print("\n" + "="*50)
        print("[処理結果サマリー]")
        print("="*50)
        print(f"処理ファイル数: {self.stats['processed']}")
        print(f"変更ファイル数: {self.stats['modified']}")
        print(f"スキップ数:     {self.stats['skipped']}")
        print(f"エラー数:       {self.stats['errors']}")
        
        if self.dry_run:
            print("\n[警告] ドライランモードで実行されました（実際の変更は行われていません）")


def main():
    """メイン関数"""
    parser = argparse.ArgumentParser(
        description="ブックマーク管理統合スクリプト",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用例:
  %(prog)s --list                              # 利用可能なディレクトリを表示
  %(prog)s process -d x-bookmarks-2025-12-15   # 指定ディレクトリを処理（全機能）
  %(prog)s process --all                       # 全ディレクトリを処理
  %(prog)s property -d x-bookmarks-2025-12-15  # プロパティ追加のみ
  %(prog)s footer -d x-bookmarks-2025-12-15    # フッター追加のみ
  %(prog)s dedup -d x-bookmarks-2025-12-15     # 重複タグ削除のみ
  %(prog)s tags-manual -d x-bookmarks-2025-12-15  # 手動タグ追加のみ
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='実行するコマンド')
    
    # 共通引数
    def add_common_args(subparser):
        subparser.add_argument('-d', '--directory', type=str, help='処理対象のディレクトリ名')
        subparser.add_argument('--all', action='store_true', help='全ブックマークディレクトリを処理')
        subparser.add_argument('--dry-run', action='store_true', help='ドライラン（実際の変更は行わない）')
    
    # list コマンド
    list_parser = subparsers.add_parser('list', help='利用可能なディレクトリを一覧表示')
    
    # process コマンド（統合処理）
    process_parser = subparsers.add_parser('process', help='統合処理（プロパティ追加、フッター追加、重複タグ削除）')
    add_common_args(process_parser)
    process_parser.add_argument('--no-property', action='store_true', help='プロパティ追加をスキップ')
    process_parser.add_argument('--no-footer', action='store_true', help='フッター追加をスキップ')
    process_parser.add_argument('--no-dedup', action='store_true', help='重複タグ削除をスキップ')
    
    # property コマンド
    property_parser = subparsers.add_parser('property', help='プロパティ追加のみ実行')
    add_common_args(property_parser)
    
    # footer コマンド
    footer_parser = subparsers.add_parser('footer', help='フッター追加のみ実行')
    add_common_args(footer_parser)
    
    # dedup コマンド
    dedup_parser = subparsers.add_parser('dedup', help='重複タグ削除のみ実行')
    add_common_args(dedup_parser)
    
    # tags-manual コマンド
    tags_manual_parser = subparsers.add_parser('tags-manual', help='手動タグ追加のみ実行（キーワードベース）')
    add_common_args(tags_manual_parser)
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    # マネージャーを初期化
    dry_run = getattr(args, 'dry_run', False)
    manager = BookmarkManager(dry_run=dry_run)
    
    try:
        if args.command == 'list':
            manager.list_directories()
        
        elif args.command == 'process':
            action_count = sum([bool(args.directory), args.all])
            if action_count == 0:
                print("エラー: --directory または --all を指定してください")
                sys.exit(1)
            if action_count > 1:
                print("エラー: --directory と --all は同時に指定できません")
                sys.exit(1)
            
            add_property = not args.no_property
            add_footer = not args.no_footer
            remove_duplicates = not args.no_dedup
            
            if args.all:
                manager.process_all_directories(add_property, add_footer, remove_duplicates)
            else:
                manager.process_specific_directory(args.directory, add_property, add_footer, remove_duplicates)
            manager.print_summary()
        
        elif args.command == 'property':
            action_count = sum([bool(args.directory), args.all])
            if action_count == 0:
                print("エラー: --directory または --all を指定してください")
                sys.exit(1)
            if action_count > 1:
                print("エラー: --directory と --all は同時に指定できません")
                sys.exit(1)
            
            if args.all:
                manager.process_all_directories(add_property=True, add_footer=False, remove_duplicates=False)
            else:
                manager.process_specific_directory(args.directory, add_property=True, add_footer=False, remove_duplicates=False)
            manager.print_summary()
        
        elif args.command == 'footer':
            action_count = sum([bool(args.directory), args.all])
            if action_count == 0:
                print("エラー: --directory または --all を指定してください")
                sys.exit(1)
            if action_count > 1:
                print("エラー: --directory と --all は同時に指定できません")
                sys.exit(1)
            
            directories = manager.find_bookmark_directories() if args.all else [manager.bookmarks_dir / args.directory]
            for directory in directories:
                manager.add_footer_to_directory(directory)
        
        elif args.command == 'dedup':
            action_count = sum([bool(args.directory), args.all])
            if action_count == 0:
                print("エラー: --directory または --all を指定してください")
                sys.exit(1)
            if action_count > 1:
                print("エラー: --directory と --all は同時に指定できません")
                sys.exit(1)
            
            directories = manager.find_bookmark_directories() if args.all else [manager.bookmarks_dir / args.directory]
            for directory in directories:
                manager.remove_duplicate_tags_from_directory(directory)
        
        elif args.command == 'tags-manual':
            action_count = sum([bool(args.directory), args.all])
            if action_count == 0:
                print("エラー: --directory または --all を指定してください")
                sys.exit(1)
            if action_count > 1:
                print("エラー: --directory と --all は同時に指定できません")
                sys.exit(1)
            
            directories = manager.find_bookmark_directories() if args.all else [manager.bookmarks_dir / args.directory]
            for directory in directories:
                manager.add_manual_tags_to_directory(directory)
    
    except KeyboardInterrupt:
        print("\n\n[警告] 処理が中断されました")
        sys.exit(1)
    except Exception as e:
        print(f"\n[エラー] 予期しないエラーが発生しました: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()

