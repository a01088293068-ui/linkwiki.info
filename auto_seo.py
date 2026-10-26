import os
import random
from openai import OpenAI

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

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
    
    system_prompt = "당신은 최고 수준의 수석 SEO 콘텐츠 마케터입니다. 자연스러운 문장 구조를 구사하세요."
    user_prompt = f"""
    'linkwiki.info'에 발행할 SEO 블로그 포스트를 Markdown 형식으로 작성해주세요.
    - 메인 키워드: {keyword}
    - 백링크 URL: https://linkwiki01.com
    - 글의 톤: {config['style']}
    - 도입부: {config['intro_structure']}
    - 앵커 텍스트: [{config['anchor_text']}](https://linkwiki01.com)
    - 분량: 공백 제외 1,500자 이상
    """

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.8,
        presence_penalty=0.6,
        frequency_penalty=0.4,
        max_tokens=3500
    )
    return response.choices[0].message.content
