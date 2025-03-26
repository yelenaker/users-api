# Используем официальный образ Python
FROM python:3.10

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /app

# Копируем файлы проекта внутрь контейнера
COPY . .

# Устанавливаем переменную окружения APP_VERSION
ARG APP_VERSION
ENV APP_VERSION=${APP_VERSION}

# Обновляем pip и устанавливаем зависимости
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    pip install uvicorn

# Указываем порт, который будет использоваться
EXPOSE 8000

# Запускаем веб-сервис
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
