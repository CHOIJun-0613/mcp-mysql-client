# server/app/nlp.py

import requests
import json
import os

# 환경 변수에서 Ollama API URL을 가져오고, 없으면 기본값으로 localhost를 사용합니다.
OLLAMA_API_URL = os.environ.get("OLLAMA_API_URL", "http://localhost:11434/api/generate")
# Ollama를 통해 다운로드한 모델의 이름
MODEL_NAME = "llama3:8b" 

def convert_natural_language_to_sql(natural_query: str, db_schema: str):
    """
    자연어 질문과 DB 스키마를 기반으로, 로컬 Ollama LLM을 호출하여 SQL 쿼리를 생성합니다.
    """
    # Instruction-tuned 모델에 맞는 형식으로 프롬프트를 구성합니다.
    # 모델이 역할을 명확히 인지하고, 요구사항에만 집중하도록 지시합니다.
    prompt = f"""
    ### 지시:
    당신은 MySQL 전문가입니다. 주어진 데이터베이스 스키마와 사용자의 질문을 바탕으로, 실행 가능한 MySQL 쿼리를 생성해야 합니다.
    - 응답은 오직 SQL 쿼리 문장 하나여야 합니다.
    - 어떠한 설명이나 다른 텍스트도 포함하지 마세요.
    - 필요한 경우에만 테이블을 JOIN하세요. 불필요한 JOIN은 피하세요.
    - 데이터베이스 스키마에 명시된 정확한 테이블 및 컬럼 이름을 사용하세요. (예: `users` 테이블의 사용자 이름은 `user_name` 컬럼에 있습니다.)
    - 사용자의 질문에 직접적으로 관련된 컬럼만 선택하거나, 명시되지 않은 경우 모든 컬럼을 선택하세요.

    ### 데이터베이스 스키마:
    {db_schema}

    ### 사용자 질문:
    "{natural_query}"

    ### SQL 쿼리:
    """

    # Ollama 서버에 보낼 데이터 페이로드
    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False,  # 응답을 스트리밍하지 않고 한 번에 받음
        "options": {
            "temperature": 0.0, # 일관된 결과를 위해 온도를 0으로 설정
            "top_p": 0.9,
            "num_predict": 128 # 최대 생성 토큰 수
        }
    }

    try:
        # 로컬 Ollama API에 POST 요청을 보냅니다.
        response = requests.post(OLLAMA_API_URL, json=payload)
        response.raise_for_status()  # HTTP 에러가 발생하면 예외를 발생시킴

        # 응답 받은 JSON 텍스트에서 'response' 키의 값을 추출합니다.
        response_text = response.json().get('response', '').strip()
        print(f"Raw response from model: {response_text}")
        
        # 모델이 가끔 ```sql ... ``` 형식으로 응답할 경우를 대비한 처리
        if response_text.startswith("```sql"):
            response_text = response_text[len("```sql"):].strip()
        if response_text.endswith("```"):
            response_text = response_text[:-len("```")].strip()
        
        # 세미콜론이 여러 개 붙는 경우를 방지
        final_sql = response_text.strip().rstrip(';') + ';'
        print(f"Processed SQL before return: {final_sql}")
        return final_sql

    except requests.exceptions.RequestException as e:
        print(f"Ollama API 호출 중 오류 발생: {e}")
        return f"Ollama 서버에 연결할 수 없습니다. Ollama가 실행 중인지 확인하세요."
    except Exception as e:
        print(f"SQL 생성 중 알 수 없는 오류 발생: {e}")
        return "SQL 생성 중 오류가 발생했습니다."
