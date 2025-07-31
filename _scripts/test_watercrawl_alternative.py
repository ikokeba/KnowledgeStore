#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
WaterCrawl 代替テスト

WaterCrawl APIの代替的な使用方法をテストするスクリプト

作成日: 2025-01-27
"""

import os
import time
from watercrawl import WaterCrawlAPIClient

def test_watercrawl_alternative():
    """WaterCrawlの代替的な使用方法をテスト"""
    
    # APIキーを確認
    api_key = os.getenv('WATERCRAWL_API_KEY')
    if not api_key:
        print("❌ WATERCRAWL_API_KEYが設定されていません")
        return
    
    try:
        # クライアントを初期化
        client = WaterCrawlAPIClient(api_key=api_key)
        print("✅ クライアント初期化成功")
        
        # テスト用のURL
        test_url = "https://example.com"
        print(f"\n🔗 テストURL: {test_url}")
        
        # 方法1: create_crawl_requestを使用
        print("\n📋 方法1: create_crawl_requestを使用")
        try:
            crawl_request = client.create_crawl_request(
                urls=[test_url],
                name="Test Crawl"
            )
            print(f"クロールリクエスト作成成功: {crawl_request}")
            
            # リクエストIDを取得
            if hasattr(crawl_request, 'id'):
                request_id = crawl_request.id
                print(f"リクエストID: {request_id}")
                
                # 結果を監視
                print("結果を監視中...")
                for i in range(10):  # 最大10回試行
                    time.sleep(2)  # 2秒待機
                    
                    try:
                        results = client.get_crawl_request_results(request_id)
                        if results:
                            print(f"結果取得成功: {results}")
                            break
                        else:
                            print(f"試行 {i+1}: 結果なし")
                    except Exception as e:
                        print(f"試行 {i+1}: エラー - {e}")
                
        except Exception as e:
            print(f"方法1エラー: {e}")
        
        # 方法2: セッション初期化を試行
        print("\n📋 方法2: セッション初期化")
        try:
            client.init_session()
            print("セッション初期化成功")
            
            # 再度scrape_urlを試行
            result = client.scrape_url(test_url)
            print(f"scrape_url結果: {result}")
            
        except Exception as e:
            print(f"方法2エラー: {e}")
        
        # 方法3: 利用可能なリクエストを確認
        print("\n📋 方法3: 利用可能なリクエストを確認")
        try:
            requests_list = client.get_crawl_requests_list()
            print(f"利用可能なリクエスト: {requests_list}")
        except Exception as e:
            print(f"方法3エラー: {e}")
            
    except Exception as e:
        print(f"❌ 初期化エラー: {e}")

if __name__ == "__main__":
    test_watercrawl_alternative() 