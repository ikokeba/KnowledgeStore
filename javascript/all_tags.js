// 全タグ一覧の表示
console.log("=== 全タグ一覧デバッグ開始 ===");

const bookmarks = dv.pages('"bookmarks"').where(p => p.tags && p.file.name !== "index");

console.log("取得されたブックマーク数:", bookmarks.length);

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

// タグの出現回数をカウント
const tagCounts = {};
bookmarks.forEach(page => {
    if (page.tags) {
        page.tags.forEach(tag => {
            tagCounts[tag] = (tagCounts[tag] || 0) + 1;
        });
    }
});

console.log("タグカウント:", tagCounts);

// 出現回数でソートして表示
const sortedTags = Object.entries(tagCounts)
    .sort(([,a], [,b]) => b - a);

dv.table(["タグ", "ブックマーク数"], sortedTags); 