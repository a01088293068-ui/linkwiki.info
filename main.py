import os
import requests
from google import genai

API_KEY = os.environ.get("BLOGGER_API_KEY")
BLOG_ID = os.environ.get("BLOG_ID")
GEMINI_KEY = os.environ.get("GEMINI_API_KEY")

client = genai.Client(api_key=GEMINI_KEY)
prompt = "최근 암호화폐 시장 동향과 주요 이슈를 요약하여 블로그 포스팅용 글로 마크다운 없이 작성해줘."
response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=prompt,
)

url = f"https://www.googleapis.com/blogger/v3/blogs/{BLOG_ID}/posts/?key={API_KEY}"
headers = {"Content-Type": "application/json"}
body = {
    "title": "오늘의 암호화폐 시장 동향",
    "content": response.text
}
requests.post(url, headers=headers, json=body)
