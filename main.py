import os
import requests
from google import genai
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request

BLOG_ID = os.environ["BLOG_ID"]
GEMINI_KEY = os.environ["GEMINI_API_KEY"]

CLIENT_ID = os.environ["GOOGLE_CLIENT_ID"]
CLIENT_SECRET = os.environ["GOOGLE_CLIENT_SECRET"]
REFRESH_TOKEN = os.environ["GOOGLE_REFRESH_TOKEN"]

# 1. Gemini로 블로그 글 생성
client = genai.Client(api_key=GEMINI_KEY)

prompt = """
링크위키인포(linkwiki.info)에 관련된
유용한 IT 및 웹사이트 활용 정보를 작성해줘.

조건:
- 한국어로 작성
- IT, 웹사이트, 인터넷 활용법 중심
- 암호화폐 등 무관한 주제 제외
- 자연스럽고 전문적인 문체
- 확인되지 않은 정보는 사실처럼 작성하지 않기
- 제목 없이 본문만 작성
- 마크다운 사용하지 않기
- HTML 문단 태그 사용
- 마지막에 https://linkwiki.info/ 자연스럽게 소개
"""

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=prompt
)

content = response.text

if not content or not content.strip():
    raise RuntimeError("Gemini 글 생성 실패")

print("Gemini 글 생성 성공")

# 2. Blogger OAuth 인증
credentials = Credentials(
    token=None,
    refresh_token=REFRESH_TOKEN,
    token_uri="https://oauth2.googleapis.com/token",
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    scopes=["https://www.googleapis.com/auth/blogger"]
)

credentials.refresh(Request())

# 3. Blogger 게시
url = f"https://www.googleapis.com/blogger/v3/blogs/{BLOG_ID}/posts/"

headers = {
    "Authorization": f"Bearer {credentials.token}",
    "Content-Type": "application/json"
}

body = {
    "kind": "blogger#post",
    "title": "유용한 IT 및 웹사이트 활용 정보",
    "content": content
}

result = requests.post(
    url,
    headers=headers,
    params={"isDraft": True},
    json=body,
    timeout=60
)

# 4. 오류 확인
if not result.ok:
    raise RuntimeError(
        f"Blogger 게시 실패: {result.status_code} / {result.text}"
    )

post = result.json()

print("Blogger 초안 생성 성공")
print("게시글 ID:", post.get("id"))
print("게시글 제목:", post.get("title"))
print("게시글 상태:", post.get("status"))
print("게시글 URL:", post.get("url"))
