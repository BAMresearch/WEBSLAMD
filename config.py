import os


class ConfigDevelopment:
    HOST = '127.0.0.1'
    PORT = '5001'
    SECRET_KEY = os.getenv('SECRET_KEY')


class ConfigTesting:
    TESTING = True
    SECRET_KEY = 'test_key'


def get_config_obj(config_name):
    if config_name == 'development':
        return ConfigDevelopment
    elif config_name == 'testing':
        return ConfigTesting
    else:
        return ConfigDevelopment
