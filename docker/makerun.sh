# .\docker 폴더에서 실행
cd ./docker
# Docker 이미지를 빌드합니다.
docker build -t ollama-llama3:latest -f ./Dockerfile .

# Docker 컨테이너를 실행합니다.
docker run -d --name ollama-llama3-container -p 11434:11434 ollama-llama3:latest

# 현재 실행 중인 컨테이너 목록 확인
docker ps

# 컨테이너의 로그 확인 (Ollama 서버 시작 및 모델 로딩 과정 확인)
docker logs -f ollama-llama3-container
