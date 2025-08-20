#!/usr/bin/env python3
"""
ブックマークファイルプロパティ追加スクリプト

目的: 各ブックマークファイルのYAMLフロントマターに「既読・整理済み: false」プロパティを追加する

使用方法:
  python _scripts/add_read_property.py --list                    # 利用可能なディレクトリを表示
  python _scripts/add_read_property.py -d <ディレクトリ名>        # 指定ディレクトリのみ処理
  python _scripts/add_read_property.py --all                    # 全ディレクトリを処理
  python _scripts/add_read_property.py --dry-run                # ドライラン（実際の変更なし）
"""

import os
import re
import sys
import argparse
from pathlib import Path
from typing import List, Dict, Tuple, Optional


class ReadPropertyAdder:
    """ブックマークファイルに「既読・整理済み」プロパティを追加するクラス"""

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
        
        # 統計情報
        self.stats = {
            "processed": 0,
            "modified": 0,
            "skipped": 0,
            "errors": 0
        }

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
            if file.is_file():
                markdown_files.append(file)
        
        return sorted(markdown_files)

    def parse_frontmatter(self, content: str) -> Tuple[Optional[str], str]:
        """
        Markdownファイルからフロントマターを抽出
        
        Args:
            content: ファイルの内容
            
        Returns:
            (フロントマター, 本文) のタプル。フロントマターがない場合はNone
        """
        # YAMLフロントマターの正規表現パターン
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
        # 既読・整理済みプロパティの存在をチェック
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
            
            # tagsセクションの開始を検出
            if line.strip() == 'tags:':
                tags_section_found = True
                continue
            
            # tagsセクション中で、次のプロパティまたは空行を検出
            if tags_section_found and not tags_section_ended:
                stripped_line = line.strip()
                
                # タグリストの項目でない場合（次のプロパティまたは空行）
                if not stripped_line.startswith('- ') and stripped_line != '':
                    # tagsセクション終了、プロパティを追加
                    new_lines.insert(-1, f"{self.property_key}: {self.property_value}")
                    tags_section_ended = True
        
        # tagsセクションが見つかったが最後まで続いていた場合
        if tags_section_found and not tags_section_ended:
            new_lines.append(f"{self.property_key}: {self.property_value}")
        
        # tagsセクションが見つからなかった場合、フロントマターの最後に追加
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

    def process_file(self, file_path: Path) -> bool:
        """
        単一のMarkdownファイルを処理
        
        Args:
            file_path: 処理対象ファイルのパス
            
        Returns:
            ファイルが変更された場合True
        """
        try:
            # ファイル読み込み
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            self.stats["processed"] += 1
            
            # フロントマターを解析
            frontmatter, body = self.parse_frontmatter(content)
            
            if frontmatter is None:
                # フロントマターが存在しない場合は新規作成
                new_frontmatter = self.create_frontmatter_if_missing()
                new_content = f"---\n{new_frontmatter}\n---\n{content}"
                
                print(f"  新規フロントマター作成: {file_path.name}")
            else:
                # 既存プロパティの存在確認
                if self.check_property_exists(frontmatter):
                    print(f"  スキップ（プロパティ既存）: {file_path.name}")
                    self.stats["skipped"] += 1
                    return False
                
                # プロパティを追加
                new_frontmatter = self.add_property_to_frontmatter(frontmatter)
                new_content = f"---\n{new_frontmatter}\n---\n{body}"
                
                print(f"  プロパティ追加: {file_path.name}")
            
            # ドライランモードでない場合のみファイルを更新
            if not self.dry_run:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
            
            self.stats["modified"] += 1
            return True
            
        except Exception as e:
            print(f"  エラー: {file_path.name} - {str(e)}")
            self.stats["errors"] += 1
            return False

    def process_directory(self, directory: Path) -> None:
        """
        指定ディレクトリ内の全Markdownファイルを処理
        
        Args:
            directory: 処理対象ディレクトリ
        """
        print(f"\n📁 ディレクトリ処理中: {directory.name}")
        
        markdown_files = self.find_markdown_files(directory)
        if not markdown_files:
            print("  Markdownファイルが見つかりません")
            return
        
        print(f"  対象ファイル数: {len(markdown_files)}")
        
        for file_path in markdown_files:
            self.process_file(file_path)

    def process_all_directories(self) -> None:
        """全ブックマークディレクトリを処理"""
        directories = self.find_bookmark_directories()
        
        if not directories:
            print("処理対象のディレクトリが見つかりません")
            return
        
        print(f"📊 処理対象ディレクトリ数: {len(directories)}")
        
        for directory in directories:
            self.process_directory(directory)

    def process_specific_directory(self, target_dir: str) -> None:
        """
        指定されたディレクトリのみを処理
        
        Args:
            target_dir: 処理対象ディレクトリ名
        """
        # パスの解析（絶対パス、相対パス、またはディレクトリ名のみ）
        target_path = Path(target_dir)
        
        # 絶対パスでない場合の処理
        if not target_path.is_absolute():
            # スラッシュを含む場合は相対パスとして扱う
            if '/' in target_dir or '\\' in target_dir:
                # そのまま相対パスとして使用
                target_path = Path(target_dir)
            else:
                # ディレクトリ名のみの場合はbookmarksディレクトリ下として扱う
                target_path = self.bookmarks_dir / target_dir
        
        if not target_path.exists():
            print(f"エラー: 指定されたディレクトリが見つかりません: {target_path}")
            return
        
        if not target_path.is_dir():
            print(f"エラー: 指定されたパスはディレクトリではありません: {target_path}")
            return
        
        self.process_directory(target_path)

    def list_directories(self) -> None:
        """利用可能なブックマークディレクトリを一覧表示"""
        directories = self.find_bookmark_directories()
        
        if not directories:
            print("ブックマークディレクトリが見つかりません")
            return
        
        print("📂 利用可能なブックマークディレクトリ:")
        for i, directory in enumerate(directories, 1):
            markdown_count = len(self.find_markdown_files(directory))
            print(f"  {i:2d}. {directory.name} ({markdown_count} files)")

    def print_summary(self) -> None:
        """処理結果のサマリーを表示"""
        print("\n" + "="*50)
        print("📊 処理結果サマリー")
        print("="*50)
        print(f"処理ファイル数: {self.stats['processed']}")
        print(f"変更ファイル数: {self.stats['modified']}")
        print(f"スキップ数:     {self.stats['skipped']}")
        print(f"エラー数:       {self.stats['errors']}")
        
        if self.dry_run:
            print("\n⚠️ ドライランモードで実行されました（実際の変更は行われていません）")


def main():
    """メイン関数"""
    parser = argparse.ArgumentParser(
        description="ブックマークファイルに「既読・整理済み」プロパティを追加",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用例:
  %(prog)s --list                    # 利用可能なディレクトリを表示
  %(prog)s -d x-bookmarks-2025-07-29  # 指定ディレクトリのみ処理
  %(prog)s --all                     # 全ディレクトリを処理
  %(prog)s --all --dry-run           # ドライラン（変更なし）
        """
    )
    
    parser.add_argument(
        '--list', 
        action='store_true',
        help='利用可能なブックマークディレクトリを一覧表示'
    )
    
    parser.add_argument(
        '-d', '--directory',
        type=str,
        help='処理対象のディレクトリ名を指定'
    )
    
    parser.add_argument(
        '--all',
        action='store_true',
        help='全ブックマークディレクトリを処理'
    )
    
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='ドライラン（実際の変更は行わない）'
    )
    
    args = parser.parse_args()
    
    # 引数の検証
    action_count = sum([
        args.list,
        bool(args.directory),
        args.all
    ])
    
    if action_count == 0:
        parser.print_help()
        sys.exit(1)
    
    if action_count > 1:
        print("エラー: --list, --directory, --all のうち1つだけを指定してください")
        sys.exit(1)
    
    # プロパティ追加処理の実行
    adder = ReadPropertyAdder(dry_run=args.dry_run)
    
    try:
        if args.list:
            adder.list_directories()
        elif args.directory:
            adder.process_specific_directory(args.directory)
            adder.print_summary()
        elif args.all:
            adder.process_all_directories()
            adder.print_summary()
    
    except KeyboardInterrupt:
        print("\n\n⚠️ 処理が中断されました")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ 予期しないエラーが発生しました: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
