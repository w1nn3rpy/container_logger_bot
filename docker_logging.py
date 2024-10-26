import docker
from collections import deque
from datetime import datetime, timedelta

# Подключение к Docker
client = docker.from_env()

# Указываем имя контейнера
container_name = "dudevpn_bot"

LOG_EXPIRY_TIME = timedelta(minutes=5)

log_queue = deque()

def add_log(log):
    # Добавляем лог с текущим временем
    log_queue.append((log, datetime.now()))
    # Удаляем старые логи
    remove_expired_logs()


def remove_expired_logs():
    while log_queue and (datetime.now() - log_queue[0][1] > LOG_EXPIRY_TIME):
        log_queue.popleft()  # Удаляем самый старый лог, если он просрочен



def stream_container_logs():
    try:
        container = client.containers.get(container_name)
        buffer = ""  # Буфер для накопления символов
        for line in container.logs(stream=True):
            for char in line.decode("utf-8"):
                if char == '\n':  # Если встретили символ новой строки
                    log_message =  buffer.strip()  # Отправляем собранную строку и очищаем буфер
                    yield log_message
                    add_log(log_message)
                    buffer = ""  # Очищаем буфер для следующей строки
                else:
                    buffer += char  # Добавляем символ в буфер

        # Если есть остатки в буфере, отправляем их
        if buffer:
            log_message = buffer.strip()
            yield log_message
            add_log(log_message)

    except Exception as e:
        yield f'Ошибка при получении логов: {e}'

