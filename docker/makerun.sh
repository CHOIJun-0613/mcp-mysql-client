# .\docker 폴더에서 실행
cd ./docker
# Docker 이미지를 빌드합니다.
docker build --no-cache -t ollama-container:latest -f ./Dockerfile .

# Docker 컨테이너를 실행합니다.
docker run -d --name ollama-container -p 11434:11434 ollama-container:latest

# gemma:7b 모델을 다운로드합니다.(5.0GB)
# Ollama 서버가 실행 중인 상태에서 모델을 다운로드합니다.

docker exec ollama-container ollama pull gemma:7b 

# 현재 실행 중인 컨테이너 목록 확인
docker ps

# 컨테이너의 로그 확인 (Ollama 서버 시작 및 모델 로딩 과정 확인)
docker logs -f ollama-container
