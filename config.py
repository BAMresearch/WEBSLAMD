class ConfigDevelopment:
    HOST = '127.0.0.1'
    PORT = '5001'


class ConfigTesting:
    TESTING = True


def get_config_obj(config_name):
    if config_name == 'development':
        return ConfigDevelopment
    elif config_name == 'testing':
        return ConfigTesting
    else:
        return ConfigDevelopment
