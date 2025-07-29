#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Xブックマークタグ自動生成スクリプト

機能:
- OpenAI APIを使用してブックマークコンテンツを分析
- 分野・技術スタック・用途別のタグを自動生成
- 生成されたタグをJSONファイルに保存

作成日: 2025-07-28
作成者: AI Assistant
更新履歴:
- 2025-07-28: 初版作成
"""

import os
import json
import re
from pathlib import Path
from typing import Dict, List, Optional
import openai
from datetime import datetime

class BookmarkTagGenerator:
    def __init__(self, openai_api_key: str):
        """
        タグ生成器の初期化
        
        Args:
            openai_api_key: OpenAI APIキー
        """
        self.client = openai.OpenAI(api_key=openai_api_key)
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
    
    def process_bookmark_file(self, file_path: str) -> List[str]:
        """
        ブックマークファイルを処理してタグを生成
        
        Args:
            file_path: ブックマークファイルのパス
            
        Returns:
            生成されたタグのリスト
        """
        # キャッシュをチェック
        if file_path in self.tags_cache:
            print(f"キャッシュからタグを取得: {file_path}")
            return self.tags_cache[file_path]
        
        # ファイル名からタイトルを抽出
        file_name = os.path.basename(file_path)
        title = file_name.replace('.md', '').replace('_', ' ')
        
        # コンテンツを抽出
        content = self.extract_content_from_markdown(file_path)
        
        if not content:
            print(f"コンテンツが空です: {file_path}")
            return []
        
        # タグを生成
        print(f"タグを生成中: {file_path}")
        tags = self.generate_tags_with_openai(content, title)
        
        # キャッシュに保存
        self.tags_cache[file_path] = tags
        self._save_tags_cache()
        
        return tags
    
    def add_tags_to_markdown(self, file_path: str, tags: List[str]):
        """
        Markdownファイルにタグを追加
        
        Args:
            file_path: ファイルパス
            tags: 追加するタグのリスト
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 既存のタグ行を削除
            content = re.sub(r'^tags:.*\n', '', content, flags=re.MULTILINE)
            
            # タグ行を追加（メタデータの後に）
            if tags:
                tags_line = f"tags: {', '.join(tags)}\n"
                
                # メタデータの後に挿入
                if '---' in content:
                    parts = content.split('---', 2)
                    if len(parts) >= 3:
                        new_content = f"{parts[0]}---{parts[1]}---\n{tags_line}\n{parts[2]}"
                    else:
                        new_content = f"{content}\n{tags_line}"
                else:
                    new_content = f"{tags_line}\n{content}"
                
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                
                print(f"タグを追加しました: {file_path}")
            
        except Exception as e:
            print(f"タグ追加エラー {file_path}: {e}")
    
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
        
        # index.md以外のMarkdownファイルを処理
        for md_file in directory.glob("*.md"):
            if md_file.name == "index.md":
                continue
            
            print(f"\n処理中: {md_file}")
            tags = self.process_bookmark_file(str(md_file))
            
            if tags:
                self.add_tags_to_markdown(str(md_file), tags)
                print(f"生成されたタグ: {', '.join(tags)}")
            else:
                print("タグが生成されませんでした")

def main():
    """メイン関数"""
    # OpenAI APIキーを環境変数から取得
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        print("エラー: OPENAI_API_KEY環境変数が設定されていません")
        print("使用方法: $env:OPENAI_API_KEY='your-api-key'")
        return
    
    # タグ生成器を初期化
    generator = BookmarkTagGenerator(api_key)
    
    # ブックマークディレクトリを処理
    bookmark_dirs = [
        "bookmarks/x-bookmarks-2025-07-23_sikibuton_cover",
        "bookmarks/x-bookmarks-2025-07-23_ikokeba"
    ]
    
    for directory in bookmark_dirs:
        print(f"\n=== {directory} を処理中 ===")
        generator.process_bookmark_directory(directory)
    
    print("\n=== 処理完了 ===")

if __name__ == "__main__":
    main() 