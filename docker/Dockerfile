# 베이스 이미지로 ollama/ollama의 특정 버전을 사용합니다.
# 'latest' 대신 특정 버전을 명시하면 예측 가능하고 일관된 빌드를 보장할 수 있습니다.
FROM ollama/ollama:0.1.41

# entrypoint.sh 스크립트를 컨테이너에 복사하고 실행 권한을 부여합니다.
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# 컨테이너가 11434 포트를 외부에 노출할 것임을 명시합니다.
# Ollama API 서버의 기본 포트입니다.
EXPOSE 11434

# 컨테이너가 시작될 때 이 스크립트를 실행하도록 설정합니다.
ENTRYPOINT ["/entrypoint.sh"]