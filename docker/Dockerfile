# 베이스 이미지로 ollama/ollama의 특정 버전을 사용합니다.
# 'latest' 대신 특정 버전을 명시하면 예측 가능하고 일관된 빌드를 보장할 수 있습니다.
FROM ollama/ollama:0.1.41

# 컨테이너가 11434 포트를 외부에 노출할 것임을 명시합니다.
# Ollama API 서버의 기본 포트입니다.
EXPOSE 11434

# Docker 엔진이 컨테이너의 상태를 확인할 수 있도록 HEALTHCHECK를 설정합니다.
# 30초마다 Ollama 서버가 응답하는지 확인합니다.
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD wget -q --spider http://localhost:11434 || exit 1

# Docker 이미지를 빌드하는 시점에 llama3:8b 모델을 미리 다운로드합니다.
# 이렇게 하면 컨테이너가 시작될 때 모델을 다운로드할 필요 없이 바로 사용할 수 있습니다.
RUN ollama run llama3:8b