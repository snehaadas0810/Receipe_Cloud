from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent

# SECRET_KEY = 'django-insecure-9kl2h@-9qg+^u#tche0o@bnjxhs9qtz9*xehu_*wibwu=!h1q%'

# DEBUG = True

# ALLOWED_HOSTS = []
# SECURITY
# SECRET_KEY = "django-insecure-xkfi1eu&39_5v@=wnpmpm8@p0w%p!e^uum@%j81!ju%q+%8438"
# DEBUG = True

SECRET_KEY = os.getenv("SECRET_KEY")
DEBUG = os.getenv("DEBUG", "False") == "True"


ALLOWED_HOSTS = [
    "13.62.94.190",
    "localhost",
    "127.0.0.1",
    "ec2-13-62-94-190.eu-north-1.compute.amazonaws.com",
    "*",
]

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "posts",  # ✅ ADD THIS
    "users",  # (if not already)
]

# ================= MIDDLEWARE =================
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

# ================= TEMPLATES =================
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        # OPTIONAL (good practice)
        "DIRS": [os.path.join(BASE_DIR, "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

# ================= DATABASE =================
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }
# ================= DATABASE =================
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ.get("DB_NAME", "postgres"),
        "USER": os.environ.get("DB_USER", "recipeuser"),
        "PASSWORD": os.environ.get("DB_PASSWORD", ""),
        "HOST": os.environ.get("DB_HOST", ""),
        "PORT": "5432",
    }
}


# ================= PASSWORD VALIDATION =================
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# ================= INTERNATIONAL =================
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# ================= STATIC FILES =================
STATIC_URL = "/static/"
STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]

# ================= MEDIA FILES =================
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# ================= AUTH USER =================
AUTH_USER_MODEL = "users.User"

# ================= LOGIN REDIRECT FIX =================
# LOGIN_URL = '/login/'              # 🔥 FIXES YOUR ERROR
# LOGIN_REDIRECT_URL = '/'          # After login
# LOGOUT_REDIRECT_URL = '/login/'   # After logout

LOGIN_URL = "/login/"  # where user goes if not logged in
LOGIN_REDIRECT_URL = "/posts/"  # ✅ after login → dashboard
LOGOUT_REDIRECT_URL = "/"  # ✅ after logout → index page


# ================= AWS S3 =================
AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")
AWS_STORAGE_BUCKET_NAME = "recipe-export-sneha"
AWS_S3_REGION_NAME = "eu-north-1"
AWS_S3_SIGNATURE_VERSION = "s3v4"
AWS_DEFAULT_ACL = None
AWS_S3_FILE_OVERWRITE = False
AWS_QUERYSTRING_AUTH = False


LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "{levelname} {asctime} {module} {message}",
            "style": "{",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
            "level": "INFO",
        },
        "core": {
            "handlers": ["console"],
            "level": "DEBUG",
        },
    },
}
