import os
import requests
from google import genai

API_KEY = os.environ.get("BLOGGER_API_KEY")
BLOG_ID = os.environ.get("BLOG_ID")
GEMINI_KEY = os.environ.get("GEMINI_API_KEY")

client = genai.Client(api_key=GEMINI_KEY)
prompt = "링크위키인포(linkwiki.info) 블로그에 발행할 유용한 IT 및 웹사이트 관련 정보를 마크다운 없이 본문 내용 위주로 작성해줘."
response = client.models.generate_content(
    model="gemini-3.8-flash",
    contents=prompt,
)

url = f"https://www.googleapis.com/blogger/v3/blogs/{BLOG_ID}/posts/?key={API_KEY}"
headers = {"Content-Type": "application/json"}
body = {
    "title": "유용한 IT 및 웹사이트 모음",
    "content": response.text
}
requests.post(url, headers=headers, json=body)
