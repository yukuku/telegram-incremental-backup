import configparser

config = configparser.ConfigParser()
config.read('config.ini', encoding='utf8')


def get_telegram_api_config():
    return config['telegram_api']

def get_db_config():
    return config['db']
