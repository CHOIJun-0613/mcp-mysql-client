import requests
import json
import os
import re
from dotenv import load_dotenv

load_dotenv()

# Groq API 설정
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
MODEL_NAME = "llama3-8b-8192" 

def convert_natural_language_to_sql(natural_query: str, db_schema: str):
    """
    자연어 질문과 DB 스키마를 기반으로, Groq LLM을 호출하여 SQL 쿼리를 생성합니다.
    """
    if not GROQ_API_KEY:
        return "GROQ_API_KEY가 .env 파일에 설정되지 않았습니다."

    # Instruction-tuned 모델에 맞는 형식으로 프롬프트를 구성합니다.
    # 모델이 역할을 명확히 인지하고, 요구사항에만 집중하도록 지시합니다.
    messages = [
        {
            "role": "system",
            "content": f"""
당신은 MySQL 전문가입니다. 주어진 데이터베이스 스키마와 사용자의 질문을 바탕으로, 실행 가능한 MySQL 쿼리를 생성해야 합니다.
- 응답은 오직 SQL 쿼리 문장 하나여야 합니다.
- 어떠한 설명이나 다른 텍스트도 포함하지 마세요.
- 필요한 경우에만 테이블을 JOIN하세요. 불필요한 JOIN은 피하세요.
- 데이터베이스 스키마에 명시된 정확한 테이블 및 컬럼 이름을 사용하세요. (예: `users` 테이블의 '사용자 이름'은 `user_name` 컬럼입니다.)
- '사용자의 이름', '사용자명', '사용자 이름'에 대한 쿼리를 생성할 때는 항상 `users` 테이블의 `user_name` 컬럼을 사용하세요.
- 테이블을 JOIN할 경우에도 데이터베이스 스키마에 명시된 정확한 테이블 및 컬럼 이름을 사용하세요.
- 사용자의 질문에 직접적으로 관련된 컬럼만 선택하거나, 명시되지 않은 경우 모든 컬럼을 선택하세요.
- 사용자의 이름을 조회하거나 참조할 때는 항상 `users` 테이블의 `user_name` 컬럼을 사용하세요.

### 데이터베이스 스키마:
{db_schema}
"""
        },
        {
            "role": "user",
            "content": f"### 사용자 질문:\n\"{natural_query}\"\n\n### SQL 쿼리:"
        }
    ]

    # Groq API에 보낼 데이터 페이로드
    payload = {
        "model": MODEL_NAME,
        "messages": messages,
        "temperature": 0.0, # 일관된 결과를 위해 온도를 0으로 설정
        "max_tokens": 128, # 최대 생성 토큰 수
        "top_p": 0.9,
        "stop": ["\n\n"] # SQL 쿼리 생성 후 중지하도록 유도
    }

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    try:
        # Groq API에 POST 요청을 보냅니다.
        response = requests.post(GROQ_API_URL, headers=headers, json=payload)
        response.raise_for_status()  # HTTP 에러가 발생하면 예외를 발생시킴

        # 응답 받은 JSON 텍스트에서 'content' 키의 값을 추출합니다.
        response_text = response.json()["choices"][0]["message"]["content"].strip()
        print(f"Raw response from model: {response_text}")
        
        # 모델이 가끔 ```sql ... ``` 형식으로 응답할 경우를 대비한 처리
        if response_text.startswith("```sql"):
            response_text = response_text[len("```sql"):].strip()
        if response_text.endswith("```"):
            response_text = response_text[:-len("```")].strip()

        # users 테이블의 'name' 컬럼을 'user_name'으로 대체 (모델이 계속 'name'을 생성하는 문제 해결)
        if "FROM users" in response_text.upper():
            response_text = re.sub(r'\bname\b', 'user_name', response_text, flags=re.IGNORECASE)
            response_text = re.sub(r'([a-zA-Z0-9_]+\.)name', r'\1user_name', response_text, flags=re.IGNORECASE)
            print(f"After name replacement: {response_text}")
        # 세미콜론이 여러 개 붙는 경우를 방지
        final_sql = response_text.strip().rstrip(';') + ';'
        print(f"Processed SQL before return: {final_sql}")
        return final_sql

    except requests.exceptions.RequestException as e:
        print(f"Groq API 호출 중 오류 발생: {e}")
        return f"Groq API 호출 중 오류 발생: {e}"
    except Exception as e:
        print(f"SQL 생성 중 알 수 없는 오류 발생: {e}")
        return "SQL 생성 중 오류가 발생했습니다."