from decouple import config

SECRET_KEY = config('PASSWORD')

database_hostname = config('DATABASE_HOSTNAME')
database_port = config('DATABASE_PORT')
database_password = config('DATABASE_PASSWORD')
database_name = config('DATABASE_NAME')
database_username = config('DATABASE_USERNAME')

my_chat_id = config('MY_CHAT_ID')
