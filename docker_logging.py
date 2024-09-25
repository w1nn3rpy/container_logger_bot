import docker

# Подключение к Docker
client = docker.from_env()

# Указываем имя контейнера
container_name = "dudevpn_bot"


def get_container_logs():
    try:
        container = client.containers.get(container_name)
        logs = container.logs(tail=100)  # Получаем последние 100 строк логов
        return logs.decode("utf-8")

    except Exception as e:
        return f'Ошибка при получении логов: {e}'
