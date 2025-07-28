import sys
import os

# 이 스크립트가 프로젝트 루트 어디에서 실행되더라도 경로를 올바르게 찾도록 설정합니다.
project_root = os.path.dirname(os.path.abspath(__file__))
server_app_path = os.path.join(project_root, 'server', 'app')
if server_app_path not in sys.path:
    sys.path.append(server_app_path)

# server.app.database 모듈에서 스키마 조회 함수를 가져옵니다.
from database import get_db_schema

def save_schema_to_file():
    """DB 스키마를 조회하여 'server/db_schema.txt' 파일에 저장합니다."""
    print("데이터베이스에서 최신 스키마 정보를 가져오는 중입니다...")
    schema_content = get_db_schema()
    
    # 프로젝트 루트 아래의 'server' 폴더에 저장 경로를 지정합니다.
    output_path = os.path.join(project_root, 'server', 'db_schema.txt')

    if "실패" in schema_content or "오류" in schema_content:
        print(f"스키마 조회에 실패하여 파일을 업데이트하지 않습니다. 오류: {schema_content}")
        return

    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(schema_content)
        print(f"✅ DB 스키마가 성공적으로 '{output_path}' 파일에 저장되었습니다.")
    except IOError as e:
        print(f"❌ 파일 작성 중 오류 발생: {e}")

if __name__ == "__main__":
    save_schema_to_file()