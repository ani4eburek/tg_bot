FROM python:3.11-slim

WORKDIR /app

# Копируем требования и устанавливаем
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь проект
COPY . .

# Запускаем бота (замени main.py на имя твоего главного файла)
CMD ["python", "main.py"]