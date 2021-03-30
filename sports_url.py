import requests
from lxml import html
import re
import datetime


def get_logintoken(login_url, session_requests):
    result = session_requests.get(login_url)
    tree = html.fromstring(result.content)
    return list(set(tree.xpath("//input[@name='logintoken']/@value")))[0]


def login(session_requests):
    payload = {"username": "st119181",
               "password": "St000QsYss%",
               "logintoken": "rE4k5W4LgoOMKR7jJUFuQzQD1dJ4s18g"}
    login_url = "https://edu.stankin.ru/login/"
    payload['logintoken'] = get_logintoken(login_url, session_requests)

    result = session_requests.post(
        login_url,
        data=payload,
        headers=dict(referer=login_url)
    )
    return session_requests


def parse_result(result):
    now = datetime.datetime.now()
    p = re.compile(b'\xd0\x98\xd0\x94\xd0\x91-19-03 ')

    match = p.search(result.content)
    print(match)
    first = match.span()[0] - 54
    last = match.span()[0] - 2
    return result.content[first:last].decode("utf-8")


def get_url():
    session_requests = requests.session()
    session_requests = login(session_requests)
    url = 'https://edu.stankin.ru/mod/forum/view.php?id=140959'
    result = session_requests.get(
        url,
        headers=dict(referer=url)
    )
    print(result.status_code)
    return parse_result(result)


if __name__ == "__main__":
    print(get_url())

