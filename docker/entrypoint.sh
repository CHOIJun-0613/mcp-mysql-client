#!/bin/sh

# 스크립트 실행 중 오류가 발생하면 즉시 중단합니다.
set -e

# Ollama 서버를 백그라운드에서 실행합니다.
ollama serve &

# 백그라운드에서 실행된 서버의 프로세스 ID(PID)를 저장합니다.
pid=$!

# 서버가 응답할 때까지 반복적으로 확인합니다. (최대 30초)
# 고정된 sleep 시간보다 안정적입니다.
echo "Waiting for Ollama server to be ready..."
max_retries=15
count=0
while ! ollama list >/dev/null 2>&1; do
    if ! ps -p $pid > /dev/null; then
        echo "Ollama server failed to start."
        exit 1
    fi
    count=$((count+1))
    if [ $count -ge $max_retries ]; then
        echo "Ollama server did not start in time."
        exit 1
    fi
    sleep 2
done

echo "Checking for gemma:7b model and pulling if it does not exist..."
# gemma:7b 모델이 없으면 다운로드합니다. 이미 있다면 이 단계는 건너뜁니다.
ollama pull gemma:7b

echo "Ollama is ready to serve."

# 백그라운드의 Ollama 서버 프로세스가 종료될 때까지 기다립니다.
# 이 명령이 없으면 스크립트가 끝나면서 컨테이너가 바로 종료됩니다.
wait $pid