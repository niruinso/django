FROM python:3.13-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    make \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

ENTRYPOINT ["sh", "-c", "echo 'ЗАПУСК ТЕСТОВ...' && make run_test && echo 'ТЕСТЫ ЗАВЕРШЕНЫ. ЗАПУСК ПРИЛОЖЕНИЯ...' && make run_launch"]