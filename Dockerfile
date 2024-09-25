# Используем базовый образ Python
FROM python:3.12

RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    docker.io \
    && rm -rf /var/lib/apt/lists/*

# Копируем все файлы проекта в контейнер
WORKDIR /usr/src/app
COPY . .

# Устанавливаем зависимости Python
RUN pip install --no-cache-dir -r requirements.txt

# Запуск бота
CMD ["python", "bot.py"]