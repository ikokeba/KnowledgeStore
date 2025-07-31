#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Xブックマークタグ自動生成・Obsidianプロパティ形式追加スクリプト

機能:
- OpenAI APIを使用してブックマークコンテンツを分析
- 分野・技術スタック・用途別のタグを自動生成
- 生成されたタグをJSONファイルに保存
- Obsidianプロパティ形式（YAML frontmatter）でタグを追加
- 指定したフォルダのみに対してタグ付けを実行
- 外部リンクがある場合はWaterCrawl APIを使用して要約を取得

作成日: 2025-07-28
作成者: AI Assistant
更新履歴:
- 2025-07-28: 初版作成
- 2025-01-27: コマンドライン引数対応、指定フォルダ処理機能追加
- 2025-01-27: Obsidianプロパティ形式タグ追加機能をマージ
- 2025-01-27: WaterCrawl API統合、外部リンク要約機能追加
"""

import os
import json
import re
import argparse
from pathlib import Path
from typing import Dict, List, Optional
import openai
from datetime import datetime
from watercrawl import WaterCrawlAPIClient

class BookmarkTagGenerator:
    def __init__(self, openai_api_key: str, watercrawl_api_key: str = None):
        """
        タグ生成器の初期化
        
        Args:
            openai_api_key: OpenAI APIキー
            watercrawl_api_key: WaterCrawl APIキー（オプション）
        """
        self.client = openai.OpenAI(api_key=openai_api_key)
        self.watercrawl_api_key = watercrawl_api_key
        if watercrawl_api_key:
            self.watercrawl_client = WaterCrawlAPIClient(api_key=watercrawl_api_key)
        else:
            self.watercrawl_client = None
        self.tags_cache_file = "bookmark_tags_cache.json"
        self.tags_cache = self._load_tags_cache()
        
    def _load_tags_cache(self) -> Dict:
        """タグキャッシュを読み込み"""
        if os.path.exists(self.tags_cache_file):
            try:
                with open(self.tags_cache_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"キャッシュ読み込みエラー: {e}")
        return {}
    
    def _save_tags_cache(self):
        """タグキャッシュを保存"""
        try:
            with open(self.tags_cache_file, 'w', encoding='utf-8') as f:
                json.dump(self.tags_cache, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"キャッシュ保存エラー: {e}")
    
    def extract_external_links(self, content: str) -> List[str]:
        """
        Markdownコンテンツから外部リンクを抽出
        
        Args:
            content: Markdownコンテンツ
            
        Returns:
            外部リンクのリスト
        """
        # Markdownリンク形式を抽出 [text](url)
        markdown_links = re.findall(r'\[([^\]]+)\]\(([^)]+)\)', content)
        
        # プレーンテキストURLを抽出
        url_pattern = r'https?://[^\s\)]+'
        plain_urls = re.findall(url_pattern, content)
        
        external_links = []
        
        # MarkdownリンクからURLを抽出
        for text, url in markdown_links:
            if url.startswith('http'):
                external_links.append(url)
        
        # プレーンテキストURLを追加
        external_links.extend(plain_urls)
        
        # 重複を除去
        external_links = list(set(external_links))
        
        return external_links
    
    def get_watercrawl_summary(self, url: str) -> Optional[str]:
        """
        WaterCrawl APIを使用してURLの要約を取得
        
        Args:
            url: 要約を取得するURL
            
        Returns:
            要約テキスト（エラーの場合はNone）
        """
        if not self.watercrawl_client:
            print(f"WaterCrawl APIキーが設定されていません: {url}")
            return None
        
        try:
            # WaterCrawlクライアントを使用してURLを抽出
            result = self.watercrawl_client.scrape_url(
                url=url,
                page_options=None,
                plugin_options=None,
                sync=True,
                download=True
            )
            
            # 結果から要約を取得
            if result and isinstance(result, dict):
                # メタデータからタイトルを取得
                metadata = result.get('result', {}).get('metadata', {})
                title = metadata.get('title', '')
                
                # Markdownコンテンツから要約を作成
                markdown_content = result.get('result', {}).get('markdown', '')
                if markdown_content:
                    # 最初の500文字を要約として使用
                    summary = markdown_content[:500]
                    if len(markdown_content) > 500:
                        summary += "..."
                    
                    # タイトルと要約を組み合わせ
                    if title:
                        return f"タイトル: {title}\n\n要約: {summary}"
                    else:
                        return summary
                else:
                    print(f"WaterCrawlからMarkdownコンテンツを取得できませんでした: {url}")
                    return None
            else:
                print(f"WaterCrawlから要約を取得できませんでした: {url}")
                return None
                
        except Exception as e:
            print(f"WaterCrawl API 呼び出しエラー: {url} - {e}")
            return None
    
    def add_external_link_summaries(self, file_path: str, external_links: List[str]):
        """
        Markdownファイルに外部リンクの要約を追加
        
        Args:
            file_path: ファイルパス
            external_links: 外部リンクのリスト
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 既存の外部リンク要約セクションを削除
            content = re.sub(r'\n## External Link Summaries.*?(?=\n##|\n---|\Z)', '', content, flags=re.DOTALL)
            
            summaries = []
            for url in external_links:
                print(f"外部リンクの要約を取得中: {url}")
                summary = self.get_watercrawl_summary(url)
                if summary:
                    summaries.append(f"### {url}\n{summary}\n")
                else:
                    summaries.append(f"### {url}\n要約の取得に失敗しました。\n")
            
            if summaries:
                # ファイルの末尾に要約セクションを追加
                summary_section = "\n## External Link Summaries\n\n" + "\n".join(summaries)
                
                # ファイルの末尾の改行を調整
                if content.endswith('\n'):
                    new_content = content + summary_section
                else:
                    new_content = content + '\n' + summary_section
                
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                
                print(f"外部リンク要約を追加しました: {file_path}")
                print(f"処理したリンク数: {len(external_links)}")
            else:
                print(f"外部リンクがありません: {file_path}")
            
        except Exception as e:
            print(f"外部リンク要約追加エラー {file_path}: {e}")
    
    def extract_content_from_markdown(self, file_path: str) -> str:
        """
        Markdownファイルからコンテンツを抽出
        
        Args:
            file_path: Markdownファイルのパス
            
        Returns:
            抽出されたコンテンツ文字列
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # メタデータ部分を除去（---で囲まれた部分）
            content = re.sub(r'^---.*?---', '', content, flags=re.DOTALL)
            
            # リンク部分を除去
            content = re.sub(r'## Links.*', '', content, flags=re.DOTALL)
            
            # 画像部分を除去
            content = re.sub(r'## Images.*', '', content, flags=re.DOTALL)
            
            # 外部リンク要約部分を除去
            content = re.sub(r'## External Link Summaries.*', '', content, flags=re.DOTALL)
            
            # 不要な改行を整理
            content = re.sub(r'\n+', '\n', content)
            
            return content.strip()
            
        except Exception as e:
            print(f"ファイル読み込みエラー {file_path}: {e}")
            return ""
    
    def generate_tags_with_openai(self, content: str, title: str) -> List[str]:
        """
        OpenAI APIを使用してタグを生成
        
        Args:
            content: ブックマークのコンテンツ
            title: ブックマークのタイトル
            
        Returns:
            生成されたタグのリスト
        """
        prompt = f"""
以下のブックマークコンテンツを分析し、分野・技術スタック・用途別のタグを生成してください。

タイトル: {title}
コンテンツ: {content[:1000]}  # 最初の1000文字のみ使用

以下のカテゴリでタグを生成してください：
1. 分野タグ（例: #AI, #機械学習, #Web開発, #データサイエンス）
2. 技術スタックタグ（例: #Python, #JavaScript, #Docker, #Git）
3. 用途タグ（例: #チュートリアル, #ツール, #ライブラリ, #記事）

タグは日本語または英語で、#で始まる形式で返してください。
最大10個のタグを生成し、カンマ区切りで返してください。
例: #AI, #Python, #機械学習, #チュートリアル, #ライブラリ
"""
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "あなたは技術的なコンテンツを分析し、適切なタグを生成する専門家です。"},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=200,
                temperature=0.3
            )
            
            tags_text = response.choices[0].message.content.strip()
            
            # タグを抽出（#で始まる部分）
            tags = re.findall(r'#[^\s,]+', tags_text)
            
            # 重複を除去
            tags = list(set(tags))
            
            return tags[:10]  # 最大10個まで
            
        except Exception as e:
            print(f"OpenAI API エラー: {e}")
            return []
    
    def add_obsidian_tags(self, file_path: str, tags: List[str]):
        """
        MarkdownファイルにObsidianプロパティ形式でタグを追加
        
        Args:
            file_path: ファイルパス
            tags: 追加するタグのリスト
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 既存のタグ行を削除
            content = re.sub(r'^tags:\s*.*\n', '', content, flags=re.MULTILINE)
            content = re.sub(r'\ntags:\s*.*(?:\n|$)', '', content)
            
            # ファイル末尾のタグ行も削除
            content = re.sub(r'\n\s*tags:.*$', '', content, flags=re.MULTILINE)
            
            if tags:
                # Obsidianプロパティ形式のタグを作成
                tags_yaml = "---\ntags:\n"
                for tag in tags:
                    # #を除去してタグ名のみを取得
                    tag_name = tag.replace('#', '').strip()
                    tags_yaml += f"  - {tag_name}\n"
                tags_yaml += "---\n\n"
                
                # ファイルの先頭に挿入
                new_content = tags_yaml + content
                
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                
                print(f"Obsidianタグを追加しました: {file_path}")
                print(f"追加されたタグ: {', '.join(tags)}")
            else:
                print(f"タグがありません: {file_path}")
            
        except Exception as e:
            print(f"タグ追加エラー {file_path}: {e}")
    
    def process_bookmark_file(self, file_path: str) -> List[str]:
        """
        ブックマークファイルを処理してタグを生成・追加
        
        Args:
            file_path: ブックマークファイルのパス
            
        Returns:
            生成されたタグのリスト
        """
        # キャッシュをチェック
        if file_path in self.tags_cache:
            print(f"キャッシュからタグを取得: {file_path}")
            tags = self.tags_cache[file_path]
        else:
            # ファイル名からタイトルを抽出
            file_name = os.path.basename(file_path)
            title = file_name.replace('.md', '').replace('_', ' ')
            
            # コンテンツを抽出
            content = self.extract_content_from_markdown(file_path)
            
            if not content:
                print(f"コンテンツが空です: {file_path}")
                return []
            
            # 外部リンクを抽出
            external_links = self.extract_external_links(content)
            
            # 外部リンクがある場合は要約を追加
            if external_links and self.watercrawl_api_key:
                print(f"外部リンクを検出: {len(external_links)}個")
                self.add_external_link_summaries(file_path, external_links)
            
            # タグを生成
            print(f"タグを生成中: {file_path}")
            tags = self.generate_tags_with_openai(content, title)
            
            # キャッシュに保存
            self.tags_cache[file_path] = tags
            self._save_tags_cache()
        
        # Obsidianプロパティ形式でタグを追加
        if tags:
            self.add_obsidian_tags(file_path, tags)
            print(f"生成されたタグ: {', '.join(tags)}")
        else:
            print("タグが生成されませんでした")
        
        return tags
    
    def process_bookmark_directory(self, directory_path: str):
        """
        ブックマークディレクトリ全体を処理
        
        Args:
            directory_path: ブックマークディレクトリのパス
        """
        directory = Path(directory_path)
        
        if not directory.exists():
            print(f"ディレクトリが存在しません: {directory_path}")
            return
        
        print(f"\n=== {directory_path} を処理中 ===")
        
        # index.md以外のMarkdownファイルを処理
        for md_file in directory.glob("*.md"):
            if md_file.name == "index.md":
                continue
            
            print(f"\n処理中: {md_file}")
            self.process_bookmark_file(str(md_file))
    
    def find_bookmark_directories(self, base_path: str = "bookmarks") -> List[str]:
        """
        bookmarksディレクトリ内のブックマークフォルダを検索
        
        Args:
            base_path: 検索するベースパス
            
        Returns:
            ブックマークディレクトリのリスト
        """
        bookmark_dirs = []
        base_dir = Path(base_path)
        
        if not base_dir.exists():
            print(f"ベースディレクトリが存在しません: {base_path}")
            return bookmark_dirs
        
        # x-bookmarks-で始まるディレクトリを検索
        for item in base_dir.iterdir():
            if item.is_dir() and item.name.startswith("x-bookmarks-"):
                bookmark_dirs.append(str(item))
        
        return sorted(bookmark_dirs)

def main():
    """メイン関数"""
    # コマンドライン引数の解析
    parser = argparse.ArgumentParser(description='Xブックマークタグ自動生成・Obsidianプロパティ形式追加スクリプト')
    parser.add_argument('--directory', '-d', type=str, 
                       help='処理するブックマークディレクトリのパス（例: bookmarks/x-bookmarks-2025-01-27_new）')
    parser.add_argument('--list', '-l', action='store_true',
                       help='利用可能なブックマークディレクトリを一覧表示')
    parser.add_argument('--all', '-a', action='store_true',
                       help='すべてのブックマークディレクトリを処理')
    
    args = parser.parse_args()
    
    # OpenAI APIキーを環境変数から取得
    openai_api_key = os.getenv('OPENAI_API_KEY')
    if not openai_api_key:
        print("エラー: OPENAI_API_KEY環境変数が設定されていません")
        print("使用方法: $env:OPENAI_API_KEY='your-api-key'")
        return
    
    # WaterCrawl APIキーを環境変数から取得
    watercrawl_api_key = os.getenv('WATERCRAWL_API_KEY')
    if not watercrawl_api_key:
        print("警告: WATERCRAWL_API_KEY環境変数が設定されていません")
        print("外部リンク要約機能は無効になります")
        print("使用方法: $env:WATERCRAWL_API_KEY='your-api-key'")
    
    # タグ生成器を初期化
    generator = BookmarkTagGenerator(openai_api_key, watercrawl_api_key)
    
    # 利用可能なディレクトリを取得
    available_dirs = generator.find_bookmark_directories()
    
    if args.list:
        print("利用可能なブックマークディレクトリ:")
        for i, dir_path in enumerate(available_dirs, 1):
            print(f"{i}. {dir_path}")
        return
    
    if args.all:
        # すべてのディレクトリを処理
        if not available_dirs:
            print("処理するブックマークディレクトリが見つかりません")
            return
        
        print(f"すべてのディレクトリを処理します（{len(available_dirs)}個）")
        for directory in available_dirs:
            generator.process_bookmark_directory(directory)
    
    elif args.directory:
        # 指定されたディレクトリを処理
        if not os.path.exists(args.directory):
            print(f"指定されたディレクトリが存在しません: {args.directory}")
            return
        
        generator.process_bookmark_directory(args.directory)
    
    else:
        # 引数が指定されていない場合はヘルプを表示
        print("使用方法:")
        print("  python tag_generator.py --list                    # 利用可能なディレクトリを一覧表示")
        print("  python tag_generator.py --all                     # すべてのディレクトリを処理")
        print("  python tag_generator.py --directory <path>        # 指定したディレクトリのみ処理")
        print("  python tag_generator.py -d bookmarks/x-bookmarks-2025-01-27_new")
        print("\n例:")
        print("  python tag_generator.py --list")
        print("  python tag_generator.py -d bookmarks/x-bookmarks-2025-01-27_new")
        return
    
    print("\n=== 処理完了 ===")

if __name__ == "__main__":
    main() 