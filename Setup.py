import pip


def install():
    pip.main(['install', 'BeautifulSoup'])
    pip.main(['install', 'yaml'])
    pip.main(['install', 'requests'])
    pip.main(['install', 'json'])


# Example
if __name__ == '__main__':
    install()
