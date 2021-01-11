

default_config = {
    "app_name": "api_project",
    "version": "0.1",
    "app_debug": True,
    "DATABASE": "instance/app.sqlite",
    "DBSchema": "schema.sql",
    "dev_port": 8080
}


class Config:

    DEBUG=False
    TESTING=False


class DevConfig(Config):

    ENV = 'development'
    SECRET_KEY = "dev"
    CONFIG = default_config 


class ProdConfig(Config):
    pass

