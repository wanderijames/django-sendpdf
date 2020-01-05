import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

WKTHMLTOPDF_PATH = "/usr/local/bin/wkhtmltopdf"

SECRET_KEY = 'fake-key'
INSTALLED_APPS = [
    "tests",
    "sendpdf"
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


STATIC_URL = '/static/'
