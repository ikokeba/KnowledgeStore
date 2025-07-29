#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Xブックマーク管理システム テストスクリプト

機能:
- システムの基本動作確認
- ファイル構造の検証
- 依存関係の確認

作成日: 2025-07-28
作成者: AI Assistant
"""

import os
import sys
from pathlib import Path

def test_directory_structure():
    """ディレクトリ構造のテスト"""
    print("=== ディレクトリ構造テスト ===")
    
    required_dirs = [
        "bookmarks",
        "_scripts",
        "_templates"
    ]
    
    for dir_name in required_dirs:
        if os.path.exists(dir_name):
            print(f"✓ {dir_name} ディレクトリが存在します")
        else:
            print(f"✗ {dir_name} ディレクトリが存在しません")
    
    # ブックマークフォルダの確認
    bookmarks_dir = Path("bookmarks")
    if bookmarks_dir.exists():
        bookmark_folders = list(bookmarks_dir.glob("x-bookmarks-*"))
        print(f"✓ ブックマークフォルダ数: {len(bookmark_folders)}")
        for folder in bookmark_folders:
            print(f"  - {folder.name}")
    else:
        print("✗ bookmarksディレクトリが存在しません")

def test_script_files():
    """スクリプトファイルのテスト"""
    print("\n=== スクリプトファイルテスト ===")
    
    required_scripts = [
        "_scripts/tag_generator.py",
        "_scripts/process_new_folders.py",
        "_scripts/test_system.py"
    ]
    
    for script in required_scripts:
        if os.path.exists(script):
            print(f"✓ {script} が存在します")
        else:
            print(f"✗ {script} が存在しません")

def test_dependencies():
    """依存関係のテスト"""
    print("\n=== 依存関係テスト ===")
    
    try:
        import openai
        print("✓ openaiライブラリが利用可能です")
    except ImportError:
        print("✗ openaiライブラリがインストールされていません")
        print("  実行: pip install openai")
    
    try:
        from pathlib import Path
        print("✓ pathlibライブラリが利用可能です")
    except ImportError:
        print("✗ pathlibライブラリが利用できません")

def test_environment_variables():
    """環境変数のテスト"""
    print("\n=== 環境変数テスト ===")
    
    api_key = os.getenv('OPENAI_API_KEY')
    if api_key:
        print("✓ OPENAI_API_KEYが設定されています")
        print(f"  キー: {api_key[:10]}...")
    else:
        print("✗ OPENAI_API_KEYが設定されていません")
        print("  設定方法: $env:OPENAI_API_KEY='your-api-key'")

def test_bookmark_files():
    """ブックマークファイルのテスト"""
    print("\n=== ブックマークファイルテスト ===")
    
    bookmarks_dir = Path("bookmarks")
    if not bookmarks_dir.exists():
        print("✗ bookmarksディレクトリが存在しません")
        return
    
    total_files = 0
    total_bookmarks = 0
    
    for folder in bookmarks_dir.glob("x-bookmarks-*"):
        if folder.is_dir():
            md_files = list(folder.glob("*.md"))
            total_files += len(md_files)
            
            # index.md以外のファイルをカウント
            bookmark_files = [f for f in md_files if f.name != "index.md"]
            total_bookmarks += len(bookmark_files)
            
            print(f"✓ {folder.name}: {len(bookmark_files)}個のブックマーク")
    
    print(f"✓ 総ブックマーク数: {total_bookmarks}")

def test_requirements_file():
    """requirements.txtファイルのテスト"""
    print("\n=== requirements.txtテスト ===")
    
    if os.path.exists("requirements.txt"):
        print("✓ requirements.txtが存在します")
        
        with open("requirements.txt", 'r') as f:
            content = f.read()
            print("  内容:")
            for line in content.strip().split('\n'):
                if line.strip():
                    print(f"    {line}")
    else:
        print("✗ requirements.txtが存在しません")

def main():
    """メイン関数"""
    print("Xブックマーク管理システム テスト開始")
    print("=" * 50)
    
    test_directory_structure()
    test_script_files()
    test_dependencies()
    test_environment_variables()
    test_bookmark_files()
    test_requirements_file()
    
    print("\n" + "=" * 50)
    print("テスト完了")
    
    print("\n次のステップ:")
    print("1. OpenAI APIキーを設定してください")
    print("2. 依存関係をインストールしてください: pip install -r requirements.txt")
    print("3. タグ生成を実行してください: python _scripts/tag_generator.py")

if __name__ == "__main__":
    main() 