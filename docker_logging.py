import docker

# Подключение к Docker
client = docker.from_env()

# Указываем имя контейнера
container_name = "dudevpn_bot"


def stream_container_logs():
    try:
        container = client.containers.get(container_name)
        for line in container.logs(stream=True):
            print(line)
            yield line.decode('utf-8')

    except Exception as e:
        return f'Ошибка при получении логов: {e}'
