import os

POSTGRES_HOST = os.getenv('POSTGRES_HOST', 'localhost:6401')
POSTGRES_DATABASE = os.getenv('POSTGRES_DATABASE', 'postgres')
POSTGRES_USER = os.getenv('POSTGRES_USER', 'postgres')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD', 'postgres')

POSTGRES_URL = f'postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}/{POSTGRES_DATABASE}'

NBRB_API_URL = 'https://api.nbrb.by/exrates/rates'