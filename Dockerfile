# Используем официальный образ Python
FROM python:3.11-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файлы проекта в контейнер
COPY app.py requirements.txt /app/
COPY templates/ /app/templates/

# Устанавливаем зависимости Python
RUN pip install --no-cache-dir -r requirements.txt

# Указываем порт, который будет открыт
EXPOSE 5000

# Указываем команду для запуска приложения
CMD ["python", "app.py"]

