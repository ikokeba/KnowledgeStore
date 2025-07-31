#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
WaterCrawl 最終テスト

WaterCrawl APIの正しいパラメータでテストするスクリプト

作成日: 2025-01-27
"""

import os
import time
from watercrawl import WaterCrawlAPIClient

def test_watercrawl_final():
    """WaterCrawlの正しいパラメータでテスト"""
    
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
        
        # 方法1: scrape_urlを正しいパラメータで使用
        print("\n📋 方法1: scrape_url（正しいパラメータ）")
        try:
            result = client.scrape_url(
                url=test_url,
                page_options=None,
                plugin_options=None,
                sync=True,
                download=True
            )
            print(f"scrape_url結果: {result}")
            if result:
                print(f"結果の型: {type(result)}")
                print(f"結果の属性: {dir(result)}")
                
                # 要約やテキストを確認
                if hasattr(result, 'summary'):
                    print(f"要約: {result.summary}")
                if hasattr(result, 'text'):
                    print(f"テキスト（最初の200文字）: {result.text[:200]}...")
                if hasattr(result, 'title'):
                    print(f"タイトル: {result.title}")
            
        except Exception as e:
            print(f"方法1エラー: {e}")
        
        # 方法2: create_crawl_requestを正しいパラメータで使用
        print("\n📋 方法2: create_crawl_request（正しいパラメータ）")
        try:
            crawl_request = client.create_crawl_request(url=test_url)
            print(f"クロールリクエスト作成成功: {crawl_request}")
            
            # リクエストIDを取得
            if hasattr(crawl_request, 'id'):
                request_id = crawl_request.id
                print(f"リクエストID: {request_id}")
                
                # 結果を監視
                print("結果を監視中...")
                for i in range(10):  # 最大10回試行
                    time.sleep(3)  # 3秒待機
                    
                    try:
                        results = client.get_crawl_request_results(request_id)
                        if results and len(results) > 0:
                            print(f"結果取得成功: {results}")
                            # 最初の結果の詳細を表示
                            first_result = results[0] if isinstance(results, list) else results
                            print(f"結果の型: {type(first_result)}")
                            print(f"結果の属性: {dir(first_result)}")
                            break
                        else:
                            print(f"試行 {i+1}: 結果なし")
                    except Exception as e:
                        print(f"試行 {i+1}: エラー - {e}")
                
        except Exception as e:
            print(f"方法2エラー: {e}")
        
        # 方法3: バッチクロールリクエストを正しいパラメータで使用
        print("\n📋 方法3: バッチクロールリクエスト（正しいパラメータ）")
        try:
            batch_request = client.create_batch_crawl_request(urls=[test_url])
            print(f"バッチクロールリクエスト作成成功: {batch_request}")
            
        except Exception as e:
            print(f"方法3エラー: {e}")
            
    except Exception as e:
        print(f"❌ 初期化エラー: {e}")

if __name__ == "__main__":
    test_watercrawl_final() 