# ── 1) 베이스 이미지: 슬림한 Python 3.10
FROM python:3.10-slim

# ── 2) 비대화형(Auto yes) 모드로
ARG DEBIAN_FRONTEND=noninteractive

# ── 3) 시스템 패키지 업데이트 & 크롬 설치
RUN apt-get update \
 && apt-get install -y --no-install-recommends \
      wget unzip curl gnupg ca-certificates \
      chromium chromium-driver \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/*

# ── 4) 환경변수: 코드에서 이 경로를 참조합니다
ENV CHROME_BIN=/usr/bin/chromium
ENV CHROMEDRIVER_BIN=/usr/bin/chromedriver

# ── 5) requirements 복사 & pip 설치
COPY requirements.txt /app/requirements.txt
WORKDIR /app
RUN pip install --upgrade pip \
 && pip install -r requirements.txt

# ── 6) 애플리케이션 코드 복사 & 포트 열기
COPY . /app
EXPOSE 8501

# ── 7) 컨테이너 시작 시 실행할 명령
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.enableCORS=false"]




