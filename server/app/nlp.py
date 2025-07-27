import openai
import os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def convert_natural_language_to_sql(natural_query: str, db_schema: str):
    if not openai.api_key:
        return "OpenAI API 키가 설정되지 않았습니다."

    prompt = f"""
    당신은 MySQL 전문가입니다. 주어진 DB 스키마를 바탕으로, 사용자의 질문에 가장 적합한 SQL 쿼리만 생성해주세요.
    어떤 설명도 추가하지 말고 오직 SQL 쿼리만 응답해야 합니다.

    ### DB 스키마:
    {db_schema}

    ### 사용자 질문:
    "{natural_query}"

    ### 생성된 SQL 쿼리:
    """
    try:
        response = openai.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You translate natural language to SQL."},
                {"role": "user", "content": prompt}
            ],
            temperature=0,
        )
        sql_query = response.choices[0].message.content.strip()
        if sql_query.startswith("```sql"):
            sql_query = sql_query.split('\n', 1)[1]
            if sql_query.endswith("```"):
                sql_query = sql_query[:-3].strip()
        return sql_query
    except Exception as e:
        return f"OpenAI API 호출 오류: {e}"