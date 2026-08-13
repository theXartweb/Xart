"""
generate_site.py

生成静态视频站点：从 vedio 文件夹读取 .mp4 文件，使用 OpenCV 读取首帧作为封面，
并生成一个 index.html（主页）和若干视频播放页（每个视频一页）。

使用:
  python generate_site.py

需求:
  - Python 3.7+
  - 安装 OpenCV：python -m pip install opencv-python-headless

输出:
  - index.html（项目根）
  - vedio/thumbnails/（保存首帧截图）
  - vedio/<video-name>.html（每个视频一个播放页）

"""

import hashlib
import os
import re
import sys
import unicodedata
from pathlib import Path
from html import escape

try:
    import cv2
except ModuleNotFoundError:
    cv2 = None

ROOT = Path(__file__).resolve().parent
VEDIO_DIR = ROOT / 'vedio'
THUMB_DIR = VEDIO_DIR / 'thumbnails'

# Basic templates (mimic the look-and-feel of the provided 1.html and vediotem.html)
INDEX_TEMPLATE = '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Xart - 视频站</title>
  <style>
    /* 简洁样式，灵感来自 1.html */
    body { font-family: "Segoe UI", "PingFang SC", "Microsoft YaHei", Arial, sans-serif; background:#fafafa; color:#333; margin:0 }
    .navbar{height:64px;display:flex;align-items:center;padding:0 5%;background:rgba(255,255,255,0.96);border-bottom:1px solid #eee}
    .logo{font-weight:800; font-size:22px; margin-right:20px}
    .container{width:88%;max-width:1280px;margin:28px auto;padding-bottom:60px}
    .section-title{font-size:20px;font-weight:700;margin-bottom:14px}
    .video-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(220px,1fr));gap:18px}
    .video-card{background:#fff;border-radius:12px;overflow:hidden;box-shadow:0 6px 18px rgba(0,0,0,0.04);cursor:pointer}
    .thumbnail{width:100%;aspect-ratio:16/9;background:#eee;display:block}
    .video-info{padding:10px}
    .video-title{font-size:14px;font-weight:600;color:#333;margin:0 0 6px}
    .video-meta{font-size:12px;color:#999;margin:0}
    a { color:inherit; text-decoration:none }
    footer{padding:22px;text-align:center;color:#aaa}
    @media (max-width:600px){ .container{width:94%} }
  </style>
</head>
<body>
  <header class="navbar"><div class="logo">Xart</div></header>
  <main class="container">
    <h2 class="section-title">全部视频</h2>
    <div class="video-grid">
      {cards}
    </div>
  </main>
  <footer>生成于 generate_site.py</footer>
</body>
</html>
'''

VIDEO_CARD = '''<article class="video-card">
  <a href="{page_rel}">
    <img class="thumbnail" src="{thumb_rel}" alt="{title}">
    <div class="video-info">
      <h3 class="video-title">{title}</h3>
      <p class="video-meta">{filename}</p>
    </div>
  </a>
</article>'''

VIDEO_PAGE_TEMPLATE = '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Xart - {title}</title>
  <style>
    body{{font-family: "Nunito", "PingFang SC", sans-serif; background:#fff7fb; margin:0; display:flex;align-items:center;justify-content:center;min-height:100vh}}
    .video-card{{width:min(92vw,900px);padding:14px;border-radius:22px;background:#fff;box-shadow:0 12px 35px rgba(0,0,0,0.06)}}
    .video-wrap{{border-radius:14px;overflow:hidden;background:#000}}
    video{{width:100%;height:auto;display:block;background:#000}}
    .video-info{{padding:14px 4px 2px}}
    .video-title{{margin:0;color:#333;font-size:18px;font-weight:700}}
    .video-subtitle{{margin:6px 0 0;color:#666;font-size:13px}}
    a.back{{display:inline-block;margin-bottom:10px;color:#999;font-size:13px}}
  </style>
</head>
<body>
  <div style="width:100%;max-width:960px;padding:20px;">
    <a class="back" href="{index_rel}">← 返回首页</a>
    <div class="video-card">
      <div class="video-wrap">
        <video controls preload="metadata" poster="{poster_rel}">
          <source src="{video_rel}" type="video/mp4">
          你的浏览器不支持 HTML5 视频播放。
        </video>
      </div>
      <div class="video-info">
        <h2 class="video-title">{title}</h2>
        <p class="video-subtitle">{subtitle}</p>
      </div>
    </div>
  </div>
</body>
</html>
'''


def slugify(name: str) -> str:
    """Create a Windows-safe slug that avoids Unicode and illegal path characters.

    We keep the human-readable title in the page itself, but use an ASCII + hash-based stub
    for the generated HTML filename and thumbnail filename so Windows filesystem paths remain stable.
    """
    normalized = unicodedata.normalize('NFKD', name)
    ascii_name = normalized.encode('ascii', 'ignore').decode('ascii')
    ascii_name = re.sub(r'[^A-Za-z0-9]+', '-', ascii_name).strip('-').lower()
    if not ascii_name:
        ascii_name = 'video'
    digest = hashlib.md5(name.encode('utf-8')).hexdigest()[:8]
    return f"{ascii_name}-{digest}"[:80]


def extract_thumbnail(video_path: Path, out_path: Path) -> bool:
    """Use OpenCV to grab the first frame of the video as a thumbnail."""
    out_path.parent.mkdir(parents=True, exist_ok=True)
    if cv2 is None:
        return False

    cap = cv2.VideoCapture(str(video_path))
    if not cap.isOpened():
        return False

    try:
        ok, frame = cap.read()
        if not ok or frame is None:
            return False
        return bool(cv2.imwrite(str(out_path), frame))
    finally:
        cap.release()


def main():
    if not VEDIO_DIR.exists() or not VEDIO_DIR.is_dir():
        print(f"错误：未找到 vedio 文件夹，路径：{VEDIO_DIR}")
        sys.exit(1)

    mp4s = [p for p in VEDIO_DIR.iterdir() if p.is_file() and p.suffix.lower() == '.mp4']
    if not mp4s:
        print(f"vedio 文件夹下没有找到 mp4 文件（{VEDIO_DIR}）。")
        sys.exit(1)

    if cv2 is None:
        print("未检测到 OpenCV（cv2），将使用在线占位图作为缩略图（需要联网）。请运行：python -m pip install opencv-python-headless")
    else:
        print("检测到 OpenCV，尝试从视频首帧提取缩略图...")

    cards_html = []

    # Ensure thumb dir exists
    THUMB_DIR.mkdir(parents=True, exist_ok=True)

    for vid in sorted(mp4s):
        filename = vid.name
        title = vid.stem
        slug = slugify(title)
        page_name = f"{slug}.html"
        thumb_name = f"{slug}.jpg"
        thumb_path = THUMB_DIR / thumb_name

        got_thumb = extract_thumbnail(vid, thumb_path)
        if got_thumb:
            thumb_rel = os.path.relpath(thumb_path, ROOT).replace('\\', '/')
        else:
            # fallback to picsum placeholder with a deterministic seed from filename
            seed = abs(hash(filename)) % 1000
            thumb_rel = f"https://picsum.photos/seed/{seed}/640/360"

        page_rel = os.path.relpath(VEDIO_DIR / page_name, ROOT).replace('\\', '/')

        # create card HTML
        card = VIDEO_CARD.format(page_rel=page_rel, thumb_rel=thumb_rel, title=escape(title), filename=escape(filename))
        cards_html.append(card)

        # Create individual video page
        poster_rel = os.path.relpath(thumb_path, VEDIO_DIR).replace('\\', '/') if got_thumb else thumb_rel
        # video_rel should be relative to the video page location (vedio/<file>.mp4)
        video_rel = os.path.relpath(vid, VEDIO_DIR).replace('\\', '/')

        video_page_content = VIDEO_PAGE_TEMPLATE.format(
            title=escape(title),
            poster_rel=poster_rel,
            video_rel=video_rel,
            subtitle=escape(filename),
            index_rel=os.path.relpath(ROOT / 'index.html', VEDIO_DIR).replace('\\', '/')
        )

        page_path = VEDIO_DIR / page_name
        page_path.write_text(video_page_content, encoding='utf-8')
        print(f"生成播放页：{page_path}")

    # Use replace instead of format because INDEX_TEMPLATE contains CSS braces that would
    # be interpreted by str.format. Replace the {cards} token directly.
    index_content = INDEX_TEMPLATE.replace('{cards}', '\n'.join(cards_html))
    (ROOT / 'index.html').write_text(index_content, encoding='utf-8')
    print(f"生成主页：{ROOT / 'index.html'}")
    print("完成。使用 OpenCV 首帧提取缩略图，不依赖外部视频工具。")


if __name__ == '__main__':
    main()
