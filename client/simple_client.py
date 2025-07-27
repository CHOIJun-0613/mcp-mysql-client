import requests
import json

SERVER_URL = "http://127.0.0.1:8000/query"

def ask_question(question: str):
    print(f"질문: {question}\n")
    try:
        response = requests.post(SERVER_URL, json={"query": question})
        if response.status_code == 200:
            result = response.json()
            print("="*30)
            print("      서버 응답 결과")
            print("="*30)
            print(f"SQL 쿼리: {result['sql_query']}")
            print(f"실행 상태: {result['status']}")
            if result['data']:
                print("데이터:")
                print(json.dumps(result['data'], indent=2, ensure_ascii=False))
            print("="*30)
        else:
            print(f"에러 발생: {response.status_code}\n{response.text}")

    except requests.exceptions.RequestException as e:
        print(f"서버에 연결할 수 없습니다: {e}")

if __name__ == "__main__":
    # 테스트하고 싶은 질문을 여기에 입력하세요.
    question_to_ask = "모든 유저의 이름을 알려줘"
    ask_question(question_to_ask)