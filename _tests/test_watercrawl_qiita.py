#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
WaterCrawl Qiitaテスト

QiitaのURLでWaterCrawl APIをテストするスクリプト

作成日: 2025-01-27
"""

import os
from watercrawl import WaterCrawlAPIClient

def test_watercrawl_qiita():
    """QiitaのURLでWaterCrawlをテスト"""
    
    # APIキーを確認
    api_key = os.getenv('WATERCRAWL_API_KEY')
    if not api_key:
        print("❌ WATERCRAWL_API_KEYが設定されていません")
        return
    
    try:
        # クライアントを初期化
        client = WaterCrawlAPIClient(api_key=api_key)
        print("✅ クライアント初期化成功")
        
        # QiitaのテストURL
        test_url = "https://qiita.com/Sicut_study/items/4f301d000ecee98e78c9"
        print(f"\n🔗 テストURL: {test_url}")
        
        # scrape_urlでテスト
        print("\n📋 scrape_urlでテスト")
        try:
            result = client.scrape_url(
                url=test_url,
                page_options=None,
                plugin_options=None,
                sync=True,
                download=True
            )
            print(f"✅ scrape_url成功")
            
            if result:
                print(f"\n📊 結果の詳細:")
                print(f"  - UUID: {result.get('uuid', 'N/A')}")
                print(f"  - URL: {result.get('url', 'N/A')}")
                print(f"  - 作成日時: {result.get('created_at', 'N/A')}")
                
                # メタデータを確認
                metadata = result.get('result', {}).get('metadata', {})
                if metadata:
                    print(f"  - タイトル: {metadata.get('title', 'N/A')}")
                
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
                else:
                    print("❌ Markdownコンテンツが取得できませんでした")
            
        except Exception as e:
            print(f"❌ scrape_urlエラー: {e}")
            
    except Exception as e:
        print(f"❌ 初期化エラー: {e}")

if __name__ == "__main__":
    test_watercrawl_qiita() 