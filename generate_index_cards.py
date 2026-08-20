# -*- coding: utf-8 -*-
#!/usr/bin/env python3
import re
import json
from html import escape
from pathlib import Path

SITE_ROOT = Path(__file__).resolve().parent
DOCS_DIR = SITE_ROOT / "docs"
INDEX_PATH = DOCS_DIR / "index.md"
SECTION_DIRS = [DOCS_DIR / "X图片", DOCS_DIR / "X视频"]
START_MARK = "<!-- AUTO_REC_CARDS_START -->"
END_MARK = "<!-- AUTO_REC_CARDS_END -->"
SECTION_LABELS = {"X图片": "图集精选", "X视频": "视频精选"}


def strip_front_matter(markdown: str) -> str:
    match = re.match(r"^---\r?\n.*?\r?\n---\r?\n?", markdown, re.S)
    return markdown[match.end():] if match else markdown


def pick_title(markdown: str, fallback: str) -> str:
    body = strip_front_matter(markdown)
    patterns = [
        r"<h1[^>]*>(.*?)</h1>",
        r"<h2[^>]*class=[\"']video-title[\"'][^>]*>(.*?)</h2>",
        r"^#\s+(.+?)\s*$",
        r"<title>(.*?)</title>",
    ]
    for pattern in patterns:
        match = re.search(pattern, body, re.I | re.M | re.S)
        if match:
            title = re.sub(r"<.*?>", "", match.group(1))
            title = re.sub(r"\s+", " ", title).strip()
            if title:
                return title.replace(" - Cosplaytele", "")
    return fallback


def slugify(value: str) -> str:
    value = re.sub(r"[\\/:*?\"<>|]+", " ", value or "untitled")
    return re.sub(r"\s+", "-", value.strip()).lower()[:80] or "untitled"


def pick_thumbnail(markdown: str, title: str, page: Path) -> str:
    # 1) 优先使用本地图库第一张：docs/X图片/image/<页面名>/NNN.xxx
    local_dir = page.parent / "image" / page.stem
    if local_dir.is_dir():
        local_images = sorted(p for p in local_dir.iterdir() if p.is_file())
        if local_images:
            # 返回相对 docs 根目录的规范路径（如 X图片/image/<slug>/001.webp）
            return local_images[0].relative_to(DOCS_DIR).as_posix()

    # 2) 回退：从 markdown 里取第一张可用图片
    pattern = r'(?:data-src|src)=["\']([^"\']+\.(?:jpe?g|png|webp|gif)(?:\?[^"\']*)?)["\']'
    blocked = ("logo", "avatar", "favicon", "icon", "thumbnail", "mini", "small", "banner", "cropped", "screenshot")
    for match in re.finditer(pattern, markdown, re.I):
        url = match.group(1).strip()
        lower = url.lower()
        if any(token in lower for token in blocked) or re.search(r"[-_]\d{2,5}x\d{2,5}", lower):
            continue
        # 远程图片可直接使用
        if lower.startswith("http://") or lower.startswith("https://"):
            return url
        # 本地相对路径：解析为相对 docs 的路径，且文件必须真实存在
        resolved = (page.parent / url).resolve()
        if resolved.is_file():
            try:
                return resolved.relative_to(DOCS_DIR.resolve()).as_posix()
            except ValueError:
                continue
    return f"https://picsum.photos/seed/{slugify(title)}/640/360"


def category_thumb(thumb: str, category: str) -> str:
    """把相对 docs 根目录的缩略图路径换算为相对分类索引页（/X图片/）的路径。"""
    prefix = category + "/"
    if thumb.startswith(prefix):
        return thumb[len(prefix):]
    return thumb


def dedupe_records(records: list[dict]) -> list[dict]:
    kept = []
    for item in records:
        duplicate = next((other for other in kept
                          if other["category"] == item["category"]
                          and (other["title"].lower().startswith(item["title"].lower())
                               or item["title"].lower().startswith(other["title"].lower()))), None)
        if duplicate is None:
            kept.append(item)
        elif len(item["title"]) > len(duplicate["title"]):
            kept[kept.index(duplicate)] = item
    return kept


def collect_records() -> list[dict]:
    records = []
    for folder in SECTION_DIRS:
        if not folder.exists():
            continue
        for path in sorted(folder.glob("*.md")):
            if path.name.lower() == "index.md":
                continue
            raw = path.read_text(encoding="utf-8", errors="replace")
            title = pick_title(raw, path.stem.replace("-", " "))
            records.append({
                "category": folder.name,
                "title": title,
                "path": path.relative_to(DOCS_DIR).with_suffix("").as_posix(),
                "thumb": pick_thumbnail(raw, title, path),
                "label": SECTION_LABELS.get(folder.name, folder.name),
            })
    records.sort(key=lambda item: (item["category"], item["title"].lower()))
    return dedupe_records(records)


def build_card(item: dict) -> str:
    title = escape(item["title"])
    alt = escape(item["title"], quote=True)
    return f'''<article class="rec-card">
  <a href="{item["path"]}">
    <figure class="rec-thumb">
      <img class="rec-img" src="{item["thumb"]}" alt="{alt}" loading="lazy">
    </figure>
    <div class="rec-body">
      <h3 class="rec-title">{title}</h3>
      <p class="rec-meta">{item["category"]} · {item["label"]}</p>
    </div>
  </a>
</article>'''


def render_section(records: list[dict]) -> str:
    random_urls = json.dumps([item["path"] + "/" for item in records], ensure_ascii=False)
    groups = []
    for category in ("X图片", "X视频"):
        items = [item for item in records if item["category"] == category][:10]
        if items:
            cards = "\n".join(build_card(item) for item in items)
            groups.append(f'''<div class="section-heading">
<h2 class="section-title">推荐 · {category}</h2>
<a class="more-link" href="{category}/">更多 <span aria-hidden="true">→</span></a>
</div>
<div class="rec-grid">
{cards}
</div>''')
    return f'''{START_MARK}
<button class="random-link" id="randomLink" type="button">随机色情 <span aria-hidden="true">↗</span></button>
<script>
(function() {{
    const randomUrls = {random_urls};
    const randomLink = document.getElementById("randomLink");
    randomLink.addEventListener("click", function() {{
        const target = randomUrls[Math.floor(Math.random() * randomUrls.length)];
        window.location.href = target;
    }});
}})();
</script>

''' + "\n\n".join(groups) + f"\n{END_MARK}" 


def main() -> None:
    records = collect_records()
    if not records:
        raise SystemExit("没有找到可用的 X图片/X视频 页面。")
    content = INDEX_PATH.read_text(encoding="utf-8", errors="replace")
    block = render_section(records)
    content = re.sub(r"(?s)<!-- AUTO_REC_CARDS_START -->.*?<!-- AUTO_REC_CARDS_END -->", block, content)
    INDEX_PATH.write_text(content, encoding="utf-8")
    for category in ("X图片", "X视频"):
        category_records = [item for item in records if item["category"] == category]
        category_index = DOCS_DIR / category / "index.md"
        category_index.write_text(render_category_index(category, category_records), encoding="utf-8")
    print(f"已生成推荐卡片：{len(records)} 条")

def render_category_index(category: str, records: list[dict]) -> str:
    cards = []
    for item in records:
        page_path = item["path"].split("/", 1)[1] + "/"
        cards.append(f'''<a class="category-card" href="{page_path}">
  <img src="{category_thumb(item["thumb"], category)}" alt="{escape(item["title"], quote=True)}" loading="lazy">
  <span>{escape(item["title"])}</span>
</a>''')
    return f'''---
hide:
  - toc
  - feedback
---
<style>
.category-page{{max-width:1200px;margin:0 auto;padding:12px 0 24px}}
.category-grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(220px,1fr));gap:16px}}
.category-card{{display:flex;flex-direction:column;overflow:hidden;border:1px solid rgba(128,128,128,.2);border-radius:14px;background:var(--md-default-bg-color);box-shadow:0 8px 24px rgba(0,0,0,.08);color:inherit;text-decoration:none;transition:transform .2s ease,box-shadow .2s ease}}
.category-card:hover{{transform:translateY(-4px);box-shadow:0 14px 30px rgba(0,0,0,.14)}}
.category-card img{{width:100%;aspect-ratio:16/9;object-fit:cover;background:#eee}}
.category-card span{{padding:12px;font-weight:600;line-height:1.4}}
</style>
<main class="category-page">
<h1>{category}</h1>
<div class="category-grid">
{chr(10).join(cards)}
</div>
</main>
'''


if __name__ == "__main__":
    main()
