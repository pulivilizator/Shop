from dataclasses import dataclass

from environs import Env


@dataclass
class DjangoSettings:
    secret_key: str
    debug: bool
    hosts: list

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
    broker_url: str


@dataclass
class Stripe:
    pub_key: str
    secret_key: str
    webhook_secret: str


@dataclass
class Config:
    django_settings: DjangoSettings
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
        django_settings=DjangoSettings(secret_key=env('DJANGO_SECRET_KEY'),
                                       debug=env.bool('DEBUG'),
                                       hosts=env.list('ALLOWED_HOSTS', delimiter=' ')),

        db=DataBase(name=env('POSTGRES_DB'),
                    user=env('POSTGRES_USER'),
                    password=env('POSTGRES_PASSWORD'),
                    host=env('POSTGRES_HOST'),
                    port=env.int('POSTGRES_PORT')),

        smtp=SMTP(email_host=env('EMAIL_HOST'),
                  email_host_user=env('EMAIL_HOST_USER'),
                  email_host_password=env('EMAIL_HOST_PASSWORD'),
                  email_port=env.int('EMAIL_PORT')),

        redis=RedisDB(host=env('REDIS_HOST'),
                      port=env.int('REDIS_PORT'),
                      db=env.int('REDIS_DB')),

        recaptcha=ReCaptchaKey(secret_key=env('GOOGLE_RECAPTCHA_SECRET_KEY'),
                               public_key=env('GOOGLE_RECAPTCHA_PUBLIC_KEY')),

        celery=CeleryData(
            broker_url=f'amqp://{env('RABBITMQ_DEFAULT_USER')}:{env('RABBITMQ_DEFAULT_PASS')}@{env('RABBITMQ_HOST')}:{env('RABBITMQ_PORT')}/{env('RABBITMQ_VHOST')}'
        ),

        stripe=Stripe(pub_key=env('STRIPE_PUBLIC_KEY'),
                      secret_key=env('STRIPE_SECRET_KEY'),
                      webhook_secret=env('STRIPE_WEBHOOK_SECRET')),

    )
