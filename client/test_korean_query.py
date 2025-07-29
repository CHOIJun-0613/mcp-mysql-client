import requests
import json
import os

# FastMCP 서버 URL
FASTMCP_SERVER_URL = "http://localhost:8000/query"

# 테스트할 한국어 질문
#natural_query = "가장 많은 주문을 한 사용자의 이름과 이메일을 조회해줘 (주문 건수 기준)"
natural_query = "가장 비싼 상품을 주문한 사용자의 이름과 상품명을 조회해줘."


'''
     1. 이메일 주소가 'gildong@example.com'인 사용자의 이름과 가입일을 알려줘.
       * (예상 SQL: SELECT user_name, signup_date FROM users WHERE email = 'gildong@example.com';)

   2. 노트북을 주문한 사용자의 이름과 이메일을 조회해줘.
       * (예상 SQL: SELECT u.user_name, u.email FROM users u JOIN orders o ON u.id = o.user_id WHERE
         o.product_name = '노트북';)

   3. 각 사용자별 총 주문 금액을 조회해줘.
       * (예상 SQL: SELECT u.user_name, SUM(o.amount) FROM users u JOIN orders o ON u.id = o.user_id GROUP BY
         u.user_name;)

   4. 2024년 7월 5일 이후에 주문된 모든 상품의 이름을 조회해줘.
       * (예상 SQL: SELECT product_name FROM orders WHERE order_date > '2024-07-05';)

   5. 가장 비싼 상품을 주문한 사용자의 이름과 상품명을 조회해줘.
       * (예상 SQL: SELECT u.user_name, o.product_name FROM users u JOIN orders o ON u.id = o.user_id ORDER BY
         o.amount DESC LIMIT 1;)
'''

# 참고: 데이터베이스 스키마는 FastMCP 서버가 API 요청 시 동적으로 조회합니다.
# 현재 적용된 스키마를 확인하려면 프로젝트 루트의 'get_db_schema.py'를 실행하여
# 'server/db_schema.txt' 파일을 생성/업데이트할 수 있습니다.

# 요청 페이로드 생성
payload = {
    "query": natural_query
}

# POST 요청 보내기
print(f"'{natural_query}' 질문을 서버로 전송합니다...")
try:
    response = requests.post(FASTMCP_SERVER_URL, json=payload)
    response.raise_for_status()  # HTTP 오류 발생 시 예외 발생
    
    print("✅ 서버 응답:")
    # JSON 응답을 예쁘게 출력
    print(json.dumps(response.json(), indent=2, ensure_ascii=False))

except requests.exceptions.RequestException as e:
    print(f"❌ FastMCP 서버 호출 중 오류 발생: {e}")
    if e.response is not None:
        try:
            # 오류 응답도 JSON 형식으로 예쁘게 출력
            print(f"서버 응답: {json.dumps(e.response.json(), indent=2, ensure_ascii=False)}")
        except json.JSONDecodeError:
            print(f"서버 응답 (Raw): {e.response.text}")
except Exception as e:
    print(f"❌ 예상치 못한 오류 발생: {e}")
