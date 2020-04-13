import ConfigParser

def get_access_credentials():
    config = ConfigParser.ConfigParser()
    config.read('mocking.cfg')

    return (config.get('server', 'user'), config.get('server', 'passwd'))
