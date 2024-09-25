# Используем базовый образ Python
FROM python:3.12

# Копируем все файлы проекта в контейнер
WORKDIR /usr/src/app
COPY . .

# Устанавливаем зависимости Python
RUN pip install --no-cache-dir -r requirements.txt

# Запуск бота
CMD ["python", "bot.py"]