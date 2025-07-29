FROM gitpod/workspace-full:latest

USER gitpod
     
# docker-compose, mysql-client, python 설치
RUN sudo apt-get update && \
    sudo apt-get install -y --no-install-recommends \
    docker-compose \
    mysql-client \
    locales \
    python3 \
    python3-pip \
    python3-venv && \
    sudo apt-get clean && \
    sudo rm -rf /var/lib/apt/lists/*

# 타임존 설정
RUN sudo ln -sf /usr/share/zoneinfo/Asia/Seoul /etc/localtime

# 한국어 로케일 설정
RUN sudo locale-gen ko_KR.UTF-8 && sudo update-locale LANG=ko_KR.UTF-8 

ENV LANG ko_KR.UTF-8
ENV LANGUAGE ko_KR:ko
ENV LC_ALL ko_KR.UTF-8