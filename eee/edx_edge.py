import datetime
import bs4
import requests
import itertools
import json
from retrying import retry
from urllib.parse import urljoin

BASE_URL = 'https://edge.edx.org/'


def login(email, password):
    session = requests.Session()
    session.get('https://edge.edx.org/login')
    session.headers.update({
        'referer': 'https://edge.edx.org/login',
        'X-CSRFToken': session.cookies['csrftoken']
        }
    )
    session.post(
        urljoin(BASE_URL, 'login_ajax'),
        data={'email': email, 'password': password},
    )
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
    )
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


@retry(stop_max_attempt_number=2)
def link_to_post(session, link):
    r = session.get(link)
    soup = bs4.BeautifulSoup(r.text)
    posts = json.loads(soup.find('section', id='discussion-container')['data-threads'])
    for random_post in posts:
        if 'resp_skip' in random_post:
            return random_post


def get_all_posts(email, password, id_number, institution, course_num, section):
    session = login(email, password)

    links = user_links(session, id_number, institution, course_num, section)
    for link in links:
        yield link_to_post(session, link)



