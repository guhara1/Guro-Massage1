# 바로GO · 구로구 출장마사지 · 홈타이 지역 안내 사이트

서울 구로구 방문형 관리 서비스(출장마사지·홈타이) **지역 안내 정적 사이트**입니다.
검색엔진을 속이는 도어웨이 페이지 대신, 생활권별로 실제 도움이 되는 정보를 담아
구글 검색 가이드라인(중복 콘텐츠 방지·E-E-A-T·신뢰 신호)에 맞춰 구성했습니다.

- **상호:** 바로GO
- **전화예약:** 0508-202-4719
- **메인 URL:** `/seoul/guro-gu-chuljangmassage/`

## 구성

| 분류 | 페이지 수 |
|------|-----------|
| 메인 | 1 |
| 대표 행정동 (신도림·구로·가리봉·고척·개봉·오류·수궁·항동) | 8 |
| 법정동·생활권 보조 (천왕·온수·궁동) | 3 |
| 역세권 | 11 |
| 생활권·주요 거점 | 8 |
| 기타 (예약·이용전확인·홈타이가이드·고객센터·개인정보) | 5 |
| 정책 보조 (이용약관) | 1 |
| **합계** | **37** |

### 통합(중복 방지) 규칙
- 구로1~5동 → **구로동** 1개 / 고척1·2동 → **고척동** / 개봉1~3동 → **개봉동** / 오류1·2동 → **오류동**
- 번호 동 개별 페이지 생성 금지, 대표동 본문에서 세부 생활권으로 설명
- 환승역(신도림·온수 등)은 노선별로 쪼개지 않고 **역명 기준 1개 URL**
- 가산디지털단지역은 금천구 성격 → 단독 페이지 미생성(가리봉동 본문 보조 설명)

## 기술
- 정적 HTML + 단일 CSS 토큰 시스템(`assets/css/style.css`, Pretendard + 프리미엄 팔레트 + 컴포넌트 오버레이)
- 모바일 내비게이션: `assets/js/main.js`
- 구조화 데이터(JSON-LD): `WebPage`, `BreadcrumbList`, `Organization`, `ImageObject` (+ 일부 `FAQPage`)
  - 오프라인 매장 주소가 없는 방문형 서비스이므로 `LocalBusiness`는 사용하지 않음
- 메타 디스크립션 80자 이내 / canonical / Open Graph / Twitter Card
- `sitemap.xml`, `robots.txt`, 루트 `index.html`(메인 리다이렉트) 자동 생성

## 빌드 방법

```bash
python3 build.py
```

모든 페이지/사이트맵/robots가 재생성됩니다. 내용 수정은 `build.py`의 `PAGES` 데이터에서 진행하세요.

> 배포 도메인은 `build.py`의 `SITE["base"]` 값을 실제 도메인으로 교체한 뒤 다시 빌드하면
> canonical·OG·sitemap의 절대 URL이 일괄 반영됩니다.

## 색인(인덱싱) 셋업

빌드 시 다음 파일이 자동 생성됩니다.

| 파일 | 용도 |
|------|------|
| `sitemap.xml` | 사이트맵 (lastmod 포함) |
| `rss.xml` | RSS 2.0 피드 (head에 `alternate` 링크 연결) |
| `robots.txt` | 구글·네이버(Yeti)·빙 허용 + 사이트맵/RSS 명시 |
| `<indexnow_key>.txt` | IndexNow 키 파일 (루트에 위치) |
| `urls.txt` | 전체 URL 목록 (통보 스크립트 입력) |

### 검색엔진 등록 (최초 1회, 가장 빠른 색인 경로)
1. **구글 Search Console** → 사이트 속성 추가 → `sitemap.xml` 제출
2. **네이버 서치어드바이저** → 사이트 등록(소유확인: head의 `naver-site-verification` 태그 사용) → `sitemap.xml`·`rss.xml` 제출
3. **빙 Webmaster Tools** → 사이트 추가 → 사이트맵 제출 (IndexNow 자동 연동)

### IndexNow — 글 올릴 때마다 즉시 통보 (빙·네이버·얀덱스)
키 파일이 배포된 뒤(`https://<도메인>/<key>.txt` 접근 가능) 실행하세요.

```bash
python build.py            # 변경 반영 + urls.txt 갱신
python tools/indexnow.py   # 전체 URL 즉시 통보 (빙·네이버·얀덱스)
# 특정 URL만:
python tools/indexnow.py https://guro-massage1.netlify.app/seoul/guro/guro-dong-chuljangmassage/
```

> IndexNow 키는 `build.py`의 `SITE["indexnow_key"]` 와 `tools/indexnow.py`의 `KEY` 가 동일해야 합니다.

### 구글 Indexing API (선택 — 구글은 IndexNow 미참여)
```bash
pip install google-auth requests
export GOOGLE_INDEXING_SA=/path/to/service-account.json
python tools/google_indexing.py            # urls.txt 전체 통보
```
사전 준비: Google Cloud에서 Indexing API 사용 설정 → 서비스 계정 생성 →
Search Console 속성에 서비스 계정을 '소유자'로 추가. 자세한 내용은 `tools/google_indexing.py` 상단 주석 참고.

> 참고: 구글·빙의 **sitemap ping 엔드포인트는 2023~2024년에 종료**되었습니다.
> 따라서 즉시 색인은 IndexNow(빙·네이버)와 구글 Indexing API/Search Console 사이트맵 제출로 처리합니다.
