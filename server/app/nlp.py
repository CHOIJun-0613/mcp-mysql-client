import requests
import json
import os
import re
from dotenv import load_dotenv

load_dotenv()

# 환경 변수에서 LLM 제공자 및 설정 로드
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "groq").lower() # 기본값은 groq

# Groq API 설정
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL_NAME = os.getenv("GROQ_MODEL_NAME", "llama3-8b-8192")

# Ollama API 설정
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_MODEL_NAME = os.getenv("OLLAMA_MODEL_NAME", "gemma:7b")

def _build_messages(natural_query: str, db_schema: str):
    """
    LLM에 전달할 메시지 형식을 구성합니다.
    """
    return [
        {
            "role": "system",
            "content": f"""
당신은 MySQL 전문가입니다. 주어진 데이터베이스 스키마와 사용자의 질문을 바탕으로, 실행 가능한 MySQL 쿼리를 생성해야 합니다.
- 응답은 오직 SQL 쿼리 문장 하나여야 합니다.
- 어떠한 설명이나 다른 텍스트도 포함하지 마세요.
- 필요한 경우에만 테이블을 JOIN하세요. 불필요한 JOIN은 피하세요.
- 데이터베이스 스키마에 명시된 정확한 테이블 및 컬럼 이름을 사용하세요. (예: `users` 테이블의 '사용자 이름'은 `user_name` 컬럼입니다.)
- 테이블을 JOIN할 경우에도 데이터베이스 스키마에 명시된 정확한 테이블 및 컬럼 이름을 사용하세요.
- 사용자의 질문에 직접적으로 관련된 컬럼만 선택하거나, 명시되지 않은 경우 모든 컬럼을 선택하세요.

### 데이터베이스 스키마:
{db_schema}
"""
        },
        {
            "role": "user",
            "content": f"### 사용자 질문:\n\"{natural_query}\"\n\n### SQL 쿼리:"
        }
    ]

def _call_groq_api(messages: list):
    """
    Groq API를 호출하여 SQL 쿼리를 생성합니다.
    """
    if not GROQ_API_KEY:
        raise ValueError("GROQ_API_KEY가 .env 파일에 설정되지 않았습니다.")

    payload = {
        "model": GROQ_MODEL_NAME,
        "messages": messages,
        "temperature": 0.0,
        "max_tokens": 128,
        "top_p": 0.9,
        "stop": ["\n\n"]
    }

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    response = requests.post(GROQ_API_URL, headers=headers, json=payload)
    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"].strip()

def _call_ollama_api(messages: list):
    """
    Ollama API를 호출하여 SQL 쿼리를 생성합니다.
    """
    ollama_url = f"{OLLAMA_BASE_URL}/api/chat"
    payload = {
        "model": OLLAMA_MODEL_NAME,
        "messages": messages,
        "stream": False, # 스트리밍 비활성화
        "options": {
            "temperature": 0.0,
            "num_predict": 128,
            "top_p": 0.9,
            "stop": ["\n\n"]
        }
    }
    headers = {
        "Content-Type": "application/json"
    }

    response = requests.post(ollama_url, headers=headers, json=payload)
    response.raise_for_status()
    return response.json()["message"]["content"].strip()

def convert_natural_language_to_sql(natural_query: str, db_schema: str):
    """
    자연어 질문과 DB 스키마를 기반으로 LLM을 호출하여 SQL 쿼리를 생성합니다.
    LLM_PROVIDER 환경 변수에 따라 Groq 또는 Ollama를 사용합니다.
    """
    messages = _build_messages(natural_query, db_schema)
    response_text = ""

    try:
        if LLM_PROVIDER == "groq":
            print(f"Using Groq API with model: {GROQ_MODEL_NAME}")
            response_text = _call_groq_api(messages)
        elif LLM_PROVIDER == "ollama":
            print(f"Using Ollama API with model: {OLLAMA_MODEL_NAME} at {OLLAMA_BASE_URL}")
            response_text = _call_ollama_api(messages)
        else:
            return f"지원하지 않는 LLM_PROVIDER: {LLM_PROVIDER}. 'groq' 또는 'ollama' 중 하나여야 합니다."

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
        print(f"API 호출 중 오류 발생: {e}")
        return f"API 호출 중 오류 발생: {e}"
    except ValueError as e:
        print(f"설정 오류: {e}")
        return f"설정 오류: {e}"
    except Exception as e:
        print(f"SQL 생성 중 알 수 없는 오류 발생: {e}")
        return "SQL 생성 중 오류가 발생했습니다."