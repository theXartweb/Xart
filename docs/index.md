---
title: 首页
hide:
   - navigation # 显示右
   - toc #显示左
   - feedback

# comments: true
---
#
<style>
    /* ================= 推荐卡片（自适应） ================= */

    .container{width:88%;max-width:1280px;margin:0 auto;padding:0 0 20px}
    .container + .container{margin-top:0;padding-top:0}
    .section-title{margin:0 0 16px}
    .section-heading{display:flex;align-items:center;justify-content:space-between;gap:16px}
    .more-link{display:inline-flex;align-items:center;gap:7px;margin:0 0 16px;padding:7px 11px;border:1px solid var(--rec-border);border-radius:999px;background:var(--rec-bg);box-shadow:var(--rec-shadow);color:var(--rec-title);font-size:13px;line-height:1;white-space:nowrap;transition:transform .2s ease,box-shadow .2s ease,color .2s ease}
    .more-link span{font-size:16px;line-height:10px;transition:transform .2s ease}
    .more-link:hover{color:var(--md-primary-fg-color);box-shadow:var(--rec-hover-shadow);transform:translateX(2px)}
    .more-link:hover span{transform:translateX(3px)}
    .random-link{display:flex;align-items:center;justify-content:center;gap:12px;width:min(100%,360px);margin:0 auto 28px;padding:15px 22px;border:1px solid rgba(255,255,255,.22);border-radius:999px;background:#1b1b1f;color:#fff;box-shadow:0 0 0 1px rgba(255,255,255,.05),0 10px 24px rgba(0,0,0,.2),0 0 28px rgba(255,76,124,.2);font:inherit;font-size:18px;font-weight:700;letter-spacing:.04em;cursor:pointer;transition:transform .25s ease,box-shadow .25s ease,background .25s ease;animation:randomPulse 2.8s ease-in-out infinite}
    .random-link span{font-size:24px;line-height:1;transition:transform .25s ease}
    .random-link:hover{background:#09090b;box-shadow:0 0 0 1px rgba(255,255,255,.12),0 16px 34px rgba(0,0,0,.3),0 0 38px rgba(255,76,124,.42);transform:translateY(-4px) scale(1.02)}
    .random-link:hover span{transform:translate(4px,-4px) rotate(8deg)}
    @keyframes randomPulse{0%,100%{box-shadow:0 0 0 1px rgba(255,255,255,.05),0 10px 24px rgba(0,0,0,.2),0 0 22px rgba(255,76,124,.16)}50%{box-shadow:0 0 0 1px rgba(255,255,255,.1),0 12px 28px rgba(0,0,0,.24),0 0 34px rgba(255,76,124,.3)}}
    a{color:inherit;text-decoration:none}
    footer{padding:22px;text-align:center;color:#aaa}

    /* ---- 主题变量：默认亮色 ---- */
    .rec-grid{
      --rec-bg:#fff;
      --rec-border:rgba(0,0,0,.06);
      --rec-shadow:0 6px 18px rgba(0,0,0,.06);
      --rec-hover-shadow:0 14px 34px rgba(0,0,0,.14);
      --rec-title:#24242a;
      --rec-meta:#8b8b93;
      --rec-thumb-bg:rgba(128,128,128,.12);
    }
    /* Material 暗色主题下自动切换 */
    [data-md-color-scheme="slate"] .rec-grid{
      --rec-bg:rgba(255,255,255,.07);
      --rec-border:rgba(255,255,255,.1);
      --rec-shadow:0 6px 18px rgba(0,0,0,.28);
      --rec-hover-shadow:0 16px 40px rgba(0,0,0,.5);
      --rec-title:rgba(255,255,255,.92);
      --rec-meta:rgba(255,255,255,.5);
      --rec-thumb-bg:rgba(255,255,255,.08);
    }

    /* ---- 自适应网格：min() 兜底，任意窄屏都不溢出 ---- */
    .rec-grid{
      display:grid;
      grid-template-columns:repeat(auto-fill,minmax(min(100%,190px),1fr));
      gap:16px;
    }

    .rec-card{
      display:flex;
      background:var(--rec-bg);
      border:1px solid var(--rec-border);
      border-radius:14px;
      overflow:hidden;
      box-shadow:var(--rec-shadow);
      cursor:pointer;
      backdrop-filter:blur(10px);
      transition:transform .3s ease,box-shadow .3s ease,border-color .3s ease;
    }
    .rec-card a{display:flex;flex-direction:column;flex:1}
    .rec-card:hover{
      transform:translateY(-5px);
      box-shadow:var(--rec-hover-shadow);
    }

    .rec-thumb{
      position:relative;
      margin:0;
      aspect-ratio:16/9;
      overflow:hidden;
      background:var(--rec-thumb-bg);
    }
    .rec-img{
      width:100%;
      height:100%;
      display:block;
      object-fit:cover;
      transition:transform .45s ease;
    }
    .rec-card:hover .rec-img{transform:scale(1.07)}

    .rec-body{
      display:flex;
      flex-direction:column;
      gap:6px;
      padding:12px 14px 14px;
    }
    .rec-title{
      margin:0;
      font-size:14px;
      font-weight:600;
      line-height:1.4;
      color:var(--rec-title);
      display:-webkit-box;
      -webkit-line-clamp:2;
      -webkit-box-orient:vertical;
      overflow:hidden;
    }
    .rec-meta{
      margin:0;
      font-size:12px;
      color:var(--rec-meta);
      white-space:nowrap;
      overflow:hidden;
      text-overflow:ellipsis;
    }

    /* ---- 断点微调 ---- */
    @media (max-width:900px){ .container{width:92%} }
    @media (max-width:600px){
      .container{width:94%}
      .rec-grid{gap:12px}
      .rec-body{padding:10px 11px 12px;gap:5px}
      .rec-title{font-size:13px}
      .rec-meta{font-size:11px}
    }
    /* 超窄屏强制单列 */
    @media (max-width:340px){
      .rec-grid{grid-template-columns:1fr}
    }
  </style>
  
  






<style>
.xart-article-card {
  width: min(100%, 640px);
  display: grid;
  grid-template-columns: 240px 1fr;
  overflow: hidden;
  border: 1px solid rgba(0, 0, 0, 0.06);
  border-radius: 24px;
  background: #fff;
  box-shadow:
    0 20px 60px rgba(0, 0, 0, 0.08),
    0 2px 8px rgba(0, 0, 0, 0.04);
  cursor: pointer;
  transition:
    transform 0.35s ease,
    box-shadow 0.35s ease;
}

.xart-article-card:hover {
  transform: translateY(-6px);
  box-shadow:
    0 30px 80px rgba(0, 0, 0, 0.12),
    0 4px 12px rgba(0, 0, 0, 0.05);
}

/* Cover */

.xart-article-cover {
  position: relative;
  min-height: 220px;
  overflow: hidden;
  background:
    radial-gradient(
      circle at 30% 20%,
      rgba(139, 92, 246, 0.95),
      transparent 35%
    ),
    radial-gradient(
      circle at 80% 80%,
      rgba(59, 130, 246, 0.9),
      transparent 45%
    ),
    linear-gradient(
      135deg,
      #111827,
      #312e81 55%,
      #6366f1
    );
}

.xart-article-cover::before {
  content: "";
  position: absolute;
  width: 180px;
  height: 180px;
  top: 35px;
  left: 40px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.12);
}

.xart-article-cover::after {
  content: "X";
  position: absolute;
  right: 28px;
  bottom: 5px;
  color: rgba(255, 255, 255, 0.08);
  font-size: 170px;
  font-weight: 800;
  line-height: 1;
  letter-spacing: -15px;
}

.xart-cover-label {
  position: absolute;
  z-index: 2;
  top: 22px;
  left: 22px;
  padding: 7px 11px;
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 999px;
  background: rgba(255, 255, 255, 0.12);
  color: #fff;
  font-size: 11px;
  font-weight: 600;
  letter-spacing: 0.08em;
  backdrop-filter: blur(12px);
}

/* Content */

.xart-article-content {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  padding: 18px 20px;
}

.xart-article-top {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.xart-article-meta {
  display: flex;
  align-items: center;
  gap: 10px;
  color: #8b8b93;
  font-size: 12px;
}

.xart-meta-dot {
  width: 3px;
  height: 3px;
  flex: 0 0 auto;
  border-radius: 50%;
  background: #b5b5bc;
}

.xart-article-title {
  margin: 0;
  color: #15151a;
  font-size: 24px;
  font-weight: 700;
  line-height: 1.3;
  letter-spacing: -0.03em;
}

.xart-article-description {
  margin: 0;
  max-width: 380px;
  overflow: hidden;
  color: #777780;
  font-size: 13px;
  line-height: 1.7;

  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
}

/* Bottom */

.xart-article-bottom {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-top: 14px;
}

.xart-author {
  display: flex;
  align-items: center;
  gap: 10px;
}

.xart-author-avatar {
  width: 32px;
  height: 32px;
  display: grid;
  flex: 0 0 auto;
  place-items: center;
  border-radius: 50%;
  background: linear-gradient(135deg, #111827, #6366f1);
  color: #fff;
  font-size: 11px;
  font-weight: 700;
}

.xart-author-info {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.xart-author-name {
  color: #24242a;
  font-size: 12px;
  font-weight: 600;
}

.xart-author-date {
  color: #9999a1;
  font-size: 10px;
}

.xart-read-button {
  width: 40px;
  height: 40px;
  display: grid;
  flex: 0 0 auto;
  place-items: center;
  border-radius: 50%;
  background: #111;
  color: #fff;
  transition: transform 0.25s ease;
}

.xart-read-button svg {
  width: 16px;
  height: 16px;
}

.xart-article-card:hover .xart-read-button {
  transform: translateX(4px);
}

/* Responsive */

@media (max-width: 620px) {
  .xart-article-card {
    grid-template-columns: 1fr;
    border-radius: 20px;
  }

  .xart-article-cover {
    min-height: 210px;
  }

  .xart-article-cover::after {
    font-size: 130px;
  }

  .xart-article-content {
    padding: 24px;
  }

  .xart-article-title {
    font-size: 23px;
  }

  .xart-article-description {
    font-size: 13px;
  }
}
</style>
<!-- AUTO_REC_CARDS_START -->
<button class="random-link" id="randomLink" type="button">随机色情 <span aria-hidden="true">↗</span></button>
<script>
(function() {
    const randomUrls = ["X图片/blacqkl-(白莉爱吃巧克力)-cosplay-barbara-genshin-impact-118-photos/", "X图片/blacqkl-(白莉爱吃巧克力)-cosplay-kanao-tsuyuri-kimetsu-no-yaiba-89-photos/", "X图片/blacqkl-(白莉爱吃巧克力)-cosplay-kasumizawa-miyu-blue-archive-89-photos/", "X图片/machi馬吉-cosplay-cyrene-honkai-star-rail-104-photos-and-1-video/", "X图片/nekokoyoshi-(爆机少女喵小吉)-and-金鱼kinngyo-cosplay-rem-and-ram-re-zero-103-photos-and-4/", "X图片/柚木-(youmu)-e-cup-natural-beauty-girl-56-photos-and-5-videos/", "X视频/play-me-pornhub-com/", "X视频/sex-table/", "X视频/日本女学生自慰/"];
    const randomLink = document.getElementById("randomLink");
    randomLink.addEventListener("click", function() {
        const target = randomUrls[Math.floor(Math.random() * randomUrls.length)];
        window.location.href = target;
    });
})();
</script>

<div class="section-heading">
<h2 class="section-title">推荐 · X图片</h2>
<a class="more-link" href="X图片/">更多 <span aria-hidden="true">→</span></a>
</div>
<div class="rec-grid">
<article class="rec-card">
  <a href="X图片/blacqkl-(白莉爱吃巧克力)-cosplay-barbara-genshin-impact-118-photos">
    <figure class="rec-thumb">
      <img class="rec-img" src="X图片/image/blacqkl-(白莉爱吃巧克力)-cosplay-barbara-genshin-impact-118-photos/001.webp" alt="Blacqkl (白莉爱吃巧克力) cosplay Barbara - Genshin Impact &quot;118 photos&quot;" loading="lazy">
    </figure>
    <div class="rec-body">
      <h3 class="rec-title">Blacqkl (白莉爱吃巧克力) cosplay Barbara - Genshin Impact &quot;118 photos&quot;</h3>
      <p class="rec-meta">X图片 · 图集精选</p>
    </div>
  </a>
</article>
<article class="rec-card">
  <a href="X图片/blacqkl-(白莉爱吃巧克力)-cosplay-kanao-tsuyuri-kimetsu-no-yaiba-89-photos">
    <figure class="rec-thumb">
      <img class="rec-img" src="X图片/image/blacqkl-(白莉爱吃巧克力)-cosplay-kanao-tsuyuri-kimetsu-no-yaiba-89-photos/001.webp" alt="Blacqkl (白莉爱吃巧克力) cosplay Kanao Tsuyuri - Kimetsu no Yaiba &quot;89 photos&quot;" loading="lazy">
    </figure>
    <div class="rec-body">
      <h3 class="rec-title">Blacqkl (白莉爱吃巧克力) cosplay Kanao Tsuyuri - Kimetsu no Yaiba &quot;89 photos&quot;</h3>
      <p class="rec-meta">X图片 · 图集精选</p>
    </div>
  </a>
</article>
<article class="rec-card">
  <a href="X图片/blacqkl-(白莉爱吃巧克力)-cosplay-kasumizawa-miyu-blue-archive-89-photos">
    <figure class="rec-thumb">
      <img class="rec-img" src="X图片/image/blacqkl-(白莉爱吃巧克力)-cosplay-kasumizawa-miyu-blue-archive-89-photos/001.webp" alt="Blacqkl (白莉爱吃巧克力) cosplay Kasumizawa Miyu - Blue Archive &quot;89 photos&quot;" loading="lazy">
    </figure>
    <div class="rec-body">
      <h3 class="rec-title">Blacqkl (白莉爱吃巧克力) cosplay Kasumizawa Miyu - Blue Archive &quot;89 photos&quot;</h3>
      <p class="rec-meta">X图片 · 图集精选</p>
    </div>
  </a>
</article>
<article class="rec-card">
  <a href="X图片/machi馬吉-cosplay-cyrene-honkai-star-rail-104-photos-and-1-video">
    <figure class="rec-thumb">
      <img class="rec-img" src="X图片/image/machi馬吉-cosplay-cyrene-honkai-star-rail-104-photos-and-1-video/001.webp" alt="Machi馬吉 cosplay Cyrene - Honkai:Star Rail &quot;104 photos and 1 video&quot;" loading="lazy">
    </figure>
    <div class="rec-body">
      <h3 class="rec-title">Machi馬吉 cosplay Cyrene - Honkai:Star Rail &quot;104 photos and 1 video&quot;</h3>
      <p class="rec-meta">X图片 · 图集精选</p>
    </div>
  </a>
</article>
<article class="rec-card">
  <a href="X图片/nekokoyoshi-(爆机少女喵小吉)-and-金鱼kinngyo-cosplay-rem-and-ram-re-zero-103-photos-and-4">
    <figure class="rec-thumb">
      <img class="rec-img" src="X图片/image/nekokoyoshi-(爆机少女喵小吉)-and-金鱼kinngyo-cosplay-rem-and-ram-re-zero-103-photos-and-4/001.webp" alt="Nekokoyoshi (爆机少女喵小吉) and 金鱼kinngyo cosplay Rem and Ram - Re:Zero &quot;103 photos and 4 videos&quot;" loading="lazy">
    </figure>
    <div class="rec-body">
      <h3 class="rec-title">Nekokoyoshi (爆机少女喵小吉) and 金鱼kinngyo cosplay Rem and Ram - Re:Zero &quot;103 photos and 4 videos&quot;</h3>
      <p class="rec-meta">X图片 · 图集精选</p>
    </div>
  </a>
</article>
<article class="rec-card">
  <a href="X图片/柚木-(youmu)-e-cup-natural-beauty-girl-56-photos-and-5-videos">
    <figure class="rec-thumb">
      <img class="rec-img" src="X图片/image/柚木-(youmu)-e-cup-natural-beauty-girl-56-photos-and-5-videos/001.webp" alt="柚木 (Youmu) - E cup natural beauty girl &quot;56 photos and 5 videos&quot;" loading="lazy">
    </figure>
    <div class="rec-body">
      <h3 class="rec-title">柚木 (Youmu) - E cup natural beauty girl &quot;56 photos and 5 videos&quot;</h3>
      <p class="rec-meta">X图片 · 图集精选</p>
    </div>
  </a>
</article>
</div>

<div class="section-heading">
<h2 class="section-title">推荐 · X视频</h2>
<a class="more-link" href="X视频/">更多 <span aria-hidden="true">→</span></a>
</div>
<div class="rec-grid">
<article class="rec-card">
  <a href="X视频/play-me-pornhub-com">
    <figure class="rec-thumb">
      <img class="rec-img" src="https://picsum.photos/seed/play-me---pornhub.com/640/360" alt="Play me - Pornhub.com" loading="lazy">
    </figure>
    <div class="rec-body">
      <h3 class="rec-title">Play me - Pornhub.com</h3>
      <p class="rec-meta">X视频 · 视频精选</p>
    </div>
  </a>
</article>
<article class="rec-card">
  <a href="X视频/sex-table">
    <figure class="rec-thumb">
      <img class="rec-img" src="https://picsum.photos/seed/摩擦台和性高潮湿屄---pornhub.com/640/360" alt="摩擦台和性高潮湿屄 - Pornhub.com" loading="lazy">
    </figure>
    <div class="rec-body">
      <h3 class="rec-title">摩擦台和性高潮湿屄 - Pornhub.com</h3>
      <p class="rec-meta">X视频 · 视频精选</p>
    </div>
  </a>
</article>
<article class="rec-card">
  <a href="X视频/日本女学生自慰">
    <figure class="rec-thumb">
      <img class="rec-img" src="https://picsum.photos/seed/日本女学生寻求刺激--pornhub.com/640/360" alt="日本女学生寻求刺激- Pornhub.com" loading="lazy">
    </figure>
    <div class="rec-body">
      <h3 class="rec-title">日本女学生寻求刺激- Pornhub.com</h3>
      <p class="rec-meta">X视频 · 视频精选</p>
    </div>
  </a>
</article>
</div>
<!-- AUTO_REC_CARDS_END -->
