# MySQL-MCP: 자연어 DB 조회 프로젝트

이 프로젝트는 **FastAPI를 기반으로 MCP(Model Context Protocol) 서버를 구현**하는 것을 목표로 합니다. 사용자가 자연어로 질문하면, AI가 이를 SQL 쿼리로 변환하여 MySQL 데이터베이스의 정보를 조회하고 결과를 반환하는 시스템입니다.

## 🚀 시작하기

### 1. 폴더 구조 생성
제공된 가이드에 따라 폴더와 파일을 생성합니다.

### 2. 환경 변수 설정
프로젝트 루트에 `.env` 파일을 만들고 DB 및 API 키 정보를 입력합니다.

### 3. 의존성 설치
각 `requirements.txt` 파일을 사용하여 필요한 라이브러리를 설치합니다.
```bash
# 서버용 라이브러리 설치
pip install -r server/requirements.txt

# 클라이언트용 라이브러리 설치
pip install -r client/requirements.txt
```

### 4. 서버 실행
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 5. 클라이언트 실행
다른 터미널을 열고 다음을 실행합니다.
```bash
python client/simple_client.py
```