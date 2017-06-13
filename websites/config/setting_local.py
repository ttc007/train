import os

DATABASES = {
    'default': {
        'NAME': 'helio_web',
        'ENGINE': 'django.db.backends.mysql',
        'HOST': 'localhost',
        'PORT': 3306,
        'USER': 'root',
        'PASSWORD': 'root'
    },
    'sql_db': {
        'NAME': 'ECS7',
        'ENGINE': 'sqlserver_pymssql',
        'HOST': '192.168.1.212\SQLEXPRESS',
        'USER': 'sa',
        'PASSWORD': 'abcde12345-',
        'POST':1433
    }
}

RECAPTCHA_PUBLIC_KEY = '6LdxuyMUAAAAAEm4t7YjahOec7Zc-8xZcdwNw_6c'
RECAPTCHA_PRIVATE_KEY = '6LdxuyMUAAAAALoyxmi8-y4rnWA_X9P3AWqca8TP'