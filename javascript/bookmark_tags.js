// 基本的なDataviewクエリを使用
console.log("=== DataviewJS デバッグ開始 ===");

// 1. 基本的なページ取得
const allPages = dv.pages();
console.log("全ページ数:", allPages.length);

// 2. bookmarksフォルダ内のページを取得
const bookmarksFolder = dv.pages('"bookmarks"');
console.log("bookmarksフォルダ内のページ数:", bookmarksFolder.length);

// 3. タグ付きファイルを取得
const taggedPages = dv.pages('"bookmarks"').where(p => p.tags);
console.log("タグ付きファイル数:", taggedPages.length);

// 4. 特定フォルダのファイルを取得
const specificFolder = dv.pages('"bookmarks/x-bookmarks-2025-07-23_ikokeba"');
console.log("特定フォルダのページ数:", specificFolder.length);

// 5. 最終的なクエリ（タグ付きファイルのみ）
const bookmarks = dv.pages('"bookmarks"').where(p => p.tags && p.file.name !== "index");
console.log("最終的なブックマーク数:", bookmarks.length);

if (bookmarks.length > 0) {
    console.log("最初のブックマーク:", bookmarks[0]);
    console.log("最初のブックマークのタグ:", bookmarks[0].tags);
}

// すべてのタグを収集
const allTags = new Set();
bookmarks.forEach(page => {
    if (page.tags) {
        console.log("ページのタグ:", page.file.name, page.tags);
        page.tags.forEach(tag => {
            allTags.add(tag);
        });
    }
});

console.log("収集されたタグ:", Array.from(allTags));

// タグを自動的にカテゴリ別に分類
const tagCategories = {
    "技術スタックタグ": [],
    "分野タグ": [],
    "用途タグ": [],
    "その他のタグ": []
};

// タグを自動分類する関数
function categorizeTag(tag) {
    const fieldTags = ["AI", "機械学習", "データサイエンス", "生成AI", "Web開発", "プログラミング"];
    const techTags = ["Python", "JavaScript", "Docker", "Git", "Obsidian"];
    const usageTags = ["チュートリアル", "Tips", "基礎学習", "ツール", "ライブラリ", "記事"];
    
    if (techTags.includes(tag)) {
        return "技術スタックタグ";
    } else if (fieldTags.includes(tag)) {
        return "分野タグ";
    } else if (usageTags.includes(tag)) {
        return "用途タグ";
    } else {
        return "その他のタグ";
    }
}

// 収集されたタグをカテゴリ別に分類
Array.from(allTags).forEach(tag => {
    const category = categorizeTag(tag);
    tagCategories[category].push(tag);
});

console.log("カテゴリ別タグ:", tagCategories);

// 各カテゴリのタグを表示（技術スタックタグを最初に）
Object.entries(tagCategories).forEach(([category, categoryTags]) => {
    if (categoryTags.length > 0) {
        // カテゴリヘッダーを表示
        dv.header(3, `🔧 ${category}`);
        
        categoryTags.forEach(tag => {
            const taggedPages = bookmarks.where(p => p.tags && p.tags.includes(tag));
            
            if (taggedPages.length > 0) {
                // タグタイトルを表示
                dv.header(4, `🏷️ ${tag} (${taggedPages.length}件)`);
                
                // ブックマークをリスト表示
                dv.list(taggedPages.file.link);
            }
        });
    }
}); 