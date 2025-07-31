#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
WaterCrawl デバッグスクリプト

WaterCrawl APIの使用方法を調査するためのスクリプト

作成日: 2025-01-27
"""

import os
from watercrawl import WaterCrawlAPIClient

def debug_watercrawl():
    """WaterCrawlの使用方法をデバッグ"""
    
    # APIキーを確認
    api_key = os.getenv('WATERCRAWL_API_KEY')
    if not api_key:
        print("❌ WATERCRAWL_API_KEYが設定されていません")
        return
    
    print(f"APIキー: {api_key[:10]}...")
    
    try:
        # クライアントを初期化
        client = WaterCrawlAPIClient(api_key=api_key)
        print("✅ クライアント初期化成功")
        
        # 利用可能なメソッドを確認
        print("\n📋 利用可能なメソッド:")
        methods = [method for method in dir(client) if not method.startswith('_')]
        for method in methods:
            print(f"  - {method}")
        
        # scrape_urlメソッドの詳細を確認
        print(f"\n🔍 scrape_urlメソッドの詳細:")
        scrape_method = getattr(client, 'scrape_url', None)
        if scrape_method:
            print(f"  型: {type(scrape_method)}")
            print(f"  ドキュメント: {scrape_method.__doc__}")
        else:
            print("  scrape_urlメソッドが見つかりません")
        
        # 簡単なテスト
        print(f"\n🧪 簡単なテスト:")
        test_url = "https://example.com"
        print(f"テストURL: {test_url}")
        
        try:
            result = client.scrape_url(test_url)
            print(f"結果: {result}")
            if result:
                print(f"結果の型: {type(result)}")
                print(f"結果の属性: {dir(result)}")
        except Exception as e:
            print(f"エラー: {e}")
            print(f"エラーの型: {type(e)}")
            
    except Exception as e:
        print(f"❌ 初期化エラー: {e}")

if __name__ == "__main__":
    debug_watercrawl() 