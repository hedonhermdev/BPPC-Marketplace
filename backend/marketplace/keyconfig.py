import os


class Secrets:
    HOST_DOMAIN = "market.hedonhermdev.tech"
    HOST_IP = os.getenv('HOST_IP') 
    HOST_RESOLVER = os.getenv('HOST_RESOLVER')
    SECRET_KEY = os.getenv('SECRET_KEY') or "VERY_SECRET_SUPER_SECRET_KEY"


class PostgresDB:
    ENGINE = "django.db.backends.postgresql"
    NAME = os.getenv('POSTGRES_DB') or "marketplace"
    USER = os.getenv('POSTGRES_USER') or "userone"
    PASSWORD = os.getenv('POSTGRES_PASSWORD') or "hedonhermdev"
    HOST = os.getenv('DB_HOST') or "localhost"
    PORT = os.getenv('DB_PORT') or 5432


class Elasticsearch:
    HOSTS = str(os.getenv("SEARCH_HOST"))+":"+str(os.getenv("SEARCH_PORT")) or "localhost:9200"
