#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
WaterCrawl シンプルテスト

watercrawl-pyを使った1つのサイトから要約を取得するサンプルコード

使用方法:
1. 環境変数を設定:
   $env:WATERCRAWL_API_KEY='your-watercrawl-api-key'

2. スクリプトを実行:
   python simple_watercrawl_test.py

作成日: 2025-01-27
"""

import os
import re
from pathlib import Path
from watercrawl import WaterCrawlAPIClient

def sanitize_filename(title: str) -> str:
    """
    タイトルを安全なファイル名に変換
    
    Args:
        title: 元のタイトル
        
    Returns:
        安全なファイル名
    """
    # 特殊文字を除去または置換
    filename = re.sub(r'[<>:"/\\|?*]', '', title)
    filename = re.sub(r'[^\w\s-]', '', filename)
    filename = re.sub(r'[-\s]+', '-', filename)
    filename = filename.strip('-')
    
    # 長さを制限（拡張子を含めて255文字以内）
    if len(filename) > 240:
        filename = filename[:240]
    
    return filename

def save_markdown_content(title: str, markdown_content: str, output_dir: str = "watercrawl_output") -> str:
    """
    Markdownコンテンツをファイルとして保存
    
    Args:
        title: ページタイトル
        markdown_content: Markdownコンテンツ
        output_dir: 出力ディレクトリ
        
    Returns:
        保存されたファイルパス
    """
    # 出力ディレクトリを作成
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)
    
    # 安全なファイル名を生成
    safe_filename = sanitize_filename(title)
    if not safe_filename:
        safe_filename = "untitled"
    
    # ファイルパスを生成
    file_path = output_path / f"{safe_filename}.md"
    
    # 重複ファイル名の処理
    counter = 1
    original_file_path = file_path
    while file_path.exists():
        file_path = output_path / f"{safe_filename}_{counter}.md"
        counter += 1
    
    # ファイルを保存
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(markdown_content)
        print(f"✅ Markdownファイルを保存しました: {file_path}")
        return str(file_path)
    except Exception as e:
        print(f"❌ ファイル保存エラー: {e}")
        return ""

def test_watercrawl_summary():
    """1つのサイトから要約を取得するテスト"""
    
    # APIキーを確認
    api_key = os.getenv('WATERCRAWL_API_KEY')
    if not api_key:
        print("❌ WATERCRAWL_API_KEYが設定されていません")
        print("環境変数を設定してください:")
        print("$env:WATERCRAWL_API_KEY='your-api-key'")
        return
    
    # WaterCrawlクライアントを初期化
    try:
        client = WaterCrawlAPIClient(api_key=api_key)
        print("✅ WaterCrawlクライアントの初期化に成功")
    except Exception as e:
        print(f"❌ WaterCrawlクライアントの初期化に失敗: {e}")
        return
    
    # テスト用のURL（技術記事サイト）
    #test_url = "https://github.com"
    test_url = "https://speakerdeck.com/oracle4engineer/llm-extension-deep-dive"
    print(f"\n🔗 テストURL: {test_url}")
    
    try:
        print("📥 URLからコンテンツを抽出中...")
        
        # URLを抽出
        result = client.scrape_url(
            url=test_url,
            page_options=None,
            plugin_options=None,
            sync=True,
            download=True
        )
        
        if result:
            print("✅ 抽出に成功")
            
            # 結果の詳細を表示
            print(f"\n📊 結果の詳細:")
            print(f"  - UUID: {result.get('uuid', 'N/A')}")
            print(f"  - URL: {result.get('url', 'N/A')}")
            print(f"  - 作成日時: {result.get('created_at', 'N/A')}")
            
            # メタデータを確認
            metadata = result.get('result', {}).get('metadata', {})
            if metadata:
                title = metadata.get('title', 'N/A')
                print(f"  - タイトル: {title}")
            
            # Markdownコンテンツを確認
            markdown_content = result.get('result', {}).get('markdown', '')
            if markdown_content:
                print(f"\n📝 Markdownコンテンツ（最初の500文字）:")
                print("-" * 50)
                print(markdown_content[:500])
                if len(markdown_content) > 500:
                    print("...")
                print("-" * 50)
                
                # 要約を作成（最初の200文字）
                summary = markdown_content[:200]
                if len(markdown_content) > 200:
                    summary += "..."
                print(f"\n📋 要約:")
                print(summary)
                
                # Markdownファイルとして保存
                print(f"\n💾 Markdownファイルを保存中...")
                saved_file_path = save_markdown_content(title, markdown_content)
                if saved_file_path:
                    print(f"📁 保存先: {saved_file_path}")
            else:
                print("❌ Markdownコンテンツが取得できませんでした")
            
        else:
            print("❌ 抽出に失敗しました")
            
    except Exception as e:
        print(f"❌ エラーが発生しました: {e}")

def main():
    """メイン関数"""
    print("WaterCrawl シンプルテスト")
    print("=" * 50)
    
    test_watercrawl_summary()
    
    print("\n" + "=" * 50)
    print("テスト完了")

if __name__ == "__main__":
    main() 