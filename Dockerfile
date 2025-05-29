FROM python:3.12-slim

# 1) 시스템 패키지 설치
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
      chromium \
      chromium-driver \
      default-jre-headless \
    && rm -rf /var/lib/apt/lists/*

# 2) 작업 디렉터리 설정
WORKDIR /app

# 3) 의존성 복사 및 설치
COPY requirements.txt /app/
RUN pip install --upgrade pip \
    && pip install -r requirements.txt

# 4) 소스 복사
COPY . /app

# 5) 환경변수 설정
ENV CHROME_BIN=/usr/bin/chromium \
    CHROMEDRIVER_BIN=/usr/bin/chromedriver

# 6) 스트림릿 실행
EXPOSE 8501
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
