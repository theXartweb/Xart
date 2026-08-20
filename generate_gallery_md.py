#!/usr/bin/env python3
import json
import os
import re
import sys
from html import unescape
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

SITE_ROOT = Path(__file__).resolve().parent
OUTPUT_DIR = SITE_ROOT / "docs" / "X图片"
# 图片存放于与各 md 文件同级的 image 文件夹，即 docs/X图片/image/<页面slug>/
IMAGE_DIR = OUTPUT_DIR / "image"


def fetch_html(url: str) -> str:
    request = Request(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        },
    )
    with urlopen(request, timeout=30) as response:
        body = response.read()
    return body.decode("utf-8", errors="replace")


def clean_title(raw: str) -> str:
    text = unescape(raw or "Gallery")
    text = re.sub(r"\s+", " ", text).strip()
    text = text.replace(" - Cosplaytele", "")
    return text or "Gallery"


def slugify(text: str) -> str:
    text = re.sub(r"[\\/:*?\"<>|]+", " ", text)
    text = text.strip()
    text = re.sub(r"\s+", "-", text)
    text = re.sub(r"-+", "-", text)
    return text.lower()[:80] or "gallery"


def extract_title(html: str) -> str:
    title_match = re.search(r"<title>(.*?)</title>", html, re.I | re.S)
    if title_match:
        return clean_title(title_match.group(1))

    h1_match = re.search(r"<h1[^>]*>(.*?)</h1>", html, re.I | re.S)
    if h1_match:
        return clean_title(re.sub(r"<.*?>", "", h1_match.group(1)))

    return "Gallery"


def normalize_image_url(url: str) -> str:
    cleaned = url.strip().rstrip(",)")
    cleaned = cleaned.split("?", 1)[0]
    return cleaned


def image_extension(url: str) -> str:
    suffix = Path(normalize_image_url(url)).suffix.lower()
    return suffix if suffix in {".jpg", ".jpeg", ".png", ".webp"} else ".webp"


def download_image(url: str, target: Path) -> None:
    request = Request(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/124.0 Safari/537.36",
            "Referer": "https://cosplaytele.com/",
        },
    )
    with urlopen(request, timeout=60) as response:
        data = response.read()
    if not data:
        raise ValueError("下载内容为空")
    target.write_bytes(data)


def is_noise_image(url: str) -> bool:
    lower = url.lower()
    if "cosplaytele.com/wp-content/uploads" not in lower:
        return True

    noise_tokens = (
        "cropped-icon",
        "favicon",
        "logo",
        "avatar",
        "thumbnail",
        "mini",
        "small",
        "banner",
        "widget",
        "icon-",
        "og-image",
        "screenshot",
        "screen-shot",
        ".ico",
        "-32x32",
        "-192x192",
        "-180x180",
        "-270x270",
        "-150x150",
        "-300x300",
    )
    if any(token in lower for token in noise_tokens):
        return True

    if re.search(r"[-_](?:\d{2,5})x(?:\d{2,5})", lower):
        return True

    return False


def title_keywords(title: str) -> list[str]:
    text = unescape(title or "")
    text = text.lower()
    text = re.sub(r"[^a-z0-9]+", " ", text)
    tokens = [part for part in text.split() if len(part) > 2]
    filtered = []
    skip = {"cosplaytele", "photos", "videos", "natural", "beauty", "girl", "honkai", "star", "rail", "topaz", "youmu", "sayo", "momo"}
    for part in tokens:
        if part not in skip and part not in filtered:
            filtered.append(part)
    return filtered


def basename_matches_title(url: str, title: str) -> bool:
    filename = normalize_image_url(url).rsplit("/", 1)[-1].lower()
    tokens = title_keywords(title)
    if not tokens:
        return True

    normalized = re.sub(r"[^a-z0-9]+", "", filename)
    for token in tokens:
        token_norm = re.sub(r"[^a-z0-9]+", "", token)
        if not token_norm:
            continue
        if token_norm in normalized:
            return True
        if token in filename:
            return True
    return False


def extract_image_urls(html: str, title: str = ""):
    pattern = r'https?://[^"\'\s<>]+(?:jpg|jpeg|png|webp)(?:\?[^"\'\s<>]*)?'
    found = []
    seen = set()

    for match in re.finditer(pattern, html, re.I):
        url = normalize_image_url(match.group(0))
        if not url or url in seen:
            continue
        if is_noise_image(url):
            continue
        seen.add(url)
        found.append(url)

    if title:
        matched = [url for url in found if basename_matches_title(url, title)]
        if matched:
            return matched

    result_images = [url for url in found if "_result" in url.lower() or "-result" in url.lower()]
    return result_images if result_images else found


def build_gallery_md(title: str, image_paths: list[str]) -> str:
    item_count = len(image_paths)
    page_title = title.strip() or "Gallery"
    safe_title = page_title
    gallery_buttons = "\n".join(
        [
            f'    <button class="gallery-item" type="button" data-index="{idx}" data-src="{path}"><img src="{path}" alt="{safe_title} {idx + 1}" loading="lazy"></button>'
            for idx, path in enumerate(image_paths)
        ]
    )
    js_urls = json.dumps(image_paths)

    return f'''---
hide:
   - toc
   - feedback

# comments: true
---
<style>
  .container{{width:92%;max-width:1200px;margin:0 auto;padding:12px 0 24px}}
  .page-header{{margin:0 0 18px}}
  .page-title{{margin:0 0 6px;font-size:2rem;line-height:1.2}}
  .page-subtitle{{margin:0;color:#666;font-size:.95rem}}
  .gallery-grid{{display:grid;grid-template-columns:repeat(auto-fill, minmax(180px, 1fr));gap:14px}}
  .gallery-item{{display:block;overflow:hidden;border-radius:14px;background:#fff;box-shadow:0 10px 26px rgba(0,0,0,.08);border:1px solid rgba(0,0,0,.05);transition:transform .22s ease, box-shadow .22s ease;cursor:pointer;padding:0}}
  .gallery-item:hover{{transform:translateY(-4px);box-shadow:0 16px 32px rgba(0,0,0,.12)}}
  .gallery-item img{{display:block;width:100%;aspect-ratio:3/4;object-fit:cover;background:#f3f3f3;user-select:none;-webkit-user-drag:none}}
  .lightbox{{position:fixed;inset:0;display:none;align-items:center;justify-content:center;background:rgba(0,0,0,.8);z-index:9999;padding:24px}}
  .lightbox.open{{display:flex}}
  .lightbox-panel{{position:relative;width:min(92vw, 1100px);max-height:90vh;background:#111;border-radius:18px;box-shadow:0 24px 70px rgba(0,0,0,.45);overflow:hidden}}
  .lightbox-image-wrap{{display:flex;align-items:center;justify-content:center;min-height:70vh;background:#000}}
  .lightbox-image-wrap img{{display:block;max-width:100%;max-height:82vh;object-fit:contain;background:#000}}
  .lightbox-close, .lightbox-prev, .lightbox-next{{position:absolute;top:50%;transform:translateY(-50%);border:none;color:#fff;background:rgba(255,255,255,.12);backdrop-filter:blur(8px);border-radius:50%;width:42px;height:42px;font-size:28px;cursor:pointer;z-index:2}}
  .lightbox-close{{top:18px;right:18px;transform:none;width:38px;height:38px;font-size:22px}}
  .lightbox-prev{{left:18px}}
  .lightbox-next{{right:18px}}
  .lightbox-info{{position:absolute;left:18px;bottom:16px;color:#fff;font-size:13px;background:rgba(0,0,0,.28);padding:7px 10px;border-radius:999px;backdrop-filter:blur(8px)}}
  .back-wrap{{padding-top:18px}}
  a.back{{display:inline-block;color:#444;background:#fff;padding:8px 12px;border-radius:18px;border:1px solid #eee;box-shadow:0 6px 18px rgba(0,0,0,0.06);text-decoration:none;font-size:13px}}
  a.back:hover{{transform:translateY(-2px);box-shadow:0 10px 24px rgba(0,0,0,0.08);color:#111}}
  @media (max-width:600px){{
    .container{{width:94%}}
    .gallery-grid{{grid-template-columns:repeat(auto-fill, minmax(140px, 1fr));gap:10px}}
    .page-title{{font-size:1.5rem}}
    .lightbox{{padding:16px}}
    .lightbox-panel{{width:min(96vw, 900px)}}
    .lightbox-prev,.lightbox-next{{width:36px;height:36px;font-size:24px}}
  }}
</style>

<main class="container">
  <header class="page-header">
    <h1 class="page-title">{page_title}</h1>
    <p class="page-subtitle">{item_count} photos · 来源：Cosplaytele</p>
  </header>

  <div class="gallery-grid" id="galleryGrid">
{gallery_buttons}
  </div>

  <div class="lightbox" id="lightbox" aria-hidden="true">
    <div class="lightbox-panel">
      <button class="lightbox-close" type="button" aria-label="Close">×</button>
      <button class="lightbox-prev" type="button" aria-label="Previous">‹</button>
      <button class="lightbox-next" type="button" aria-label="Next">›</button>
      <div class="lightbox-image-wrap">
        <img id="lightboxImage" src="" alt="Preview">
      </div>
      <div class="lightbox-info" id="lightboxInfo">1 / {item_count}</div>
    </div>
  </div>

  <div class="back-wrap"><a class="back" href="../index.html">返回首页</a></div>
</main>

<script>
(function() {{
  const imageUrls = {js_urls};
  const lightbox = document.getElementById('lightbox');
  const lightboxImage = document.getElementById('lightboxImage');
  const lightboxInfo = document.getElementById('lightboxInfo');
  const closeBtn = document.querySelector('.lightbox-close');
  const prevBtn = document.querySelector('.lightbox-prev');
  const nextBtn = document.querySelector('.lightbox-next');
  const items = Array.from(document.querySelectorAll('.gallery-item'));
  let currentIndex = 0;

  function updateViewer(index) {{
    currentIndex = (index + imageUrls.length) % imageUrls.length;
    lightboxImage.src = imageUrls[currentIndex];
    lightboxImage.alt = '{safe_title} ' + (currentIndex + 1);
    lightboxInfo.textContent = (currentIndex + 1) + ' / ' + imageUrls.length;
  }}

  function openLightbox(index) {{
    updateViewer(index);
    lightbox.classList.add('open');
    lightbox.setAttribute('aria-hidden', 'false');
  }}

  function closeLightbox() {{
    lightbox.classList.remove('open');
    lightbox.setAttribute('aria-hidden', 'true');
  }}

  items.forEach((item) => {{
    item.addEventListener('click', function () {{
      openLightbox(Number(item.dataset.index));
    }});
  }});

  closeBtn.addEventListener('click', closeLightbox);
  prevBtn.addEventListener('click', function () {{
    updateViewer(currentIndex - 1);
  }});
  nextBtn.addEventListener('click', function () {{
    updateViewer(currentIndex + 1);
  }});

  lightbox.addEventListener('click', function (event) {{
    if (event.target === lightbox) closeLightbox();
  }});

  document.addEventListener('keydown', function (event) {{
    if (!lightbox.classList.contains('open')) return;
    if (event.key === 'Escape') closeLightbox();
    if (event.key === 'ArrowLeft') updateViewer(currentIndex - 1);
    if (event.key === 'ArrowRight') updateViewer(currentIndex + 1);
  }});
}})();
</script>
'''


def parse_count(value: str) -> int:
    try:
        count = int(value)
    except ValueError as exc:
        raise ValueError("图片数量必须是整数。") from exc

    if count <= 0:
        raise ValueError("图片数量必须大于 0。")
    return count


def split_urls(text: str) -> list[str]:
    """把用户输入拆分为网址列表，兼容换行、逗号、分号、空格分隔。"""
    urls = re.split(r"[\s,，;；]+", text.strip())
    return [u for u in urls if u.startswith("http://") or u.startswith("https://")]


def read_urls_from_stdin() -> list[str]:
    """交互式读取多个网址：每行一个（可粘贴多行），输入空行结束。"""
    print("请输入网址（每行一个，可粘贴多个；输入空行结束）：")
    lines = []
    while True:
        try:
            line = input()
        except EOFError:
            break
        if not line.strip():
            break
        lines.append(line)
    return split_urls("\n".join(lines))


def process_one(url: str, target_count: int) -> dict:
    """抓取单个网址并生成画廊页面，返回结果字典。"""
    result = {"url": url, "ok": False}
    try:
        html = fetch_html(url)
    except (HTTPError, URLError) as exc:
        result["error"] = f"抓取页面失败：{exc}"
        return result

    title = extract_title(html)
    image_urls = extract_image_urls(html, title)

    if not image_urls:
        result["error"] = "未提取到图片链接（页面可能使用了懒加载/脚本生成图片）"
        return result

    if len(image_urls) > target_count:
        image_urls = image_urls[:target_count]

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    filename = slugify(title) + ".md"
    target = OUTPUT_DIR / filename
    asset_dir = IMAGE_DIR / slugify(title)
    asset_dir.mkdir(parents=True, exist_ok=True)
    local_paths = []
    failed_count = 0
    for index, image_url in enumerate(image_urls, start=1):
        local_file = asset_dir / f"{index:03d}{image_extension(image_url)}"
        try:
            download_image(image_url, local_file)
        except (HTTPError, URLError, OSError, ValueError) as exc:
            failed_count += 1
            print(f"    下载失败，已跳过：{image_url} ({exc})")
            continue
        relative_path = Path(os.path.relpath(local_file, target.parent)).as_posix()
        # MkDocs 默认 use_directory_urls: true，页面会构建到 <父目录>/<slug>/index.html（比 md 深一层）。
        # 原始 HTML 块内的相对路径 MkDocs 不会改写，必须相对最终页面 URL 再上一层 ../。
        relative_path = "../" + relative_path
        local_paths.append(relative_path)

    if not local_paths:
        result["error"] = "没有成功下载任何图片，未生成 Markdown 页面"
        return result

    page_md = build_gallery_md(title, local_paths)
    target.write_text(page_md, encoding="utf-8")
    result.update(
        {"ok": True, "title": title, "path": str(target), "count": len(local_paths), "failed": failed_count}
    )
    return result


def batch_generate(urls: list[str], target_count: int) -> None:
    """批量处理多个网址，统一图片数量，生成多个 md 页面。"""
    print(f"共 {len(urls)} 个网址，统一保留 {target_count} 张图片。\n")
    ok_count = 0
    fail_count = 0
    for index, url in enumerate(urls, start=1):
        print(f"[{index}/{len(urls)}] 处理：{url}")
        result = process_one(url, target_count)
        if result["ok"]:
            ok_count += 1
            print(f"    ✓ 已生成：{result['path']}（{result['title']}，{result['count']} 张）")
            if result["failed"]:
                print(f"    下载失败 {result['failed']} 张")
        else:
            fail_count += 1
            print(f"    ✗ 失败：{result['error']}")
        print()

    print(f"完成：成功 {ok_count} 个，失败 {fail_count} 个。")
    if ok_count:
        print("提示：可运行 `python generate_index_cards.py` 刷新首页推荐与分类索引。")


def main():
    args = sys.argv[1:]

    # 用法 1（批量）：python generate_gallery_md.py <统一数量> [url1 url2 ...]
    # 未在命令行附带网址时进入交互式粘贴：每行一个，空行结束。
    if args and args[0].lstrip("-").isdigit():
        try:
            target_count = parse_count(args[0])
        except ValueError as exc:
            print(f"参数错误：{exc}")
            raise SystemExit(1)
        if len(args) > 1:
            urls = split_urls(" ".join(args[1:]))
        else:
            urls = read_urls_from_stdin()
        if not urls:
            print("没有可用的网址。")
            raise SystemExit(1)
        batch_generate(urls, target_count)
        return

    # 用法 2（兼容旧版，单页面）：python generate_gallery_md.py <url> <count>
    if len(args) >= 2:
        url = args[0].strip()
        try:
            target_count = parse_count(args[1])
        except ValueError as exc:
            print(f"参数错误：{exc}")
            raise SystemExit(1)
        result = process_one(url, target_count)
        if not result["ok"]:
            print(result["error"])
            raise SystemExit(1)
        print(f"已生成：{result['path']}")
        print(f"标题：{result['title']}")
        print(f"图片数量：{result['count']}")
        if result["failed"]:
            print(f"下载失败数量：{result['failed']}")
        return

    # 用法 3（纯交互，支持批量）：先输入统一数量，再粘贴多个网址
    count_text = input("请输入统一的图片数量：").strip()
    try:
        target_count = parse_count(count_text)
    except ValueError as exc:
        print(f"参数错误：{exc}")
        raise SystemExit(1)
    urls = read_urls_from_stdin()
    if not urls:
        print("没有可用的网址。")
        raise SystemExit(1)
    batch_generate(urls, target_count)


if __name__ == "__main__":
    main()
