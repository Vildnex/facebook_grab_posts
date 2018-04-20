FacebookDATA = {}


class FacebookGroupData:
    message = ""
    time = ""
    group_link = ""

    def __init__(self, message, time, group_link):
        self.message = message
        self.time = time
        self.group_link = group_link


def get_html_group_pages(session, email, password):
    # Attempt to login to Facebook
    response = session.post('https://m.facebook.com/login.php', data = {
        'email': email,
        'pass': password
    }, allow_redirects = False)

    # If c_user cookie is present, login was successful
    facebook_groups = []
    if 'c_user' in response.cookies:
        for group in FacebookDATA['GROUPS']:
            facebook_groups.append(session.get('https://m.facebook.com/groups/' + str(
                group)).text + "%MYSPLITER%" + 'https://m.facebook.com/groups/' + str(group))
    return facebook_groups


def get_group_data(facebook_groups):
    from bs4 import BeautifulSoup
    fb_group_data = []
    message = ""
    time = ""
    for group in facebook_groups:
        soup = BeautifulSoup(group, 'lxml')
        for article in soup.findAll("div", role = 'article'):
            for span in article.findAll("span"):
                for p in span.findAll("p"):
                    for href in p.findAll("a"):
                        message += href.text + "\n"
                        break
                    message += p.text + "\n"
            for abbr in article.findAll("abbr"):
                time = abbr.text
            if message and time:
                if message is not "\n":
                    fb_group_data.append(FacebookGroupData(message, time, group.split("%MYSPLITER%")[1]))
            message = ""
            time = ""
    return fb_group_data


def init_variables():
    import yaml

    stream = open("config.yml", "r")
    docs = yaml.load_all(stream)
    for doc in docs:
        for key, value in doc.items():
            FacebookDATA[key] = value


def write_facebook_data(data):
    import json
    data_to_json = []
    for inf in data:
        data_to_json.append({
            'link': inf.group_link,
            'message': inf.message,
            'time': inf.time
        })

    with open('data.json', 'w') as outfile:
        json.dump(data_to_json, outfile)


def run():
    import requests
    init_variables()
    session = requests.session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (X11; Linux i686; rv:39.0) Gecko/20100101 Firefox/39.0'
    })
    facebook_groups = get_html_group_pages(session, FacebookDATA['FACEBOOK_ID'], FacebookDATA['FACEBOOK_PW'])

    fb_group_data = get_group_data(facebook_groups)
    write_facebook_data(fb_group_data)


if __name__ == "__main__":
    run()
