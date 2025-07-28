import requests
import json
import os

# FastMCP 서버 URL
FASTMCP_SERVER_URL = "http://localhost:8000/query"

# 한국어 질문
natural_query = "가장 많은 주문을 한 사용자의 이름과 이메일을 조회해줘 (주문 건수 기준)"

# 데이터베이스 스키마 (이전 단계에서 가져온 스키마를 여기에 붙여넣습니다.)
db_schema = """
Table `orders` (
  `order_id` int,
  `user_id` int,
  `product_name` varchar(100),
  `amount` decimal(10,2),
  `order_date` date,
);

Table `post` (
  `post_id` binary(16),
  `author` varchar(255),
  `contents` varchar(255),
  `created_date_time` datetime(6),
  `title` varchar(255),
);

Table `user` (
  `user_id` binary(16),
  `email` varchar(255),
  `name` varchar(255),
  `password` varchar(255),
);

Table `users` (
  `id` int,
  `user_name` varchar(50),
  `email` varchar(100),
  `signup_date` date,
);
"""

# 요청 페이로드 생성
payload = {
    "query": natural_query
}

# POST 요청 보내기
try:
    response = requests.post(FASTMCP_SERVER_URL, json=payload)
    response.raise_for_status()  # HTTP 오류 발생 시 예외 발생
    print(response.json())
except requests.exceptions.RequestException as e:
    print(f"FastMCP 서버 호출 중 오류 발생: {e}")
    if e.response is not None:
        print(f"서버 응답: {e.response.json()}")
except Exception as e:
    print(f"예상치 못한 오류 발생: {e}")
