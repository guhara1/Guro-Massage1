# -*- coding: utf-8 -*-
"""
IndexNow 즉시 색인 통보 — 빙(Bing) + 네이버(Naver) + Yandex
글을 올리거나 수정한 뒤 한 번 실행하면 참여 검색엔진에 변경 URL을 즉시 통보합니다.

사용법:
  python tools/indexnow.py                 # 전체 URL(urls.txt) 통보
  python tools/indexnow.py URL1 URL2 ...   # 지정한 URL만 통보

표준 라이브러리만 사용합니다(추가 설치 불필요).
"""
import sys, os, json, urllib.request, urllib.error

HOST = "guro-massage1.pages.dev"
BASE = f"https://{HOST}"
KEY = "a3f1c9d2e4b6478894c0a5f3e21d7b6c"
KEY_LOCATION = f"{BASE}/{KEY}.txt"

# IndexNow는 한 곳에 보내면 참여 엔진끼리 공유되지만,
# 확실하게 하려고 빙·네이버·얀덱스 엔드포인트에 각각 통보합니다.
ENDPOINTS = [
    "https://api.indexnow.org/indexnow",
    "https://www.bing.com/indexnow",
    "https://searchadvisor.naver.com/indexnow",
    "https://yandex.com/indexnow",
]

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def load_urls():
    args = [a for a in sys.argv[1:] if a.startswith("http")]
    if args:
        return args
    path = os.path.join(ROOT, "urls.txt")
    if not os.path.exists(path):
        sys.exit("urls.txt 가 없습니다. 먼저 `python build.py` 를 실행하세요.")
    with open(path, encoding="utf-8") as f:
        return [ln.strip() for ln in f if ln.strip()]


def submit(endpoint, urls):
    payload = json.dumps({
        "host": HOST,
        "key": KEY,
        "keyLocation": KEY_LOCATION,
        "urlList": urls,
    }).encode("utf-8")
    req = urllib.request.Request(
        endpoint, data=payload, method="POST",
        headers={"Content-Type": "application/json; charset=utf-8"},
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return resp.status, resp.read(200).decode("utf-8", "ignore")
    except urllib.error.HTTPError as e:
        return e.code, e.read(200).decode("utf-8", "ignore")
    except Exception as e:  # noqa
        return None, str(e)


def main():
    urls = load_urls()
    print(f"통보 대상 {len(urls)}개 URL · 키 위치 {KEY_LOCATION}\n")
    for ep in ENDPOINTS:
        status, body = submit(ep, urls)
        ok = status in (200, 202)
        mark = "OK " if ok else "-- "
        print(f"  [{mark}] {ep} → {status} {body[:80]}".rstrip())
    print("\n참고: 200/202 는 정상 접수입니다. 색인 반영까지는 검색엔진별로 시간이 걸릴 수 있습니다.")


if __name__ == "__main__":
    main()
