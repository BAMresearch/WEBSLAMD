import os


class ConfigDevelopment:
    HOST = '127.0.0.1'
    PORT = '5001'
    SECRET_KEY = os.getenv('SECRET_KEY')
    SESSION_TYPE = 'filesystem'


class ConfigTesting:
    TESTING = True
    WTF_CSRF_ENABLED = False


class ConfigDemo:
    SECRET_KEY = os.getenv('SECRET_KEY')
    SESSION_TYPE = 'filesystem'


def get_config_obj(config_name):
    if config_name == 'development':
        return ConfigDevelopment
    elif config_name == 'testing':
        return ConfigTesting
    elif config_name == 'demo':
        return ConfigDemo
    else:
        return ConfigDevelopment
