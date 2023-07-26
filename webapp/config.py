import os
from dotenv import load_dotenv, find_dotenv

if find_dotenv():
    load_dotenv()
else:
    exit("Переменные окружения не загружены, т.к отсутствует файл .env")

DJANGO_SECRET_KEY = os.getenv("DJANGO_SECRET_KEY")
