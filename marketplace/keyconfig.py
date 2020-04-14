class Secrets:
    HOST_DOMAIN = "marketplace.bits-dvm.org"
    HOST_IP = "157.245.3.147"
    HOST_RESOLVER = "www.iparv.com.br"
    SECRET_KEY = "zg(od63#s(ix=)12#f=q6asvox!o0#vm5_fu^ahsl!md&=kjxa"


class PostgresDB:
    ENGINE = "django.db.backends.postgresql"
    NAME = "marketplace"
    USER = "userone"
    PASSWORD = "hedonhermdev"
    HOST = "marketplace_db"
    PORT = "5432"


class Elasticsearch:
    HOSTS = "marketplace_search:9201"
