import os
import random
import time
from google import genai
from google.genai.errors import APIError
from httpx import RemoteProtocolError

client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

def get_randomized_seo_config(keyword: str) -> dict:
    styles = [
        "전문가적이고 객관적인 분석 톤",
        "친근하고 실용적인 가이드 톤",
        "최신 트렌드 리포트 톤",
        "트러블슈팅 및 문제해결 톤"
    ]
    intro_structures = [
        "시선 강탈형 훅: 흥미로운 통계나 사실 제시",
        "공감대 형성형 훅: 독자의 고민이나 질문 던지기",
        "개념 정의형 훅: 핵심 현상에 대한 정의와 배경 설명",
        "시급성 강조형 훅: 최근 변화를 언급하며 이유 설명"
    ]
    anchor_pools = [
        {"category": "브랜드 앵커", "examples": ["링크위키(LinkWiki)", "LinkWiki 공식 아카이브"]},
        {"category": "키워드 앵커", "examples": [keyword, f"최신 {keyword} 가이드"]},
        {"category": "일반 앵커", "examples": ["관련 상세 정보 참고하기", "공식 데이터 바로가기"]}
    ]
    
    selected_style = random.choice(styles)
    selected_intro = random.choice(intro_structures)
    chosen_pool = random.choices(anchor_pools, weights=[0.2, 0.4, 0.4], k=1)[0]
    selected_anchor_text = random.choice(chosen_pool["examples"])
    
    return {
        "style": selected_style,
        "intro_structure": selected_intro,
        "anchor_text": selected_anchor_text
    }

def generate_seo_post(keyword: str) -> str:
    config = get_randomized_seo_config(keyword)
    
    prompt = f"""
    당신은 최고 수준의 수석 SEO 콘텐츠 마케터입니다. 자연스러운 문장 구조를 구사하세요.
    'linkwiki.info'에 발행할 SEO 블로그 포스트를 Markdown 형식으로 작성해주세요.
    - 메인 키워드: {keyword}
    - 백링크 URL: https://linkwiki.info
    - 글의 톤: {config['style']}
    - 도입부: {config['intro_structure']}
    - 앵커 텍스트: [{config['anchor_text']}](https://linkwiki.info)
    - 분량: 공백 제외 1,500자 이상
    """

    max_retries = 7
    for attempt in range(max_retries):
        try:
            response = client.models.generate_content(
                model="gemini-3.8-flash",
                contents=prompt
            )
            return response.text
        except (APIError, RemoteProtocolError) as e:
            is_server_issue = False
            if isinstance(e, APIError) and e.code == 503:
                is_server_issue = True
            elif isinstance(e, RemoteProtocolError):
                is_server_issue = True

            if is_server_issue and attempt < max_retries - 1:
                wait_time = (attempt + 1) * 4
                print(f"서버 연결 끊김 또는 과부하 감지. {wait_time}초 후 재시도합니다... (시도 {attempt + 1}/{max_retries})")
                time.sleep(wait_time)
            else:
                raise e

if __name__ == "__main__":
    post = generate_seo_post("링크위키")
    print(post)
