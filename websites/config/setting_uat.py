import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

DATABASES = {
    'default': {
        'NAME': 'helio_web',
        'ENGINE': 'django.db.backends.mysql',
        'HOST': 'localhost',
        'PORT': 3306,
        'USER': 'helio',
        'PASSWORD': 'admin@helio.vn'
    },
    'sql_db': {
        'NAME': 'ECS7',
        'ENGINE': 'sqlserver_pymssql',
        'HOST': '113.160.225.204:1433',
        'USER': 'sa',
        'PASSWORD': 'vooc2017',
        'PORT':1433
    }

}

RECAPTCHA_PUBLIC_KEY = '6LfMmSYUAAAAANJJC-toiepJxWBFlPXgfz9Cg5tA'
RECAPTCHA_PRIVATE_KEY = '6LfMmSYUAAAAAI8a3MHrDW07gjr9kddPAMd2nOTL'

FB_APP_ID = '753086748186657'
SOCIAL_AUTH_FACEBOOK_KEY = '753086748186657'
SOCIAL_AUTH_FACEBOOK_SECRET = '560179f08361bae229869d5b50312ea5'

PUSH_NOTIFICATIONS_SETTINGS = {
    "FCM_API_KEY": "AAAAMkND2_U:APA91bEVkDFA8uACGPTTj-Vc86kg4fuyhrPuUmGHJdzkuBaaJh4ZQuc09zMZCEt2xaSj5Xi7opPT9OZHq-hxDrWmqfkRGqRv38uC2nqHHK3Xwy-jwglWoSwIYywpT-qcsoW9TKAsiUayeRAkj_AYJ0AG-D02Ubx0jg",
    "FCM_ERROR_TIMEOUT": 3600,
    "APNS_CERTIFICATE": os.path.join(BASE_DIR, "key_apns/pem_dev/push_dev.pem"),
    "APNS_USE_SANDBOX": True,
    "APNS_TOPIC": "vn.vooc.helio.mobile",
}
