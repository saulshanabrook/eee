import datetime
import itertools
import json
import functools

import bs4
from requests_futures.sessions import FuturesSession
import requests
from urllib.parse import urljoin

BASE_URL = 'https://edge.edx.org/'


def login(email, password):
    session = FuturesSession(max_workers=20)

    adapter = requests.adapters.HTTPAdapter(pool_connections=200, pool_maxsize=200, max_retries=20)
    session.mount('https://', adapter)

    session.get('https://edge.edx.org/login').result()
    session.headers.update({
        'referer': 'https://edge.edx.org/login',
        'X-CSRFToken': session.cookies['csrftoken']
        }
    )
    session.post(
        urljoin(BASE_URL, 'login_ajax'),
        data={'email': email, 'password': password},
    ).result()
    return session


def has_next_page(soup, page_number):
    total_pages = soup.find('section', class_='discussion-user-threads')['data-num-pages']
    return int(total_pages) != page_number


def user_links(session, id_number, institution, course_num, section, page_number=1):
    print('looking for links for {} on page {}'.format(id_number, page_number))
    r = session.get(
        '{}courses/{}/{}/{}/discussion/forum/users/{}?page={}'.format(
            BASE_URL,
            institution,
            course_num,
            section,
            id_number,
            page_number
        )
    ).result()
    soup = bs4.BeautifulSoup(r.text)
    yield from extract_comment_links(soup)
    if has_next_page(soup, page_number):
        page_number += 1

        yield from user_links(session, id_number, institution, course_num, section, page_number)


def extract_comment_links(soup):
    profile_data = json.loads(soup.find('section', class_='discussion-user-threads')['data-threads'])

    for dictionary in profile_data:
        link = (
            '{0}courses/{1[course_id]}/discussion/forum/'
            '{1[commentable_id]}/threads/{1[id]}'
        ).format(BASE_URL, dictionary)
        print('found {}'.format(link))
        yield link

def process_post_response(session, r):
    print("Processing {}".format(r.url))
    soup = bs4.BeautifulSoup(r.text)
    posts = json.loads(soup.find('section', id='discussion-container')['data-threads'])
    for random_post in posts:
        if 'resp_skip' in random_post:
            r.post = random_post
            return


def get_all_posts(email, password, id_number, institution, course_num, section):
    print("Logging in")
    session = login(email, password)
    print("getting links")
    links = user_links(session, id_number, institution, course_num, section)
    post_future = functools.partial(
        session.get,
        background_callback=process_post_response)

    print("now creating futures")
    r_futures = [post_future(link) for link in links]
    print("now looking for results")
    posts = [r_future.result().post for r_future in r_futures]
    return posts



