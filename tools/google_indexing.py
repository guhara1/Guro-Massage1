# -*- coding: utf-8 -*-
"""
Google Indexing API 색인 통보 (구글은 IndexNow 미참여)
구글에 URL_UPDATED / URL_DELETED 알림을 보냅니다.

사전 준비 (1회):
  1) Google Cloud Console에서 프로젝트 생성 → "Indexing API" 사용 설정
  2) 서비스 계정 생성 후 JSON 키 다운로드 (예: service-account.json)
  3) Google Search Console에서 해당 사이트 속성에 서비스 계정 이메일을
     '소유자(owner)' 권한으로 추가
  4) 의존성 설치:  pip install google-auth requests

사용법:
  export GOOGLE_INDEXING_SA=/path/to/service-account.json
  python tools/google_indexing.py                 # urls.txt 전체 통보
  python tools/google_indexing.py URL1 URL2 ...    # 지정 URL만
  python tools/google_indexing.py --delete URL     # 삭제 통보

참고: Indexing API는 공식적으로 JobPosting/BroadcastEvent 대상이지만
URL 단위 갱신 통보에 널리 사용됩니다. 일일 호출 쿼터(기본 200)가 있습니다.
"""
import os, sys

ENDPOINT = "https://indexing.googleapis.com/v3/urlNotifications:publish"
SCOPES = ["https://www.googleapis.com/auth/indexing"]
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def load_urls(args):
    urls = [a for a in args if a.startswith("http")]
    if urls:
        return urls
    path = os.path.join(ROOT, "urls.txt")
    if not os.path.exists(path):
        sys.exit("urls.txt 가 없습니다. 먼저 `python build.py` 를 실행하세요.")
    with open(path, encoding="utf-8") as f:
        return [ln.strip() for ln in f if ln.strip()]


def main():
    sa = os.environ.get("GOOGLE_INDEXING_SA")
    if not sa or not os.path.exists(sa):
        sys.exit("환경변수 GOOGLE_INDEXING_SA 에 서비스 계정 JSON 경로를 지정하세요.")
    try:
        from google.oauth2 import service_account
        from google.auth.transport.requests import AuthorizedSession
    except ImportError:
        sys.exit("의존성이 필요합니다:  pip install google-auth requests")

    delete = "--delete" in sys.argv
    args = [a for a in sys.argv[1:] if a != "--delete"]
    urls = load_urls(args)
    notif = "URL_DELETED" if delete else "URL_UPDATED"

    creds = service_account.Credentials.from_service_account_file(sa, scopes=SCOPES)
    session = AuthorizedSession(creds)

    ok = 0
    for url in urls:
        r = session.post(ENDPOINT, json={"url": url, "type": notif}, timeout=30)
        mark = "OK " if r.status_code == 200 else "-- "
        print(f"  [{mark}] {notif} {url} → {r.status_code} {r.text[:80]}".rstrip())
        ok += r.status_code == 200
    print(f"\n완료: {ok}/{len(urls)} 성공")


if __name__ == "__main__":
    main()
