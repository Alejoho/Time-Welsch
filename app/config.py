import os


class BaseConfig(object):
    """Base configuration."""

    # main config
    SECRET_KEY = os.getenv("SECRET_KEY")
    SECURITY_PASSWORD_SALT = os.getenv("SECURITY_PASSWORD_SALT")

    # API keys
    HUNTER_API_KEY = os.getenv("HUNTER_API_KEY")
    RECAPTCHA_PUBLIC_KEY = os.getenv("RECAPTCHA_PUBLIC_KEY")
    RECAPTCHA_PRIVATE_KEY = os.getenv("RECAPTCHA_PRIVATE_KEY")

    # mail settings
    MAIL_SERVER = "smtp.gmail.com"
    MAIL_PORT = 587
    MAIL_USE_TLS = True

    # gmail authentication
    MAIL_USERNAME = os.getenv("MAIL_USERNAME")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")

    # mail accounts
    MAIL_DEFAULT_SENDER = os.getenv("MAIL_DEFAULT_SENDER")
    MAIL_CONTACT_ME_RECEIVER = os.getenv("MAIL_CONTACT_ME_RECEIVER")

    # token max ages
    ACCOUNT_CONFIRMATION_MAX_AGE = 3600
    RESET_PASSWORD_MAX_AGE = 300

    REMEMBER_COOKIE_DURATION = 2592000


class DevelopmentConfig(BaseConfig):
    """Development configuration."""

    DEBUG = True
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
    JOBS = [
        {
            "id": "delete_demo_users_job",
            "func": "app.routes.complements:delete_demo_users",
            "trigger": "interval",
            "seconds": 15,
        }
    ]


class ProductionConfig(BaseConfig):
    """Production configuration."""

    DEBUG = False
    WTF_CSRF_ENABLED = True
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
    JOBS = [
        {
            "id": "delete_demo_users_job",
            "func": "app.routes.complements:delete_demo_users",
            "trigger": "interval",
            "days": 1,
        }
    ]
