# -*- coding: utf-8 -*-
"""
바로GO · 구로구 출장마사지 정적 사이트 생성기
- 36개 페이지(메인 1 / 대표 행정동 8 / 보조 생활권 3 / 역세권 11 / 생활권 8 / 기타 5)
- 공통 셸(헤더/푸터/CSS) + 페이지별 고유 본문(중복 콘텐츠 방지)
- Schema: WebPage, BreadcrumbList, Organization, ImageObject
"""
import os, html, json

# ----------------------------------------------------------------------------
# 사이트 공통 설정
# ----------------------------------------------------------------------------
SITE = {
    "name": "바로GO",
    "brand_full": "바로GO 구로구 출장마사지",
    "phone": "0508-202-4719",
    "phone_tel": "0508-202-4719",
    "base": "https://guro-massage1.pages.dev",  # 배포 도메인
    "main_url": "/",
    "og_image": "/assets/img/og-cover.svg",
    "hours": "오전 11시 ~ 익일 오전 5시 (연중무휴)",
    "pay": "현장 결제 (현금·계좌이체), 카드 결제는 사전 문의",
    "cancel": "예약 시간 1시간 전까지 무료 변경·취소 / 이후 이동 시작 시 이동비 발생 가능",
    "area": "서울 구로구 전 지역 방문 (지역별 이동 시간 상이)",
}
OUT = os.path.dirname(os.path.abspath(__file__))

# ----------------------------------------------------------------------------
# 상단 메뉴 (드롭다운 구조)
# ----------------------------------------------------------------------------
NAV = [
    ("구로 홈", SITE["main_url"], []),
    ("지역별 안내", "#", [
        ("신도림동 출장마사지", "/seoul/guro/sindorim-dong-chuljangmassage/"),
        ("구로동 출장마사지", "/seoul/guro/guro-dong-chuljangmassage/"),
        ("가리봉동 출장마사지", "/seoul/guro/garibong-dong-chuljangmassage/"),
        ("고척동 출장마사지", "/seoul/guro/gocheok-dong-chuljangmassage/"),
        ("개봉동 출장마사지", "/seoul/guro/gaebong-dong-chuljangmassage/"),
        ("오류동 출장마사지", "/seoul/guro/oryu-dong-chuljangmassage/"),
        ("수궁동 출장마사지", "/seoul/guro/sugung-dong-chuljangmassage/"),
        ("항동 출장마사지", "/seoul/guro/hang-dong-chuljangmassage/"),
    ]),
    ("역세권 안내", "#", [
        ("신도림역 출장마사지", "/seoul/guro/sindorim-station-chuljangmassage/"),
        ("구로역 출장마사지", "/seoul/guro/guro-station-chuljangmassage/"),
        ("구일역 출장마사지", "/seoul/guro/guil-station-chuljangmassage/"),
        ("개봉역 출장마사지", "/seoul/guro/gaebong-station-chuljangmassage/"),
        ("오류동역 출장마사지", "/seoul/guro/oryu-dong-station-chuljangmassage/"),
        ("온수역 출장마사지", "/seoul/guro/onsu-station-chuljangmassage/"),
        ("천왕역 출장마사지", "/seoul/guro/cheonwang-station-chuljangmassage/"),
        ("남구로역 출장마사지", "/seoul/guro/namguro-station-chuljangmassage/"),
        ("대림역 출장마사지", "/seoul/guro/daerim-station-chuljangmassage/"),
        ("구로디지털단지역 출장마사지", "/seoul/guro/guro-digital-complex-station-chuljangmassage/"),
        ("도림천역 출장마사지", "/seoul/guro/dorimcheon-station-chuljangmassage/"),
    ]),
    ("생활권 안내", "#", [
        ("신도림 생활권", "/seoul/guro/sindorim-area-chuljangmassage/"),
        ("구로디지털단지 생활권", "/seoul/guro/guro-digital-complex-area-chuljangmassage/"),
        ("고척스카이돔 인근", "/seoul/guro/gocheok-skydome-area-chuljangmassage/"),
        ("개봉역 생활권", "/seoul/guro/gaebong-area-chuljangmassage/"),
        ("오류동·천왕 생활권", "/seoul/guro/oryu-cheonwang-area-chuljangmassage/"),
        ("온수역·수궁동 생활권", "/seoul/guro/onsu-sugung-area-chuljangmassage/"),
        ("가리봉동·남구로 생활권", "/seoul/guro/garibong-namguro-area-chuljangmassage/"),
        ("항동 주거지 생활권", "/seoul/guro/hang-dong-area-chuljangmassage/"),
    ]),
    ("예약 안내", "/seoul/guro/reservation/", []),
    ("이용 전 확인", "/seoul/guro/before-visit/", []),
    ("홈타이 가이드", "/seoul/guro/hometai-guide/", []),
    ("고객센터", "/seoul/guro/support/", []),
]

FOOTER_COLS = [
    ("지역별 안내", [
        ("신도림동", "/seoul/guro/sindorim-dong-chuljangmassage/"),
        ("구로동", "/seoul/guro/guro-dong-chuljangmassage/"),
        ("고척동", "/seoul/guro/gocheok-dong-chuljangmassage/"),
        ("개봉동", "/seoul/guro/gaebong-dong-chuljangmassage/"),
        ("오류동", "/seoul/guro/oryu-dong-chuljangmassage/"),
    ]),
    ("역세권 안내", [
        ("신도림역", "/seoul/guro/sindorim-station-chuljangmassage/"),
        ("구로디지털단지역", "/seoul/guro/guro-digital-complex-station-chuljangmassage/"),
        ("개봉역", "/seoul/guro/gaebong-station-chuljangmassage/"),
        ("온수역", "/seoul/guro/onsu-station-chuljangmassage/"),
        ("남구로역", "/seoul/guro/namguro-station-chuljangmassage/"),
    ]),
    ("이용 안내", [
        ("예약 안내", "/seoul/guro/reservation/"),
        ("이용 전 확인사항", "/seoul/guro/before-visit/"),
        ("홈타이 이용 가이드", "/seoul/guro/hometai-guide/"),
        ("고객센터", "/seoul/guro/support/"),
        ("개인정보 처리방침", "/seoul/guro/privacy/"),
    ]),
]

# ----------------------------------------------------------------------------
# 렌더링 헬퍼
# ----------------------------------------------------------------------------
def esc(s): return html.escape(s, quote=True)

def render_nav(current_url):
    items = []
    for label, href, subs in NAV:
        cur = ' aria-current="page"' if href == current_url else ""
        if subs:
            lis = "".join(
                f'<li><a href="{esc(u)}">{esc(t)}</a></li>' for t, u in subs
            )
            items.append(
                f'<li class="nav-item"><a href="{esc(href)}"{cur}>{esc(label)} <span aria-hidden="true">▾</span></a>'
                f'<ul class="dropdown">{lis}</ul></li>'
            )
        else:
            items.append(f'<li class="nav-item"><a href="{esc(href)}"{cur}>{esc(label)}</a></li>')
    menu = "".join(items)
    return f"""<header class="site-header">
  <div class="container">
    <nav class="nav" aria-label="주 메뉴">
      <a class="brand" href="{SITE['main_url']}" aria-label="{esc(SITE['brand_full'])} 홈">
        <span class="mark">바로<b>GO</b></span><span>바로GO</span>
      </a>
      <button class="nav-toggle" aria-label="메뉴 열기" aria-expanded="false" aria-controls="navmenu">☰</button>
      <ul class="nav-menu" id="navmenu">{menu}
        <li class="nav-item"><a class="nav-cta" href="tel:{SITE['phone_tel']}">전화예약 {SITE['phone']}</a></li>
      </ul>
    </nav>
  </div>
</header>"""

def render_footer():
    cols = ""
    for title, links in FOOTER_COLS:
        lis = "".join(f'<li><a href="{esc(u)}">{esc(t)}</a></li>' for t, u in links)
        cols += f'<div class="footer-col"><h4>{esc(title)}</h4><ul>{lis}</ul></div>'
    return f"""<footer class="site-footer">
  <div class="container">
    <div class="footer-grid">
      <div class="footer-brand">
        <a class="brand" href="{SITE['main_url']}"><span class="mark">바로<b>GO</b></span><span>바로GO</span></a>
        <p>서울 구로구 방문형 관리 서비스(출장마사지·홈타이) 지역 안내 사이트입니다. 자택·숙소·사무실 인근 방문 가능 지역과 예약 전 확인사항을 안내합니다.</p>
        <p class="footer-phone"><a href="tel:{SITE['phone_tel']}">전화예약 {SITE['phone']}</a></p>
        <p>운영시간 {esc(SITE['hours'])}</p>
        <div class="footer-cta">
          <a class="btn btn--orange" href="https://t.me/googleseolab" target="_blank" rel="noopener">웹사이트 제작문의</a>
          <a class="btn btn--orange" href="https://t.me/googleseolab" target="_blank" rel="noopener">제휴문의</a>
        </div>
      </div>
      {cols}
    </div>
    <div class="footer-bottom">
      <p class="disclaimer">바로GO는 합법적인 방문형 관리 서비스만 안내하며, 불법·선정적 서비스는 일절 제공하거나 알선하지 않습니다. 본 사이트는 별도의 오프라인 매장 주소를 운영하지 않는 방문형 안내 서비스입니다.</p>
      <p>© 2026 바로GO. All rights reserved. · <a href="/seoul/guro/privacy/">개인정보 처리방침</a> · <a href="/seoul/guro/terms/">이용약관</a></p>
    </div>
  </div>
</footer>
<a class="float-call" href="tel:{SITE['phone_tel']}" aria-label="전화예약 {SITE['phone']}">
  <span class="dot" aria-hidden="true"></span><span class="label">전화예약 {SITE['phone']}</span>
</a>"""

# --- 코스별 기본 요금 ---
def render_pricing():
    tel = SITE["phone_tel"]
    return f"""<section class="pricing" aria-label="코스별 기본 요금">
  <div class="pricing-head">
    <h2>코스별 기본 요금</h2>
    <p>60·90·120분 코스별 기본 요금입니다. 숨겨진 추가 비용 없이 투명하게 안내합니다.</p>
  </div>
  <div class="pricing-grid">
    <div class="price-card">
      <h3>60분 코스</h3>
      <div class="price-amount">90,000<span class="won">원</span></div>
      <div class="price-min">60분</div>
      <p class="price-desc">기본 컨디션·릴랙스 케어</p>
      <a class="btn price-btn-outline" href="tel:{tel}">예약 문의</a>
    </div>
    <div class="price-card is-featured">
      <span class="price-badge">추천</span>
      <h3>90분 코스</h3>
      <div class="price-amount">150,000<span class="won">원</span></div>
      <div class="price-min">90분</div>
      <p class="price-desc">아로마 포함 추천 구성</p>
      <a class="btn btn--gold" href="tel:{tel}">예약 문의</a>
    </div>
    <div class="price-card">
      <h3>120분 코스</h3>
      <div class="price-amount">180,000<span class="won">원</span></div>
      <div class="price-min">120분</div>
      <p class="price-desc">전신 집중 프리미엄 케어</p>
      <a class="btn price-btn-outline" href="tel:{tel}">예약 문의</a>
    </div>
  </div>
  <p class="pricing-note">지역·예약 시간대·이동 거리에 따라 상담 시 최종 확인됩니다. <a href="/seoul/guro/reservation/">상세 요금 안내 보기 →</a></p>
</section>"""

# --- 본문 블록 렌더 ---
def block(b):
    if b[0] == "pricing":
        return render_pricing()
    kind = b[0]
    if kind == "h2":
        return f"<h2>{esc(b[1])}</h2>"
    if kind == "h3":
        return f"<h3>{esc(b[1])}</h3>"
    if kind == "p":
        return f"<p>{b[1]}</p>"  # 본문은 신뢰 가능한 자체 작성, 일부 인라인 링크 허용
    if kind == "ul":
        lis = "".join(f"<li>{esc(x)}</li>" for x in b[1])
        return f"<ul>{lis}</ul>"
    if kind == "check":
        lis = "".join(f"<li>{esc(x)}</li>" for x in b[1])
        return f'<ul class="checklist">{lis}</ul>'
    if kind == "notice":
        cls = "notice notice--info" if (len(b) > 2 and b[2] == "info") else "notice"
        return f'<div class="{cls}">{b[1]}</div>'
    if kind == "table":
        rows = "".join(f"<tr><th>{esc(k)}</th><td>{esc(v)}</td></tr>" for k, v in b[1])
        return f'<table class="info-table"><tbody>{rows}</tbody></table>'
    if kind == "faq":
        items = "".join(
            f"<details><summary>{esc(q)}</summary><p>{esc(a)}</p></details>" for q, a in b[1]
        )
        return f'<div class="faq">{items}</div>'
    if kind == "cards":
        cs = ""
        for t, d, u, tag in b[1]:
            tg = f'<span class="tag">{esc(tag)}</span>' if tag else ""
            cs += (f'<a class="card" href="{esc(u)}">{tg}<h3>{esc(t)}</h3>'
                   f'<p>{esc(d)}</p><span class="card-link">자세히 보기 →</span></a>')
        n = b[2] if len(b) > 2 else 3
        return f'<div class="grid grid--{n}">{cs}</div>'
    return ""

def render_blocks(blocks):
    return "\n".join(block(b) for b in blocks)

# --- Schema (JSON-LD) ---
def schema_blocks(page):
    org = {
        "@type": "Organization",
        "@id": SITE["base"] + "/#org",
        "name": SITE["name"],
        "url": SITE["base"] + SITE["main_url"],
        "telephone": SITE["phone"],
        "areaServed": "서울특별시 구로구",
        "description": "서울 구로구 방문형 관리 서비스(출장마사지·홈타이) 지역 안내",
    }
    crumbs = page.get("crumbs", [])
    crumb_items = []
    for i, (name, url) in enumerate(crumbs, 1):
        item = {"@type": "ListItem", "position": i, "name": name}
        if url:
            item["item"] = SITE["base"] + url
        crumb_items.append(item)
    breadcrumb = {"@type": "BreadcrumbList", "itemListElement": crumb_items}
    image = {
        "@type": "ImageObject",
        "url": SITE["base"] + SITE["og_image"],
        "width": 1200, "height": 630,
        "caption": page["h1"],
    }
    webpage = {
        "@type": "WebPage",
        "@id": SITE["base"] + page["url"] + "#webpage",
        "url": SITE["base"] + page["url"],
        "name": page["title"],
        "description": page["desc"],
        "inLanguage": "ko-KR",
        "isPartOf": {"@id": SITE["base"] + "/#website"},
        "primaryImageOfPage": image,
        "publisher": {"@id": SITE["base"] + "/#org"},
        "breadcrumb": {"@type": "BreadcrumbList", "itemListElement": crumb_items},
    }
    graph = {"@context": "https://schema.org", "@graph": [org, webpage, breadcrumb, image]}
    faq = page.get("faq_schema")
    out = [json.dumps(graph, ensure_ascii=False, indent=2)]
    if faq:
        faq_obj = {
            "@context": "https://schema.org",
            "@type": "FAQPage",
            "mainEntity": [
                {"@type": "Question", "name": q,
                 "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq
            ],
        }
        out.append(json.dumps(faq_obj, ensure_ascii=False, indent=2))
    return "\n".join(f'<script type="application/ld+json">\n{o}\n</script>' for o in out)

def render_breadcrumb(crumbs):
    lis = ""
    for name, url in crumbs:
        if url:
            lis += f'<li><a href="{esc(url)}">{esc(name)}</a></li>'
        else:
            lis += f"<li>{esc(name)}</li>"
    return f'<nav class="breadcrumb" aria-label="현재 위치"><div class="container"><ol>{lis}</ol></div></nav>'

# --- 사이드바(관련 링크 + 예약 카드) ---
def render_sidebar(related):
    links = "".join(f'<li><a href="{esc(u)}">{esc(t)}</a></li>' for t, u in related)
    return f"""<aside class="sidebar">
  <div class="side-card">
    <h4>전화로 바로 예약</h4>
    <p style="font-size:var(--fs-sm);color:var(--color-ink-3);margin:0 0 12px">방문 가능 지역과 예약 가능 시간을 빠르게 확인하세요.</p>
    <a class="btn btn--primary" style="width:100%" href="tel:{SITE['phone_tel']}">전화예약 {SITE['phone']}</a>
    <table class="info-table" style="margin-top:14px;border:none">
      <tbody>
        <tr><th>운영시간</th><td>{esc(SITE['hours'])}</td></tr>
        <tr><th>방문 지역</th><td>구로구 전 지역</td></tr>
      </tbody>
    </table>
  </div>
  <div class="side-card">
    <h4>함께 보면 좋은 안내</h4>
    <ul class="side-links">{links}</ul>
  </div>
</aside>"""

# ----------------------------------------------------------------------------
# 페이지 HTML 조립
# ----------------------------------------------------------------------------
def page_html(page):
    canonical = SITE["base"] + page["url"]
    kw = ", ".join(page.get("keywords", []))
    head = f"""<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(page['title'])}</title>
<meta name="description" content="{esc(page['desc'])}">
<meta name="keywords" content="{esc(kw)}">
<meta name="naver-site-verification" content="deeefa9fb53f1a6d805eb4c64d40cf5add6a10f4">
<link rel="canonical" href="{esc(canonical)}">
<meta name="robots" content="index, follow, max-image-preview:large">
<meta property="og:type" content="website">
<meta property="og:site_name" content="{esc(SITE['name'])}">
<meta property="og:title" content="{esc(page['title'])}">
<meta property="og:description" content="{esc(page['desc'])}">
<meta property="og:url" content="{esc(canonical)}">
<meta property="og:image" content="{esc(SITE['base'] + SITE['og_image'])}">
<meta property="og:locale" content="ko_KR">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{esc(page['title'])}">
<meta name="twitter:description" content="{esc(page['desc'])}">
<meta name="twitter:image" content="{esc(SITE['base'] + SITE['og_image'])}">
<link rel="icon" href="/assets/img/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://cdn.jsdelivr.net" crossorigin>
<link rel="stylesheet" href="/assets/css/style.css">
{schema_blocks(page)}
</head>
<body>
<a class="skip-link" href="#main">본문 바로가기</a>
{render_nav(page['url'])}
{render_breadcrumb(page['crumbs'])}
"""

    # Hero
    hero = f"""<section class="hero">
  <div class="container">
    <span class="eyebrow">{esc(page.get('eyebrow','구로구 출장마사지 · 홈타이'))}</span>
    <h1>{esc(page['h1'])}</h1>
    <p>{page['hero_sub']}</p>
    <div class="hero-actions">
      <a class="btn btn--gold" href="tel:{SITE['phone_tel']}">전화예약 {SITE['phone']}</a>
      <a class="btn btn--outline" href="/seoul/guro/reservation/">예약 안내 보기</a>
    </div>
    <div class="hero-meta">
      <span>● 구로구 전 지역 방문</span>
      <span>● {esc(SITE['hours'])}</span>
      <span>● 합법적 방문형 관리 서비스</span>
    </div>
  </div>
</section>"""

    # Body
    main_inner = render_blocks(page["blocks"])
    if page.get("full_width"):
        body = f'<div class="container">{main_inner}</div>'
    else:
        body = f"""<div class="container">
  <div class="layout">
    <div class="prose">{main_inner}</div>
    {render_sidebar(page.get('related', []))}
  </div>
</div>"""

    main = f'<main id="main" class="section">{body}</main>'
    tail = f"""{render_footer()}
<script src="/assets/js/main.js" defer></script>
</body>
</html>"""
    return head + hero + main + tail

def write_page(page):
    rel = page["url"].strip("/")
    d = os.path.join(OUT, rel)
    os.makedirs(d, exist_ok=True)
    with open(os.path.join(d, "index.html"), "w", encoding="utf-8") as f:
        f.write(page_html(page))

# ----------------------------------------------------------------------------
# 공통 부분 블록
# ----------------------------------------------------------------------------
def trust_blocks(region):
    """페이지별 예약 전 확인사항(지역명만 자연스럽게 삽입, 항목은 공통 신뢰정보)."""
    return [
        ("h2", f"{region} 예약 전 확인사항"),
        ("p", f"{region}에서 방문형 관리 서비스를 예약하기 전에는 아래 항목을 먼저 확인하는 것이 좋습니다. 방문 가능 여부와 이동 시간은 정확한 위치에 따라 달라지므로 전화로 확인 후 예약하시길 권합니다."),
        ("table", [
            ("방문 가능 지역", SITE["area"]),
            ("예약 가능 시간", SITE["hours"]),
            ("추가 이동비", "기본 방문권 외 외곽·심야 시간대는 이동비가 추가될 수 있어 사전 안내"),
            ("결제 방식", SITE["pay"]),
            ("취소 기준", SITE["cancel"]),
            ("개인정보", "예약에 필요한 최소 정보만 수집하며 서비스 종료 후 안전하게 파기"),
        ]),
        ("notice", "바로GO는 자택·숙소·사무실 인근에서 이용하는 <strong>합법적인 방문형 관리 서비스</strong>만 안내합니다. 불법·선정적 서비스는 제공하지 않으며, 허위 후기나 과장된 할인 문구를 사용하지 않습니다."),
    ]

CALL_BLOCK = ("notice", f'예약·상담은 전화로 가장 빠르게 도와드립니다. <strong><a href="tel:{SITE["phone_tel"]}">전화예약 {SITE["phone"]}</a></strong> · 운영시간 {SITE["hours"]}', "info")

PAGES = []

# ============================ 메인 페이지 ============================
PAGES.append({
    "url": SITE["main_url"],
    "title": "구로구 출장마사지｜신도림·구로디지털단지·개봉 홈타이 안내",
    "desc": "구로구 출장마사지·홈타이 예약 전 신도림, 구로동, 개봉, 오류 생활권을 확인하세요.",
    "h1": "구로구 출장마사지 · 구로구 홈타이 지역별 예약 안내",
    "eyebrow": "서울 구로구 방문형 관리 서비스",
    "hero_sub": "신도림·구로디지털단지·고척·개봉·오류·항동까지, 현재 위치 기준 방문 가능 지역과 예약 전 확인사항을 한 곳에서 안내합니다. 자택·숙소·사무실 인근에서 이용하는 합법적인 방문형 관리 서비스입니다.",
    "crumbs": [("구로구 출장마사지", SITE["main_url"])],
    "keywords": ["구로구 출장마사지","구로 출장마사지","구로 홈타이","신도림 출장마사지","구로디지털단지 출장마사지","개봉동 출장마사지","오류동 출장마사지","고척동 출장마사지","남구로역 출장마사지","온수역 출장마사지"],
    "full_width": True,
    "blocks": [
        ("h2", "구로구에서 출장마사지를 찾을 때 먼저 확인할 기준"),
        ("p", "구로구 출장마사지를 찾는 분들은 보통 현재 위치에서 가까운 방문 가능 지역을 먼저 확인합니다. 구로구는 서울 서남권에 있는 지역으로, 신도림역과 구로역을 중심으로 한 교통 생활권, 구로디지털단지역과 남구로역 주변의 업무·상업 생활권, 고척동과 개봉동의 주거 생활권, 오류동·천왕동·온수동·항동으로 이어지는 서남부 주거권이 함께 있습니다. 바로GO는 이 모든 생활권의 방문 기준을 페이지별로 나누어 안내합니다."),
        ("notice", f'예약·상담은 전화가 가장 빠릅니다. <strong><a href="tel:{SITE["phone_tel"]}">전화예약 {SITE["phone"]}</a></strong> · 운영시간 {SITE["hours"]}', "info"),

        ("pricing",),

        ("h2", "신도림·구로디지털단지·개봉·오류 생활권의 차이"),
        ("p", "구로구는 지역마다 분위기와 이동 환경이 다릅니다. 신도림은 1·2호선이 만나는 환승 교통권으로 호텔·오피스가 많고, 구로디지털단지는 IT·벤처 기업이 모인 업무지구입니다. 고척동과 개봉동은 안양천을 낀 조용한 주거권이며, 오류동·수궁동·항동은 아파트 단지가 넓게 자리한 서남부 주거권입니다. 같은 구로구라도 위치에 따라 방문 동선과 이동 시간이 달라지므로, 현재 위치와 가까운 지역 안내를 먼저 확인하시면 편리합니다."),

        ("h2", "대표 행정동별 방문 가능 지역 안내"),
        ("p", "대표 행정동은 신도림동, 구로동, 가리봉동, 고척동, 개봉동, 오류동, 수궁동, 항동으로 구성합니다. 고척1·2동은 고척동으로, 개봉1~3동은 개봉동으로, 오류1·2동은 오류동으로 묶습니다. 수궁동 페이지에서는 궁동과 온수동 생활권을 함께 설명하고, 천왕동은 오류동·천왕 생활권에서 보조로 다룹니다."),
        ("cards", [
            ("신도림동 출장마사지", "신도림역·디큐브시티·도림천 인접 생활권 방문 안내", "/seoul/guro/sindorim-dong-chuljangmassage/", "대표 행정동"),
            ("구로동 출장마사지", "구로역·남구로역·구로디지털단지·구로구청 생활권", "/seoul/guro/guro-dong-chuljangmassage/", "대표 행정동"),
            ("가리봉동 출장마사지", "남구로역·가산 인접권·구로디지털단지 주변", "/seoul/guro/garibong-dong-chuljangmassage/", "대표 행정동"),
            ("고척동 출장마사지", "고척스카이돔·구일역·안양천 주거 생활권", "/seoul/guro/gocheok-dong-chuljangmassage/", "대표 행정동"),
            ("개봉동 출장마사지", "개봉역·개봉시장·구로 서부 주거권", "/seoul/guro/gaebong-dong-chuljangmassage/", "대표 행정동"),
            ("오류동 출장마사지", "오류동역·천왕 인접 생활권 서남부 주거권", "/seoul/guro/oryu-dong-chuljangmassage/", "대표 행정동"),
            ("수궁동 출장마사지", "온수역·궁동·온수동 생활권 통합 안내", "/seoul/guro/sugung-dong-chuljangmassage/", "대표 행정동"),
            ("항동 출장마사지", "항동 주거지·푸른수목원 인근 생활권", "/seoul/guro/hang-dong-chuljangmassage/", "대표 행정동"),
        ], 4),

        ("h2", "신도림역·구로역·개봉역·온수역 역세권 안내"),
        ("p", "지하철로 이동하거나 역 주변에서 머무르실 때는 역세권 안내가 편리합니다. 신도림역·온수역 같은 환승역부터 구로디지털단지역 업무지구, 개봉역 주거권까지 역별로 인근 방문 동선과 이용 기준을 정리했습니다. 현재 위치에서 가까운 역을 선택해 확인하세요."),
        ("cards", [
            ("신도림역 출장마사지", "환승 생활권 중심 방문 기준", "/seoul/guro/sindorim-station-chuljangmassage/", "역세권"),
            ("구로디지털단지역 출장마사지", "구로 업무지구 방문 기준", "/seoul/guro/guro-digital-complex-station-chuljangmassage/", "역세권"),
            ("개봉역 출장마사지", "개봉동 중심 주거권 방문", "/seoul/guro/gaebong-station-chuljangmassage/", "역세권"),
            ("온수역 출장마사지", "수궁동·온수동 환승권 안내", "/seoul/guro/onsu-station-chuljangmassage/", "역세권"),
            ("남구로역 출장마사지", "구로동·가리봉동 인접권", "/seoul/guro/namguro-station-chuljangmassage/", "역세권"),
            ("구로역 출장마사지", "구로동·구로역 인근 방문", "/seoul/guro/guro-station-chuljangmassage/", "역세권"),
        ], 3),

        ("h2", "구로구 홈타이 예약 전 확인사항"),
        ("p", "구로구 출장마사지 예약 전에는 방문 가능 지역, 예약 가능 시간, 추가 이동비, 결제 방식, 취소 기준, 개인정보 처리 기준을 먼저 확인해야 합니다. 신도림·구로디지털단지처럼 교통 접근성이 좋은 지역도 있지만, 항동이나 수궁동 일부 지역은 차량 이동 시간이 달라질 수 있습니다. 정확한 위치를 알려주시면 방문 가능 여부와 예상 이동 시간을 안내해 드립니다."),
        ("table", [
            ("상호", "바로GO"),
            ("전화예약", SITE["phone"]),
            ("방문 가능 지역", SITE["area"]),
            ("예약 가능 시간", SITE["hours"]),
            ("결제 방식", SITE["pay"]),
            ("취소 기준", SITE["cancel"]),
        ]),

        ("h2", "바로GO 구로구 출장마사지를 안심하고 이용하는 이유"),
        ("p", "바로GO는 구로구에서 자택·숙소·사무실 인근으로 방문하는 합법적인 방문형 관리 서비스만 안내합니다. 예약 전에 방문 가능 지역과 비용, 시간을 분명히 안내해 처음 이용하시는 분도 부담 없이 예약하실 수 있습니다."),
        ("check", [
            "허위 후기·가짜 체험담·과장된 할인 문구를 사용하지 않습니다",
            "불법·선정적 서비스는 제공하지 않는 합법적 방문형 관리 서비스입니다",
            "방문 지역·추가 이동비·결제·취소 기준을 예약 전에 명확히 안내합니다",
            "예약에 필요한 최소한의 개인정보만 받고 이용 후 안전하게 파기합니다",
            "정확한 위치를 알려주시면 예상 이동 시간을 미리 안내해 드립니다",
        ]),

        ("h2", "예약부터 방문까지 이용 순서"),
        ("p", "먼저 현재 위치와 가까운 대표 행정동이나 역세권 안내에서 방문 가능 지역과 이동 기준을 확인하세요. 예약 안내에서 가능 시간과 결제·취소 기준을 확인한 뒤, 전화로 정확한 위치를 알려주시면 예약이 완료됩니다. 홈타이가 처음이라면 홈타이 이용 가이드에서 출장마사지와의 차이와 이용 전 준비 사항을 먼저 살펴보시길 권합니다."),
        ("cards", [
            ("예약 안내", "예약 가능 지역·시간·결제·취소 기준 확인", "/seoul/guro/reservation/", "이용 안내"),
            ("이용 전 확인사항", "자택·숙소·사무실 인근 이용 전 점검 항목", "/seoul/guro/before-visit/", "이용 안내"),
            ("홈타이 이용 가이드", "출장마사지와 홈타이 차이, 처음 이용 안내", "/seoul/guro/hometai-guide/", "이용 안내"),
        ], 3),
        ("faq", [
            ("구로구 어디까지 방문 가능한가요?", "신도림동, 구로동, 가리봉동, 고척동, 개봉동, 오류동, 수궁동, 항동 등 구로구 전 지역을 방문합니다. 항동·수궁동 일부 외곽은 이동 시간이 더 걸릴 수 있어 전화로 확인 후 예약을 권합니다."),
            ("출장마사지와 홈타이는 무엇이 다른가요?", "두 용어 모두 방문형 관리 서비스를 가리키며, 홈타이는 자택·숙소에서 받는 형태를 강조하는 표현으로 쓰입니다. 자세한 내용은 홈타이 이용 가이드에서 확인하실 수 있습니다."),
            ("예약은 어떻게 하나요?", f"전화예약 {SITE['phone']}로 현재 위치와 희망 시간을 알려주시면 방문 가능 여부와 예상 이동 시간을 안내해 드립니다."),
        ]),
    ],
    "faq_schema": [
        ("구로구 어디까지 방문 가능한가요?", "신도림동, 구로동, 가리봉동, 고척동, 개봉동, 오류동, 수궁동, 항동 등 구로구 전 지역을 방문합니다. 항동·수궁동 일부 외곽은 이동 시간이 더 걸릴 수 있어 전화로 확인 후 예약을 권합니다."),
        ("출장마사지와 홈타이는 무엇이 다른가요?", "두 용어 모두 방문형 관리 서비스를 가리키며, 홈타이는 자택·숙소에서 받는 형태를 강조하는 표현으로 쓰입니다."),
        ("예약은 어떻게 하나요?", f"전화예약 {SITE['phone']}로 현재 위치와 희망 시간을 알려주시면 방문 가능 여부와 예상 이동 시간을 안내해 드립니다."),
    ],
})


# ---------------------------------------------------------------------------
# 표준 콘텐츠 페이지 빌더 (고유 본문 + 공통 신뢰 블록)
# ---------------------------------------------------------------------------
def content_page(url, title, desc, h1, eyebrow, hero_sub, crumbs, keywords,
                 region, intro_blocks, mid_blocks, related, faq, breadcrumb_extra=None):
    crumbs_full = [("구로 홈", SITE["main_url"])] + crumbs
    blocks = []
    blocks += intro_blocks
    blocks.append(CALL_BLOCK)
    blocks.append(("pricing",))
    blocks += mid_blocks
    blocks += trust_blocks(region)
    if faq:
        blocks.append(("h2", f"{region} 자주 묻는 질문"))
        blocks.append(("faq", faq))
    return {
        "url": url, "title": title, "desc": desc, "h1": h1, "eyebrow": eyebrow,
        "hero_sub": hero_sub, "crumbs": crumbs_full, "keywords": keywords,
        "blocks": blocks, "related": related, "faq_schema": faq,
    }

DIST_CRUMB = ("지역별 안내", None)
STN_CRUMB = ("역세권 안내", None)
AREA_CRUMB = ("생활권 안내", None)

# ============================ 대표 행정동 (8) ============================
PAGES.append(content_page(
    "/seoul/guro/sindorim-dong-chuljangmassage/",
    "신도림동 출장마사지｜신도림역·디큐브시티 생활권 홈타이 안내",
    "신도림동 출장마사지 예약 전 신도림역, 디큐브시티 주변을 확인하세요.",
    "신도림동 출장마사지 · 신도림 생활권 홈타이 안내",
    "신도림동 · 대표 행정동",
    "신도림역 환승 생활권과 디큐브시티, 도림천 인접 주거권까지 신도림동 방문 가능 지역과 예약 전 확인사항을 안내합니다.",
    [DIST_CRUMB, ("신도림동 출장마사지", None)],
    ["신도림동 출장마사지","신도림 출장마사지","신도림 홈타이","신도림역 출장마사지","도림천역 출장마사지"],
    "신도림동",
    [
        ("h2", "신도림동에서 출장마사지를 찾을 때"),
        ("p", "신도림동은 1·2호선 신도림역을 중심으로 사람이 많이 오가는 지역입니다. 디큐브시티와 현대백화점, 테크노마트로 이어지는 상업권과 도림천 인접 주거권이 함께 있어, 같은 신도림동이라도 위치에 따라 방문 동선이 달라집니다. 신도림역과 도림천역 일대를 모두 방문 안내합니다."),
        ("p", "신도림역 일대는 호텔·오피스텔이 밀집해 있어 숙소·사무실 인근 방문 문의가 많습니다. 건물 출입 방법(공동현관 비밀번호·프런트 안내 등)을 미리 확인해 두시면 더 빠르고 편하게 안내받으실 수 있습니다."),
    ],
    [
        ("h2", "신도림동 주요 생활권"),
        ("check", [
            "신도림역·디큐브시티 상업 생활권 — 오피스·호텔·숙소 인근 방문",
            "도림천·도림천역 인접 주거 생활권 — 자택 방문 중심",
            "신도림 테크노마트·현대백화점 인근 — 업무·쇼핑 동선",
        ]),
        ("p", "신도림역 인근은 호텔·오피스텔이 많아 숙소·사무실 인근 방문 문의가 많고, 도림천 방향은 주거지 자택 방문이 많은 편입니다. 정확한 건물 위치를 알려주시면 진입 동선과 예상 이동 시간을 안내해 드립니다."),
    ],
    [("신도림역 출장마사지","/seoul/guro/sindorim-station-chuljangmassage/"),
     ("도림천역 출장마사지","/seoul/guro/dorimcheon-station-chuljangmassage/"),
     ("신도림 생활권 출장마사지","/seoul/guro/sindorim-area-chuljangmassage/"),
     ("구로동 출장마사지","/seoul/guro/guro-dong-chuljangmassage/"),
     ("홈타이 이용 가이드","/seoul/guro/hometai-guide/")],
    [("신도림동 어디까지 방문하나요?","신도림역, 디큐브시티, 도림천역 인근을 포함한 신도림동 전 지역을 방문합니다. 건물 위치를 알려주시면 진입 동선을 함께 안내합니다."),
     ("신도림역에서 숙소로 받을 수 있나요?","네, 신도림역 인근 호텔·숙소 방문이 가능합니다. 숙소 이용 전 확인사항을 참고하시고 전화로 예약해 주세요.")],
))

PAGES.append(content_page(
    "/seoul/guro/guro-dong-chuljangmassage/",
    "구로동 출장마사지｜구로역·구로디지털단지 생활권 안내",
    "구로동 출장마사지·홈타이 이용 전 구로역, 남구로, 디지털단지를 확인하세요.",
    "구로동 출장마사지 · 구로동 홈타이 생활권 안내",
    "구로동 · 대표 행정동",
    "구로1~5동을 모두 포함하는 구로동 전 지역 안내입니다. 구로역·남구로역·구로디지털단지역·구로구청 인근 생활권의 방문 기준을 설명합니다.",
    [DIST_CRUMB, ("구로동 출장마사지", None)],
    ["구로동 출장마사지","구로 출장마사지","구로 홈타이","구로역 출장마사지","남구로역 출장마사지","구로디지털단지 출장마사지"],
    "구로동",
    [
        ("h2", "구로동은 어떤 지역인가요"),
        ("p", "구로동은 구로1동부터 구로5동까지 폭넓게 이어지는 큰 생활권입니다. 구로역, 남구로역, 구로디지털단지역, 구로구청 인근까지 모두 구로동 생활권에 포함되며, 번호와 관계없이 구로동 전 지역을 방문합니다."),
        ("p", "구로동은 업무지구와 주거지가 함께 있는 지역입니다. 구로디지털단지 주변은 사무실 인근 방문이 많고, 남구로역 주변은 주거지와 상권이 함께 있어 자택·숙소 방문도 잦습니다. 위치에 따라 이동 동선이 달라지므로 정확한 주소를 알려주시면 예상 시간을 안내해 드립니다."),
    ],
    [
        ("h2", "구로동 주요 생활권"),
        ("check", [
            "구로역 인근 — 신도림 방향 환승권과 주거·상업 혼합권",
            "구로디지털단지역 인근 — IT 업무지구, 사무실 인근 방문 다수",
            "남구로역 인근 — 주거지와 상권이 함께 있는 생활권",
            "구로구청·구로시장 인근 — 행정·생활 중심 주거권",
        ]),
        ("p", "대림역은 구로·영등포 경계에 있어 구로동에서 가까운 인접 생활권으로 함께 안내합니다. 구로디지털단지역 일대는 업무지구라 역세권 안내에서 더 자세히 확인하실 수 있습니다."),
    ],
    [("구로역 출장마사지","/seoul/guro/guro-station-chuljangmassage/"),
     ("남구로역 출장마사지","/seoul/guro/namguro-station-chuljangmassage/"),
     ("구로디지털단지역 출장마사지","/seoul/guro/guro-digital-complex-station-chuljangmassage/"),
     ("구로디지털단지 생활권 출장마사지","/seoul/guro/guro-digital-complex-area-chuljangmassage/"),
     ("예약 안내","/seoul/guro/reservation/")],
    [("구로1동, 구로2동도 방문하나요?","네. 구로1동부터 구로5동까지 모두 구로동 생활권으로 방문이 가능합니다. 정확한 위치를 알려주시면 동선을 안내합니다."),
     ("구로디지털단지 사무실로 방문되나요?","네, 사무실 인근 방문이 가능합니다. 사무실 인근 이용 전 확인사항을 참고해 주세요.")],
))

PAGES.append(content_page(
    "/seoul/guro/garibong-dong-chuljangmassage/",
    "가리봉동 출장마사지｜남구로역·가산 인접 생활권 안내",
    "가리봉동 출장마사지 예약 전 남구로역, 가산 인접 생활권을 확인하세요.",
    "가리봉동 출장마사지 · 남구로역 인접 생활권 안내",
    "가리봉동 · 대표 행정동",
    "남구로역과 가산디지털단지 인접권, 구로디지털단지 주변 생활권으로 연결되는 가리봉동의 방문 기준을 안내합니다.",
    [DIST_CRUMB, ("가리봉동 출장마사지", None)],
    ["가리봉동 출장마사지","가리봉 출장마사지","가리봉 홈타이","남구로역 출장마사지"],
    "가리봉동",
    [
        ("h2", "가리봉동 방문 가능 지역"),
        ("p", "가리봉동은 남구로역과 가산디지털단지역 인접권, 구로디지털단지 주변 생활권과 연결되는 지역입니다. 주거지와 상권, 업무지구가 가까이 있어 자택·숙소·사무실 인근 방문 문의가 고르게 들어옵니다. 남구로 생활권과 함께 방문 안내합니다."),
        ("p", "가산디지털단지역은 가리봉동과 맞닿아 있지만 행정구역상 금천구에 가깝습니다. 가산 경계 지역은 위치에 따라 방문 가능 여부가 달라질 수 있어, 전화로 확인 후 안내해 드립니다."),
    ],
    [
        ("h2", "가리봉동 주요 생활권"),
        ("check", [
            "남구로역 인근 — 주거지·상권 혼합 생활권",
            "구로디지털단지 인접권 — 업무지구 사무실 인근 방문",
            "가산디지털단지 인접권 — 금천구 경계, 인접 생활권으로 안내",
        ]),
    ],
    [("남구로역 출장마사지","/seoul/guro/namguro-station-chuljangmassage/"),
     ("구로동 출장마사지","/seoul/guro/guro-dong-chuljangmassage/"),
     ("가리봉동·남구로 생활권 출장마사지","/seoul/guro/garibong-namguro-area-chuljangmassage/"),
     ("예약 안내","/seoul/guro/reservation/")],
    [("가리봉동에서 가산 쪽도 방문하나요?","가리봉동과 인접한 가산 경계 지역은 위치에 따라 방문 가능합니다. 가산디지털단지 중심부는 금천구 안내가 더 정확할 수 있어 전화로 확인 후 예약을 권합니다.")],
))

PAGES.append(content_page(
    "/seoul/guro/gocheok-dong-chuljangmassage/",
    "고척동 출장마사지｜고척스카이돔·구일역 인근 안내",
    "고척동 출장마사지·홈타이 이용 전 고척스카이돔, 구일역 주변을 확인하세요.",
    "고척동 출장마사지 · 고척스카이돔 인근 생활권 안내",
    "고척동 · 대표 행정동",
    "고척1·2동을 모두 포함하는 고척동 전 지역 안내입니다. 고척스카이돔, 구일역, 안양천 인근 주거 생활권 방문 기준을 설명합니다.",
    [DIST_CRUMB, ("고척동 출장마사지", None)],
    ["고척동 출장마사지","고척 출장마사지","고척 홈타이","구일역 출장마사지","고척스카이돔 출장마사지"],
    "고척동",
    [
        ("h2", "고척동은 주거 생활권 중심입니다"),
        ("p", "고척동은 고척1동과 고척2동을 아우르는 지역으로, 번호와 관계없이 고척동 전 지역을 방문합니다. 고척스카이돔, 구일역, 안양천 인근으로 이어지는 조용한 주거 생활권이 중심이며, 신도림이나 구로디지털단지 같은 번화가와는 분위기가 다릅니다. 주거지 방문과 고척스카이돔 인근 이동 기준을 중심으로 안내해 드립니다."),
    ],
    [
        ("h2", "고척동 주요 생활권"),
        ("check", [
            "고척스카이돔 인근 — 행사일 교통 혼잡 시 이동 시간 변동",
            "구일역 인근 — 안양천 방향 주거권 자택 방문",
            "고척근린공원·안양천 인접 — 조용한 주거 생활권",
        ]),
        ("p", "고척스카이돔은 야구 경기나 공연이 있는 날 주변 교통이 혼잡해질 수 있어, 이런 날에는 예상 이동 시간을 넉넉히 잡고 예약하시는 것이 좋습니다."),
    ],
    [("구일역 출장마사지","/seoul/guro/guil-station-chuljangmassage/"),
     ("고척스카이돔 인근 출장마사지","/seoul/guro/gocheok-skydome-area-chuljangmassage/"),
     ("개봉동 출장마사지","/seoul/guro/gaebong-dong-chuljangmassage/"),
     ("이용 전 확인사항","/seoul/guro/before-visit/")],
    [("고척스카이돔 경기 있는 날도 방문되나요?","네, 방문 가능합니다. 다만 경기·공연일에는 주변 도로가 혼잡할 수 있어 이동 시간이 평소보다 길어질 수 있습니다.")],
))

PAGES.append(content_page(
    "/seoul/guro/gaebong-dong-chuljangmassage/",
    "개봉동 출장마사지｜개봉역·구로 서부 주거권 안내",
    "개봉동 출장마사지 예약 전 개봉역, 구로 서부 주거권을 확인하세요.",
    "개봉동 출장마사지 · 구로 서부 주거권 안내",
    "개봉동 · 대표 행정동",
    "개봉1~3동을 모두 포함하는 개봉동 전 지역 안내입니다. 개봉역, 개봉시장, 구로 서부 주거권 방문 기준을 설명합니다.",
    [DIST_CRUMB, ("개봉동 출장마사지", None)],
    ["개봉동 출장마사지","개봉 출장마사지","개봉 홈타이","개봉역 출장마사지"],
    "개봉동",
    [
        ("h2", "개봉동은 어떤 지역인가요"),
        ("p", "개봉동은 개봉1동부터 개봉3동까지 아우르는 지역으로, 번호와 관계없이 개봉동 전 지역을 방문합니다. 개봉역과 개봉시장을 중심으로 한 구로 서부 주거권이 핵심이며, 아파트와 빌라가 어우러진 생활 밀착형 주거 지역입니다. 자택 방문 문의가 특히 많습니다."),
    ],
    [
        ("h2", "개봉동 주요 생활권"),
        ("check", [
            "개봉역·개봉시장 인근 — 생활 중심 주거권",
            "개봉1·2·3동 주거권 — 아파트·빌라 밀집 자택 방문",
            "안양천·광명 경계 인접권 — 서부 주거 생활권",
        ]),
    ],
    [("개봉역 출장마사지","/seoul/guro/gaebong-station-chuljangmassage/"),
     ("개봉역 생활권 출장마사지","/seoul/guro/gaebong-area-chuljangmassage/"),
     ("오류동 출장마사지","/seoul/guro/oryu-dong-chuljangmassage/"),
     ("예약 안내","/seoul/guro/reservation/")],
    [("개봉1동, 개봉3동도 방문하나요?","네. 개봉1~3동 모두 개봉동 생활권으로 방문이 가능합니다.")],
))

PAGES.append(content_page(
    "/seoul/guro/oryu-dong-chuljangmassage/",
    "오류동 출장마사지｜오류동역·천왕 인접 생활권 안내",
    "오류동 출장마사지·홈타이 이용 전 오류동역, 천왕 인접권을 확인하세요.",
    "오류동 출장마사지 · 서남부 주거 생활권 안내",
    "오류동 · 대표 행정동",
    "오류1·2동을 모두 포함하는 오류동 전 지역 안내입니다. 오류동역과 천왕역, 천왕동 인접 생활권 방문 기준을 설명합니다.",
    [DIST_CRUMB, ("오류동 출장마사지", None)],
    ["오류동 출장마사지","오류 출장마사지","오류 홈타이","오류동역 출장마사지","천왕역 출장마사지"],
    "오류동",
    [
        ("h2", "오류동과 서남부 생활권"),
        ("p", "오류동은 오류1동과 오류2동을 아우르는 지역으로, 번호와 관계없이 오류동 전 지역을 방문합니다. 오류동역과 천왕역, 천왕동 인접 생활권까지 이어지는 서남부 주거권이며, 인접한 천왕동도 함께 방문 안내합니다. 구로구 서남부는 도심보다 차량 이동 시간이 더 걸릴 수 있어 예상 시간을 미리 안내해 드립니다."),
    ],
    [
        ("h2", "오류동 주요 생활권"),
        ("check", [
            "오류동역 인근 — 1호선 주거권 중심 생활권",
            "천왕동·천왕역 인접권 — 서부 주거 생활권 (보조 안내)",
            "오류시장·경인로 인근 — 생활 중심권",
        ]),
    ],
    [("오류동역 출장마사지","/seoul/guro/oryu-dong-station-chuljangmassage/"),
     ("천왕역 출장마사지","/seoul/guro/cheonwang-station-chuljangmassage/"),
     ("오류동·천왕 생활권 출장마사지","/seoul/guro/oryu-cheonwang-area-chuljangmassage/"),
     ("수궁동 출장마사지","/seoul/guro/sugung-dong-chuljangmassage/"),
     ("예약 안내","/seoul/guro/reservation/")],
    [("천왕동도 방문하나요?","네. 천왕동은 오류동·천왕 생활권으로 함께 안내하며 방문이 가능합니다.")],
))

PAGES.append(content_page(
    "/seoul/guro/sugung-dong-chuljangmassage/",
    "수궁동 출장마사지｜온수역·궁동·온수동 생활권 안내",
    "수궁동 출장마사지 예약 전 온수역, 궁동, 온수동 주변을 확인하세요.",
    "수궁동 출장마사지 · 온수·궁동 생활권 안내",
    "수궁동 · 대표 행정동",
    "수궁동과 함께 궁동·온수동 생활권까지 방문 안내합니다. 온수역 환승권과 주거 생활권 방문 기준을 설명합니다.",
    [DIST_CRUMB, ("수궁동 출장마사지", None)],
    ["수궁동 출장마사지","온수동 출장마사지","궁동 출장마사지","온수역 출장마사지","수궁동 홈타이"],
    "수궁동",
    [
        ("h2", "수궁동은 궁동·온수동을 함께 안내합니다"),
        ("p", "수궁동은 행정동으로, 법정동인 궁동과 온수동을 포함합니다. 1·7호선 온수역을 중심으로 한 환승권과 조용한 주거권이 함께 있는 지역으로, 궁동·온수동을 포함한 수궁동 전 지역을 방문 안내합니다."),
    ],
    [
        ("h2", "수궁동 주요 생활권"),
        ("check", [
            "온수역 인근 — 1·7호선 환승권, 숙소·사무실 인근 방문",
            "궁동 주거권 — 조용한 자택 방문 중심 생활권",
            "온수동 주거권 — 부천 경계 인접 서부 주거권",
        ]),
    ],
    [("온수역 출장마사지","/seoul/guro/onsu-station-chuljangmassage/"),
     ("온수역·수궁동 생활권 출장마사지","/seoul/guro/onsu-sugung-area-chuljangmassage/"),
     ("항동 출장마사지","/seoul/guro/hang-dong-chuljangmassage/"),
     ("개인정보 처리방침","/seoul/guro/privacy/")],
    [("궁동과 온수동도 방문하나요?","네. 궁동과 온수동은 수궁동 생활권으로 함께 방문이 가능합니다.")],
))

PAGES.append(content_page(
    "/seoul/guro/hang-dong-chuljangmassage/",
    "항동 출장마사지｜항동 주거지·푸른수목원 인근 안내",
    "항동 출장마사지·홈타이 이용 전 항동 주거지 방문 기준을 확인하세요.",
    "항동 출장마사지 · 항동 주거지 생활권 안내",
    "항동 · 대표 행정동",
    "항동 주거지와 푸른수목원 인근 생활권을 중심으로 항동 방문 가능 지역과 이동 기준을 안내합니다.",
    [DIST_CRUMB, ("항동 출장마사지", None)],
    ["항동 출장마사지","항동 홈타이","항동지구 출장마사지","푸른수목원 출장마사지"],
    "항동",
    [
        ("h2", "항동 주거지 방문 안내"),
        ("p", "항동은 항동지구 신규 주거단지와 푸른수목원 인근 생활권이 중심인 구로구 서남부 지역입니다. 신도림·구로디지털단지 같은 도심 교통권과는 거리가 있어 차량 이동 시간이 더 걸릴 수 있어, 항동 주거지의 이동 기준을 미리 명확히 안내해 드립니다."),
    ],
    [
        ("h2", "항동 주요 생활권"),
        ("check", [
            "항동지구 아파트 단지 — 자택 방문 중심 신규 주거권",
            "푸른수목원 인근 — 조용한 주거·녹지 생활권",
            "성공회대·부천 경계 인접권 — 서남부 외곽 생활권",
        ]),
        ("p", "항동은 외곽 주거권이라 예상 이동 시간을 넉넉히 안내해 드리며, 정확한 단지·동·호수를 알려주시면 진입 동선을 함께 확인합니다."),
    ],
    [("항동 주거지 생활권 출장마사지","/seoul/guro/hang-dong-area-chuljangmassage/"),
     ("수궁동 출장마사지","/seoul/guro/sugung-dong-chuljangmassage/"),
     ("오류동 출장마사지","/seoul/guro/oryu-dong-chuljangmassage/"),
     ("예약 전 확인사항","/seoul/guro/before-visit/")],
    [("항동도 방문 가능한가요?","네, 항동지구와 푸른수목원 인근까지 방문 가능합니다. 외곽 지역 특성상 이동 시간이 더 걸릴 수 있어 전화로 예약을 권합니다.")],
))


# ============================ 법정동·생활권 보조 (3) ============================
PAGES.append(content_page(
    "/seoul/guro/cheonwang-area-chuljangmassage/",
    "천왕동 생활권 출장마사지｜천왕역·오류동 인접 안내",
    "천왕동 생활권 출장마사지 예약 전 천왕역, 오류동 인접권을 확인하세요.",
    "천왕동 생활권 출장마사지 안내",
    "천왕동 · 생활권 보조 안내",
    "천왕동은 오류동·천왕 생활권으로 묶어 안내하는 법정동입니다. 천왕역과 천왕지구 주거권 방문 기준을 설명합니다.",
    [AREA_CRUMB, ("천왕동 생활권", None)],
    ["천왕동 출장마사지","천왕역 출장마사지","천왕지구 출장마사지"],
    "천왕동",
    [
        ("h2", "천왕동은 오류동과 함께 안내합니다"),
        ("p", "천왕동은 행정구역상 오류동과 가까운 서남부 생활권으로, 바로GO는 천왕동을 단독 행정동 페이지가 아닌 오류동·천왕 생활권 보조 안내로 다룹니다. 천왕역과 천왕지구 아파트 단지를 중심으로 한 조용한 주거권이 특징이며, 자택 방문 문의가 많습니다."),
    ],
    [
        ("h2", "천왕동 주요 생활권"),
        ("check", [
            "천왕역 인근 — 7호선 주거권, 천왕지구 단지 방문",
            "천왕지구 아파트 — 자택 방문 중심 신규 주거권",
            "오류동 경계 인접권 — 서남부 생활권 연결",
        ]),
    ],
    [("천왕역 출장마사지","/seoul/guro/cheonwang-station-chuljangmassage/"),
     ("오류동·천왕 생활권 출장마사지","/seoul/guro/oryu-cheonwang-area-chuljangmassage/"),
     ("오류동 출장마사지","/seoul/guro/oryu-dong-chuljangmassage/"),
     ("예약 안내","/seoul/guro/reservation/")],
    [("천왕지구 아파트도 방문하나요?","네, 천왕지구 단지 자택 방문이 가능합니다. 단지·동·호수를 알려주시면 진입 동선을 안내합니다.")],
))

PAGES.append(content_page(
    "/seoul/guro/onsu-area-chuljangmassage/",
    "온수동 생활권 출장마사지｜온수역·수궁동 인접 안내",
    "온수동 생활권 출장마사지 예약 전 온수역, 수궁동 인접권을 확인하세요.",
    "온수동 생활권 출장마사지 안내",
    "온수동 · 생활권 보조 안내",
    "온수동은 수궁동·온수역 생활권과 함께 방문하는 법정동입니다. 온수역 인근 주거·환승 생활권 방문 기준을 설명합니다.",
    [AREA_CRUMB, ("온수동 생활권", None)],
    ["온수동 출장마사지","온수역 출장마사지","온수 홈타이"],
    "온수동",
    [
        ("h2", "온수동은 수궁동·온수역과 함께 안내합니다"),
        ("p", "온수동은 수궁동에 속한 법정동으로, 수궁동·온수역 생활권과 함께 방문 안내합니다. 1·7호선 온수역 환승권과 부천 경계 인접 주거권이 함께 있어, 숙소·사무실 인근과 자택 방문 문의가 고르게 들어옵니다."),
    ],
    [
        ("h2", "온수동 주요 생활권"),
        ("check", [
            "온수역 인근 — 1·7호선 환승권, 숙소·사무실 인근",
            "온수동 주거권 — 부천 경계 인접 서부 주거권",
            "수궁동·궁동 연결권 — 조용한 생활권",
        ]),
    ],
    [("온수역 출장마사지","/seoul/guro/onsu-station-chuljangmassage/"),
     ("수궁동 출장마사지","/seoul/guro/sugung-dong-chuljangmassage/"),
     ("온수역·수궁동 생활권 출장마사지","/seoul/guro/onsu-sugung-area-chuljangmassage/"),
     ("이용 전 확인사항","/seoul/guro/before-visit/")],
    [("온수동에서 부천 경계 쪽도 방문하나요?","온수동 내 위치는 방문 가능하며, 부천 경계를 넘는 지역은 전화로 확인 후 안내해 드립니다.")],
))

PAGES.append(content_page(
    "/seoul/guro/gung-dong-area-chuljangmassage/",
    "궁동 생활권 출장마사지｜수궁동·온수역 인접 안내",
    "궁동 생활권 출장마사지 예약 전 수궁동, 온수역 인접권을 확인하세요.",
    "궁동 생활권 출장마사지 안내",
    "궁동 · 생활권 보조 안내",
    "궁동은 수궁동 생활권과 함께 방문하는 법정동입니다. 궁동 근린공원 인근 조용한 주거 생활권 방문 기준을 설명합니다.",
    [AREA_CRUMB, ("궁동 생활권", None)],
    ["궁동 출장마사지","궁동 홈타이","수궁동 출장마사지"],
    "궁동",
    [
        ("h2", "궁동은 수궁동 생활권으로 안내합니다"),
        ("p", "궁동은 수궁동에 속한 법정동으로, 수궁동 생활권과 함께 방문 안내합니다. 궁동저수지·궁동근린공원 인근의 조용한 주거권이 특징이며, 자택 방문 문의가 많은 지역입니다. 온수역 환승권과도 가까워 이동 동선을 함께 안내해 드립니다."),
    ],
    [
        ("h2", "궁동 주요 생활권"),
        ("check", [
            "궁동근린공원·궁동저수지 인근 — 녹지 주거권",
            "온수역 인접권 — 1·7호선 환승 동선 연결",
            "수궁동 연결 주거권 — 자택 방문 중심",
        ]),
    ],
    [("수궁동 출장마사지","/seoul/guro/sugung-dong-chuljangmassage/"),
     ("온수역 출장마사지","/seoul/guro/onsu-station-chuljangmassage/"),
     ("온수역·수궁동 생활권 출장마사지","/seoul/guro/onsu-sugung-area-chuljangmassage/"),
     ("예약 안내","/seoul/guro/reservation/")],
    [("궁동도 방문 가능한가요?","네, 궁동 주거권 자택 방문이 가능합니다. 정확한 위치를 알려주시면 이동 시간을 안내합니다.")],
))

# ============================ 역세권 (11) ============================
PAGES.append(content_page(
    "/seoul/guro/sindorim-station-chuljangmassage/",
    "신도림역 출장마사지｜신도림동 환승 생활권 홈타이 안내",
    "신도림역 출장마사지 예약 전 신도림동 환승 생활권을 확인하세요.",
    "신도림역 출장마사지 · 환승 생활권 안내",
    "신도림역 · 역세권 안내",
    "1·2호선 신도림역 환승 생활권을 중심으로 디큐브시티, 호텔·오피스 인근 방문 기준을 안내합니다. 역명 기준 하나의 페이지로 운영합니다.",
    [STN_CRUMB, ("신도림역 출장마사지", None)],
    ["신도림역 출장마사지","신도림 출장마사지","신도림역 홈타이"],
    "신도림역",
    [
        ("h2", "신도림역 환승 생활권 방문 안내"),
        ("p", "신도림역은 1호선과 2호선이 만나는 환승역으로, 디큐브시티와 호텔·오피스텔이 밀집해 숙소·사무실 인근 방문 문의가 많습니다. 1호선·2호선 어느 노선을 이용하셔도 동일하게 신도림역 일대를 방문 안내해 드립니다."),
    ],
    [
        ("h2", "신도림역 인근 방문 포인트"),
        ("check", [
            "디큐브시티·디큐브호텔 인근 — 숙소 방문 다수",
            "신도림역 오피스·테크노마트 — 사무실 인근 방문",
            "도림천 방향 주거권 — 자택 방문 동선 연결",
        ]),
    ],
    [("신도림동 출장마사지","/seoul/guro/sindorim-dong-chuljangmassage/"),
     ("신도림 생활권 출장마사지","/seoul/guro/sindorim-area-chuljangmassage/"),
     ("도림천역 출장마사지","/seoul/guro/dorimcheon-station-chuljangmassage/"),
     ("예약 안내","/seoul/guro/reservation/")],
    [("신도림역 호텔로 방문되나요?","네, 신도림역 인근 호텔·숙소 방문이 가능합니다. 숙소 이용 전 확인사항을 참고해 주세요.")],
))

PAGES.append(content_page(
    "/seoul/guro/guro-station-chuljangmassage/",
    "구로역 출장마사지｜구로동·구로역 인근 방문 안내",
    "구로역 출장마사지 예약 전 구로동, 구로역 인근 방문 기준을 확인하세요.",
    "구로역 출장마사지 · 구로역 인근 방문 안내",
    "구로역 · 역세권 안내",
    "1호선 구로역 인근 주거·상업 혼합 생활권 방문 기준을 안내합니다. 구로동 안내와 함께 보시면 동선 파악에 도움이 됩니다.",
    [STN_CRUMB, ("구로역 출장마사지", None)],
    ["구로역 출장마사지","구로 출장마사지","구로역 홈타이"],
    "구로역",
    [
        ("h2", "구로역 인근 방문 안내"),
        ("p", "구로역은 1호선 주요 역으로 신도림 방향 환승 동선과 가깝고, AK플라자 인근 상업권과 주거권이 함께 있습니다. 구로역 인근은 구로동 생활권의 일부로, 더 넓은 구로동 안내도 함께 확인하실 수 있습니다."),
    ],
    [
        ("h2", "구로역 인근 방문 포인트"),
        ("check", [
            "구로역·AK플라자 인근 — 상업권 숙소·사무실 방문",
            "구로역 주변 아파트·주거권 — 자택 방문",
            "신도림 방향 인접권 — 환승 동선 연결",
        ]),
    ],
    [("구로동 출장마사지","/seoul/guro/guro-dong-chuljangmassage/"),
     ("남구로역 출장마사지","/seoul/guro/namguro-station-chuljangmassage/"),
     ("신도림역 출장마사지","/seoul/guro/sindorim-station-chuljangmassage/"),
     ("예약 안내","/seoul/guro/reservation/")],
    [("구로역과 구로동은 어떻게 다른가요?","구로역 페이지는 역 주변 이동 기준을, 구로동 페이지는 구 전체 생활권을 안내합니다. 두 페이지를 함께 보면 동선 파악에 도움이 됩니다.")],
))

PAGES.append(content_page(
    "/seoul/guro/guil-station-chuljangmassage/",
    "구일역 출장마사지｜고척동·안양천 생활권 안내",
    "구일역 출장마사지 예약 전 고척동, 안양천 생활권을 확인하세요.",
    "구일역 출장마사지 · 고척동 생활권 안내",
    "구일역 · 역세권 안내",
    "1호선 구일역과 안양천, 고척스카이돔 인근 주거 생활권 방문 기준을 안내합니다.",
    [STN_CRUMB, ("구일역 출장마사지", None)],
    ["구일역 출장마사지","고척동 출장마사지","구일역 홈타이"],
    "구일역",
    [
        ("h2", "구일역 인근 방문 안내"),
        ("p", "구일역은 1호선 역으로 안양천을 사이에 두고 고척동과 인접해 있습니다. 고척스카이돔과 가까워 행사일에는 주변 교통이 혼잡할 수 있으며, 평소에는 조용한 주거권 자택 방문이 많은 지역입니다."),
    ],
    [
        ("h2", "구일역 인근 방문 포인트"),
        ("check", [
            "고척스카이돔 인근 — 행사일 이동 시간 변동 가능",
            "안양천 방향 주거권 — 자택 방문 중심",
            "고척동 아파트 단지 — 생활 주거권",
        ]),
    ],
    [("고척동 출장마사지","/seoul/guro/gocheok-dong-chuljangmassage/"),
     ("고척스카이돔 인근 출장마사지","/seoul/guro/gocheok-skydome-area-chuljangmassage/"),
     ("개봉동 출장마사지","/seoul/guro/gaebong-dong-chuljangmassage/"),
     ("이용 전 확인사항","/seoul/guro/before-visit/")],
    [("구일역 근처 고척동도 방문하나요?","네, 구일역과 인접한 고척동 주거권 전 지역을 방문합니다.")],
))

PAGES.append(content_page(
    "/seoul/guro/gaebong-station-chuljangmassage/",
    "개봉역 출장마사지｜개봉동 중심 주거권 안내",
    "개봉역 출장마사지 예약 전 개봉동 중심 주거권을 확인하세요.",
    "개봉역 출장마사지 · 개봉동 주거권 안내",
    "개봉역 · 역세권 안내",
    "1호선 개봉역과 개봉시장 중심 주거권 방문 기준을 안내합니다. 개봉동 안내와 함께 보시면 좋습니다.",
    [STN_CRUMB, ("개봉역 출장마사지", None)],
    ["개봉역 출장마사지","개봉동 출장마사지","개봉역 홈타이"],
    "개봉역",
    [
        ("h2", "개봉역 인근 방문 안내"),
        ("p", "개봉역은 1호선 역으로 개봉시장과 구로 서부 주거권의 중심에 있습니다. 역 주변 방문 동선을 중심으로 안내하며, 주거지와 세부 생활권은 개봉동 안내에서 함께 확인하실 수 있습니다."),
    ],
    [
        ("h2", "개봉역 인근 방문 포인트"),
        ("check", [
            "개봉역·개봉시장 인근 — 생활 중심 상업권",
            "개봉1·2·3동 주거권 — 자택 방문 중심",
            "광명 경계 인접권 — 서부 주거 생활권",
        ]),
    ],
    [("개봉동 출장마사지","/seoul/guro/gaebong-dong-chuljangmassage/"),
     ("개봉역 생활권 출장마사지","/seoul/guro/gaebong-area-chuljangmassage/"),
     ("오류동역 출장마사지","/seoul/guro/oryu-dong-station-chuljangmassage/"),
     ("예약 안내","/seoul/guro/reservation/")],
    [("개봉역과 개봉동은 어떻게 다른가요?","개봉역 페이지는 역 주변 이동 기준을, 개봉동 페이지는 주거지와 생활권 전반을 안내합니다.")],
))

PAGES.append(content_page(
    "/seoul/guro/oryu-dong-station-chuljangmassage/",
    "오류동역 출장마사지｜오류동·천왕 인접 생활권 안내",
    "오류동역 출장마사지 예약 전 오류동, 천왕 인접 생활권을 확인하세요.",
    "오류동역 출장마사지 · 서남부 생활권 안내",
    "오류동역 · 역세권 안내",
    "1호선 오류동역과 천왕 인접 서남부 주거 생활권 방문 기준을 안내합니다.",
    [STN_CRUMB, ("오류동역 출장마사지", None)],
    ["오류동역 출장마사지","오류동 출장마사지","오류동역 홈타이"],
    "오류동역",
    [
        ("h2", "오류동역 인근 방문 안내"),
        ("p", "오류동역은 1호선 역으로 오류동 주거권의 중심에 있습니다. 경인로를 따라 상권이 형성되어 있고, 천왕동 방향으로 주거권이 이어집니다. 서남부 지역 특성상 위치에 따라 차량 이동 시간이 달라질 수 있어 정확한 위치를 확인 후 안내합니다."),
    ],
    [
        ("h2", "오류동역 인근 방문 포인트"),
        ("check", [
            "오류동역·오류시장 인근 — 생활 중심권",
            "경인로 방향 상업·주거 혼합권",
            "천왕동 방향 인접 주거권 — 서남부 생활권 연결",
        ]),
    ],
    [("오류동 출장마사지","/seoul/guro/oryu-dong-chuljangmassage/"),
     ("천왕역 출장마사지","/seoul/guro/cheonwang-station-chuljangmassage/"),
     ("오류동·천왕 생활권 출장마사지","/seoul/guro/oryu-cheonwang-area-chuljangmassage/"),
     ("이용 전 확인사항","/seoul/guro/before-visit/")],
    [("오류동역에서 천왕동도 방문하나요?","네, 오류동역과 인접한 천왕동 생활권까지 방문이 가능합니다.")],
))

PAGES.append(content_page(
    "/seoul/guro/onsu-station-chuljangmassage/",
    "온수역 출장마사지｜수궁동·온수동 환승권 안내",
    "온수역 출장마사지 예약 전 수궁동, 온수동 환승권을 확인하세요.",
    "온수역 출장마사지 · 환승권 생활권 안내",
    "온수역 · 역세권 안내",
    "1·7호선 온수역 환승권과 수궁동·온수동·궁동 주거 생활권 방문 기준을 안내합니다. 역명 기준 하나의 페이지로 운영합니다.",
    [STN_CRUMB, ("온수역 출장마사지", None)],
    ["온수역 출장마사지","온수동 출장마사지","온수역 홈타이"],
    "온수역",
    [
        ("h2", "온수역 환승권 방문 안내"),
        ("p", "온수역은 1호선과 7호선이 만나는 환승역으로, 수궁동·온수동·궁동 생활권의 관문 역할을 합니다. 1·7호선 어느 노선을 이용하셔도 동일하게 온수역 일대를 방문 안내합니다. 부천 경계와 가까워 위치에 따라 이동 시간이 달라질 수 있습니다."),
    ],
    [
        ("h2", "온수역 인근 방문 포인트"),
        ("check", [
            "온수역 인근 — 1·7호선 환승권, 숙소·사무실 방문",
            "수궁동·궁동 방향 주거권 — 자택 방문",
            "온수동 부천 경계 인접권 — 서부 생활권",
        ]),
    ],
    [("수궁동 출장마사지","/seoul/guro/sugung-dong-chuljangmassage/"),
     ("온수역·수궁동 생활권 출장마사지","/seoul/guro/onsu-sugung-area-chuljangmassage/"),
     ("궁동 생활권 출장마사지","/seoul/guro/gung-dong-area-chuljangmassage/"),
     ("예약 안내","/seoul/guro/reservation/")],
    [("온수역에서 수궁동·온수동도 방문하나요?","네. 온수역과 인접한 수궁동·온수동·궁동 생활권 전 지역을 방문합니다. 정확한 위치를 알려주시면 동선을 안내합니다.")],
))

PAGES.append(content_page(
    "/seoul/guro/cheonwang-station-chuljangmassage/",
    "천왕역 출장마사지｜천왕동·오류동 서부 생활권 안내",
    "천왕역 출장마사지 예약 전 천왕동, 오류동 서부 생활권을 확인하세요.",
    "천왕역 출장마사지 · 천왕지구 생활권 안내",
    "천왕역 · 역세권 안내",
    "7호선 천왕역과 천왕지구 주거권, 오류동 서부 생활권 방문 기준을 안내합니다.",
    [STN_CRUMB, ("천왕역 출장마사지", None)],
    ["천왕역 출장마사지","천왕동 출장마사지","천왕역 홈타이"],
    "천왕역",
    [
        ("h2", "천왕역 인근 방문 안내"),
        ("p", "천왕역은 7호선 역으로 천왕지구 아파트 단지가 밀집한 조용한 주거권의 중심입니다. 오류동 서부 생활권과 이어지며, 자택 방문 문의가 많습니다. 단지 진입 동선을 미리 확인하면 방문이 원활합니다."),
    ],
    [
        ("h2", "천왕역 인근 방문 포인트"),
        ("check", [
            "천왕지구 아파트 단지 — 자택 방문 중심",
            "천왕역 인근 — 7호선 주거권",
            "오류동 서부 인접권 — 서남부 생활권 연결",
        ]),
    ],
    [("천왕동 생활권 출장마사지","/seoul/guro/cheonwang-area-chuljangmassage/"),
     ("오류동·천왕 생활권 출장마사지","/seoul/guro/oryu-cheonwang-area-chuljangmassage/"),
     ("오류동 출장마사지","/seoul/guro/oryu-dong-chuljangmassage/"),
     ("이용 전 확인사항","/seoul/guro/before-visit/")],
    [("천왕지구 아파트로 방문되나요?","네, 천왕지구 단지 자택 방문이 가능합니다. 단지·동·호수를 알려주시면 진입 동선을 안내합니다.")],
))

PAGES.append(content_page(
    "/seoul/guro/namguro-station-chuljangmassage/",
    "남구로역 출장마사지｜구로동·가리봉동 인접권 안내",
    "남구로역 출장마사지 예약 전 구로동, 가리봉동 인접권을 확인하세요.",
    "남구로역 출장마사지 · 구로동·가리봉동 인접권 안내",
    "남구로역 · 역세권 안내",
    "7호선 남구로역과 구로동·가리봉동 주거·상업 혼합 생활권 방문 기준을 안내합니다.",
    [STN_CRUMB, ("남구로역 출장마사지", None)],
    ["남구로역 출장마사지","구로동 출장마사지","가리봉동 출장마사지"],
    "남구로역",
    [
        ("h2", "남구로역 인근 방문 안내"),
        ("p", "남구로역은 7호선 역으로 구로동과 가리봉동이 만나는 지점에 있습니다. 주거지와 상권이 함께 있어 자택·숙소·사무실 인근 방문 문의가 고르게 들어오며, 구로디지털단지 업무권과도 가깝습니다."),
    ],
    [
        ("h2", "남구로역 인근 방문 포인트"),
        ("check", [
            "남구로역 인근 — 주거·상권 혼합 생활권",
            "구로동 방향 — 구로구청·구로시장 생활권 연결",
            "가리봉동 방향 — 구로디지털단지 업무권 인접",
        ]),
    ],
    [("구로동 출장마사지","/seoul/guro/guro-dong-chuljangmassage/"),
     ("가리봉동 출장마사지","/seoul/guro/garibong-dong-chuljangmassage/"),
     ("가리봉동·남구로 생활권 출장마사지","/seoul/guro/garibong-namguro-area-chuljangmassage/"),
     ("예약 안내","/seoul/guro/reservation/")],
    [("남구로역에서 가리봉동도 방문하나요?","네, 남구로역과 인접한 가리봉동·구로동 전 지역을 방문합니다.")],
))

PAGES.append(content_page(
    "/seoul/guro/daerim-station-chuljangmassage/",
    "대림역 출장마사지｜구로동·대림 인접 생활권 안내",
    "대림역 출장마사지 예약 전 구로동, 대림 인접 생활권을 확인하세요.",
    "대림역 출장마사지 · 구로·영등포 경계 생활권 안내",
    "대림역 · 역세권 안내",
    "2·7호선 대림역은 구로·영등포 경계 성격이 있어 구로동 인접 생활권 중심으로 방문 기준을 안내합니다.",
    [STN_CRUMB, ("대림역 출장마사지", None)],
    ["대림역 출장마사지","구로동 출장마사지","대림역 홈타이"],
    "대림역",
    [
        ("h2", "대림역은 경계 생활권으로 안내합니다"),
        ("p", "대림역은 2·7호선 환승역으로 구로구와 영등포구의 경계에 있습니다. 대림역 구로 방향은 구로동 인접 생활권으로 방문 안내하며, 영등포 방향 위치는 전화로 확인 후 방문 가능 여부를 안내해 드립니다."),
    ],
    [
        ("h2", "대림역 인근 방문 포인트"),
        ("check", [
            "대림역 구로 방향 — 구로동 생활권 연결",
            "남구로역 인접권 — 7호선 주거·상권",
            "영등포 경계 — 위치별 방문 가능 여부 확인",
        ]),
    ],
    [("구로동 출장마사지","/seoul/guro/guro-dong-chuljangmassage/"),
     ("남구로역 출장마사지","/seoul/guro/namguro-station-chuljangmassage/"),
     ("가리봉동·남구로 생활권 출장마사지","/seoul/guro/garibong-namguro-area-chuljangmassage/"),
     ("예약 안내","/seoul/guro/reservation/")],
    [("대림역 영등포 방향도 방문하나요?","대림역 구로 방향은 안내가 가능하며, 영등포 경계 위치는 전화로 확인 후 방문 여부를 안내합니다.")],
))

PAGES.append(content_page(
    "/seoul/guro/guro-digital-complex-station-chuljangmassage/",
    "구로디지털단지역 출장마사지｜구로 업무지구 방문 안내",
    "구로디지털단지역 출장마사지 예약 전 업무지구 방문 기준을 확인하세요.",
    "구로디지털단지역 출장마사지 · 업무지구 방문 안내",
    "구로디지털단지역 · 역세권 안내",
    "2호선 구로디지털단지역 업무지구 방문 기준을 안내합니다. 사무실 인근 방문이 많은 지역의 출입 동선과 이동 기준을 다룹니다.",
    [STN_CRUMB, ("구로디지털단지역 출장마사지", None)],
    ["구로디지털단지역 출장마사지","구로디지털단지 출장마사지","구로디지털 홈타이"],
    "구로디지털단지역",
    [
        ("h2", "구로디지털단지역 업무지구 방문 안내"),
        ("p", "구로디지털단지역은 2호선 역으로 IT·벤처 기업이 밀집한 구로 업무지구의 중심입니다. 사무실 인근 방문 문의가 특히 많은 지역으로, 업무지구의 건물 출입 동선과 이동 기준을 중심으로 안내해 드립니다."),
    ],
    [
        ("h2", "구로디지털단지역 인근 방문 포인트"),
        ("check", [
            "디지털단지 오피스 — 사무실 인근 방문 다수",
            "마리오아울렛·상업권 — 숙소·상업 동선",
            "남구로역·가리봉동 인접권 — 주거권 연결",
        ]),
        ("p", "업무지구 특성상 평일 낮과 저녁 시간대 문의가 많으며, 사무실 인근 이용 시에는 건물 출입 동선을 미리 확인하시는 것이 좋습니다."),
    ],
    [("구로디지털단지 생활권 출장마사지","/seoul/guro/guro-digital-complex-area-chuljangmassage/"),
     ("구로동 출장마사지","/seoul/guro/guro-dong-chuljangmassage/"),
     ("남구로역 출장마사지","/seoul/guro/namguro-station-chuljangmassage/"),
     ("이용 전 확인사항","/seoul/guro/before-visit/")],
    [("사무실에서도 이용 가능한가요?","네, 사무실 인근 방문이 가능합니다. 사무실 인근 이용 전 확인사항을 참고하시고 출입 동선을 함께 알려주세요.")],
))

PAGES.append(content_page(
    "/seoul/guro/dorimcheon-station-chuljangmassage/",
    "도림천역 출장마사지｜신도림동·도림천 생활권 안내",
    "도림천역 출장마사지 예약 전 신도림동, 도림천 생활권을 확인하세요.",
    "도림천역 출장마사지 · 신도림 도림천 생활권 안내",
    "도림천역 · 역세권 안내",
    "2호선 도림천역과 신도림동 도림천 인접 주거 생활권 방문 기준을 안내합니다.",
    [STN_CRUMB, ("도림천역 출장마사지", None)],
    ["도림천역 출장마사지","신도림동 출장마사지","도림천 홈타이"],
    "도림천역",
    [
        ("h2", "도림천역 인근 방문 안내"),
        ("p", "도림천역은 2호선 신정지선 역으로 신도림동 도림천 인접 주거권에 있습니다. 신도림역 상업권과 가까우면서도 조용한 주거권이라 자택 방문 문의가 많습니다. 신도림동 안내와 함께 보시면 생활권 파악에 도움이 됩니다."),
    ],
    [
        ("h2", "도림천역 인근 방문 포인트"),
        ("check", [
            "도림천 방향 주거권 — 자택 방문 중심",
            "신도림역 인접권 — 환승·상업 동선 연결",
            "양천 경계 인접권 — 서부 주거 생활권",
        ]),
    ],
    [("신도림동 출장마사지","/seoul/guro/sindorim-dong-chuljangmassage/"),
     ("신도림역 출장마사지","/seoul/guro/sindorim-station-chuljangmassage/"),
     ("신도림 생활권 출장마사지","/seoul/guro/sindorim-area-chuljangmassage/"),
     ("예약 안내","/seoul/guro/reservation/")],
    [("도림천역 근처 신도림동도 방문하나요?","네, 도림천역과 인접한 신도림동 주거권 전 지역을 방문합니다.")],
))


# ============================ 생활권·주요 거점 (8) ============================
PAGES.append(content_page(
    "/seoul/guro/sindorim-area-chuljangmassage/",
    "신도림 생활권 출장마사지｜신도림역·디큐브시티 주변 안내",
    "신도림 생활권 출장마사지 예약 전 신도림역, 디큐브시티 주변을 확인하세요.",
    "신도림 생활권 출장마사지 · 디큐브시티 주변 안내",
    "신도림 생활권 · 주요 거점",
    "신도림역과 디큐브시티를 중심으로 한 생활권 전반의 방문 동선과 이용 기준을 안내합니다.",
    [AREA_CRUMB, ("신도림 생활권 출장마사지", None)],
    ["신도림 생활권 출장마사지","신도림 출장마사지","신도림 홈타이"],
    "신도림 생활권",
    [
        ("h2", "신도림 생활권 전반 안내"),
        ("p", "신도림 생활권은 신도림역 환승권을 중심으로 디큐브시티, 현대백화점, 테크노마트, 도림천 주거권까지 폭넓게 이어집니다. 신도림역 안내가 역 주변 동선을 다룬다면, 이 생활권 안내는 신도림 일대 전체의 방문 동선과 이용 흐름을 폭넓게 다룹니다."),
    ],
    [
        ("h2", "신도림 생활권 구성"),
        ("check", [
            "상업·숙소권 — 디큐브시티·호텔·오피스",
            "주거권 — 도림천·도림천역 방향",
            "환승권 — 1·2호선 신도림역 중심 이동",
        ]),
    ],
    [("신도림동 출장마사지","/seoul/guro/sindorim-dong-chuljangmassage/"),
     ("신도림역 출장마사지","/seoul/guro/sindorim-station-chuljangmassage/"),
     ("도림천역 출장마사지","/seoul/guro/dorimcheon-station-chuljangmassage/"),
     ("예약 안내","/seoul/guro/reservation/")],
    [("신도림 생활권은 어디까지인가요?","신도림역, 디큐브시티, 도림천 주거권을 포함합니다. 정확한 위치를 알려주시면 동선을 안내합니다.")],
))

PAGES.append(content_page(
    "/seoul/guro/guro-digital-complex-area-chuljangmassage/",
    "구로디지털단지 생활권 출장마사지｜업무지구·구로동 방문 안내",
    "구로디지털단지 생활권 출장마사지 예약 전 업무지구, 구로동을 확인하세요.",
    "구로디지털단지 생활권 출장마사지 · 업무지구 방문 안내",
    "구로디지털단지 생활권 · 주요 거점",
    "구로디지털단지 업무지구와 구로동 주거권이 만나는 생활권의 방문 기준을 안내합니다.",
    [AREA_CRUMB, ("구로디지털단지 생활권 출장마사지", None)],
    ["구로디지털단지 생활권 출장마사지","구로디지털단지 출장마사지","구로 홈타이"],
    "구로디지털단지 생활권",
    [
        ("h2", "구로디지털단지 생활권 전반 안내"),
        ("p", "구로디지털단지 생활권은 IT·벤처 업무지구와 마리오아울렛 상업권, 인접 구로동 주거권이 함께 어우러진 지역입니다. 사무실 인근 방문 문의가 많은 만큼, 업무지구의 이동 동선과 주거권 방문 기준을 함께 안내합니다."),
    ],
    [
        ("h2", "구로디지털단지 생활권 구성"),
        ("check", [
            "업무지구 — 디지털단지 오피스 사무실 인근",
            "상업권 — 마리오아울렛·먹자골목",
            "주거권 — 구로동·가리봉동 인접 생활권",
        ]),
    ],
    [("구로디지털단지역 출장마사지","/seoul/guro/guro-digital-complex-station-chuljangmassage/"),
     ("구로동 출장마사지","/seoul/guro/guro-dong-chuljangmassage/"),
     ("가리봉동·남구로 생활권 출장마사지","/seoul/guro/garibong-namguro-area-chuljangmassage/"),
     ("이용 전 확인사항","/seoul/guro/before-visit/")],
    [("업무지구 사무실도 방문하나요?","네, 사무실 인근 방문이 가능합니다. 건물 출입 동선을 알려주시면 원활하게 안내해 드립니다.")],
))

PAGES.append(content_page(
    "/seoul/guro/gocheok-skydome-area-chuljangmassage/",
    "고척스카이돔 인근 출장마사지｜고척동·구일역 생활권 안내",
    "고척스카이돔 인근 출장마사지 예약 전 고척동, 구일역 주변을 확인하세요.",
    "고척스카이돔 인근 출장마사지 · 고척동 생활권 안내",
    "고척스카이돔 인근 · 주요 거점",
    "고척스카이돔과 구일역, 안양천 주거권을 중심으로 한 생활권 방문 기준을 안내합니다.",
    [AREA_CRUMB, ("고척스카이돔 인근 출장마사지", None)],
    ["고척스카이돔 출장마사지","고척동 출장마사지","구일역 출장마사지"],
    "고척스카이돔 인근",
    [
        ("h2", "고척스카이돔 인근 생활권 안내"),
        ("p", "고척스카이돔 인근은 구일역과 안양천 주거권이 함께 있는 생활권입니다. 야구 경기나 공연이 있는 날에는 주변 도로가 혼잡해질 수 있어, 이런 날에는 예상 이동 시간을 넉넉히 잡고 예약하시는 것이 좋습니다. 평소에는 조용한 주거권 자택 방문이 많습니다."),
    ],
    [
        ("h2", "고척스카이돔 인근 생활권 구성"),
        ("check", [
            "고척스카이돔 — 행사일 교통 혼잡 시 이동 변동",
            "구일역·안양천 — 주거권 자택 방문",
            "고척동 단지 — 생활 주거 생활권",
        ]),
    ],
    [("고척동 출장마사지","/seoul/guro/gocheok-dong-chuljangmassage/"),
     ("구일역 출장마사지","/seoul/guro/guil-station-chuljangmassage/"),
     ("개봉동 출장마사지","/seoul/guro/gaebong-dong-chuljangmassage/"),
     ("예약 안내","/seoul/guro/reservation/")],
    [("경기 있는 날 고척스카이돔 인근도 방문하나요?","네, 방문 가능합니다. 다만 행사일에는 도로 혼잡으로 이동 시간이 평소보다 길어질 수 있습니다.")],
))

PAGES.append(content_page(
    "/seoul/guro/gaebong-area-chuljangmassage/",
    "개봉역 생활권 출장마사지｜개봉동 주거권 방문 안내",
    "개봉역 생활권 출장마사지 예약 전 개봉동 주거권을 확인하세요.",
    "개봉역 생활권 출장마사지 · 개봉동 주거권 안내",
    "개봉역 생활권 · 주요 거점",
    "개봉역과 개봉시장을 중심으로 한 구로 서부 주거 생활권의 방문 기준을 안내합니다.",
    [AREA_CRUMB, ("개봉역 생활권 출장마사지", None)],
    ["개봉역 생활권 출장마사지","개봉동 출장마사지","개봉 홈타이"],
    "개봉역 생활권",
    [
        ("h2", "개봉역 생활권 전반 안내"),
        ("p", "개봉역 생활권은 개봉시장과 개봉1~3동 주거권을 아우르는 구로 서부 생활권입니다. 개봉역 안내가 역 주변 동선을 다룬다면, 이 생활권 안내는 개봉 일대 주거권의 방문 흐름을 폭넓게 다룹니다."),
    ],
    [
        ("h2", "개봉역 생활권 구성"),
        ("check", [
            "개봉시장 인근 — 생활 중심 상업권",
            "개봉1·2·3동 주거권 — 자택 방문 중심",
            "광명 경계 인접권 — 서부 생활권 연결",
        ]),
    ],
    [("개봉동 출장마사지","/seoul/guro/gaebong-dong-chuljangmassage/"),
     ("개봉역 출장마사지","/seoul/guro/gaebong-station-chuljangmassage/"),
     ("오류동 출장마사지","/seoul/guro/oryu-dong-chuljangmassage/"),
     ("이용 전 확인사항","/seoul/guro/before-visit/")],
    [("개봉역 생활권은 어디까지인가요?","개봉시장과 개봉1~3동 주거권을 포함합니다. 정확한 위치를 알려주시면 동선을 안내합니다.")],
))

PAGES.append(content_page(
    "/seoul/guro/oryu-cheonwang-area-chuljangmassage/",
    "오류동·천왕 생활권 출장마사지｜오류동역·천왕역 주변 안내",
    "오류동·천왕 생활권 출장마사지 예약 전 오류동역, 천왕역 주변을 확인하세요.",
    "오류동·천왕 생활권 출장마사지 · 서남부 안내",
    "오류동·천왕 생활권 · 주요 거점",
    "오류동역과 천왕역, 천왕지구 주거권을 아우르는 구로구 서남부 생활권 방문 기준을 안내합니다.",
    [AREA_CRUMB, ("오류동·천왕 생활권 출장마사지", None)],
    ["오류동 출장마사지","천왕동 출장마사지","천왕역 출장마사지","오류동역 출장마사지"],
    "오류동·천왕 생활권",
    [
        ("h2", "오류동·천왕 생활권 전반 안내"),
        ("p", "오류동·천왕 생활권은 1호선 오류동역과 7호선 천왕역을 중심으로 한 구로구 서남부 주거권입니다. 오류동 상권과 천왕지구 아파트 단지가 함께 있어, 위치에 따라 이동 동선이 달라집니다. 서남부 특성상 예상 이동 시간을 넉넉히 안내합니다."),
    ],
    [
        ("h2", "오류동·천왕 생활권 구성"),
        ("check", [
            "오류동역·오류시장 — 생활 중심권",
            "천왕역·천왕지구 — 단지 자택 방문",
            "경인로 방향 — 상업·주거 혼합 동선",
        ]),
    ],
    [("오류동 출장마사지","/seoul/guro/oryu-dong-chuljangmassage/"),
     ("천왕역 출장마사지","/seoul/guro/cheonwang-station-chuljangmassage/"),
     ("천왕동 생활권 출장마사지","/seoul/guro/cheonwang-area-chuljangmassage/"),
     ("예약 안내","/seoul/guro/reservation/")],
    [("오류동과 천왕동을 함께 안내하는 이유는?","두 지역이 서남부 주거권으로 가까이 이어져 있어, 이동 동선을 함께 보면 방문 계획에 도움이 되기 때문입니다.")],
))

PAGES.append(content_page(
    "/seoul/guro/onsu-sugung-area-chuljangmassage/",
    "온수역·수궁동 생활권 출장마사지｜궁동·온수동 방문 안내",
    "온수역·수궁동 생활권 출장마사지 예약 전 궁동, 온수동을 확인하세요.",
    "온수역·수궁동 생활권 출장마사지 · 궁동·온수동 안내",
    "온수역·수궁동 생활권 · 주요 거점",
    "온수역 환승권과 수궁동·궁동·온수동 주거권을 아우르는 생활권 방문 기준을 안내합니다.",
    [AREA_CRUMB, ("온수역·수궁동 생활권 출장마사지", None)],
    ["온수역 출장마사지","수궁동 출장마사지","궁동 출장마사지","온수동 출장마사지"],
    "온수역·수궁동 생활권",
    [
        ("h2", "온수역·수궁동 생활권 전반 안내"),
        ("p", "온수역·수궁동 생활권은 1·7호선 온수역 환승권을 중심으로 수궁동, 궁동, 온수동 주거권이 이어지는 구로구 서부 생활권입니다. 부천 경계와 가까워 위치에 따라 이동 시간이 달라질 수 있어, 정확한 위치를 확인 후 안내합니다."),
    ],
    [
        ("h2", "온수역·수궁동 생활권 구성"),
        ("check", [
            "온수역 — 1·7호선 환승권, 숙소·사무실 방문",
            "궁동 — 궁동근린공원 인근 녹지 주거권",
            "온수동 — 부천 경계 인접 서부 주거권",
        ]),
    ],
    [("수궁동 출장마사지","/seoul/guro/sugung-dong-chuljangmassage/"),
     ("온수역 출장마사지","/seoul/guro/onsu-station-chuljangmassage/"),
     ("궁동 생활권 출장마사지","/seoul/guro/gung-dong-area-chuljangmassage/"),
     ("이용 전 확인사항","/seoul/guro/before-visit/")],
    [("궁동·온수동도 함께 방문하나요?","네, 온수역·수궁동 생활권으로 궁동과 온수동을 함께 안내하며 방문이 가능합니다.")],
))

PAGES.append(content_page(
    "/seoul/guro/garibong-namguro-area-chuljangmassage/",
    "가리봉동·남구로 생활권 출장마사지｜남구로역 인접권 안내",
    "가리봉동·남구로 생활권 출장마사지 예약 전 남구로역 인접권을 확인하세요.",
    "가리봉동·남구로 생활권 출장마사지 · 인접권 안내",
    "가리봉동·남구로 생활권 · 주요 거점",
    "남구로역과 가리봉동, 구로동 인접 주거·상업 혼합 생활권 방문 기준을 안내합니다.",
    [AREA_CRUMB, ("가리봉동·남구로 생활권 출장마사지", None)],
    ["가리봉동 출장마사지","남구로역 출장마사지","구로 홈타이"],
    "가리봉동·남구로 생활권",
    [
        ("h2", "가리봉동·남구로 생활권 전반 안내"),
        ("p", "가리봉동·남구로 생활권은 7호선 남구로역을 중심으로 가리봉동과 구로동, 구로디지털단지 업무권이 인접한 주거·상업 혼합 생활권입니다. 자택·숙소·사무실 인근 방문 문의가 고르게 들어오는 지역입니다."),
    ],
    [
        ("h2", "가리봉동·남구로 생활권 구성"),
        ("check", [
            "남구로역 — 주거·상권 혼합 중심권",
            "가리봉동 — 가산 인접권, 업무지구 연결",
            "구로동 — 구로구청·구로시장 생활권",
        ]),
    ],
    [("가리봉동 출장마사지","/seoul/guro/garibong-dong-chuljangmassage/"),
     ("남구로역 출장마사지","/seoul/guro/namguro-station-chuljangmassage/"),
     ("구로디지털단지 생활권 출장마사지","/seoul/guro/guro-digital-complex-area-chuljangmassage/"),
     ("예약 안내","/seoul/guro/reservation/")],
    [("이 생활권은 어디까지 방문하나요?","남구로역, 가리봉동, 구로동 인접권을 포함합니다. 가산 경계 위치는 전화로 확인 후 안내합니다.")],
))

PAGES.append(content_page(
    "/seoul/guro/hang-dong-area-chuljangmassage/",
    "항동 주거지 생활권 출장마사지｜항동·푸른수목원 인근 안내",
    "항동 주거지 생활권 출장마사지 예약 전 항동, 푸른수목원 인근을 확인하세요.",
    "항동 주거지 생활권 출장마사지 · 푸른수목원 인근 안내",
    "항동 주거지 생활권 · 주요 거점",
    "항동지구와 푸른수목원 인근 주거 생활권을 중심으로 방문 가능 지역과 이동 기준을 안내합니다.",
    [AREA_CRUMB, ("항동 주거지 생활권 출장마사지", None)],
    ["항동 출장마사지","항동지구 출장마사지","푸른수목원 출장마사지"],
    "항동 주거지 생활권",
    [
        ("h2", "항동 주거지 생활권 전반 안내"),
        ("p", "항동 주거지 생활권은 항동지구 신규 아파트 단지와 푸른수목원 인근 녹지 주거권이 중심인 구로구 서남부 외곽 생활권입니다. 도심 교통권과 거리가 있어 차량 이동 시간이 더 걸릴 수 있으며, 단지 진입 동선을 미리 확인하면 방문이 원활합니다."),
    ],
    [
        ("h2", "항동 주거지 생활권 구성"),
        ("check", [
            "항동지구 아파트 단지 — 자택 방문 중심",
            "푸른수목원 인근 — 녹지 주거권",
            "성공회대·부천 경계 인접권 — 외곽 생활권",
        ]),
    ],
    [("항동 출장마사지","/seoul/guro/hang-dong-chuljangmassage/"),
     ("수궁동 출장마사지","/seoul/guro/sugung-dong-chuljangmassage/"),
     ("온수역·수궁동 생활권 출장마사지","/seoul/guro/onsu-sugung-area-chuljangmassage/"),
     ("예약 전 확인사항","/seoul/guro/before-visit/")],
    [("항동지구 단지도 방문하나요?","네, 항동지구 단지 자택 방문이 가능합니다. 외곽 지역 특성상 이동 시간이 더 걸릴 수 있어 전화로 예약을 권합니다.")],
))


# ============================ 기타 페이지 (예약/이용/가이드/고객센터/약관/개인정보) ============================
PAGES.append({
    "url": "/seoul/guro/reservation/",
    "title": "구로구 출장마사지 예약 안내｜예약 가능 지역·시간·결제 기준",
    "desc": "구로구 출장마사지 예약 가능 지역, 시간, 추가 이동비, 결제·취소 기준을 확인하세요.",
    "h1": "구로구 출장마사지 예약 안내",
    "eyebrow": "이용 안내 · 예약",
    "hero_sub": "예약 가능 지역과 시간, 추가 이동비, 결제 방식, 예약 변경·취소 기준을 한눈에 정리했습니다. 전화로 위치를 알려주시면 방문 가능 여부를 안내해 드립니다.",
    "crumbs": [("구로 홈", SITE["main_url"]), ("예약 안내", None)],
    "keywords": ["구로구 출장마사지 예약","구로 홈타이 예약","출장마사지 예약 안내"],
    "related": [("이용 전 확인사항","/seoul/guro/before-visit/"),("홈타이 이용 가이드","/seoul/guro/hometai-guide/"),("고객센터","/seoul/guro/support/")],
    "blocks": [
        ("h2", "예약 가능 지역 확인"),
        ("p", "바로GO는 서울 구로구 전 지역을 방문합니다. 신도림·구로동·구로디지털단지처럼 교통 접근성이 좋은 지역은 이동이 빠르고, 항동·수궁동·천왕동 등 서남부 외곽은 이동 시간이 더 걸릴 수 있습니다. 정확한 위치(동·단지·건물)를 알려주시면 방문 가능 여부와 예상 이동 시간을 안내해 드립니다."),
        CALL_BLOCK,
        ("pricing",),
        ("h2", "예약 가능 시간 안내"),
        ("p", f"운영시간은 {SITE['hours']}입니다. 예약이 몰리는 시간대에는 대기가 발생할 수 있어, 희망 시간보다 여유 있게 문의해 주시면 원활하게 안내해 드립니다."),
        ("h2", "추가 이동비 안내"),
        ("p", "기본 방문권 외에 외곽 지역이나 심야 시간대는 이동비가 추가될 수 있습니다. 추가 이동비는 예약 전 전화로 미리 안내해 드리며, 임의로 부과하지 않습니다."),
        ("h2", "결제 방식 안내"),
        ("table", [
            ("결제 방식", SITE["pay"]),
            ("결제 시점", "서비스 진행 전 현장 결제 기준"),
            ("영수증", "요청 시 안내"),
        ]),
        ("h2", "예약 변경·취소 기준"),
        ("p", SITE["cancel"] + " 단순 변심에 의한 잦은 취소는 이후 예약이 제한될 수 있습니다."),
        ("check", [
            "예약 시간 1시간 전까지 무료 변경·취소",
            "이동 시작 후 취소 시 이동비가 발생할 수 있음",
            "노쇼(무단 불참) 시 이후 예약 제한 가능",
        ]),
        ("notice", "바로GO는 합법적인 방문형 관리 서비스만 안내합니다. 불법·선정적 서비스 요청은 예약이 불가하며, 허위 정보로 인한 예약은 취소될 수 있습니다."),
    ],
    "full_width": False,
})

PAGES.append({
    "url": "/seoul/guro/before-visit/",
    "title": "구로구 출장마사지 이용 전 확인사항｜자택·숙소·사무실 안내",
    "desc": "출장마사지 이용 전 자택·숙소·사무실 인근 확인사항과 개인정보·안전 기준을 확인하세요.",
    "h1": "이용 전 확인사항",
    "eyebrow": "이용 안내 · 확인사항",
    "hero_sub": "자택, 숙소, 사무실 인근에서 방문형 관리 서비스를 이용하기 전에 확인하면 좋은 사항과 고객 안전·개인정보 기준을 정리했습니다.",
    "crumbs": [("구로 홈", SITE["main_url"]), ("이용 전 확인사항", None)],
    "keywords": ["출장마사지 이용 전 확인","홈타이 이용 안내","방문 전 확인사항"],
    "related": [("예약 안내","/seoul/guro/reservation/"),("홈타이 이용 가이드","/seoul/guro/hometai-guide/"),("개인정보 처리방침","/seoul/guro/privacy/")],
    "blocks": [
        ("h2", "방문 가능 주소 확인"),
        ("p", "방문 전에는 정확한 주소와 진입 동선(공동현관, 주차, 엘리베이터 등)을 확인하는 것이 좋습니다. 주소가 정확할수록 예상 시간에 맞춰 방문할 수 있습니다."),
        ("h2", "자택 이용 전 확인사항"),
        ("check", [
            "공동현관 비밀번호 또는 출입 방법 확인",
            "편안한 공간과 기본적인 정리 상태 확인",
            "주차 가능 여부 또는 인근 주차 안내",
        ]),
        ("h2", "숙소 이용 전 확인사항"),
        ("check", [
            "호텔·모텔 등 숙소명과 호실 확인",
            "프런트 출입 정책(외부인 방문 가능 여부) 확인",
            "체크인 상태에서 예약 권장",
        ]),
        ("h2", "사무실 인근 이용 전 확인사항"),
        ("check", [
            "건물 출입 통제 여부와 출입 방법 확인",
            "이용 가능한 공간 확보 여부 확인",
            "주변에 방해되지 않는 시간대 선택",
        ]),
        ("h2", "개인정보 처리 기준"),
        ("p", "예약에 필요한 최소한의 정보(연락처, 방문 주소, 희망 시간)만 수집하며, 서비스 종료 후 안전하게 파기합니다. 자세한 내용은 개인정보 처리방침에서 확인하실 수 있습니다."),
        ("h2", "고객 안전 안내"),
        ("p", "바로GO는 고객과 관리사 모두의 안전을 중요하게 생각합니다. 음주 과다 상태나 안전이 우려되는 상황에서는 서비스가 제한될 수 있습니다."),
        ("notice", "바로GO는 <strong>불법·선정적 서비스를 제공하지 않습니다.</strong> 관련 요청 시 예약이 정중히 거절되며, 모든 서비스는 합법적인 방문형 관리 범위 내에서 진행됩니다."),
    ],
    "full_width": False,
})

PAGES.append({
    "url": "/seoul/guro/hometai-guide/",
    "title": "홈타이 이용 가이드｜출장마사지와 홈타이 차이·이용 기준",
    "desc": "홈타이란 무엇인지, 출장마사지와의 차이와 구로구 이용 전 기준을 확인하세요.",
    "h1": "홈타이 이용 가이드",
    "eyebrow": "이용 안내 · 가이드",
    "hero_sub": "홈타이의 의미, 출장마사지와의 차이, 구로구에서 처음 이용할 때 알아두면 좋은 기준을 정리했습니다.",
    "crumbs": [("구로 홈", SITE["main_url"]), ("홈타이 이용 가이드", None)],
    "keywords": ["홈타이","홈타이 이용 가이드","출장마사지 홈타이 차이","구로 홈타이"],
    "related": [("예약 안내","/seoul/guro/reservation/"),("이용 전 확인사항","/seoul/guro/before-visit/"),("구로동 출장마사지","/seoul/guro/guro-dong-chuljangmassage/")],
    "blocks": [
        ("h2", "홈타이란?"),
        ("p", "홈타이는 자택이나 숙소처럼 고객이 머무는 공간으로 관리사가 방문해 진행하는 방문형 관리 서비스를 가리키는 표현입니다. '홈(home)'에서 받는다는 의미가 강조된 용어로, 별도 매장을 방문하지 않고 편한 공간에서 이용한다는 점이 특징입니다."),
        ("h2", "출장마사지와 홈타이 차이"),
        ("p", "출장마사지와 홈타이는 모두 관리사가 고객의 위치로 방문하는 방문형 관리 서비스를 가리키며, 실질적인 의미는 거의 같습니다. 다만 '홈타이'는 자택·숙소 이용을 강조할 때, '출장마사지'는 방문(출장)이라는 형태를 강조할 때 주로 쓰입니다."),
        ("table", [
            ("공통점", "관리사가 고객 위치로 방문하는 방문형 서비스"),
            ("홈타이 강조점", "자택·숙소 등 머무는 공간에서 이용"),
            ("출장마사지 강조점", "방문(출장) 형태 자체"),
        ]),
        ("h2", "구로구 홈타이 이용 전 기준"),
        ("check", [
            "방문 가능 지역과 예상 이동 시간 확인",
            "예약 가능 시간과 추가 이동비 확인",
            "자택·숙소·사무실 이용 환경 점검",
            "결제·취소 기준 확인",
        ]),
        ("h2", "지역별 이동 기준"),
        ("p", "구로구는 신도림·구로디지털단지처럼 교통이 편리한 지역과 항동·수궁동·천왕동처럼 외곽 주거권이 함께 있습니다. 지역에 따라 이동 시간이 달라지므로, 정확한 위치를 알려주시면 예상 시간을 안내해 드립니다."),
        ("h2", "추가 비용 확인 기준"),
        ("p", "외곽 지역이나 심야 시간대는 이동비가 추가될 수 있으며, 모든 추가 비용은 예약 전 전화로 미리 안내합니다."),
        ("h2", "처음 이용하는 고객 안내"),
        ("p", f"홈타이가 처음이라면 예약 시 전화로 궁금한 점을 편하게 문의해 주세요. 방문 가능 여부, 예상 시간, 준비 사항을 친절히 안내해 드립니다. 전화예약 {SITE['phone']}."),
        CALL_BLOCK,
        ("notice", "바로GO의 홈타이·출장마사지는 모두 합법적인 방문형 관리 서비스입니다. 불법·선정적 서비스는 제공하지 않습니다."),
    ],
    "full_width": False,
})

PAGES.append({
    "url": "/seoul/guro/support/",
    "title": "고객센터｜바로GO 구로구 출장마사지 문의·운영 기준",
    "desc": "바로GO 구로구 출장마사지 문의, 자주 묻는 질문, 운영 기준과 사이트 소개를 확인하세요.",
    "h1": "고객센터",
    "eyebrow": "고객센터",
    "hero_sub": "문의 방법, 자주 묻는 질문, 운영 기준과 사이트 소개를 정리했습니다. 가장 빠른 상담은 전화 문의입니다.",
    "crumbs": [("구로 홈", SITE["main_url"]), ("고객센터", None)],
    "keywords": ["바로GO 고객센터","구로구 출장마사지 문의","출장마사지 자주 묻는 질문"],
    "related": [("예약 안내","/seoul/guro/reservation/"),("이용 전 확인사항","/seoul/guro/before-visit/"),("개인정보 처리방침","/seoul/guro/privacy/")],
    "blocks": [
        ("h2", "문의하기"),
        ("p", f"예약·상담 문의는 전화가 가장 빠르고 정확합니다. 현재 위치와 희망 시간을 알려주시면 방문 가능 여부와 예상 이동 시간을 안내해 드립니다."),
        ("table", [
            ("상호", "바로GO"),
            ("전화예약", SITE["phone"]),
            ("운영시간", SITE["hours"]),
            ("방문 지역", "서울 구로구 전 지역"),
        ]),
        CALL_BLOCK,
        ("h2", "자주 묻는 질문"),
        ("faq", [
            ("예약은 어떻게 하나요?", f"전화예약 {SITE['phone']}로 위치와 희망 시간을 알려주시면 됩니다."),
            ("구로구 전 지역 방문이 되나요?", "네, 신도림동·구로동·고척동·개봉동·오류동·수궁동·항동 등 구로구 전 지역을 방문합니다."),
            ("추가 비용이 있나요?", "외곽·심야 시간대는 이동비가 추가될 수 있으며, 예약 전 미리 안내합니다."),
            ("불법·선정적 서비스도 가능한가요?", "아니요. 바로GO는 합법적인 방문형 관리 서비스만 제공하며 관련 요청은 정중히 거절합니다."),
        ]),
        ("h2", "운영 기준"),
        ("check", [
            "합법적인 방문형 관리 서비스만 안내",
            "허위 후기·과장 할인 문구 미사용",
            "추가 비용은 예약 전 사전 안내",
            "개인정보는 최소 수집 후 안전하게 파기",
        ]),
        ("h2", "사이트 소개"),
        ("p", "바로GO는 서울 구로구의 방문형 관리 서비스(출장마사지·홈타이) 지역 안내 사이트입니다. 신도림·구로디지털단지·고척·개봉·오류·항동 등 구로구 생활권별 방문 가능 지역과 예약 전 확인사항을 신뢰할 수 있는 정보 중심으로 제공합니다. 별도의 오프라인 매장 주소를 운영하지 않는 방문형 서비스입니다."),
    ],
    "faq_schema": [
        ("예약은 어떻게 하나요?", f"전화예약 {SITE['phone']}로 위치와 희망 시간을 알려주시면 됩니다."),
        ("구로구 전 지역 방문이 되나요?", "네, 신도림동·구로동·고척동·개봉동·오류동·수궁동·항동 등 구로구 전 지역을 방문합니다."),
        ("추가 비용이 있나요?", "외곽·심야 시간대는 이동비가 추가될 수 있으며, 예약 전 미리 안내합니다."),
    ],
    "full_width": False,
})

PAGES.append({
    "url": "/seoul/guro/privacy/",
    "title": "개인정보 처리방침｜바로GO 구로구 출장마사지",
    "desc": "바로GO가 수집하는 개인정보 항목, 이용 목적, 보관·파기 기준을 안내합니다.",
    "h1": "개인정보 처리방침",
    "eyebrow": "정책",
    "hero_sub": "바로GO는 예약에 필요한 최소한의 개인정보만 수집하고, 서비스 종료 후 안전하게 파기합니다.",
    "crumbs": [("구로 홈", SITE["main_url"]), ("개인정보 처리방침", None)],
    "keywords": ["개인정보 처리방침","바로GO 개인정보"],
    "related": [("이용약관","/seoul/guro/terms/"),("고객센터","/seoul/guro/support/"),("예약 안내","/seoul/guro/reservation/")],
    "blocks": [
        ("h2", "1. 수집하는 개인정보 항목"),
        ("p", "바로GO는 예약 및 상담을 위해 다음의 최소한의 정보만 수집합니다: 연락처(전화번호), 방문 주소(예약 지역), 희망 예약 시간. 그 외 민감정보는 수집하지 않습니다."),
        ("h2", "2. 개인정보의 이용 목적"),
        ("p", "수집한 정보는 예약 접수, 방문 가능 여부 확인, 예약 안내 및 변경·취소 처리 목적으로만 이용합니다."),
        ("h2", "3. 보유 및 파기"),
        ("p", "수집한 개인정보는 서비스 제공이 완료되면 지체 없이 파기합니다. 전자적 파일은 복구할 수 없는 방법으로 삭제하며, 별도 보관이 필요한 경우에도 관련 법령이 정한 기간을 초과하지 않습니다."),
        ("h2", "4. 제3자 제공"),
        ("p", "바로GO는 고객의 동의 없이 개인정보를 제3자에게 제공하지 않습니다. 다만 법령에 의한 요청이 있는 경우는 예외로 합니다."),
        ("h2", "5. 이용자의 권리"),
        ("p", "이용자는 본인의 개인정보에 대한 열람·정정·삭제를 요청할 수 있으며, 전화 문의를 통해 처리할 수 있습니다."),
        ("h2", "6. 문의"),
        ("p", f"개인정보 관련 문의는 전화예약 {SITE['phone']}로 연락해 주시기 바랍니다."),
    ],
    "full_width": False,
})

PAGES.append({
    "url": "/seoul/guro/terms/",
    "title": "이용약관｜바로GO 구로구 출장마사지",
    "desc": "바로GO 구로구 출장마사지 서비스 이용약관과 운영 기준을 안내합니다.",
    "h1": "이용약관",
    "eyebrow": "정책",
    "hero_sub": "바로GO 방문형 관리 서비스의 이용약관과 운영 기준을 안내합니다.",
    "crumbs": [("구로 홈", SITE["main_url"]), ("이용약관", None)],
    "keywords": ["이용약관","바로GO 이용약관"],
    "related": [("개인정보 처리방침","/seoul/guro/privacy/"),("고객센터","/seoul/guro/support/"),("예약 안내","/seoul/guro/reservation/")],
    "blocks": [
        ("h2", "제1조 (목적)"),
        ("p", "본 약관은 바로GO가 제공하는 서울 구로구 방문형 관리 서비스(출장마사지·홈타이) 안내 및 예약과 관련한 이용 조건을 규정합니다."),
        ("h2", "제2조 (서비스 범위)"),
        ("p", "바로GO는 합법적인 방문형 관리 서비스만을 안내하고 예약을 중개합니다. 불법·선정적 서비스는 일절 제공하거나 알선하지 않습니다."),
        ("h2", "제3조 (예약 및 취소)"),
        ("p", "예약은 전화로 접수되며, 예약 시간 1시간 전까지 무료로 변경·취소할 수 있습니다. 이후 이동 시작 시에는 이동비가 발생할 수 있습니다."),
        ("h2", "제4조 (이용자의 의무)"),
        ("p", "이용자는 정확한 예약 정보를 제공해야 하며, 관리사의 안전과 정당한 서비스 진행을 방해해서는 안 됩니다. 불법·선정적 요청 시 서비스가 거절될 수 있습니다."),
        ("h2", "제5조 (책임의 한계)"),
        ("p", "허위 정보 제공으로 인한 예약 오류, 또는 이용자의 귀책으로 발생한 문제에 대해서는 책임이 제한될 수 있습니다."),
        ("h2", "제6조 (문의)"),
        ("p", f"약관 관련 문의는 전화예약 {SITE['phone']}로 연락해 주시기 바랍니다."),
    ],
    "full_width": False,
})

# ============================ 생성 + 사이트맵 + robots ============================
def build():
    seen = set()
    for p in PAGES:
        if p["url"] in seen:
            raise SystemExit(f"중복 URL: {p['url']}")
        seen.add(p["url"])
        write_page(p)
    # sitemap.xml
    urls = "".join(
        f"  <url><loc>{SITE['base']}{p['url']}</loc>"
        f"<changefreq>weekly</changefreq>"
        f"<priority>{'1.0' if p['url']==SITE['main_url'] else '0.8'}</priority></url>\n"
        for p in PAGES
    )
    sitemap = ('<?xml version="1.0" encoding="UTF-8"?>\n'
               '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
               f"{urls}</urlset>\n")
    with open(os.path.join(OUT, "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write(sitemap)
    # robots.txt
    with open(os.path.join(OUT, "robots.txt"), "w", encoding="utf-8") as f:
        f.write("User-agent: *\nAllow: /\n\n"
                f"Sitemap: {SITE['base']}/sitemap.xml\n")
    # 메인 페이지는 루트(/)에서 생성되므로 루트 index.html은 곧 메인입니다.
    # 예전 메인 경로(/seoul/guro-gu-chuljangmassage/)는 루트로 301 리다이렉트(Cloudflare Pages _redirects)
    with open(os.path.join(OUT, "_redirects"), "w", encoding="utf-8") as f:
        f.write("/seoul/guro-gu-chuljangmassage/    /    301\n"
                "/seoul/guro-gu-chuljangmassage     /    301\n")
    print(f"생성 완료: {len(PAGES)} 페이지(메인=/) + sitemap.xml + robots.txt + _redirects")

if __name__ == "__main__":
    build()
