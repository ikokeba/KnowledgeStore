#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
WaterCrawl統合使用例

このスクリプトは、WaterCrawl APIを使用して外部リンクの要約を取得する方法を示します。

使用方法:
1. 環境変数を設定:
   $env:OPENAI_API_KEY='your-openai-api-key'
   $env:WATERCRAWL_API_KEY='your-watercrawl-api-key'

2. スクリプトを実行:
   python example_watercrawl_usage.py

作成日: 2025-01-27
作成者: AI Assistant
"""

import os
import sys
from pathlib import Path

# プロジェクトルートをパスに追加
sys.path.append(str(Path(__file__).parent))

from tag_generator import BookmarkTagGenerator

def example_external_link_extraction():
    """外部リンク抽出の例"""
    print("=== 外部リンク抽出の例 ===")
    
    # テスト用のMarkdownコンテンツ
    test_content = """
    # サンプルブックマーク
    
    これは技術記事のサンプルです。
    
    ## 関連リンク
    
    - [GitHub](https://github.com/example/repo)
    - [公式ドキュメント](https://docs.example.com)
    - [ブログ記事](https://blog.example.com/article)
    
    プレーンテキストURL: https://example.com
    
    ## その他の情報
    
    この記事は技術的な内容を含んでいます。
    """
    
    # タグ生成器のインスタンスを作成（APIキーは不要）
    generator = BookmarkTagGenerator("dummy_key")
    
    # 外部リンクを抽出
    external_links = generator.extract_external_links(test_content)
    
    print("検出された外部リンク:")
    for i, link in enumerate(external_links, 1):
        print(f"{i}. {link}")
    
    return external_links

def example_watercrawl_summary():
    """WaterCrawl要約の例"""
    print("\n=== WaterCrawl要約の例 ===")
    
    # APIキーを確認
    watercrawl_api_key = os.getenv('WATERCRAWL_API_KEY')
    if not watercrawl_api_key:
        print("⚠ WATERCRAWL_API_KEYが設定されていません")
        print("環境変数を設定してから再実行してください:")
        print("$env:WATERCRAWL_API_KEY='your-api-key'")
        return
    
    # タグ生成器のインスタンスを作成
    generator = BookmarkTagGenerator("dummy_key", watercrawl_api_key)
    
    # テスト用のURL（実際の技術記事サイト）
    test_url = "https://github.com"
    
    print(f"URLの要約を取得中: {test_url}")
    summary = generator.get_watercrawl_summary(test_url)
    
    if summary:
        print("取得された要約:")
        print(summary)
    else:
        print("要約の取得に失敗しました")

def example_full_processing():
    """完全な処理の例"""
    print("\n=== 完全な処理の例 ===")
    
    # APIキーを確認
    openai_api_key = os.getenv('OPENAI_API_KEY')
    watercrawl_api_key = os.getenv('WATERCRAWL_API_KEY')
    
    if not openai_api_key:
        print("⚠ OPENAI_API_KEYが設定されていません")
        return
    
    if not watercrawl_api_key:
        print("⚠ WATERCRAWL_API_KEYが設定されていません")
        print("外部リンク要約機能は無効になります")
    
    # タグ生成器のインスタンスを作成
    generator = BookmarkTagGenerator(openai_api_key, watercrawl_api_key)
    
    # テスト用のMarkdownファイルを作成
    test_file = "test_bookmark.md"
    test_content = """---
title: テストブックマーク
---

# テストブックマーク

これはテスト用のブックマークです。

## 関連リンク

- [GitHub](https://github.com/example/repo)
- [公式ドキュメント](https://docs.example.com)

## 内容

この記事は技術的な内容を含んでいます。
"""
    
    # テストファイルを作成
    with open(test_file, 'w', encoding='utf-8') as f:
        f.write(test_content)
    
    try:
        print(f"テストファイルを作成: {test_file}")
        
        # ファイルを処理
        print("ファイルを処理中...")
        tags = generator.process_bookmark_file(test_file)
        
        print(f"生成されたタグ: {tags}")
        
        # 処理後のファイル内容を表示
        with open(test_file, 'r', encoding='utf-8') as f:
            processed_content = f.read()
        
        print("\n処理後のファイル内容:")
        print("=" * 50)
        print(processed_content)
        print("=" * 50)
        
    finally:
        # テストファイルを削除
        if os.path.exists(test_file):
            os.remove(test_file)
            print(f"\nテストファイルを削除: {test_file}")

def main():
    """メイン関数"""
    print("WaterCrawl統合使用例")
    print("=" * 50)
    
    # 外部リンク抽出の例
    example_external_link_extraction()
    
    # WaterCrawl要約の例
    example_watercrawl_summary()
    
    # 完全な処理の例
    example_full_processing()
    
    print("\n" + "=" * 50)
    print("使用例完了")
    
    print("\n実際の使用:")
    print("1. 環境変数を設定してください")
    print("2. python _scripts/tag_generator.py --directory <path> を実行してください")

if __name__ == "__main__":
    main() 