// 人気タグの表示
console.log("=== 人気タグデバッグ開始 ===");

const bookmarks = dv.pages('"bookmarks"').where(p => p.tags && p.file.name !== "index");

console.log("取得されたブックマーク数:", bookmarks.length);

// タグの出現回数をカウント
const tagCounts = {};
bookmarks.forEach(page => {
    if (page.tags) {
        console.log("ページのタグ:", page.file.name, page.tags);
        page.tags.forEach(tag => {
            tagCounts[tag] = (tagCounts[tag] || 0) + 1;
        });
    }
});

console.log("タグカウント:", tagCounts);

// 出現回数でソートして上位10件を表示
const sortedTags = Object.entries(tagCounts)
    .sort(([,a], [,b]) => b - a)
    .slice(0, 10);

dv.table(["タグ", "ブックマーク数"], sortedTags); 