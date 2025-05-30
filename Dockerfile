FROM python:3.12-slim

# 1) 시스템 패키지 업데이트 & 크롬 의존성 설치
RUN apt-get update && apt-get install -y --no-install-recommends \
      chromium \
      chromium-driver \
      ca-certificates \
      fonts-liberation \
      libnss3 \
      libatk1.0-0 \
      libcups2 \
      libxss1 \
      libasound2 \
      libdrm2 \
      libdbus-1-3 \
      libexpat1 \
      libfontconfig1 \
      libffi7 \
      libgbm1 \
      libgtk-3-0 \
      libpango-1.0-0 \
      libxcomposite1 \
      libxdamage1 \
      libxrandr2 \
      libxshmfence1 \
      xdg-utils \
  && apt-get clean \
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
