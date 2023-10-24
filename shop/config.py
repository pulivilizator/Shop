from environs import Env
from dataclasses import dataclass


@dataclass
class DataBase:
    name: str
    user: str
    password: str
    host: str
    port: int


@dataclass
class RedisDB:
    host: str
    port: int
    db: int


@dataclass
class SMTP:
    email_host: str
    email_host_user: str
    email_host_password: str
    email_port: int


@dataclass
class ReCaptchaKey:
    secret_key: str
    public_key: str


@dataclass
class CeleryData:
    host: str
    port: int
    rabbitmq_user: str
    rabbitmq_password: str
    rabbitmq_vhost: str


@dataclass
class Stripe:
    pub_key: str
    secret_key: str
    webhook_secret: str


@dataclass
class Config:
    db: DataBase
    redis: RedisDB
    smtp: SMTP
    recaptcha: ReCaptchaKey
    celery: CeleryData
    stripe: Stripe


def config(path=None):
    env = Env()
    env.read_env(path)

    return Config(

        db=DataBase(name=env('DB_NAME'),
                    user=env('DB_USER'),
                    password=env('DB_PASSWORD'),
                    host=env('DB_HOST'),
                    port=env.int('DB_PORT')),

        smtp=SMTP(email_host=env('EMAIL_HOST'),
                  email_host_user=env('EMAIL_HOST_USER'),
                  email_host_password=env('EMAIL_HOST_PASSWORD'),
                  email_port=env.int('EMAIL_PORT')),

        redis=RedisDB(host=env('REDIS_HOST'),
                      port=env.int('REDIS_PORT'),
                      db=env.int('REDIS_DB')),

        recaptcha=ReCaptchaKey(secret_key=env('GOOGLE_RECAPTCHA_SECRET_KEY'),
                               public_key=env('GOOGLE_RECAPTCHA_PUBLIC_KEY')),

        celery=CeleryData(host=env('CELERY_HOST'),
                          port=env.int('CELERY_PORT'),
                          rabbitmq_user=env('CELERY_RABBITMQ_USER'),
                          rabbitmq_password=env('CELERY_RABBITMQ_PASSWORD'),
                          rabbitmq_vhost=env('CELERY_RABBITMQ_VHOST')),

        stripe=Stripe(pub_key=env('STRIPE_PUBLIC_KEY'),
                      secret_key=env('STRIPE_SECRET_KEY'),
                      webhook_secret=env('STRIPE_WEBHOOK_SECRET')),

    )
