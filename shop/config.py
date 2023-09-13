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
class Config:
    db: DataBase
    redis: RedisDB



def config(path=None):
    env = Env()
    env.read_env(path)

    return Config(db=DataBase(name=env('DB_NAME'),
                    user=env('DB_USER'),
                    password=env('DB_PASSWORD'),
                    host=env('DB_HOST'),
                    port=env.int('DB_PORT')),
                  redis=RedisDB(host=env('REDIS_HOST'),
                                port=env.int('REDIS_PORT'),
                                db=env.int('REDIS_DB'))
                  )
